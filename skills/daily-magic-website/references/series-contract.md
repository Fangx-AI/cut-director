# Master V1 Series Contract

## Fixed Output

- Canvas: 1920×1080.
- Frame rate: 30 fps.
- Duration: 720 frames / 24 seconds.
- Platform: Bilibili horizontal.
- Language: Simplified Chinese.
- Voice: Doubao Dayi.
- Episode structure: six fixed shot jobs.

## Fixed Visual System

- `masterVersion`: `daily-magic-website-v1`
- Primary font: `Smiley Sans` after confirming it is available in ChatCut.
- Palette mode: `source-native-single-accent`.
- Series neutrals: near-black, white, and neutral gray.
- Accent: derive one color from the official website identity or UI.
- Captions: white Chinese text, dark outline or opaque dark backing, bottom safe area.
- Corners: use the source UI’s geometry; do not add decorative rounding to every surface.
- Shadows, glow, grain, gradients, and glass are off unless visible in the real source.

## Fixed Motion Set

Only these primitives are allowed in Master V1:

1. `hard-cut`: direct editorial cut.
2. `masked-push`: one directional reveal or page push.
3. `focus-lock`: dim nonessential page areas and accurately focus a real target.
4. `slow-crop`: restrained 1.00–1.08 source crop over a shot.

Do not use random 3D rotation, elastic cards, light sweeps, decorative scan lines, floating particles, arbitrary parallax, or multiple unrelated entrance directions.

## Controlled Variability

May change:

- Website, facts, copy, screenshots, screen recordings, outputs, and accent color.
- One flow variant selected from the approved list.
- Which verified CutDirector Prompt implements a matching local shot.

May not change without explicit series-version approval:

- Duration, shot order, frame ranges, type hierarchy, caption position, motion set, voice, or QA threshold.

## Master Approval

The written contract alone does not approve a visual style. The first episode is a calibration episode.

Record:

- Approval status.
- Approved ChatCut timeline ID or exported-video reference.
- Approval date.
- Any explicit exceptions.

Final validation must fail while the master reference is provisional. Every later episode must compare its settled frames with the approved master reference.

## Version Changes

Test a proposed visual change on a timeline named:

```text
候选母版｜<change-name>｜验证版
```

Adopt it only after the user approves the actual rendered result. Then increment the master version and update this contract, the episode template, validator, shot grammar, and quality gate together.
