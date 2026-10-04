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

## 第二轮：取舍落实到可测试行为

研究日期：2026-10-04。重新读取下列固定提交的 Skill / 规则 / 当前依赖说明，避免沿用旧搜索摘要。本轮没有安装或执行外部 Skill，没有复制代码、模板、素材或整段提示词。

| 固定来源 | 值得吸收 | 不采用或保持边界 |
| --- | --- | --- |
| [majia-chatcut-koubo](https://github.com/maojiebc/majia-chatcut-koubo/blob/40640162d47d9c1308785be526adc52309671c0a/SKILL.md) | 字幕、源转写与原声修改是不同对象；小批回读，版本变化让旧证据失效 | 不把其全部审批与内部状态搬给用户；沿用本项目已有授权范围，普通清理不强制走动画审批 |
| [i-hate-editing · Cutting](https://github.com/ranahaani/i-hate-editing/blob/6c662176671d76e12f747df049991881255292d4/rules/cutting.md) | 对改变的接缝作局部复核，查重复起句、残句和失效编号；重复未必是错误 | 不固定保留最后一遍，不靠整片 ASR 宣布干净，不用未支持的 J/L cut；[完整流程](https://github.com/ranahaani/i-hate-editing/blob/6c662176671d76e12f747df049991881255292d4/SKILL.md) 的外部音频增强、个人代理和固定视觉音效不作默认依赖 |
| [Vibetool talking-head-video](https://github.com/Vibetool/talking-head-video/blob/5b46d7924ac18a6e1d1aead9be7b7c27d235153c/SKILL.md) | 需要解释时才进入知识图形窗口，其他时间保留口播；已接受原声是视觉层的时间依据 | 不固定圆形左上 PiP，不把其保留整条原音轨的包装流程误认为粗剪引擎；位置、图形和退出按当前画面决定 |
| [zinan92 videocut · autocut](https://github.com/zinan92/videocut/blob/d0ac421b385736de854a8a38508ed233c5972809/capabilities/autocut/SKILL.md) | 失败起句、重说、句内重复和残句分别判断；执行与选择分开，留下源区间记录 | 不扩建第二套本地 ASR / 编码流水线；不能把静音 fallback 或规则命中当成语义清理成功 |
| [duyi-scripted-video-edit 当前说明](https://github.com/duyi2076/duyi-scripted-video-edit/blob/b9b631021403d717a813ec1dce283972c3ea37b4/README.md) | 将编辑决策与时间运算分开；逻辑测试、真实 ASR 与整片渲染分开报告 | CC BY-NC 4.0 禁止商业使用：仅研究原理，不移植代码、文档或素材；不照搬其 macOS 与外部 ASR 依赖，也不外推 4K 承诺 |

### 本轮落点

| 用户收益 | 本项目的实际实现或规则 | 验证边界 |
| --- | --- | --- |
| “这句话必须保留”不会在调快后消失 | [计划工具](speech-edit-plan.md) 增加 `protected_ranges`，检查完整保留、原顺序、无其他片段插入 | 计划测试覆盖成功与拒绝写报告的 CLI；区间需代理先从真实原声定位，不是自动识别所有限定词 |
| 剪点不会只被整片识别结果掩盖 | 工具生成剪后 `review_windows`，保留两侧源位置和当前版本；连续源分段不伪造切口 | 合成时间测试；尚未用真人音频验证短窗复转写或实际听感 |
| 小修改不破坏整条视频 | [语音规则](speech-editing.md) 要求受影响窗口重验，疑似重复先对照原声 | S21–S22 是待执行行为场景，不算真实通过案例 |
| 动画为解释服务 | [完整流程](talking-head-workflow.md) 按比较、步骤、数据选择讲解窗口，不改已接受原声 | S23 为待执行场景；既有动画证据不自动覆盖新素材或新变体 |

这次新增代码为原创，未把外部项目列为运行依赖。固定来源用于追溯设计，不表示已运行、已认证或获得作者背书。自动生成复核清单与真正听过清单中的音频必须分开记录。
