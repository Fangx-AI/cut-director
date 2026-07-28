# Visual Grammar

## Four Layout Modes

Use only these modes.

### 1. `type-stage`

Purpose: series hook.

- Black canvas with a subtle dark grid.
- Main title occupies roughly 72–82% of the width.
- Use no more than three lines.
- Keep one semantic keyword in series yellow; other title text is white.
- Enter each line from above with motion blur and a sharp settle.
- Keep the episode badge in the upper-left title rail.

Reference-sized starting point at 1080×1920:

- Side rail: 96–120 px
- Main title: approximately 112–142 px, very heavy square sans
- Line gap: 8–20 px
- Series yellow: approximately `#F6C515`
- Background: approximately `#070909`
- Grid: 1 px, 3–5% opacity

The exact font family is not proven by the source. Match weight, width, counters, and Chinese glyph quality; do not claim an exact face.

### 2. `logo-stage`

Purpose: identity anchor.

- Center the verified logo or app icon.
- Keep the canvas black and uncluttered.
- Put the verified product name directly below.
- Draw one red pointer only when it helps identity recognition.
- Do not add feature copy here.

### 3. `floating-proof-card`

Purpose: calm presentation of a real screen or official page.

- Content width: 80–82% of canvas.
- Horizontal rails: approximately 9–10% on each side.
- Place the primary card near the vertical middle, not at the top.
- Preserve the native media aspect ratio.
- Use a dark 8–14 px outer edge or shadow and modest corner radius only when compatible with the source.
- Add a soft, blurred reflection/spotlight below the card. The reflection must derive from the same real media.
- Align the caption rail to the content width.
- Keep substantial black negative space above and below.

Reference geometry for near-square media:

- Card: about x=104–976 px
- Card top: about y=550 px
- Card width: about 872 px
- Caption: about x=105–975 px, y=1450–1565 px
- Caption text: approximately 48–60 px

If media is not near-square, preserve it; do not stretch it to these exact dimensions.

### 4. `immersive-ui-crop`

Purpose: navigation, filtering, scrolling, and evidence inspection.

- Let the real browser capture fill the portrait canvas.
- Crop or zoom to the exact interaction or evidence; do not shrink unreadable desktop UI into the center.
- Keep key labels readable at 100% review scale.
- Use a translucent dark caption bar only where it does not cover the interaction.
- A focus lens may duplicate and enlarge a real UI region inside a circular mask.

## Typography Components

### Body Caption

- One line preferred; two lines maximum.
- White, heavy sans, centered.
- Dark neutral bar at roughly 78–92% opacity.
- Caption describes the visible proof, not an abstract slogan.
- Keep punctuation and line breaks editable.
- Move the caption rather than cover a cursor, control, number, or result.

### Stacked Speech Bubbles

- Use only in the one-line value proof.
- Two bubbles maximum.
- First: light neutral with dark text.
- Second: source-native accent with white text.
- Alternate tail direction.
- Enter after the product screen has settled, four–five frames per bubble.
- Each bubble holds one short phrase; do not put a paragraph in it.

### Hand-Drawn Annotation

- Series annotation color: warm red, approximately `#E44A36`.
- Stroke width: roughly 12–18 px at 1080 px canvas width.
- Animate the stroke over six–ten frames.
- Circle or point to one verified target only.
- The target must remain readable through the stroke.
- Never paste a static circle that appears before the evidence.

## Motion Recipe Set

Only these recipe IDs are allowed:

| Recipe | Use | Frame behavior at 30 fps |
|---|---|---|
| `staggered-line-drop` | Hook | 4–6 frame entry per line; 5–10 frame stagger |
| `badge-diagonal-peel` | Episode badge | 8–9 frame diagonal reveal |
| `hook-logo-collapse` | Hook to identity | 7 frame overlapping collapse; no dissolve |
| `hand-drawn-pointer` | Logo/evidence | 6–10 frame live draw |
| `diagonal-page-curl` | Identity to first product proof | 9 frame curl; real screenshot is the page |
| `stacked-bubble-pop` | Value proof | 4–5 frames per bubble after card settle |
| `radial-zoom-bridge` | Section boundary | 4 frame directional/radial blur; next frame readable |
| `focus-lens` | Filter or control | Circular clipped duplicate at 1.35–1.8× scale |
| `overzoom-settle` | Enter a new proof card | 10–14 frame scale-down into final geometry |
| `hard-cut` | Demo run | One-frame cut at an action or clause boundary |
| `evidence-circle-draw` | Statistic or friction proof | 6–10 frame live circle |
| `scroll-focus` | Access path | Real page scroll; card frame remains stable |
| `return-state-settle` | Closing | 8–14 frame return/scale settle to useful product state |

## Motion Discipline

- Use motion blur only while speed is high.
- End every stylized transition on a sharp readable frame.
- Avoid dissolves, random rotations, 3D card spins, parallax for its own sake, decorative particles, and arbitrary camera shake.
- Do not apply a stylized transition between every demo. The hard-cut demo run is deliberately calm.
- Match motion to a spoken clause boundary.
- Keep cursor motion real and purposeful; remove wandering or hesitation.

## Information Rhythm

The reference profile uses these duration envelopes:

| Beat family | Frames | Seconds |
|---|---:|---:|
| `series-hook` | 50–80 | 1.67–2.67 |
| `identity-anchor` | 42–70 | 1.40–2.33 |
| `value-proof` | 70–120 | 2.33–4.00 |
| `navigation-proof` | 110–200 | 3.67–6.67 |
| `demo-run` | 300–480 | 10.00–16.00 |
| `credibility-proof` | 70–125 | 2.33–4.17 |
| `friction-proof` | 40–90 | 1.33–3.00 |
| `access-path` | 120–210 | 4.00–7.00 |
| `return-close` | 24–60 | 0.80–2.00 |

Episode duration must remain 900–1350 frames (30–45 seconds) for this profile.

## Rejected Patterns

Reject the shot if any of these appear:

- Empty wireframe, skeleton UI, or invented dashboard
- Blurred product content presented as proof
- Tiny full-page screenshot the viewer cannot read
- Decorative text that repeats the caption without adding hierarchy
- Random accent colors unrelated to series or source
- A transition longer than the information it introduces
- Static red circles or arrows with no draw animation
- Generic final URL card replacing the product
