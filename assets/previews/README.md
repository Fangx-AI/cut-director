# Lightweight previews

These files are derived from existing project media. No new scene, Logo,
caption or effect was added. The source MP4s and existing GIFs remain unchanged.
Animated previews 001, 002 and 005 use the corresponding original MP4s in
[`verified-prompts`](../verified-prompts/). Preview 004 uses the existing GIF,
which is already a shortened overview of the 87-second source video.

| Preview | Original | Encoding |
| --- | --- | --- |
| `prompt-001.webp` | `prompt-001-gesture-logo-pop.mp4` | 800px, 12 fps, WebP quality 78 |
| `prompt-002.webp` | `prompt-002-split-screen-explainer.mp4` | 800px, 10 fps, WebP quality 78 |
| `prompt-004.webp` | `prompt-004-top-chapter-progress-rail.gif` | 800px, 10 fps, WebP quality 78 |
| `prompt-005.webp` | `prompt-005-diagonal-card-waterfall.mp4` | 800px, 12 fps, WebP quality 78 |
| `prompt-001-still.jpg` | Same source, at 1 second | Reduced-motion fallback |
| `prompt-002-still.jpg` | Same source, at 12 seconds | Reduced-motion fallback |

The gallery also has static reduced-motion fallbacks for 003-015:

| Preview | Source location | Frame time |
| --- | --- | --- |
| 003 | Original MP4 in `verified-prompts` | 4.5 seconds |
| 004 | Original MP4 in `verified-prompts` | 25 seconds |
| 005 | Original MP4 in `verified-prompts` | 2.5 seconds |
| 006 | Original MP4 in `verified-prompts` | 2 seconds |
| 007 | Original MP4 in `verified-prompts` | 1.5 seconds |
| 008 | Original MP4 in `verified-prompts` | 1.8 seconds |
| 009 | Original MP4 in `verified-prompts` | 2.7 seconds |
| 010, 011, 013-015 | Original MP4 in [`prompt-examples`](../prompt-examples/) | 4.5 seconds |
| 012 | Original MP4 in `prompt-examples` | 3.3 seconds |

The preview has no sound. Open the MP4 for original frame rate, detail and any
audio. A source that has no audio is not made into an audio-verified example.
Reduced-motion preference is handled with a native HTML `picture` source; its
actual behavior must be checked on GitHub after a change.

Reproduction command, from the repository root (replace `N` and `FPS` with the
table values). 004 reads the existing GIF instead of the MP4; 004 and 005 use
compression level 3, while 001 and 002 use level 6:

```sh
ffmpeg -i assets/verified-prompts/SOURCE.mp4 -vf "fps=FPS,scale=800:-1:flags=lanczos" -an -c:v libwebp_anim -lossless 0 -q:v 78 -compression_level 6 -loop 0 assets/previews/prompt-N.webp
```

Static fallbacks use `-ss TIME -frames:v 1 -vf "scale=800:-1:flags=lanczos" -q:v 3`.

Source and derived presenter media (001-009) follow the [reserved-media policy](../../LICENSE).
Original local demonstrations (010-015) and their derived stills retain CC BY-SA 4.0;
the same third-party and trademark exceptions still apply.
