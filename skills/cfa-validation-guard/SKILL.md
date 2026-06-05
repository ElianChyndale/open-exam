---
name: cfa-validation-guard
description: |
  校验规则治理器。把重复的 agent 风险、错误补丁路径、无证据高层结论，
  变成可执行的 validation rule 和 pre-output checklist。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Validation Guard

与其重复犯同类错，不如把它变成规则。

## SOUL

具体、可执行、能拦截。

- trigger 必须具体
- check step 必须能跑
- failure message 必须给出安全修正

## When To Trigger

当出现这些情况时触发：

- agent 错误可能再次误导输出
- MOC patch 需要先验校验
- 同类根因遗漏已经重复
- 需要在生成前加检查，而不是事后道歉

## Data And Persistence

目标资产：

- `.system/memory/validation/`
- 对应 agent / pattern / strategy evidence

常见上游：

- `cfa-agent-auditor`
- `cfa-pattern-miner`

## Workflow

1. 确认当前问题值得规则化，而不是只值得解释一次。
2. 写出：
   - trigger
   - check steps
   - failure message
3. 如果涉及 MOC patch，先校验：
   - formula ownership
   - patch target
   - gap_target 分类
4. 将规则保存为长期防错资产。

## Output Contract

每条 validation rule 必须包含：

- trigger
- executable check steps
- safe correction / failure message

## Guardrails

- 不写“看情况判断”式伪规则
- 不跳过 patch target 与公式归属判断
- 不把 validation 当重复总结

## Handoff

- 上游：
  - `cfa-agent-auditor`
  - `cfa-pattern-miner`
- 下游：
  - `experience-hub`
  - 相关执行 skill（在输出前遵守该规则）

