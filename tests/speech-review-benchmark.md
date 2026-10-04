# 中文语音决策对照：方案测试，不是成片比赛

2026-10-04。**本轮持平，没有得到 CutDirector 剪得更准的证据。**

## 怎么测的

- 两个独立代理、各运行一次，不继承此前聊天。使用父任务的同一默认模型配置；未固定或记录精确模型版本、随机种子，不做统计显著性结论。
- 基线只读宿主的官方 `talking-head-guide`。实验侧读同一指南及固定提交 `c02bbdc6bcffcf691e949d4eb66fdb63b3bf820b` 的 CutDirector Skill 与相关参考。不是直接运行 ChatCut 内部 Agent，也不是其他工具的产品对比。
- 两侧收到相同的请求、上下文、分好的文字单元和 JSON 输出格式；不提供答案、评分脚本、历史结果或此前聊天。没有媒体、ASR、剪辑、试听或导出能力。
- [样本与允许动作](fixtures/speech/review-cases.json) 在调用代理前固定为 Git blob `fa2b60371dba20cb5e3c1021bfe4fa14ae3c21be`，未按结果修改答案。输入包由脚本移除 `expected` 后提供。

8 个场景共 34 个单元：词内“额”与犹豫词、有意义连接词、最后一遍不完整的重录、改口数字与价格限定、覆盖型重复、讲解中引用“重来”、只改字幕不剪原声、保护句与必要停顿、不确定 ASR。

这不是完全盲测：代理知道自己读到的指南；文字已由维护者划分，部分上下文明确给出了语义边界。允许多种合理动作的单元并不都具有区分度。真实含糊语音会更难。

## 实际结果

| 项目 | 官方指南基线 | CutDirector |
| --- | --- | --- |
| 符合允许动作的单元 | 34 / 34 | 34 / 34 |
| 全部单元符合的场景 | 8 / 8 | 8 / 8 |
| 预定义严重错误 | 0 | 0 |
| 标为待复核的单元 | 3 | 3 |
| 媒体是否通过 | 否 | 否 |

两侧每个单元的动作一致，解释措辞不同。没有证据表明本轮存在净准确性提升，也不能把一次小样本的全部符合宣传成普遍准确率。

实际输出：[基线原始决策](records/speech-review-2026-10-04/baseline.json) · [CutDirector 原始决策](records/speech-review-2026-10-04/cutdirector.json)。文件仅规范化 JSON 排版，决策与理由没有重写；样本均为原创合成文字，不含用户素材。

## 复算与复跑

输出不含答案的输入包：

```sh
python scripts/evaluate_speech_review.py tests/fixtures/speech/review-cases.json --packet
```

复算这一次代理输出：

```sh
python scripts/evaluate_speech_review.py tests/fixtures/speech/review-cases.json --baseline tests/records/speech-review-2026-10-04/baseline.json --cutdirector tests/records/speech-review-2026-10-04/cutdirector.json
```

评分器要求案例与单元完整且唯一、动作合法、理由与下一步非空。它只评分 `keep / cut / shorten / review` 是否在预先允许的范围内，不评分理由好不好听。纯文字输入若声称 `audio_verified: true`，记严重错误；所有输出的 `media_verified` 均为 `false`。

单元测试中的构造答案用于验证评分代码，不是新的模型试验。重新调用代理须重新保存真实输出、指南版本和运行条件；增加更有区分度的场景时先固定输入与判定，再运行，不为制造优势事后改答案。

## 下一步验证什么

使用同一段有权使用的未剪中文原片、相同请求和工具，在独立项目副本中对照；公开素材另需许可。先记录未经人工修正的结果，再记录修复过程。

重点看：错选重录、误删限定、漏删失败起句、接缝听感、局部恢复、字幕/效果重锚、额外操作与确认次数、实际耗时及可播放导出。时间映射和保护区间的程序测试不能代替这些结果。

**本轮真人对照尚未完成。** CutDirector 当前可证明的是可检查的剪辑计划、保护范围和复核窗口，不是领先于官方语义判断或稳定的一键成片。
