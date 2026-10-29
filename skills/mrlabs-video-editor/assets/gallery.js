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
  if (!doc) return;
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
  const fxDescriptions = fxArray.length
    ? fxArray.map(fx => FX_LABELS[fx] || fx).join('; ')
    : 'Tanpa efek tambahan (fokus pada tipografi tema & depth hook)';
  const bgCondition = forceNonPortrait
    ? `Paksa gunakan latar belakang tema (${spec.background}) di belakang cutout subjek`
    : `Jika video sudah potrait (height > width), tidak perlu background tema; gunakan latar asli video dengan cutout subject.webm untuk efek depth`;

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
      `Edit my talking-head video using the mrlabs-video-editor skill with these settings:`,
      `- Visual Theme: ${spec.name} ("${selected}")`,
      `- Caption Position: ${captionPos} (${POS_LABELS[captionPos]})`,
      `- Active Video Effects: ${fxArray.length ? fxArray.join(', ') : 'none'} (${fxDescriptions})`,
      `- Background Condition: ${forceNonPortrait ? `Use theme background (${spec.background}) behind subject cutout` : 'If source video is already portrait, skip theme background and keep original room with subject.webm depth cutout'}`,
      `- Config JSON: ${JSON.stringify(payload)}`
    ].join('\n');
  }

  return [
    `Tolong edit video talking-head saya menggunakan skill mrlabs-video-editor dengan pengaturan berikut:`,
    `- Tema Visual: ${spec.name} ("${selected}")`,
    `- Posisi Caption: ${POS_LABELS[captionPos]}`,
    `- Efek Video: ${fxDescriptions}`,
    `- Kondisi Latar: ${bgCondition}`,
    `- Config JSON: ${JSON.stringify(payload)}`
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
