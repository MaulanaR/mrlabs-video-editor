"""Sample alpha bounds for placement; this is not continuous facial tracking."""
import argparse
import io
from pathlib import Path
import subprocess
from mrlabs_core import mrlabs_read, mrlabs_write, mrlabs_tool


def mrlabs_main():
    from PIL import Image
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    rows = []
    for segment in mrlabs_read(args.project / "segments.json"):
        for fraction in (0.2, 0.5, 0.8):
            time = (segment["frame"] + segment["frames"] * fraction) / 30
            result = subprocess.run([mrlabs_tool("ffmpeg"), "-v", "error", "-c:v", "libvpx-vp9", "-ss", str(time),
                                     "-i", str(args.project / "assets/subject.webm"), "-frames:v", "1", "-vf",
                                     "alphaextract,scale=270:480", "-f", "image2pipe", "-vcodec", "png", "-"],
                                    capture_output=True, check=True)
            image = Image.open(io.BytesIO(result.stdout)).convert("L").point(lambda value: 255 if value > 128 else 0)
            bounds = image.getbbox()
            rows.append({"segment": segment["id"], "time": time, "bounds": [n*4 for n in bounds] if bounds else None})
    mrlabs_write(args.project / "head-samples.json", rows)
    print("Alpha bounds sampled; inspect face clearance manually.")


if __name__ == "__main__":
    mrlabs_main()
