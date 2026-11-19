"""Data-driven HyperFrames composition, 13 viral talking-head effects, and local asset integration."""
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
    "echo-wall": {
        "id": "echo-wall",
        "name": "Echo Repeat Stack",
        "summary_id": "Tumpukan 5 baris kata kunci berulang di belakang kepala dengan gradasi opacity (100% ke 18%).",
        "summary_en": "5-layer repeating keyword stack behind the speaker's head with decaying opacity.",
        "uses_depth": True,
    },
    "cover-story": {
        "id": "cover-story",
        "name": "Magazine Cover Story",
        "summary_id": "Frame berubah jadi sampul majalah: masthead serif raksasa di belakang kepala, edisi & barcode.",
        "summary_en": "Transforms the frame into an editorial magazine cover with giant serif masthead and barcode.",
        "uses_depth": True,
    },
    "grid-3x3": {
        "id": "grid-3x3",
        "name": "3×3 Reel Matrix",
        "summary_id": "Video utama mengecil ke tile tengah dikelilingi 8 tile video referensi dalam grid 3×3.",
        "summary_en": "Shrinks the main shot into the center tile while 8 surrounding reel tiles pop in around it.",
        "uses_depth": False,
    },
    "prompt-bar": {
        "id": "prompt-bar",
        "name": "AI Prompt & Tool Pills",
        "summary_id": "Kotak prompt Claude dengan tombol kirim oranye ↑ ditambah badge tool (FFmpeg, Remotion).",
        "summary_en": "Claude-style prompt input bar with orange send button and floating tool pills.",
        "uses_depth": False,
    },
    "grade-hud": {
        "id": "grade-hud",
        "name": "Colorist Tone Curve HUD",
        "summary_id": "Panel grafik kurva warna (Tone Curve) & slider saturasi/kontras di atas kepala.",
        "summary_en": "Live Tone Curve graph and color grading sliders floating above the speaker's head.",
        "uses_depth": False,
    },
    "side-stack": {
        "id": "side-stack",
        "name": "Side Block & Starburst",
        "summary_id": "Teks blok vertikal rata kiri/kanan di samping bahu + bintang geometris berputar di belakang.",
        "summary_en": "Left/right vertical condensed block text flanking the shoulders with a spinning starburst.",
        "uses_depth": True,
    },
    "tactile-board": {
        "id": "tactile-board",
        "name": "Tactile Sticky & Wireframe",
        "summary_id": "Sticky note checklist kuning & kartu sketsa wireframe kertas mengapit presenter.",
        "summary_en": "Tactile sticky-note checklist and paper wireframe storyboard card flanking the presenter.",
        "uses_depth": False,
    },
    "before-after": {
        "id": "before-after",
        "name": "Before / After Stage",
        "summary_id": "Kartu komparasi 🔴 Before mentah di kiri vs 🟢 After hasil edit di panggung utama.",
        "summary_en": "Portfolio comparison stage with a muted 🔴 Before card on the left and 🟢 After badge.",
        "uses_depth": False,
    },
    "kinetic-bounce": {
        "id": "kinetic-bounce",
        "name": "Kinetic Text Ping-Pong",
        "summary_id": "Posisi caption otomatis berpindah-pindah kiri ↔ kanan ↔ atas ↔ dada mengikuti ritme bicara.",
        "summary_en": "Captions dynamically jump left, right, upper corner, and center chest on every phrase.",
        "uses_depth": False,
    },
    "camera-handheld": {
        "id": "camera-handheld",
        "name": "Handheld Cinema Rig",
        "summary_id": "Gerakan kamera handheld organik + viewfinder REC sinema agar rekaman tripod terasa hidup.",
        "summary_en": "Organic handheld camera sway + cinema viewfinder HUD so static tripod footage feels alive.",
        "uses_depth": False,
    },
    "whip-pan": {
        "id": "whip-pan",
        "name": "Whip-Pan Snap Cut",
        "summary_id": "Kamera menyapu cepat horizontal (whip-pan) + kemiringan dinamis di setiap pergantian poin.",
        "summary_en": "Snappy horizontal camera whip-pans and subtle directional tilts on key phrase transitions.",
        "uses_depth": False,
    },
    "split-canvas": {
        "id": "split-canvas",
        "name": "Dynamic Split Stage",
        "summary_id": "Video presenter meluncur jadi bingkai kartu di bawah sementara setengah layar jadi panggung teks besar.",
        "summary_en": "Slides the presenter into a rounded lower frame while the upper half becomes a kinetic headline stage.",
        "uses_depth": False,
    },
    "spotlight-dim": {
        "id": "spotlight-dim",
        "name": "Cinematic Spotlight",
        "summary_id": "Latar meredup dramatis dengan sorotan radial & kamera dolly push-in lambat ke ekspresi wajah.",
        "summary_en": "Dramatic radial stage spotlight vignette paired with a slow cinematic dolly push-in.",
        "uses_depth": False,
    },
}

CAPTION_POSITIONS = (
    "bottom",
    "above-head",
    "below-face",
    "chest-float",
    "split-script",
    "hierarchy-glow",
    "shoulder-note",
    "dynamic-kinetic",
)

