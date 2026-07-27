# Production specification

## Visual system

- Default canvas: 16:9 landscape
- Target export: 3840×2160 when source and tool limits allow
- Chinese-first labels; retain English only for proper nouns, logos, and product names
- Use a consistent dark technology-news palette with one warm alert accent and one cool information accent unless the user supplies a brand system
- Keep the first frame simple: the opening promise only, without the first story headline

## Material priority and uniqueness

Use real video before images. Use images before generated media. Crop and animate images only when it adds readable motion, not to disguise lack of footage.

Assign every placed asset a unique ledger ID. Before final export, compare adjacent and non-adjacent shots for identical frames, repeated source clips, repeated screenshots, and near-identical crops. Replace accidental repeats.

When the narration first names a person, company, model, product, or event, the picture must already show that subject or an unmistakably relevant visual.

## Narration

- Default voice: `liuchang`
- Delivery: bright, upbeat, high-energy, confident, quick but intelligible technology bulletin
- Maintain the same energy through every story and the ending
- Do not use a low, sentimental, sleepy, solemn, or documentary-style opening
- Avoid silent gaps longer than about 0.5 seconds, except a deliberate beat no longer than about 0.8 seconds
- Use short pickup lines or visual compression rather than padding with empty music

Listen to the rendered audio, not only the TTS prompt. Regenerate any line whose actual delivery drops in energy.

## Subtitles

- Burn in Simplified Chinese subtitles unless the user requests a separate subtitle file
- Keep each subtitle to one or two short lines
- Break by meaning, not fixed character count
- High contrast with a subtle stroke or background plate
- Keep subtitles clear of the top progress bar and platform UI-safe edges
- Verify names, model numbers, dates, and punctuation manually

## Segmented top progress bar

Create one persistent horizontal navigation strip at the very top of the frame. It represents the whole video, not only the current story.

Structure:

- left cap: `片头`
- one dynamic segment per selected story, labeled with a concise Chinese topic
- right cap: `片尾`
- a thin active fill line advances continuously from 0% at video start to 100% at video end
- the active story segment receives a restrained highlight

Rules:

- Derive labels and segment durations from the final timeline; never hard-code five stories
- Segment widths should roughly reflect actual story durations while remaining legible
- Progress must be driven by global timeline time, not reset for each story
- Keep the bar within the top safe area and small enough not to cover key footage
- Use Chinese labels whenever possible
- Motion must be smooth and deterministic
- If a story is removed or reordered, regenerate both labels and timing

## Transitions and sound

- Prefer direct cuts, short directional wipes, scale/position matches, and brief graphic bridges
- Avoid decorative transitions that delay the next visual
- Background music should add urgency without masking consonants
- Use sound effects sparingly for the opening, section changes, and progress milestones

## Final watch checklist

Watch once for story logic, once for picture/audio sync, and once at thumbnail/mobile scale. Check the first five seconds separately because retention is most fragile there.
