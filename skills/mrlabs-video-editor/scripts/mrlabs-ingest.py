"""Register explicitly selected sources, contact sheets, and ID/EN transcripts."""
import argparse
from pathlib import Path
from mrlabs_core import (MRLABS_DEFAULTS, mrlabs_config, mrlabs_write, mrlabs_probe,
                         mrlabs_run, mrlabs_tool, mrlabs_transcribe, mrlabs_hash)


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--language", choices=["id", "en", "auto", "mixed"])
    parser.add_argument("--model")
    parser.add_argument("--skip-transcription", action="store_true", help="Register only; useful with an existing transcript")
    args = parser.parse_args()
    project = args.project.resolve()
    if (project / "sources.json").exists():
        raise ValueError("Sumber proyek sudah terdaftar. Gunakan proyek baru agar pemetaan clip tetap utuh.")
    sources, report = {}, []
    config = mrlabs_config(project)
    config.update({key: value for key, value in {"language": args.language, "model": args.model}.items() if value})
    work = project / "work"
    work.mkdir(parents=True, exist_ok=True)
    for index, source in enumerate(args.sources, 1):
        source = source.resolve(strict=True)
        probe = mrlabs_probe(source)
        video = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
        if not video:
            raise ValueError(f"Video stream missing: {source}")
        duration = float(probe["format"]["duration"])
        cid = f"c{index}"
        sources[cid] = {"path": source.as_posix(), "sha256": mrlabs_hash(source), "duration": duration,
                        "width": video["width"], "height": video["height"]}
        mrlabs_run([mrlabs_tool("ffmpeg"), "-v", "error", "-y", "-i", source, "-vf",
                    f"fps=8/{duration},scale=180:-2,tile=8x1", "-frames:v", "1", work / f"{cid}-sheet.jpg"])
        if not args.skip_transcription:
            transcript = mrlabs_transcribe(source, config["language"], config["model"], config["device"], config["keywords"])
            mrlabs_write(project / f"transcript-{cid}.json", transcript)
            report.append(f"=== {cid}: {source.name} ===\n" + "\n".join(f"[{s['start']:.2f}-{s['end']:.2f}] {s['text']}" for s in transcript["segments"]))
    mrlabs_write(project / "project.json", config)
    mrlabs_write(project / "sources.json", sources)
    (project / "transcript.txt").write_text("\n\n".join(report), encoding="utf-8")
    print(f"Registered {len(sources)} sources. Review transcripts and prepare edl.json before assembly.")


if __name__ == "__main__":
    mrlabs_main()
