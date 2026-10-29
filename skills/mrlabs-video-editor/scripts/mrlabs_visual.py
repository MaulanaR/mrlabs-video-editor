"""Data-driven HyperFrames composition, 5 viral talking-head effects, and local asset integration."""
import html
import json
from pathlib import Path
import shutil
from mrlabs_core import (MRLABS_ROOT, mrlabs_read, mrlabs_config, mrlabs_duration, mrlabs_probe,
                         mrlabs_caption_groups, mrlabs_validate_words, mrlabs_write, mrlabs_frames)
from mrlabs_broll import mrlabs_validate_broll

MRLABS_EFFECTS = {
    "orbit": {
        "id": "orbit",
        "name": "ORBIT 3D Cards",
        "summary_id": "Kartu UI & metrik berputar 3D mengelilingi tubuh (lewat di belakang & di depan subjek).",
        "summary_en": "3D floating UI & metric cards orbiting behind and in front of the speaker.",
        "uses_depth": True,
    },
    "ui-world": {
        "id": "ui-world",
        "name": "UI World Window",
        "summary_id": "Setengah atas layar menjadi window AI/aplikasi interaktif yang menjalankan langkah kerja.",
        "summary_en": "Top half transforms into an interactive AI workflow window while the speaker talks below.",
        "uses_depth": False,
    },
    "digital-zoom": {
        "id": "digital-zoom",
        "name": "Digital Zoom Punch-In",
        "summary_id": "Kamera punch-in halus (1.24x) ke wajah/gestur pada momen penekanan penting.",
        "summary_en": "Smooth programmatic camera punch-in (1.24x) on key emphasis moments.",
        "uses_depth": False,
    },
    "headline-wall": {
        "id": "headline-wall",
        "name": "Headline Wall",
        "summary_id": "Potongan koran & headline menempel satu per satu di dinding belakang presenter (depth layer).",
        "summary_en": "Newspaper clippings and highlighted headlines stick onto the wall behind the presenter.",
        "uses_depth": True,
    },
    "pull-back-reveal": {
        "id": "pull-back-reveal",
        "name": "Pull Back Reveal",
        "summary_id": "Kamera zoom-out memperlihatkan video sedang diputar di dalam timeline desktop video editor.",
        "summary_en": "Camera pulls back to reveal the video playing inside a desktop NLE timeline interface.",
        "uses_depth": False,
    },
}


def mrlabs_theme(theme_id):
    themes = mrlabs_read(MRLABS_ROOT / "assets/themes.json")["themes"]
    return next(theme for theme in themes if theme["id"] == theme_id)


def mrlabs_is_portrait(project=None, media=None, config=None):
    """Return True when source video already supports portrait (height > width)."""
    if config and config.get("portrait") is not None:
        return bool(config["portrait"])
    if project:
        project = Path(project)
        sources_file = project / "sources.json"
        if sources_file.exists():
            sources = mrlabs_read(sources_file)
            edl_file = project / "edl.json"
            clips = ([sources[seg["clip"]] for seg in mrlabs_read(edl_file) if seg.get("clip") in sources]
                     if edl_file.exists() else list(sources.values()))
            if clips:
                return all(int(clip["height"]) > int(clip["width"]) for clip in clips)
    if media and Path(media).exists():
        streams = mrlabs_probe(media).get("streams", [])
        video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
        if video and "width" in video and "height" in video:
            return int(video["height"]) > int(video["width"])
    return True


def mrlabs_head_top(project=None):
    """Return sampled top-of-head Y coordinate from head-samples.json when available."""
    if not project:
        return None
    samples_file = Path(project) / "head-samples.json"
    if not samples_file.exists():
        return None
    tops = [int(row["bounds"][1]) for row in mrlabs_read(samples_file) if row.get("bounds")]
    return min(tops) if tops else None


def mrlabs_caption_top(project=None, config=None, visual=None):
    """Compute safe Y coordinate for above-head captions (clamped to safe zone >= 220px)."""
    explicit = (visual or {}).get("caption_top") or (config or {}).get("caption_top")
    if explicit is not None:
        return max(220, min(1350, int(explicit)))
    head_y = mrlabs_head_top(project)
    if head_y is not None:
        return max(220, min(420, head_y - 150))
    return 310


