# MR Labs Video Editor — Pro Talking-Head & Captioning Studio

Skill AI Video Editor untuk mengubah rekaman *talking-head* asli menjadi video vertikal `1080×1920` (Reels / Shorts / TikTok) menggunakan **HyperFrames + GSAP + Faster-Whisper**, lengkap dengan **30 Mode Pro Talking-Head**, **6 Mode Posisi & Tipografi Caption**, **13 Efek Depth Viral**, **22 keluarga font OFL** (+ Helvetica lokal), dan **30 SFX CC0**.

---

## 🚀 Cara Pakai Pertama Kali (Untuk User Baru)

### Langkah 1 — Install Skill (Cukup Sekali)
Buka terminal atau chat AI Agent kamu (**Antigravity / Claude Code / Codex**), lalu ketik:

```text
Clone https://github.com/MaulanaR/mrlabs-video-editor, install skill mrlabs-video-editor beserta environment-nya, lalu buka studio HTML-nya.
```

*(Atau jika kamu sudah men-download/clone folder repo ini, cukup ketik di chat AI: **`Install skill ini dan buka studio-nya`**).*

### Langkah 2 — Panggil Skill Tanpa Konteks (Otomatis Buka Studio HTML)
Setiap kali mau mengedit video baru, kamu cukup mengetik di chat:

```text
$mrlabs-video-editor
```
*(atau `/mrlabs-video-editor` / `"buka studio mrlabs"`)*

AI akan otomatis menjalankan `python "skills/mrlabs-video-editor/scripts/mrlabs-gallery.py" --open` dan **membuka halaman Daylight Studio ([`theme-gallery.html`](skills/mrlabs-video-editor/assets/theme-gallery.html)) di browser kamu**:
1. **Pilih file video raw** langsung dari komputermu di bagian `00 / PILIH FILE VIDEO RAW` (resolusi & orientasi potrait/landscape otomatis terdeteksi, bahkan bisa langsung di-*preview* di monitor Studio).
2. **Pilih 1 dari 30 Mode Pro Talking-Head**, **6 Mode Caption**, dan **13 Efek Viral**.
3. Klik tombol **`📋 Salin Prompt Murni ke Chat ↗`** lalu *paste* langsung ke ruang chat AI Agent!

---

## 🎨 30 Mode Pro Talking-Head (`themes.json`)

| No | Mode / ID | Karakter Visual & Kegunaan | Efek Bawaan |
| :--- | :--- | :--- | :--- |
| **01** | **Creator Hook** (`obsidian-studio`) | Latar hitam `#0A0A0A`, angka kuning `#FCE373` raksasa di belakang kepala, caption dada | `orbit` |
| **02** | **Verge Glass** (`verge-glass`) | Latar hitam `#0A0A0C`, metrik biru es `#5CC8FF` di belakang subjek, review tech & AI | `ui-world` |
| **03** | **Monocle Brief** (`monocle-brief`) | Latar putih `#FFFFFF`, serif DM Serif Display, aksen hijau emerald `#6EE7B7` bisnis | `headline-wall` |
| **04** | **Kinfolk Linen** (`kinfolk-linen`) | Latar putih `#FFFFFF`, serif Instrument Serif tenang, aksen champagne `#FDE68A` | `digital-zoom` |
| **05** | **Founder Slate** (`founder-slate`) | Latar putih `#FFFFFF`, Space Grotesk tegas, aksen biru langit `#93C5FD` founder | `pull-back-reveal` |
| **06** | **Neon Script** (`neon-script`) | Header blok putih tinggi di belakang kepala + cursive script neon `#E2FF32` di dada | `side-stack` |
| **07** | **Echo Stack** (`echo-pulse`) | Tumpukan kata kunci berulang 5 lapis (`#FF6B4A`) di belakang kepala | `echo-wall` |
| **08** | **Cover Story** (`vogue-cover`) | Sampul majalah serif raksasa (`#F5E6C8`) di belakang kepala + edisi & barcode | `cover-story` |
| **09** | **Pixel Creator** (`pixel-creator`) | Kombinasi font mono hijau lime `#A3E635` & sans putih di belakang kepala | `prompt-bar` |
| **10** | **Tactile Paper** (`tactile-paper`) | Kanvas meja kertas hangat dengan caption bertingkat emas menyala (`#FBBF24`) | `tactile-board` |
| **11** | **3×3 Reel Matrix** (`claude-grid`) | Aksen tembaga Claude `#E87B55` dengan matriks 3×3 mengelilingi tile tengah | `grid-3x3` |
| **12** | **Colorist HUD** (`colorist-grade`) | Grade sinematik *moody* dengan grafik Tone Curve & slider warna di atas kepala | `grade-hud` |
| **13** | **Sticker UI Cutout** (`sticker-pop`) | Garis tepi stiker putih pada cutout tubuh di depan latar UI gelap (`#38BDF8`) | `orbit` |
| **14** | **Shoulder Callout** (`shoulder-note`) | Aksen emerald `#34D399` + catatan mikro 3 baris melayang di samping bahu/pelipis | `digital-zoom` |
| **15** | **Before / After Stage** (`before-after-stage`) | Panggung komparasi `🔴 Before` mentah di kiri vs `🟢 After` hasil edit di kanan | `before-after` |
| **16** | **Hormozi Punch** (`hormozi-punch`) | Tipografi `Montserrat` 900 super-tebal dengan aksen kuning `#FFEA00` & hijau `#22C55E` | `digital-zoom` |
| **17** | **Bebas Tower** (`bebas-tower`) | Headline `Bebas Neue` kondensasi tinggi merah `#FF3B30` di belakang bahu + `Inter` | `echo-wall` |
| **18** | **Anton Impact** (`anton-slam`) | Display `Anton` ekstra-padat untuk hook 3 detik pertama dengan oranye `#FF7A00` | `side-stack` |
| **19** | **Cupertino Keynote** (`inter-minimal`) | Tipografi `Inter` presisi ala Apple Keynote di kanvas putih `#FFFFFF` + biru `#3B82F6` | `ui-world` |
| **20** | **Oswald Dispatch** (`oswald-press`) | Kapsul berita `Oswald` ruang redaksi investigasi dengan aksen emas `#FACC15` | `headline-wall` |
| **21** | **Syne Art House** (`syne-avant`) | Tipografi `Syne` eksperimental dengan aksen ungu `#C084FC` & cursive `split-script` | `orbit` |
| **22** | **Outfit Creator** (`outfit-creator`) | Geometri bulat `Outfit` ramah di kanvas putih dengan aksen coral `#FB7185` | `tactile-board` |
| **23** | **Archivo Kinetic** (`archivo-kinetic`) | Grotesque neo-teknis `Archivo` 900 untuk breakdown metrik & kecepatan (`#2DD4BF`) | `grid-3x3` |
| **24** | **Playfair Luxury** (`playfair-luxury`) | Serif kontras tinggi `Playfair Display` dengan kilau emas sampanye `#FDE047` | `cover-story` |
| **25** | **JetBrains Terminal** (`jetbrains-dev`) | Monospace `JetBrains Mono` tajam untuk AI engineer, coder & terminal HUD (`#22D3EE`) | `prompt-bar` |
| **26** | **Iman Documentary** (`iman-cinema`) | Dokumenter bisnis hangat dengan tungsten amber `#F59E0B`, `Bebas Neue` & `Montserrat` | `grade-hud` |
| **27** | **Productive Desk** (`abdaal-desk`) | Meja studi produktif `Outfit` + coretan tangan `Caveat` di kanvas putih (`#38BDF8`) | `tactile-board` |
| **28** | **Beast Retention** (`beast-retention`) | Kombinasi `Anton` & `Montserrat` ExtraBold dengan glow cyan elektrik `#00F0FF` | `digital-zoom` |
| **29** | **Editorial Opinion** (`nyt-opinion`) | Kolom opini `Playfair Display` & `DM Sans` dengan callout bahu emas `#FBBF24` | `headline-wall` |
| **30** | **Agency Pitch Deck** (`agency-pitch`) | Panggung komparasi `Syne` & `Archivo` dengan aksen acid-lime `#BEF264` | `before-after` |

