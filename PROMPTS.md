# CutDirector · 完整 Prompt

[返回首页](README.md) · [按用途选择](PROMPT-LIBRARY.md)

## 已验证效果

每个 Verified Prompt 都来自真实的 ChatCut 时间线：先完成、再验证，最后才公开为可复用 Prompt。

### Prompt 001 · 手势触发 Logo 弹出

[![Prompt 001 - 手势触发双侧官方 Logo 弹出](assets/verified-prompts/prompt-001-gesture-logo-pop.gif)](assets/verified-prompts/prompt-001-gesture-logo-pop.mp4)

**快速使用**

```text
当人物分别指向左右时，在左侧弹出 [品牌 A] 官方 Logo，右侧弹出 [品牌 B] 官方 Logo。先做这个片段给我看。
```

适合品牌对比、工具介绍和产品推荐。CutDirector 会在内部查找真实手势、验证官方素材、保护人物与字幕，并检查入场和退场。

<details>
<summary><strong>查看完整精确 Prompt</strong></summary>

```text
在 [时间段]，给人物两侧的指向手势添加 [品牌 A] 和 [品牌 B] 的官方 Logo 弹出特效：[品牌 A] 在画面左侧，[品牌 B] 在画面右侧，分别跟随对应手指抬起时弹出，手势结束时退场。请自动获取可验证的官方 Logo，保持人物全屏，不遮挡脸、字幕、手和产品，并先展示关键帧让我确认。
```

</details>

[查看 Prompt 001 的完整说明](references/prompt-001-gesture-logo-pop.md)

### Prompt 002 · 双栏讲解

[![Prompt 002 - 左侧要点逐条浮现，右侧长文本缓慢滚动](assets/verified-prompts/prompt-002-split-screen-explainer.gif)](assets/verified-prompts/prompt-002-split-screen-explainer.mp4)

**快速使用**

```text
把这段做成双栏讲解：左边按照口播依次出现重点，右边缓慢滚动完整资料。
```

适合 Prompt、代码、报告、合同和论文讲解。左侧负责结论，右侧只承担“完整材料正在流动”的证据作用。

<details>
<summary><strong>查看完整精确 Prompt</strong></summary>

```text
在 [时间段] 制作一段横屏双栏信息动效。左侧作为主视觉，显示标题「[标题]」，并让 [3-5 个要点] 按照叙述顺序逐条浮现：当前项高亮，历史项降低亮度保留，最后进入全部完成状态。右侧作为辅助信息区，放入 [完整长文本] 并让文字持续、匀速、缓慢地由下向上滚动。长文本不要求在视频结束前展示完，不要为了滚完全文而加快速度。右侧宽度不得超过画面的 45%，保持原视频时长和画幅，并先展示开始、中段和结束关键帧让我确认。
```

</details>

[观看 Prompt 002 演示视频](assets/verified-prompts/prompt-002-split-screen-explainer.mp4) · [查看完整说明](references/prompt-002-split-screen-explainer.md)

### Prompt 003 · 品牌双模式能力对比

[![Prompt 003 - 品牌图标贯穿普通模式与办公模式对比](assets/verified-prompts/prompt-003-brand-mode-comparison.gif)](assets/verified-prompts/prompt-003-brand-mode-comparison.mp4)

**快速使用**

```text
把这段做成品牌双模式对比：顶部保留官方图标，左边只放 [模式 A] 的一个核心能力，右边让 [模式 B] 的能力逐项落下，最后收束成「[能力 A] → [最终结果 B]」。使用纯黑背景和轻快卡点，图标不要单独淡出。
```

适合普通版与专业版、聊天模式与办公模式、免费版与付费版等双模式讲解。它用一个品牌图标维持身份连续性，以非对称信息量强调能力差异，并在结尾把多项功能压缩为一句结果。

<details>
<summary><strong>查看完整精确 Prompt</strong></summary>

```text
在 [时间段] 制作一段横屏全屏品牌双模式对比动效。

使用纯黑背景，顶部居中放置 [品牌] 的可验证官方图标。图标作为整段的品牌锚点，贯穿两个信息阶段，不要在中间转场时单独淡出或重新出现。

第一阶段并排展示两种模式：左侧标题「[模式 A]」，只保留一项核心能力「[能力 A]」；右侧标题「[模式 B]」，按照口播顺序依次出现 2-4 项能力。左侧使用中性灰弱化，右侧使用一个高亮强调色，不添加小号英文装饰。

第二阶段让第一阶段的标题和能力块一起退场，品牌图标保持稳定，然后把画面收束为「[能力 A] → [最终结果 B]」，下方补充一句「[总结句]」。音效使用轻、短、清脆的卡点，避免低沉 boom、机械拖尾和连续 whoosh。先展示第一阶段、能力递进、中间转场、最终结论和导出成片的实际第一帧让我确认；独立导出时，第一帧不得露出上一镜。
```

