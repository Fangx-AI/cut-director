# ChatCut 与演示兼容说明

[返回首页](../README.md) · [选择 Prompt](../PROMPT-LIBRARY.md)

文档与当前 Desktop 工具合同核对：2026-10-04。执行前仍以实际宿主提供的工具及 Skill 为准；文档检查不等于跨端剪辑已实测。

| 环境 | 使用方式 | 本项目的边界 |
|---|---|---|
| ChatCut 内置 Agent | 使用原生生成与时间线能力执行 Prompt | 自然语言 Prompt 可以作为任务输入；具体工具由内置 Agent 决定 |
| ChatCut Desktop ACP / local CLI | 当前官方 MG Skill 使用 inline JSX 创建素材，再放置到时间线 | 不能照搬标准 Remotion TSX；需按宿主 JSX 与属性合同适配 |
| Codex hosted ChatCut 插件 | 先读当前 plugin basics，再发现实际可用能力 | 不假设 Desktop 的工具必然存在，也不套用 Claude 的 Skill 名称 |
| 本地 Remotion | 用示例源文件渲染和修改 | 010–015 是这个范围的演示，不等于 ChatCut 时间线验证 |

## 媒体与项目边界

先区分 **ChatCut Desktop** 与 **Codex Browser 中的 ChatCut 网页**。有 Desktop 工具并不等于用户已经选择它；普通仓库开发、研究或文档测试不授权操作用户的桌面项目。用户明确选择 Desktop 或继续已建立的 Desktop 剪辑时，才按当前工具合同确认 active project，并核对它是否为这次目标。

当前 Desktop 工具声明：本地注册素材不会自动上传，网页与 hosted 插件可能只看到重新链接占位；网页已上传或生成的素材可由 Desktop 下载使用。项目结构能跨端同步，不代表媒体双向自动同步。进入目标端后先检查实际可播放素材，不用创建新内容掩盖缺失文件。

Desktop 的当前直接编辑合同要求通过工具执行，不向其聊天框投递提示词或驱动桌面 UI。发现工具目录不能作为授权或运行成功证据；工具调用还可能启动 Desktop，因此后台仓库检查不做无关探测调用。

官方[产品区别](https://chatcut.io/docs/chatcut-products)也将媒体所在位置作为环境选择依据。本文关于本地媒体方向和 Desktop 调用边界来自本次连接的工具声明，尚未另外执行跨端传输回归。

## 导出目标

网页与 hosted Agent Plugin 使用云端导出；Desktop 的本地视频渲染是另一条路径，官方文档列出 4K 与受硬件支持的 HDR。Desktop 发起的某些其他导出仍可能走云端，不能仅凭“来自客户端”判断全部导出行为。见[官方导出区别](https://chatcut.io/docs/web-export-limits)。

先检查本次端、源媒体、可用输出规格与真实导出文件；不能把放大的 1080p 素材质量描述为原生 4K，也不能用网页下载链接声称已在本地完成渲染。

<details>
<summary>版本核对快照，不是最低兼容版本承诺</summary>

2026-10-04：[Codex 插件 manifest](https://github.com/ChatCut-Inc/agent-plugin/blob/877b9177144feeecdef0da70f0e4d5cb760f6037/codex/.codex-plugin/plugin.json) 为 `1.10.15`；[公开版本页](https://chatcut.io/docs/releases)列出 Agent Plugin `1.10.12`、Desktop `0.4.21`。仓库和发布页不完全同步，分别记录，不由这些数值推断用户已安装的版本。

</details>

## MG 与图片

Desktop 直接编写 MG 时，遵守当前官方 Skill 的纯 JS JSX、注入组件、`Component({item})`、`item.props` 与属性声明要求。素材创建与时间线放置是两个步骤；在合成画面里检查才算完成视觉验证。

图片能力按当前环境发现。官方 Codex 包本次没有 `image-gen` Skill，而 Claude 包有；缺少同名 Skill 不代表必须停止所有图片任务，也不能编造调用。使用当前实际可用、符合任务范围的图片工具。

## 风格、声音与交付

- 优先沿用当前项目已应用的 Design Style，读取完整风格规则。普通素材继承风格；要求原样复刻时保留模板指定的视觉形式。
- 生成音乐只负责得到音频。精确落点、裁切、淡入淡出和旁白避让由后期完成；不能靠生成 Prompt 保证精确卡点。
- “可编辑”需说明对象：本地源代码、ChatCut MG 属性、字幕，或导出的其他软件工程。导出视频本身不是可编辑图层。
- 既有 Verified 状态保留其原验证范围，不自动扩展到新宿主、新画幅和新变体。

来源：[官方插件](https://github.com/ChatCut-Inc/agent-plugin) · [MG Skill](https://github.com/ChatCut-Inc/agent-plugin/blob/main/codex/skills/create-motion-graphics/SKILL.md) · [Design Styles](https://chatcut.io/docs/design-styles) · [音乐 Skill](https://github.com/ChatCut-Inc/agent-plugin/blob/main/codex/skills/music/SKILL.md) · [版本页](https://chatcut.io/docs/releases)
