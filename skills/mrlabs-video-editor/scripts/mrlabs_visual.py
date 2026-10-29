"""Data-driven HyperFrames composition and local asset integration."""
import html
import json
from pathlib import Path
import shutil
from mrlabs_core import (MRLABS_ROOT, mrlabs_read, mrlabs_config, mrlabs_duration,
                         mrlabs_caption_groups, mrlabs_validate_words, mrlabs_write, mrlabs_frames)
from mrlabs_broll import mrlabs_validate_broll


def mrlabs_theme(theme_id):
    themes = mrlabs_read(MRLABS_ROOT / "assets/themes.json")["themes"]
    return next(theme for theme in themes if theme["id"] == theme_id)


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


def mrlabs_css(theme):
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
    tokens["pattern"] = theme.get("pattern", "none")
    tokens["pattern-size"] = theme.get("pattern_size", "auto")
    variables = ":root{" + ";".join("--" + key + ":" + value for key, value in tokens.items()) + "}"
    return font_css + variables + (MRLABS_ROOT / "assets/render-themes.css").read_text(encoding="utf-8")


def mrlabs_build(project, theme_id=None, safe=False):
    project = Path(project).resolve()
    config = mrlabs_config(project)
    theme = mrlabs_theme(theme_id or config["theme"])
    media = project / "assets/aroll.mp4"
    duration = mrlabs_frames(media) / config["fps"]
    words = mrlabs_read(project / "words.json")
    mrlabs_validate_words(words, duration)
    visual_file = project / "visual.json"
    visual = mrlabs_read(visual_file) if visual_file.exists() else {}
    broll_file = project / "broll.json"
    broll = mrlabs_validate_broll(mrlabs_read(broll_file).get("cues", []), duration, project) if broll_file.exists() else []
    mrlabs_copy_assets(project)
    markup, timeline, references = [], [], []
    markup.append(f'<video id="aroll" class="base" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{duration}" data-track-index="0"></video>')
    markup.append('<div class="shade"></div><div class="art-direction" aria-hidden="true"></div>')
    markup.append(f'<audio id="voice" src="assets/aroll.mp4" data-start="0" data-duration="{duration}" data-track-index="1" data-volume="1"></audio>')
    markup.append(f'<div id="brand" class="brand">{html.escape(config["brand"])}</div>')
    markup.append(f'<div id="credit" class="credit">{html.escape(config["credit"])}</div>')
    timeline.append("tl.from('#brand',{opacity:0,y:16,duration:.35,ease:'power3.out'},.1);")
    timeline.append("tl.from('#credit',{opacity:0,y:10,duration:.4,ease:'sine.out'},.2);")
    for index, group in enumerate(mrlabs_caption_groups(words)):
        name = f"caption-{index}"
        spans = " ".join(f'<span id="{name}-w{k}">{html.escape(word["text"])}</span>' for k, word in enumerate(group["words"]))
        markup.append(f'<div id="{name}" class="caption {theme["caption_style"]}" style="opacity:0">{spans}</div>')
        initial, final = mrlabs_entrance(theme, "caption", group["end"]-group["start"])
        timeline.append(f"tl.fromTo('#{name}',{json.dumps(initial)},{json.dumps(final)},{group['start']});")
        for k, word in enumerate(group["words"]):
            timeline.append(f"tl.set('#{name}-w{k}',{{color:'{theme['highlight']}'}},{word['start']});")
        # End-of-caption state reset is required for seekable transcript-driven text.
        timeline.append(f"tl.set('#{name}',{{opacity:0}},{group['end']});")
    titles = visual.get("titles", [])
    for index, title in enumerate(titles):
        start, end = title["start"], title["end"]
        if not 0 <= start < end <= duration or len(title["text"]) > 100:
            raise ValueError("Invalid title length/timing")
        behind = title.get("behind_subject", False)
        if behind and not (project / "assets/subject.webm").exists():
            raise ValueError("Title behind subject requires a verified subject.webm")
        name = f"title-{index}"
        size = min(112, max(65, 1800 / max(1, len(title["text"]))))
        markup.append(f'<div id="{name}" class="title" style="opacity:0;z-index:{2 if behind else 7};font-size:{size}px">{html.escape(title["text"])}</div>')
        initial, final = mrlabs_entrance(theme, "title", end-start)
        timeline.append(f"tl.fromTo('#{name}',{json.dumps(initial)},{json.dumps(final)},{start});")
        timeline.append(f"tl.set('#{name}',{{opacity:0}},{end});")
    if any(title.get("behind_subject") for title in titles):
        markup.append(f'<video id="subject" class="subject" style="z-index:3" src="assets/subject.webm" muted playsinline data-start="0" data-duration="{duration}" data-track-index="2"></video>')
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
    document = f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><title>MR Labs — {html.escape(theme['name'])}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{mrlabs_css(theme)}</style></head>
    <body><div id="main" data-theme="{theme['id']}" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">{''.join(markup)}</div>
    <script>const tl=gsap.timeline({{paused:true}});{''.join(timeline)}window.__timelines={{main:tl}};</script></body></html>'''
    (project / "index.html").write_text(document, encoding="utf-8")
    mrlabs_write(project / "hyperframes.json", {"width":1080,"height":1920,"fps":30})
    mrlabs_write(project / "build-report.json", {"theme": theme["id"], "theme_edition": theme.get("edition", 2), "duration": duration, "safe_guide": safe,
                                                 "broll": references, "captions": len(words), "needs_visual_audio_review": True})
    return project / "index.html"
