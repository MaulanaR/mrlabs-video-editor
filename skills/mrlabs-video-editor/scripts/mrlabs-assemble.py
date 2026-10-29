"""Assemble reviewed edl.json from originals into a frame-indexed vertical cut."""
import argparse
import math
from pathlib import Path
from mrlabs_core import (MRLABS_ROOT, mrlabs_read, mrlabs_write, mrlabs_config, mrlabs_run,
                         mrlabs_tool, mrlabs_probe, mrlabs_frames, mrlabs_hash)


def mrlabs_validate_edl(edl, sources):
    if not edl:
        raise ValueError("EDL kosong")
    seen = set()
    for segment in edl:
        if segment["id"] in seen:
            raise ValueError("Segment id harus unik")
        seen.add(segment["id"])
        source = sources[segment["clip"]]
        start, end = float(segment["in"]), float(segment["out"])
        zoom = float(segment.get("zoom", 1))
        if not all(map(math.isfinite, (start, end, zoom))) or not 0 <= start < end <= source["duration"] + 0.02 or zoom < 1:
            raise ValueError(f"Invalid EDL range: {segment}")
        if end - start < 0.10:
            raise ValueError("Segment terlalu pendek (<0.10s)")


def mrlabs_theme_bg(theme_id):
    themes = mrlabs_read(MRLABS_ROOT / "assets/themes.json")["themes"]
    theme = next((t for t in themes if t["id"] == theme_id), themes[0])
    return theme["background"].lstrip("#")


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    config = mrlabs_config(project)
    edl, sources = mrlabs_read(project / "edl.json"), mrlabs_read(project / "sources.json")
    mrlabs_validate_edl(edl, sources)
    output_path = (project / "assets/aroll.mp4").resolve()
    for source in sources.values():
        if Path(source["path"]).resolve() == output_path:
            raise ValueError("Output assembly tidak boleh menimpa video sumber.")
        if mrlabs_hash(source["path"]) != source["sha256"]:
            raise ValueError("Sumber berubah setelah ingest; review dan register ulang pada proyek baru.")
    fps, width, height = config["fps"], config["width"], config["height"]
    if (fps, width, height) != (30, 1080, 1920):
        raise ValueError("Versi 1 memakai profil 1080x1920 30fps.")
    work, assets = project / "work" / "assembly", project / "assets"
    work.mkdir(parents=True, exist_ok=True)
    assets.mkdir(exist_ok=True)
    ffmpeg = mrlabs_tool("ffmpeg")
    bg_hex = mrlabs_theme_bg(config.get("theme", "signal-clean"))
    parts, segments, frame = [], [], 0
    for index, segment in enumerate(edl):
        source = sources[segment["clip"]]
        source_path = Path(source["path"])
        if not any(stream["codec_type"] == "audio" for stream in mrlabs_probe(source_path)["streams"]):
            raise ValueError(f"Source audio missing: {source_path.name}")
        start, end = segment["in"], segment["out"]
        duration, zoom = end - start, segment.get("zoom", 1)
        sw, sh = int(source["width"]), int(source["height"])
        is_portrait = sh > sw if config.get("portrait") is None else bool(config["portrait"])
        crop = ""
        if zoom > 1:
            cw, ch = max(2, round(sw / zoom / 2) * 2), max(2, round(sh / zoom / 2) * 2)
            cx, cy = segment.get("cx", 0.5), segment.get("cy", 0.5)
            x, y = min(max(round(cx * sw - cw / 2), 0), sw - cw), min(max(round(cy * sh - ch / 2), 0), sh - ch)
            crop = f"crop={cw}:{ch}:{x}:{y},"
        # Condition: if source video already supports portrait, fill directly without background pad.
        if is_portrait:
            vf = crop + f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},fps={fps},setpts=N/{fps}/TB"
        else:
            vf = crop + f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x{bg_hex},fps={fps},setpts=N/{fps}/TB"
        part = work / f"part-{index:03}.mkv"
        mrlabs_run([ffmpeg, "-v", "error", "-y", "-ss", start, "-i", source_path, "-t", duration,
                    "-map", "0:v:0", "-map", "0:a:0", "-vf", vf, "-af",
                    f"asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, duration-0.02)}:d=0.02",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", part])
        count = mrlabs_frames(part)
        segments.append({**segment, "src_in": start, "src_out": end, "portrait": is_portrait, "frame": frame, "frames": count})
        frame += count
        parts.append(part)
    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{part.name}'\n" for part in parts), encoding="utf-8")
    target = assets / "aroll.mp4"
    mrlabs_run([ffmpeg, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat,
                "-vf", f"setpts=N/{fps}/TB", "-r", fps, "-fps_mode", "cfr", "-af", "asetpts=PTS-STARTPTS",
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", target])
    if mrlabs_frames(target) != frame:
        raise RuntimeError("Frame mismatch: assembly ditolak sebelum tahap visual.")
    mrlabs_write(project / "segments.json", segments)
    print(f"Assembled {len(segments)} segments, {frame} frames ({frame/fps:.2f}s).")


if __name__ == "__main__":
    mrlabs_main()