CAMERA_MOTIONS = (
    "none",
    "handheld-float",
    "dolly-push",
    "whip-pan",
    "dutch-tilt",
    "beat-punch",
    "split-cam",
)

CAPTION_CHOREOGRAPHIES = (
    "static",
    "ping-pong",
    "orbit-drift",
    "bento-scatter",
    "vertical-rail",
    "word-slam",
    "typewriter-hud",
)


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


def mrlabs_effect_specimen_html(theme=None, visual=None):
    """Return the 13 viral effect layers + shoulder callout so both gallery specimens and video builds can toggle/animate them."""
    custom_cards = (visual or {}).get("orbit_cards") or []
    if custom_cards:
        c1 = custom_cards[0]
        c2 = custom_cards[1] if len(custom_cards) > 1 else custom_cards[0]
        c3 = custom_cards[2] if len(custom_cards) > 2 else custom_cards[0]
        orbit_html = (
            f'<div id="fx-orbit-1" class="fx-item fx-orbit-card card-1 fx-orbit-img"><img src="{c1}" alt="Card 1"></div>'
            f'<div id="fx-orbit-2" class="fx-item fx-orbit-card card-2 fx-orbit-img"><img src="{c2}" alt="Card 2"></div>'
            f'<div id="fx-orbit-3" class="fx-item fx-orbit-card card-3 fx-orbit-img"><img src="{c3}" alt="Card 3"></div>'
        )
    else:
        orbit_html = (
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
        )
    echo_word = (visual or {}).get("echo_word") or "IMMEDIATELY"
    return (
        '<div class="fx-layer" aria-hidden="true">'
        + orbit_html +
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
        # 6. ECHO WALL (5-layer repeating word stack behind head)
        f'<div id="fx-echo-wall" class="fx-item fx-echo-wall">'
        f'<span>{html.escape(echo_word)}</span>'
        f'<span>{html.escape(echo_word)}</span>'
        f'<span>{html.escape(echo_word)}</span>'
        f'<span>{html.escape(echo_word)}</span>'
        f'<span>{html.escape(echo_word)}</span>'
        '</div>'
        # 7. COVER STORY (Editorial magazine masthead + barcode)
        '<div id="fx-cover-story" class="fx-item fx-cover-story">'
        '<div class="fx-cs-header">'
        '<div><span>ONE SENTENCE</span><b>The whole video, edited.</b></div>'
        '<div style="text-align:right"><span>ISSUE NO. 01 · 2026</span><b>Just Claude.</b></div>'
        '</div>'
        '<div class="fx-cs-masthead">CLAUDE</div>'
        '<div class="fx-cs-barcode"><div class="fx-cs-bars"></div><small>EDITED BY MR LABS</small></div>'
        '</div>'
        # 8. GRID 3x3 (3x3 reel matrix surrounding center tile)
        '<div id="fx-grid-3x3" class="fx-item fx-grid-3x3">'
        '<div class="fx-grid-cell"><small>REEL 01</small><strong>Creator Hook</strong><span>▶ 1.4M</span></div>'
        '<div class="fx-grid-cell"><small>REEL 02</small><strong>Neon Script</strong><span>▶ 890K</span></div>'
        '<div class="fx-grid-cell"><small>REEL 03</small><strong>Cover Story</strong><span>▶ 2.1M</span></div>'
        '<div class="fx-grid-cell"><small>REEL 04</small><strong>Echo Stack</strong><span>▶ 640K</span></div>'
        '<div class="fx-grid-cell center-hole"><small>LIVE SHOT</small><strong>CENTER TILE</strong><span>● ACTIVE</span></div>'
        '<div class="fx-grid-cell"><small>REEL 06</small><strong>Pixel Hybrid</strong><span>▶ 1.1M</span></div>'
        '<div class="fx-grid-cell"><small>REEL 07</small><strong>Tactile Desk</strong><span>▶ 950K</span></div>'
        '<div class="fx-grid-cell"><small>REEL 08</small><strong>Colorist HUD</strong><span>▶ 780K</span></div>'
        '<div class="fx-grid-cell"><small>REEL 09</small><strong>Sticker UI</strong><span>▶ 1.8M</span></div>'
        '</div>'
        # 9. PROMPT BAR (Claude prompt input box + tool pills)
        '<div id="fx-prompt-bar" class="fx-item fx-prompt-bar">'
        '<div class="fx-pb-input">'
        '<span>Shrink my shot into the centre tile of a 3×3 grid, then pop 8 reels around it...</span>'
        '<div class="fx-pb-send">↑</div>'
        '</div>'
        '<div class="fx-tool-pill tp-1"><i></i><span>▶ Remotion</span></div>'
        '<div class="fx-tool-pill tp-2"><i></i><span>⚡ FFmpeg</span></div>'
        '</div>'
        # 10. GRADE HUD (Tone Curve + Basic grading sliders)
        '<div id="fx-grade-hud" class="fx-item fx-grade-hud">'
        '<div class="fx-gh-curve">'
        '<small>TONE CURVE · LUT</small>'
        '<svg viewBox="0 0 200 120"><line x1="0" y1="120" x2="200" y2="0" stroke="rgba(255,255,255,.2)" stroke-dasharray="4 4"/>'
        '<path d="M0,115 C55,112 75,80 105,55 C140,26 168,8 200,5" fill="none" stroke="var(--accent)" stroke-width="4"/>'
        '<circle cx="62" cy="92" r="5" fill="#fff"/><circle cx="142" cy="28" r="5" fill="#fff"/></svg>'
        '</div>'
        '<div class="fx-gh-sliders">'
        '<div class="fx-gh-row"><span>Highlights</span><div class="fx-gh-bar"><i style="left:32%"></i></div><span>-35</span></div>'
        '<div class="fx-gh-row"><span>Blacks</span><div class="fx-gh-bar"><i style="left:64%"></i></div><span>+12</span></div>'
        '<div class="fx-gh-row"><span>Saturation</span><div class="fx-gh-bar"><i style="left:38%"></i></div><span>-15%</span></div>'
        '<div class="fx-gh-row"><span>Vignette</span><div class="fx-gh-bar"><i style="left:72%"></i></div><span>+18</span></div>'
        '</div>'
        '</div>'
        # 11. SIDE STACK (Vertical side block text + spinning starburst)
        '<div id="fx-side-stack" class="fx-item fx-side-stack">'
        '<div class="fx-ss-star">✳</div>'
        '<div class="fx-ss-left">IMPORT<br>YOUR<br>CLIP</div>'
        '<div class="fx-ss-right">AND AI<br>HANDLES<br>THE REST</div>'
        '</div>'
        # 12. TACTILE BOARD (Sticky note checklist + wireframe sketch card)
        '<div id="fx-tactile-board" class="fx-item fx-tactile-board">'
        '<div class="fx-tb-wire"><small>📌 STORYBOARD · 1–2 MONTHS</small><div class="fx-tb-wire-box">▶ WIREFRAME</div></div>'
        '<div class="fx-tb-note"><span>✓ concept</span><span>✓ story</span><span>✓ style</span><span>✓ final cut</span></div>'
        '</div>'
        # 13. BEFORE / AFTER STAGE (Split comparison stage)
        '<div id="fx-before-after" class="fx-item fx-before-after">'
        '<div class="fx-ba-pill-before"><i></i><span>Before</span></div>'
        '<div class="fx-ba-before"><img src="previews/creator.png" onerror="this.style.display=\'none\'" alt="Before raw"></div>'
        '<div class="fx-ba-pill-after"><i></i><span>After · Pro Edit</span></div>'
        '</div>'
        # Shoulder callout note (for shoulder-note mode)
        '<div id="fx-shoulder-callout" class="fx-shoulder-callout">'
        '<span>dikerjakan sekitar</span><b>3–4 bulan sebelumnya</b><span>secara terjadwal</span>'
        '</div>'
        # 14. KINETIC BOUNCE (Dynamic shifting kinetic chips showing alternating positions)
        '<div id="fx-kinetic-bounce" class="fx-item fx-kinetic-bounce">'
        '<div class="fx-kb-tag kb-left">01 · KIRI BAHU</div>'
        '<div class="fx-kb-tag kb-right">02 · KANAN BAHU</div>'
        '<div class="fx-kb-tag kb-center">03 · CENTER PUNCH</div>'
        '</div>'
        # 15. CAMERA HANDHELD (Cinema viewfinder brackets + REC indicator + live lens metadata)
        '<div id="fx-camera-handheld" class="fx-item fx-camera-handheld">'
        '<div class="fx-ch-corner tl"></div><div class="fx-ch-corner tr"></div>'
        '<div class="fx-ch-corner bl"></div><div class="fx-ch-corner br"></div>'
        '<div class="fx-ch-top"><span class="fx-ch-rec">● REC · 24MM F/1.4</span><span>ISO 400 · HANDHELD RIG</span></div>'
        '<div class="fx-ch-bottom"><span>AF-TRACK: FACE</span><span>STABILIZER: ORGANIC</span></div>'
        '</div>'
        # 16. WHIP PAN (Directional speed streak + motion HUD indicator)
        '<div id="fx-whip-pan" class="fx-item fx-whip-pan">'
        '<div class="fx-wp-streaks"><i></i><i></i><i></i></div>'
        '<div class="fx-wp-badge">⚡ WHIP-PAN DIRECTOR · AUTO CUT</div>'
        '</div>'
        # 17. SPLIT CANVAS (Upper kinetic typography stage while video slides to lower card)
        '<div id="fx-split-canvas" class="fx-item fx-split-canvas">'
        '<div class="fx-sc-stage">'
        '<span class="fx-sc-kicker">● DYNAMIC SPLIT STAGE · AI KEYNOTE</span>'
        '<strong class="fx-sc-headline">TEKS BERGERAK.<br>KAMERA MENGIKUTI.</strong>'
        '<div class="fx-sc-pills"><span>01 / HOOK</span><span>02 / CAMERA</span><span>03 / RETENTION</span></div>'
        '</div>'
        '</div>'
        # 18. SPOTLIGHT DIM (Radial cinematic stage spotlight overlay)
        '<div id="fx-spotlight-dim" class="fx-item fx-spotlight-dim">'
        '<div class="fx-sl-vignette"></div>'
        '<div class="fx-sl-badge">◉ SPOTLIGHT FOCUS · DOLLY IN</div>'
        '</div>'
        '</div>'
    )


