# Paket visual — edisi 03

Buka `../assets/theme-gallery.html` untuk membandingkan sepuluh arah visual, mengganti contoh Indonesia/Inggris, memutar gerakan, dan menyalin konfigurasi. Rak font dan SFX dapat dibuka di bagian Peralatan Kreatif.

Lima tema Original tetap seperti edisi 02. Lima tema Fun ditambahkan pada edisi 03. ID teknis dipertahankan agar `project.json` lama tetap terbaca. Proyek yang di-build ulang mendapat desain sesuai ID tema yang dipilih; file HTML dan MP4 lama tidak berubah otomatis. Default tetap `signal-clean`, kini bernama Atlas Studio.

| Nama / ID kompatibel | Tipografi dan palet | Subtitle dan gerakan | Bingkai B-roll |
|---|---|---|---|
| **Atlas Studio** / `signal-clean` | Plus Jakarta Sans + IBM Plex Mono; kertas, hitam, merah vermilion | Strip putih beraksen garis merah, rata kiri, naik singkat | Bingkai persegi dengan bayangan merah |
| **Voltage Pop** / `kinetic-punch` | Bricolage Grotesque + DM Sans; biru elektrik, kuning asam | Slab kuning miring, tipografi berat, scale dengan spring | Poster miring dengan outline kuning |
| **Maison Journal** / `editorial-noir` | Instrument Serif + Manrope; ivory, wine, rose | Teks tengah dengan dua garis tipis, focus reveal | Mat galeri sempit dengan border halus |
| **Playroom** / `warm-story` | Fraunces + DM Sans + Caveat; lilac, butter, plum | Kapsul kuning, gerak naik ringan | Kartu kolase miring dengan sudut bulat |
| **Blueprint Lab** / `tech-grid` | Space Grotesk + IBM Plex Mono; navy dan cyan | Panel monospace beraksen kiri, masuk horizontal | Jendela diagram bersudut terpotong |
| **Peach Doodle** / `peach-doodle` | Fraunces + DM Sans; peach/coral, pola coretan | Balon ucapan lembut | Bingkai organik putus-putus |
| **Bubble Pop** / `bubble-pop` | Poppins Bold + Roboto; pink/lilac, pola gelembung | Kapsul bundar dengan gerak spring | Oval mengambang |
| **Groovy Mint** / `groovy-mint` | Bricolage + DM Sans; mint/lavender, gelombang retro | Kurva asimetris | Bentuk kerikil lembut |
| **Sunny Picnic** / `sunny-picnic` | Poppins Bold + Roboto; kuning, pola bunga | Tepi bertitik dan lengkungan kelopak | Bingkai melengkung lebar |
| **Orbit Candy** / `orbit-candy` | Roboto 700 + Roboto Light 300; ungu, orbit dan bintang | Kapsul ringan di panel gelap | Elips dengan garis orbit |

`assets/themes.json` menyimpan token warna, font, durasi dan rotasi. `assets/render-themes.css` menyimpan geometri yang dipakai bersama oleh renderer dan galeri. `assets/DESIGN.md` menjelaskan arah artistik. Setelah mengubah token/CSS, jalankan `python scripts/mrlabs-gallery.py` dari folder skill untuk memperbarui HTML galeri, lalu build ulang proyek video yang relevan.

Galeri adalah studi desain vektor dengan judul dan subtitle contoh. Preset render memakai video asli sebagai latar; warna latar polos di galeri tidak mengganti ruangan sumber. Ukuran judul video menyesuaikan panjang teks. B-roll full-frame memakai crossfade dan tetap memenuhi layar tanpa rotasi; bingkai khusus hanya berlaku pada insert. Judul, caption dan insert menggunakan keluarga gerakan tema yang sama. Durasi masuk dibatasi 35% dari cue yang singkat agar konten tetap terbaca. Replay galeri memakai animasi CSS lokal; produksi memakai GSAP deterministik dengan easing dari tema.

Suggested SFX tetap mengikuti pasangan pada katalog. Tambahkan hanya pada aksi yang relevan dan dengarkan bersama narasi. Pergantian tema tidak otomatis menambahkan musik atau mengubah isi/timing ucapan. Area teks mengikuti profil konservatif 1080×1920, namun posisi wajah, panjang judul, dan keterbacaan tetap perlu diperiksa pada footage sebenarnya. Ilustrasi galeri tidak membuktikan kualitas footage final.

Pola tema Fun berupa SVG lokal di dalam token CSS (tanpa unduhan gambar atau media generatif). Galeri menampilkan pola di seluruh latar; pada video asli pola hanya menjadi dekorasi margin atas/bawah, agar bagian tengah presenter tidak tertutup. Lima tema baru menggunakan placeholder tipografi untuk memperlihatkan bingkai. Tidak dibuat video contoh atau render baru untuk penambahan ini.
