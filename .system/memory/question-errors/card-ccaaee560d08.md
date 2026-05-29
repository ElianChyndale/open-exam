---
card_id: card-ccaaee560d08
source_layer: question
topic: Economics
los: "M08: Exchange Rate Calculations — exchange rate depreciation/appreciation asymmetry"
root_cause: formula_misuse
fix_rule: 汇率涨跌不对称：A 对 B 贬值 x%，不等于 B 对 A 升值 x%。升值比例 = 1/(1 - x) - 1。
next_drill: 24 小时内重做 2 道 Economics / M08 Exchange Rate Calculations 同类题。
review_due_at: 2026-05-28
linked_patterns: []
question_source: unknown
source_type: manual
evidence_assets: []
moc_target: CFA_tier1/Economics/00-Economics-MOC.md
correct_resolution: C. More than 12 percent. [1/(1 - 0.12)] - 1 = 1/0.88 - 1 = 0.1364 = 13.64%. GBP appreciated more than 12% because the base currency changes — depreciation and appreciation are not symmetric.
---

## Prompt

Over the past month, the Swiss franc (CHF) has depreciated 12 percent against the British pound (GBP). How much has the pound sterling appreciated against the Swiss franc?

A. 12 percent
B. Less than 12 percent
C. More than 12 percent

## Wrong Output

A. 12 percent — incorrectly assumed symmetric offset.

## Root Cause

**formula_misuse**: 误以为 A 对 B 贬值 x% 等价于 B 对 A 升值 x%。实际上，外汇涨跌是不对称的——因为分母（base currency）变了。

**Fix Rule**: 汇率涨跌不对称：A 对 B 贬值 x%，升值比例 = 1/(1 - x) - 1，一定大于 x%。

## Correct Resolution

CHF depreciated 12% against GBP → new rate = (1 - 0.12) = 0.88 of original.
GBP appreciation against CHF = 1/0.88 - 1 = 1.1364 - 1 = 0.1364 = 13.64% → more than 12%.

## Linked Module

[[M08-Exchange-Rate-Calculations]] in Economics — this is a direct application of exchange rate percentage change calculations.