</details>

[观看 Prompt 003 演示视频](assets/verified-prompts/prompt-003-brand-mode-comparison.mp4) · [查看完整说明](references/prompt-003-brand-mode-comparison.md)

### Prompt 004 · 自适应章节导航与全片进度条

[![Prompt 004 - 根据视频结构自适应选择章节导航或全片进度](assets/verified-prompts/prompt-004-top-chapter-progress-rail.gif)](assets/verified-prompts/prompt-004-top-chapter-progress-rail.mp4)

**快速使用**

```text
分析这条视频的结构、画幅和安全区，自适应选择完整章节导航、当前章节、纯进度或保持干净。只要显示进度，就必须从头到尾连续运行，跨章节和镜头不清零。
```

它不预设日报、课程、访谈或任何固定题材，也不默认横屏、顶部位置或深色科技风。CutDirector 会根据真实章节、标签密度、横竖画幅、人物与 UI 安全区选择合适形态；没有可靠章节时不虚构章节，没有安全区或观看价值时保持干净。

<details>
<summary><strong>查看核心精确 Prompt</strong></summary>

```text
分析 [整条视频或确认时间段] 的实际内容、画幅、节奏和安全区，为它添加一条自适应的“章节或段落导航 + 全片进度”信息条。

先识别视频是否存在真实章节，再选择完整章节导航、当前章节模式、纯进度模式或保持干净。位置顶部优先但不固定，视觉语言继承原片，不套用固定题材、画幅、坐标或科技风。

只要显示进度，就从第一帧 0% 开始，按真实播放时间连续填充，到最后一帧达到 100%；跨章节和镜头绝不清零、回跳、提前跑满或重复入场。先提交结构、形态和安全区依据，再展示代表帧与实时预览让我确认。
```

</details>

[观看 Prompt 004 演示视频](assets/verified-prompts/prompt-004-top-chapter-progress-rail.mp4) · [查看完整说明](references/prompt-004-top-chapter-progress-rail.md)

### Prompt 005 · 斜向卡片滚动（真实源视频复用）

[![Prompt 005 - 斜向卡片滚动](assets/verified-prompts/prompt-005-diagonal-card-waterfall.gif)](assets/verified-prompts/prompt-005-diagonal-card-waterfall.mp4)

**快速使用**

```text
在 [目标时间段] 使用 page-waterfall-wall 斜向卡片滚动镜头。先检查目标网站、官方演示和当前 ChatCut 素材库；如果存在来源可验证的 `page-waterfall-wall.mp4`，直接导入原视频，不重新生成、重绘或用 Motion Graphic 复刻。

保留源视频的 1920×1080、30fps、约 5 秒时长、原始播放速度和完整画面，不添加标题、字幕、角标、品牌包装、粒子、故障或其他覆盖层。目标画幅不一致时只做最小必要适配，禁止拉伸、变速和无意义裁切。

如果没有可验证的源视频，就保持画面干净并请求源文件。只有用户明确同意，而且具备真实网站截图或真实录屏时，才允许先做一个代表镜头复刻；不得生成、重绘或虚构产品 UI。

先展示首帧、中段和尾帧，确认来源、画面完整、无覆盖、无裁切、无黑边后，以 H.264、1080p、30fps 导出。
```

**类型：真实源视频复用型。** 它适合网站合集、产品案例、作品集和界面功能的高密度视觉展示，但不是可编辑卡片模板。卡片文字、图片和运动已经存在于源视频中，用户不能通过 Prompt 005 替换；需要更换卡片内容时应使用另一条可编辑 Motion Graphic Prompt。

<details>
<summary><strong>查看核心精确 Prompt</strong></summary>

```text
在 [目标时间段] 使用 page-waterfall-wall 斜向卡片滚动镜头。

先检查目标网站、官方演示和当前 ChatCut 素材库。若已经存在网站提供或官方来源的 `page-waterfall-wall.mp4`，直接导入并使用原视频，不重新生成、重绘或用 Motion Graphic 复刻。

保留原素材的 1920×1080、30fps、约 5 秒时长、播放速度和完整画面，不添加大标题、字幕、角标、品牌包装、粒子、故障或其他覆盖层。只有在目标画幅不一致时才做最小必要适配，禁止拉伸和无意义裁切。

只有确认不存在可用的真实源视频，并且得到用户明确同意后，才可以用真实网站截图或真实录屏复刻；不得生成、重绘或虚构产品 UI。无法取得可靠素材时保持画面干净并请求源文件。

先展示首帧、中段和尾帧，确认来源、画面完整、无覆盖、无裁切、无黑边后，以 H.264、1080p、30fps 导出。
```

