"""Optional subject cutout; only run when a chosen visual needs depth layering."""
import argparse
from pathlib import Path
from mrlabs_core import mrlabs_hf, mrlabs_frames


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    mrlabs_hf(["remove-background", "assets/aroll.mp4", "-o", "assets/subject.webm", "--quality", "best"], project)
    if mrlabs_frames(project / "assets/aroll.mp4") != mrlabs_frames(project / "assets/subject.webm"):
        raise RuntimeError("Frame count berbeda; jangan pakai cutout ini.")
    print("Cutout frame count verified. Inspect hair/hands and movement before using it.")


if __name__ == "__main__":
    mrlabs_main()
