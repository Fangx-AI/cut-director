---
name: cut-director
description: Direct already-shot talking-head, interview, tutorial, lecture, podcast, knowledge, and presenter-led product videos in ChatCut. Use when a user describes a desired visual effect or asks to make speech-led footage more polished, dynamic, cinematic, clear, or visually engaging through visual-beat planning, motion graphics, supporting visuals, speaker composition, reusable CutDirector Prompts, or verified ChatCut execution.
---

# CutDirector

## Scope

Direct visuals for already-shot, presenter-led videos. Preserve finished A-roll and original wording by default. Do not use this Skill for a general montage, an unshot script, or a non-presenter-led video.

Let the user describe the result in natural language. Never ask the user to fill an internal schema, recipe, crop parameter, animation curve, or verification checklist.

## Core Workflow

1. Inspect the source, transcript, timing, frame, speaker, gestures, captions, Logo, product UI, existing text, motion paths, and real empty space.
2. Load only references needed for this request. Identify verbatim anchors and select visual Beats that help the viewer.
3. Match a verified effect recipe when its viewing task and constraints fit. Otherwise design a custom Beat using the same safety and fallback principles.
4. Deliver a confirmable Visual Beat Map and select exactly one representative Beat.
5. After the first approval, initialize or resume the project manifest and pass every recipe gate before executing only the representative Beat.
6. Record actual post-write evidence, reach `verified`, and show the result. Expand only after the second explicit approval.

The model owns semantics, director judgment, visual language, and medium choice. Deterministic scripts own required fields, IDs, time ranges, approval state, asset verification state, fallback chains, and evidence completeness. Read `references/pipeline-contract.md` before execution.

## Confirmation Boundary

Do not generate media, create MG, modify the timeline, consume credits, or claim execution before the first approval.

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

012–015 are local demonstrations, not verified ChatCut recipes. Use as custom Beat references; do not imply native property or real-footage verification. Preserve finished A-roll unless editing it is explicitly within the user’s request. Read [compatibility](references/compatibility.md) before choosing the current execution surface.

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

For full-video planning, use `references/visual-beat-map.md`. For one effect or a local revision, present only the affected content, placement, timing, input needs and preview decision. Keep the complete internal evidence without making the user read every field. A full plan includes:

- overall director judgment and one named visual language;
- the Visual Beat Map with exact displayed content, speaker treatment, safe zones, editable properties, media/person window, asset responsibilities, compositing, sound, user prompt, director constraints, risks, scores, and quality decision;
- exactly one representative Beat;
- segments that should remain clean;
- high-risk or credit-consuming confirmations;
- a first-approval checklist covering visual language, speaker treatment, and every credit-consuming action; and
- the post-approval execution order.

Reply in the user's language. Present the result, not the internal recipe or JSON contract.

## Execution And Validation

After the first approval, read `references/chatcut-execution-handoff.md` and route only the representative Beat to the required ChatCut execution Skills.

Use the internal cache and state flow in `references/pipeline-contract.md`. Before every ChatCut write, merge known facts and require an `executing` transition. After the write, record actual asset, beginning, middle, and ending evidence and require a `verified` transition. For any Beat that covers or replaces the speaker frame, beginning and ending evidence must include the clean frame outside the Beat, the transition in progress, and the settled state; a good middle frame does not prove a clean handoff.

Never expose the manifest, commands, gates, or recovery mechanics as user work. Do not override a validation failure: fix a known fact, apply a documented fallback, or ask for the single blocking input. Show the verified result and wait for the second approval before expansion.
