"""Bilingual contextual suggestions and checks for explicitly reviewed B-roll."""
import math
import re
from pathlib import Path
from mrlabs_core import mrlabs_duration

MRLABS_TOPICS = [
    ("ai", ["ai", "kecerdasan buatan", "chatgpt", "prompt", "artificial intelligence"],
     "Rekaman layar tindakan yang sedang dijelaskan", "AI tool prompt interface screen recording"),
    ("code", ["kode", "coding", "programming", "debug", "pemrograman"],
     "Potongan kode yang relevan beserta bagian yang disorot", "code editor debugging screen recording"),
    ("data", ["data", "spreadsheet", "excel", "laporan", "report"],
     "Tabel atau diagram dari data yang benar-benar tersedia", "spreadsheet data analysis screen recording"),
    ("automation", ["otomatis", "otomasi", "automation", "workflow"],
     "Diagram alur pemicu dan hasil otomasi", "automation workflow process diagram"),
    ("website", ["website", "situs", "landing page", "dashboard"],
     "Rekaman halaman atau fitur yang disebut", "website dashboard product walkthrough"),
    ("video", ["video", "editing", "subtitle", "caption"],
     "Timeline editor atau perbandingan sebelum-sesudah dari bahan asli", "video editing timeline captions"),
    ("finance", ["uang", "anggaran", "budget", "finance", "biaya", "cost"],
     "Diagram biaya berdasarkan angka sumber; tanpa mengarang statistik", "budget planning spreadsheet"),
    ("learning", ["belajar", "tutorial", "learning", "lesson", "panduan"],
     "Demonstrasi langkah yang sedang diajarkan", "hands on learning tutorial demonstration"),
]


def mrlabs_matches(text, phrase):
    return re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text.casefold()) is not None


def mrlabs_broll_plan(transcript):
    cues = []
    for segment in transcript["segments"]:
        text = segment["text"]
        topic = next((row for row in MRLABS_TOPICS if any(mrlabs_matches(text, term) for term in row[1])), None)
        if not topic:
            continue
        start = segment["start"]
        end = min(segment["end"], start + 4.0)
        if end - start < 0.5:
            continue
        cues.append({"id": f"broll-{len(cues)+1:02}", "start": start, "end": end,
                     "anchor": text, "topic": topic[0], "visual_goal": topic[2],
                     "queries": [f"{text} rekaman layar", topic[3]],
                     "preferred_sources": ["user-screen-recording", "user-assets", "rights-verified-web"],
                     "status": "proposed", "role": "illustration", "mode": "pip",
                     "note": "Saran berbasis kata kunci. Agen harus meninjau konteks dan mencari aset; ini belum aset siap pakai."})
    return {"schema": 1, "status": "needs-editorial-review", "cues": cues}


def mrlabs_validate_broll(cues, duration, project):
    validated, previous_end = [], 0.0
    for cue in sorted(cues, key=lambda item: item["start"]):
        start, end, offset = float(cue["start"]), float(cue["end"]), float(cue.get("source_in", 0))
        if not all(map(math.isfinite, (start, end, offset))) or not 0 <= start < end <= duration or offset < 0 or start < previous_end:
            raise ValueError("B-roll harus berada di timeline dan tidak saling tumpang tindih.")
        if cue.get("status") != "approved" or cue.get("rights_verified") is not True:
            raise ValueError("B-roll belum direview atau hak penggunaan belum diverifikasi.")
        if not cue.get("anchor") or not cue.get("source_page") or not cue.get("license"):
            raise ValueError("B-roll membutuhkan anchor, source_page dan license.")
        if cue.get("role") not in ("illustration", "evidence") or cue.get("mode", "pip") not in ("pip", "full"):
            raise ValueError("Invalid B-roll role/mode")
        asset = Path(cue["file"])
        asset = asset if asset.is_absolute() else Path(project) / asset
        asset = asset.resolve(strict=True)
        kind = "image" if asset.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp") else "video"
        if kind == "video" and offset + end - start > mrlabs_duration(asset) + 0.04:
            raise ValueError("Durasi B-roll sumber tidak cukup.")
        validated.append({**cue, "path": asset, "kind": kind})
        previous_end = end
    return validated