</details>

[观看 Prompt 005 演示视频](assets/verified-prompts/prompt-005-diagonal-card-waterfall.mp4) · [查看完整说明](references/prompt-005-diagonal-card-waterfall.md)

### Prompt 006 · 浅灰三卡翻面（正反面可编辑）

[![Prompt 006 - 原版浅灰三卡依次翻面，六个卡面均可编辑](assets/verified-prompts/prompt-006-editable-three-card-flip.gif)](assets/verified-prompts/prompt-006-editable-three-card-flip.mp4)

**快速使用**

```text
在 [目标时间段] 复刻原版浅灰三卡翻面镜头。使用 1920×1080、30fps、3 秒画布，在 #EDEDEB 浅灰背景上水平居中排列三张 414×230 白色卡片，保留左上角小标题、原版间距、轻阴影和从左到右的错峰节奏。

分别使用以下内容：
- 卡片 1 正面：[正面内容]；卡片 1 背面：[背面内容]
- 卡片 2 正面：[正面内容]；卡片 2 背面：[背面内容]
- 卡片 3 正面：[正面内容]；卡片 3 背面：[背面内容]

六个卡面必须独立可编辑。未填写的可选字段直接隐藏并自动回流，不得显示骨架线、空白图片区或占位内容；所有文字保留为 Motion Graphic 文字属性，不得烘焙进图片或视频。

三张卡分别从第 20、32、44 帧开始进行 16 帧的 Y 轴原地翻转，只在接近 90° 的最窄边缘态切换正反面。背面落稳后必须正向可读，禁止镜像、反字和闪回；第 60 帧全部完成并保持到结尾。

不要改变原版视觉，不添加深色背景、玻璃拟态、辉光、粒子、随机旋转或夸张弹跳。先检查正面稳定态、三次边缘态、三张背面和最终保持帧，再导出成片。
```

适合把三个功能、方案或案例依次揭示为三个结果。它保留已经验收的浅灰背景、三卡尺寸、间距和从左到右错峰节奏；演示里的文字和数字只是示例，用户可以分别替换六个卡面的文字、图片与强调色，未填写字段会隐藏并自动回流。

<details>
<summary><strong>查看核心精确 Prompt</strong></summary>

```text
在 [目标时间段] 制作一段原版浅灰三卡依次翻面镜头。保留三张横向并排的白色卡片、浅灰背景、左上角小标题，以及原版的卡片尺寸、间距、层级、透视和从左到右错峰节奏；固定三张卡片，不自动增减，也不要重新设计成深色、玻璃拟态或其他视觉风格。

三张卡片的正面和背面必须分别独立可编辑。请使用以下内容：
- 卡片 1 正面：[正面内容]；卡片 1 背面：[背面内容]
- 卡片 2 正面：[正面内容]；卡片 2 背面：[背面内容]
- 卡片 3 正面：[正面内容]；卡片 3 背面：[背面内容]

每个卡面可填写标题、副标题、分类、说明、指标和用户提供或项目中已验证的图片。未填写的可选字段直接隐藏并自动回流，禁止留下骨架线、灰色占位块、空白图片区或伪造内容；每个卡面至少保留一项真实、可读的内容。所有文案都保留为 Motion Graphic 可编辑文字图层，不得烘焙进 PNG、截图或视频。图片只使用用户提供或项目中已验证的真实素材，不生成、重绘或虚构产品 UI。

翻转使用 Y 轴原地翻面：先稳定展示三张正面，再让卡片 1、2、3 依次翻转。只有卡片接近 90°、画面最窄的边缘态时才能切换正反面；背面落稳后必须正向可读，禁止镜像字、反字或在翻转中途闪回另一面。独立演示默认使用 1920×1080、30fps、3 秒：正面保持到第 20 帧，三张卡分别从第 20、32、44 帧开始翻转，每张用 16 帧完成，全部背面在第 60 帧落稳并保持到结尾。目标时长不足时优先延长片段、精简卡面文案或依次完成翻转，不得靠过度加速牺牲可读性。

不添加辉光、粒子、玻璃拟态、随机旋转、夸张弹跳、大标题或无关装饰。先展示正面稳定态、至少一个 90° 边缘态、每张背面落稳后的状态和最终保持帧，并提供实时播放预览让我确认；导出前再次检查六个卡面的文字与图片都能独立修改。
```

