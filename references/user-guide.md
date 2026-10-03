# 用 CutDirector 剪好第一条口播

[返回首页](../README.md) · [选择效果](../PROMPT-LIBRARY.md)

## 安装与更新

推荐在支持 Skill Installer 的 Codex 中发送：

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

执行剪辑还需要连接 ChatCut；安装本 Skill 不会自动安装、登录或购买 ChatCut。

**使用终端安装。** 已安装 Node.js 时，可以用 [skills CLI](https://github.com/vercel-labs/skills) 指定 Codex：

```sh
npx skills add Fangx-AI/cut-director --skill cut-director --agent codex --global
```

CLI 会显示目标和安装方式，确认后再安装。需要只装在当前项目时去掉 `--global`。其他支持 Skill 的助手可选择对应 `--agent`，但剪辑执行是否可用仍取决于它有没有 ChatCut 连接与所需工具。

**手动安装。** Clone 仓库，把整个目录复制到 `~/.codex/skills/cut-director`。不要只复制 SKILL.md：它需要 references、recipes 和 scripts。重启 Codex 后，用 `$cut-director` 调用。

<details>
<summary>Windows：使用目录连接，避免更新时重复复制</summary>

Windows 开发者可以创建 Junction，把已 clone 的仓库连接到 Skills 目录。目标已有同名目录时先检查，不直接覆盖个人修改。

```powershell
git clone https://github.com/Fangx-AI/cut-director.git
New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills"
New-Item -ItemType Junction -Path "$HOME\.codex\skills\cut-director" -Target (Resolve-Path .\cut-director)
```

更新时，先在仓库运行 `git status` 检查本地改动，再 `git pull --ff-only`。复制安装的用户需把更新后的目录同步到安装目录；Junction 会直接反映仓库文件。重启 Codex 重新加载。

</details>

CLI 安装的版本可用 `npx skills update cut-director --global` 更新；更新前保存个人修改。仓库包含演示媒体，首次下载会比纯文本 Skill 更大；安装完成不等于 ChatCut 已连接。

## 第一次只需要这些

提供目标 ChatCut 项目或已拍视频，再说清这次要做什么：剪语音、调整节奏、加字幕、配声音、加动画或完整剪辑。目标画幅或风格与当前项目不同时补充说明。可以先只给逐字稿做方案，但没有视频和音频无法实际剪辑或试听。

```text
使用 $cut-director 剪辑这条口播：去无意义口癖、失败重录和重复句，保留自然节奏。
再加清楚的字幕和适合内容的动画，沿用当前项目风格。
```

语音清理请求可直接在范围内执行并展示粗剪。要求只预览时先预览；新增动画风格先看代表片段，沿用已接受的方向继续。所有字幕、动画和音效以剪后时间为依据。已提供的信息和已确认的方向应延续使用。详见[完整流程](talking-head-workflow.md)。

## 怎样修改

| 反馈 | 助手应做什么 |
|---|---|
| “这句其实不用删” | 恢复对应原声，再更新受影响的字幕、动画和音效时间 |
| “去掉口癖，但别像机器一样” | 清理犹豫和失败重复，保留连接词、态度和必要气口 |
| “字更大，其他别动” | 保留内容、时序、风格，检查放大后的溢出与遮挡 |
| “每个案例后面都停太久” | 找出共享的退场或保持规则；区分动画空等与原声停顿 |
| “还是太单调” | 检查视觉任务是否重复；用比较、真实演示、累积等合适形式替换 |
| “这个风格可以，继续” | 记录已接受方向，在确认范围内复用，不重复问同一风格问题 |

只做动画时保留原声剪辑；完整剪辑可处理口癖、重录和空等。改变观点顺序、删独有信息或调整语速，需要属于你的这次要求。

## 常见问题

**找不到 Skill？** 检查目录内是否有 SKILL.md，安装目录是否正确，再重启 Codex。旧调用名 `$chatcut-talking-head-visual-director` 已改为 `$cut-director`；避免两个版本同时安装。

**只能给方案，不能执行？** 检查 ChatCut 是否已连接、项目是否可读，以及当前宿主有没有对应能力。参见[兼容说明](compatibility.md)。

**示例能直接改吗？** 010–015 提供[本地示例源代码](../assets/prompt-examples/source/README.md)。ChatCut 已验证素材按各页说明替换字段；005 是源视频复用，不是可换内容的卡片模板。

**有声示例哪里听？** 打开效果页的 MP4；动态 WebP 和 GIF 预览没有声音。012 的声音是原创节拍演示，不含旁白，因此不作为旁白避让已经验收的证据。

**能剪完整口播吗？** 可以按当前宿主能力从语音清理到字幕、声音、动画和导出；也可以只做其中一项。选题、未拍脚本创作、拍摄和发布由你的其他工作流负责。新增语音规则仍需要用真实素材试听验证，已验证动画不代表任意口播都已验收。

**可以商用吗？** 项目有代码、Prompt、品牌和第三方素材的不同授权边界，见[授权说明](../LICENSE)与[第三方声明](../THIRD_PARTY_NOTICES.md)。
