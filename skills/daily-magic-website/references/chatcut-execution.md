# ChatCut Execution Order

## Required Skill Routing

Load:

- `chatcut:chatcut-plugin-basics` for project targeting and edit boundaries.
- `chatcut:asset-import` for local screenshots, recordings, and downloaded official media.
- `chatcut:create-motion-graphics` for editable labels, masks, focus, and real-media arrangements.
- `chatcut:voice` for Dayi narration.
- `chatcut:verification` before handoff.
- `chatcut:export` only when the user explicitly asks for export.

## Fixed Order

1. Target the explicit project.
2. List timelines.
3. Create a fresh 1920×1080 timeline at 30 fps.
4. Import all verified real media through the official asset-import session and helper.
5. Wait for upload readiness before frame inspection or rendering.
6. Build S01–S06 in the fixed ranges.
7. Generate six separate Dayi segments.
8. Inspect actual audio durations.
9. Place each segment inside its shot.
10. Configure captions if requested or part of the approved master.
11. Render settled frames and seams.
12. Complete final plan QA and validate.
13. Export only on request.

## Motion Graphic Boundary

Use Motion Graphics to direct attention to real sources. Keep media in editable `image` or `video` properties. Expose all visible copy, numbers, colors, fonts, and URLs as editable properties.

Do not build the whole episode as one unconstrained one-off Motion Graphic. Use six shot-scoped items or a versioned master template whose six internal ranges exactly match the contract.

## Failure Handling

- Asset import denied: stop and provide the official upload fallback.
- Missing remote media: do not claim frame verification.
- Unsupported font: search the ChatCut font catalog and use the approved master fallback.
- Insufficient voice credits: do not substitute the voice; report a visual-only draft.
- Render mismatch: classify code, property, timing, placement, media, or upload failure before changing design.
