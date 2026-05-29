---
name: cfa-daily-todo-planner
description: Convert the user's daily plan into a concise task-level today_todo.md and archive older todo files. Use this whenever the user mentions today's arrangement, todo list, daily tasks, schedule, what to do today, or asks to update today_todo.md.
---

# CFA Daily Todo Planner

Use this skill when the user tells you their day plan or asks to update `today_todo.md`.

The todo file is an execution surface, not a detailed study note. Keep it fast, readable, and task-level.

## Source And Destination

- Current active todo: `today_todo.md` at the repository root.
- Archive folder: `schedule/todo_archive/`.
- Standard CLI workflow: `python scripts/cfa.py write-todo --payload "{...}"`.

## Task Granularity

Write one checkbox per meaningful outcome.

Good:

- `完成 Corporate Issuers 主学习`
- `做 Corporate Issuers 练习题`
- `处理今天新增错题`
- `整理学习区和设备`

Too detailed:

- `检查椅子螺丝是否拧紧`
- `用自己的话复述关键概念`
- `把不熟的内容加入下一轮复习清单`
- `总结 3-5 个高频考点`

If a detail is merely how to do the task, fold it into the larger task or omit it.

## Structure

Use this shape:

```markdown
---
date: YYYY-MM-DD
focus: one-line focus
status: active
---

# 今日 Todo

> Focus: one-line focus

## Tasks
- [ ] task
- [ ] task

## Time Blocks
- morning: ...
- afternoon: ...

## Review
- 完成了什么：
- 卡住或调整：
- 明天保留：
```

`Time Blocks` are optional. Use them only when the user gives timing or asks for timing.

## Behavior

1. Read the existing `today_todo.md` before modifying it.
2. Archive the existing file through the workflow before writing the new one.
3. Convert the user's plan into 3-8 task-level checkboxes.
4. Keep review short. Do not create a long journal.
5. If the day includes CFA study, prefer task names that match the learning system: study, review pack, practice questions, record mistakes, mock/retro.

## Payload Pattern

```json
{
  "date": "YYYY-MM-DD",
  "title": "今日 Todo",
  "focus": "今天的主目标",
  "tasks": [
    "完成 Corporate Issuers 主学习",
    "做 Corporate Issuers 练习题",
    "处理今天新增错题"
  ],
  "time_blocks": [
    "上午：主学习",
    "下午：练习题和错题",
    "晚上：轻复盘"
  ]
}
```
