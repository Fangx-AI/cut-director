# 用 CutDirector 剪好第一条口播

[返回首页](../README.md) · [选择效果](../PROMPT-LIBRARY.md)

## 安装与更新

推荐在支持 Skill Installer 的 Codex 中发送：

```text
$skill-installer 安装 Fangx-AI/cut-director。
使用分支 codex/talking-head-editor 的仓库根目录。
技能目录命名 cut-director，不覆盖已有版本。
```

上面安装完整口播流程的预览分支，尚未合并到 `main`；真人素材回归仍待完成。执行剪辑还需要连接 ChatCut；安装本 Skill 不会自动安装、登录或购买 ChatCut。

### 主分支与其他安装方式

下面未指定分支的方式安装 `main`，不包含尚未合并的预览改动：

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
使用仓库根目录，技能命名 cut-director，不覆盖已有版本。
```

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

<a id="install-a-preview"></a>

### 指定版本与测试分支

未指定版本的 URL 和 CLI 命令安装 `main`。本轮完整语音流程在 [PR 19](https://github.com/Fangx-AI/cut-director/pull/19) 的 `codex/talking-head-editor` 分支中，尚未合并；不要把主分支安装当成本轮预览。

要体验本轮版本，在 Codex 中发送这一段：

```text
$skill-installer 安装 Fangx-AI/cut-director。
使用分支 codex/talking-head-editor 的仓库根目录。
技能目录命名 cut-director，不覆盖已有版本。
```

固定历史版本时，把分支名换成目标提交 SHA。已有同名安装时先保留个人修改；安装器拒绝覆盖不代表应直接删除原目录。

**已有旧版，想隔离试用？** 选一个独立测试项目，让安装助手把预览版放到该项目的 `.agents/skills/cut-director`，而不是任意下载目录或全局 Skills。然后在这个项目目录中开始 Codex 对话；下一轮若未出现，可重启 Codex。项目级扫描位置依据 [Codex 官方说明](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

同名 Skill 可能同时出现在选择器中，不要假定项目版本会覆盖全局旧版。先让助手确认本次读取的 `SKILL.md` 完整路径和安装来源版本；有歧义时明确提供测试项目中的 `SKILL.md` 路径。这里只确认指南已加载，不代表 ChatCut 或媒体已可用。

<details>
<summary>安装助手与维护者：根目录和带斜杠分支的参数</summary>

当前 Skill Installer 脚本应使用 `--repo Fangx-AI/cut-director`、`--ref codex/talking-head-editor`、`--path .`、`--name cut-director`。隔离使用时另加 `--dest <测试项目>/.agents/skills`；结果为其下的 `cut-director` 目录。在任意下载目录做文件测试，不等于 Codex 在当前项目已经发现这个 Skill。

不要只根据 `.../tree/codex/talking-head-editor` URL 猜 ref：当前安装器把 `tree` 后第一个路径段作为 ref，带斜杠分支应显式传 `--ref`。根目录 `.` 也需要明确 `--name`，不能把 `.` 当技能目录名。

本轮已通过官方 Skill Installer 的真实 GitHub 下载，在隔离目录安装测试分支；不表示用户的全局安装已更新。

</details>

## 第一次只需要这些

提供有权使用的已拍视频或目标 ChatCut 项目，说明在 Desktop 还是网页端工作；已有的信息不用再填一次。第一次建议只在独立测试副本剪一小段原声，先听是否自然，再继续全片。这里的 30 秒是试用建议，不是每个任务的硬性限制。

```text
使用 $cut-director，在独立测试副本中
先剪这条口播的开头 30 秒；不足 30 秒就用实际时长。
去无意义口癖、失败重录和重复句，压缩空等，保留原意与自然语气。
先只剪原声，不新增字幕、动画或生成素材。
给我可播放的粗剪，并说明重要删减和仍需核对的地方。
```

听关键接缝、数字与否定句，以及必要的停顿。可以直接反馈“这句别删”或“这里太急”，先局部恢复再继续，不需要整片重做。

认可粗剪后再说：

```text
这个原声节奏可以，按这个方向继续剩下的口播。
再加清楚的字幕和适合内容的动画，沿用当前风格。
新的视觉风格先给我看一个片段。
```

安装成功、ChatCut 已连接、文字方案和实际应用的剪辑，是四件不同的事。只有逐字稿时只能先做方案；静帧预览或字幕文字改正不代表原声已剪好。要求只预览时不要应用。所有字幕、动画和音效以剪后时间为依据。详见[完整流程](talking-head-workflow.md)。

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

**桌面端能播，网页只显示重新链接？** Desktop 注册的本地素材不会自动上传；同一项目在网页或 hosted 插件里可能缺少可播放媒体。不要反复剪辑或生成代替缺失文件，先确认这次在哪个端工作以及素材是否可用。见[媒体跨端说明](compatibility.md#媒体与项目边界)。

**示例能直接改吗？** 010–015 提供[本地示例源代码](../assets/prompt-examples/source/README.md)。ChatCut 已验证素材按各页说明替换字段；005 是源视频复用，不是可换内容的卡片模板。

**有声示例哪里听？** 打开效果页的 MP4；动态 WebP 和 GIF 预览没有声音。012 的声音是原创节拍演示，不含旁白，因此不作为旁白避让已经验收的证据。

**能剪完整口播吗？** 可以按当前宿主能力从语音清理到字幕、声音、动画和导出；也可以只做其中一项。选题、未拍脚本创作、拍摄和发布由你的其他工作流负责。新增语音规则仍需要用真实素材试听验证，已验证动画不代表任意口播都已验收。

**可以商用吗？** 项目有代码、Prompt、品牌和第三方素材的不同授权边界，见[授权说明](../LICENSE)与[第三方声明](../THIRD_PARTY_NOTICES.md)。
