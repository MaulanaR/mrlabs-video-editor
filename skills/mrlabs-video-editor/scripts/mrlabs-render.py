"""Render a reviewed composition, reject safe guides and preserve final versions."""
import argparse
from pathlib import Path
from mrlabs_core import mrlabs_read, mrlabs_hf


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--quality", choices=["draft", "standard", "high"], default="high")
    args = parser.parse_args()
    project = args.project.resolve()
    report = mrlabs_read(project / "build-report.json")
    document = (project / "index.html").read_text(encoding="utf-8")
    if report["safe_guide"] or '<div class="safe">' in document:
        raise ValueError("Preview guide aktif. Rebuild tanpa --safe sebelum render.")
    target = args.output if args.output.is_absolute() else project / args.output
    if target.exists():
        raise FileExistsError("Pilih nama versi baru; final lama tidak ditimpa.")
    target.parent.mkdir(parents=True, exist_ok=True)
    mrlabs_hf(["lint"], project)
    mrlabs_hf(["render", "--output", str(target.resolve()), "--quality", args.quality], project)


if __name__ == "__main__":
    mrlabs_main()
