<div align="center">

![CutDirector · Cut the noise. Keep the voice.](assets/brand-banner.svg)

# CutDirector

**把原始口播剪干净，再配上字幕。**

给 Codex、Claude Code 等智能体用的口播剪辑 Skill。它是一本剪辑手册：告诉智能体剪什么、留什么、在哪下刀、字幕怎么断，剪辑工具由智能体用它自己环境里现成的。

[开始使用](#开始使用) · [口播剪辑](references/talking-head-cut.md) · [重录与口误](references/talking-head-retakes.md) · [字幕](references/talking-head-subtitles.md) · [更新记录](CHANGELOG.md)

</div>

## 它做什么

| 处理 | 说明 |
|---|---|
| 去停顿 | 过长的停顿缩短到自然的长度，不剪光；节奏分紧凑、自然、舒缓三档 |
| 去语气词和口吃 | "嗯、呃"、"我我我"、"除非你是除非你是" |
| 去重录和口误 | 同一句说了好几遍只留最好的一遍；"三月……不对，四月"只留改正后的 |
| 配字幕 | 一屏一行，跟着剪辑后的时间走，放在人脸下方、平台按钮上方，同时给 SRT |

不做的事：特效、音乐、B-roll、调色，也不改说话人的原话。

## 一步到位

把视频交给智能体，直接拿到剪好、带字幕的成片。智能体自己做完所有判断，交付时只用几句话告诉你剪了什么、哪几处值得听一下：

> 剪好了：`成片_字幕版.mp4`，4:19 剪到 3:09，另附 `成片.srt`。
>
> 有两处你可以听一下：成片 1:05 那句你说了好几遍，我留了最后一遍；0:43 的"他"我按识别结果写的，如果指的是产品应该是"它"。
>
> 哪里不对直接说，比如"1:05 换成前一遍"，我改完重新出。

想先看删除清单再出片，跟它说"先给我看清单"就行。

## 不用装东西

Skill 只是指导，不附带程序，也不要求你安装模型或注册服务。智能体环境里能拿到逐字转写时，就剪口误、重录并配字幕；拿不到时只去停顿，并如实告诉你口误没处理。

## 开始使用

**1. 安装 Skill。** 在支持 Skill Installer 的 Codex 中发送：

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

也可以 clone 仓库，把整个目录复制到 `~/.codex/skills/cut-director`（Claude Code 放到 `~/.claude/skills/cut-director`），然后重启。

**2. 发一句话。**

```text
使用 $cut-director 把这条口播剪干净并配上字幕：<视频路径>
```

## 指南

| 文档 | 内容 |
|---|---|
| [口播剪辑](references/talking-head-cut.md) | 剪什么、留什么、节奏、下刀、自检、交付 |
| [重录与口误](references/talking-head-retakes.md) | 判断顺序、重说信号、风险分级、选哪一遍、10 个实例 |
| [字幕](references/talking-head-subtitles.md) | 时间换算、文字校对、中文断句、位置样式、自检 |

规则来自对 video-use、橙风剪口播、cut-video、FunClip、JJKoubo 等开源项目的学习，并用真实口播素材实测修订过，来源写在每份指南末尾。

## 开源与署名

| 内容 | 授权 |
| --- | --- |
| 脚本与测试 | [AGPL-3.0-or-later](LICENSES/AGPL-3.0-or-later.txt) |
| `SKILL.md` 与指南文档 | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt)：允许转载、改编和商用，但必须署名、标明修改，并以相同协议分享 |
| 用 CutDirector 剪出的成片 | 归你所有，不会因为使用本 Skill 而适用上述许可证 |
| CutDirector 名称与品牌 | 见[品牌政策](TRADEMARKS.md) |

转载或改编时请保留：

```text
CutDirector by Fangx-AI
https://github.com/Fangx-AI/cut-director
Licensed under CC BY-SA 4.0. Changes, if any, must be identified.
```

完整边界以 [`LICENSE`](LICENSE)、[`NOTICE`](NOTICE)、[`TRADEMARKS.md`](TRADEMARKS.md) 和 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) 为准。

## 参与贡献

最有用的贡献是实测反馈：用一条真实口播跑一遍，记下指南哪里不清楚、判断错了。详见[贡献指南](CONTRIBUTING.md)。

```sh
python -m unittest discover -s tests
python scripts/check_local_links.py
```
