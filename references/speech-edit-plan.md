# 语音剪辑计划与剪后时间

`scripts/speech_edit_plan.py` 供代理内部使用。用户只描述剪辑需求，不填写这些字段。

工具检查已经选好的保留区间、来源、顺序、保护区间与可信词边界，把原片锚点映射到剪后时间，并定位要复核的剪点。它不判断语义、不自动删口癖、不转写或编码视频，也不调用 ChatCut。

## 输入与适用范围

- `version: "0.1"`，`mode: "linear-1x"`，`revision` 为当前粗剪版本。
- `sources`：按默认拼接顺序列出素材的 `source_id` 与秒单位 `duration`；可附 `words`，每个词含 `word_id`、`text`、`start`、`end`。
- `keep`：按剪后播放顺序列出 `segment_id`、`source_id`、`start`、`end`。它们自动连续拼接，没有空 gap。
- `cuts`：可选的删减说明，含 `cut_id`、来源区间、`kind` 与 `reason`。类别为 filler / false_start / retake / redundancy / production_aside / silence。
- `protected_ranges`：可选，含 `protection_id`、`source_id`、`start`、`end`、`reason`。代理把用户明确要求保留的原句或停顿解析为源区间；工具拒绝漏留、倒序和在区间内部插入其他片段。相邻且连续的多个 `keep` 可以组成同一个保护单元。这个字段不是自动语义识别，也不能代替确认是哪一版重录。
- `allow_reorder` 默认 false。重组需要在授权范围内设 true 并记录 `reorder_reason`，工具中的开关本身不是用户授权证明。

同一素材保留区间不能重叠或复用；区间必须在源时长内，明确删减不能和保留内容重叠。仅支持声画同步的线性 1x 拼接。多机位、转场重叠、变速、音视频分离和重复使用素材必须回到宿主实际时间映射。

有可信词点时，保留和删减的边界不能落在词内。ASR 估计区间未经核实时，不应作为音频自然度证明；没有词点时报告 `word_boundaries_checked: false`。词边界验证只检查给定的数据，不能检查工具未收到的词。

## 使用

```sh
python scripts/speech_edit_plan.py tests/fixtures/speech/natural-cleanup.json
python scripts/speech_edit_plan.py tests/fixtures/speech/natural-cleanup.json --anchor camera-a 7.2 8.6
python scripts/speech_edit_plan.py tests/fixtures/speech/natural-cleanup.json --review-context 1.5
```

需要内部缓存时，用 `--output .talkdirector/<job>/speech-map.json`。输入计划可放同一忽略目录，运行时不写入公开 Recipe。

输出包含连续时间线、所有未保留源区间和粗剪版本。锚点返回所有保留交集；如果其原句已删除、被部分删除或跨切口拆分，`requires_reanchor` 为 true。不要只取第一个交集继续挂动画或字幕，需回读当前语句重新定位。

恢复或删改语音后，生成新 revision，从实际宿主读回当前源区间再计算。旧映射只作历史记录。字幕与视觉锚点使用最新 revision；时间算术通过不代表当前 ChatCut 时间线确实采用了这些区间。

## 复核窗口

`review_windows` 标记源区间不连续的相邻片段、不同源文件的交接，以及裁剪/跳过素材后的首尾。来自同一素材的连续区间只是工程分段，不产生虚假剪点。每条含当前 `revision`、类型、剪后 `check_at`、剪后窗口起止和两侧源位置。

默认在剪点两侧各取最多 1.5 秒，首尾受成片时长约束；代理可用 `--review-context` 按问题调整。窗口不决定停顿该剪多短，也不是 ASR 调用。密集剪点的窗口可能重叠，但不合成一个整片窗口，避免丢掉每个待查接缝；很短的成片仍可能被单个窗口覆盖。整片首尾检查不因没有裁剪窗口而省略。

在实际剪后媒体中播放这些窗口，查断字、重复起句、残句、自然气口和口型。需要时扩到完整句。复转写只作线索，不能自动判定刻意重复为错误。保留与实际版本绑定的试听结果；重新剪辑或恢复后重新生成窗口。`media_verified` 仍为 false，不能把清单当成试听证据。

## 验证范围

测试使用合成的已知源词点和编辑区间，检查断词、越界、重叠、重排、删除后的偏移、多素材、失效锚点、保护单元完整性与复核窗口。`media_verified` 始终 false：工具没有试听、看画面或执行剪辑。真实语音与最终导出需按 [口播流程](talking-head-workflow.md) 检查。