---

## ✨ 13 Efek Viral (`mrlabs_visual.py`)

- `orbit` — **ORBIT 3D Cards**: Kartu UI & metrik berputar 3D di belakang dan di depan tubuh.
- `ui-world` — **UI World Window**: Setengah atas layar menjadi window AI/aplikasi interaktif.
- `digital-zoom` — **Digital Zoom Punch-In**: Kamera *punch-in* halus `1.24×` ke wajah pada kata kunci.
- `headline-wall` — **Headline Wall**: Potongan koran & artikel menempel di dinding belakang subjek.
- `pull-back-reveal` — **Pull Back Reveal**: Kamera *zoom-out* ke antarmuka timeline desktop video editor.
- `echo-wall` — **Echo Repeat Stack**: 5 baris kata berulang di belakang kepala dengan gradasi *opacity*.
- `cover-story` — **Magazine Cover Story**: Masthead majalah raksasa + info edisi + barcode.
- `grid-3x3` — **3×3 Reel Matrix**: Video utama mengecil ke tengah grid `3×3` dikelilingi 8 video lain.
- `prompt-bar` — **AI Prompt & Tool Pills**: Kotak input prompt Claude + tombol `↑` + pill `Remotion` & `FFmpeg`.
- `grade-hud` — **Colorist Tone Curve HUD**: Panel kurva warna SVG & slider *grading* di atas kepala.
- `side-stack` — **Side Block & Starburst**: Teks blok vertikal di kiri/kanan bahu + bintang berputar.
- `tactile-board` — **Tactile Sticky & Wireframe**: Sticky note checklist kuning & kartu sketsa wireframe.
- `before-after` — **Before / After Stage**: Kartu `🔴 Before` di kiri + badge `🟢 After · Pro Edit`.

---

## 🛠️ Perintah CLI & Verifikasi Lokal

Lihat dokumentasi lengkap di [`skills/mrlabs-video-editor/SKILL.md`](skills/mrlabs-video-editor/SKILL.md) dan [`references/commands.md`](skills/mrlabs-video-editor/references/commands.md).

```powershell
# Buka Daylight Studio & Prompt Generator di browser
python skills/mrlabs-video-editor/scripts/mrlabs-gallery.py --open

# Verifikasi integritas 22 aset font & SFX + jalankan unit test
python skills/mrlabs-video-editor/scripts/mrlabs-assets.py
python -m unittest discover -s skills/mrlabs-video-editor/tests -v
```
