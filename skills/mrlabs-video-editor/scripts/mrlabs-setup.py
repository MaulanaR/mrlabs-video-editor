"""Check runtime; --install creates this skill's virtual environment and syncs global skill folders."""
import argparse
import importlib.util
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import venv
from mrlabs_core import MRLABS_ROOT, mrlabs_tool, mrlabs_write, mrlabs_run


def mrlabs_sync_global_skills():
    home = Path.home()
    targets = [
        home / ".gemini/config/skills/mrlabs-video-editor",
        home / ".codex/skills/mrlabs-video-editor",
        home / ".claude/skills/mrlabs-video-editor",
    ]
    synced = []
    for dst in targets:
        try:
            if dst.resolve() == MRLABS_ROOT.resolve():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                MRLABS_ROOT,
                dst,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".venv", "__pycache__", "*.pyc"),
            )
            synced.append(str(dst))
        except Exception:
            continue
    return synced


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Create .venv, install dependencies, and register global skill copies.")
    parser.add_argument("--open", action="store_true", help="Open theme-gallery.html in browser after setup.")
    args = parser.parse_args()
    if args.install:
        target = MRLABS_ROOT / ".venv"
        venv.EnvBuilder(with_pip=True).create(target)
        py = target / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")
        subprocess.run([str(py), "-m", "pip", "install", "faster-whisper==1.2.1", "av<19", "Pillow>=10,<13"], check=True)
        synced = mrlabs_sync_global_skills()
        if synced:
            print("Global skill synced to:", ", ".join(synced))
        gallery_cmd = [str(py), str(MRLABS_ROOT / "scripts/mrlabs-gallery.py")]
        if args.open:
            gallery_cmd.append("--open")
        subprocess.run(gallery_cmd, check=True)
        subprocess.run([str(py), str(Path(__file__))], check=True)
        return
    tools = {}
    for name in ("ffmpeg", "ffprobe", "node"):
        try:
            tools[name] = mrlabs_tool(name)
        except RuntimeError:
            tools[name] = None
    asr = importlib.util.find_spec("faster_whisper") is not None
    pillow = importlib.util.find_spec("PIL") is not None
    node_ok = bool(tools.get("node")) and int(mrlabs_run([tools["node"], "--version"]).strip().lstrip("v").split(".")[0]) >= 22
    ready = all(tools.values()) and asr and pillow and node_ok
    record = {"os": platform.system(), "python": sys.executable, "tools": tools,
              "asr": asr, "pillow": pillow, "node_22_or_newer": node_ok, "ready": ready, "language": "id", "model": "small"}
    mrlabs_write(MRLABS_ROOT / ".platform.json", record)
    if args.open:
        subprocess.run([sys.executable, str(MRLABS_ROOT / "scripts/mrlabs-gallery.py"), "--open"], check=True)
    print(record)
    print("READY" if ready else "PARTIAL: jalankan mrlabs-setup.py --install; FFmpeg dan Node 22+ harus tersedia.")
    if not ready:
        raise SystemExit(1)


if __name__ == "__main__":
    mrlabs_main()
