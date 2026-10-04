---
name: cut-director
description: Edit recorded talking-head and speech-led videos in ChatCut. Use for filler-word, false-start, retake and redundant-sentence cleanup, natural pacing, captions, audio, motion graphics, B-roll and export, or a local revision to any of these. Preserve the speaker's meaning and voice while delivering an editable, verified cut.
---

# CutDirector

## Scope

Edit already-recorded talking-head, tutorial, lecture, interview, podcast and presenter-led product footage. Spoken delivery drives the edit: clean the speech, establish its rhythm, then support it with captions, sound and visuals as requested. Preserve the speaker's intended meaning, factual qualifiers and natural voice. Do not use this Skill for an unshot script or a general non-speech montage.

Let the user describe the result in natural language. Never ask the user to fill an internal schema, recipe, crop parameter, animation curve, or verification checklist.

## Choose The Requested Edit

Read [the talking-head workflow](references/talking-head-workflow.md) for a full edit. Load only the branch needed for a local request:

| User request | Work to do |
| --- | --- |
| Remove fillers, false starts, mistakes, retakes or dead air | Read [speech editing](references/speech-editing.md), edit A-roll and listen to the joins; no visual plan required |
| Remove redundant sentences, shorten or restructure | Read speech editing; distinguish duplicate content from useful examples, qualifications and emphasis; only reorder within the requested scope |
| Add or revise captions, voice treatment, music or export | Read the matching section of the workflow and current host guidance; preserve the accepted speech cut |
| Add one animation or effect | Use the visual workflow below on the current cut; preserve A-roll |
| Edit the whole talking-head video | Clean speech first, establish current timing, then captions, sound and suitable visual Beats; deliver the requested editable project or export |

For a general edit with no pacing preference, use natural pacing. Honor supplied duration targets and preferences without another intake form. When the user supplies only text, give an editorial proposal; do not claim to have cut speech or validated sound.

## Speech Editing

Use the current host's talking-head and transcription guidance. The spoken-content edit surface is Script where available: read the current script, stage semantic edits, apply the authorized edit, and read the regenerated result. ASR corrections do not cut audio. Read [speech editing](references/speech-editing.md) before selecting cuts.

- Judge fillers by their role in the actual sentence and audio, not a global word list. Never delete characters inside words such as `额度` or `那个方案`.
- Choose one complete, correct and well-delivered take; the last take is a candidate, not an automatic winner. Retain useful setup that is absent from the replacement.
- Distinguish mistakes from emphasis, callbacks, summaries and repeated statements that add a qualifier or new information. Do not remove unique meaning under the label "redundant".
- Compress empty delays while keeping clause boundaries, breaths and rhetorical pauses. Low volume or an ASR gap alone does not prove silence.
- Resolve explicit must-keep sentences and pauses to source ranges before cutting. Preserve each protected unit intact; a request to tighten pacing does not cancel it.
- Keep linked audio and video together. A Script gap on the only video track can produce black; retain source silence when breathing room is needed.
- After each applied batch, re-read the actual timeline. Speech changes invalidate downstream timing; regenerate captions and re-anchor visuals, gestures and sound to the current cut.

For linear 1x edits with known source ranges, [the speech edit plan](references/speech-edit-plan.md) checks boundaries and protected units, maps anchors, and locates changed joins for review. It validates a chosen edit; it does not decide which sentences to delete, transcribe media or execute ChatCut calls. The existing visual recipe manifest is for visual effects, not a prerequisite for ordinary speech cleanup.

## Visual Workflow

1. Inspect the current speech cut, transcript, timing, frame, speaker, gestures, captions, Logo, product UI, existing text, motion paths, and real empty space. If this task includes speech cleanup, stabilize that edit first.
2. Load only references needed for this request. Identify verbatim anchors and select visual Beats that help the viewer.
3. Match a verified effect recipe when its viewing task and constraints fit. Otherwise design a custom Beat using the same safety and fallback principles.
4. Deliver a confirmable Visual Beat Map and select exactly one representative Beat.
5. After the first approval, initialize or resume the project manifest and pass every recipe gate before executing only the representative Beat.
6. Record actual post-write evidence, reach `verified`, and show the result. Expand within actual authorization recorded as second-approval evidence; request it only when it is missing.

The model owns semantics, director judgment, visual language, and medium choice. Deterministic scripts own required fields, IDs, time ranges, approval state, asset verification state, fallback chains, and evidence completeness. Read `references/pipeline-contract.md` before execution.

## Authorization And Review

