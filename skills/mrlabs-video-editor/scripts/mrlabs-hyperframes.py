"""Run the pinned HyperFrames CLI using the current Node runtime."""
import sys
from mrlabs_core import mrlabs_hf


def mrlabs_main():
    mrlabs_hf(sys.argv[1:])


if __name__ == "__main__":
    mrlabs_main()
