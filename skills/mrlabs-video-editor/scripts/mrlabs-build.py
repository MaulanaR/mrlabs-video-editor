"""Build a data-driven MR Labs HyperFrames composition."""
import argparse
from pathlib import Path
from mrlabs_visual import mrlabs_build


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--theme")
    parser.add_argument("--safe", action="store_true", help="Preview guide only; rebuild without --safe before render")
    args = parser.parse_args()
    print(mrlabs_build(args.project, args.theme, args.safe))


if __name__ == "__main__":
    mrlabs_main()
