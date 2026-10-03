<div align="center">

<img src="assets/cutdirector-cover-v2.jpg" alt="CutDirector: speech-led editing, natural rhythm, and focused visuals. Concept artwork, not a product screenshot." width="100%">

# CutDirector

**Clean the speech. Keep the voice. Make the point visible.**

A ChatCut editing skill for already-recorded talking-head videos.
Filler words, retakes, pacing, captions, sound, and visuals, all serving what you say.

[Get started](#get-started) · [Watch examples](#watch-real-examples) · [Choose a visual](PROMPT-LIBRARY.md) · [中文](README.md)

</div>

## Get Started

In Codex with Skill Installer, send:

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

Restart Codex, connect ChatCut, and open your project. For a terminal installation with Node.js, see the [skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add Fangx-AI/cut-director --skill cut-director --agent codex --global
```

Then ask for the outcome:

```text
Use $cut-director on this talking-head video.
Remove meaningless fillers, failed retakes,
redundant sentences, and empty delays.
Keep the meaning and natural delivery.
Add clear captions and relevant visuals.
Preview one clip for any new visual style.
```

You can request just one change, such as "remove fillers only," "tighten the pacing," "fix captions," or "add a Logo here." Keep the accepted parts of the edit.

Execution requires accessible media and the appropriate ChatCut tools. Text alone supports a proposal, not audio editing or listening validation. The skill does not include a ChatCut account or generation credits.

## Watch Real Examples

[![Official brand icons appear beside the presenter at confirmed pointing gestures](assets/verified-prompts/prompt-001-gesture-logo-pop.gif)](assets/verified-prompts/prompt-001-gesture-logo-pop.mp4)

**001 · Gesture-triggered Logos** · Verified on a ChatCut timeline.

Keep the presenter full-frame; place official assets at confirmed gesture times without covering the face or captions.

[Prompt and conditions](references/prompt-001-gesture-logo-pop.md) · [Full video](assets/verified-prompts/prompt-001-gesture-logo-pop.mp4)

[![Key points appear on the left while supporting long text scrolls slowly on the right](assets/verified-prompts/prompt-002-split-screen-explainer.gif)](assets/verified-prompts/prompt-002-split-screen-explainer.mp4)

**002 · Points and scrolling evidence** · Verified on a ChatCut timeline.

Explain the points while showing the underlying text. Adjust its speed and space without extending the clip just to display every line.

[Prompt and conditions](references/prompt-002-split-screen-explainer.md) · [Full video](assets/verified-prompts/prompt-002-split-screen-explainer.mp4)

**[Explore all 15 animated examples →](PROMPT-LIBRARY.md)**

## Start With The Speech

| Problem | Editorial approach |
| --- | --- |
| Hesitation and failed starts | Remove meaningless fragments, not every connector or repeated word |
| Several takes of the same sentence | Keep the complete, correct, well-delivered take, not automatically the last |
| Repetition and rambling | Remove covered content; preserve new facts, examples, qualifications and emphasis |
| Long delays or rushed joins | Keep breaths and rhetorical pauses; listen to the changed joins |
| Captions or effects drift after cuts | Re-read the current cut and re-anchor downstream timing |
| A point needs visual support | Choose relevant Logos, keywords, steps, charts or real supporting footage |

The full path is **speech cut → aligned captions → purposeful visuals and sound → editable project and requested export**. A local change goes directly to its relevant stage.

> **Validation scope:** 9 visual examples were verified in their original ChatCut cases; 6 are local animation demos. The new speech rules and linear timing helper have synthetic logic tests. Real-footage deletion accuracy, natural audio, and end-to-end export still need regression testing. The cover is concept artwork. See [test scope](tests/speech-validation.md).

## Choose By What The Viewer Needs

| Viewing task | Starting point |
| --- | --- |
| Recognize a brand | [001 · Gesture Logo](references/prompt-001-gesture-logo-pop.md) |
| Explain points alongside source text | [002 · Split screen](references/prompt-002-split-screen-explainer.md) |
| Follow a long explanation | [004 · Chapters and progress](references/prompt-004-top-chapter-progress-rail.md) |
| Focus on a real page | [007 · Page focus](references/prompt-007-hd-page-focus-lock.md) |
| See a change in the same subject | [014 · Matched before/after](references/prompt-014-matched-before-after.md) |
| Accumulate toward one conclusion | [013 · Incremental payoff](references/prompt-013-incremental-payoff.md) |

```text
Use $cut-director with Prompt [number].
Target: [sentence or time range].
Keep my speech cut and style.
Show one clip first.
```

[Visual library](PROMPT-LIBRARY.md) · [Full prompts](PROMPTS.md) · [123 official references](VISUAL-GALLERY.md) · [Aspect-ratio variants](references/prompt-variants.md)

The detailed visual pages are currently in Chinese. Replies and project work should follow your language.

## Keep Improving The Accepted Cut

"Restore this sentence," "make the text larger, leave the rest," and "scroll slower without extending the clip" are local revisions. Preserve accepted direction and verify what changed.

The skill serves talking-head videos, tutorials, lectures, interviews, and presenter-led product explanations. Topic selection, unshot scriptwriting, and publishing belong to other workflows.

[Contribute a real example](CONTRIBUTING.md) · [Report an issue](https://github.com/Fangx-AI/cut-director/issues) · [Changelog](CHANGELOG.md)

<details>
<summary>Developer checks and deeper references</summary>

```sh
python scripts/validate_talkdirector.py
python -m unittest discover -s tests
python scripts/check_local_links.py
```

[Skill definition](SKILL.md) · [Talking-head workflow](references/talking-head-workflow.md) · [Speech editing](references/speech-editing.md) · [Host compatibility](references/compatibility.md) · [Research](references/talking-head-research.md) · [Demo sources](assets/prompt-examples/source/README.md)

</details>

## Licensing

Code: **AGPL-3.0-or-later**. Original prompts and documentation: **CC BY-SA 4.0**.
Using the skill does not automatically relicense your own output. Presenter footage, brand media, official references and third-party Logos have separate rights.

[Full license](LICENSE) · [Attribution](NOTICE) · [Brand policy](TRADEMARKS.md) · [Third-party notices](THIRD_PARTY_NOTICES.md)
