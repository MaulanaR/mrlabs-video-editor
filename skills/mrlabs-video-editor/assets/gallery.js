let selected = 'obsidian-studio';
let language = 'id';
let forceNonPortrait = false;
let captionPos = 'below-face';
let activeEffects = new Set();

const FX_LABELS = {
  'orbit': 'ORBIT 3D Cards (kartu UI/metrik berputar di belakang & depan badan)',
  'ui-world': 'UI World Window (window aplikasi/AI interaktif di bagian atas)',
  'digital-zoom': 'Digital Zoom Punch-In (zoom halus 1.24x ke wajah pada kata kunci)',
  'headline-wall': 'Headline Wall (kliping berita/artikel menempel di dinding belakang badan)',
  'pull-back-reveal': 'Pull Back Reveal (zoom-out ke tampilan timeline desktop video editor)'
};

const POS_LABELS = {
  'below-face': 'Di bawah muka / di depan dada (below-face / chest-float, Y: 1050px)',
  'above-head': 'Di atas kepala presenter (above-head, Y: 310px)',
  'bottom': 'Di bagian bawah frame (bottom, Y: 1265px)'
};

const configInput = document.querySelector('#config');
const promptOutput = document.querySelector('#prompt-output');
const statusEl = document.querySelector('.status');
const studioFrame = document.querySelector('#studio-frame');
const studioBadge = document.querySelector('#studio-badge');
const selectedThemeLabel = document.querySelector('#selected-theme-label');
const allFrames = () => [...document.querySelectorAll('iframe')];

document.fonts.load('400 28px "Helvetica"').then(faces => {
  const el = document.querySelector('#helvetica-status');
  if (el) {
    el.textContent = faces.length
      ? 'Helvetica lokal tersedia. File font tidak dibundel.'
      : 'Helvetica belum tersedia; contoh ini memakai Roboto.';
  }
}).catch(() => {
  const el = document.querySelector('#helvetica-status');
  if (el) el.textContent = 'Helvetica belum tersedia; contoh ini memakai Roboto.';
});

function syncFrameState(frame, isStudio = false) {
  const doc = frame.contentDocument;
  if (!doc?.documentElement) return;
  doc.documentElement.lang = language;
  doc.querySelectorAll('[data-id]').forEach(el => {
    el.textContent = el.dataset[language];
  });
  const main = doc.querySelector('#main');
  if (!main) return;
  main.dataset.portrait = forceNonPortrait ? 'false' : 'true';
  main.dataset.captionPos = captionPos;
  ['orbit', 'ui-world', 'digital-zoom', 'headline-wall', 'pull-back-reveal'].forEach(fx => {
    if (activeEffects.has(fx)) {
      main.setAttribute(`data-fx-${fx}`, 'true');
    } else {
      main.removeAttribute(`data-fx-${fx}`);
    }
  });
}

function syncAllFrames() {
  allFrames().forEach(frame => syncFrameState(frame, frame === studioFrame));
}

