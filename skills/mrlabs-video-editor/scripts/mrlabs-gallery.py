"""Build the interactive Daylight Pro Talking-Head & Captioning Studio and AI prompt generator."""
import argparse
import hashlib
import html
import json
import os
import webbrowser
from mrlabs_core import MRLABS_ROOT, mrlabs_read
from mrlabs_visual import MRLABS_EFFECTS, mrlabs_css, mrlabs_motion, mrlabs_effect_specimen_html

DEFAULT_PRO_FX = {
    "obsidian-studio": "orbit",
    "verge-glass": "ui-world",
    "monocle-brief": "headline-wall",
    "kinfolk-linen": "digital-zoom",
    "founder-slate": "pull-back-reveal",
    "neon-script": "side-stack",
    "echo-pulse": "echo-wall",
    "vogue-cover": "cover-story",
    "pixel-creator": "prompt-bar",
    "tactile-paper": "tactile-board",
    "claude-grid": "grid-3x3",
    "colorist-grade": "grade-hud",
    "sticker-pop": "orbit",
    "shoulder-note": "digital-zoom",
    "before-after-stage": "before-after",
}


def mrlabs_bilingual(tag, class_name, indonesian, english):
    return f'<{tag} class="{class_name}" data-id="{html.escape(indonesian, quote=True)}" data-en="{html.escape(english, quote=True)}">{html.escape(indonesian)}</{tag}>'


def mrlabs_bilingual_title(theme):
    if "\n" in theme["heading_id"] and "\n" in theme["heading_en"]:
        id_kicker, id_hero = theme["heading_id"].split("\n", 1)
        en_kicker, en_hero = theme["heading_en"].split("\n", 1)
        kicker = mrlabs_bilingual("span", "title-kicker", id_kicker, en_kicker)
        hero = mrlabs_bilingual("span", "title-hero", id_hero, en_hero)
        return f'<div class="title">{kicker}{hero}</div>'
    return mrlabs_bilingual("div", "title", theme["heading_id"], theme["heading_en"])


