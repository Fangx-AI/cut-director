---
name: daily-info-gap-video
description: Produce a finished Chinese daily information-gap or news-recap video from current hot topics, including research, deduplication, material-first scripting, ChatCut editing, energetic narration, subtitles, a segmented top progress bar, covers, 4K export, and posting copy. Use for requests such as “做今天的AI每日大事”, “做一期90秒科技信息差”, “把今日热点剪成成片”, or recurring daily news-video production.
---

# Daily Info Gap Video

Create the complete publish-ready package, not just a topic list or script. Treat “AI每日大事” as one preset of a reusable workflow that can also cover technology, business, products, finance, and other daily information-gap topics.

This is an end-to-end finished-video Skill. Treat CutDirector’s verified Prompts as optional shot-level building blocks: a Prompt solves one local viewing or editing task, while this Skill owns the whole episode from topic selection through export and delivery. Never mistake successful execution of one Prompt for completion of the video.

## Load the production rules

Always read:

- `references/editorial-rules.md`
- `references/production-spec.md`
- `references/cover-and-delivery.md`

Also read `references/ai-daily-preset.md` when the subject is AI or the user asks for “AI每日大事”.

For an editable ChatCut project, invoke `chatcut:chatcut-plugin-basics` first, then use the relevant ChatCut skills for asset import, transcription, voice, motion graphics, verification, image/video generation, and export. Follow each invoked skill exactly.

## Defaults

Unless the user overrides them:

- Language and audience: Simplified Chinese, mainland general audience
- Format: 16:9 landscape
- Duration: about 90 seconds; fit the story count to the day rather than forcing five items
- Opening line: `90秒看完今日{主题}大事`
- Narration: `liuchang`, bright, high-energy, confident technology-news delivery for the entire episode
- Export: highest practical quality, target 4K
- Covers: one 4:3 landscape image and one 3:4 portrait image
- Publishing: prepare a semi-automatic handoff; do not submit the final platform post without explicit authorization

Ask a question only when a missing choice would materially change the result. Otherwise state the assumption and continue.

## Workflow

### 1. Set the episode brief

Resolve the date, subject, target platform, approximate duration, prior-episode cutoff, and delivery folder. If the user supplied a hot-list page or source feed, use it as the candidate pool rather than as the sole authority.

### 2. Research and select stories

Browse current sources because daily news is time-sensitive. Verify each candidate against the original announcement or another authoritative source whenever possible.

Build a compact candidate ledger containing:

- event and source
- publication/event time
- heat or corroboration count
- why a general viewer should care
- duplicate cluster and prior-episode status
- available real video, images, or generated-material need

Remove repeated events and near-duplicates. Prefer stories that are fresh, widely discussed, consequential, understandable, and visually expressible. Select the natural number of worthwhile stories, normally three to seven.

### 3. Acquire and inspect materials before writing

Create a shot ledger per story. Use this priority:

1. Relevant real video
2. Relevant real image
3. Generated video or image only when necessary

Inspect every video clip before scripting: identify what it visibly proves, usable time ranges, shot changes, logos/text, resolution, and whether its pacing supports narration. Never write claims that the available visuals cannot support.

Do not reuse the same shot or materially identical image in separate timeline positions unless the repetition is an explicit recap. Track asset IDs and source URLs to enforce this.

### 4. Write to the edit

Write a beat sheet that maps each narration clause to an exact visual. Start with the opening promise, then move immediately into the first story’s visual as soon as the first story is mentioned.

The copy must explain the public-facing consequence before technical parameters. Use concrete language, tension, comparison, surprise, and “why it matters”; avoid reading specifications, corporate phrasing, and rigid “第一条、第二条” enumeration.

Keep narration nearly continuous. Rewrite, tighten visuals, or add a short connective line if a silent gap would exceed about 0.5 seconds outside an intentional pause.

### 5. Build the editable video

Create or update the ChatCut project:

- place narration first and cut visuals to its semantic beats
- use actual video whenever available
- add readable Chinese subtitles
- add the persistent segmented top progress bar described in `references/production-spec.md`
- use restrained transitions that preserve momentum
- keep all on-screen microcopy Chinese unless a proper noun requires English
- keep music and effects below narration

Generate missing media only after real-media options are exhausted. Generated clips must be clearly aligned with the spoken claim and must not impersonate documentary evidence.

### 6. Create covers and posting package

Generate both cover ratios from the same visual identity and episode hook. Use the fixed prompt framework in `references/cover-and-delivery.md`, changing only the date, theme, hero subject, and short hook.

Prepare title, description, tags, source notes, and any AI-content declaration. Keep titles curiosity-driven but factually defensible.

### 7. Verify and export

Watch the full timeline and verify:

- story and visual start on the same beat
- no duplicate footage
- narration stays bright and energetic throughout
- no unexplained long silence
- captions are accurate and readable
- the top bar fills smoothly and its segment boundaries match the edit
- no unsupported claims or stale/repeated stories
- cover text is legible at thumbnail size

Export the final video and package it with both covers and posting metadata in the dated folder. Report exact clickable file paths.

## Typical triggers

- “生成今天的AI大事90秒视频”
- “从这个热榜挑最值得讲的几件事，直接做成片”
- “做一期面向大众的科技信息差，不要堆参数”
- “沿用昨天的风格，但不要重复昨天的事情和素材”
