# MR Labs visual directions — edition 02

All five directions are a complete remake. Theme IDs stay stable for existing projects; names and visual systems change. `themes.json` owns palette, typography and timing. `render-themes.css` owns per-theme geometry and is shared by rendered compositions and gallery specimens.

| Direction | Style prompt | Colors | Typography | Motion |
|---|---|---|---|---|
| Atlas Studio | Swiss editorial layout, oversized left-aligned type, red index line, squared documentary inserts and a white caption strip. | Paper #F6F4EE, black #20211F, vermilion #BE3424 | Plus Jakarta Sans + IBM Plex Mono | Short upward reveal, precise stop |
| Voltage Pop | Electric blue poster, acid-yellow structural marks, heavy headlines, off-axis B-roll and a yellow subtitle slab. | Cobalt #213BE6, yellow #E9FF63, white #FFFFFF | Bricolage Grotesque + DM Sans | Compressed scale and slight rotation, spring settle |
| Maison Journal | A quiet wine-and-ivory magazine cover, centered serif headline, fine rules, framed B-roll and a minimal caption underline. | Ivory #F5EDDF, wine #562A3A, rose #94485B | Instrument Serif + Manrope | Gentle focus reveal |
| Playroom | Soft lilac collage with butter-yellow notes, rounded display type, offset paper edges and a playful capsule subtitle. | Lilac #DCD1F2, butter #FFF3AF, plum #48266B | Fraunces + DM Sans + Caveat label | Buoyant upward entrance |
| Blueprint Lab | Technical navy canvas, thin cyan drafting lines, clipped-corner footage frame, monospaced annotations and a left-ruled caption panel. | Navy #071E29, cyan #78ECDE, fog #E4F6F4 | Space Grotesk + IBM Plex Mono | Horizontal reveal with decisive stop |

Do not add film grain, fake metrics, fabricated profile data, or replace the source room. Decorative framing must not crop the original subject. B-roll labels, title, captions and attribution have separate conservative portrait zones. Synthetic gallery illustrations demonstrate graphic treatment only; they are not user footage or factual diagrams. Keep narration and timing unchanged when switching theme. Preview entrances are replayable; production uses the deterministic GSAP timeline.


## Edition 03 — Fun collection

Keep the original five token sets unchanged. New directions favor curved silhouettes, organic frames, repeat patterns and solid readable caption plates. Poppins Bold is the actual 700 face; Roboto Light is weight 300 of the bundled variable font. Helvetica is optional local-only, never silently represented as a bundled font.

| Direction | Palette / pattern | Type / shapes |
|---|---|---|
| Peach Doodle | Peach #FFF1E6, coral #B3432C; loose scribbles and sparkles | Fraunces + DM Sans; dashed organic insert, speech-tail caption |
| Bubble Pop | Lilac #F0E8FD, pink #FFC5E4, plum #43215F; bubbles and dots | Poppins Bold + Roboto; floating capsules and oval insert |
| Groovy Mint | Mint #E1F5D0, lavender #C6A9EF, green #304F38; rolling waves | Bricolage + DM Sans; soft asymmetrical pebble shapes |
| Sunny Picnic | Cream #FFF7D1, butter #FFCB66, brown #673B20; daisies and pollen | Poppins Bold + Roboto; petal curves and dotted edging |
| Orbit Candy | Navy-purple #211B4B, lilac #3A3066, pink #FFB8CA; orbits and stars | Roboto 700 + 300; elliptical insert and rounded caption plate |

Patterns are embedded vector tile assets, not generated example media. In the gallery they fill the background. On original footage decorative pattern overlays are restricted to top/bottom margins, leaving the presenter area clear. No production sample is requested for this edition.


## Edition 04 — Pro Influencer collection (White & Black backgrounds + Portrait condition)

Keep all ten earlier token sets unchanged. Five professional creator directions use clean **White (`#FFFFFF`)** and **Black (`#0A0A0C` / `#0A0A0A`)** backgrounds, architectural restraint, hairline geometry, zero rotation, and high-trust editorial typography suited to thought leaders, executives, founders, and domain experts.

**Portrait condition:** When the source video already supports portrait (`height > width`), the theme background is skipped (`--canvas-background: transparent`, `data-portrait="true"`, and no background padding in `mrlabs-assemble.py`) so the portrait video fills the 1080×1920 frame directly. When the source video is non-portrait (`width >= height`), the White or Black theme background is applied automatically.

| Direction | Style prompt | Colors | Typography | Motion |
|---|---|---|---|---|
| Verge Glass | Dark keynote bento cards on black background, 1px specular border, ice-blue top rule and floating dock caption bar. | Black #0A0A0C, slate #14171F, white #FFFFFF, ice #38BDF8 | Plus Jakarta Sans + Manrope + IBM Plex Mono | Crisp upward bento reveal |
| Monocle Brief | Broadsheet white canvas, double press rules, racing-green column frame and executive briefing bar. | White #FFFFFF, stone #F4F4F0, black #111111, emerald #14532D | DM Serif Display + Plus Jakarta Sans + IBM Plex Mono | Composed focus reveal |
| Kinfolk Linen | Quiet luxury gallery white mat, warm alabaster border, centered serif headline and terracotta top rule. | White #FFFFFF, alabaster #F5F3EE, charcoal #171715, bronze #8C5238 | Instrument Serif + DM Sans + Manrope | Calm dissolve reveal |
| Obsidian Studio | Matte studio black, champagne gold L-rule, letterbox documentary insert and lower-third subtitle plate. | Black #0A0A0A, graphite #171717, white #FAFAFA, champagne #D4AF7A | Fraunces + Manrope + Space Grotesk | Decisive horizontal cinema slide |
| Founder Slate | Executive pitch-deck white canvas, cobalt accent bar, clean slate elevation plates and monospace labels. | White #FFFFFF, slate #F1F5F9, carbon #0F172A, cobalt #2563EB | Space Grotesk + DM Sans + IBM Plex Mono | Fast structured deck rise |