</details>

[观看 Prompt 006 演示视频](assets/verified-prompts/prompt-006-editable-three-card-flip.mp4) · [查看完整说明](references/prompt-006-editable-three-card-flip.md)

### Prompt 007 · 高清页面输入标注与焦点锁定

[![Prompt 007 - 真实高清页面输入标注与焦点锁定](assets/verified-prompts/prompt-007-hd-page-focus-lock.gif)](assets/verified-prompts/prompt-007-hd-page-focus-lock.mp4)

**快速使用**

```text
在 [目标时间段] 制作 1920×1080、30fps、2.5 秒的“高清页面输入标注与焦点锁定”镜头。底层只使用用户提供或项目中已验证、分辨率不低于输出的 [真实页面截图/录屏]，按 1:1 或 contain 完整显示；禁止放大低清图、AI 重绘、虚构产品 UI、拉伸或无意义裁切。

上方添加透明 Motion Graphic 讲解层，把 [编辑标注]、[字段标签]、[输入文字]、[焦点标签]、颜色、遮罩强度、焦点框 X/Y/宽/高/圆角与标注面板位置全部开放为可编辑属性。可选标签留空后隐藏并回流；新增标签必须明确属于后期讲解，不能冒充网站原生 UI。

第 0–14 帧标注面板入场，第 8–34 帧逐字输入，第 14–30 帧压暗非重点区，第 20–38 帧锁定焦点框，第 28–42 帧显示焦点标签，第 42–74 帧稳定保持。焦点框准确贴合 [目标区域]，不遮挡正文，也不用过度模糊或大幅推拉代替聚焦。

先在 100% 尺度检查页面清晰度，再核对首帧、输入中段、遮罩、焦点框和最终保持帧，确认标注与原生 UI 边界明确后再导出。
```

适合演示搜索、筛选、定位功能和页面重点。真实页面负责事实证据，Motion Graphic 只负责可编辑的后期讲解；没有清晰真实素材时，Prompt 会请求原图或录屏，不会画一个“看起来像真的”网站。

[观看 Prompt 007 演示视频](assets/verified-prompts/prompt-007-hd-page-focus-lock.mp4) · [查看完整说明](references/prompt-007-hd-page-focus-lock.md)

### Prompt 008 · 真实图片卡组飞入与主卡落位

[![Prompt 008 - 真实图片卡组飞入、展开并抬升主卡](assets/verified-prompts/prompt-008-real-image-deck-hero.gif)](assets/verified-prompts/prompt-008-real-image-deck-hero.mp4)

**快速使用**

```text
在 [目标时间段] 制作 1920×1080、30fps、3 秒的“真实图片卡组飞入与主卡落位”镜头。提供 3–5 张用户或项目中来源可验证的真实图片，以及每张卡各自的 [标签]、[标题] 和 [主卡序号]。cardCount 必须等于真实图片数量，heroIndex 必须有效；禁止重复图片凑数、生成或重绘产品 UI、空白图片区、骨架线和占位词。

每张图片、标签、标题以及场景标签、背景色、卡片色、文字色、强调色和字体均独立可编辑。图片统一 contain 完整显示；可选标签为空时隐藏并回流。3、4、5 张卡分别使用约 430×318、355×276、292×242 的卡面。

每张卡从第 index×3 帧开始用 12 帧飞入，第 16–48 帧收束为稳定扇形，背景第 0–42 帧由深到浅，主卡第 30–52 帧抬升到约 1.12 倍，第 52–89 帧稳定保持。不要添加随机旋转、粒子、辉光、无关大标题或连续弹跳。

先逐张核对图片来源和标题，再检查首卡飞入、卡组收束、主卡抬升和最终保持帧；确认 contain 无裁切、主卡序号正确后再导出。
```

适合作品集、案例合集、网站功能和产品截图的高密度展示。复用的是卡组运动与主次层级，演示中的图片和文案不是固定内容。

[观看 Prompt 008 演示视频](assets/verified-prompts/prompt-008-real-image-deck-hero.mp4) · [查看完整说明](references/prompt-008-real-image-deck-hero.md)

### Prompt 009 · 输入—反馈—结果三拍因果链

[![Prompt 009 - 输入、反馈、结果三拍因果讲解](assets/verified-prompts/prompt-009-input-feedback-result.gif)](assets/verified-prompts/prompt-009-input-feedback-result.mp4)

**快速使用**

