---
name: cfa-review-pack-builder
description: |
  当日复习资料生成器。把到期错题、低信心事件、重复 pattern、MOC warm start
  组合成一份人类可直接学习的复习资料，而不是系统日志。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Review Pack Builder

复习包是给人学的，不是给代理看的。

## SOUL

可读、可回忆、可执行。

- 先决定今天该看什么
- 再把它排成好学的顺序
- 不把系统内部调度噪音暴露给学习者

## When To Trigger

当用户：

- 说“给我今天复习资料”
- 说“今天先复习什么”
- 想看 spaced review / warm start / readable question cards
- 想修 daily-review-pack 的质量

时触发。

## Data And Persistence

常用命令：

```powershell
python scripts/cfa.py record-progress --payload "{...}"
python scripts/cfa.py daily-review-pack --date YYYY-MM-DD --focus-topic "<topic>" --max-items 30 --knowledge-depth expanded
```

读取来源：

- `.system/events/`
- `.system/memory/`
- 活跃的 `CFA_tier1/*/00-*-MOC.md`

## Workflow

1. 先按 due / overdue 卡片挑选核心复习项。
2. 再加入 recurrence >= 3 的 pattern。
3. 再补 recent low-confidence items。
4. 如果有 focus topic，加入该 topic 的 MOC warm start。
5. 把输出排成：
   - `## 一、知识点和公式`
   - `## 二、错题`
6. 保持题目可读，不把 metadata 直接倾倒给用户。

## Output Contract

一份好的复习包必须：

- 可直接阅读
- 可追溯到本地证据
- 带 warm start
- 带 readable question cards

## Guardrails

- 不把 visible 内容写成 agent work log
- 不隐藏题干到长 metadata bullet 里
- 不在 options 缺失时发明选项
- 不在 focus topic 存在时完全不覆盖该 topic

## Handoff

- 上游：
  - `cfa-strategy-coach`
  - `cfa-pattern-miner`
- 下游：
  - `cfa-daily-todo-planner`
  - `experience-hub`

