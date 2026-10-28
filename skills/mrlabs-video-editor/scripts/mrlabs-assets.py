"""Fetch the curated, pinned OFL fonts and CC0 sound pack. No account required."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REF = "9862abc066c9b83bf84c3e8ed1fc2d8d48f9bbf0"
FONTS = [
    ("plusjakartasans", "Plus Jakarta Sans"), ("manrope", "Manrope"),
    ("spacegrotesk", "Space Grotesk"), ("dmsans", "DM Sans"),
    ("bricolagegrotesque", "Bricolage Grotesque"), ("fraunces", "Fraunces"),
    ("instrumentserif", "Instrument Serif"), ("dmserifdisplay", "DM Serif Display"),
    ("ibmplexmono", "IBM Plex Mono"), ("caveat", "Caveat"),
]
SOUNDS = ["click_001", "confirmation_001", "open_001", "close_001", "maximize_001",
          "minimize_001", "glitch_001", "pluck_001", "scroll_001", "switch_001"]
PACK = "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip"


def mrlabs_fetch(url):
    request = Request(url, headers={"User-Agent": "MRLabs-Video-Editor/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def mrlabs_record(path, data, **metadata):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {"file": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data), **metadata}


def mrlabs_collect():
    records, css = [], []
    for slug, family in FONTS:
        base = f"https://raw.githubusercontent.com/google/fonts/{REF}/ofl/{slug}/"
        listing = json.loads(mrlabs_fetch(f"https://api.github.com/repos/google/fonts/contents/ofl/{slug}?ref={REF}"))
        candidates = sorted(item["name"] for item in listing if item["name"].endswith(".ttf") and "Italic" not in item["name"])
        if not candidates:
            raise ValueError(f"No upright TTF: {family}")
        selected = next((name for name in candidates if "Regular" in name or "[" in name), candidates[0])
        url = base + quote(selected)
        target = ROOT / "assets" / "fonts" / f"{slug}.ttf"
        data = mrlabs_fetch(url)
        if data[:4] not in (b"\x00\x01\x00\x00", b"OTTO"):
            raise ValueError(f"Invalid font response: {family}")
        license_path = ROOT / "assets" / "fonts" / f"{slug}-OFL.txt"
        license_path.parent.mkdir(parents=True, exist_ok=True)
        license_data = mrlabs_fetch(base + "OFL.txt")
        if b"SIL OPEN FONT LICENSE" not in license_data.upper():
            raise ValueError(f"Unexpected font license: {family}")
        license_path.write_bytes(license_data)
        records.append(mrlabs_record(target, data, kind="font", family=family, id=slug, license="OFL-1.1",
                                      license_file=license_path.relative_to(ROOT).as_posix(), source_url=url,
                                      source_page=f"https://github.com/google/fonts/tree/{REF}/ofl/{slug}",
                                      upstream_filename=selected))
        variable = "[" in selected
        weight = "100 900" if variable else "400"
        css.append(f'@font-face{{font-family:"{family}";src:url("{slug}.ttf") format("truetype");font-weight:{weight};font-display:block;}}')
        print(f"FONT {family}", flush=True)
    archive_bytes = mrlabs_fetch(PACK)
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    license_data = archive.read("License.txt")
    if b"CC0" not in license_data:
        raise ValueError("Unexpected SFX license")
    license_path = ROOT / "assets" / "sfx" / "Kenney-LICENSE.txt"
    license_path.parent.mkdir(parents=True, exist_ok=True)
    license_path.write_bytes(license_data)
    for name in SOUNDS:
        entry = f"Audio/{name}.ogg"
        records.append(mrlabs_record(ROOT / "assets" / "sfx" / f"{name}.ogg", archive.read(entry),
                                      kind="sfx", id=name, creator="Kenney", license="CC0-1.0",
                                      license_file="assets/sfx/Kenney-LICENSE.txt", source_url=PACK,
                                      source_page="https://opengameart.org/content/interface-sounds",
                                      publisher_page="https://kenney.nl/assets/interface-sounds",
                                      archive_entry=entry, archive_sha256=hashlib.sha256(archive_bytes).hexdigest()))
    (ROOT / "assets" / "fonts" / "fonts.css").write_text("\n".join(css) + "\n", encoding="utf-8")
    (ROOT / "assets" / "catalog.json").write_text(json.dumps({"schema": 1, "assets": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Collected {len(FONTS)} font families and {len(SOUNDS)} SFX.")


def mrlabs_verify():
    records = json.loads((ROOT / "assets" / "catalog.json").read_text(encoding="utf-8"))["assets"]
    for record in records:
        data = (ROOT / record["file"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError(f"Hash mismatch: {record['file']}")
        if not (ROOT / record["license_file"]).is_file():
            raise ValueError(f"Missing license: {record['id']}")
    print(f"Verified {len(records)} assets and their license files.")


def mrlabs_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Download curated assets; replaces only this catalog's asset files")
    args = parser.parse_args()
    mrlabs_collect() if args.fetch else mrlabs_verify()


if __name__ == "__main__":
    mrlabs_main()
