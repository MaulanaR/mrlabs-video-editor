# Bundled open-license assets

12 font families are shipped as original TTF files from the Google Fonts repository at pinned commit `9862abc066c9b83bf84c3e8ed1fc2d8d48f9bbf0`. Each has its own unmodified OFL text. Variable fonts include their supported weight axes; static files are regular upright styles except Poppins, which deliberately bundles the requested Bold (700) file.

| Font | Typical role |
|---|---|
| Plus Jakarta Sans | Clear tutorial titles/captions |
| Manrope | Editorial body/captions |
| Space Grotesk | Technology headings |
| DM Sans | Warm story body/captions |
| Bricolage Grotesque | Bold hook/display |
| Fraunces | Warm serif storytelling |
| Instrument Serif | Optional refined short title |
| DM Serif Display | Editorial serif title |
| IBM Plex Mono | Steps, code and labels |
| Caveat | Optional handwritten annotation |
| Poppins Bold (700) | Rounded bold display/headings |
| Roboto (400) / Roboto Light (300) | Regular and light body/captions; one variable font |

Helvetica is an optional **local-only** font. No Helvetica binary is downloaded or redistributed. `fonts.css` looks for an installed Helvetica Regular; the gallery reports when it is unavailable and shows Roboto as an explicit fallback. Use Helvetica in production only with an appropriate local license and verify availability in the renderer. This addition does not claim portable Helvetica embedding. See [Monotype licensing](https://support.monotype.com/en/articles/7872341-licensing).

Poppins and Roboto retain their individual OFL files and pinned sources in the catalog. The gallery exposes Poppins at weight 700 and separate Roboto 400 / Light 300 specimens; Light is not a separate family. Theme fields use `heading_font: Poppins, heading_weight: 700`, or `body_font: Roboto, caption_weight: 300`.

The 10 SFX are unchanged OGG files from Kenney Interface Sounds, published by Kenney under CC0. They are obtained from Kenney's author-uploaded OpenGameArt mirror. `Kenney-LICENSE.txt` retains the pack's license. These are UI/accent sounds, not a claim to include whooshes or music.

| File ID | Editorial use |
|---|---|
| click_001 | Button/tap |
| confirmation_001 | Completed step |
| open_001 | Card/window reveal |
| close_001 | Close a demonstrated UI |
| maximize_001 | Expand a card |
| minimize_001 | Collapse an element |
| glitch_001 | Brief technical accent, sparingly |
| pluck_001 | Keyword/punch accent |
| scroll_001 | Scroll action |
| switch_001 | Change mode/option |

`../assets/catalog.json` records exact source files, source pages, creator (SFX), license files, byte sizes and SHA-256 hashes. `mrlabs-assets.py` verifies offline hashes/licenses; `--fetch` obtains the curated files again and regenerates the catalog and font CSS. After re-fetching run `mrlabs-gallery.py` to refresh the shelf.

Sources: [Google Fonts](https://github.com/google/fonts), [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds), [author's OpenGameArt upload](https://opengameart.org/content/interface-sounds).
