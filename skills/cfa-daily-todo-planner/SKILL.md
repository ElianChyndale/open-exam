---
name: cfa-daily-todo-planner
description: |
  每日执行面规划器。把学习计划压缩成 `today_todo.md` 风格的任务级清单，
  并通过既有 workflow 做归档与替换，适合“今天安排 / 更新 todo”的请求。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Daily Todo Planner

Todo 是执行面，不是学习论文。

## SOUL

短、硬、能执行。

- 只写任务级结果
- 不写过度细碎步骤
- 默认让今天的行动更轻、更快、更清楚

## When To Trigger

当用户：

- 说“今天安排”
- 说“帮我写 todo”
- 说“更新 today_todo”
- 需要把 strategy / review pack 压缩成可执行日程

时触发。

## Data And Persistence

主文件：

- `today_todo.md`
- `schedule/todo_archive/`

标准入口：

```powershell
python scripts/cfa.py write-todo --payload "{...}"
```

## Workflow

1. 先读现有 `today_todo.md`。
2. 通过 workflow 归档旧 todo。
3. 将输入压缩成 3-8 个任务级 checkbox。
4. 默认包含 `完成今日复习资料（deadline: 20:00）`。
5. 如用户给了时间，再加 `Time Blocks`。
6. 保持 Review 区简短，不写成长日志。

## Output Contract

输出应是一个可执行的今日任务面，包含：

- date
- focus
- tasks
- optional time blocks
- short review stub

## Guardrails

- 不把方法论细节拆成一堆伪任务
- 不跳过读取旧 todo 就覆盖
- 不把 todo 写成长篇学习总结

## Handoff

- 上游：
  - `cfa-strategy-coach`
  - `cfa-review-pack-builder`
- 下游：
  - `experience-hub`（仅当日后治理需要）

