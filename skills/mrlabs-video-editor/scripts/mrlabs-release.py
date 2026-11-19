"""Build a clean, commercial-ready .zip distribution package for buyers (Lynk.id / Mayar / Gumroad)."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import zipfile

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parent.parent

EXCLUDED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".playwright-cli", "node_modules", ".hyperframes", "projects", "output", "dist"}
EXCLUDED_FILES = {".platform.json", "config.local.json", ".DS_Store", "Thumbs.db"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".log"}

BUYER_GUIDE_MD = """# 🎬 MR Labs Video Editor Pro — Panduan Pembeli

Terima kasih telah membeli **MR Labs Video Editor Pro (Daylight Studio Edition)**!
Paket ini berisi **40 Mode Visual (30 Pro Talking-Head + 10 Kinetic & Camera Lab dengan posisi teks berubah-ubah & gerakan kamera otomatis)**, **7 Mode Layout Caption**, **18 Efek Depth & Kinetic Viral**, **23 Keluarga Font OFL** (termasuk **Arimo / Helvetica Twin**), dan **30 SFX Antarmuka**.

---

## 🚀 Cara Install (Cukup Sekali — Pilih Salah Satu)

### Cara A — Lewat Chat AI Agent (Paling Mudah)
1. Ekstrak file `.zip` ini ke folder mana saja di komputermu (misal: `D:\\mrlabs-video-editor-pro`).
2. Buka folder tersebut di **Antigravity / Claude Code / Cursor / Codex**.
3. Ketik perintah ini di ruang chat AI:
   ```text
   Install skill ini dan buka studio-nya
   ```
4. Selesai! AI akan otomatis meng-install *environment*, mendaftarkan skill `$mrlabs-video-editor` secara global di komputermu, dan membuka **Daylight Studio (`theme-gallery.html`)** di browser.

### Cara B — Klik 2× File Shortcut (Khusus Windows)
- Klik 2× **`INSTALL-DAN-BUKA-STUDIO.bat`** untuk meng-install *environment* Python + mendaftarkan skill + membuka Studio di browser.
- Atau klik 2× **`BUKA-STUDIO.bat`** jika hanya ingin langsung membuka halaman Studio & Prompt Generator di browser.

---

## ✨ Cara Pakai Sehari-hari untuk Edit Video

Setiap kali kamu ingin mengedit video baru:

1. **Buka Studio:**
   Ketik di chat AI:
   ```text
   $mrlabs-video-editor
   ```
   *(atau klik 2× file `BUKA-STUDIO.bat` / buka `skills/mrlabs-video-editor/assets/theme-gallery.html` di browser).*

2. **Atur di Halaman Daylight Studio:**
   - **00 / Pilih File Video Raw:** Klik `📂 Pilih Video...` dan pilih video mentahmu (`.mp4` / `.mov` / `.mkv`). Resolusi & orientasi potrait/landscape akan terdeteksi otomatis.
   - **01 / Pilih Mode Pro Talking-Head:** Pilih 1 dari **30 Mode Visual** (`Creator Hook`, `Hormozi Punch`, `Neon Script`, `Cover Story`, `3×3 Reel Matrix`, `Iman Documentary`, `Beast Retention`, dll.).
   - **02 / Pilih Posisi Caption:** Pilih 1 dari **6 Mode Caption** (`Di Bawah Muka`, `Di Atas Kepala`, `Di Bawah Frame`, `Split Script Neon`, `Hierarchy Glow`, `Shoulder Callout`).
   - **04 / Pilih Efek Viral:** Centang efek yang diinginkan dari **13 Efek Viral**.

3. **Salin & Tempel Prompt Murni:**
   Klik tombol **`📋 Salin Prompt Murni ke Chat ↗`** di bagian `05`, lalu *paste* langsung ke ruang chat AI Agent kamu. AI akan mengerjakan pemotongan klip, transkripsi kata-per-kata, komposisi visual, hingga render `.mp4` akhir secara otomatis!

---

## 📋 Prasyarat Sistem (Untuk Render Video Penuh)
- **Python 3.10+** (https://python.org)
- **Node.js 22+** (https://nodejs.org)
- **FFmpeg & ffprobe** terinstal di `PATH` sistem
"""

BUKA_STUDIO_BAT = """@echo off
chcp 65001 >nul
title MR Labs Video Editor Pro — Buka Studio
cd /d "%~dp0"
python "skills\\mrlabs-video-editor\\scripts\\mrlabs-setup.py" --open
if errorlevel 1 (
    start "" "%~dp0skills\\mrlabs-video-editor\\assets\\theme-gallery.html"
)
"""

INSTALL_STUDIO_BAT = """@echo off
chcp 65001 >nul
title MR Labs Video Editor Pro — Installer & Studio Launcher
cd /d "%~dp0"
echo ============================================================
echo   MR LABS VIDEO EDITOR PRO — INSTALLER ^& STUDIO LAUNCHER
echo ============================================================
echo.
python "skills\\mrlabs-video-editor\\scripts\\mrlabs-setup.py" --install --open
echo.
echo Selesai! Halaman Daylight Studio telah dibuka di browser Anda.
pause
"""


def mrlabs_should_include(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return False
    if path.name in EXCLUDED_FILES:
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return True


def mrlabs_build_release(output_path: Path = None) -> dict:
    # 1. Verify assets & rebuild gallery HTML first so package is always fresh
    subprocess.run([sys.executable, str(SKILL_ROOT / "scripts" / "mrlabs-assets.py")], check=True)
    subprocess.run([sys.executable, str(SKILL_ROOT / "scripts" / "mrlabs-gallery.py")], check=True)

    target = output_path or (REPO_ROOT / "dist" / "mrlabs-video-editor-pro.zip")
    target = Path(target).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    file_count = 0
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # Add buyer guide & 1-click launchers at root of zip
        zf.writestr("CARA-PAKAI-PEMBELI.md", BUYER_GUIDE_MD)
        zf.writestr("BUKA-STUDIO.bat", BUKA_STUDIO_BAT.replace("\n", "\r\n"))
        zf.writestr("INSTALL-DAN-BUKA-STUDIO.bat", INSTALL_STUDIO_BAT.replace("\n", "\r\n"))
        file_count += 3

        # Add all clean files inside skills/mrlabs-video-editor
        for item in sorted(SKILL_ROOT.rglob("*")):
            if not item.is_file():
                continue
            rel_to_skill = item.relative_to(SKILL_ROOT)
            if not mrlabs_should_include(rel_to_skill):
                continue
            arcname = (Path("skills") / "mrlabs-video-editor" / rel_to_skill).as_posix()
            zf.write(item, arcname)
            file_count += 1

    data = target.read_bytes()
    info = {
        "package": str(target),
        "files": file_count,
        "bytes": len(data),
        "size_mb": round(len(data) / (1024 * 1024), 2),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    print(f"Built buyer package: {info['package']}")
    print(f"Files: {info['files']} | Size: {info['size_mb']} MB | SHA256: {info['sha256'][:16]}...")
    return info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Custom output .zip path (default: dist/mrlabs-video-editor-pro.zip)")
    args = parser.parse_args()
    mrlabs_build_release(Path(args.output) if args.output else None)
