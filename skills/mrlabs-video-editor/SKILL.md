---
name: mrlabs-video-editor
description: Edit original talking-head footage into Indonesian or English vertical videos with reviewed cuts, contextual B-roll, fifteen MR Labs visual packs, local open-license fonts and SFX, and final-render verification. Use for original-video editing, subtitle styling, or choosing these visual packs; not for creating a faceless video from a topic alone.
---

# MR Labs Video Editor

Edit the explicitly selected original footage. Default communication and transcription language is Bahasa Indonesia (`id`); preserve English speech when `en` or `mixed` is chosen. Keep the original face, recorded voice, and meaning. This skill is a new MR Labs implementation inspired by [tenfoldmarc/video-edit-skill](https://github.com/tenfoldmarc/video-edit-skill).

## Scope and starting point

- Start with at least one talking-head video with audible speech. Accept an existing transcript; do not re-transcribe if a reliable timed transcript is already available.
- Read the user's named files first. Do not silently select unrelated recent files from Downloads.
- `SK` means the absolute folder containing this file. `PROJECT` is a separate project directory. Never put private footage, transcripts, credentials or production renders into the distributable skill.
- Keep source files unchanged. Record clip IDs, source ranges, and frame-based output positions. Preserve old final renders when revising.
- When asked for a plan first, show the timed edit plan and wait for approval before production. For a new full edit, default to a concise plan review; existing explicit authorization remains valid. Software fixtures and theme illustrations are not user-video production.

## Local runtime and names

Use Python 3.10+, Node 22+, FFmpeg/ffprobe, faster-whisper and Pillow. Read [references/commands.md](references/commands.md) for exact PowerShell examples and data formats.

1. Run `python "SK/scripts/mrlabs-setup.py"`. `--install` builds a virtual environment inside this skill; use its Python for subsequent commands. The first real transcription can download its selected multilingual model.
2. All executable filenames use `mrlabs-*.py`. Python functions/modules use `mrlabs_...` because hyphens are invalid in Python identifiers. Do not reintroduce the upstream script names.
3. On PowerShell, prefix a quoted Python executable with `&`. Keep paths as separate subprocess arguments and write text as UTF-8.
4. `mrlabs-hyperframes.py` invokes a pinned HyperFrames version. Do not auto-upgrade it during a project. If blocked, report the actual error; do not claim setup proves rendering.

## Language and transcript

- Project defaults: `language: id`, `model: small` (multilingual), `device: cpu`. English: `--language en`; unknown language: `--language auto`; bilingual speech: `--language mixed` with a multilingual model. `medium` is an optional accuracy upgrade.
- Always use `task=transcribe`; do not translate speech unless requested. English-only `.en` models are rejected unless the source is explicitly `en`.
- The mixed option enables multilingual decoding; it does not guarantee perfect code switching. Listen to names and English technical terms in Indonesian sentences. Maintain project `keywords` and correct actual recognition errors without rewriting the speaker's message.
- Review uncertain words and timing, especially around cuts. Export both the word JSON and `captions.srt`.

## Visual choice

Show [assets/theme-gallery.html](assets/theme-gallery.html) when the user needs help choosing. The local gallery has ID/EN examples, fifteen layouts, replayable motion, twelve bundled font families plus optional local Helvetica, and ten playable SFX. Edition 04 adds five restrained Pro Influencer directions with pure White (`#FFFFFF`) and Black (`#0A0A0C` / `#0A0A0A`) backgrounds while preserving the five Fun directions (Edition 03) and five Original directions (Edition 02) and their configuration IDs. If the source video already supports portrait (`height > width`), the theme background is skipped automatically (`--canvas-background: transparent`, `data-portrait="true"`). Theme tokens live in [assets/themes.json](assets/themes.json); the gallery and video builder share [assets/render-themes.css](assets/render-themes.css). Read [assets/DESIGN.md](assets/DESIGN.md) before changing these visual directions.

| Theme | Use |
|---|---|
| Atlas Studio / `signal-clean` (default) | Education/tutorials; paper and vermilion, Swiss typography, indexed square frame |
| Voltage Pop / `kinetic-punch` | Hooks and quick tips; cobalt and acid yellow, tilted poster, spring entrance |
| Maison Journal / `editorial-noir` | Opinions/interviews; ivory and wine, centered serif, gallery mat |
| Playroom / `warm-story` | Creative stories; lilac and butter, rounded notes, playful collage |
| Blueprint Lab / `tech-grid` | Coding/data/automation; navy and cyan, drafting lines, monospace captions |
| Peach Doodle / `peach-doodle` | Peach doodles, soft speech-tail caption, dashed organic frame |
| Bubble Pop / `bubble-pop` | Lilac bubbles, Poppins Bold headings, round capsules |
| Groovy Mint / `groovy-mint` | Mint rolling waves, asymmetrical pebble shapes |
| Sunny Picnic / `sunny-picnic` | Yellow floral pattern, petal-like curves, Poppins Bold |
| Orbit Candy / `orbit-candy` | Purple orbital rings, ellipse frame, Roboto Light captions |
| Verge Glass / `verge-glass` | Pro tech/productivity reviews; black `#0A0A0C` background, bento glass, ice-blue rule |
| Monocle Brief / `monocle-brief` | Executive business/finance; white `#FFFFFF` background, DM Serif Display, racing green |
| Kinfolk Linen / `kinfolk-linen` | Quiet luxury/lifestyle/wellness; white `#FFFFFF` background, Instrument Serif, bronze rule |
| Obsidian Studio / `obsidian-studio` | Cinema/podcast/masterclass; black `#0A0A0A` background, Fraunces, champagne gold L-frame |
| Founder Slate / `founder-slate` | Startup/AI/founder updates; white `#FFFFFF` background, Space Grotesk, cobalt bar |

Read [references/visual-packs.md](references/visual-packs.md) for treatment details. Choose one coherent pack unless the brief calls for a purposeful section change. Font, accent, geometry, caption and motion differ; do not present palette swaps as new themes.

## Viral Talking-Head Effects (`effects` in `visual.json` or `project.json`)

| Effect ID | Behavior | Depth / Cutout |
|---|---|---|
| `orbit` | **ORBIT 3D Cards** — floating UI/metric cards orbit 360° around the speaker, passing behind (`z-index: 2`) and in front (`z-index: 8`) | Uses `subject.webm` (`z-index: 3`) |
| `ui-world` | **UI World Window** — top half of the vertical frame becomes an interactive AI/Claude workflow window while speaker talks below | Foreground (`z-index: 7`) |
| `digital-zoom` | **Digital Zoom Punch-In** — smooth programmatic `1.24×` camera punch-in onto speaker's face/gestures on emphasis cues | Scales `aroll` + `subject` |
| `headline-wall` | **Headline Wall** — angled newspaper clippings and highlighted headlines stick onto the wall behind the speaker one by one | Uses `subject.webm` (`z-index: 2` behind `3`) |
| `pull-back-reveal` | **Pull Back Reveal** — camera zooms out to reveal the vertical video playing inside a desktop NLE video editor timeline interface | NLE frame (`z-index: 10`) |

Caption positions (`caption_position` in `visual.json` or `project.json`): `"below-face"` / `"chest-float"` (below face / across chest at `y=1050`), `"above-head"` (above head at `y=310`), or `"bottom"` (lower third at `y=1265`).

## Edit workflow

1. **Ingest:** run `mrlabs-ingest.py PROJECT SOURCE...`, review source metadata/contact sheets and transcripts. Set language/theme in `project.json`.
2. **Propose:** select clean, complete takes by delivery and meaning. Create `edl.json`. Preserve natural breaths and qualifications; do not assume the last take is the best. Show source ranges, output timestamps, wording, visual treatment and missing assets.
3. **Assemble:** after applicable plan approval, run `mrlabs-assemble.py PROJECT` and `mrlabs-transcribe.py PROJECT`. Frame mismatch is an error, not a warning to ignore. Review the newly timed transcript.
4. **Contextual B-roll:** read [references/contextual-broll.md](references/contextual-broll.md), run `mrlabs-broll.py PROJECT`, then review the keyword-based suggestions against the actual story. Search for relevant internet assets when useful and rights-verifiable; prioritize the user's demonstrations for specific product claims. Record approved source/rights metadata in `broll.json`. A proposal is not a downloaded or verified asset.
5. **Depth only when useful:** run `mrlabs-cutout.py` and `mrlabs-headpos.py` only for behind-subject titles. Alpha bounds are sampled, not continuous face tracking. Check motion and readability; use a front caption if the mask or placement is poor.
6. **Compose:** add optional titles/SFX to `visual.json`. Run `mrlabs-build.py PROJECT --safe`; inspect actual layout and text wrapping. B-roll renders muted and leaves the original narration in the mix. Full-frame B-roll still needs safe placement of captions/branding. Use imagery as illustration, never as invented evidence.
7. **Render:** rebuild without `--safe`. Run HyperFrames lint then `mrlabs-render.py PROJECT OUTPUT.mp4`. The renderer rejects builds containing the guide and refuses to overwrite existing final outputs.
8. **Verify:** run `mrlabs-check-cuts.py PROJECT OUTPUT.mp4 --phone`. Inspect the final cut evidence and sample middle/last frames even for a single segment. Watch the final video and listen for word truncation, A/V sync, clicks and SFX balance. The report intentionally leaves manual visual/listening review pending; only mark complete after performing those reviews. Deliver the full render, phone copy, SRT and editable project location with remaining limitations.

## Asset and layout constraints

- Read [references/assets.md](references/assets.md) for the bundled font/SFX inventory and licenses. Verify `mrlabs-assets.py` before delivery; `--fetch` re-downloads the curated catalog from recorded sources. Do not commit local environments, model caches or user media.
- For the v1 1080×1920 profile keep critical text below y=220 and above y=1470, 35px side clearance and right-side icon clearance lower down. These are this profile's conservative defaults, not permanent platform specifications. Inspect the actual target layout.
- Never cover the face with text/cards. Caption length and wrapping are reviewed at phone scale. The sample builder is a starting composition; context-driven positioning still needs visual review.
- Keep voice primary. Suggested SFX gain is 0.07–0.12; the builder caps explicit gain at 0.3. No mandatory music, no fabricated social metrics, no AI room replacement, no grain by default.
- Internet footage requires an actual source page, license/permission record and review. An @credit alone is not a reuse license. External uploads, publication, paid asset purchase, Git push and deployment require their own user authorization.

## Compatibility boundaries

v1 composition and assembly support 1080×1920 at 30fps. Other formats need a deliberate profile change. The HyperFrames compiler/render may require network on first use and loads pinned GSAP from a CDN; the theme gallery, bundled fonts and SFX work locally. B-roll searching is performed by the agent through available web tools; the Python helper provides contextual search briefs and validation, not a stock-library API integration. Theme samples are designed illustrations, not proof of final footage quality.
