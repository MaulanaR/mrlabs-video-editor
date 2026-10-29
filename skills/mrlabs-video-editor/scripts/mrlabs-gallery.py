"""Build the interactive theme studio, live effect preview (using creator.png), and AI prompt generator."""
import hashlib
import html
import json
from mrlabs_core import MRLABS_ROOT, mrlabs_read
from mrlabs_visual import MRLABS_EFFECTS, mrlabs_css, mrlabs_motion, mrlabs_effect_specimen_html


def mrlabs_bilingual(tag, class_name, indonesian, english):
    return f'<{tag} class="{class_name}" data-id="{html.escape(indonesian, quote=True)}" data-en="{html.escape(english, quote=True)}">{html.escape(indonesian)}</{tag}>'


def mrlabs_bilingual_title(theme):
    if theme.get("talking_head") and "\n" in theme["heading_id"] and "\n" in theme["heading_en"]:
        id_kicker, id_hero = theme["heading_id"].split("\n", 1)
        en_kicker, en_hero = theme["heading_en"].split("\n", 1)
        kicker = mrlabs_bilingual("span", "title-kicker", id_kicker, en_kicker)
        hero = mrlabs_bilingual("span", "title-hero", id_hero, en_hero)
        return f'<div class="title">{kicker}{hero}</div>'
    return mrlabs_bilingual("div", "title", theme["heading_id"], theme["heading_en"])