def mrlabs_caption_slot(choreography, index):
    """Return dynamic (top, left, width, align, rotation, extra_class) for a caption group index."""
    patterns = {
        "ping-pong": [
            (960, 48, 520, "left", -2, "choreo-left"),
            (880, 512, 520, "right", 2, "choreo-right"),
            (1070, 50, 980, "center", 0, "choreo-center"),
            (520, 48, 490, "left", -1.5, "choreo-upper-left"),
        ],
        "orbit-drift": [
            (1050, 50, 980, "center", 0, "choreo-center"),
            (540, 530, 500, "right", 1.5, "choreo-upper-right"),
            (1140, 48, 560, "left", -1.5, "choreo-lower-left"),
            (320, 65, 950, "center", 0, "choreo-top"),
        ],
        "bento-scatter": [
            (1020, 52, 560, "left", -1.5, "choreo-pill"),
            (490, 488, 540, "right", 1.5, "choreo-pill"),
            (1160, 120, 840, "center", 0, "choreo-pill"),
            (500, 52, 540, "left", -1, "choreo-pill"),
        ],
        "vertical-rail": [
            (1040, 50, 980, "center", 0, "choreo-center"),
            (480, 875, 160, "center", 0, "choreo-rail-right"),
            (1040, 50, 980, "center", 0, "choreo-center"),
            (480, 45, 160, "center", 0, "choreo-rail-left"),
        ],
        "word-slam": [
            (980, 50, 980, "center", -3, "choreo-slam"),
            (520, 48, 560, "left", 3, "choreo-slam"),
            (1120, 472, 560, "right", -2.5, "choreo-slam"),
            (310, 65, 950, "center", 2, "choreo-slam"),
        ],
        "typewriter-hud": [
            (1060, 50, 980, "center", 0, "choreo-hud"),
            (325, 65, 950, "center", 0, "choreo-hud"),
            (1020, 48, 580, "left", 0, "choreo-hud"),
            (1020, 452, 580, "right", 0, "choreo-hud"),
        ],
    }
    slots = patterns.get(choreography)
    if not slots:
        return None
    return slots[index % len(slots)]


