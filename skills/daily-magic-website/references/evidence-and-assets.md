# Evidence and Assets

## Principle

The product is the visual. Motion Graphics may direct attention to real evidence but may not substitute for it.

## Asset Priority

Use:

1. Official embedded demo video
2. Official downloadable image, logo, or product media
3. Verified browser screen recording
4. Verified browser screenshot
5. User-provided media

Do not use:

- AI-generated product UI
- Hand-redrawn interface
- Generic stock footage presented as the product
- Empty wireframes, skeleton screens, or placeholder cards
- A third-party screenshot when the official state can be captured

Decorative generated media is outside the reference grammar and requires explicit user approval.

## Capture Rules

For each browser recording:

- Start from a loaded, readable state.
- Use a deterministic viewport and zoom.
- Hide unrelated browser chrome when possible.
- Remove cursor wandering, failed clicks, and loading dead time.
- Record a complete interaction with its visible result.
- Capture enough pre-roll and post-roll for a clean edit.
- Do not crop away the control that caused the result.
- Preserve text sharpness; avoid scaling beyond the source resolution.

For each screenshot:

- Capture the exact state supporting the planned claim.
- Keep the source page URL.
- Record capture date and viewport.
- Preserve the original before annotation.

## Claim Ledger

Every factual statement needs a claim record:

- `id`
- exact spoken or visible text
- source URL
- evidence type
- capture time
- `evidenceCaptured: true`
- optional notes about volatility

Numbers, awards, prices, “free”, “no login”, privacy claims, language counts, platform support, and user counts are claims.

If a claim changes, recapture it. If it cannot be verified, remove or rewrite it.

## Material Ledger

Every material needs:

- `id`
- `type`
- source URL or local path
- capture time
- provenance status
- rights status
- whether it contains product UI
- `synthetic: false`

Allowed types:

- `official-logo`
- `official-image`
- `official-video`
- `browser-screenshot`
- `browser-recording`
- `user-provided`

## Viewer-Job Substitution

When a literal reference element does not exist, preserve the viewer job:

- Usage number → official customer list, review score, award, case study, or adoption proof
- “Free” → no login, open source, browser access, trial, export, or another verified objection remover
- Language dropdown → search, install, import, login, upload, export, or another first-use path

Do not preserve a literal scene by inventing content.

## Repository Boundary

Do not commit the user’s source master or acquired third-party media unless the user explicitly authorizes redistribution and the rights status permits it.

The Skill repository should contain:

- Analytical measurements
- Source metadata and hashes
- Plans and validators
- Reusable instructions

It should not contain the original master video or copied website media by default.