function buildPromptText() {
  const spec = (window.__MRLABS_SPECIMENS && window.__MRLABS_SPECIMENS[selected]) || { name: selected, background: '#0A0A0A' };
  const fxArray = [...activeEffects];
  const creatorHook = selected === 'obsidian-studio';
  const themeName = creatorHook ? 'Obsidian Studio' : spec.name;
  const positions = {
    id: { 'above-head': 'di atas kepala saya', 'below-face': 'di bawah muka saya / di depan dada', bottom: 'di bagian bawah frame' },
    en: { 'above-head': 'above my head', 'below-face': 'below my face / across my chest', bottom: 'in the lower part of the frame' }
  };
  const effects = {
    orbit: 'ORBIT 3D Cards', 'ui-world': 'UI World Window',
    'digital-zoom': 'Digital Zoom Punch-In', 'headline-wall': 'Headline Wall',
    'pull-back-reveal': 'Pull Back Reveal'
  };
  const effectNames = fxArray.map(fx => effects[fx] || fx).join(', ');

  const payload = {
    theme: selected,
    caption_position: captionPos,
    effects: fxArray,
    portrait: !forceNonPortrait,
    language
  };
  configInput.value = JSON.stringify(payload);

  const posShort = captionPos === 'below-face' ? 'Di Bawah Muka' : (captionPos === 'above-head' ? 'Di Atas Kepala' : 'Di Bawah Frame');
  if (studioBadge) {
    studioBadge.textContent = `${spec.name} · ${posShort}${fxArray.length ? ` · +${fxArray.length} FX` : ''}`;
  }
  if (selectedThemeLabel) {
    selectedThemeLabel.textContent = `${spec.name} (${selected})`;
  }

  if (language === 'en') {
    return [
      'Edit my talking-head video using the `$mrlabs-video-editor` skill.',
      '',
      'Video file: [enter the video file path]',
      'Instagram profile: [enter the profile image path, if available]',
      'Visual reference: [attach the reference image, if available]',
      '',
      `Use the **${themeName}** theme (\`${selected}\`)${creatorHook ? ' with captions in the *Creator Hook* reference style' : ''}:`,
      '',
      `- Place bold, white conversational captions ${positions.en[captionPos]}. Use short, readable phrases timed to the actual speech.`,
      `- At important moments, show **very large ${creatorHook ? 'yellow' : `theme-accent (${spec.accent || spec.background})`} keywords** below the conversational captions. Select words actually spoken; “EDIT AI”, “ORBIT”, and “FOLLOW” are examples only, and must not be inserted if absent from the speech.`,
      '- Place the large keywords **behind my head and body** using a subject cutout, so my head naturally occludes part of the letters. Keep the keywords readable and preserve my original face and recorded voice. Check mask edges and movement in the final video.',
      forceNonPortrait
        ? `- Place the subject cutout over the selected theme background (${spec.background}).`
        : '- Keep the original video background when the source is already vertical. For other aspect ratios, plan the reframing and theme background around the subject.',
      '- Do not add numbers, statistics, or claims that I did not say. Treat preview text, metrics, and UI as illustrations, never as factual source material.',
      `- Keep effects clear of my face and captions.${fxArray.length ? ` Use ${effectNames} when the corresponding feature is discussed; space the effects across relevant moments rather than showing all at once.` : ' Do not add optional effects; focus on typography and keyword depth.'}`,
      '- Show the supplied Instagram profile during the follow call to action. If the image or call to action is absent, flag it in the plan instead of inventing profile details or speech.',
      '- Use the attached reference image to check composition, relative text size, color, and occlusion. Adapt placement to my actual head position; the gallery preview alone does not guarantee an identical result.',
      '',
      'Review the transcript and propose a timestamped edit plan first, including the exact phrases, keywords, selected effects, and missing assets. Wait for my approval before production. Then deliver the full-quality video, a lightweight phone version, and an SRT subtitle file.'
    ].join('\n');
  }

  return [
    'Edit video talking-head saya menggunakan skill `$mrlabs-video-editor`.',
    '',
    'File video: [masukkan lokasi file video]',
    'Profil Instagram: [masukkan lokasi gambar profil, jika ada]',
    'Referensi visual: [lampirkan gambar referensi, jika ada]',
    '',
    `Gunakan tema **${themeName}** (\`${selected}\`)${creatorHook ? ' dengan gaya caption seperti referensi *Creator Hook*' : ''}:`,
    '',
    `- Letakkan caption percakapan berwarna putih, tebal, ${positions.id[captionPos]}. Gunakan potongan frasa pendek yang mengikuti waktu ucapan dan mudah dibaca.`,
    `- Pada bagian penting, tampilkan **kata kunci ${creatorHook ? 'berwarna kuning' : `berwarna aksen tema (${spec.accent || spec.background})`} dengan ukuran sangat besar** di bawah caption percakapan. Pilih kata kunci dari isi ucapan; “EDIT AI”, “ORBIT”, atau “FOLLOW” hanya contoh, jangan dimasukkan jika tidak diucapkan.`,
    '- Tempatkan kata besar **di belakang kepala dan badan saya** menggunakan cutout subjek, sehingga sebagian huruf tertutup secara alami oleh kepala. Pastikan kata tetap terbaca dan pertahankan wajah serta suara asli. Periksa tepi cutout dan pergerakannya pada hasil video.',
    forceNonPortrait
      ? `- Gunakan latar belakang tema (${spec.background}) di belakang cutout subjek sesuai pilihan saya.`
      : '- Gunakan latar asli video jika sumber sudah vertikal. Untuk rasio lain, rencanakan penyesuaian framing dan latar tema dengan memperhatikan posisi subjek.',
    '- Jangan tambahkan angka, statistik, atau klaim yang tidak saya ucapkan. Teks, metrik, dan UI di preview hanya ilustrasi, bukan sumber fakta untuk video.',
    `- Sesuaikan posisi efek agar tidak menutupi wajah atau bertabrakan dengan caption.${fxArray.length ? ` Gunakan efek ${effectNames} pada saat fitur tersebut dibahas; sebarkan pada momen yang relevan, bukan ditampilkan sekaligus.` : ' Tanpa efek tambahan; fokus pada tipografi dan kedalaman kata kunci.'}`,
    '- Tampilkan profil Instagram yang saya berikan pada bagian ajakan follow. Jika gambar atau ajakan follow tidak tersedia, catat dalam rencana tanpa mengarang identitas profil atau ucapan.',
    '- Gunakan gambar referensi yang dilampirkan untuk memeriksa komposisi, perbandingan ukuran teks, warna, dan bagian huruf yang tertutup subjek. Sesuaikan posisi dengan kepala saya di video; preview galeri saja tidak menjamin hasil identik.',
    '',
    'Tinjau transkrip dan susun rencana edit bertimestamp terlebih dahulu, termasuk frasa persis, kata kunci, efek terpilih, dan aset yang belum tersedia. Tunggu persetujuan saya sebelum produksi. Setelah saya setujui, lanjutkan produksi dan berikan video kualitas penuh, versi ringan untuk ponsel, serta file subtitle SRT.'
  ].join('\n');
}

