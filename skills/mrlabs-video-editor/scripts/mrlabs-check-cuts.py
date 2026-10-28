"""Extract final-render cut evidence, including single-segment projects."""
import argparse
from pathlib import Path
import re
from mrlabs_core import mrlabs_read, mrlabs_write, mrlabs_run, mrlabs_tool, mrlabs_probe, mrlabs_frames


def mrlabs_main():
    from PIL import Image
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("render", type=Path)
    parser.add_argument("--phone", action="store_true")
    args = parser.parse_args()
    segments = mrlabs_read(args.project / "segments.json")
    expected = sum(segment["frames"] for segment in segments)
    actual = mrlabs_frames(args.render)
    evidence = args.project / "work/final-qa"
    evidence.mkdir(parents=True, exist_ok=True)
    cuts = sorted({number for segment in segments[1:] for number in (segment["frame"]-1, segment["frame"])})
    if not cuts:
        cuts = sorted({0, max(0, actual//2), max(0, actual-1)})
    images = []
    for number in cuts:
        target = evidence / f"frame-{number:06}.png"
        mrlabs_run([mrlabs_tool("ffmpeg"), "-v", "error", "-y", "-i", args.render, "-vf",
                    f"select=eq(n\\,{number}),scale=240:-2", "-frames:v", "1", target])
        with Image.open(target) as image:
            images.append(image.convert("RGB").copy())
    columns = min(6, len(images))
    sheet = Image.new("RGB", (240*columns, images[0].height*((len(images)+columns-1)//columns)), "#181818")
    for index, image in enumerate(images):
        sheet.paste(image, ((index % columns)*240, (index//columns)*image.height))
    sheet.save(evidence / "cut-check.jpg")
    streams = mrlabs_probe(args.render)["streams"]
    audio = any(stream["codec_type"] == "audio" for stream in streams)
    peak = None
    if audio:
        import subprocess
        process = subprocess.run([mrlabs_tool("ffmpeg"), "-hide_banner", "-i", str(args.render), "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, encoding="utf-8", errors="replace", check=True)
        match = re.search(r"max_volume: ([\-\w.]+) dB", process.stderr)
        peak = match.group(1) if match else None
    mrlabs_write(evidence / "report.json", {"expected_frames":expected,"actual_frames":actual,"frames_match":actual==expected,
                                            "audio_present":audio,"audio_peak_db":peak,"sample_frames":cuts,
                                            "manual_visual_review":"pending","manual_listening_review":"pending"})
    if actual != expected or not audio:
        raise RuntimeError("Final QA structural check failed; inspect report.json")
    if args.phone:
        target = args.render.with_name(args.render.stem + "-phone.mp4")
        mrlabs_run([mrlabs_tool("ffmpeg"), "-v", "error", "-y", "-i", args.render, "-vf", "scale=720:-2",
                    "-c:v", "libx264", "-crf", "26", "-c:a", "aac", "-movflags", "+faststart", target])
    print(f"Frame and audio structure checked. LOOK at {evidence / 'cut-check.jpg'} and LISTEN before marking complete.")


if __name__ == "__main__":
    mrlabs_main()
