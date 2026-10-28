"""Shared MR Labs project, language, process and caption utilities."""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

MRLABS_ROOT = Path(__file__).resolve().parents[1]
MRLABS_DEFAULTS = {"schema": 1, "language": "id", "model": "small", "device": "cpu",
                   "theme": "signal-clean", "fps": 30, "width": 1080, "height": 1920,
                   "keywords": ["MR Labs", "ChatGPT", "Cloudflare", "HyperFrames"],
                   "brand": "MR LABS", "credit": "by @maulanarahman_"}


def mrlabs_read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def mrlabs_write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def mrlabs_config(project):
    file = Path(project) / "project.json"
    return {**MRLABS_DEFAULTS, **(mrlabs_read(file) if file.exists() else {})}


def mrlabs_tool(name):
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f"Program belum tersedia / missing tool: {name}")
    return found


def mrlabs_run(argv, cwd=None):
    result = subprocess.run([str(arg) for arg in argv], cwd=cwd, capture_output=True,
                            encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError(f"{Path(str(argv[0])).name} exit {result.returncode}:\n{result.stderr[-5000:]}")
    return result.stdout


def mrlabs_probe(path):
    return json.loads(mrlabs_run([mrlabs_tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))


def mrlabs_duration(path):
    return float(mrlabs_probe(path)["format"]["duration"])


def mrlabs_frames(path):
    return int(mrlabs_run([mrlabs_tool("ffprobe"), "-v", "error", "-select_streams", "v:0", "-count_frames",
                           "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path]).strip())


def mrlabs_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mrlabs_language(language="id", model="small"):
    if language not in ("id", "en", "auto", "mixed"):
        raise ValueError("Bahasa harus id, en, auto, atau mixed.")
    if model.endswith(".en") and language != "en":
        raise ValueError("Model .en hanya boleh untuk bahasa Inggris eksplisit. Gunakan small/medium untuk Indonesia.")
    return {"model": model, "language": language if language in ("id", "en") else None,
            "task": "transcribe", "word_timestamps": True, "vad_filter": True,
            "multilingual": language == "mixed"}


def mrlabs_transcribe(media, language="id", model="small", device="cpu", keywords=None):
    options = mrlabs_language(language, model)
    from faster_whisper import WhisperModel
    engine = WhisperModel(options.pop("model"), device=device, compute_type="int8" if device == "cpu" else "float16")
    options["initial_prompt"] = ", ".join(keywords or []) or None
    segments, info = engine.transcribe(str(media), **options)
    rows, words = [], []
    for segment in segments:
        rows.append({"start": round(segment.start, 3), "end": round(segment.end, 3), "text": segment.text.strip()})
        for word in segment.words or []:
            words.append({"text": word.word.strip(), "start": round(word.start, 3), "end": round(word.end, 3),
                          "probability": round(word.probability, 3)})
    return {"requested_language": language, "detected_language": info.language, "model": model,
            "segments": rows, "words": words, "needs_listening_review": True}


def mrlabs_validate_words(words, duration):
    previous = 0.0
    for word in words:
        start, end = float(word["start"]), float(word["end"])
        if not all(map(math.isfinite, (start, end))) or not 0 <= start <= end <= duration + 0.06 or start < previous:
            raise ValueError(f"Timestamp subtitle tidak valid: {word}")
        if not str(word["text"]).strip():
            raise ValueError("Empty subtitle word")
        previous = start


def mrlabs_caption_groups(words, max_words=5, max_chars=32):
    groups, pending = [], []
    for word in words:
        text = " ".join(str(item["text"]) for item in pending + [word])
        gap = bool(pending and word["start"] - pending[-1]["end"] > 0.45)
        if pending and (len(pending) >= max_words or len(text) > max_chars or gap):
            groups.append({"start": pending[0]["start"], "end": pending[-1]["end"], "words": pending})
            pending = []
        pending.append(word)
        if str(word["text"]).endswith((".", "?", "!")):
            groups.append({"start": pending[0]["start"], "end": pending[-1]["end"], "words": pending})
            pending = []
    if pending:
        groups.append({"start": pending[0]["start"], "end": pending[-1]["end"], "words": pending})
    return groups


def mrlabs_srt_time(seconds):
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def mrlabs_export_srt(path, words):
    blocks = []
    for index, group in enumerate(mrlabs_caption_groups(words), 1):
        text = " ".join(word["text"] for word in group["words"])
        blocks.append(f"{index}\n{mrlabs_srt_time(group['start'])} --> {mrlabs_srt_time(group['end'])}\n{text}\n")
    Path(path).write_text("\n".join(blocks), encoding="utf-8")


def mrlabs_hf(arguments, cwd=None):
    node = Path(mrlabs_tool("node"))
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    candidates = [node.parent / "node_modules/npm/bin/npx-cli.js"]
    if npm:
        candidates.append(Path(npm).parent / "node_modules/npm/bin/npx-cli.js")
    npx = next((path for path in candidates if path.is_file()), None)
    # Some Windows npm caches contain the complete package but lack .bin shims.
    # Resolve only an exact-version package and launch its declared entry directly.
    cached_entry = None
    npm_cli = node.parent / "node_modules/npm/bin/npm-cli.js"
    if npm_cli.is_file():
        cache = Path(mrlabs_run([node, npm_cli, "config", "get", "cache"]).strip())
        for manifest in (cache / "_npx").glob("*/node_modules/hyperframes/package.json"):
            package = mrlabs_read(manifest)
            entry = manifest.parent / "bin/hyperframes.mjs"
            if package.get("version") == "0.8.34" and entry.is_file():
                cached_entry = entry
                break
    if cached_entry:
        argv = [str(node), str(cached_entry), *arguments]
    elif npx:
        argv = [str(node), str(npx), "--yes", "hyperframes@0.8.34", *arguments]
    else:
        argv = [mrlabs_tool("npx"), "--yes", "hyperframes@0.8.34", *arguments]
    # Stream progress; shell=False handles paths with spaces on Windows.
    environment = os.environ.copy()
    environment["PATH"] = os.pathsep.join([str(node.parent), str(Path(mrlabs_tool("ffmpeg")).parent), environment.get("PATH", "")])
    subprocess.run(argv, cwd=cwd, env=environment, check=True)


def mrlabs_failure(error):
    print(f"MRLABS ERROR: {error}", file=sys.stderr)
    return 1