def mrlabs_format_title_html(text, theme):
    """Format two-line talking-head hook titles as kicker + giant hero behind head."""
    if theme.get("talking_head") and "\n" in text:
        kicker, hero = text.split("\n", 1)
        return f'<span class="title-kicker">{html.escape(kicker)}</span><span class="title-hero">{html.escape(hero)}</span>'
    return html.escape(text)


def mrlabs_normalize_effects(visual=None, config=None, duration=6.0):
    """Normalize effects list from visual.json or config.json into validated effect specs."""
    raw = (visual or {}).get("effects")
    if raw is None and config:
        raw = config.get("effects")
    if not raw:
        return []
    normalized = []
    for item in raw:
        if isinstance(item, str):
            effect_id = item.strip().lower()
            spec = {"type": effect_id, "start": 0.0, "end": float(duration)}
        elif isinstance(item, dict):
            effect_id = str(item.get("type") or item.get("id") or "").strip().lower()
            spec = {
                "type": effect_id,
                "start": float(item.get("start", 0.0)),
                "end": float(item.get("end", duration)),
                **{k: v for k, v in item.items() if k not in ("type", "id", "start", "end")},
            }
        else:
            raise ValueError(f"Format effect tidak valid: {item}")
        if effect_id not in MRLABS_EFFECTS:
            raise ValueError(f"Effect '{effect_id}' tidak dikenal. Pilihan: {', '.join(MRLABS_EFFECTS)}")
        if not 0 <= spec["start"] < spec["end"] <= duration + 1e-6:
            raise ValueError(f"Rentang waktu effect '{effect_id}' di luar durasi video")
        normalized.append(spec)
    return normalized


def mrlabs_effect_specimen_html(theme=None):
    """Return the 5 viral effect layers so both gallery specimens and video builds can toggle/animate them."""
    return (
        '<div class="fx-layer" aria-hidden="true">'
        # 1. ORBIT (3D cards passing behind z=2 and in front of z=8 the subject z=3)
        '<div id="fx-orbit-1" class="fx-item fx-orbit-card card-1">'
        '<span class="orb-tag">● ORBIT METRIC 01</span>'
        '<strong class="orb-val">+14.2K</strong>'
        '<span class="orb-sub">Organic Reach · 7 Hari</span>'
        '</div>'
        '<div id="fx-orbit-2" class="fx-item fx-orbit-card card-2">'
        '<span class="orb-tag">● ORBIT WORKFLOW 02</span>'
        '<strong class="orb-val">98.4%</strong>'
        '<span class="orb-sub">Hook Hold Rate · AI Cut</span>'
        '</div>'
        '<div id="fx-orbit-3" class="fx-item fx-orbit-card card-3">'
        '<span class="orb-tag">● ORBIT SPEED 03</span>'
        '<strong class="orb-val">4.2×</strong>'
        '<span class="orb-sub">Lebih Cepat Tanpa Template</span>'
        '</div>'
        # 2. UI WORLD (Top-half interactive AI / Claude window)
        '<div id="fx-ui-world" class="fx-item fx-ui-world">'
        '<div class="fx-ui-bar">'
        '<div class="fx-ui-dots"><i></i><i></i><i></i></div>'
        '<span>claude-code — mrlabs-video-editor</span>'
        '<span class="fx-ui-badge">● UI WORLD LIVE</span>'
        '</div>'
        '<div class="fx-ui-prompt">&gt; Terapkan tema, potong jeda, pasang depth cutout &amp; sinkronkan caption...</div>'
        '<div class="fx-ui-steps">'
        '<div class="fx-ui-step"><b>STEP 01 · CUT</b><span>Silence &amp; filler dihapus</span></div>'
        '<div class="fx-ui-step"><b>STEP 02 · DEPTH</b><span>Subject cutout 30fps siap</span></div>'
        '<div class="fx-ui-step"><b>STEP 03 · RENDER</b><span>1080×1920 MP4 terverifikasi</span></div>'
        '</div>'
        '</div>'
        # 3. DIGITAL ZOOM HUD
        '<div id="fx-zoom-hud" class="fx-item fx-zoom-hud">'
        '<span class="fx-zoom-pill">⊕ DIGITAL ZOOM 1.24×</span>'
        '<span class="fx-zoom-pill">AF-C LOCKED</span>'
        '</div>'
        # 4. HEADLINE WALL (Behind subject at z-index: 2)
        '<div id="fx-hw-1" class="fx-item fx-headline-card hw-1">'
        '<small>THE CREATOR DISPATCH · EDISI PAGI</small>'
        '<strong>Workflow Video AI Pangkas Waktu Edit Hingga 84%</strong>'
        '</div>'
        '<div id="fx-hw-2" class="fx-item fx-headline-card hw-2">'
        '<small>TECH BRIEF · RISET RETENSI</small>'
        '<strong>Depth Hook di Belakang Kepala Naikkan Watch Time</strong>'
        '</div>'
        '<div id="fx-hw-3" class="fx-item fx-headline-card hw-3">'
        '<small>GROWTH INDEX · STUDI KASUS</small>'
        '<strong>14,000 Followers Baru Dari Konten Talking-Head Bersih</strong>'
        '</div>'
        '<div id="fx-hw-4" class="fx-item fx-headline-card hw-4">'
        '<small>STUDIO MONOCLE · VISUAL NOTE</small>'
        '<strong>Tanpa Template Norak: Tipografi Tajam &amp; Cutout Presisi</strong>'
        '</div>'
        # 5. PULL BACK REVEAL (Desktop NLE Editor Chrome + Timeline)
        '<div id="fx-pullback" class="fx-item fx-pullback">'
        '<div class="fx-pb-top">'
        '<span>MR LABS STUDIO NLE // PULL BACK REVEAL</span>'
        '<span>00:00:04:18 · 1080×1920 · 30 FPS</span>'
        '<span class="fx-pb-rec">● LIVE TIMELINE</span>'
        '</div>'
        '<div class="fx-pb-timeline">'
        '<div class="fx-pb-playhead"></div>'
        '<div class="fx-pb-ruler"><span>00:00</span><span>00:02</span><span>00:04</span><span>00:06</span><span>00:08</span></div>'
        '<div class="fx-pb-track">V3 · FX LAYER &amp; CAPTIONS <span>ACTIVE · GSAP 3.14</span></div>'
        '<div class="fx-pb-track">V2 · SUBJECT CUTOUT (VP9 ALPHA) <span>Z-INDEX 3 · LOCKED</span></div>'
        '<div class="fx-pb-track">V1 · A-ROLL CAMERA + AUDIO WAVEFORM <span>-14 LUFS · SYNCED</span></div>'
        '</div>'
        '</div>'
        '</div>'
    )


