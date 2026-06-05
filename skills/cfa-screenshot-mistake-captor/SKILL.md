---
name: cfa-screenshot-mistake-captor
description: |
  截图题目证据录入器。把模考、练习包、QBank 截图先保留为原始证据，再转换成结构化题目事件；
  适用于“用户发截图，希望进入错题系统”的场景。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Screenshot Mistake Captor

截图先是证据，之后才是数据。

## SOUL

原始证据优先。

- 先保住截图身份
- 再做保守提取
- 看不清就留空，不硬猜

## When To Trigger

当用户：

- 发来错题截图
- 发来模考截图
- 发来题库页面截图
- 希望“把这张题图录进去”

时触发。

## Data And Persistence

需要尽量产出：

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
- `source_type=screenshot`
- `evidence_assets`
- `moc_target`

持久化路径：

- 截图 draft / capture artifact
- 后续 `record-mistake`

## Workflow

1. 把截图视为原始证据，不预设其字段已经干净。
2. 保留截图路径或 identity 到 `evidence_assets`。
3. 提取可见且可信的题目信息。
4. 对以下信息保守处理：
   - LOS
   - 题源
   - 正确答案
   - subject / MOC path
5. 如能构造可信 payload，则路由到 `record-mistake`。
6. 如仍不完整，则先保留 draft / handoff artifact，等后续补全。

## Output Contract

输出至少包含：

- 截图证据标识
- 结构化 payload 或 draft
- 明确的不确定字段列表

## Guardrails

- 不要因为截图模糊就脑补 LOS、题源、正确结论
- 不要丢失原始截图身份
- 不要把截图录入说成“已完全提取”，除非真的持久化了 draft 或 event

## Handoff

- 上游：`cfa-intent-router`
- 常见下游：
  - `cfa-question-captor`
  - `cfa-pattern-miner`
  - `cfa-review-synthesizer`

