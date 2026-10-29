"""Build the offline theme gallery from the same CSS and tokens as video output."""
import html
from mrlabs_core import MRLABS_ROOT, mrlabs_read
from mrlabs_visual import mrlabs_css, mrlabs_motion


def mrlabs_bilingual(tag, class_name, indonesian, english):
    return f'<{tag} class="{class_name}" data-id="{html.escape(indonesian, quote=True)}" data-en="{html.escape(english, quote=True)}">{html.escape(indonesian)}</{tag}>'


def mrlabs_art(theme, number):
    """Original vector specimens; no fabricated statistics or sourced footage."""
    if theme.get("collection") == "fun":
        return '<div class="theme-placeholder"><span>B-roll</span><small>RUANG VISUAL / VISUAL SPACE</small></div>'
    bg, panel, fg, accent = (theme[k] for k in ('background','panel','foreground','accent'))
    art = {
        'signal-clean': f'<rect width="810" height="456" fill="{panel}"/><circle cx="570" cy="195" r="140" fill="{accent}"/><path d="M60 290V110H240V290ZM275 290V55H455V290Z" fill="{bg}"/><path d="M60 310H745" stroke="{fg}" stroke-width="3"/><text x="70" y="170" font-family="sans-serif" font-size="40" fill="{fg}">A</text><path d="M100 240H360L335 215M360 240L335 265" stroke="{fg}" stroke-width="8" fill="none"/>',
        'kinetic-punch': f'<rect width="810" height="456" fill="{panel}"/><path d="M410 10 445 110 535 55 510 155 625 160 545 230 625 300 510 295 535 400 445 345 410 445 375 345 285 400 310 295 195 300 275 230 195 160 310 155 285 55 375 110Z" fill="{accent}"/><path d="M395 100 465 100 420 205 475 205 355 335 390 235 340 235Z" fill="{bg}"/>',
        'editorial-noir': f'<rect width="810" height="456" fill="{panel}"/><path d="M210 430V210A195 195 0 0 1 600 210V430Z" fill="{accent}"/><circle cx="550" cy="100" r="57" fill="{bg}"/><path d="M120 350Q345 190 690 350V456H120Z" fill="{fg}"/><path d="M170 398Q370 275 650 386" fill="none" stroke="{bg}" stroke-width="2"/>',
        'warm-story': f'<rect width="810" height="456" fill="{bg}"/><rect x="110" y="55" width="340" height="275" rx="40" fill="{accent}" transform="rotate(-8 280 190)"/><rect x="360" y="65" width="310" height="270" rx="150" fill="{panel}"/><path d="M460 165Q500 200 540 165M590 165Q625 200 660 165M500 240Q560 295 625 240" stroke="{fg}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M180 200H355M270 115V285" stroke="{panel}" stroke-width="36" stroke-linecap="round"/>',
        'tech-grid': f'<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="{accent}" opacity=".18" fill="none"/></pattern></defs><rect width="810" height="456" fill="{bg}"/><rect width="810" height="456" fill="url(#grid)"/><g stroke="{accent}" fill="{panel}" stroke-width="3"><path d="M180 215H405V110H625M405 215V300H625" fill="none"/><rect x="65" y="155" width="180" height="120"/><circle cx="405" cy="215" r="47"/><rect x="590" y="55" width="150" height="105"/><rect x="590" y="250" width="150" height="105"/></g><g fill="{accent}" font-family="monospace" font-size="28"><text x="105" y="225">IN</text><text x="388" y="225">+</text><text x="622" y="120">RUN</text><text x="622" y="315">OUT</text></g>'
    }[theme['id']]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 456" role="img" aria-label="Ilustrasi grafis {html.escape(theme["name"])}">{art}</svg>'


