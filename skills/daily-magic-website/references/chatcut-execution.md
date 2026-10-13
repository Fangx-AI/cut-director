# ChatCut Execution

## Skill Order

Use the applicable ChatCut skills in this order:

1. Asset import
2. Motion Graphics
3. Voice
4. Transcription/captions when needed
5. Verification
6. Export only when requested

## Timeline Setup

- Canvas: 1080×1920
- Frame rate: 30 fps
- Duration: plan-defined, 900–1350 frames
- Background: reference black/grid system
- Timeline name: `每日神器网站｜<episodeId>｜<websiteName>｜EHOrMdeO-v1`

Do not alter the active user timeline before the episode plan passes validation.

## Build Order

### 1. Place Real Media

Place all logo, screenshot, browser-recording, official-video, and user-provided sources first.

Trim demo clips to the planned action:

- The action begins immediately.
- The result becomes visible.
- No loading or failed interaction remains.
- Three–five demos fill the `demo-run` beat.

### 2. Establish Layout Modes

Build the four approved modes:

- `type-stage`
- `logo-stage`
- `floating-proof-card`
- `immersive-ui-crop`

For a floating card, derive reflection and ambient light from the same media. Never substitute a synthetic mockup.

### 3. Apply Motion Recipes

Apply only the recipe declared by each beat.

For stylized transitions:

- Work in frames, not approximate seconds.
- Match the measured duration envelope.
- Add blur only during fast motion.
- Inspect every transition frame.
- End on a sharp evidence frame.

For the demo run:

- Use one-frame hard cuts.
- Place the cut on a spoken clause or visible action boundary.
- Do not add a transition between demonstrations.

### 4. Add Annotations

- Magnifier: clipped duplicate of real UI, 1.35–1.8×.
- Arrow/circle: live red draw, six–ten frames.
- Speech bubbles: two maximum, four–five frame entry each.
- Captions: placed after all visual overlays so nothing hides them.

### 5. Place Narration

Use one voice segment per beat or a continuous master with verified beat markers.

- Keep word boundaries intact.
- Keep body gaps under 180 ms.
- Match each clause to the visible proof.
- Do not let a caption change before its visual evidence.
- Use short audio fades only where separate clips could click.

### 6. Sound and Mix

Reference measurements are -12.5 LUFS integrated and 1.1 LU loudness range. Treat these as a calibration target, not permission to clip.

- Keep narration dominant.
- Keep music below speech.
- Avoid abrupt music edits at hard visual cuts.
- Verify peaks and intelligibility on the rendered preview.

## Verification Render

Before final handoff, render a preview and inspect:

- One settled frame per beat
- All stylized transition frames
- Every demo cut seam
- All annotation draw frames
- First and final frame
- Audio waveform and body gaps

Record verified frame numbers in the episode plan.

## Failure Handling

- Missing real media: stop and acquire it; do not fake the UI.
- Missing evidence: rewrite or remove the claim.
- Unreadable crop: change the layout mode or recapture at higher resolution.
- Voice unavailable: keep the visual draft and report the limitation.
- Motion recipe cannot be reproduced: keep it in a test timeline; do not improvise a new production effect.
- Export not requested: stop after verified review state.
