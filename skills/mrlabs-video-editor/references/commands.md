# Commands and project data

All executable scripts use `mrlabs-*.py`; module names and function identifiers use `mrlabs_`. These are fresh MR Labs implementations of the workflow, not renamed copies of upstream functions. Conceptual mapping:

| Source stage | MR Labs executable |
|---|---|
| setup | mrlabs-setup.py |
| ingest | mrlabs-ingest.py |
| assemble | mrlabs-assemble.py |
| transcribe_cut | mrlabs-transcribe.py |
| cutout | mrlabs-cutout.py |
| headpos | mrlabs-headpos.py |
| build | mrlabs-build.py |
| hf | mrlabs-hyperframes.py |
| check_cuts | mrlabs-check-cuts.py |
| New asset library | mrlabs-assets.py |
| New contextual briefs | mrlabs-broll.py |
| New pack gallery | mrlabs-gallery.py |
| Protected output render | mrlabs-render.py |

PowerShell example, run from the repository root (adapt the source/project locations):

```powershell
python skills/mrlabs-video-editor/scripts/mrlabs-setup.py --install
$mrlabsPy = (Resolve-Path 'skills/mrlabs-video-editor/.venv/Scripts/python.exe').Path
$mrlabsScripts = (Resolve-Path 'skills/mrlabs-video-editor/scripts').Path
& $mrlabsPy "$mrlabsScripts/mrlabs-ingest.py" projects/demo 'D:/video/rekaman.mp4'
# English: add --language en; bilingual: --language mixed
```

Review transcripts/contact sheets, then author the EDL and the timed edit plan. For already reliable transcripts `--skip-transcription` registers media without ASR. No ASR model or remote upload is required to build the theme gallery.

## Minimal project.json

```json
{"schema":1,"language":"id","model":"small","device":"cpu","theme":"signal-clean","fps":30,"width":1080,"height":1920,"keywords":["MR Labs","ChatGPT"],"brand":"MR LABS","credit":"by @maulanarahman_"}
```

Supported languages: `id`, `en`, `auto`, `mixed`. `task=transcribe` keeps the spoken language. Do not assume mixed mode fixes all borrowed technical words. `small` is multilingual; `small.en` is rejected unless language is explicitly `en`.

## edl.json

```json
[{"id":"hook","clip":"c1","in":1.0,"out":5.0,"zoom":1.0,"line":"Kalimat sumber yang dipilih."}]
```

`clip` references the source registry written by ingest. Validate ranges against the original duration; add `cx`, `cy` in 0..1 for a punch-in center. The assembly reads originals and writes derived `assets/aroll.mp4` and frame-based `segments.json`. For a revision, back up prior derived assets or use a separate version directory before reassembling; assembly replaces its derived working files.

```powershell
& $mrlabsPy "$mrlabsScripts/mrlabs-assemble.py" projects/demo
& $mrlabsPy "$mrlabsScripts/mrlabs-transcribe.py" projects/demo
& $mrlabsPy "$mrlabsScripts/mrlabs-broll.py" projects/demo
```

The last command produces proposals; review and source real B-roll using `contextual-broll.md`. Put only approved cues into `broll.json`. Do not commit private transcripts or media.

## Optional visual.json

```json
{"titles":[{"text":"Mulai dari satu langkah","start":0.2,"end":2.8,"behind_subject":false}],"sfx":[{"id":"click_001","time":0.3,"gain":0.1}]}
```

`words.json` is an array of `{text,start,end}` words on the assembled timeline. It may be imported after human correction. The builder escapes caption/title content before emitting HTML. Fonts/SFX are copied locally into a project's `assets/mrlabs/`. B-roll uses project/local files plus the rights ledger.

```powershell
& $mrlabsPy "$mrlabsScripts/mrlabs-build.py" projects/demo --safe
Push-Location projects/demo
& $mrlabsPy "$mrlabsScripts/mrlabs-hyperframes.py" lint
& $mrlabsPy "$mrlabsScripts/mrlabs-hyperframes.py" snapshot --at 1 --no-end --describe false
Pop-Location
# Inspect snapshots, fix, then remove the preview guide:
& $mrlabsPy "$mrlabsScripts/mrlabs-build.py" projects/demo
& $mrlabsPy "$mrlabsScripts/mrlabs-render.py" projects/demo renders/demo-v1.mp4
& $mrlabsPy "$mrlabsScripts/mrlabs-check-cuts.py" projects/demo projects/demo/renders/demo-v1.mp4 --phone
```

Render output paths are relative to PROJECT unless absolute. Existing final files are never overwritten. `mrlabs-render.py` lints then renders. Run final checks from encoded output, watch and listen manually, and retain the report's honest pending status until completed.