def mrlabs_specimen(theme, number):
    css = mrlabs_css(theme).replace('assets/mrlabs/fonts/', 'fonts/')
    motion = mrlabs_motion(theme)
    transform = f'translate({motion.get("x",0)}px,{motion.get("y",0)}px) scale({motion.get("scale",1)}) rotate({motion.get("rotation",0)}deg)'
    label = mrlabs_bilingual('div', 'broll-label', ('BINGKAI / ' if theme.get('collection')=='fun' else 'ILUSTRASI / ')+theme['name'], ('FRAME / ' if theme.get('collection')=='fun' else 'ILLUSTRATION / ')+theme['name'])
    title = mrlabs_bilingual('div', 'title', theme['heading_id'], theme['heading_en'])
    caption = mrlabs_bilingual('div', 'caption '+theme['caption_style'], theme['caption_id'], theme['caption_en'])
    return f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><style>{css}
    .preview-bg{{position:absolute;inset:0;background:var(--background)}}
    .specimen-index{{position:absolute;bottom:85px;right:85px;font:400 160px var(--heading-font);color:var(--accent);opacity:.22}}
    .specimen-note{{position:absolute;bottom:120px;left:65px;font:400 23px var(--label-font);letter-spacing:.1em;color:var(--muted)}}
    .broll svg{{display:block;width:100%;height:100%;object-fit:cover}}
    .theme-placeholder{{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:35px 40px 85px;background:var(--panel);color:var(--foreground)}}
    .theme-placeholder span{{font:var(--heading-weight) 105px var(--heading-font);letter-spacing:-.04em}}
    .theme-placeholder small{{font:400 18px var(--body-font);letter-spacing:.12em;margin-top:8px}}
    .caption{{color:var(--highlight)}}
    .replay .title,.replay .caption,.replay .broll{{animation:entrance {theme['enter_seconds']}s cubic-bezier(.2,.8,.2,1) both}}
    .replay .broll{{animation-delay:.16s}}.replay .caption{{animation-delay:.3s}}
    @keyframes entrance{{from{{opacity:0;transform:{transform};filter:{motion.get('filter','none')}}}to{{opacity:1;transform:translate(0,0) scale(1) rotate(0);filter:none}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style></head><body><div id="main" data-theme="{theme['id']}"><div class="preview-bg"></div><div class="art-direction"></div><div class="brand">MR LABS</div>{title}<div class="broll">{mrlabs_art(theme,number)}{label}</div>{caption}<div class="credit">by @maulanarahman_</div><div class="specimen-index">{number:02d}</div><div class="specimen-note">VISUAL STUDY<br>EDITION {theme.get("edition", 2):02d}</div></div></body></html>'''


def mrlabs_main():
    themes = mrlabs_read(MRLABS_ROOT / 'assets/themes.json')['themes']
    assets = mrlabs_read(MRLABS_ROOT / 'assets/catalog.json')['assets']
    cards, fun_cards = [], []
    for number,t in enumerate(themes,1):
        specimen=html.escape(mrlabs_specimen(t,number),quote=True)
        swatches=''.join(f'<i style="background:{t[key]}"></i>' for key in ('background','foreground','accent'))
        target_cards = fun_cards if t.get('collection') == 'fun' else cards
        target_cards.append(f'''<article class="package" style="--accent:{t['accent']}"><div class="card-heading"><span>{number:02d}</span><span>{t['energy'].upper()}</span></div><div class="screen"><iframe title="{t['name']} — contoh komposisi" tabindex="-1" srcdoc="{specimen}"></iframe></div><div class="details"><h2>{t['name']}</h2><p class="tagline">{t['tagline']}</p><p class="use">{t['use_for']}</p><div class="swatches">{swatches}<span>{t['heading_font']}</span></div><button class="pick" data-theme="{t['id']}" aria-pressed="{'true' if number==1 else 'false'}">{'Terpilih' if number==1 else 'Pilih tema'}<span aria-hidden="true">↗</span></button></div></article>''')
    fonts=[]
    sounds=[]
    for asset in assets:
        if asset['kind']=='font':
            for sample in asset.get('specimens', [{'label':asset['family'],'weight':400}]):
                fonts.append(f'<div class="font-specimen"><small>{sample["label"]} · {sample["weight"]} · OFL</small><p style="font-family:\'{asset["family"]}\';font-weight:{sample["weight"]};font-synthesis:none">Ide kecil. Dampak besar.</p></div>')
        else:
            sounds.append(f'<label class="sound"><span>{asset["id"]}</span><audio controls preload="metadata" src="sfx/{asset["id"]}.ogg"></audio></label>')
    fonts.append('<div class="font-specimen helvetica"><small>Helvetica · 400 · lokal berlisensi</small><p style="font-family:Helvetica,Roboto,sans-serif">Ide kecil. Dampak besar.</p><small id="helvetica-status" role="status">Memeriksa font lokal; fallback: Roboto.</small></div>')
    document='''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>MR Labs — Visual Directions 03</title><link rel="stylesheet" href="fonts/fonts.css"><link rel="stylesheet" href="gallery.css"></head><body><main><nav><a class="wordmark" href="#">MR<span>↗</span>LABS</a><span>VIDEO EDITOR / DESIGN LIBRARY</span><span class="edition">EDITION 03</span></nav><header><div><div class="kicker">SEPULUH TEMA. BEBAS BEREKSPRESI.</div><h1>Cerita yang sama.<br><span>Rasa yang berbeda.</span></h1><p>Lima tema baru yang lebih fun: bentuk organik, pola playful, dan font pilihan baru. Lima tema sebelumnya tetap tersedia di koleksi Original.</p></div><div class="controls"><button id="language">Contoh: Indonesia</button><button id="replay">↻ Putar gerakan</button><small>Contoh ilustratif · 9:16<br>Geometri mengikuti preset render</small></div></header><div class="collection-heading" id="fun"><div><span class="kicker">BARU / 06—10</span><h2>Fun, in every shape.</h2></div><p>Bingkai melengkung. Pola yang punya karakter.</p></div><section class="packages" aria-label="Lima tema Fun">'''+''.join(fun_cards)+'''</section><div class="collection-heading" id="original"><div><span class="kicker">ORIGINAL / 01—05</span><h2>Lima karakter pilihanmu.</h2></div><p>Koleksi sebelumnya, tetap tersedia.</p></div><section class="packages" aria-label="Lima tema Original">'''+''.join(cards)+'''</section><section class="selection" aria-label="Konfigurasi tema"><div><span class="kicker">PILIHANMU</span><p class="status" role="status" aria-live="polite">Atlas Studio terpilih</p></div><label for="config" class="sr-only">Konfigurasi pilihan</label><input id="config" readonly value='{"theme":"signal-clean","language":"id"}'><button id="copy">Salin konfigurasi ↗</button></section><div class="asset-header"><h2>Peralatan kreatif.</h2><p>Aset lokal. Siap dirangkai.</p></div><details class="asset-group"><summary>01 / Koleksi font · 12 keluarga + Helvetica lokal <span>+</span></summary><p class="asset-note">Poppins Bold (700), Roboto (400), dan Roboto Light (300) tersedia lokal. Helvetica memakai instalasi lokal berlisensi, dengan fallback Roboto jika tidak tersedia.</p><div class="font-shelf">'''+''.join(fonts)+'''</div></details><details class="asset-group"><summary>02 / Sepuluh aksen suara <span>+</span></summary><p class="asset-note">Kenney Interface Sounds · CC0. Efek mengikuti aksi dan tetap di bawah narasi.</p><div class="sound-shelf">'''+''.join(sounds)+'''</div></details><footer><span>MR LABS / MADE FOR YOUR NEXT IDEA.</span><p>Font <a href="https://github.com/google/fonts">Google Fonts / OFL</a> · SFX <a href="https://kenney.nl/assets/interface-sounds">Kenney / CC0</a> · <a href="catalog.json">Sumber & lisensi</a></p><p>Ilustrasi desain, bukan footage pengguna. ID tema tetap kompatibel dengan proyek sebelumnya.</p></footer></main><script src="gallery.js"></script></body></html>'''
    target=MRLABS_ROOT/'assets/theme-gallery.html'
    target.write_text(document,encoding='utf-8')
    print(target)


if __name__=='__main__':
    mrlabs_main()
