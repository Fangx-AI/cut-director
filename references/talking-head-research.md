# 口播剪辑 Skill 研究记录

研究日期：2026-10-03。目标是将 CutDirector 从口播视觉增强扩展为已拍口播的剪辑工作流。下面记录读过的实际工作规则与取舍；项目 Star 和作者宣称不作为剪辑质量证明。

| 阅读来源 | 吸收的机制 | CutDirector 的取舍 |
| --- | --- | --- |
| [ChatCut 官方 talking-head-guide](https://github.com/ChatCut-Inc/agent-plugin/blob/877b9177144feeecdef0da70f0e4d5cb760f6037/codex/skills/talking-head-guide/SKILL.md) | Script 是语义剪辑入口，ASR 修正与剪音频分开；重录需要完整上下文；写后回读 | 遵循当前宿主合同；中文犹豫词先检查匹配方式，不把固定静音值当成全片自然度保证 |
| [cut-motion 的口播粗剪规则](https://github.com/Endless1936/cut-motion/blob/75b4fc10d2024e013761835e9635be31ff2d3a49/docs/talking-head-trim-standard.md) | 中文字符不能全局当口癖；语义、停顿、边界分开处理；先交付可听粗剪再规划画面 | 默认按表达质量选完整重录，最后一版不是硬规则；保留针对问题的试听，不规定所有视频必须相同帧率 |
| [ChatCut Video Editing Workflow](https://github.com/francoeur003/chatcut-video-editing-skill/blob/0d857477f261def79da62821aff0468b0780988e/chatcut-video-editing/references/workflow.md) | 多素材可编辑串联；工具写后重读；剪完再字幕、效果和导出 | 不照搬特定云端导入会话；使用当前宿主支持的导入、Script 与音频处理能力 |
| [本地 rough-cut Skill](https://github.com/vincentventalon/claude-code-video-editing-skill/blob/65b56dfad3e983c54cac9e85a50d920508f2b016/SKILL.md) | 用确定性工具处理物理切割，保留被选/被删尝试以便人工检查；自动规则后再读保留文稿 | 不仅靠静音岛或最后一遍自动选重录；不新增本地 ASR/编码器作为本次默认执行引擎 |
| [Premiere Agent](https://github.com/Kemerd/premiere-agent/blob/main/SKILL.md) | 节奏预设、词边界、声画一致的剪点以及可审阅编辑决策 | 采用用户可选节奏、词点保护；不采用强制删除每个超过阈值的停顿 |

上述来源作为技术与编辑方法研究。本次新增实现与文档为 CutDirector 原创，未复制外部代码、整段指令或素材。外部项目的工具、版本、授权和验证范围仍以各自仓库为准。

## 本次落实

- 主入口识别语音清理、精简、重组、字幕、声音、动画、导出与局部修改。
- 中文口癖、失败重复、强调、连接词与独有条件分别判断。
- 语音剪辑请求不再等待动画方案；预览与应用区分，既有授权继续有效。
- 剪后时间与原片时间分开；提供线性 1x 保留区间检查和锚点映射。
- 现有动画标签保持原验证范围；新增语音自然度需要真实口播试听，不能由逻辑测试证明。

后续最有用的验证是同一段真实中文毛片的前后对比：至少包含纯犹豫音、有意义的“然后”、数字修正、重复重录、刻意强调和章节停顿，记录误删、漏删、接缝与字幕/动画重锚表现。
