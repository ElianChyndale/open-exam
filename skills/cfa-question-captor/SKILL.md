---
name: cfa-question-captor
description: |
  题目证据标准化录入器。把错题、非独立作答、强提示完成、答案对但口径不清的题目，
  统一转换成可信的 `record-mistake` payload 与后续复盘资产。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Question Captor

把题目层证据变成结构化事件，而不是聊天里的模糊总结。

## SOUL

宁可不完整，也不脑补。

- 优先保留真实证据
- 优先让 payload 可持久化
- 优先把“哪里不确定”说清楚

## When To Trigger

当用户出现这些场景时触发：

- 真正做错了一道题
- 题没错，但不是独立完成
- 直接看了解析
- 靠强提示才做出来
- 想把题目证据录入本地系统

## Data And Persistence

应尽量补全这些字段：

- `source_layer`
- `topic`
- `los`
- `prompt_or_question`
- `wrong_choice_or_output`
- `correct_resolution`
- `error_type`
- `confidence`
- `time_spent`
- `evidence_refs`
- `question_source`
- `source_type`
- `evidence_assets`
- `moc_target`

持久化入口：

```powershell
python scripts/cfa.py record-mistake --payload "{...}"
```

## Workflow

1. 从用户输入中提取最小可信事实。
2. 判断这是不是 `question` 层，而不是 `bias` 或 `agent` 层。
3. 构造 `record-mistake` payload。
4. 标明来源和证据：
   - typed / screenshot
   - mock / qbank / custom drill
   - 是否为 `is_correct=true` 的高价值非错题证据
5. 如果题目暴露 MOC 缺口，保留 `moc_target` 与 gap 方向线索。
6. 通过 CLI 持久化，而不是只停留在聊天结论。

## Output Contract

输出必须给出：

- 结构化 payload
- 一条可执行 `fix_rule`
- 一条 `next_drill`
- 必要时说明哪些字段仍不确定

## Guardrails

- 不要凭空编 LOS
- 不要把不确定信息包装成确定结论
- 不要在证据不足时直接改 MOC
- 不要把题目层错误误升级成 strategy

## Handoff

- 上游：`cfa-intent-router`
- 常见下游：
  - `cfa-pattern-miner`
  - `cfa-review-synthesizer`
  - `cfa-strategy-coach`
  - `cfa-validation-guard`（当题目录入暴露 agent 风险时）

