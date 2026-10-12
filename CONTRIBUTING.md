# 参与贡献

CutDirector 只做一件事：把原始口播剪干净，再配上字幕。最有价值的贡献，是用真实素材跑一遍以后发现的问题。

## 提交什么

1. **实测反馈**：用一条真实口播按指南剪一遍，逐条记下指南哪里不清楚、难执行、判断错了或缺了规则，附具体时间点和原话。
2. **新规则或实例**：中文口播里常见、但指南还没覆盖的情况，例如新的重说模式、断句难点。写清"原文 → 判断 → 结果"。
3. **修正**：规则互相矛盾、数字不合理、表述含糊的地方。

不要提交无权分发的视频、音频或人物素材。引用其他项目的做法时，在对应指南末尾的参考表里写明来源。

## 在哪里修改

- 剪辑规则：`references/talking-head-cut.md`
- 重录与口误：`references/talking-head-retakes.md`
- 字幕：`references/talking-head-subtitles.md`
- 入口与硬规则：`SKILL.md`

指南只写"怎么做才对"，不绑定具体工具，也不要求用户安装软件或注册服务。

## 自查

```sh
python -m unittest discover -s tests
python scripts/check_local_links.py
```
