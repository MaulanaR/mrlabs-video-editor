# Paket visual — 15 Mode Pro Talking-Head & Captioning

Buka `../assets/theme-gallery.html` untuk membandingkan lima belas mode Pro Talking-Head (`01—15`), memilih dari 6 mode posisi/tipografi caption (`below-face`, `above-head`, `bottom`, `split-script`, `hierarchy-glow`, `shoulder-note`), mengaktifkan 13 efek viral (`orbit`, `ui-world`, `digital-zoom`, `headline-wall`, `pull-back-reveal`, `echo-wall`, `cover-story`, `grid-3x3`, `prompt-bar`, `grade-hud`, `side-stack`, `tactile-board`, `before-after`), menguji mode video potrait vs latar putih/hitam/kertas, dan menyalin prompt AI maupun konfigurasi JSON.

**Kondisi Video Potrait:** Jika video sumber sudah mendukung format potrait (`height > width`), latar belakang tema otomatis dinonaktifkan (`--canvas-background: transparent`, `data-portrait="true"`, tanpa padding latar di `mrlabs-assemble.py`) sehingga video potrait langsung memenuhi layar 1080×1920. Latar putih (`#FFFFFF`), kertas hangat, atau hitam (`#0A0A0A` / `#0A0A0C`) hanya dipakai ketika video belum potrait atau saat mode latar studio diaktifkan.

| No | Nama / ID | Tipografi dan palet | Subtitle & Depth Hook | Efek Bawaan Studio |
|---|---|---|---|---|
| 01 | **Creator Hook** / `obsidian-studio` (default) | Plus Jakarta Sans + IBM Plex Mono; latar hitam `#0A0A0A`, kuning `#FCE373` | Baris setup putih di atas kepala + angka kuning raksasa di belakang kepala; caption melayang di dada | `orbit` |
| 02 | **Verge Glass** / `verge-glass` | Plus Jakarta Sans + Manrope; latar hitam `#0A0A0C`, biru es `#5CC8FF` | Hook metrik biru es raksasa di belakang kepala; caption bersih di depan dada | `ui-world` |
| 03 | **Monocle Brief** / `monocle-brief` | DM Serif Display + Plus Jakarta Sans; latar putih `#FFFFFF`, hijau emerald `#6EE7B7` | Angka serif raksasa di belakang kepala; caption tajam tanpa kotak | `headline-wall` |
| 04 | **Kinfolk Linen** / `kinfolk-linen` | Instrument Serif + DM Sans; latar putih `#FFFFFF`, champagne hangat `#FDE68A` | Kata kunci serif tenang di belakang kepala; caption bersih rata tengah | `digital-zoom` |
| 05 | **Founder Slate** / `founder-slate` | Space Grotesk + DM Sans; latar putih `#FFFFFF`, biru langit `#93C5FD` | Label progres tebal di belakang kepala; caption kontras tinggi di dada | `pull-back-reveal` |
| 06 | **Neon Script** / `neon-script` | Bricolage Grotesque + Caveat; latar hitam `#0A0A0A`, neon lime `#E2FF32` | Huruf blok putih tinggi di belakang kepala + cursive script neon menyala di dada (`split-script`) | `side-stack` |
| 07 | **Echo Stack** / `echo-pulse` | Poppins + Plus Jakarta Sans; latar hitam `#0A0A0C`, coral `#FF6B4A` | Tumpukan kata berulang 5 lapis di belakang kepala dengan gradasi opacity | `echo-wall` |
| 08 | **Cover Story** / `vogue-cover` | Instrument Serif + Plus Jakarta Sans; latar hitam `#0A0A0A`, krem `#F5E6C8` | Sampul majalah serif raksasa di belakang kepala lengkap dengan edisi & barcode | `cover-story` |
| 09 | **Pixel Creator** / `pixel-creator` | IBM Plex Mono + Plus Jakarta Sans; latar hitam `#0A0A0C`, hijau lime `#A3E635` | Kombinasi font mono-pixel hijau lime & sans putih di belakang kepala | `prompt-bar` |
| 10 | **Tactile Paper** / `tactile-paper` | Fraunces + Plus Jakarta Sans + Caveat; latar kertas `#FFFFFF`, emas `#FBBF24` | Kanvas meja kertas hangat dengan caption bertingkat emas menyala (`hierarchy-glow`) | `tactile-board` |
| 11 | **3×3 Reel Matrix** / `claude-grid` | Space Grotesk + Plus Jakarta Sans; latar hitam `#0A0A0A`, terracotta `#E87B55` | Aksen tembaga Claude dengan grid 3×3 video mengelilingi presenter di tengah | `grid-3x3` |
| 12 | **Colorist HUD** / `colorist-grade` | DM Serif Display + Manrope; latar hitam `#0A0A0C`, amber `#F59E0B` | Gradasi warna moody sinematik dengan kurva Tone Curve & slider live | `grade-hud` |
| 13 | **Sticker UI Cutout** / `sticker-pop` | Poppins + Plus Jakarta Sans; latar hitam `#0A0A0C`, cyan `#38BDF8` | Garis tepi stiker putih pada cutout tubuh di depan latar UI produk gelap | `orbit` |
| 14 | **Shoulder Callout** / `shoulder-note` | Plus Jakarta Sans + DM Sans; latar putih `#FFFFFF`, emerald `#34D399` | Catatan mikro 3 baris melayang di samping bahu/pelipis + subtitle emerald (`shoulder-note`) | `digital-zoom` |
| 15 | **Before / After Stage** / `before-after-stage` | Plus Jakarta Sans + IBM Plex Mono; latar hitam `#0A0A0A`, hijau `#4ADE80` | Panggung komparasi `🔴 Before` di kiri vs `🟢 After` hero frame di kanan (`hierarchy-glow`) | `before-after` |

`assets/themes.json` menyimpan token warna, font, durasi dan rotasi. `assets/render-themes.css` menyimpan geometri yang dipakai bersama oleh renderer dan galeri. Setelah mengubah token/CSS, jalankan `python scripts/mrlabs-gallery.py` dari folder skill untuk memperbarui HTML galeri, lalu build ulang proyek video yang relevan.
