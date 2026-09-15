# 找到适合这一句的 Prompt

[返回首页](README.md) · [001–011 完整展示](PROMPTS.md) · [官方效果参考](VISUAL-GALLERY.md)

先选你要帮助观众理解什么，再选动画。点开效果页，复制 Prompt，替换方括号中的内容即可。

**先试这些：** 品牌指向用 001；页面看不清用 007；开头缺重点用 010；音乐和画面脱节用 012；每句都重新起停用 013；成果差异不明显用 014；多个演示衔接松散用 015。

| 编号 | 想实现的效果 | 观看任务 | 准备什么 | 验证范围 |
|---|---|---|---|---|
| 001 | [手势触发 Logo](references/prompt-001-gesture-logo-pop.md) | 认出品牌 | 官方 Logo + 真实手势 | ChatCut 已验证 |
| 002 | [分屏要点与长文](references/prompt-002-split-screen-explainer.md) | 解释观点 | 逐字文案 | ChatCut 已验证 |
| 003 | [品牌能力递进](references/prompt-003-brand-mode-comparison.md) | 解释变化 | 官方 Logo + 两种模式 | ChatCut 已验证 |
| 004 | [自适应章节导航](references/prompt-004-top-chapter-progress-rail.md) | 连接段落 | 全片结构与时间 | ChatCut 已验证 |
| 005 | [原素材瀑布墙](references/prompt-005-diagonal-card-waterfall.md) | 展示广度 | 指定源视频，不可换卡片内容 | ChatCut 已验证 |
| 006 | [三卡翻面](references/prompt-006-editable-three-card-flip.md) | 解释变化 | 三组正反面内容 | ChatCut 已验证 |
| 007 | [真实页面焦点锁定](references/prompt-007-hd-page-focus-lock.md) | 证明结果 | 高清截图或录屏 | ChatCut 已验证 |
| 008 | [图片卡组与主卡](references/prompt-008-real-image-deck-hero.md) | 展示选择 | 3–5 张真实图片 | ChatCut 已验证 |
| 009 | [输入、反馈、结果](references/prompt-009-input-feedback-result.md) | 解释因果 | 三拍文案，可选结果图 | ChatCut 已验证 |
| 010 | [三段式数字片头](references/prompt-010-three-stage-count-hook.md) | 抓住注意 | 消息、数量、观众收益 | 本地演示 |
| 011 | [任务推进看板](references/prompt-011-task-board-progression.md) | 解释流程 | 真实任务状态 | 本地演示 |
| 012 | [语义重音与音乐落点](references/prompt-012-semantic-audio-accent.md) | 抓住注意 | 已有音乐 + 强调词 | 本地演示 |
| 013 | [短句累积与兑现](references/prompt-013-incremental-payoff.md) | 解释递进 | 2–4 条短句 + 结论 | 本地演示 |
| 014 | [同构图前后对比](references/prompt-014-matched-before-after.md) | 证明结果 | 同一对象前后素材 | 本地演示 |
| 015 | [真实演示连续接力](references/prompt-015-demo-relay.md) | 连接段落 | 真实演示片段与语义锚点 | 本地演示 |

## 怎样理解验证状态

- **ChatCut 已验证**：001–009 有仓库已有的真实时间线演示。具体效果、素材和默认画幅以各页为准，不表示所有版本和变体都已验证。
- **本地演示**：010–015 有可复现的本地 Remotion 预览；不等于 ChatCut 原生 MG 或属性面板已验证。014、015 使用原创抽象示例，展示剪辑结构，不冒充真实产品实录。
- **官方参考**：外部目录的结构参考，独立于以上两类；收录不等于本项目完成验证。

## 选画幅与声音

先告诉助手目标画幅。006/008 的竖版、4:3 适配和 007 的跟随焦点属于[可选变体](references/prompt-variants.md)，需要在目标画面验证。固定构图的原样复刻不会自动变成多比例模板。

012 的 MP4 带原创节拍，其他新增示例默认无声。听感看 MP4，GIF 只说明画面。原声已经完成时，加入动效不等于授权重新剪辑或变速。

## 一句话组合使用

```text
使用 $cut-director：开头参考 010；解释三个原因时参考 013；结果用 014 的前后对比。沿用当前风格和原声，先给我看最有代表性的一个片段。
```

只有确实需要时才组合多种效果；同一句通常选一个清楚的视觉任务就够了。
