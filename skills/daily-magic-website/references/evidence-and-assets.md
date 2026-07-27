# Evidence and Asset Policy

## Source Hierarchy

Prefer:

1. Official product page or official documentation.
2. Official demo video, screenshots, press kit, or product account.
3. Visible browser capture of the official product.
4. User-provided media with known provenance.

Use third-party commentary only for discovery, never as the sole proof of a product claim when an official source exists.

## Required Evidence Record

For every spoken number, capability, comparison, or availability claim, record:

- Claim ID.
- Exact claim text.
- Direct source URL.
- Evidence type.
- Capture date.
- Whether the evidence was captured.

Do not use a claim in narration until `evidenceCaptured` is true.

## Real UI Rule

Real product UI must come from:

- Original website images or videos.
- Browser screenshots.
- Browser screen recordings.
- User-provided product media.

Never:

- Generate a fake UI.
- Replace missing UI with skeleton cards.
- Use abstract placeholders while describing a concrete feature.
- Reconstruct a brand logo.
- Present a Motion Graphic as a screenshot of the product.

Motion Graphics may add:

- Masks and focus regions.
- Labels and pointers.
- Accurate editable text.
- Verified numbers.
- Layout of several real source images.

## Media Record

Each material needs:

- Stable material ID.
- Type: `official-video`, `official-image`, `browser-screenshot`, `browser-recording`, or `user-provided`.
- Source URL or local source reference.
- `provenanceVerified: true`.
- Rights status sufficient for the user’s intended use.

Shots S01–S05 must reference at least one material. S06 may reuse a prior material.

## Missing Evidence

If the website blocks access or a critical feature requires unavailable authentication:

- State the limitation.
- Remove or soften the unsupported claim.
- Do not replace the missing proof with generated media.
- Ask for user-provided footage only when it materially changes the episode.