A request to clean or edit speech authorizes reversible editing within that scope. If the user requests preview only, stage and preview without applying. Do not force a Visual Beat Map or representative-animation approval onto a speech-only task. Ask only about a content-changing decision outside the requested scope or a missing input that prevents a reliable cut.

For new visual directions or credit-consuming generation, use the visual proposal and recipe gates below. Existing authorization carries forward within its scope; do not claim work is complete before it has been executed and checked.

Use existing source context and approvals before asking for anything. Planning, Prompt selection, and read-only inspection do not require execution approval. For a simple requested effect, give a short proposal proportional to the task; do not force a full-video table or reject effect density the user did not request.

If execution approval is missing, show the concrete representative proposal and ask only for the missing decision. If a source or verbatim anchor is missing, ask one focused source question. Never invent timing or facts.

Approvals persist within their actual scope. Record existing approval evidence in the manifest rather than repeatedly asking the same question. A local revision to an accepted Beat can reuse valid direction and scope; update affected facts and verification evidence. New direction, material scope changes, or additional paid actions need the applicable authorization. Do not fabricate the `first` or `second` evidence fields or bypass the existing pipeline gates.

## Recipe Routing

Load only the matching recipe and its public reference:

| User intent | Internal recipe | Public compatibility path |
| --- | --- | --- |
| Official Logo follows a confirmed pointing gesture | `recipes/prompt-001-gesture-logo-pop.json` | `references/prompt-001-gesture-logo-pop.md` |
| Left-side points plus a continuously scrolling long-text evidence column | `recipes/prompt-002-split-screen-explainer.json` | `references/prompt-002-split-screen-explainer.md` |
| One official brand icon connects two product modes, with progressive capabilities and a final result comparison | `recipes/prompt-003-brand-mode-comparison.json` | `references/prompt-003-brand-mode-comparison.md` |
| An adaptive progress overlay selects full section tabs, current-section mode, progress-only, or keep-clean from the actual structure, aspect ratio, and safe zones | `recipes/prompt-004-top-chapter-progress-rail.json` | `references/prompt-004-top-chapter-progress-rail.md` |
| Reuse a verified website-provided `page-waterfall-wall.mp4` unchanged; recreate from real screenshots only when no source exists and the user explicitly approves | `recipes/prompt-005-diagonal-card-waterfall.json` | `references/prompt-005-diagonal-card-waterfall.md` |
| Three original-style light-background cards flip from independently editable front faces to independently editable back faces, with the face swap only at the 90-degree edge | `recipes/prompt-006-editable-three-card-flip.json` | `references/prompt-006-editable-three-card-flip.md` |
| A verified high-resolution real page receives editable typing annotation, a dimming mask, and an accurately positioned focus lock | `recipes/prompt-007-hd-page-focus-lock.json` | `references/prompt-007-hd-page-focus-lock.md` |
| Three to five verified real images fly in as a deck, settle into a fan, and elevate a user-selected hero card | `recipes/prompt-008-real-image-deck-hero.json` | `references/prompt-008-real-image-deck-hero.md` |
| Editable input, feedback, and result beats explain one causal chain; optional real result media is verified and abstract UI never masquerades as a product interface | `recipes/prompt-009-input-feedback-result.json` | `references/prompt-009-input-feedback-result.md` |

Treat recipe triggers as routing evidence, not keyword-only commands. A visual resemblance is insufficient when the viewing task differs.

Apply the recipe's required inputs, asset strategy, safe zones, timing, fallback chain, and verification rules internally. Keep the published Prompt text and paths stable. If a recipe blocks execution, follow its named fallback rather than improvising around the guardrail.

For gesture effects, require a user-confirmed exact time range before asset acquisition or timeline work. If several gestures are plausible, inspect candidate frames and ask only for the exact target range. Do not equate any moving hand with an intentional trigger.

For real brands, use verifiable official assets and never generate, redraw, or stylistically imitate a real Logo. If identity or provenance cannot be verified, stop that asset and request one verified source.

## Viewer-task routing

For reusable material, consult [the Prompt index](PROMPT-LIBRARY.md). In addition to the existing verified recipes:

- Music and visual emphasis do not land together: [012](references/prompt-012-semantic-audio-accent.md).
- Clauses should accumulate toward one conclusion: [013](references/prompt-013-incremental-payoff.md).
- Show a real change to the same subject: [014](references/prompt-014-matched-before-after.md).
- Connect real demonstration clips within existing speech: [015](references/prompt-015-demo-relay.md).
- Adapt 006/008 to another ratio or add a following focus to 007: [variants](references/prompt-variants.md).

