<div align="center">

![CutDirector](assets/brand-banner.svg)

# CutDirector

**把原始口播剪干净，再配上字幕。**

</div>

给 Codex、Claude Code 等智能体用的口播剪辑 Skill。把视频交给智能体，直接拿到剪好、带字幕的成片。

- 去掉过长停顿、"嗯呃"、口吃、重说和口误，同一句说了好几遍只留最好的一遍
- 配一行一行的字幕，同时给 SRT；想要美化可以说“字幕重点强调一下”，有 6 种样式可选
- 不加特效，不改你的原话
- 不用安装任何东西

## 安装

在 Codex 中发送：

```text
$skill-installer install https://github.com/Fangx-AI/cut-director
```

或者把整个仓库放到 `~/.codex/skills/cut-director`（Claude Code 是 `~/.claude/skills/cut-director`），然后重启。

## 使用

```text
使用 $cut-director 把这条口播剪干净并配上字幕：<视频路径>
```

剪完它会告诉你剪了多少、哪几处值得听一下。哪里不对直接说，比如"1:05 换成前一遍"。

## 字幕样式

默认是普通字幕。说“字幕美化一下”“重点强调”时，它会从下面几种里挑（详见 [references/subtitle-styles.md](references/subtitle-styles.md)），只改样式，不改字：

| `standard` 普通 | `highlight` 重点高亮 | `box` 半透明底条 |
|---|---|---|
| ![standard](assets/subtitle-styles/standard.jpg) | ![highlight](assets/subtitle-styles/highlight.jpg) | ![box](assets/subtitle-styles/box.jpg) |
| **`variety` 综艺大字** | **`minimal` 极简** | **`karaoke` 逐字变色** |
| ![variety](assets/subtitle-styles/variety.jpg) | ![minimal](assets/subtitle-styles/minimal.jpg) | ![karaoke](assets/subtitle-styles/karaoke.jpg) |

## 致谢

剪辑和字幕规则参考了 [video-use](https://github.com/browser-use/video-use)、[橙风剪口播](https://github.com/Agentchengfeng/chengfeng-videocut-skills)、[cut-video](https://github.com/louisedesadeleer/cut-video)、[FunClip](https://github.com/modelscope/FunClip)、[JJKoubo](https://github.com/darrenli6/JJKoubo) 的做法，并用真实口播实测修订。

## 许可

`SKILL.md` 和 `references/` 采用 [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt)，脚本采用 [AGPL-3.0-or-later](LICENSES/AGPL-3.0-or-later.txt)，详见 [LICENSE](LICENSE)。转载或改编请署名 CutDirector by Fangx-AI。用它剪出的成片归你所有。
