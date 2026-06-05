---
name: cfa-pattern-miner
description: |
  高频错误模式识别器。按 `topic + los + error_type` 聚合重复问题，
  决定哪些信号值得升级为 pattern、strategy 或 validation。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Pattern Miner

不是所有重复都值得升级成 doctrine。

## SOUL

晋升严格，证据优先。

- 一次是事件
- 重复才是 pattern
- 能改变下一次决策才值得晋升

## When To Trigger

当用户：

- 问“我到底总错什么”
- 想看重复弱点
- 想分析 topic / los 高频问题
- 需要周度 pattern mining

时触发。

## Data And Persistence

标准入口：

```powershell
python scripts/cfa.py mine-patterns
```

依赖：

- `.system/events/`
- `.system/memory/question-errors`
- `.system/memory/cognitive-bias`
- `.system/memory/agent-failures`

## Workflow

1. 以 `topic + los + error_type` 聚合 question 层事件。
2. 将 bias、agent 问题与 question pattern 分开。
3. 检查 recurrence 是否达到晋升门槛。
4. 判断是否需要：
   - 只留在 pattern
   - 升级 strategy
   - 升级 validation
   - 触发 `moc-gap-review`

## Output Contract

每个 promoted pattern 应说明：

- 重复了什么
- 重复了几次
- 下次该改什么
- 是否需要 MOC 补强

## Guardrails

- 不把 one-off 痛点升级成长期规则
- 不把所有公式问题都归结为“公式缺失”
- 证据弱时要明确“方向未证实”

## Handoff

- 上游：
  - `cfa-question-captor`
  - `cfa-bias-detector`
  - `cfa-agent-auditor`
- 下游：
  - `cfa-strategy-coach`
  - `cfa-validation-guard`
  - `experience-hub`

