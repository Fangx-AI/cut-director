# 字幕样式

默认还是 [subtitles.md](subtitles.md) 里的普通字幕。只有用户明确要“美化、花字、重点强调、高亮、动画、卡拉OK”之类时，才从下面选一种。断句、文字、时间、位置的规则不变：**只改样式，不改字，不加话。**

用 [scripts/subtitle_styles.py](../scripts/subtitle_styles.py) 把校对好的 SRT 转成 ASS，再在出成片的那一次编码里用 ffmpeg 的 `ass` 滤镜烧进去（`ass=字幕.ass:fontsdir=字体文件夹`）。不要在已经烧过字幕的成片上再烧一遍：会叠字，画质也会再降一次。要从原片按剪辑记录重新编码。

```bash
python scripts/subtitle_styles.py --list
python scripts/subtitle_styles.py 成片.srt -o 字幕.ass --style highlight --size 1080x1920 --font "Noto Sans SC" --highlights highlights.json
```

## 样式

| 样式 | 效果 | 适合 |
|---|---|---|
| `standard` | ![standard](../assets/subtitle-styles/standard.jpg) | 默认。白字、深色描边、淡阴影 |
| `highlight` | ![highlight](../assets/subtitle-styles/highlight.jpg) | 用户要“美化、重点强调”时的首选。粗白字加柔和阴影，每屏最多一个关键词变黄并放大 1.15 倍，出现时 0.12 秒淡入上浮 |
| `box` | ![box](../assets/subtitle-styles/box.jpg) | 背景很花、描边压不住时。半透明黑色底条 |
| `variety` | ![variety](../assets/subtitle-styles/variety.jpg) | 节奏快、偏娱乐的口播。大字、深蓝描边，关键词放大后弹回 |
| `minimal` | ![minimal](../assets/subtitle-styles/minimal.jpg) | 背景干净、偏知识类。字细一点，没有描边，只有柔和阴影 |
| `karaoke` | ![karaoke](../assets/subtitle-styles/karaoke.jpg) | 用户明确要“逐字变色”。需要逐字时间（`--words`），没有逐字时间就不用这个样式，不要平均分配时间冒充逐字 |

全片只用一种样式。字号按画面宽度算，位置用 `--bottom`（字幕底边在画面高度的比例，默认 0.78）；先抽帧量下巴位置再定，不挡脸、不进最下面约 18% 的按钮区。

## 字体

- 用户有品牌字体按用户的来；否则用清晰的黑体，例如 Noto Sans SC / 思源黑体（SIL OFL，可以随成片使用）。
- `--font` 填字体的族名，不是文件名。字体文件放进一个文件夹，用 `fontsdir` 指过去，烧之前先渲染一帧确认真的用上了这个字体（找不到时 libass 会悄悄换成别的字体）。
- 可变字体（文件名带 `VF`）默认字重常常是最细的一档。要粗体时，先用 fontTools 的 `instancer` 导出一份固定字重（比如 800），改一个不会和系统字体冲突的族名再用。

## 高亮（`highlight`、`variety`）

高亮写在一个 JSON 里，键是第几屏（从 1 开始），值是这一屏里要高亮的原文片段，必须一字不差：

```json
{"3": "一切 AI 化", "48": "200 块", "226": "100%"}
```

怎么挑：

- 每屏最多一个词或短语，相邻两屏不要都高亮。全片大约三到四成的屏有高亮；满屏黄字等于没有重点。
- 优先：产品和技术名（Claude、Codex、GitHub、上下文、提示词……）、确切的数字和价格、一句话里的结论词（“最重要的不是工具”）。
- 同一个词出现很多次时，只在前几次和最关键的几处高亮。
- 不高亮否定句里被否定的那半个词（“不准确”里只高亮“准确”会把意思说反）；要高亮就整个“不准确”。
- 短语太长、占了大半屏时，挑里面最核心的几个字高亮。
- 挑完的列表存成文件放在成片旁边，用户想改直接改 JSON 重出。

## 卡拉OK（`karaoke`）

`--words` 是每屏一组 `[字, 开始秒, 结束秒]`，时间是成片时间，来自剪辑时的那份逐字转写（换算方法见 [subtitles.md](subtitles.md#时间)）。每屏的字连起来必须和 SRT 里这一屏的文字一样。

## 自检

除了 [subtitles.md](subtitles.md#自检) 的清单，再看：

- 抽帧至少包括两三屏有高亮的：颜色对、放大后没出界、和正文在同一条基线上。
- 有动画的样式，抽一帧刚出现 0.05 秒左右的画面，确认淡入正常、没有残影。
- 脚本报“可能超宽”的屏按 subtitles.md 拆屏，不要缩字号硬塞。
- 烧完的成片和旧的字幕版不能逐字节相同；相同说明滤镜里换字幕文件那一步没生效。

## 参考

样式的种类参考了开源字幕工具的常见做法，例如 [ai-video-captions](https://github.com/nicolaigaina/ai-video-captions)（Karaoke、Hormozi 等预设）和 [PupCaps](https://github.com/hosuaby/PupCaps)（关键词高亮）。代码和参数是 CutDirector 自己写的，并用真实口播实测过。
