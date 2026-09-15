# 用 CutDirector 做出第一个镜头

[返回首页](../README.md) · [选择效果](../PROMPT-LIBRARY.md)

## 安装与更新

推荐在支持 Skill Installer 的 Codex 中发送：

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

也可以 clone 仓库，把整个目录复制到 `~/.codex/skills/cut-director`。不要只复制 SKILL.md：它需要 references、recipes 和 scripts。重启 Codex 后，用 `$cut-director` 调用。执行剪辑还需要连接 ChatCut；安装本 Skill 不会自动安装、登录或购买 ChatCut。

Windows 开发者可以创建 Junction，把已 clone 的仓库连接到 Skills 目录。目标已有同名目录时先检查，不直接覆盖个人修改。

```powershell
git clone https://github.com/Fangx-AI/cut-director.git
New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills"
New-Item -ItemType Junction -Path "$HOME\.codex\skills\cut-director" -Target (Resolve-Path .\cut-director)
```

更新时，先在仓库运行 `git status` 检查本地改动，再 `git pull --ff-only`。复制安装的用户需把更新后的目录同步到安装目录；Junction 会直接反映仓库文件。重启 Codex 重新加载。

## 第一次只需要这些

提供目标 ChatCut 项目或已拍视频，再说清想强化的句子。目标画幅或风格与当前项目不同时补充说明。可以先只给逐字稿做方案，但没有视频无法验证真实人物位置和时间。

```text
使用 $cut-director：在“这三个步骤”附近加入递进图形。
沿用原声和当前项目风格，目标 3:4，先看一个片段。
```

助手会说明视觉任务、所用素材和代表片段。确认方案后执行，检查真实合成画面，再决定是否扩展。已提供的信息和已确认的方向应延续使用。

## 怎样修改

| 反馈 | 助手应做什么 |
|---|---|
| “字更大，其他别动” | 保留内容、时序、风格，检查放大后的溢出与遮挡 |
| “每个案例后面都停太久” | 找出共享的退场或保持规则；区分动画空等与原声停顿 |
| “还是太单调” | 检查视觉任务是否重复；用比较、真实演示、累积等合适形式替换 |
| “这个风格可以，继续” | 记录已接受方向，在确认范围内复用，不重复问同一风格问题 |

如果要删原声停顿、调整语速或改观点顺序，请明确说明。原声清理与加视觉是不同操作。

## 常见问题

**找不到 Skill？** 检查目录内是否有 SKILL.md，安装目录是否正确，再重启 Codex。旧调用名 `$chatcut-talking-head-visual-director` 已改为 `$cut-director`；避免两个版本同时安装。

**只能给方案，不能执行？** 检查 ChatCut 是否已连接、项目是否可读，以及当前宿主有没有对应能力。参见[兼容说明](compatibility.md)。

**示例能直接改吗？** 010–015 提供[本地示例源代码](../assets/prompt-examples/source/README.md)。ChatCut 已验证素材按各页说明替换字段；005 是源视频复用，不是可换内容的卡片模板。

**有声示例哪里听？** 打开效果页的 MP4；GIF 没有声音。012 的声音是原创节拍演示，不含旁白，因此不作为旁白避让已经验收的证据。

**为什么没有生成一整条视频？** 当前项目负责已拍口播的视觉增强。完整选题、脚本、拍摄、发布不是本 Skill 的默认工作。

**可以商用吗？** 项目有代码、Prompt、品牌和第三方素材的不同授权边界，见[授权说明](../LICENSE)与[第三方声明](../THIRD_PARTY_NOTICES.md)。