def mrlabs_art(theme, number):
    """Original vector specimens for B-roll cards on non-talking-head themes."""
    if theme.get("collection") == "fun":
        return '<div class="theme-placeholder"><span>B-roll</span><small>RUANG VISUAL / VISUAL SPACE</small></div>'
    bg, panel, fg, accent = (theme[k] for k in ('background', 'panel', 'foreground', 'accent'))
    art = {
        'signal-clean': f'<rect width="810" height="456" fill="{panel}"/><circle cx="570" cy="195" r="140" fill="{accent}"/><path d="M60 290V110H240V290ZM275 290V55H455V290Z" fill="{bg}"/><path d="M60 310H745" stroke="{fg}" stroke-width="3"/><text x="70" y="170" font-family="sans-serif" font-size="40" fill="{fg}">A</text><path d="M100 240H360L335 215M360 240L335 265" stroke="{fg}" stroke-width="8" fill="none"/>',
        'kinetic-punch': f'<rect width="810" height="456" fill="{panel}"/><path d="M410 10 445 110 535 55 510 155 625 160 545 230 625 300 510 295 535 400 445 345 410 445 375 345 285 400 310 295 195 300 275 230 195 160 310 155 285 55 375 110Z" fill="{accent}"/><path d="M395 100 465 100 420 205 475 205 355 335 390 235 340 235Z" fill="{bg}"/>',
        'editorial-noir': f'<rect width="810" height="456" fill="{panel}"/><path d="M210 430V210A195 195 0 0 1 600 210V430Z" fill="{accent}"/><circle cx="550" cy="100" r="57" fill="{bg}"/><path d="M120 350Q345 190 690 350V456H120Z" fill="{fg}"/><path d="M170 398Q370 275 650 386" fill="none" stroke="{bg}" stroke-width="2"/>',
        'warm-story': f'<rect width="810" height="456" fill="{bg}"/><rect x="110" y="55" width="340" height="275" rx="40" fill="{accent}" transform="rotate(-8 280 190)"/><rect x="360" y="65" width="310" height="270" rx="150" fill="{panel}"/><path d="M460 165Q500 200 540 165M590 165Q625 200 660 165M500 240Q560 295 625 240" stroke="{fg}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M180 200H355M270 115V285" stroke="{panel}" stroke-width="36" stroke-linecap="round"/>',
        'tech-grid': f'<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="{accent}" opacity=".18" fill="none"/></pattern></defs><rect width="810" height="456" fill="{bg}"/><rect width="810" height="456" fill="url(#grid)"/><g stroke="{accent}" fill="{panel}" stroke-width="3"><path d="M180 215H405V110H625M405 215V300H625" fill="none"/><rect x="65" y="155" width="180" height="120"/><circle cx="405" cy="215" r="47"/><rect x="590" y="55" width="150" height="105"/><rect x="590" y="250" width="150" height="105"/></g><g fill="{accent}" font-family="monospace" font-size="28"><text x="105" y="225">IN</text><text x="388" y="225">+</text><text x="622" y="120">RUN</text><text x="622" y="315">OUT</text></g>',
    }.get(theme['id'], f'<rect width="810" height="456" fill="{panel}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 456" role="img" aria-label="Ilustrasi grafis {html.escape(theme["name"])}">{art}</svg>'


def mrlabs_specimen(theme, number):
    """Build a 1080x1920 specimen using previews/creator.png + previews/creator-cutout.png and 5 toggleable effects."""
    css = mrlabs_css(theme).replace('assets/mrlabs/fonts/', 'fonts/')
    motion = mrlabs_motion(theme)
    is_th = bool(theme.get('talking_head'))
    caption_pos = 'below-face' if theme.get('caption_position') in ('chest-float', 'below-face') else theme.get('caption_position', 'bottom')
    default_portrait = 'true'
    transform = f'translate({motion.get("x",0)}px,{motion.get("y",0)}px) scale({motion.get("scale",1)}) rotate({motion.get("rotation",0)}deg)'
    label = mrlabs_bilingual('div', 'broll-label', ('BINGKAI / ' if theme.get('collection')=='fun' else 'ILUSTRASI / ')+theme['name'], ('FRAME / ' if theme.get('collection')=='fun' else 'ILLUSTRATION / ')+theme['name'])
    title = mrlabs_bilingual_title(theme)
    caption = mrlabs_bilingual('div', 'caption '+theme['caption_style'], theme['caption_id'], theme['caption_en'])
    broll_block = '' if is_th else f'<div class="broll">{mrlabs_art(theme,number)}{label}</div>'
    fx_html = mrlabs_effect_specimen_html(theme)
    return f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><style>{css}
    .preview-bg{{position:absolute;inset:0;background:var(--background);z-index:0}}
    #main[data-portrait="true"] .preview-bg{{background:transparent!important}}
    #main[data-portrait="false"] .preview-bg{{background:var(--background)!important;display:block!important}}
    /* Hide decorative B-roll card when any of the 5 talking-head effects are active so creator.png is unobstructed */
    #main:is([data-fx-orbit="true"],[data-fx-ui-world="true"],[data-fx-digital-zoom="true"],[data-fx-headline-wall="true"],[data-fx-pull-back-reveal="true"]) .broll{{display:none!important}}
    /* On non-talking-head themes, place title behind cutout when headline-wall or depth is tested, or keep clean */
    .specimen-index{{position:absolute;bottom:85px;right:85px;z-index:8;font:400 140px var(--heading-font);color:var(--accent);opacity:.22;pointer-events:none}}
    .specimen-note{{position:absolute;bottom:120px;left:65px;z-index:8;font:400 22px var(--label-font);letter-spacing:.1em;color:var(--muted);pointer-events:none}}
    .broll svg{{display:block;width:100%;height:100%;object-fit:cover}}
    .theme-placeholder{{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:35px 40px 85px;background:var(--panel);color:var(--foreground)}}
    .theme-placeholder span{{font:var(--heading-weight) 105px var(--heading-font);letter-spacing:-.04em}}
    .theme-placeholder small{{font:400 18px var(--body-font);letter-spacing:.12em;margin-top:8px}}
    #main:not([data-talking-head="true"]) .caption{{color:var(--highlight)}}
    .replay .title,.replay .caption,.replay .broll{{animation:entrance {theme['enter_seconds']}s cubic-bezier(.2,.8,.2,1) both}}
    .replay .broll{{animation-delay:.16s}}.replay .caption{{animation-delay:.3s}}
    @keyframes entrance{{from{{opacity:0;transform:{transform};filter:{motion.get('filter','none')}}}to{{opacity:1;transform:translate(0,0) scale(1) rotate(0);filter:none}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style></head><body><div id="main" data-theme="{theme['id']}" data-talking-head="{'true' if is_th else 'false'}" data-portrait="{default_portrait}" data-default-portrait="{default_portrait}" data-caption-pos="{caption_pos}" data-default-caption-pos="{caption_pos}"><div class="preview-bg"></div><img class="base" src="previews/creator.png" alt="Foto kreator"><div class="shade"></div><div class="art-direction"></div><img class="subject" src="previews/creator-cutout.png" alt="Cutout kreator">{fx_html}<div class="brand">MR LABS</div>{title}{broll_block}{caption}<div class="credit">by @maulanarahman_</div><div class="specimen-index">{number:02d}</div><div class="specimen-note">VISUAL STUDY<br>EDITION {theme.get("edition", 2):02d}</div></div></body></html>'''


def mrlabs_main():
    # Refresh the prompt generator when its content changes, including cached gallery tabs.
    script_version = hashlib.sha256((MRLABS_ROOT / 'assets/gallery.js').read_bytes()).hexdigest()[:12]
    themes = mrlabs_read(MRLABS_ROOT / 'assets/themes.json')['themes']
    assets = mrlabs_read(MRLABS_ROOT / 'assets/catalog.json')['assets']
    cards, fun_cards, pro_cards = [], [], []
    theme_pills = []
    specimens_map = {}

    # Default studio theme: obsidian-studio (Creator Hook)
    default_theme_id = 'obsidian-studio'

    for number, t in enumerate(themes, 1):
        raw_specimen = mrlabs_specimen(t, number)
        specimens_map[t['id']] = {
            "id": t["id"],
            "name": t["name"],
            "collection": t.get("collection", "original"),
            "tagline": t["tagline"],
            "background": t["background"],
            "accent": t["accent"],
            "talking_head": bool(t.get("talking_head")),
            "caption_position": "below-face" if t.get("caption_position") in ("chest-float", "below-face") else t.get("caption_position", "bottom"),
            "srcdoc": raw_specimen,
        }
        specimen = html.escape(raw_specimen, quote=True)
        swatches = ''.join(f'<i style="background:{t[key]}"></i>' for key in ('background', 'foreground', 'accent'))
        collection = t.get('collection')
        is_selected = (t['id'] == default_theme_id)
        target_cards = pro_cards if collection == 'pro' else (fun_cards if collection == 'fun' else cards)
        target_cards.append(
            f'<article class="package" data-card-theme="{t["id"]}" style="--accent:{t["accent"]}">'
            f'<div class="card-heading"><span>{number:02d}</span><span>{t["energy"].upper()}</span></div>'
            f'<div class="screen"><iframe title="{t["name"]} — contoh komposisi" tabindex="-1" srcdoc="{specimen}"></iframe></div>'
            f'<div class="details"><h2>{t["name"]}</h2><p class="tagline">{t["tagline"]}</p><p class="use">{t["use_for"]}</p>'
            f'<div class="swatches">{swatches}<span>{t["heading_font"]}</span></div>'
            f'<button class="pick" data-theme="{t["id"]}" aria-pressed="{"true" if is_selected else "false"}">{"Terpilih" if is_selected else "Pilih tema"}<span aria-hidden="true">↗</span></button>'
            f'</div></article>'
        )
        badge = "PRO" if collection == "pro" else ("FUN" if collection == "fun" else "ORIG")
        theme_pills.append(
            f'<button type="button" class="theme-chip" data-theme="{t["id"]}" aria-pressed="{"true" if is_selected else "false"}">'
            f'<i style="background:{t["accent"]}"></i><span>{t["name"]}</span><small>{badge}</small></button>'
        )

    effect_cards = []
    for fx_id, fx in MRLABS_EFFECTS.items():
        effect_cards.append(
            f'<label class="fx-chip" data-fx="{fx_id}">'
            f'<input type="checkbox" value="{fx_id}" class="fx-toggle">'
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

    document = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>MR Labs — Visual Studio &amp; Prompt Generator</title><link rel="stylesheet" href="fonts/fonts.css"><link rel="stylesheet" href="gallery.css"></head><body><main>
<nav><a class="wordmark" href="#">MR<span>↗</span>LABS</a><span>VIDEO EDITOR / INTERACTIVE STUDIO &amp; PROMPT GENERATOR</span><span class="edition">EDITION 04</span></nav>
<header>
  <div>
    <div class="kicker">STUDIO INTERAKTIF · BASE FOTO KREATOR ASLI + 5 EFEK VIRAL</div>
    <h1>Rancang gayamu.<br><span>Salin prompt-nya.</span></h1>
    <p>Pilih tema dari 15 paket visual, tentukan posisi caption (di bawah muka atau di atas kepala), aktifkan efek depth seperti <b>ORBIT</b>, <b>UI World</b>, <b>Digital Zoom</b>, <b>Headline Wall</b>, dan <b>Pull Back Reveal</b> langsung di atas foto aslimu, lalu salin prompt-nya.</p>
  </div>
  <div class="controls">
    <button id="language" type="button">Contoh: Indonesia</button>
    <button id="portrait" type="button" aria-pressed="false">Latar: Potrait Asli (Tanpa BG)</button>
    <button id="replay" type="button">↻ Putar ulang animasi</button>
    <small>Base: assets/previews/creator.png + 3D Cutout<br>Semua perubahan langsung tampil di layar kiri &amp; bawah</small>
  </div>
</header>

<section class="studio-builder" aria-label="Interactive Prompt Generator Studio">
  <div class="studio-preview-col">
    <div class="studio-monitor-head">
      <span class="kicker">LIVE PREVIEW · 1080×1920</span>
      <span id="studio-badge">Creator Hook · Di Bawah Muka</span>
    </div>
    <div class="screen studio-screen">
      <iframe id="studio-frame" title="Live Interactive Studio Preview" srcdoc="{default_srcdoc}"></iframe>
    </div>
  </div>

  <div class="studio-controls-col">
    <div class="builder-group">
      <div class="builder-label"><span>01 / PILIH TEMA VISUAL (15 TEMA)</span><small id="selected-theme-label">Creator Hook (obsidian-studio)</small></div>
      <div class="theme-chip-grid">{''.join(theme_pills)}</div>
    </div>

    <div class="builder-row-2">
      <div class="builder-group">
        <div class="builder-label"><span>02 / POSISI CAPTION</span><small>Sesuaikan dengan framing wajah</small></div>
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
        </div>
      </div>

      <div class="builder-group">
        <div class="builder-label"><span>03 / KONDISI LATAR VIDEO</span><small>Aturan otomatis potrait</small></div>
        <div class="pos-chip-grid" role="radiogroup" aria-label="Mode Background">
          <button type="button" class="bg-chip" data-bg-mode="portrait" aria-pressed="true">
            <strong>Video Sudah Potrait (Tanpa BG)</strong>
            <small>Gunakan ruang asli creator.png</small>
          </button>
          <button type="button" class="bg-chip" data-bg-mode="studio" aria-pressed="false">
            <strong>Non-Potrait (Latar Putih/Hitam Tema)</strong>
            <small>Cutout di atas latar Putih/Hitam tema</small>
          </button>
        </div>
      </div>
    </div>

    <div class="builder-group">
      <div class="builder-label">
        <span>04 / PILIH EFEK VIDEO (BISA PILIH BANYAK)</span>
        <button type="button" id="clear-fx" class="mini-btn">Reset Efek</button>
      </div>
      <div class="fx-chip-grid">{''.join(effect_cards)}</div>
    </div>

    <div class="builder-group prompt-box">
      <div class="builder-label">
        <span>05 / PROMPT GENERATOR &amp; CONFIG JSON</span>
        <span class="status" role="status" aria-live="polite">Siap disalin ke AI Agent</span>
      </div>
      <label for="prompt-output" class="sr-only">Prompt AI</label>
      <p class="asset-note">Prompt mengikuti pilihan di atas. Isi lokasi video dan profil, lalu lampirkan gambar referensi saat mengirim prompt. Rencana edit perlu disetujui sebelum produksi.</p>
      <textarea id="prompt-output" rows="6" readonly></textarea>
      <div class="prompt-actions">
        <button type="button" id="copy-prompt" class="primary-btn">📋 Salin Prompt AI ↗</button>
        <input id="config" readonly value='{{"theme":"obsidian-studio","caption_position":"below-face","effects":[],"language":"id"}}'>
        <button type="button" id="copy">Salin JSON ↗</button>
      </div>
    </div>
  </div>
</section>

<div class="collection-heading" id="pro"><div><span class="kicker">BARU / 11—15</span><h2>Pro Talking-Head. Depth Hook &amp; Floating Caption.</h2></div><p>Teks di atas &amp; belakang kepala presenter, caption melayang di bawah muka. Klik kartu mana saja untuk memuat ke Studio di atas.</p></div>
<section class="packages" aria-label="Lima tema Pro Influencer">{''.join(pro_cards)}</section>

<div class="collection-heading" id="fun"><div><span class="kicker">FUN / 06—10</span><h2>Fun, in every shape.</h2></div><p>Bingkai melengkung. Pola yang punya karakter.</p></div>
<section class="packages" aria-label="Lima tema Fun">{''.join(fun_cards)}</section>

<div class="collection-heading" id="original"><div><span class="kicker">ORIGINAL / 01—05</span><h2>Lima karakter pilihanmu.</h2></div><p>Koleksi editorial pertama yang tetap tersedia.</p></div>
<section class="packages" aria-label="Lima tema Original">{''.join(cards)}</section>

<div class="asset-header"><h2>Peralatan kreatif.</h2><p>Aset lokal. Siap dirangkai.</p></div>
<details class="asset-group"><summary>01 / Koleksi font · 12 keluarga + Helvetica lokal <span>+</span></summary><p class="asset-note">Poppins Bold (700), Roboto (400), dan Roboto Light (300) tersedia lokal. Helvetica memakai instalasi lokal berlisensi, dengan fallback Roboto jika tidak tersedia.</p><div class="font-shelf">{''.join(fonts)}</div></details>
<details class="asset-group"><summary>02 / Sepuluh aksen suara <span>+</span></summary><p class="asset-note">Kenney Interface Sounds · CC0. Efek mengikuti aksi dan tetap di bawah narasi.</p><div class="sound-shelf">{''.join(sounds)}</div></details>
<footer><span>MR LABS / MADE FOR YOUR NEXT IDEA.</span><p>Font <a href="https://github.com/google/fonts">Google Fonts / OFL</a> · SFX <a href="https://kenney.nl/assets/interface-sounds">Kenney / CC0</a> · <a href="catalog.json">Sumber &amp; lisensi</a></p><p>Base foto kreator: <code>assets/previews/creator.png</code> + <code>creator-cutout.png</code>.</p></footer>
</main>
<script>window.__MRLABS_SPECIMENS={specimens_json};</script>
<script src="gallery.js?v={script_version}"></script></body></html>'''
    target = MRLABS_ROOT / 'assets/theme-gallery.html'
    target.write_text(document, encoding='utf-8')
    print(target)


if __name__ == '__main__':
    mrlabs_main()
