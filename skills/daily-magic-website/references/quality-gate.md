# Quality Gate

## Gate 1: Evidence

- Every product visual is real and provenance-verified.
- Every spoken capability is visible or source-backed.
- Every number, price/access statement, award, and platform claim has captured evidence.
- No generated or redrawn product UI appears.
- No blank, loading, skeleton, or placeholder state is presented as proof.

## Gate 2: Composition

- Only the four approved layout modes appear.
- Hook hierarchy is readable in under one second.
- Floating cards occupy about 80–82% of canvas width and preserve aspect ratio.
- Immersive crops keep the relevant UI readable at 100% review scale.
- Captions do not cover controls, cursor, evidence, or results.
- Reflections derive from the same real media and do not look like random fog.
- Source-native colors remain intact.

## Gate 3: Temporal Craft

- Every beat stays inside its duration envelope.
- Every declared motion recipe matches the visual grammar.
- Hook lines, badge, bubbles, arrows, and circles animate over the measured frame range.
- High-speed frames use appropriate directional or radial blur.
- Every stylized transition ends sharp.
- The demo run contains three–five real clips joined only by hard cuts.
- Demo cuts land on action or clause boundaries.
- The final beat returns to a useful product state.

Inspect transition strips frame-by-frame. Do not approve from a single thumbnail.

## Gate 4: Typography

- Chinese glyphs are correct and not substituted by a broken fallback.
- Hook uses no more than three lines.
- One hook keyword carries the yellow emphasis.
- Body captions are one line when possible, two lines maximum.
- Speech bubbles contain short phrases only.
- No text is clipped, mirrored, blurred at settle, or placed outside the safe rail.

## Gate 5: Audio

- Narration is continuous through the body.
- Internal silence does not exceed 180 ms.
- No cut occurs inside a word.
- Copy speed does not exceed the plan.
- Narration remains intelligible over music.
- Loudness is verified near the reference target without clipping.
- The final audio resolves cleanly rather than stopping mid-word.

## Gate 6: Final-State Verification

For final validation, the episode plan must confirm:

- `referenceProfileVerified`
- `nineBeatOrderVerified`
- `realUiOnly`
- `claimsVerified`
- `layoutModesVerified`
- `motionRecipesVerified`
- `demoHardCutsVerified`
- `captionsVerified`
- `noEmptyOrUnreadableUi`
- `audioContinuityVerified`
- `finalProductStateVerified`
- `frameInspectionComplete`

`delivery.verifiedFrames` must include at least:

- One settled frame from each of nine beats
- One frame from every stylized transition
- The final frame

## Automatic Rejection

Reject the film if:

- Any product view is synthetic or invented.
- Any UI is too small to read.
- A transition is improvised outside the recipe set.
- The demo run uses random transitions.
- A claim lacks evidence.
- A red annotation appears statically rather than drawing.
- The ending becomes a generic CTA or URL card.
- The output is landscape under this portrait reference profile.
