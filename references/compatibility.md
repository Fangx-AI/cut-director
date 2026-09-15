# ChatCut 与演示兼容说明

[返回首页](../README.md) · [选择 Prompt](../PROMPT-LIBRARY.md)

最后核对：2026-09-15。执行前仍以当前宿主提供的工具及 Skill 为准。

| 环境 | 使用方式 | 本项目的边界 |
|---|---|---|
| ChatCut 内置 Agent | 使用原生生成与时间线能力执行 Prompt | 自然语言 Prompt 可以作为任务输入；具体工具由内置 Agent 决定 |
| ChatCut Desktop ACP / local CLI | 当前官方 MG Skill 使用 inline JSX 创建素材，再放置到时间线 | 不能照搬标准 Remotion TSX；需按宿主 JSX 与属性合同适配 |
| Codex hosted ChatCut 插件 | 先读当前 plugin basics，再发现实际可用能力 | 不假设 Desktop 的工具必然存在，也不套用 Claude 的 Skill 名称 |
| 本地 Remotion | 用示例源文件渲染和修改 | 010–015 是这个范围的演示，不等于 ChatCut 时间线验证 |

当前官方 Codex 插件 manifest 为 1.10.12；官方 releases 页面另列 Agent Plugin 0.2.25。两个来源口径不一致，分别记录，不用其中一个数字推断另一个环境已过期。

## MG 与图片

Desktop 直接编写 MG 时，遵守当前官方 Skill 的纯 JS JSX、注入组件、`Component({item})`、`item.props` 与属性声明要求。素材创建与时间线放置是两个步骤；在合成画面里检查才算完成视觉验证。

图片能力按当前环境发现。官方 Codex 包本次没有 `image-gen` Skill，而 Claude 包有；缺少同名 Skill 不代表必须停止所有图片任务，也不能编造调用。使用当前实际可用、符合任务范围的图片工具。

## 风格、声音与交付

- 优先沿用当前项目已应用的 Design Style，读取完整风格规则。普通素材继承风格；要求原样复刻时保留模板指定的视觉形式。
- 生成音乐只负责得到音频。精确落点、裁切、淡入淡出和旁白避让由后期完成；不能靠生成 Prompt 保证精确卡点。
- “可编辑”需说明对象：本地源代码、ChatCut MG 属性、字幕，或导出的其他软件工程。导出视频本身不是可编辑图层。
- 既有 Verified 状态保留其原验证范围，不自动扩展到新宿主、新画幅和新变体。

来源：[官方插件](https://github.com/ChatCut-Inc/agent-plugin) · [MG Skill](https://github.com/ChatCut-Inc/agent-plugin/blob/main/codex/skills/create-motion-graphics/SKILL.md) · [Design Styles](https://chatcut.io/docs/design-styles) · [音乐 Skill](https://github.com/ChatCut-Inc/agent-plugin/blob/main/codex/skills/music/SKILL.md) · [版本页](https://chatcut.io/docs/releases)
