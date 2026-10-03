# 语音剪辑计划与剪后时间

`scripts/speech_edit_plan.py` 供代理内部使用。用户只描述剪辑需求，不填写这些字段。

工具检查已经选好的保留区间、来源、顺序与可信词边界，并把原片锚点映射到剪后时间。它不判断语义、不自动删口癖、不转写或编码视频，也不调用 ChatCut。

## 输入与适用范围

- `version: "0.1"`，`mode: "linear-1x"`，`revision` 为当前粗剪版本。
- `sources`：按默认拼接顺序列出素材的 `source_id` 与秒单位 `duration`；可附 `words`，每个词含 `word_id`、`text`、`start`、`end`。
- `keep`：按剪后播放顺序列出 `segment_id`、`source_id`、`start`、`end`。它们自动连续拼接，没有空 gap。
- `cuts`：可选的删减说明，含 `cut_id`、来源区间、`kind` 与 `reason`。类别为 filler / false_start / retake / redundancy / production_aside / silence。
- `allow_reorder` 默认 false。重组需要在授权范围内设 true 并记录 `reorder_reason`，工具中的开关本身不是用户授权证明。

同一素材保留区间不能重叠或复用；区间必须在源时长内，明确删减不能和保留内容重叠。仅支持声画同步的线性 1x 拼接。多机位、转场重叠、变速、音视频分离和重复使用素材必须回到宿主实际时间映射。

有可信词点时，保留和删减的边界不能落在词内。ASR 估计区间未经核实时，不应作为音频自然度证明；没有词点时报告 `word_boundaries_checked: false`。词边界验证只检查给定的数据，不能检查工具未收到的词。

## 使用

```sh
python scripts/speech_edit_plan.py tests/fixtures/speech/natural-cleanup.json
python scripts/speech_edit_plan.py tests/fixtures/speech/natural-cleanup.json --anchor camera-a 7.2 8.6
```

需要内部缓存时，用 `--output .talkdirector/<job>/speech-map.json`。输入计划可放同一忽略目录，运行时不写入公开 Recipe。

输出包含连续时间线、所有未保留源区间和粗剪版本。锚点返回所有保留交集；如果其原句已删除、被部分删除或跨切口拆分，`requires_reanchor` 为 true。不要只取第一个交集继续挂动画或字幕，需回读当前语句重新定位。

恢复或删改语音后，生成新 revision，从实际宿主读回当前源区间再计算。旧映射只作历史记录。字幕与视觉锚点使用最新 revision；时间算术通过不代表当前 ChatCut 时间线确实采用了这些区间。

## 验证范围

测试使用合成的已知源词点和编辑区间，检查断词、越界、重叠、重排、删除后的偏移、多素材与失效锚点。`media_verified` 始终 false：工具没有试听、看画面或执行剪辑。真实语音与最终导出需按 [口播流程](talking-head-workflow.md) 检查。