012–015 are local demonstrations, not verified ChatCut recipes. Use as custom Beat references; do not imply native property or real-footage verification. Preserve accepted A-roll for visual-only tasks. Read [compatibility](references/compatibility.md) before choosing the current execution surface.

## Planning References

### Supplementary Prompt material

For a release/count/viewer-benefit title sequence, consult [Prompt 010](references/prompt-010-three-stage-count-hook.md). For multiple persistent task cards moving through workflow states, consult [Prompt 011](references/prompt-011-task-board-progression.md).

These are local Remotion examples, not verified ChatCut recipes. Use them as custom-Beat references within the existing scope and approval workflow; do not claim ChatCut execution or property editability from the local preview. Their source files and verification limits are linked in each reference. Do not substitute Prompt 010 for a full-video progress rail (004), or Prompt 011 for a single input–feedback–result explanation (009).

For full-video planning, consult these references as needed:

1. `references/visual-director-framework.md`
2. `references/transcript-to-beats.md`
3. `references/visual-language.md`
4. `references/visual-beat-map.md`
5. `references/quality-gate.md`

Then load only what the selected Beats need:

| Need | Load |
| --- | --- |
| Official Prompt lookup or reuse | `references/chatcut-official-catalog.md`, `references/chatcut-prompt-routing.md`, `references/chatcut-official-prompt-patterns.md` |
| Full-screen, PiP, split-screen, or speaker placement | `references/composition-and-speaker-presence.md` |
| Keywords, lists, charts, chapter cards, or other MG | `references/mg-animation-director.md` |
| Generated visuals, images, or B-roll | `references/generated-visuals-director.md` |
| Full examples | `references/examples-zh.md` or `references/examples-en.md` |

Treat official ChatCut patterns as information-structure and motion references, never mandatory aesthetics, fabricated product UI, or automatic speaker placement.

## Director Rules

- Preserve transcript anchors verbatim. Use approximate or anchor-only timing when exact timestamps are unavailable.
- Default to 3-8 Beats per 30-60 seconds; fewer or zero is valid.
- Keep one purpose and one visual focus per Beat. A generated Beat defaults to one continuous shot and one primary camera move.
- Protect face, captions, gestures, product, Logo, existing text, and motion paths. Lower-right PiP is never a default.
- Let real product UI become the primary focus whenever visible; keep overlays secondary and non-obstructive. Never fabricate product UI as evidence.
- Give every reference asset one explicit responsibility.
- Apply the Quality Gate. Delete or downgrade weak, obstructive, misleading, visually cheap, or unverifiable candidates.

## User-Facing Output

For speech editing, show the usable project or preview, duration change, a short explanation of the meaningful cuts and any passages needing review. Quote actual words instead of internal segment IDs. Do not require the user to approve a row for every filler.

For full-video visual planning, use `references/visual-beat-map.md`. For one effect or a local revision, present only the affected content, placement, timing, input needs and preview decision. Keep the complete internal evidence without making the user read every field. A full visual plan includes:

- overall director judgment and one named visual language;
- the Visual Beat Map with exact displayed content, speaker treatment, safe zones, editable properties, media/person window, asset responsibilities, compositing, sound, user prompt, director constraints, risks, scores, and quality decision;
- exactly one representative Beat;
- segments that should remain clean;
- high-risk or credit-consuming confirmations;
- a first-approval checklist covering visual language, speaker treatment, and every credit-consuming action; and
- the post-approval execution order.

Reply in the user's language. Present the result, not the internal recipe or JSON contract.

## Execution And Validation

Read [the execution handoff](references/chatcut-execution-handoff.md) for the active speech, caption, audio, visual or export task. For visual execution, route the approved representative Beat to the required current ChatCut capabilities.

For visual recipe writes, use the internal cache and state flow in `references/pipeline-contract.md`, merge known facts and require an `executing` transition. After the write, record actual asset, beginning, middle, and ending evidence and require a `verified` transition. For any Beat that covers or replaces the speaker frame, beginning and ending evidence must include the clean frame outside the Beat, the transition in progress, and the settled state; a good middle frame does not prove a clean handoff.

For speech cuts, verify the regenerated transcript and actual audio at changed joins, plus A/V sync, visible continuity and the ending. For captions, verify the current cut's wording, timing and safe areas. For an export, inspect the actual file, requested resolution, sound and start/end. Script checks, rendered frames and listening are different evidence; disclose any unavailable check. New speech rules are not automatically covered by the existing nine verified visual recipes.

Never expose the manifest, commands, gates, or recovery mechanics as user work. Do not override a validation failure: fix a known fact, apply a documented fallback, or ask for the single blocking input. Show the verified result and request expansion approval only if the corresponding authorization is missing.