def mrlabs_copy_assets(project):
    target = Path(project) / "assets" / "mrlabs"
    for name in ("fonts", "sfx"):
        shutil.copytree(MRLABS_ROOT / "assets" / name, target / name, dirs_exist_ok=True)


def mrlabs_motion(theme):
    return {"rise": {"y": 36}, "punch": {"scale": 0.82, "rotation": -3},
            "focus": {"filter": "blur(7px)", "scale": 1.015}, "float": {"y": 46, "rotation": 2},
            "slide": {"x": -56}}[theme["motion"]]


def mrlabs_entrance(theme, role, cue_duration, full=False):
    # Keep the final tilt after GSAP normalizes CSS rotate into transform.
    tilt = 0 if full else theme[role + "_rotation"]
    initial = {"opacity": 0, **({} if full else mrlabs_motion(theme))}
    initial["rotation"] = initial.get("rotation", 0) + tilt
    final = {"opacity": 1, "y": 0, "x": 0, "scale": 1, "rotation": tilt, "filter": "blur(0px)",
             "duration": min(theme["enter_seconds"], cue_duration*.35),
             "ease": theme["ease"], "immediateRender": False}
    return initial, final


def mrlabs_css(theme, portrait=False, caption_top=310):
    font_css = (MRLABS_ROOT / "assets/fonts/fonts.css").read_text(encoding="utf-8").replace('url("', 'url("assets/mrlabs/fonts/')
    tokens = {}
    for key in ("background", "panel", "foreground", "muted", "accent", "ink",
                "caption_background", "caption_foreground", "highlight", "grade"):
        tokens[key.replace("_", "-")] = theme[key]
    for key in ("heading_font", "body_font", "label_font"):
        tokens[key.replace("_", "-")] = '"' + theme[key] + '"'
        if theme[key] == "Helvetica":
            tokens[key.replace("_", "-")] += ',"Roboto",sans-serif'
    for key in ("heading_weight", "caption_weight"):
        tokens[key.replace("_", "-")] = str(theme[key])
    for key in ("radius", "caption_size"):
        tokens[key.replace("_", "-")] = str(theme[key]) + "px"
    for key in ("title_rotation", "caption_rotation", "broll_rotation"):
        tokens[key.replace("_", "-")] = str(theme[key]) + "deg"
    # Condition: if the video already supports portrait, no theme background is needed.
    tokens["canvas-background"] = "transparent" if portrait else theme["background"]
    tokens["pattern"] = "none" if portrait else theme.get("pattern", "none")
    tokens["pattern-size"] = theme.get("pattern_size", "auto")
    tokens["caption-top"] = f"{int(caption_top)}px"
    variables = ":root{" + ";".join("--" + key + ":" + value for key, value in tokens.items()) + "}"
    return font_css + variables + (MRLABS_ROOT / "assets/render-themes.css").read_text(encoding="utf-8")