function updateUI() {
  if (promptOutput) {
    promptOutput.value = buildPromptText();
  }
  document.querySelectorAll('.pick').forEach(btn => {
    const isSel = btn.dataset.theme === selected;
    btn.setAttribute('aria-pressed', String(isSel));
    btn.firstChild.textContent = isSel ? 'Terpilih' : 'Pilih tema';
  });
  document.querySelectorAll('.theme-chip').forEach(chip => {
    chip.setAttribute('aria-pressed', String(chip.dataset.theme === selected));
  });
  document.querySelectorAll('.pos-chip').forEach(chip => {
    chip.setAttribute('aria-pressed', String(chip.dataset.pos === captionPos));
  });
  document.querySelectorAll('.bg-chip').forEach(chip => {
    const isStudioBg = chip.dataset.bgMode === 'studio';
    chip.setAttribute('aria-pressed', String(isStudioBg === forceNonPortrait));
  });
  const portraitBtn = document.querySelector('#portrait');
  if (portraitBtn) {
    portraitBtn.setAttribute('aria-pressed', String(forceNonPortrait));
    portraitBtn.textContent = forceNonPortrait
      ? 'Latar: Putih/Hitam Tema (Non-Potrait)'
      : 'Latar: Potrait Asli (Tanpa BG)';
  }
  syncAllFrames();
}

