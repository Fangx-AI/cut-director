# 本地 Prompt 示例源文件

[返回素材索引](../../../PROMPT-LIBRARY.md)

## 012–015 · 节奏与信息结构

`RhythmExamples.tsx` 提供 `Prompt012`、`Prompt013`、`Prompt014`、`Prompt015`，均为 1280×720、30fps、180 帧。图形与动画独立制作；014/015 是抽象结构示例，非产品录屏。

在 React 19.2.3、Remotion / @remotion/cli 4.0.521 项目中，将文件用作入口：

```sh
npx remotion render RhythmExamples.tsx Prompt012 prompt-012-silent.mp4 --codec=h264 --crf=21
python make_accent.py accent.wav
ffmpeg -i prompt-012-silent.mp4 -i accent.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -shortest prompt-012.mp4
npx remotion render RhythmExamples.tsx Prompt013 prompt-013.mp4 --codec=h264 --crf=21
npx remotion render RhythmExamples.tsx Prompt014 prompt-014.mp4 --codec=h264 --crf=21
npx remotion render RhythmExamples.tsx Prompt015 prompt-015.mp4 --codec=h264 --crf=21
```

`make_accent.py` 只使用 Python 标准库，以固定随机种子合成原创 120 BPM 节拍，不需要下载音乐。012 无旁白，不能据此宣称旁白避让已试听验证。013–015 发布预览移除静音音轨；如渲染器自动附带静音轨，可用 `ffmpeg -i input.mp4 -c:v copy -an output.mp4` 移除。

颜色、字体和角标可用 CLI `--props` 修改；短句与形状在源码中修改。其他内容长度、数量、画幅和 fps 需要调整构图与时间。此示例不保证直接在 ChatCut 执行，见[兼容说明](../../../references/compatibility.md)。

## 010–011 · 片头与看板

`PromptExamples.tsx` 同时提供两个独立 Composition：`Prompt010`、`Prompt011`。内容为独立重制的通用示例，不含客户视频、第三方案例录屏、人物素材或配乐。

- 已使用 React 19.2.3、Remotion / @remotion/cli 4.0.521 导出。
- 1280×720、30fps、180 帧、6 秒，无音轨。
- 在已有相同版本的 Remotion 项目中运行，无需改动本仓库维护依赖。
- 将 `PromptExamples.tsx` 复制到该项目中，作为入口文件直接运行：

```sh
npx remotion render PromptExamples.tsx Prompt010 prompt-010.mp4 --codec=h264 --crf=20
npx remotion render PromptExamples.tsx Prompt011 prompt-011.mp4 --codec=h264 --crf=20
```

浏览器无法自动下载时，可增加 `--browser-executable` 指向本机 Chrome。示例优先使用 Microsoft YaHei，其他系统需要提供合适的中文字体，并通过 `fontFamily` prop 指定；字体未随仓库分发。

通过组件的 `defaultProps` 或 Remotion CLI `--props` JSON 文件修改文案、颜色和字体。数量可通过 `count` 修改；看板示例的 `columns` 与 `tasks` 均为三个元素。代码中的时间按 Composition 总帧数缩放，但改变时长仍需检查可读性。

源示例画布为 16:9。其他比例当前仅等比缩放留边，不自动重排；竖版需自行调整构图。源文件可编辑不代表 ChatCut MG 属性已验证。提示词中的可选录屏、不同任务数和未完成状态等扩展需要在目标环境实现与检查。

## 素材范围

源代码依仓库 AGPL-3.0-or-later 规则发布；原创 Prompt 与说明依 CC BY-SA 4.0 规则发布。MP4/GIF 为本项目新绘制的文字与几何动效示例，无第三方素材，按 CC BY-SA 4.0 提供。署名：CutDirector by Fangx-AI，https://github.com/Fangx-AI/cut-director 。