def mrlabs_build(project, theme_id=None, safe=False):
    project = Path(project).resolve()
    config = mrlabs_config(project)
    theme = mrlabs_theme(theme_id or config["theme"])
    media = project / "assets/aroll.mp4"
    portrait = mrlabs_is_portrait(project, media, config)
    duration = mrlabs_frames(media) / config["fps"]
    words = mrlabs_read(project / "words.json")
    mrlabs_validate_words(words, duration)
    visual_file = project / "visual.json"
    visual = mrlabs_read(visual_file) if visual_file.exists() else {}
    caption_pos = visual.get("caption_position") or config.get("caption_position") or theme.get("caption_position", "bottom")
    if caption_pos not in ("bottom", "above-head", "below-face", "chest-float"):
        raise ValueError("caption_position harus 'bottom', 'above-head', 'below-face', atau 'chest-float'")
    caption_top = mrlabs_caption_top(project, config, visual)
    has_cutout = (project / "assets/subject.webm").exists()
    caption_behind = bool(visual.get("caption_behind_subject", False))
    if caption_behind and not has_cutout:
        raise ValueError("Caption behind subject requires a verified subject.webm")
    effects = mrlabs_normalize_effects(visual, config, duration)
    broll_file = project / "broll.json"
    broll = mrlabs_validate_broll(mrlabs_read(broll_file).get("cues", []), duration, project) if broll_file.exists() else []
    mrlabs_copy_assets(project)
    markup, timeline, references = [], [], []
    markup.append(f'<video id="aroll" class="base" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{duration}" data-track-index="0"></video>')
    markup.append('<div class="shade"></div><div class="art-direction" aria-hidden="true"></div>')
    markup.append(f'<audio id="voice" src="assets/aroll.mp4" data-start="0" data-duration="{duration}" data-track-index="1" data-volume="1"></audio>')
    markup.append(f'<div id="brand" class="brand">{html.escape(config["brand"])}</div>')
    markup.append(f'<div id="credit" class="credit">{html.escape(config["credit"])}</div>')
    markup.append(mrlabs_effect_specimen_html(theme))
    timeline.append("tl.from('#brand',{opacity:0,y:16,duration:.35,ease:'power3.out'},.1);")
    timeline.append("tl.from('#credit',{opacity:0,y:10,duration:.4,ease:'sine.out'},.2);")
    caption_z = 2 if caption_behind else 9
    for index, group in enumerate(mrlabs_caption_groups(words)):
        name = f"caption-{index}"
        spans = " ".join(f'<span id="{name}-w{k}">{html.escape(word["text"])}</span>' for k, word in enumerate(group["words"]))
        markup.append(f'<div id="{name}" class="caption {theme["caption_style"]}" style="opacity:0;z-index:{caption_z}">{spans}</div>')
        initial, final = mrlabs_entrance(theme, "caption", group["end"]-group["start"])
        timeline.append(f"tl.fromTo('#{name}',{json.dumps(initial)},{json.dumps(final)},{group['start']});")
        for k, word in enumerate(group["words"]):
            timeline.append(f"tl.set('#{name}-w{k}',{{color:'{theme['highlight']}'}},{word['start']});")
        # End-of-caption state reset is required for seekable transcript-driven text.
        timeline.append(f"tl.set('#{name}',{{opacity:0}},{group['end']});")
    titles = visual.get("titles", [])
    used_behind = caption_behind or any(MRLABS_EFFECTS[fx["type"]]["uses_depth"] and has_cutout for fx in effects)
    for index, title in enumerate(titles):
        start, end = title["start"], title["end"]
        if not 0 <= start < end <= duration or len(title["text"]) > 100:
            raise ValueError("Invalid title length/timing")
        if "behind_subject" in title:
            behind = bool(title["behind_subject"])
            if behind and not has_cutout:
                raise ValueError("Title behind subject requires a verified subject.webm")
        else:
            behind = bool(theme.get("talking_head") and has_cutout)
        used_behind = used_behind or behind
        name = f"title-{index}"
        size = min(112, max(65, 1800 / max(1, len(title["text"]))))
        style_size = "" if (theme.get("talking_head") and "\n" in title["text"]) else f";font-size:{size}px"
        markup.append(f'<div id="{name}" class="title" style="opacity:0;z-index:{2 if behind else 7}{style_size}">{mrlabs_format_title_html(title["text"], theme)}</div>')
        initial, final = mrlabs_entrance(theme, "title", end-start)
        timeline.append(f"tl.fromTo('#{name}',{json.dumps(initial)},{json.dumps(final)},{start});")
        timeline.append(f"tl.set('#{name}',{{opacity:0}},{end});")
    if used_behind:
        markup.append(f'<video id="subject" class="subject" style="z-index:3" src="assets/subject.webm" muted playsinline data-start="0" data-duration="{duration}" data-track-index="2"></video>')
    # Wire timeline cues for the 5 viral effects when specified in visual.json / config.json
    fx_attrs = []
    for fx in effects:
        fx_type, start, end = fx["type"], fx["start"], fx["end"]
        fx_attrs.append(f'data-fx-{fx_type}="true"')
        if fx_type == "digital-zoom":
            targets = "['#aroll','#subject']" if used_behind else "['#aroll']"
            timeline.append(f"tl.fromTo({targets},{{scale:1,y:0}},{{scale:1.24,y:42,duration:.38,ease:'power3.out',immediateRender:false}},{start});")
            timeline.append(f"tl.to({targets},{{scale:1,y:0,duration:.42,ease:'power2.inOut'}},{max(start + 0.4, end - 0.42)});")
            timeline.append(f"tl.fromTo('#fx-zoom-hud',{{opacity:0}},{{opacity:1,duration:.2,immediateRender:false}},{start});")
            timeline.append(f"tl.set('#fx-zoom-hud',{{opacity:0}},{end});")
        elif fx_type == "ui-world":
            timeline.append(f"tl.fromTo('#fx-ui-world',{{opacity:0,y:-36,scale:.95}},{{opacity:1,y:0,scale:1,duration:.35,ease:'back.out(1.4)',immediateRender:false}},{start});")
            timeline.append(f"tl.set('#fx-ui-world',{{opacity:0}},{end});")
        elif fx_type == "headline-wall":
            for idx in range(1, 5):
                t_in = min(end - 0.1, start + (idx - 1) * 0.18)
                timeline.append(f"tl.fromTo('#fx-hw-{idx}',{{opacity:0,scale:1.25,y:-20}},{{opacity:1,scale:1,y:0,duration:.28,ease:'back.out(1.6)',immediateRender:false}},{t_in});")
                timeline.append(f"tl.set('#fx-hw-{idx}',{{opacity:0}},{end});")
        elif fx_type == "orbit":
            for idx in range(1, 4):
                timeline.append(f"tl.fromTo('#fx-orbit-{idx}',{{opacity:0}},{{opacity:1,duration:.25,immediateRender:false}},{start});")
                timeline.append(f"tl.set('#fx-orbit-{idx}',{{opacity:0}},{end});")
        elif fx_type == "pull-back-reveal":
            targets = "['#aroll','#subject']" if used_behind else "['#aroll']"
            timeline.append(f"tl.fromTo('#fx-pullback',{{opacity:0}},{{opacity:1,duration:.35,ease:'power2.out',immediateRender:false}},{start});")
            timeline.append(f"tl.fromTo({targets},{{scale:1,y:0}},{{scale:.82,y:-60,duration:.45,ease:'power3.out',immediateRender:false}},{start});")
            timeline.append(f"tl.to({targets},{{scale:1,y:0,duration:.35,ease:'power2.inOut'}},{max(start + 0.45, end - 0.35)});")
            timeline.append(f"tl.set('#fx-pullback',{{opacity:0}},{end});")
    for index, cue in enumerate(broll):
        target = project / "assets" / "broll" / f"broll-{index}{cue['path'].suffix.lower()}"
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.resolve() != cue["path"]:
            shutil.copy2(cue["path"], target)
        source = target.relative_to(project).as_posix()
        name, length = f"broll-{index}", cue["end"]-cue["start"]
        if cue["kind"] == "video":
            child = f'<video id="bmedia-{index}" src="{source}" muted playsinline data-start="{cue["start"]}" data-duration="{length}" data-media-start="{cue.get("source_in",0)}" data-track-index="{10+index}"></video>'
        else:
            child = f'<img src="{source}" alt="{html.escape(cue["anchor"], quote=True)}">'
        credit = html.escape(cue.get("credit", ""))
        label = ("Ilustrasi" if config["language"] != "en" else "Illustration") if cue["role"] == "illustration" else ""
        markup.append(f'<div id="{name}" class="broll {"full" if cue.get("mode")=="full" else ""}" style="opacity:0">{child}<div class="broll-label">{label} {credit}</div></div>')
        initial, final = mrlabs_entrance(theme, "broll", length, full=cue.get("mode")=="full")
        timeline.append(f"tl.fromTo('#{name}',{json.dumps(initial)},{json.dumps(final)},{cue['start']});")
        timeline.append(f"tl.set('#{name}',{{opacity:0}},{cue['end']});")
        references.append({key: value for key, value in cue.items() if key not in ("path", "kind")})
    catalog = mrlabs_read(MRLABS_ROOT / "assets/catalog.json")["assets"]
    sfx_ids = {row["id"] for row in catalog if row["kind"] == "sfx"}
    for index, cue in enumerate(visual.get("sfx", [])):
        if cue["id"] not in sfx_ids or not 0 <= cue["time"] < duration:
            raise ValueError("SFX id/time invalid")
        gain = float(cue.get("gain", theme["sfx_gain"]))
        if not 0 <= gain <= .3:
            raise ValueError("SFX gain must be 0..0.3; voice remains primary")
        path = project / f"assets/mrlabs/sfx/{cue['id']}.ogg"
        length = min(mrlabs_duration(path), duration-cue["time"])
        markup.append(f'<audio id="sfx-{index}" src="assets/mrlabs/sfx/{cue["id"]}.ogg" data-start="{cue["time"]}" data-duration="{length}" data-track-index="{100+index}" data-volume="{gain}"></audio>')
    if safe:
        markup.append('<div class="safe"></div>')
    language = "en" if config["language"] == "en" else "id"
    fx_attr_str = (" " + " ".join(dict.fromkeys(fx_attrs))) if fx_attrs else ""
    document = f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><title>MR Labs — {html.escape(theme['name'])}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{mrlabs_css(theme, portrait=portrait, caption_top=caption_top)}</style></head>
    <body><div id="main" data-theme="{theme['id']}" data-talking-head="{'true' if theme.get('talking_head') else 'false'}" data-portrait="{'true' if portrait else 'false'}" data-caption-pos="{caption_pos}"{fx_attr_str} data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">{''.join(markup)}</div>
    <script>const tl=gsap.timeline({{paused:true}});{''.join(timeline)}window.__timelines={{main:tl}};</script></body></html>'''
    (project / "index.html").write_text(document, encoding="utf-8")
    mrlabs_write(project / "hyperframes.json", {"width":1080,"height":1920,"fps":30})
    mrlabs_write(project / "build-report.json", {"theme": theme["id"], "theme_edition": theme.get("edition", 2),
                                                 "portrait_video": portrait, "background_applied": not portrait,
                                                 "caption_position": caption_pos,
                                                 "caption_top": caption_top if caption_pos == "above-head" else (1050 if caption_pos in ("below-face", "chest-float") else 1265),
                                                 "effects": [fx["type"] for fx in effects],
                                                 "duration": duration, "safe_guide": safe,
                                                 "broll": references, "captions": len(words), "needs_visual_audio_review": True})
    return project / "index.html"
