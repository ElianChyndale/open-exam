---
name: codex-self-cycle
description: |
  OpenExam 的自治迭代 orchestrator。用于 Codex 在本地依据证据自动选择下一条安全任务、
  执行、验证、记账并继续规划，不属于普通 CFA 学习技能。
metadata:
  version: OpenExam Skill Pack v1
---

# Codex Self-Cycle

这是系统维护与功能迭代 skill，不是 learner-facing CFA skill。

## SOUL

持续推进，但不失控。

- 先看本地事实
- 先选可验证任务
- 做完就记账，再继续
- 没有候选时宁可停，不 invent work

## When To Trigger

当用户要求这些时触发：

- “自己继续做”
- “不要停”
- “按 loop 自动推进”
- “继续实现计划，不等我确认”
- “自己修循环、自己找下一步”

## Data And Persistence

先读：

- `AGENTS.md`
- `.system/events/`
- `.system/memory/`
- `.system/memory/codex-loop/`
- `docs/codex_tasks/`

标准命令：

```powershell
python scripts/cfa.py codex-loop-plan --mode unattended
python scripts/cfa.py codex-loop-complete --candidate-id "<id>" --summary "<...>" --artifact "<path>" --verification "<...>"
```

## Workflow

1. 先读取本地 source of truth。
2. 生成下一条 loop 计划。
3. 打开 `ITER-xxx` 与 `TASK-xxx`。
4. 按 task safety limits 执行。
5. 跑验证。
6. 标记完成。
7. 立即再生成下一条计划。
8. 若无 eligible candidate，则停，不编造任务。

## Output Contract

完成记录必须明确：

- 做了什么
- 改了哪些 artifact
- 用什么验证
- 是否已生成下一条 plan

## Guardrails

- 不改 locked question-bank prompts / answers / explanations
- 不碰 secrets / destructive filesystem / remote refs
- 没有验证就不 claim complete
- 不把 ordinary learner requests 错当成 self-cycle request

## Handoff

- 上游：用户或系统级自治要求
- 下游：
  - `docs/codex_tasks/TASK-xxx.md`
  - 具体实现任务本身
  - 完成后再回到 `codex-loop-plan`