def mrlabs_camera_timeline(camera_motion, targets, duration, groups):
    """Return GSAP timeline snippets for continuous or phrase-synced camera movements."""
    if not camera_motion or camera_motion == "none" or duration <= 0:
        return []
    lines = []
    if camera_motion == "handheld-float":
        step = 1.6
        t = 0.0
        idx = 0
        waypoints = [
            (1.06, 14, -10, 0.7),
            (1.075, -12, 8, -0.8),
            (1.055, 10, 12, 0.5),
            (1.07, -14, -8, -0.6),
        ]
        lines.append(f"tl.set({targets},{{scale:1.06,x:0,y:0,rotation:0}},0);")
        while t < duration:
            sc, dx, dy, rot = waypoints[idx % len(waypoints)]
            seg = min(step, duration - t)
            lines.append(f"tl.to({targets},{{scale:{sc},x:{dx},y:{dy},rotation:{rot},duration:{seg:.2f},ease:'sine.inOut'}},{t:.2f});")
            t += step
            idx += 1
    elif camera_motion == "dolly-push":
        lines.append(f"tl.fromTo({targets},{{scale:1.0,y:0}},{{scale:1.18,y:28,duration:{duration:.2f},ease:'none',immediateRender:false}},0);")
    elif camera_motion == "whip-pan":
        beats = [g["start"] for g in groups[1::2]] or [round(duration * 0.33, 2), round(duration * 0.66, 2)]
        lines.append(f"tl.set({targets},{{scale:1.08,x:0,rotation:0}},0);")
        for idx, beat in enumerate(beats):
            direction = 1 if idx % 2 == 0 else -1
            lines.append(f"tl.to({targets},{{x:{direction * 58},rotation:{direction * 1.8},scale:1.14,duration:.14,ease:'power3.in'}},{max(0.0, beat - 0.14):.2f});")
            lines.append(f"tl.to({targets},{{x:0,rotation:0,scale:1.08,duration:.28,ease:'power3.out'}},{beat:.2f});")
    elif camera_motion == "dutch-tilt":
        beats = [g["start"] for g in groups[::2]] or [0.0, round(duration * 0.5, 2)]
        for idx, beat in enumerate(beats):
            angle = -3.2 if idx % 2 == 0 else 3.2
            lines.append(f"tl.to({targets},{{scale:1.13,rotation:{angle},y:14,duration:.36,ease:'power2.out'}},{beat:.2f});")
    elif camera_motion == "beat-punch":
        beats = [g["start"] for g in groups] or [0.0, round(duration * 0.4, 2), round(duration * 0.75, 2)]
        scales = [1.0, 1.14, 1.04, 1.18]
        for idx, beat in enumerate(beats):
            sc = scales[idx % len(scales)]
            dy = int((sc - 1.0) * 160)
            lines.append(f"tl.to({targets},{{scale:{sc},y:{dy},duration:.24,ease:'back.out(1.4)'}},{beat:.2f});")
    elif camera_motion == "split-cam":
        split_in = min(0.6, duration * 0.15)
        split_out = max(split_in + 0.5, duration - 0.6)
        lines.append(f"tl.to({targets},{{scale:.72,y:340,borderRadius:'36px',duration:.45,ease:'power3.out'}},{split_in:.2f});")
        lines.append(f"tl.to({targets},{{scale:1.0,y:0,borderRadius:'0px',duration:.42,ease:'power2.inOut'}},{split_out:.2f});")
    return lines


