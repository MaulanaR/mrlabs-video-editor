let selected = 'obsidian-studio';
let language = 'id';
let forceNonPortrait = false;
let captionPos = 'below-face';
let activeEffects = new Set(['orbit']);
let userCustomizedEffects = false;
let userCustomizedCaptionPos = false;

let userVideoMeta = null; // { name, width, height, duration, objectUrl }
let showUserVideoInMonitor = false;
let userProfileObjectUrl = '';
let showProfileInMonitor = false;

const ALL_FX = [
  'orbit',
  'ui-world',
  'digital-zoom',
  'headline-wall',
  'pull-back-reveal',
  'echo-wall',
  'cover-story',
  'grid-3x3',
  'prompt-bar',
  'grade-hud',
  'side-stack',
  'tactile-board',
  'before-after'
];

const FX_NAMES = {
  'orbit': 'ORBIT 3D Cards',
  'ui-world': 'UI World Window',
  'digital-zoom': 'Digital Zoom Punch-In',
  'headline-wall': 'Headline Wall',
  'pull-back-reveal': 'Pull Back Reveal',
  'echo-wall': 'Echo Repeat Stack',
  'cover-story': 'Magazine Cover Story',
  'grid-3x3': '3×3 Reel Matrix',
  'prompt-bar': 'AI Prompt & Tool Pills',
  'grade-hud': 'Colorist Tone Curve HUD',
  'side-stack': 'Side Block & Starburst',
  'tactile-board': 'Tactile Sticky & Wireframe',
  'before-after': 'Before / After Stage'
};

const POS_SHORT = {
  'below-face': 'Di Bawah Muka',
  'above-head': 'Di Atas Kepala',
  'bottom': 'Di Bawah Frame',
  'split-script': 'Split Script Neon',
  'hierarchy-glow': 'Hierarchy Glow',
  'shoulder-note': 'Shoulder Callout'
};

const configInput = document.querySelector('#config');
const promptOutput = document.querySelector('#prompt-output');
const statusEl = document.querySelector('.status');
const studioFrame = document.querySelector('#studio-frame');
const studioBadge = document.querySelector('#studio-badge');
const selectedThemeLabel = document.querySelector('#selected-theme-label');

const videoFileInput = document.querySelector('#video-file');
const videoPathInput = document.querySelector('#video-path');
const folderPathInput = document.querySelector('#folder-path');
const profileFileInput = document.querySelector('#profile-file');
const profilePathInput = document.querySelector('#profile-path');
const notesInput = document.querySelector('#notes-input');
const brandInput = document.querySelector('#brand-input');
const creditInput = document.querySelector('#credit-input');
const keywordsInput = document.querySelector('#keywords-input');
const videoMetaBadge = document.querySelector('#video-meta-badge');
const toggleUserVideoBtn = document.querySelector('#toggle-user-video');
const toggleProfilePreviewBtn = document.querySelector('#toggle-profile-preview');

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

