# Paket visual — 30 Mode Pro Talking-Head & Captioning

Buka `../assets/theme-gallery.html` untuk membandingkan tiga puluh mode Pro Talking-Head (`01—30`), memilih dari 6 mode posisi/tipografi caption (`below-face`, `above-head`, `bottom`, `split-script`, `hierarchy-glow`, `shoulder-note`), mengaktifkan 13 efek viral (`orbit`, `ui-world`, `digital-zoom`, `headline-wall`, `pull-back-reveal`, `echo-wall`, `cover-story`, `grid-3x3`, `prompt-bar`, `grade-hud`, `side-stack`, `tactile-board`, `before-after`), menguji mode video potrait vs latar putih/hitam/kertas, dan menyalin prompt AI maupun konfigurasi JSON.

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
| 16 | **Hormozi Punch** / `hormozi-punch` | Montserrat 900 + JetBrains Mono; latar hitam `#0A0A0A`, kuning `#FFEA00` & hijau `#22C55E` | Tipografi Montserrat Black super-tebal retensi tinggi di dada (`chest-float`) | `digital-zoom` |
| 17 | **Bebas Tower** / `bebas-tower` | Bebas Neue + Inter; latar hitam `#0A0A0C`, merah sinyal `#FF3B30` | Headline Bebas Neue kondensasi tinggi di belakang bahu + subtitle Inter (`hierarchy-glow`) | `echo-wall` |
| 18 | **Anton Impact** / `anton-slam` | Anton + Outfit; latar hitam `#0A0A0A`, oranye `#FF7A00` | Display Anton ekstra-padat untuk hook 3 detik pertama | `side-stack` |
| 19 | **Cupertino Keynote** / `inter-minimal` | Inter + JetBrains Mono; latar putih `#FFFFFF`, biru `#3B82F6` | Tipografi Inter presisi ala presentasi Apple dengan kartu kaca terang | `ui-world` |
| 20 | **Oswald Dispatch** / `oswald-press` | Oswald + Inter; latar hitam `#0A0A0C`, emas `#FACC15` | Kapsul berita Oswald ruang redaksi investigasi + catatan bahu (`shoulder-note`) | `headline-wall` |
| 21 | **Syne Art House** / `syne-avant` | Syne + Plus Jakarta Sans; latar hitam `#0A0A0A`, ungu `#C084FC` | Tipografi Syne eksperimental dengan caption cursive menyala (`split-script`) | `orbit` |
| 22 | **Outfit Creator** / `outfit-creator` | Outfit + Caveat; latar putih `#FFFFFF`, coral `#FB7185` | Geometri bulat Outfit ramah untuk kreator edukasi & personal branding | `tactile-board` |
| 23 | **Archivo Kinetic** / `archivo-kinetic` | Archivo + JetBrains Mono; latar hitam `#0A0A0C`, mint `#2DD4BF` | Grotesque neo-teknis Archivo untuk breakdown metrik & kecepatan | `grid-3x3` |
| 24 | **Playfair Luxury** / `playfair-luxury` | Playfair Display + Inter; latar hitam `#0A0A0A`, emas sampanye `#FDE047` | Serif kontras tinggi Playfair Display dengan kilau emas sampanye (`hierarchy-glow`) | `cover-story` |
| 25 | **JetBrains Terminal** / `jetbrains-dev` | JetBrains Mono + Inter; latar hitam `#0A0A0C`, cyan `#22D3EE` | Monospace JetBrains Mono tajam untuk AI engineer, coder & devtool | `prompt-bar` |
| 26 | **Iman Documentary** / `iman-cinema` | Bebas Neue + Montserrat; latar hitam `#0A0A0A`, tungsten amber `#F59E0B` | Estetika dokumenter bisnis sinematik hangat (`hierarchy-glow`) | `grade-hud` |
| 27 | **Productive Desk** / `abdaal-desk` | Outfit + Inter + Caveat; latar putih `#FFFFFF`, biru langit `#38BDF8` | Gaya meja studi produktif dengan coretan tangan Caveat (`split-script`) | `tactile-board` |
| 28 | **Beast Retention** / `beast-retention` | Anton + Montserrat; latar hitam `#0A0A0A`, hyper-cyan `#00F0FF` | Kombinasi Anton & Montserrat ExtraBold dengan glow cyan elektrik (`hierarchy-glow`) | `digital-zoom` |
| 29 | **Editorial Opinion** / `nyt-opinion` | Playfair Display + DM Sans; latar putih `#FFFFFF`, emas `#FBBF24` | Kolom opini dengan callout bahu bergaya dokumenter (`shoulder-note`) | `headline-wall` |
| 30 | **Agency Pitch Deck** / `agency-pitch` | Syne + Archivo; latar hitam `#0A0A0C`, acid-lime `#BEF264` | Panggung komparasi agensi kreatif untuk audit kreatif & ROAS (`hierarchy-glow`) | `before-after` |

`assets/themes.json` menyimpan token warna, font, durasi dan rotasi. `assets/render-themes.css` menyimpan geometri yang dipakai bersama oleh renderer dan galeri. Setelah mengubah token/CSS, jalankan `python scripts/mrlabs-gallery.py` dari folder skill untuk memperbarui HTML galeri, lalu build ulang proyek video yang relevan.