def mrlabs_copy_assets(project):
    target = Path(project) / "assets" / "mrlabs"
    for name in ("fonts", "sfx"):
        shutil.copytree(MRLABS_ROOT / "assets" / name, target / name, dirs_exist_ok=True)


def mrlabs_motion(theme):
    return {"rise": {"y": 36}, "punch": {"scale": 0.82, "rotation": -3},
            "focus": {"filter": "blur(7px)", "scale": 1.015}, "float": {"y": 46, "rotation": 2},
            "slide": {"x": -56}, "glide": {"y": 24, "scale": 0.96}}[theme["motion"]]


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
    if caption_pos not in CAPTION_POSITIONS:
        raise ValueError(f"caption_position harus salah satu dari: {', '.join(CAPTION_POSITIONS)}")
    camera_motion = visual.get("camera_motion") or config.get("camera_motion") or theme.get("camera_motion", "none")
    if camera_motion not in CAMERA_MOTIONS:
        raise ValueError(f"camera_motion harus salah satu dari: {', '.join(CAMERA_MOTIONS)}")
    caption_choreography = visual.get("caption_choreography") or config.get("caption_choreography") or theme.get("caption_choreography", "static")
    if caption_choreography not in CAPTION_CHOREOGRAPHIES:
        raise ValueError(f"caption_choreography harus salah satu dari: {', '.join(CAPTION_CHOREOGRAPHIES)}")
    caption_top = mrlabs_caption_top(project, config, visual)
    has_cutout = (project / "assets/subject.webm").exists()
    caption_behind = bool(visual.get("caption_behind_subject", False))
    if caption_behind and not has_cutout:
        raise ValueError("Caption behind subject requires a verified subject.webm")
    effects = mrlabs_normalize_effects(visual, config, duration)
    effect_types = {fx["type"] for fx in effects}
    if (caption_pos == "dynamic-kinetic" or "kinetic-bounce" in effect_types) and caption_choreography == "static":
        caption_choreography = "ping-pong"
    broll_file = project / "broll.json"
    broll = mrlabs_validate_broll(mrlabs_read(broll_file).get("cues", []), duration, project) if broll_file.exists() else []
    mrlabs_copy_assets(project)
    markup, timeline, references = [], [], []
    markup.append(f'<video id="aroll" class="base" src="assets/aroll.mp4" muted playsinline data-start="0" data-duration="{duration}" data-track-index="0"></video>')
    markup.append('<div class="shade"></div><div class="art-direction" aria-hidden="true"></div>')
    markup.append(f'<audio id="voice" src="assets/aroll.mp4" data-start="0" data-duration="{duration}" data-track-index="1" data-volume="1"></audio>')
    markup.append(f'<div id="brand" class="brand">{html.escape(config["brand"])}</div>')
    markup.append(f'<div id="credit" class="credit">{html.escape(config["credit"])}</div>')
    markup.append(mrlabs_effect_specimen_html(theme, visual=visual))
    timeline.append("tl.from('#brand',{opacity:0,y:16,duration:.35,ease:'power3.out'},.1);")
    timeline.append("tl.from('#credit',{opacity:0,y:10,duration:.4,ease:'sine.out'},.2);")
    caption_z = 2 if caption_behind else 9
    groups = mrlabs_caption_groups(words)
    for index, group in enumerate(groups):
        name = f"caption-{index}"
        spans = " ".join(f'<span id="{name}-w{k}">{html.escape(word["text"])}</span>' for k, word in enumerate(group["words"]))
        slot = mrlabs_caption_slot(caption_choreography, index) if caption_choreography != "static" else None
        extra_cls = f" {slot[5]}" if slot else ""
        slot_style = f";top:{slot[0]}px;left:{slot[1]}px;width:{slot[2]}px;text-align:{slot[3]}" if slot else ""
        markup.append(f'<div id="{name}" class="caption {theme["caption_style"]}{extra_cls}" style="opacity:0;z-index:{caption_z}{slot_style}">{spans}</div>')
        initial, final = mrlabs_entrance(theme, "caption", group["end"]-group["start"])
        if slot and slot[4]:
            initial["rotation"] = initial.get("rotation", 0) + slot[4]
            final["rotation"] = slot[4]
        timeline.append(f"tl.fromTo('#{name}',{json.dumps(initial)},{json.dumps(final)},{group['start']});")
        for k, word in enumerate(group["words"]):
            timeline.append(f"tl.set('#{name}-w{k}',{{color:'{theme['highlight']}'}},{word['start']});")
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

    cam_targets = "['#aroll','#subject']" if used_behind else "['#aroll']"
    if camera_motion != "none":
        timeline.extend(mrlabs_camera_timeline(camera_motion, cam_targets, duration, groups))

    # Wire timeline cues for all 18 viral & kinetic effects when specified in visual.json / config.json
    timeline.append(
        "tl.set(['.fx-orbit-card','#fx-ui-world','#fx-zoom-hud','.fx-headline-card','#fx-pullback',"
        "'#fx-echo-wall','#fx-cover-story','#fx-grid-3x3','#fx-prompt-bar','#fx-grade-hud',"
        "'#fx-side-stack','#fx-tactile-board','#fx-before-after','#fx-profile-card',"
        "'#fx-kinetic-bounce','#fx-camera-handheld','#fx-whip-pan','#fx-split-canvas','#fx-spotlight-dim'],{display:'none',opacity:0},0);"
    )
    simple_block_fx = {
        "echo-wall": ("#fx-echo-wall", "flex"),
        "cover-story": ("#fx-cover-story", "block"),
        "prompt-bar": ("#fx-prompt-bar", "block"),
        "grade-hud": ("#fx-grade-hud", "grid"),
        "side-stack": ("#fx-side-stack", "block"),
        "tactile-board": ("#fx-tactile-board", "block"),
        "before-after": ("#fx-before-after", "block"),
        "kinetic-bounce": ("#fx-kinetic-bounce", "block"),
    }
    for fx in effects:
        fx_type, start, end = fx["type"], fx["start"], fx["end"]
        if fx_type == "digital-zoom":
            targets = cam_targets
            timeline.append(f"tl.set('#fx-zoom-hud',{{display:'flex',opacity:0}},{start});")
            timeline.append(f"tl.to('#fx-zoom-hud',{{opacity:1,duration:.2}},{start});")
            timeline.append(f"tl.fromTo({targets},{{scale:1,y:0}},{{scale:1.24,y:42,duration:.38,ease:'power3.out',immediateRender:false}},{start});")
            timeline.append(f"tl.to({targets},{{scale:1,y:0,duration:.42,ease:'power2.inOut'}},{max(start + 0.4, end - 0.42)});")
            timeline.append(f"tl.to('#fx-zoom-hud',{{opacity:0,duration:.2}},{max(start + 0.3, end - 0.2)});")
            timeline.append(f"tl.set('#fx-zoom-hud',{{display:'none'}},{end});")
        elif fx_type == "camera-handheld":
            timeline.append(f"tl.set('#fx-camera-handheld',{{display:'block',opacity:0}},{start});")
            timeline.append(f"tl.to('#fx-camera-handheld',{{opacity:1,duration:.3}},{start});")
            if camera_motion == "none":
                timeline.extend(mrlabs_camera_timeline("handheld-float", cam_targets, end - start, groups))
            timeline.append(f"tl.to('#fx-camera-handheld',{{opacity:0,duration:.25}},{max(start + 0.4, end - 0.25)});")
            timeline.append(f"tl.set('#fx-camera-handheld',{{display:'none'}},{end});")
        elif fx_type == "whip-pan":
            timeline.append(f"tl.set('#fx-whip-pan',{{display:'block',opacity:0}},{start});")
            timeline.append(f"tl.to('#fx-whip-pan',{{opacity:1,duration:.22}},{start});")
            if camera_motion == "none":
                timeline.extend(mrlabs_camera_timeline("whip-pan", cam_targets, end - start, groups))
            timeline.append(f"tl.to('#fx-whip-pan',{{opacity:0,duration:.22}},{max(start + 0.4, end - 0.22)});")
            timeline.append(f"tl.set('#fx-whip-pan',{{display:'none'}},{end});")
        elif fx_type == "split-canvas":
            timeline.append(f"tl.set('#fx-split-canvas',{{display:'block',opacity:0,y:-24}},{start});")
            timeline.append(f"tl.to('#fx-split-canvas',{{opacity:1,y:0,duration:.38,ease:'power3.out'}},{start});")
            timeline.append(f"tl.to({cam_targets},{{scale:.72,y:340,borderRadius:'36px',duration:.45,ease:'power3.out'}},{start});")
            timeline.append(f"tl.to({cam_targets},{{scale:1,y:0,borderRadius:'0px',duration:.4,ease:'power2.inOut'}},{max(start + 0.5, end - 0.4)});")
            timeline.append(f"tl.to('#fx-split-canvas',{{opacity:0,y:-16,duration:.28}},{max(start + 0.45, end - 0.28)});")
            timeline.append(f"tl.set('#fx-split-canvas',{{display:'none'}},{end});")
        elif fx_type == "spotlight-dim":
            timeline.append(f"tl.set('#fx-spotlight-dim',{{display:'block',opacity:0}},{start});")
            timeline.append(f"tl.to('#fx-spotlight-dim',{{opacity:1,duration:.45,ease:'sine.out'}},{start});")
            if camera_motion == "none":
                timeline.append(f"tl.to({cam_targets},{{scale:1.15,y:24,duration:{max(0.5, end - start):.2f},ease:'none'}},{start});")
            timeline.append(f"tl.to('#fx-spotlight-dim',{{opacity:0,duration:.35}},{max(start + 0.5, end - 0.35)});")
            timeline.append(f"tl.set('#fx-spotlight-dim',{{display:'none'}},{end});")
        elif fx_type == "ui-world":
            timeline.append(f"tl.set('#fx-ui-world',{{display:'flex',opacity:0,y:-36,scale:.95}},{start});")
            timeline.append(f"tl.to('#fx-ui-world',{{opacity:1,y:0,scale:1,duration:.35,ease:'back.out(1.4)'}},{start});")
            timeline.append(f"tl.to('#fx-ui-world',{{opacity:0,y:-20,scale:.95,duration:.25}},{max(start + 0.4, end - 0.25)});")
            timeline.append(f"tl.set('#fx-ui-world',{{display:'none'}},{end});")
        elif fx_type == "headline-wall":
            timeline.append(f"tl.set('.fx-headline-card',{{display:'block',opacity:0}},{start});")
            for idx in range(1, 5):
                t_in = min(end - 0.1, start + (idx - 1) * 0.18)
                timeline.append(f"tl.fromTo('#fx-hw-{idx}',{{opacity:0,scale:1.25,y:-20}},{{opacity:1,scale:1,y:0,duration:.28,ease:'back.out(1.6)',immediateRender:false}},{t_in});")
            timeline.append(f"tl.to('.fx-headline-card',{{opacity:0,duration:.25}},{max(start + 0.6, end - 0.25)});")
            timeline.append(f"tl.set('.fx-headline-card',{{display:'none'}},{end});")
        elif fx_type == "orbit":
            t_mid = start + (end - start) * 0.48
            dur1 = (end - start) * 0.48
            dur2 = (end - start) * 0.52
            timeline.append(f"tl.set('#fx-orbit-1',{{display:'flex',opacity:0,x:40,y:-20,scale:.82,zIndex:2}},{start});")
            timeline.append(f"tl.to('#fx-orbit-1',{{opacity:1,duration:.3}},{start});")
            timeline.append(f"tl.to('#fx-orbit-1',{{x:180,y:25,scale:.96,duration:{dur1:.2f},ease:'power1.inOut'}},{start});")
            timeline.append(f"tl.set('#fx-orbit-1',{{zIndex:8}},{t_mid:.2f});")
            timeline.append(f"tl.to('#fx-orbit-1',{{x:370,y:60,scale:1.05,duration:{dur2:.2f},ease:'power1.out'}},{t_mid:.2f});")
            timeline.append(f"tl.to('#fx-orbit-1',{{opacity:0,scale:.9,duration:.25}},{end - 0.25:.2f});")
            timeline.append(f"tl.set('#fx-orbit-1',{{display:'none'}},{end});")

            timeline.append(f"tl.set('#fx-orbit-2',{{display:'flex',opacity:0,x:380,y:60,scale:1.05,zIndex:8}},{start});")
            timeline.append(f"tl.to('#fx-orbit-2',{{opacity:1,duration:.3}},{start});")
            timeline.append(f"tl.to('#fx-orbit-2',{{x:560,y:20,scale:.95,duration:{dur1:.2f},ease:'power1.inOut'}},{start});")
            timeline.append(f"tl.set('#fx-orbit-2',{{zIndex:2}},{t_mid:.2f});")
            timeline.append(f"tl.to('#fx-orbit-2',{{x:680,y:-30,scale:.82,duration:{dur2:.2f},ease:'power1.out'}},{t_mid:.2f});")
            timeline.append(f"tl.to('#fx-orbit-2',{{opacity:0,scale:.8,duration:.25}},{end - 0.25:.2f});")
            timeline.append(f"tl.set('#fx-orbit-2',{{display:'none'}},{end});")

            timeline.append(f"tl.set('#fx-orbit-3',{{display:'flex',opacity:0,x:680,y:-50,scale:.85,zIndex:2}},{start});")
            timeline.append(f"tl.to('#fx-orbit-3',{{opacity:1,duration:.35}},{start + 0.1:.2f});")
            timeline.append(f"tl.to('#fx-orbit-3',{{x:640,y:20,scale:.92,duration:{(end - start)*0.85:.2f},ease:'sine.inOut'}},{start + 0.1:.2f});")
            timeline.append(f"tl.to('#fx-orbit-3',{{opacity:0,scale:.8,duration:.25}},{end - 0.25:.2f});")
            timeline.append(f"tl.set('#fx-orbit-3',{{display:'none'}},{end});")
        elif fx_type == "pull-back-reveal":
            targets = "['#aroll','#subject']" if used_behind else "['#aroll']"
            timeline.append(f"tl.set('#fx-pullback',{{display:'flex',opacity:0}},{start});")
            timeline.append(f"tl.to('#fx-pullback',{{opacity:1,duration:.35,ease:'power2.out'}},{start});")
            timeline.append(f"tl.fromTo({targets},{{scale:1,y:0}},{{scale:.82,y:-60,duration:.45,ease:'power3.out',immediateRender:false}},{start});")
            timeline.append(f"tl.to({targets},{{scale:1,y:0,duration:.35,ease:'power2.inOut'}},{max(start + 0.45, end - 0.35)});")
            timeline.append(f"tl.to('#fx-pullback',{{opacity:0,duration:.3}},{max(start + 0.45, end - 0.3)});")
            timeline.append(f"tl.set('#fx-pullback',{{display:'none'}},{end});")
        elif fx_type == "grid-3x3":
            targets = "['#aroll','#subject']" if used_behind else "['#aroll']"
            timeline.append(f"tl.set('#fx-grid-3x3',{{display:'grid',opacity:0}},{start});")
            timeline.append(f"tl.to('#fx-grid-3x3',{{opacity:1,duration:.3,ease:'power2.out'}},{start});")
            timeline.append(f"tl.fromTo({targets},{{scale:1,y:0}},{{scale:.34,y:-40,duration:.42,ease:'power3.out',immediateRender:false}},{start});")
            timeline.append(f"tl.to({targets},{{scale:1,y:0,duration:.38,ease:'power2.inOut'}},{max(start + 0.45, end - 0.38)});")
            timeline.append(f"tl.to('#fx-grid-3x3',{{opacity:0,duration:.28}},{max(start + 0.45, end - 0.28)});")
            timeline.append(f"tl.set('#fx-grid-3x3',{{display:'none'}},{end});")
        elif fx_type in simple_block_fx:
            sel, disp = simple_block_fx[fx_type]
            timeline.append(f"tl.set('{sel}',{{display:'{disp}',opacity:0,y:24}},{start});")
            timeline.append(f"tl.to('{sel}',{{opacity:1,y:0,duration:.32,ease:'power3.out'}},{start});")
            timeline.append(f"tl.to('{sel}',{{opacity:0,y:-16,duration:.25}},{max(start + 0.4, end - 0.25)});")
            timeline.append(f"tl.set('{sel}',{{display:'none'}},{end});")

    profile_card = visual.get("profile_card")
    if profile_card and profile_card.get("file"):
        card_file = Path(profile_card["file"])
        if not card_file.is_absolute():
            card_file = project / card_file
        if card_file.exists():
            target_card = project / "assets" / f"profile-card{card_file.suffix.lower()}"
            shutil.copy2(card_file, target_card)
            rel_card = target_card.relative_to(project).as_posix()
            c_start = float(profile_card.get("start", max(0.0, duration - 5.0)))
            c_end = float(profile_card.get("end", duration))
            markup.append(f'<div id="fx-profile-card" class="fx-profile-card" style="display:none;opacity:0;z-index:9"><img src="{rel_card}" alt="Profile IG"></div>')
            timeline.append(f"tl.set('#fx-profile-card',{{display:'block',opacity:0,scale:.8,y:30}},{c_start});")
            timeline.append(f"tl.to('#fx-profile-card',{{opacity:1,scale:1,y:0,duration:.45,ease:'back.out(1.5)'}},{c_start});")
            timeline.append(f"tl.to('#fx-profile-card',{{opacity:0,scale:.9,duration:.3}},{max(c_start + 0.5, c_end - 0.3)});")
            timeline.append(f"tl.set('#fx-profile-card',{{display:'none'}},{c_end});")
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
    fx_attr_str = ""
    document = f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><title>MR Labs — {html.escape(theme['name'])}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{mrlabs_css(theme, portrait=portrait, caption_top=caption_top)}</style></head>
    <body><div id="main" data-theme="{theme['id']}" data-talking-head="{'true' if theme.get('talking_head') else 'false'}" data-portrait="{'true' if portrait else 'false'}" data-caption-pos="{caption_pos}" data-camera="{camera_motion}" data-choreo="{caption_choreography}"{fx_attr_str} data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">{''.join(markup)}</div>
    <script>const tl=gsap.timeline({{paused:true}});{''.join(timeline)}window.__timelines={{main:tl}};</script></body></html>'''
    (project / "index.html").write_text(document, encoding="utf-8")
    mrlabs_write(project / "hyperframes.json", {"width":1080,"height":1920,"fps":30})
    mrlabs_write(project / "build-report.json", {"theme": theme["id"], "theme_edition": theme.get("edition", 6),
                                                 "portrait_video": portrait, "background_applied": not portrait,
                                                 "caption_position": caption_pos,
                                                 "camera_motion": camera_motion,
                                                 "caption_choreography": caption_choreography,
                                                 "caption_top": caption_top if caption_pos == "above-head" else (1050 if caption_pos in ("below-face", "chest-float", "split-script", "hierarchy-glow", "shoulder-note", "dynamic-kinetic") else 1265),
                                                 "effects": [fx["type"] for fx in effects],
                                                 "duration": duration, "safe_guide": safe,
                                                 "broll": references, "captions": len(words), "needs_visual_audio_review": True})
    return project / "index.html"