```text
在 [目标时间段] 制作 1920×1080、30fps、3.5 秒的“输入 → 反馈 → 结果”三拍因果镜头。填写 [输入文字]、[反馈短句]、[结果标题]，并可选填写场景标签、步骤标签、眉题、结果说明、元信息和 [真实结果图片]；文字、颜色、字体与图片全部独立可编辑。

所有文字保留为 Motion Graphic 属性，不得烘焙进图片或视频。可选字段留空后隐藏并回流；无结果图时使用单栏结果卡，只有图片来源可验证时才切换图文双栏并用 contain 完整显示。禁止生成或重绘产品 UI、假数据、空白图片区、骨架线和占位词。

第 5–28 帧逐字输入，第 28–48 帧输入卡压缩为反馈胶囊，第 35–58 帧显示反馈，第 52–74 帧结果卡进入，第 74–88 帧落稳，因果进度线第 0–96 帧连续推进，最终保持到第 104 帧。三拍必须清楚读成“动作发生—系统反馈—结果出现”；结尾不闪黑、不硬切、不把结果突然收回。

默认把它明确当作后期抽象讲解，不冒充真实产品原生 UI。若要证明真实产品操作，必须先使用用户提供或项目中已验证的录屏/截图作为底层证据，本 Prompt 只承担编辑标注。检查输入、反馈、结果和最终保持帧后再导出。
```

适合把“做了什么—系统如何响应—最终得到什么”压缩成一个清晰镜头。它既能独立做抽象解释，也能叠在真实产品证据上，但不会把演示 Motion Graphic 伪装成产品实录。

[观看 Prompt 009 演示视频](assets/verified-prompts/prompt-009-input-feedback-result.mp4) · [查看完整说明](references/prompt-009-input-feedback-result.md)

| Prompt | 观看任务 | 状态 |
| --- | --- | --- |
| **001** | 手势触发一个或多个官方品牌 Logo 弹出 | **已验证上线** |
| **002** | 左侧要点逐条浮现，右侧长文本缓慢滚动 | **已验证上线** |
| **003** | 品牌图标贯穿两种模式，能力递进后收束为结果对比 | **已验证上线** |
| **004** | 根据结构、画幅与安全区选择章节导航、当前章节、纯进度或保持干净 | **已验证上线** |
| **005** | 原样复用网站提供的 page-waterfall-wall 源视频；属于素材复用型，卡片内容不可替换 | **已验证上线** |
| **006** | 保留原版浅灰三卡构图与依次翻面节奏，六个卡面内容均可独立编辑 | **已验证上线** |
| **007** | 用真实高清页面承载事实，叠加可编辑输入标注、暗场和焦点锁定 | **已验证上线** |
| **008** | 3–5 张真实图片错峰飞入并收束为卡组，用户指定主卡抬升落位 | **已验证上线** |
| **009** | 输入、反馈、结果三拍形成可编辑因果链，可选使用已验证结果图片 | **已验证上线** |

后续案例只在真实时间线中完成并通过验证后，才会加入这个系列。

## 补充 Prompt 素材

以下两项由制作实践提炼，并提供独立重制的本地 Remotion 演示与可编辑源文件。**尚未进行 ChatCut 时间线验证，不计入上方 9 个 Verified Prompt。** 使用时按目标口播和安全区适配。

### Prompt 010 · 三段式数字片头

[![三段式数字片头](assets/prompt-examples/prompt-010-three-stage-count-hook.gif)](assets/prompt-examples/prompt-010-three-stage-count-hook.mp4)

```text
把 [目标时间段] 做成“发布消息 → 数量与内容 → 观众收益”的三段式片头。大字快速推入，准确数量短暂跳动后落稳，最后让收益句滑入。按口播切换，文字、数量、配色和时长可编辑。
```

[完整 Prompt 与替换说明](references/prompt-010-three-stage-count-hook.md) · [MP4 演示](assets/prompt-examples/prompt-010-three-stage-count-hook.mp4)

### Prompt 011 · 任务卡片推进看板

[![任务卡片推进看板](assets/prompt-examples/prompt-011-task-board-progression.gif)](assets/prompt-examples/prompt-011-task-board-progression.mp4)

```text
把 [流程主题] 做成三列任务看板。同一批任务卡片错峰从 [起始状态] 进入 [处理中状态]，停留后再进入 [完成状态]。完成时变色并打勾，保留卡片身份和文字；按实际状态展示，不编造完成结果。
```

[完整 Prompt 与替换说明](references/prompt-011-task-board-progression.md) · [MP4 演示](assets/prompt-examples/prompt-011-task-board-progression.mp4) · [两项示例源文件与导出方法](assets/prompt-examples/source/README.md)

