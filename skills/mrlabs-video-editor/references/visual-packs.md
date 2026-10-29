# Paket visual — edisi 04

Buka `../assets/theme-gallery.html` untuk membandingkan lima belas arah visual, mengganti contoh Indonesia/Inggris, menguji mode video potrait vs latar putih/hitam, memutar gerakan, dan menyalin konfigurasi. Rak font dan SFX dapat dibuka di bagian Peralatan Kreatif.

Lima tema Original tetap seperti edisi 02, lima tema Fun dari edisi 03 tetap utuh, dan lima tema Pro Influencer berlatar **Putih (`#FFFFFF`)** dan **Hitam (`#0A0A0C` / `#0A0A0A`)** ditambahkan pada edisi 04 untuk kreator profesional yang menginginkan tampilan bersih, berwibawa, dan tidak norak.

**Kondisi Video Potrait:** Jika video sumber sudah mendukung format potrait (`height > width`), latar belakang tema otomatis dinonaktifkan (`--canvas-background: transparent`, `data-portrait="true"`, tanpa padding latar di `mrlabs-assemble.py`) sehingga video potrait langsung memenuhi layar 1080×1920. Latar putih/hitam hanya dipakai ketika video belum potrait (misalnya landscape/square) atau saat pratinjau galeri.

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
| **Verge Glass** / `verge-glass` | Plus Jakarta Sans + Manrope + IBM Plex Mono; latar hitam `#0A0A0C`, putih, biru es | Dock gelap beraksen kiri biru es, naik presisi | Kartu bento gelap bersudut 24px |
| **Monocle Brief** / `monocle-brief` | DM Serif Display + Plus Jakarta Sans; latar putih `#FFFFFF`, hitam `#111111`, hijau emerald | Panel briefing bergaris ganda, focus reveal | Bingkai kolom pers dengan bayangan hijau |
| **Kinfolk Linen** / `kinfolk-linen` | Instrument Serif + DM Sans; latar putih `#FFFFFF`, alabaster, perunggu | Kartu putih tenang rata tengah, dissolve halus | Mat atelier bersudut lembut dengan garis perunggu |
| **Obsidian Studio** / `obsidian-studio` | Fraunces + Manrope + Space Grotesk; latar hitam `#0A0A0A`, grafit, champagne gold | Pelat sinematik beraksen emas di bawah, slide horizontal | Bingkai dokumenter letterbox beraksen emas |
| **Founder Slate** / `founder-slate` | Space Grotesk + DM Sans + IBM Plex Mono; latar putih `#FFFFFF`, karbon `#0F172A`, biru kobalt | Kartu eksekutif putih beraksen biru kobalt, naik cepat | Kartu pitch-deck bersih dengan bar atas biru |

`assets/themes.json` menyimpan token warna, font, durasi dan rotasi. `assets/render-themes.css` menyimpan geometri yang dipakai bersama oleh renderer dan galeri. `assets/DESIGN.md` menjelaskan arah artistik. Setelah mengubah token/CSS, jalankan `python scripts/mrlabs-gallery.py` dari folder skill untuk memperbarui HTML galeri, lalu build ulang proyek video yang relevan.

Galeri adalah studi desain vektor dengan judul dan subtitle contoh. Preset render memakai video asli sebagai latar; jika video sumber sudah mendukung potrait (`height > width`), latar belakang tema tidak ditampilkan. Ukuran judul video menyesuaikan panjang teks. B-roll full-frame memakai crossfade dan tetap memenuhi layar tanpa rotasi; bingkai khusus hanya berlaku pada insert. Judul, caption dan insert menggunakan keluarga gerakan tema yang sama. Durasi masuk dibatasi 35% dari cue yang singkat agar konten tetap terbaca. Replay galeri memakai animasi CSS lokal; produksi memakai GSAP deterministik dengan easing dari tema.

Suggested SFX tetap mengikuti pasangan pada katalog. Tambahkan hanya pada aksi yang relevan dan dengarkan bersama narasi. Pergantian tema tidak otomatis menambahkan musik atau mengubah isi/timing ucapan. Area teks mengikuti profil konservatif 1080×1920, namun posisi wajah, panjang judul, dan keterbacaan tetap perlu diperiksa pada footage sebenarnya. Ilustrasi galeri tidak membuktikan kualitas footage final.
