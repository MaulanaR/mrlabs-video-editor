"""Transcribe the assembled cut without translating; default Bahasa Indonesia."""
import argparse
from pathlib import Path
from mrlabs_core import (mrlabs_config, mrlabs_transcribe, mrlabs_write,
                         mrlabs_export_srt, mrlabs_validate_words, mrlabs_duration)


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--language", choices=["id", "en", "auto", "mixed"])
    parser.add_argument("--model")
    args = parser.parse_args()
    config = mrlabs_config(args.project)
    media = args.input or args.project / "assets" / "aroll.mp4"
    result = mrlabs_transcribe(media, args.language or config["language"], args.model or config["model"], config["device"], config["keywords"])
    mrlabs_validate_words(result["words"], mrlabs_duration(media))
    mrlabs_write(args.project / "transcript.json", result)
    mrlabs_write(args.project / "words.json", result["words"])
    mrlabs_export_srt(args.project / "captions.srt", result["words"])
    print(f"Transcribed ({result['detected_language']}); review names, timing and audio before delivery.")


if __name__ == "__main__":
    mrlabs_main()