function joinPath(folder, file) {
  const cleanFile = (file || '').trim().replace(/^["']|["']$/g, '');
  const cleanFolder = (folder || '').trim().replace(/^["']|["']$/g, '').replace(/[\\/]+$/, '');
  if (!cleanFile) return cleanFolder ? `${cleanFolder}\\input.mp4` : './input.mp4';
  if (/^[a-zA-Z]:[\\/]/.test(cleanFile) || cleanFile.startsWith('/') || cleanFile.startsWith('./') || cleanFile.startsWith('..\\')) {
    return cleanFile;
  }
  if (cleanFolder) {
    const sep = cleanFolder.includes('/') && !cleanFolder.includes('\\') ? '/' : '\\';
    return `${cleanFolder}${sep}${cleanFile}`;
  }
  return cleanFile;
}

function getResolvedVideoPath() {
  return joinPath(folderPathInput?.value, videoPathInput?.value);
}

function getResolvedProfilePath() {
  const raw = (profilePathInput?.value || '').trim();
  if (!raw) return '';
  return joinPath(folderPathInput?.value, raw);
}

function getKeywordsList() {
  const raw = (keywordsInput?.value || '').trim();
  if (!raw) return ['MR Labs', 'Claude Code', 'HyperFrames'];
  return raw.split(',').map(s => s.trim()).filter(Boolean);
}

function syncCheckboxesWithSet() {
  document.querySelectorAll('.fx-toggle').forEach(cb => {
    const isOn = activeEffects.has(cb.value);
    cb.checked = isOn;
    cb.closest('.fx-chip')?.classList.toggle('active', isOn);
  });
}

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
  const defaultCardPos = main.dataset.defaultCaptionPos || 'below-face';
  main.dataset.captionPos = (isStudio || userCustomizedCaptionPos) ? captionPos : defaultCardPos;

  const brandEl = doc.querySelector('.brand');
  if (brandEl && brandInput) {
    brandEl.textContent = brandInput.value.trim() || 'MR LABS';
  }
  const creditEl = doc.querySelector('.credit');
  if (creditEl && creditInput) {
    creditEl.textContent = creditInput.value.trim() || 'by @maulanarahman_';
  }

  if (isStudio) {
    const userVid = doc.querySelector('#user-preview-video');
    const baseImg = doc.querySelector('#default-base-img');
    const subjImg = doc.querySelector('#default-subject-img');
    if (userVid && baseImg && subjImg) {
      if (showUserVideoInMonitor && userVideoMeta?.objectUrl) {
        if (userVid.src !== userVideoMeta.objectUrl) {
          userVid.src = userVideoMeta.objectUrl;
        }
        userVid.style.display = 'block';
        userVid.play().catch(() => {});
        baseImg.style.display = 'none';
        subjImg.style.display = 'none';
      } else {
        userVid.pause?.();
        userVid.style.display = 'none';
        baseImg.style.display = '';
        subjImg.style.display = '';
      }
    }

    const profCard = doc.querySelector('#fx-profile-card');
    const profImg = doc.querySelector('#user-profile-img');
    if (profCard && profImg) {
      if (showProfileInMonitor && userProfileObjectUrl) {
        profImg.src = userProfileObjectUrl;
        profCard.style.display = 'block';
        profCard.style.opacity = '1';
      } else {
        profCard.style.display = 'none';
        profCard.style.opacity = '0';
      }
    }
  }

  const defaultCardFx = main.dataset.defaultFx || '';
  ALL_FX.forEach(fx => {
    let shouldEnable = false;
    if (isStudio) {
      shouldEnable = activeEffects.has(fx);
    } else if (userCustomizedEffects) {
      shouldEnable = activeEffects.has(fx);
    } else {
      shouldEnable = defaultCardFx ? (fx === defaultCardFx) : false;
    }
    if (shouldEnable) {
      main.setAttribute(`data-fx-${fx}`, 'true');
    } else {
      main.removeAttribute(`data-fx-${fx}`);
    }
  });
}

function syncAllFrames() {
  allFrames().forEach(frame => syncFrameState(frame, frame === studioFrame));
}

function buildStatefulSrcdoc(rawSrcdoc) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(rawSrcdoc, 'text/html');
  doc.documentElement.lang = language;
  doc.querySelectorAll('[data-id]').forEach(el => {
    el.textContent = el.dataset[language];
  });
  const main = doc.querySelector('#main');
  if (main) {
    main.dataset.portrait = forceNonPortrait ? 'false' : 'true';
    main.dataset.captionPos = captionPos;
    ALL_FX.forEach(fx => {
      if (activeEffects.has(fx)) {
        main.setAttribute(`data-fx-${fx}`, 'true');
      } else {
        main.removeAttribute(`data-fx-${fx}`);
      }
    });
  }
  return '<!doctype html>' + doc.documentElement.outerHTML;
}

function buildPromptText() {
  const spec = (window.__MRLABS_SPECIMENS && window.__MRLABS_SPECIMENS[selected]) || { name: selected, background: '#0A0A0A' };
  const fxArray = [...activeEffects];
  const creatorHook = selected === 'obsidian-studio';
  const themeName = creatorHook ? 'Obsidian Studio' : spec.name;

  const videoPath = getResolvedVideoPath();
  const profilePath = getResolvedProfilePath();
  const brandVal = (brandInput?.value || 'MR LABS').trim();
  const creditVal = (creditInput?.value || 'by @maulanarahman_').trim();
  const notesVal = (notesInput?.value || '').trim();
  const kwList = getKeywordsList();

  const positions = {
    id: {
      'above-head': 'di atas kepala saya (`above-head`, Y: 310px)',
      'below-face': 'di bawah muka / di depan dada saya (`below-face` / `chest-float`, Y: 1050px)',
      'bottom': 'di bagian bawah frame (`bottom`, Y: 1265px)',
      'split-script': 'di depan dada dengan gaya Split Script Neon (`split-script`, font cursive Caveat menyala)',
      'hierarchy-glow': 'di depan dada dengan gaya Hierarchy Glow 2-baris (`hierarchy-glow`, baris pengantar kecil + kata kunci emas menyala)',
      'shoulder-note': 'di depan dada disertai catatan mikro 3 baris di samping bahu/pelipis (`shoulder-note`)'
    },
    en: {
      'above-head': 'above my head (`above-head`, Y: 310px)',
      'below-face': 'below my face / across my chest (`below-face` / `chest-float`, Y: 1050px)',
      'bottom': 'in the lower part of the frame (`bottom`, Y: 1265px)',
      'split-script': 'across my chest in Split Script Neon style (`split-script`, glowing Caveat cursive script)',
      'hierarchy-glow': 'across my chest in 2-line Hierarchy Glow style (`hierarchy-glow`, small setup line + glowing accent keyword)',
      'shoulder-note': 'across my chest paired with a 3-line micro Shoulder Callout note beside my temple/shoulder (`shoulder-note`)'
    }
  };
  const effectNames = fxArray.map(fx => `${FX_NAMES[fx] || fx} (\`${fx}\`)`).join(', ');

  const payload = {
    source_video: videoPath,
    theme: selected,
    caption_position: captionPos,
    effects: fxArray,
    portrait: !forceNonPortrait,
    language,
    brand: brandVal,
    credit: creditVal,
    keywords: kwList
  };
  if (profilePath) payload.profile_card = profilePath;
  if (userVideoMeta) {
    payload.detected_resolution = `${userVideoMeta.width}x${userVideoMeta.height}`;
    payload.detected_duration_sec = Number(userVideoMeta.duration.toFixed(2));
  }
  configInput.value = JSON.stringify(payload);

  const posShort = POS_SHORT[captionPos] || captionPos;
  if (studioBadge) {
    studioBadge.textContent = `${spec.name} · ${posShort}${fxArray.length ? ` · +${fxArray.length} FX` : ''}`;
  }
  if (selectedThemeLabel) {
    selectedThemeLabel.textContent = `${spec.name} (${selected})`;
  }

  const metaLineId = userVideoMeta
    ? ` (${userVideoMeta.width}×${userVideoMeta.height}px, durasi ${userVideoMeta.duration.toFixed(1)} detik, orientasi ${userVideoMeta.height > userVideoMeta.width ? 'Potrait 9:16' : 'Landscape'})`
    : '';
  const metaLineEn = userVideoMeta
    ? ` (${userVideoMeta.width}×${userVideoMeta.height}px, duration ${userVideoMeta.duration.toFixed(1)}s, ${userVideoMeta.height > userVideoMeta.width ? 'Portrait 9:16' : 'Landscape'})`
    : '';

  if (language === 'en') {
    const lines = [
      'Edit my talking-head video using the `$mrlabs-video-editor` skill.',
      '',
      `Source video: \`${videoPath}\`${metaLineEn}`,
      `Theme mode: **${themeName}** (\`${selected}\`)`,
      `Brand & credit: \`${brandVal}\` · \`${creditVal}\``,
      `Transcript keywords: ${kwList.join(', ')}`
    ];
    if (profilePath) {
      lines.push(`Instagram profile card: \`${profilePath}\` (show during the follow call-to-action)`);
    }
    if (notesVal) {
      lines.push(`Special instructions: ${notesVal}`);
    }
    lines.push(
      '',
      'Visual & editing rules:',
      `- Place conversational captions ${positions.en[captionPos] || positions.en['below-face']}. Keep phrases short and timed to actual speech.`,
      `- Highlight key spoken moments with large **${creatorHook ? 'yellow (#FCE373)' : `theme-accent (${spec.accent || spec.background})`}** depth titles behind my head and shoulders using a subject cutout (\`subject.webm\`), so my head naturally occludes part of the letters.`,
      forceNonPortrait
        ? `- Place my subject cutout over the **${themeName}** studio background (\`${spec.background}\`).`
        : '- Keep my original portrait video background without adding a synthetic canvas background (`data-portrait="true"`).',
      fxArray.length
        ? `- Activate these viral effects at relevant moments in the timeline (spaced cleanly, never all overlapping at once): ${effectNames}.`
        : '- No extra overlay effects; focus purely on clean typography and depth behind the subject.',
      '- Do not invent numbers, statistics, or words not present in my actual speech.',
      '',
      'Configuration (`project.json` / `visual.json`):',
      '```json',
      JSON.stringify(payload, null, 2),
      '```',
      '',
      'Review the transcript and propose a timestamped edit plan first. Wait for my approval, then render the full 1080×1920 MP4, phone copy, and `captions.srt`.'
    );
    return lines.join('\n');
  }

  const lines = [
    'Edit video talking-head saya menggunakan skill `$mrlabs-video-editor`.',
    '',
    `File video utama: \`${videoPath}\`${metaLineId}`,
    `Mode tema: **${themeName}** (\`${selected}\`)`,
    `Brand & credit: \`${brandVal}\` · \`${creditVal}\``,
    `Kata kunci transkrip (Whisper): ${kwList.join(', ')}`
  ];
  if (profilePath) {
    lines.push(`Gambar profil Instagram / CTA: \`${profilePath}\` (tampilkan pada bagian ajakan follow)`);
  }
  if (notesVal) {
    lines.push(`Instruksi khusus: ${notesVal}`);
  }
  lines.push(
    '',
    'Aturan visual & komposisi:',
    `- Letakkan caption percakapan ${positions.id[captionPos] || positions.id['below-face']}. Gunakan potongan frasa pendek yang mengikuti waktu ucapan.`,
    `- Pada poin penting yang diucapkan, tampilkan kata kunci besar berwarna **${creatorHook ? 'kuning (#FCE373)' : `aksen tema (${spec.accent || spec.background})`}** di belakang kepala dan bahu saya menggunakan cutout subjek (\`subject.webm\`), sehingga sebagian huruf tertutup alami oleh kepala.`,
    forceNonPortrait
      ? `- Tempatkan cutout subjek di atas latar belakang studio tema **${themeName}** (\`${spec.background}\`).`
      : '- Pertahankan latar asli video karena sumber sudah vertikal/potrait (`data-portrait="true"`, tanpa tambahan latar belakang tema).',
    fxArray.length
      ? `- Gunakan efek berikut pada bagian pembahasan yang relevan (sebarkan secara bergantian di timeline, jangan ditumpuk sekaligus): ${effectNames}.`
      : '- Tanpa efek tambahan; fokus pada ketajaman tipografi dan depth kata kunci di belakang kepala.',
    '- Jangan mengarang angka, klaim, atau teks yang tidak saya ucapkan di dalam video.',
    '',
    'Konfigurasi siap pakai (`project.json` / `visual.json`):',
    '```json',
    JSON.stringify(payload, null, 2),
    '```',
    '',
    'Susun rencana edit bertimestamp dari transkrip terlebih dahulu. Setelah saya setujui, jalankan produksi hingga menghasilkan video 1080×1920 kualitas penuh, versi ringan untuk HP, dan file `captions.srt`.'
  );
  return lines.join('\n');
}

function updateUI() {
  syncCheckboxesWithSet();
  if (promptOutput) {
    promptOutput.value = buildPromptText();
  }
  document.querySelectorAll('.pick').forEach(btn => {
    const isSel = btn.dataset.theme === selected;
    btn.setAttribute('aria-pressed', String(isSel));
    btn.firstChild.textContent = isSel ? 'Terpilih' : 'Gunakan Mode Ini';
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
  if (spec) {
    if (!userCustomizedEffects && spec.default_fx) {
      activeEffects = new Set([spec.default_fx]);
    }
    if (!userCustomizedCaptionPos && spec.caption_position) {
      captionPos = spec.caption_position;
    }
    if (studioFrame) {
      studioFrame.srcdoc = buildStatefulSrcdoc(spec.srcdoc);
    }
  }
  updateUI();
  if (scrollStudio) {
    document.querySelector('.studio-builder')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// Handle local Raw Video file selection -> auto-detect resolution, duration & portrait orientation!
videoFileInput?.addEventListener('change', () => {
  const file = videoFileInput.files && videoFileInput.files[0];
  if (!file) return;
  if (videoPathInput && (!videoPathInput.value.trim() || !videoPathInput.value.includes('\\'))) {
    videoPathInput.value = file.name;
  }
  const objUrl = URL.createObjectURL(file);
  const probeVid = document.createElement('video');
  probeVid.preload = 'metadata';
  probeVid.onloadedmetadata = () => {
    const w = probeVid.videoWidth || 1080;
    const h = probeVid.videoHeight || 1920;
    const dur = probeVid.duration || 0;
    const isPortrait = h > w;
    userVideoMeta = { name: file.name, width: w, height: h, duration: dur, objectUrl: objUrl };
    forceNonPortrait = !isPortrait;
    if (videoMetaBadge) {
      videoMetaBadge.textContent = `✓ ${file.name} · ${w}×${h} (${isPortrait ? 'Potrait' : 'Landscape'}) · ${dur.toFixed(1)} dtk`;
      videoMetaBadge.classList.add('ready');
    }
    if (toggleUserVideoBtn) {
      toggleUserVideoBtn.style.display = 'inline-flex';
      showUserVideoInMonitor = true;
      toggleUserVideoBtn.textContent = '🖼 Kembali ke Foto Contoh Studio';
    }
    if (statusEl) {
      statusEl.textContent = `✓ Video ${file.name} (${w}×${h}) siap di prompt`;
    }
    updateUI();
  };
  probeVid.src = objUrl;
});

toggleUserVideoBtn?.addEventListener('click', () => {
  showUserVideoInMonitor = !showUserVideoInMonitor;
  toggleUserVideoBtn.textContent = showUserVideoInMonitor
    ? '🖼 Kembali ke Foto Contoh Studio'
    : '👁 Tampilkan Video Raw Saya di Monitor';
  syncAllFrames();
});

// Handle Profile Image file selection
profileFileInput?.addEventListener('change', () => {
  const file = profileFileInput.files && profileFileInput.files[0];
  if (!file) return;
  if (profilePathInput && !profilePathInput.value.trim()) {
    profilePathInput.value = file.name;
  }
  userProfileObjectUrl = URL.createObjectURL(file);
  if (toggleProfilePreviewBtn) {
    toggleProfilePreviewBtn.style.display = 'inline-flex';
    showProfileInMonitor = true;
    toggleProfilePreviewBtn.textContent = '🙈 Sembunyikan Kartu IG di Monitor';
  }
  updateUI();
});

toggleProfilePreviewBtn?.addEventListener('click', () => {
  showProfileInMonitor = !showProfileInMonitor;
  toggleProfilePreviewBtn.textContent = showProfileInMonitor
    ? '🙈 Sembunyikan Kartu IG di Monitor'
    : '👤 Preview Kartu IG di Monitor';
  syncAllFrames();
});

// Live update prompt when any text input changes
[videoPathInput, folderPathInput, profilePathInput, notesInput, brandInput, creditInput, keywordsInput].forEach(inp => {
  inp?.addEventListener('input', () => {
    if (inp === videoPathInput && videoPathInput.value.trim() && !userVideoMeta && videoMetaBadge) {
      videoMetaBadge.textContent = `✓ Path: ${getResolvedVideoPath()}`;
      videoMetaBadge.classList.add('ready');
    }
    updateUI();
  });
});

const resize = new ResizeObserver(entries => entries.forEach(({ target }) => {
  const iframe = target.querySelector('iframe');
  if (iframe) iframe.style.transform = `scale(${target.clientWidth / 1080})`;
}));
document.querySelectorAll('.screen').forEach(screen => resize.observe(screen));

allFrames().forEach(frame => frame.addEventListener('load', () => syncFrameState(frame, frame === studioFrame)));

document.querySelectorAll('.pick').forEach(button => button.addEventListener('click', () => {
  selectTheme(button.dataset.theme, true);
  if (statusEl) statusEl.textContent = `Mode ${button.dataset.theme} dimuat ke Studio`;
}));

document.querySelectorAll('.theme-chip').forEach(chip => chip.addEventListener('click', () => {
  selectTheme(chip.dataset.theme, false);
  if (statusEl) statusEl.textContent = `Mode ${chip.dataset.theme} aktif`;
}));

document.querySelectorAll('.pos-chip').forEach(chip => chip.addEventListener('click', () => {
  userCustomizedCaptionPos = true;
  captionPos = chip.dataset.pos;
  updateUI();
  if (statusEl) statusEl.textContent = `Mode caption: ${captionPos}`;
}));

document.querySelectorAll('.bg-chip').forEach(chip => chip.addEventListener('click', () => {
  forceNonPortrait = chip.dataset.bgMode === 'studio';
  updateUI();
}));

document.querySelectorAll('.fx-toggle').forEach(checkbox => checkbox.addEventListener('change', () => {
  userCustomizedEffects = true;
  const fx = checkbox.value;
  if (checkbox.checked) {
    activeEffects.add(fx);
  } else {
    activeEffects.delete(fx);
  }
  updateUI();
  if (statusEl) {
    statusEl.textContent = activeEffects.size
      ? `${activeEffects.size} efek aktif: ${[...activeEffects].join(', ')}`
      : 'Semua efek tambahan dimatikan';
  }
}));

document.querySelector('#all-fx')?.addEventListener('click', () => {
  userCustomizedEffects = true;
  activeEffects = new Set(ALL_FX);
  updateUI();
  if (statusEl) statusEl.textContent = `Semua ${ALL_FX.length} efek diaktifkan`;
});

document.querySelector('#clear-fx')?.addEventListener('click', () => {
  userCustomizedEffects = true;
  activeEffects.clear();
  updateUI();
  if (statusEl) statusEl.textContent = 'Efek di-reset';
});

document.querySelector('#language')?.addEventListener('click', () => {
  language = language === 'id' ? 'en' : 'id';
  document.querySelector('#language').textContent = language === 'id' ? 'Bahasa Prompt: Indonesia' : 'Prompt Language: English';
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
    if (statusEl) statusEl.textContent = '✓ Prompt murni berhasil disalin!';
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
window.addEventListener('load', () => syncAllFrames());
