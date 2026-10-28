# Theme remake validation — 2026-10-29

All five visual directions were remade: Atlas Studio, Voltage Pop, Maison Journal, Playroom and Blueprint Lab. Stable configuration IDs are preserved. The gallery and video builder share `assets/render-themes.css`; HTML gallery specimens are generated from the same palette/type catalog. Test footage is synthetic, not a user production video.

| Check | Observed result |
|---|---|
| Behavioral tests | 10 passed, including short-cue readability and preserving poster tilt without tilting/shrinking full-frame B-roll |
| Skill and assets | Skill validator passed; 20 asset hashes and licenses verified |
| Gallery | Desktop 1560px and mobile 390px: no horizontal overflow; ID/EN examples, theme selection and replay exercised; fonts loaded; console had no errors |
| Layout | All five sample layouts in ID and EN: title/insert/caption/credit boxes do not overlap; credit remains above y=1470 |
| Five actual MP4 renders | Each preset linted with 0 errors / 0 warnings and encoded at 1080×1920, 30fps, 3 seconds, exactly 90 frames, with an audio stream |
| Encoded visual review | Extracted frames at 0.5s, 1.1s and 2.1s for every theme; verified distinct title/caption/insert treatments, intended tilt and straight full-frame inserts |
| Gallery delivery | Existing in-app browser tab refreshed to Visual Directions 02 |

Evidence: `assets/previews/themes-v2.png` inside the skill; ignored local `output/verification/theme-remake-renders.json`, `theme-remake-render.log`, `theme-remake-contact-final.png`, and `theme-remake-project/renders/`. The gallery was tested over localhost HTTP. Direct file-URL browsing was unavailable in the automated browser; it is not claimed as verified.

These are template and software checks. Speech recognition was not re-run for this visual-only remake. No actual user footage was edited, and no manual production-audio listening review is claimed. No commit, push or publication was performed.

## Earlier baseline — 2026-10-28

Completed locally on Windows x64 with Python 3.12.2, Node 22.19.0, FFmpeg 8.1.1, faster-whisper 1.2.1 and pinned HyperFrames 0.8.34. These are local checks, not a publication or a production edit of user footage.

| Check | Observed result |
|---|---|
| Skill structure | `quick_validate.py`: valid |
| Behavioral unit tests | 8 passed: language routing/rejection, ASR option forwarding, caption grouping/times, B-roll context/rights/ranges, EDL validation |
| Real Indonesian ASR | Multilingual `small`, language `id`: 21 timed words from a local 9-second excerpt; recognition still needs human correction |
| Real English ASR | Multilingual `small`, language `en`: 17 timed words from a locally synthesized English fixture; kept English wording |
| Bundled assets | 10 font families + 10 SFX; SHA-256 checks and bundled licenses verified |
| SFX decoding | All 10 OGG assets decoded by FFmpeg without errors |
| Browser fonts | All 10 font faces reached `loaded` |
| Gallery controls | Theme selection, ID/EN switching, replay of all 5 packs and audio playback exercised |
| Gallery layout | Desktop 1560px and mobile 390px: no horizontal overflow; gallery inspected visually |
| Python names | All script function definitions use `mrlabs_`; executable names use `mrlabs-*.py` |
| Five composition presets | Each generated and linted: 0 errors, 0 warnings |
| Synthetic media pipeline | Ingest → two-segment assembly → contextual brief → image PiP + full-frame video B-roll → captions/title/SFX → actual MP4 render |
| Encoded output | 1080×1920, 30fps, 3 seconds, 90 expected/90 actual frames, audio stream present, peak -13.6 dB |
| Source preservation | Synthetic source SHA-256 unchanged after pipeline |
| Final-image evidence | Encoded contact sheet inspected; full-frame B-roll credit moved clear of captions/branding |
| Single-segment QA | No-cut case handled using first/middle/last frames (0,45,89) |

Reproduce basic checks from the repository root:

```powershell
python skills/mrlabs-video-editor/scripts/mrlabs-assets.py
python -m unittest discover -s skills/mrlabs-video-editor/tests -v
python skills/mrlabs-video-editor/scripts/mrlabs-gallery.py
```

With the optional runtime installed, the synthetic pipeline can be run using:

```powershell
python skills/mrlabs-video-editor/tests/mrlabs-smoke.py --render
```

`--asr` additionally expects private local `output/verification/indonesian.wav` and `english.wav`; these audio fixtures and their transcripts are intentionally not distributed. Actual model files, caches, browser logs, media fixtures and rendered evidence stay under ignored directories. The runtime in this validation was reused from an existing compatible local virtual environment; a fresh-machine installation was not tested.

Known limits: mixed-language option is wired and uses a multilingual model, but no dedicated mixed-audio accuracy benchmark was performed. CPU cutout/background removal was not re-benchmarked. At this earlier baseline, one preset was rendered to MP4; all five were generated/linted and inspected in the illustrative gallery. The edition 02 checks above supersede that render count. Automated audio/peak checks are not manual listening. No production video is claimed fully reviewed: QA reports leave manual visual/listening status pending until an actual full review is performed. Internet B-roll retrieval remains an agent editorial workflow, not an API scraper, and the integration test used synthetic owned fixtures rather than an external stock asset. No commit, push, deployment or publication was performed.
