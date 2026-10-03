# Lightweight previews

These files are derived from the corresponding original MP4s in
[`verified-prompts`](../verified-prompts/). No new scene, Logo, caption or effect
was added. The source MP4s and existing GIFs remain unchanged.

| Preview | Original | Encoding |
| --- | --- | --- |
| `prompt-001.webp` | `prompt-001-gesture-logo-pop.mp4` | 800px, 12 fps, WebP quality 78 |
| `prompt-002.webp` | `prompt-002-split-screen-explainer.mp4` | 800px, 10 fps, WebP quality 78 |
| `prompt-001-still.jpg` | Same source, at 1 second | Reduced-motion fallback |
| `prompt-002-still.jpg` | Same source, at 12 seconds | Reduced-motion fallback |

The preview has no sound. Open the MP4 for original frame rate, detail and any
audio. A source that has no audio is not made into an audio-verified example.
Reduced-motion preference is handled with a native HTML `picture` source; its
actual behavior must be checked on GitHub after a change.

Reproduction command, from the repository root (replace `N` and `FPS` with the
table values):

```sh
ffmpeg -i assets/verified-prompts/SOURCE.mp4 -vf "fps=FPS,scale=800:-1:flags=lanczos" -an -c:v libwebp_anim -lossless 0 -q:v 78 -compression_level 6 -loop 0 assets/previews/prompt-N.webp
```

Source and derived presenter media follow the [reserved-media policy](../../LICENSE).
