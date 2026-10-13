---
name: daily-magic-website
description: Produce reference-calibrated Chinese “每日神器网站” portrait videos from a website URL in ChatCut. Use when Codex must study or reproduce the EHOrMdeO master film’s visual grammar, research a website, acquire real official UI media, create a deterministic 30–45 second 1080×1920 episode, validate a nine-beat episode plan, place fast continuous narration, or revise an episode without random layouts, transitions, generated product UI, unsupported claims, empty placeholders, or a generic CTA ending.
---

# 每日神器网站

## Goal

Build repeatable website-recommendation films from one measured industry reference, not from taste guesses.

The master reference is the user-provided `EHOrMdeO.mp4`. The repository stores only its technical fingerprint and analytical observations; never add or redistribute the source video.

Content is editable. Grammar is controlled:

- Replace the website, copy, real captures, proof points, and source-native color.
- Keep the nine viewer jobs in order.
- Use only the four layout modes and measured motion recipes.
- Recalibrate the grammar only when the user approves a new master reference.

## Required Reading

Before planning, read:

1. [reference-analysis.md](references/reference-analysis.md)
2. [visual-grammar.md](references/visual-grammar.md)
3. [evidence-and-assets.md](references/evidence-and-assets.md)

Before editing ChatCut, read [chatcut-execution.md](references/chatcut-execution.md).

Before handoff or export, read [quality-gate.md](references/quality-gate.md).

## Non-Negotiable Rules

- Produce 1080×1920 at 30 fps for this reference profile. A horizontal film needs a separately approved horizontal master; never stretch this grammar into 16:9.
- Use real official UI, official media, verified browser captures, or user-provided product footage.
- Never generate, redraw, beautify, or fake a product interface.
- Do not invent a transition. Route every beat to an allowed motion recipe.
- Keep the product readable. Stylized motion is brief and settles to a sharp evidence frame.
- Keep the demo run to three–five real demonstrations joined by hard cuts.
- Make every spoken capability, number, pricing statement, and access claim visible or source-backed.
- Use the master’s two presentation modes intentionally: floating proof card or immersive UI crop.
- Keep narration continuous and clause-aligned; do not leave dead air between beats.
- End by returning to a useful product state. Do not append a generic URL card, “点赞关注”, or invented CTA.
- Keep all website content, numbers, URLs, captions, colors, screenshots, recordings, and demo ranges editable.
- Do not export unless the user asks.

## Workflow

### 1. Confirm the Reference Profile

Use `EHOrMdeO-master-v1` unless the user supplies and approves another master.

If the reference must be re-audited, run:

```powershell
python scripts/analyze_reference_video.py <video.mp4> <analysis-directory> --ffmpeg <ffmpeg.exe> --ffprobe <ffprobe.exe>
```

The script extracts every frame, contact sheets, scene candidates, silence data, loudness data, and a machine-readable fingerprint. Analytical outputs stay outside the repository.

### 2. Research the Website

Inspect the official website and official documentation/demo surfaces. Collect enough real evidence for all nine viewer jobs:

1. Series hook
2. Identity anchor
3. One-sentence value proof
4. Breadth or navigation proof
5. Core demo run
6. Credibility proof
7. Friction proof
8. Access path
9. Return close

If a website lacks a public usage number, award, price, or localization feature, use another verified proof serving the same viewer job. Never fabricate the missing fact.

### 3. Acquire Real Media

Follow this order:

1. Website-provided original video
2. Website-provided original image or logo
3. Verified browser screen recording
4. Verified browser screenshot
5. User-provided media

Capture the actual interaction, not a blank loading state. For every asset, record source URL, capture time, provenance, rights status, and whether it contains product UI.

### 4. Build and Validate the Episode Plan

Copy [episode-plan.template.json](assets/episode-plan.template.json) into the task workspace and replace all sample values.

Keep the nine beat families in order. Durations may move only inside the measured envelopes. The demo run must contain three–five subclips whose ranges are contiguous and whose joins are hard cuts.

Validate before any ChatCut write:

```powershell
python scripts/validate_episode_plan.py <episode-plan.json> --stage plan
```

Repair every validation error. Do not bypass the validator.

### 5. Execute in ChatCut

Load the applicable ChatCut skills for asset import, Motion Graphics, voice, verification, and export. Follow [chatcut-execution.md](references/chatcut-execution.md).

Name the timeline:

```text
每日神器网站｜<episodeId>｜<websiteName>｜EHOrMdeO-v1
```

Build the visual proof first, then narration, then captions, then sound, then verification. Motion Graphics may frame, crop, magnify, annotate, reflect, label, or transition real media; it may not replace the product.

### 6. Narration

The current series default is Doubao Dayi (`voiceId: dayi`), but voice identity remains editable. Timing behavior is mandatory:

- One clause per visible proof.
- No silence longer than 180 ms inside the body.
- No cut inside a spoken word.
- No speed-up above the value recorded in the episode plan.
- Shorten copy before compressing delivery.
- Keep the mix near the reference’s dense, controlled level; verify rather than guessing.

If voice generation is unavailable, keep the verified visual plan and report the limitation. Do not silently substitute another voice.

### 7. Verify

Inspect:

- Every settled beat frame
- Every stylized transition frame-by-frame
- Every hard-cut seam in the demo run
- Every evidence annotation before, during, and after its draw
- The final visible frame
- Caption legibility and UI occlusion
- Audio continuity and loudness

Complete `qa` and `delivery`, then run:

```powershell
python scripts/validate_episode_plan.py <episode-plan.json> --stage final
```

Do not call the episode complete until final validation passes.

### 8. Handoff

Report:

- Timeline and duration
- Reference profile
- Real source assets used
- Claims and evidence sources
- Voice and mix status
- Verification status
- Any known source limitation
- Whether export was requested or intentionally skipped

Keep experiments in clearly named test timelines. Never let a candidate effect silently enter the production grammar.
