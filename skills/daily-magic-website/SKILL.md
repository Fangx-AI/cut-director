---
name: daily-magic-website
description: Produce repeatable, evidence-based Chinese “每日神器网站” horizontal videos from a website URL in ChatCut. Use when Codex must research a website, collect real official UI media, write and validate a fixed-format episode plan, create a polished 24-second 16:9 website recommendation video with Dayi narration, reuse compatible CutDirector local-edit Prompts, verify composed frames, or revise an existing episode without introducing random layouts, motion, colors, or unsupported product claims.
---

# 每日神器网站

## Goal

Produce a stable series, not a new visual experiment for every website. Keep the master structure and motion grammar fixed. Replace only verified website content, real source media, claims, and episode copy.

Treat `cut-director` as the parent repository:

- This Skill owns complete “每日神器网站” episodes.
- Root CutDirector Prompt recipes own reusable local editing effects.
- Route a shot to a Prompt only when its viewer job and required inputs match.

## Mandatory References

Read before planning:

1. [series-contract.md](references/series-contract.md)
2. [shot-grammar.md](references/shot-grammar.md)

Read [evidence-and-assets.md](references/evidence-and-assets.md) before researching or acquiring media.

Read [chatcut-execution.md](references/chatcut-execution.md) before modifying ChatCut.

Read [quality-gate.md](references/quality-gate.md) before handoff, export, or calling an episode complete.

## Non-Negotiable Rules

- Never invent a new composition, palette, transition, or motion language per website.
- Never call a style “Master V1” until the user approves an actual rendered calibration episode and its reference is recorded.
- Never generate, redraw, or fake a real product interface.
- Use official website screenshots, official demo media, user-provided media, or verified browser captures.
- Keep one source-native accent color plus series neutrals. Do not add a second arbitrary accent.
- Use only the six fixed shot jobs and frame ranges in Master V1.
- Make every spoken product claim visible or provable in its shot.
- Do not show an abstract placeholder as if it were the product.
- Keep every likely-to-change title, number, URL, color, image, and video source editable.
- Do not export unless the user asks.
- Do not silently replace Dayi when voice generation is unavailable.
- Treat any new effect idea as a separate candidate Prompt test, never as an unreviewed production change.

## Workflow

### 1. Intake

Require:

- Website URL.
- Target ChatCut project or permission to create one.
- Any user-provided reference episode or series update.

Default to:

- 1920×1080, 30 fps, 720 frames.
- Chinese horizontal Bilibili delivery.
- Doubao Dayi voice (`provider: doubao`, `voiceId: dayi`).
- Master V1 visual and shot grammar.

Do not ask for choices already frozen by the series contract.

### 2. Research the Website

Inspect the official site and its official documentation/demo surfaces. Capture:

- The strongest immediately understandable product view.
- One complete core interaction.
- One concrete result or output.
- One proof of scale, usefulness, or credibility when available.
- Brand name, URL, and one source-native accent color.

Record every factual claim with its source. Follow [evidence-and-assets.md](references/evidence-and-assets.md).

### 3. Build the Episode Plan

Copy [episode-plan.template.json](assets/episode-plan.template.json) into a task-local working file. Replace all example values.

Select exactly one controlled flow variant:

- `browse-filter-detail`
- `input-action-result`
- `query-filter-result`
- `input-progress-output`
- `overview-example-detail`

Fill all six shots. Do not change shot IDs, jobs, frame ranges, or master visual-system values.

If `masterReference.status` is `provisional`, produce a calibration episode only. After the user approves its actual rendered result, set the reference to `approved` and record the stable ChatCut timeline or exported-video ID. Later episodes must compare against that reference.

Validate before any ChatCut write:

```powershell
python scripts/validate_episode_plan.py <episode-plan.json> --stage plan
```

If validation fails, repair the plan. Do not work around the validator.

### 4. Acquire Real Media

Follow this priority:

1. Website-provided original video.
2. Website-provided original images.
3. Verified browser screenshot or screen recording.
4. User-provided media.

Use AI generation only for clearly non-product decorative media after explicit user approval. Never use it for UI evidence.

### 5. Execute in ChatCut

Load and follow the applicable ChatCut skills. Use [chatcut-execution.md](references/chatcut-execution.md) as the fixed order of operations.

Create a fresh timeline named:

```text
每日神器网站 <episodeId>｜<websiteName>｜Master V1
```

Execute the six planned shots exactly. Use real media as the visual base; Motion Graphics may focus, label, mask, compare, or arrange that media but may not replace it.

Use compatible root CutDirector Prompts only through the routing table in [shot-grammar.md](references/shot-grammar.md).

### 6. Generate and Place Voice

Generate six separate Dayi segments, one per shot. Keep each segment inside its assigned shot range.

Use a consistent performance direction:

```text
年轻男性科技产品推荐口播，清晰、克制、有节奏；关键功能和数字重读，句尾收稳，不要播音腔。
```

Inspect actual durations before placement. Shorten copy before increasing speed beyond the series limit.

If ChatCut credits are insufficient, keep the verified visual draft, report the missing voice honestly, and stop. Do not use another voice or external TTS without user approval.

### 7. Verify

Render and inspect at least:

- One settled frame from each of S01–S06.
- Every seam between adjacent shots when motion or opacity overlaps.
- The final visible frame.

Complete the `qa` and `delivery` fields in the episode plan, then run:

```powershell
python scripts/validate_episode_plan.py <episode-plan.json> --stage final
```

Do not call the episode complete until final validation passes.

### 8. Handoff

Report:

- Timeline name and duration.
- Real source assets used.
- Any claim or media limitation.
- Voice status.
- Verification status.
- Whether export was requested or intentionally not performed.

Keep failed experiments as clearly named candidate/test timelines; never present them as Master V1.
