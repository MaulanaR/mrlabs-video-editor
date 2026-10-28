# Paket visual — edisi 02

Buka `../assets/theme-gallery.html` untuk membandingkan lima arah visual, mengganti contoh Indonesia/Inggris, memutar gerakan, dan menyalin konfigurasi. Rak font dan SFX dapat dibuka di bagian Peralatan Kreatif.

Kelima tema dibuat ulang. ID teknis dipertahankan agar `project.json` lama tetap terbaca. Proyek yang di-build ulang mendapat desain edisi 02; file HTML dan MP4 lama tidak berubah otomatis. Default tetap `signal-clean`, kini bernama Atlas Studio.

| Nama / ID kompatibel | Tipografi dan palet | Subtitle dan gerakan | Bingkai B-roll |
|---|---|---|---|
| **Atlas Studio** / `signal-clean` | Plus Jakarta Sans + IBM Plex Mono; kertas, hitam, merah vermilion | Strip putih beraksen garis merah, rata kiri, naik singkat | Bingkai persegi dengan bayangan merah |
| **Voltage Pop** / `kinetic-punch` | Bricolage Grotesque + DM Sans; biru elektrik, kuning asam | Slab kuning miring, tipografi berat, scale dengan spring | Poster miring dengan outline kuning |
| **Maison Journal** / `editorial-noir` | Instrument Serif + Manrope; ivory, wine, rose | Teks tengah dengan dua garis tipis, focus reveal | Mat galeri sempit dengan border halus |
| **Playroom** / `warm-story` | Fraunces + DM Sans + Caveat; lilac, butter, plum | Kapsul kuning, gerak naik ringan | Kartu kolase miring dengan sudut bulat |
| **Blueprint Lab** / `tech-grid` | Space Grotesk + IBM Plex Mono; navy dan cyan | Panel monospace beraksen kiri, masuk horizontal | Jendela diagram bersudut terpotong |

`assets/themes.json` menyimpan token warna, font, durasi dan rotasi. `assets/render-themes.css` menyimpan geometri yang dipakai bersama oleh renderer dan galeri. `assets/DESIGN.md` menjelaskan arah artistik. Setelah mengubah token/CSS, jalankan `python scripts/mrlabs-gallery.py` dari folder skill untuk memperbarui HTML galeri, lalu build ulang proyek video yang relevan.

Galeri adalah studi desain vektor dengan judul dan subtitle contoh. Preset render memakai video asli sebagai latar; warna latar polos di galeri tidak mengganti ruangan sumber. Ukuran judul video menyesuaikan panjang teks. B-roll full-frame memakai crossfade dan tetap memenuhi layar tanpa rotasi; bingkai khusus hanya berlaku pada insert. Judul, caption dan insert menggunakan keluarga gerakan tema yang sama. Durasi masuk dibatasi 35% dari cue yang singkat agar konten tetap terbaca. Replay galeri memakai animasi CSS lokal; produksi memakai GSAP deterministik dengan easing dari tema.

Suggested SFX tetap mengikuti pasangan pada katalog. Tambahkan hanya pada aksi yang relevan dan dengarkan bersama narasi. Pergantian tema tidak otomatis menambahkan musik atau mengubah isi/timing ucapan. Area teks mengikuti profil konservatif 1080×1920, namun posisi wajah, panjang judul, dan keterbacaan tetap perlu diperiksa pada footage sebenarnya. Ilustrasi galeri tidak membuktikan kualitas footage final.
