"""Propose anchored ID/EN B-roll search briefs; never fabricate downloaded assets."""
import argparse
from pathlib import Path
from mrlabs_core import mrlabs_read, mrlabs_write
from mrlabs_broll import mrlabs_broll_plan


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    proposal = mrlabs_broll_plan(mrlabs_read(args.project / "transcript.json"))
    mrlabs_write(args.project / "broll-proposals.json", proposal)
    print(f"{len(proposal['cues'])} contextual briefs. Review meaning, search sources, then record approved assets in broll.json.")


if __name__ == "__main__":
    mrlabs_main()
