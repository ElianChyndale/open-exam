---
name: cfa-question-captor
description: Turn a CFA question mistake into a structured MistakeEvent and MistakeCard. Use whenever the user reports a wrong answer, misread option, weak LOS, or wants to save a wrong question for later review.
---

# CFA Question Captor

Normalize question mistakes into:

- topic
- LOS
- wrong choice
- correct resolution
- error type
- confidence
- time spent
- evidence refs
- question source
- source type
- evidence assets
- moc target

Always produce one executable fix rule and one next drill.

## Formula-aware MOC targeting

When a mistake exposes a framework gap, preserve enough evidence to decide the right MOC destination instead of collapsing everything into “formula missing”.

- `knowledge_tree_core_formula`: the main formula is missing from the node's `核心公式`
- `formula_table_variant`: the node has the main formula, but the table misses a variant, conversion, or rearrangement
- `both`: the tree node and formula table both need reinforcement
- `knowledge_tree_concept`: the tree is missing a concept branch or distinction
- `exam_trap`: the issue is misuse or confusion, not missing formula storage

## Workflow

1. Extract the minimum trustworthy facts from the user's question or screenshot.
2. Decide whether this is really a `question` error rather than a `bias` or `agent` failure.
3. Normalize the mistake into a `record-mistake` payload.
4. Preserve provenance:
   - where the question came from
   - whether the evidence is a screenshot or typed note
   - which MOC should absorb future repeated gaps
   - whether the user is pointing to a missing core formula, variant formula, concept branch, or exam trap
5. Persist through the CLI rather than leaving the result as chat-only analysis.

## MOC Auto-Patch

每次完成错题录入后，必须执行 MOC 补缺检查：

1. 读取 `moc-gap-review` 产出（`.system/memory/strategy/moc-gap-review.md`）
2. 先验证公式是否真的属于目标知识树节点，再决定补哪里
3. 按 `gap_target` 选择补写位置：
   - `knowledge_tree_core_formula` -> 补知识树节点下的 `核心公式`
   - `formula_table_variant` -> 只补「核心公式速查」表
   - `both` -> 树和表一起补
   - `knowledge_tree_concept` -> 补知识树概念分支
   - `exam_trap` -> 补「高频考试陷阱速查」或节点警示行
4. 调用 `docs/moc-auto-patch-workflow.md` 参考流程执行

## 补写示例

- 主公式缺失 → 追加节点下 `核心公式`
- 变形公式缺失 → 追加公式表行：`| 指标 | 公式 | 知识树节点 | 考试说明 |`
- 概念混淆 → 追加陷阱表行：`| 错误理解 | 正确理解 |`
- 计算链缺失 → 新增知识树分支：`├── X.N 题目名【考试核心】← 高频错因`

## Discipline

- Do not invent a LOS if the evidence cannot support it.
- Do not hide uncertainty; record the best honest approximation.
- Prefer a slightly rough but truthful payload over a polished hallucination.
- Do not patch a formula into a node until formula ownership has been validated against the concept and the existing MOC structure.