function selectTheme(themeId, scrollStudio = false) {
  selected = themeId;
  const spec = window.__MRLABS_SPECIMENS && window.__MRLABS_SPECIMENS[themeId];
  if (spec && studioFrame) {
    studioFrame.srcdoc = spec.srcdoc;
  }
  updateUI();
  if (scrollStudio) {
    document.querySelector('.studio-builder')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

const resize = new ResizeObserver(entries => entries.forEach(({ target }) => {
  const iframe = target.querySelector('iframe');
  if (iframe) iframe.style.transform = `scale(${target.clientWidth / 1080})`;
}));
document.querySelectorAll('.screen').forEach(screen => resize.observe(screen));

allFrames().forEach(frame => frame.addEventListener('load', () => syncFrameState(frame, frame === studioFrame)));

document.querySelectorAll('.pick').forEach(button => button.addEventListener('click', () => {
  selectTheme(button.dataset.theme, true);
  if (statusEl) statusEl.textContent = `Tema ${button.dataset.theme} dimuat ke Studio`;
}));

document.querySelectorAll('.theme-chip').forEach(chip => chip.addEventListener('click', () => {
  selectTheme(chip.dataset.theme, false);
  if (statusEl) statusEl.textContent = `Tema ${chip.dataset.theme} aktif`;
}));

document.querySelectorAll('.pos-chip').forEach(chip => chip.addEventListener('click', () => {
  captionPos = chip.dataset.pos;
  updateUI();
  if (statusEl) statusEl.textContent = `Posisi caption: ${captionPos}`;
}));

document.querySelectorAll('.bg-chip').forEach(chip => chip.addEventListener('click', () => {
  forceNonPortrait = chip.dataset.bgMode === 'studio';
  updateUI();
}));

document.querySelectorAll('.fx-toggle').forEach(checkbox => checkbox.addEventListener('change', () => {
  const fx = checkbox.value;
  if (checkbox.checked) {
    activeEffects.add(fx);
  } else {
    activeEffects.delete(fx);
  }
  checkbox.closest('.fx-chip')?.classList.toggle('active', checkbox.checked);
  updateUI();
  if (statusEl) {
    statusEl.textContent = activeEffects.size
      ? `${activeEffects.size} efek aktif: ${[...activeEffects].join(', ')}`
      : 'Semua efek tambahan dimatikan';
  }
}));

document.querySelector('#clear-fx')?.addEventListener('click', () => {
  activeEffects.clear();
  document.querySelectorAll('.fx-toggle').forEach(cb => {
    cb.checked = false;
    cb.closest('.fx-chip')?.classList.remove('active');
  });
  updateUI();
  if (statusEl) statusEl.textContent = 'Efek di-reset';
});

document.querySelector('#language')?.addEventListener('click', () => {
  language = language === 'id' ? 'en' : 'id';
  document.querySelector('#language').textContent = language === 'id' ? 'Contoh: Indonesia' : 'Sample: English';
  updateUI();
});

document.querySelector('#portrait')?.addEventListener('click', () => {
  forceNonPortrait = !forceNonPortrait;
  updateUI();
});

document.querySelector('#replay')?.addEventListener('click', () => {
  allFrames().forEach(frame => frame.contentDocument?.body.classList.remove('replay'));
  requestAnimationFrame(() => requestAnimationFrame(() => {
    allFrames().forEach(frame => frame.contentDocument?.body.classList.add('replay'));
  }));
});

document.querySelector('#copy-prompt')?.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(promptOutput.value);
    if (statusEl) statusEl.textContent = '✓ Prompt AI berhasil disalin!';
  } catch {
    promptOutput.select();
    if (statusEl) statusEl.textContent = 'Tekan Ctrl+C untuk menyalin prompt';
  }
});

document.querySelector('#copy')?.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(configInput.value);
    if (statusEl) statusEl.textContent = '✓ Config JSON berhasil disalin!';
  } catch {
    configInput.select();
    if (statusEl) statusEl.textContent = 'Tekan Ctrl+C untuk menyalin JSON';
  }
});

document.querySelectorAll('audio').forEach(audio => audio.addEventListener('play', () => {
  document.querySelectorAll('audio').forEach(other => {
    if (other !== audio) other.pause();
  });
}));

updateUI();
