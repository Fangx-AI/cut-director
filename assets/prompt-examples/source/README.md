# 本地 Prompt 示例源文件

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