def mrlabs_specimen(theme, number):
    """Build a 1080x1920 talking-head specimen using previews/creator.png + previews/creator-cutout.png and 13 toggleable effects."""
    css = mrlabs_css(theme).replace('assets/mrlabs/fonts/', 'fonts/')
    motion = mrlabs_motion(theme)
    raw_pos = theme.get('caption_position', 'below-face')
    caption_pos = 'below-face' if raw_pos in ('chest-float', 'below-face') else raw_pos
    default_portrait = 'true'
    default_fx = DEFAULT_PRO_FX.get(theme['id'], '')
    fx_attr = f' data-default-fx="{default_fx}" data-fx-{default_fx}="true"' if default_fx else ''
    transform = f'translate({motion.get("x",0)}px,{motion.get("y",0)}px) scale({motion.get("scale",1)}) rotate({motion.get("rotation",0)}deg)'
    title = mrlabs_bilingual_title(theme)
    caption = mrlabs_bilingual('div', 'caption '+theme['caption_style'], theme['caption_id'], theme['caption_en'])
    fx_html = mrlabs_effect_specimen_html(theme)
    return f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><style>{css}
    .preview-bg{{position:absolute;inset:0;background:var(--background);z-index:0}}
    #main[data-portrait="true"] .preview-bg{{background:transparent!important}}
    #main[data-portrait="false"] .preview-bg{{background:var(--background)!important;display:block!important}}
    .specimen-index{{position:absolute;bottom:85px;right:85px;z-index:8;font:400 140px var(--heading-font);color:var(--accent);opacity:.22;pointer-events:none}}
    .specimen-note{{position:absolute;bottom:120px;left:65px;z-index:8;font:400 22px var(--label-font);letter-spacing:.1em;color:var(--muted);pointer-events:none}}
    .replay .title,.replay .caption{{animation:entrance {theme['enter_seconds']}s cubic-bezier(.2,.8,.2,1) both}}
    .replay .caption{{animation-delay:.22s}}
    @keyframes entrance{{from{{opacity:0;transform:{transform};filter:{motion.get('filter','none')}}}to{{opacity:1;transform:translate(0,0) scale(1) rotate(0);filter:none}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style></head><body><div id="main" data-theme="{theme['id']}" data-talking-head="true" data-portrait="{default_portrait}" data-default-portrait="{default_portrait}" data-caption-pos="{caption_pos}" data-default-caption-pos="{caption_pos}"{fx_attr}><div class="preview-bg"></div><video id="user-preview-video" class="base" muted loop playsinline style="display:none"></video><img id="default-base-img" class="base" src="previews/creator.png" alt="Foto kreator"><div class="shade"></div><div class="art-direction"></div><img id="default-subject-img" class="subject" src="previews/creator-cutout.png" alt="Cutout kreator"><div id="fx-profile-card" class="fx-profile-card" style="display:none;opacity:0;z-index:9"><img id="user-profile-img" src="" alt="Profile IG"></div>{fx_html}<div class="brand">MR LABS</div>{title}{caption}<div class="credit">by @maulanarahman_</div><div class="specimen-index">{number:02d}</div><div class="specimen-note">VISUAL STUDY<br>PRO CAPTIONING</div></div></body></html>'''


def mrlabs_main():
    script_version = hashlib.sha256((MRLABS_ROOT / 'assets/gallery.js').read_bytes()).hexdigest()[:12]
    themes = mrlabs_read(MRLABS_ROOT / 'assets/themes.json')['themes']
    assets = mrlabs_read(MRLABS_ROOT / 'assets/catalog.json')['assets']
    pro_cards = []
    theme_pills = []
    specimens_map = {}

    default_theme_id = 'obsidian-studio'
    default_active_fx = {'orbit'}

    for number, t in enumerate(themes, 1):
        raw_specimen = mrlabs_specimen(t, number)
        raw_pos = t.get("caption_position", "below-face")
        norm_pos = "below-face" if raw_pos in ("chest-float", "below-face") else raw_pos
        specimens_map[t['id']] = {
            "id": t["id"],
            "name": t["name"],
            "collection": t.get("collection", "pro"),
            "tagline": t["tagline"],
            "background": t["background"],
            "accent": t["accent"],
            "talking_head": True,
            "default_fx": DEFAULT_PRO_FX.get(t["id"], ""),
            "caption_position": norm_pos,
            "srcdoc": raw_specimen,
        }
        specimen = html.escape(raw_specimen, quote=True)
        swatches = ''.join(f'<i style="background:{t[key]}"></i>' for key in ('background', 'foreground', 'accent'))
        is_selected = (t['id'] == default_theme_id)
        fx_badge = DEFAULT_PRO_FX.get(t['id'])
        fx_label = f' · FX: {MRLABS_EFFECTS[fx_badge]["name"].upper()}' if fx_badge else ''
        pro_cards.append(
            f'<article class="package" data-card-theme="{t["id"]}" style="--accent:{t["accent"]}">'
            f'<div class="card-heading"><span>{number:02d}</span><span>{t["energy"].upper()}{fx_label}</span></div>'
            f'<div class="screen"><iframe title="{t["name"]} — contoh komposisi" tabindex="-1" srcdoc="{specimen}"></iframe></div>'
            f'<div class="details"><h2>{t["name"]}</h2><p class="tagline">{t["tagline"]}</p><p class="use">{t["use_for"]}</p>'
            f'<div class="swatches">{swatches}<span>{t["heading_font"]}</span></div>'
            f'<button class="pick" data-theme="{t["id"]}" aria-pressed="{"true" if is_selected else "false"}">{"Terpilih" if is_selected else "Gunakan Mode Ini"}<span aria-hidden="true">↗</span></button>'
            f'</div></article>'
        )
        theme_pills.append(
            f'<button type="button" class="theme-chip" data-theme="{t["id"]}" aria-pressed="{"true" if is_selected else "false"}">'
            f'<i style="background:{t["accent"]}"></i><span>{t["name"]}</span><small>{number:02d}</small></button>'
        )

    effect_cards = []
    for fx_id, fx in MRLABS_EFFECTS.items():
        is_checked = fx_id in default_active_fx
        effect_cards.append(
            f'<label class="fx-chip{" active" if is_checked else ""}" data-fx="{fx_id}">'
            f'<input type="checkbox" value="{fx_id}" class="fx-toggle"{" checked" if is_checked else ""}>'
            f'<div class="fx-chip-body">'
            f'<div class="fx-chip-head"><strong>{fx["name"]}</strong><code>{fx_id}</code></div>'
            f'<p>{fx["summary_id"]}</p>'
            f'</div></label>'
        )

    fonts, sounds = [], []
    for asset in assets:
        if asset['kind'] == 'font':
            for sample in asset.get('specimens', [{'label': asset['family'], 'weight': 400}]):
                fonts.append(f'<div class="font-specimen"><small>{sample["label"]} · {sample["weight"]} · OFL</small><p style="font-family:\'{asset["family"]}\';font-weight:{sample["weight"]};font-synthesis:none">Ide kecil. Dampak besar.</p></div>')
        else:
            sounds.append(f'<label class="sound"><span>{asset["id"]}</span><audio controls preload="metadata" src="sfx/{asset["id"]}.ogg"></audio></label>')
    fonts.append('<div class="font-specimen helvetica"><small>Helvetica · 400 · lokal berlisensi</small><p style="font-family:Helvetica,Roboto,sans-serif">Ide kecil. Dampak besar.</p><small id="helvetica-status" role="status">Memeriksa font lokal; fallback: Roboto.</small></div>')

    default_srcdoc = html.escape(specimens_map[default_theme_id]["srcdoc"], quote=True)
    specimens_json = json.dumps(specimens_map, ensure_ascii=False)

    document = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>MR Labs — Pro Talking-Head &amp; Captioning Studio</title><link rel="stylesheet" href="fonts/fonts.css"><link rel="stylesheet" href="gallery.css"></head><body><main>
<nav>
  <a class="wordmark" href="#">MR<span>↗</span>LABS</a>
  <span>PRO TALKING-HEAD STUDIO &amp; PROMPT GENERATOR</span>
  <div class="nav-links">
    <a href="#studio">01. Studio Builder</a>
    <a href="#pro">02. 15 Mode Visual</a>
    <a href="#assets">03. Font &amp; SFX</a>
  </div>
  <span class="edition">15 PRO MODES · EDITION 05</span>
</nav>

<header>
  <div>
    <div class="kicker">✦ DAYLIGHT STUDIO · 15 MODE PRO + 13 EFEK VIRAL</div>
    <h1>Pilih videomu.<br><span>Salin prompt murninya.</span></h1>
    <p>Pilih langsung file <b>video raw</b> dari komputermu, tentukan <b>1 dari 15 mode visual</b>, atur <b>6 posisi caption</b>, dan nyalakan <b>13 efek viral</b>. Prompt yang dihasilkan sudah terisi lengkap dengan path file, resolusi, dan konfigurasi murni yang siap langsung ditempel ke chat AI Agent tanpa perlu mengedit kurung siku lagi.</p>
  </div>
  <div class="controls">
    <button id="language" type="button">Bahasa Prompt: Indonesia</button>
    <button id="portrait" type="button" aria-pressed="false">Latar: Potrait Asli (Tanpa BG)</button>
    <button id="replay" type="button">↻ Putar ulang animasi</button>
    <small>Resolusi &amp; orientasi potrait/landscape otomatis terdeteksi saat kamu memilih file video.</small>
  </div>
</header>

<section class="studio-builder" id="studio" aria-label="Interactive Prompt Generator Studio">
  <div class="studio-preview-col">
    <div class="studio-monitor-head">
      <span class="kicker">LIVE MONITOR · 1080×1920</span>
      <span id="studio-badge">Creator Hook · Di Bawah Muka · +1 FX</span>
    </div>
    <div class="screen studio-screen">
      <iframe id="studio-frame" title="Live Interactive Studio Preview" srcdoc="{default_srcdoc}"></iframe>
    </div>
    <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
      <button type="button" id="toggle-user-video" class="mini-btn" style="flex:1;display:none">👁 Tampilkan Video Raw Saya di Monitor</button>
      <button type="button" id="toggle-profile-preview" class="mini-btn" style="flex:1;display:none">👤 Preview Kartu IG di Monitor</button>
    </div>
  </div>

  <div class="studio-controls-col">
    <div class="builder-group project-inputs">
      <div class="builder-label">
        <span>00 / PILIH FILE VIDEO RAW &amp; ASET PROYEK (OTOMATIS MASUK KE PROMPT)</span>
        <span id="video-meta-badge" class="meta-pill">Belum ada file dipilih (default: ./input.mp4)</span>
      </div>

      <div class="input-grid-2">
        <div class="field-card">
          <div class="field-head">
            <label for="video-path">🎬 File Video Raw Utama</label>
            <small>Wajib · .mp4 / .mov / .mkv</small>
          </div>
          <div class="file-picker-row">
            <label class="file-btn">
              <span>📂 Pilih Video...</span>
              <input type="file" id="video-file" accept="video/*">
            </label>
            <input type="text" id="video-path" class="text-input" placeholder="Atau tempel path lengkap: D:\\Video\\raw.mp4">
          </div>
        </div>

        <div class="field-card">
          <div class="field-head">
            <label for="folder-path">📁 Folder Kerja / Direktori Video (Opsional)</label>
            <small>Digabung otomatis dengan nama file</small>
          </div>
          <input type="text" id="folder-path" class="text-input" placeholder="Contoh: D:\\KERJAAN YOUTUBE\\footage">
        </div>

        <div class="field-card">
          <div class="field-head">
            <label for="profile-path">👤 Gambar Profil IG / Kartu CTA (Opsional)</label>
            <small>Muncul saat ajakan follow</small>
          </div>
          <div class="file-picker-row">
            <label class="file-btn">
              <span>🖼️ Pilih Gambar...</span>
              <input type="file" id="profile-file" accept="image/*">
            </label>
            <input type="text" id="profile-path" class="text-input" placeholder="Opsional: path gambar profil IG">
          </div>
        </div>

        <div class="field-card">
          <div class="field-head">
            <label for="notes-input">✨ Instruksi / Catatan Edit Tambahan (Opsional)</label>
            <small>Langsung masuk ke prompt</small>
          </div>
          <input type="text" id="notes-input" class="text-input" placeholder="Misal: Tonjolkan kata Claude, potong jeda awal...">
        </div>
      </div>

      <div class="input-grid-3">
        <div class="field-card">
          <div class="field-head"><label for="brand-input">🏷️ Brand Header Atas</label><small>Live di monitor</small></div>
          <input type="text" id="brand-input" class="text-input" value="MR LABS">
        </div>
        <div class="field-card">
          <div class="field-head"><label for="credit-input">✍️ Credit / Handle</label><small>Live di monitor</small></div>
          <input type="text" id="credit-input" class="text-input" value="by @maulanarahman_">
        </div>
        <div class="field-card">
          <div class="field-head"><label for="keywords-input">🔤 Kata Kunci Transkrip (Whisper Hint)</label><small>Pisahkan koma</small></div>
          <input type="text" id="keywords-input" class="text-input" placeholder="Misal: MR Labs, Claude Code, HyperFrames">
        </div>
      </div>
    </div>

    <div class="builder-group">
      <div class="builder-label"><span>01 / PILIH MODE PRO TALKING-HEAD (15 MODE)</span><small id="selected-theme-label">Creator Hook (obsidian-studio)</small></div>
      <div class="theme-chip-grid">{''.join(theme_pills)}</div>
    </div>

    <div class="builder-row-2">
      <div class="builder-group">
        <div class="builder-label"><span>02 / POSISI &amp; MODE CAPTION (6 MODE)</span><small>Sesuaikan tipografi &amp; letak</small></div>
        <div class="pos-chip-grid" role="radiogroup" aria-label="Posisi Caption">
          <button type="button" class="pos-chip" data-pos="below-face" aria-pressed="true">
            <strong>Di Bawah Muka / Dada</strong>
            <small>Floating bersih di depan dada (Y: 1050px)</small>
          </button>
          <button type="button" class="pos-chip" data-pos="above-head" aria-pressed="false">
            <strong>Di Atas Kepala</strong>
            <small>Tepat di atas kepala presenter (Y: 310px)</small>
          </button>
          <button type="button" class="pos-chip" data-pos="bottom" aria-pressed="false">
            <strong>Di Bawah Frame</strong>
            <small>Posisi klasik sepertiga bawah (Y: 1265px)</small>
          </button>
          <button type="button" class="pos-chip" data-pos="split-script" aria-pressed="false">
            <strong>Split Script Neon</strong>
            <small>Cursive Caveat menyala di dada ala Vids</small>
          </button>
          <button type="button" class="pos-chip" data-pos="hierarchy-glow" aria-pressed="false">
            <strong>Hierarchy Glow 2-Baris</strong>
            <small>Baris pengantar + kata kunci emas menyala</small>
          </button>
          <button type="button" class="pos-chip" data-pos="shoulder-note" aria-pressed="false">
            <strong>Shoulder Callout Note</strong>
            <small>Caption dada + catatan mikro di samping bahu</small>
          </button>
        </div>
      </div>

      <div class="builder-group">
        <div class="builder-label"><span>03 / KONDISI LATAR VIDEO</span><small>Otomatis terdeteksi dari video</small></div>
        <div class="pos-chip-grid" role="radiogroup" aria-label="Mode Background">
          <button type="button" class="bg-chip" data-bg-mode="portrait" aria-pressed="true">
            <strong>Video Sudah Potrait (Tanpa BG)</strong>
            <small>Gunakan ruang asli video potrait</small>
          </button>
          <button type="button" class="bg-chip" data-bg-mode="studio" aria-pressed="false">
            <strong>Non-Potrait (Latar Putih/Hitam Tema)</strong>
            <small>Cutout di atas latar Putih/Hitam/Kertas tema</small>
          </button>
        </div>
      </div>
    </div>

    <div class="builder-group">
      <div class="builder-label">
        <span>04 / PILIH EFEK VIDEO (13 EFEK VIRAL · BISA PILIH BANYAK)</span>
        <div style="display:flex;gap:8px">
          <button type="button" id="all-fx" class="mini-btn">✨ Semua Efek</button>
          <button type="button" id="clear-fx" class="mini-btn">Reset Efek</button>
        </div>
      </div>
      <div class="fx-chip-grid">{''.join(effect_cards)}</div>
    </div>

    <div class="builder-group prompt-box">
      <div class="builder-label">
        <span>05 / PROMPT MURNI SIAP TEMPEL KE CHAT AI &amp; CONFIG JSON</span>
        <span class="status" role="status" aria-live="polite">✓ Prompt murni siap dipakai</span>
      </div>
      <label for="prompt-output" class="sr-only">Prompt AI</label>
      <p class="asset-note">Prompt di bawah ini sudah otomatis berisi nama/lokasi file video, resolusi, mode tema, posisi caption, efek terpilih, serta blok konfigurasi JSON—langsung salin dan tempel ke chat.</p>
      <textarea id="prompt-output" rows="9" readonly></textarea>
      <div class="prompt-actions">
        <button type="button" id="copy-prompt" class="primary-btn">📋 Salin Prompt Murni ke Chat ↗</button>
        <input id="config" readonly value='{{"theme":"obsidian-studio","caption_position":"below-face","effects":["orbit"],"language":"id"}}'>
        <button type="button" id="copy">Salin JSON Saja ↗</button>
      </div>
    </div>
  </div>
</section>

<div class="collection-heading" id="pro"><div><span class="kicker">PRO TALKING-HEAD / 01—15</span><h2>15 Mode Talking-Head, Depth Hook &amp; 13 Efek Viral.</h2></div><p>5 mode klasik + 10 mode baru hasil bedah referensi kreator global. Klik kartu mana saja untuk memuat tema &amp; efek bawaannya ke Studio di atas.</p></div>
<section class="packages" aria-label="Lima belas tema Pro Influencer">{''.join(pro_cards)}</section>

<div class="asset-header" id="assets"><h2>Peralatan kreatif lokal.</h2><p>12 keluarga font berlisensi terbuka + 10 aksen suara antarmuka.</p></div>
<details class="asset-group"><summary>01 / Koleksi font · 12 keluarga + Helvetica lokal <span>+</span></summary><p class="asset-note">Poppins Bold (700), Roboto (400), dan Roboto Light (300) tersedia lokal. Helvetica memakai instalasi lokal berlisensi, dengan fallback Roboto jika tidak tersedia.</p><div class="font-shelf">{''.join(fonts)}</div></details>
<details class="asset-group"><summary>02 / Sepuluh aksen suara <span>+</span></summary><p class="asset-note">Kenney Interface Sounds · CC0. Efek mengikuti aksi dan tetap di bawah narasi.</p><div class="sound-shelf">{''.join(sounds)}</div></details>
<footer><span>MR LABS / DAYLIGHT STUDIO EDITION 05.</span><p>Font <a href="https://github.com/google/fonts">Google Fonts / OFL</a> · SFX <a href="https://kenney.nl/assets/interface-sounds">Kenney / CC0</a> · <a href="catalog.json">Sumber &amp; lisensi</a></p><p>Base foto kreator: <code>assets/previews/creator.png</code> + <code>creator-cutout.png</code>.</p></footer>
</main>
<script>window.__MRLABS_SPECIMENS={specimens_json};</script>
<script src="gallery.js?v={script_version}"></script></body></html>'''
    target = MRLABS_ROOT / 'assets/theme-gallery.html'
    target.write_text(document, encoding='utf-8')
    print(target)
    return target


def mrlabs_open_gallery(target=None):
    target = (target or (MRLABS_ROOT / 'assets/theme-gallery.html')).resolve()
    if hasattr(os, 'startfile'):
        os.startfile(str(target))
    else:
        webbrowser.open(target.as_uri())
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--open', action='store_true', help='Open theme-gallery.html in the default browser after building.')
    args = parser.parse_args()
    out = mrlabs_main()
    if args.open:
        mrlabs_open_gallery(out)
