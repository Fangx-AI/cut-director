# Master V1 Shot Grammar

## Timeline

| Shot | Frames | Seconds | Viewer job | Required visual |
|---|---:|---:|---|---|
| S01 | 0–89 | 0.0–3.0 | Hook the problem | Strongest real product view |
| S02 | 90–209 | 3.0–7.0 | Identify and prove the website | Full real page plus one sourced fact |
| S03 | 210–359 | 7.0–12.0 | Show the core operation | One continuous real user action |
| S04 | 360–509 | 12.0–17.0 | Show the concrete result | Real output/result/detail |
| S05 | 510–629 | 17.0–21.0 | Clarify who should use it and why | Real evidence with at most three labels |
| S06 | 630–719 | 21.0–24.0 | Close and hold | Website name, URL, restrained real page |

Frame ranges are half-open in data: `startFrame` inclusive and `endFrame` exclusive.

## Copy Limits

| Shot | Voiceover maximum | On-screen text maximum |
|---|---:|---:|
| S01 | 28 Chinese characters | 14 characters |
| S02 | 36 | 16 |
| S03 | 38 | 16 |
| S04 | 38 | 16 |
| S05 | 32 | 18 |
| S06 | 26 | 18 |

Count punctuation and Latin tokens conservatively. Shorten copy when it does not fit. Do not speed Dayi beyond `1.18`.

## Flow Variants

Choose one:

- `browse-filter-detail`: libraries, galleries, directories, inspiration sites.
- `input-action-result`: utilities and transformation tools.
- `query-filter-result`: search, data, and discovery products.
- `input-progress-output`: generators and asynchronous creation tools.
- `overview-example-detail`: static resources, showcases, and collections.

S03 must show the middle action of the selected flow. S04 must show its real result. Do not change the shot order to accommodate missing evidence; acquire better evidence or state the limitation.

## CutDirector Prompt Routing

Use these parent-repository recipes only when their real viewing task matches:

| Need | Root recipe |
|---|---|
| Website provides an original diagonal page wall video | `../../../recipes/prompt-005-diagonal-card-waterfall.json` |
| A high-resolution real page needs typing annotation and focus lock | `../../../recipes/prompt-007-hd-page-focus-lock.json` |
| Three to five verified real images need a deck and selected hero | `../../../recipes/prompt-008-real-image-deck-hero.json` |
| A real input, feedback, and result causal chain must be explained | `../../../recipes/prompt-009-input-feedback-result.json` |

Read the matching public explanation in `../../../references/` before use.

Do not add a Prompt because it looks impressive. A mismatch between Prompt job and shot job is a validation failure.

## Transition Rules

- Default seam: hard cut.
- S01→S02: masked push only when the same real page continues.
- S02→S03: hard cut into the first action frame.
- S03→S04: action-result cut or the source video’s natural continuation.
- S04→S05: hard cut.
- S05→S06: restrained dip or opacity settle lasting no more than 10 frames.
- Hold the final URL fully readable for at least 24 frames.
