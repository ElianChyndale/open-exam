---
name: cfa-note-annotator-workspace
description: |
  `cfa-note-annotator` 的评测与迭代工作区说明。用于查看 benchmark、对比 with_skill / without_skill 输出、
  复盘调优方向；不是用户日常学习技能。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Note Annotator Workspace

这是 skill 迭代工作区，不是 learner-facing skill。

## SOUL

用证据调优，不靠主观感觉。

- 看 benchmark
- 看 before / after
- 看真实失败模式

## When To Trigger

当需要：

- 调优 `cfa-note-annotator`
- 查看 benchmark 结果
- 比较 `with_skill` / `without_skill`
- 复盘 workspace 里的迭代证据

时触发。

## Data And Persistence

工作区主要文件：

- `iteration-1/benchmark.json`
- `iteration-1/benchmark.md`
- `iteration-1/review.html`
- 各 case 下的 `with_skill/` 与 `without_skill/`

## Workflow

1. 读取 benchmark 总结果。
2. 对比各案例的 with / without skill 输出。
3. 找出最稳定的增益点与最常见失败点。
4. 将调优意见反馈给 `cfa-note-annotator` 文档或评测说明。

## Output Contract

应产出：

- 这轮 skill 调优主要改进了什么
- 哪些失败模式还未解决
- 下一轮迭代应优先打哪里

## Guardrails

- 不把 workspace 当正式知识存储
- 不把 benchmark 结论写成用户学习结论
- 不把实验性结果冒充正式行为规范

## Handoff

- 上游：skill 调优请求
- 下游：
  - `cfa-note-annotator`
  - `codex-self-cycle`（当调优进入自治迭代时）

