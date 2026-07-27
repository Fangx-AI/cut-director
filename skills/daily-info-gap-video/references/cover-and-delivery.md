# Cover and delivery

## Fixed cover prompt framework

Keep the identity stable across days while varying the episode subject.

Prompt:

> 为中文短视频栏目“每日信息差”制作高记忆点科技新闻封面。深海军蓝到黑色背景，强烈橙红警报色与电光青点缀；左侧或中央放置一个具有固定栏目辨识度的橙色未来感“情报侦察球”机器人，单眼雷达镜头发出青色扫描光，电影级3D硬表面细节，强轮廓光，速度感与紧迫感。画面保留清晰的大标题安全区，主标题为“{HOOK}”，副标可为“今日速报”，角落显示日期“{DATE}”和栏目名“每日信息差”。围绕当天主题“{THEME}”加入一个明确但不杂乱的英雄视觉“{HERO_SUBJECT}”。中文排版巨大、粗壮、短促，缩略图尺寸仍清楚；不要小英文、不要密集参数、不要复杂信息图、不要水印、不要平台UI。商业科技媒体封面，强对比，高点击但不夸大事实。

Generate two independent compositions from the same identity:

- 4:3 landscape: hero visual and title can share left/right weight
- 3:4 portrait: stack hero and title vertically; keep the main title inside the central safe area

Do not merely crop one ratio into the other. Inspect both images for malformed Chinese text; if text quality is unreliable, generate the clean visual background and add exact text in the editor.

## Hook rules

- Keep the main cover hook short, ideally 6–12 Chinese characters
- Promise speed, consequence, surprise, or relevance
- Do not list every story
- Do not claim a fixed story count unless the episode actually contains it
- The recurring spoken opener may remain `90秒看完今日{主题}大事`; the cover hook can feature the strongest verified tension of the day

## Delivery folder

Use:

`{workspace}/{YYYY-MM-DD}/`

Recommended contents:

- `每日信息差_{YYYY-MM-DD}_4K.mp4`
- `每日信息差_{YYYY-MM-DD}_封面_4比3.png`
- `每日信息差_{YYYY-MM-DD}_封面_3比4.png`
- `投稿信息.md`
- optional `来源与素材清单.md`

For an AI preset, keeping the established `AI每日大事_...` filename prefix is acceptable.

## 投稿信息.md

Include:

- recommended title and two alternatives
- platform category
- tags
- concise description
- AI-generated-content declaration when applicable
- story list with primary source URLs
- material credits or license notes
- final video duration and resolution
- any uncertainty or manual checks still required

Prepare the upload package automatically. Stop before final publication unless the user explicitly authorizes that platform action.
