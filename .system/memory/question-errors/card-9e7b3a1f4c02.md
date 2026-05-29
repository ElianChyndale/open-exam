---
card_id: card-9e7b3a1f4c02
source_layer: question
topic: Economics
los: "M08: Exchange Rate Calculations — initial rate from appreciation percentage"
root_cause: formula_misuse
fix_rule: 汇率 = price currency / base currency。base currency 在分母，升值 8% 意味着分数值提高 8% → new = old × (1+r) → old = new / (1+r)。不要把 base 当成分子去乘。
next_drill: 24 小时内重做 2 道 Economics / M08 Exchange Rate Calculations 同类题。
review_due_at: 2026-05-28
linked_patterns: []
question_source: unknown
source_type: manual
evidence_assets: []
moc_target: CFA_tier1/Economics/00-Economics-MOC.md
correct_resolution: B. 1.3426. 1.4500 / X = 1.08 → X = 1.4500 / 1.08 = 1.3426. Base currency appreciation means the new rate = old rate × (1 + appreciation rate), so solve for old rate by dividing.
---

## Prompt

An exchange rate between two currencies has increased to 1.4500. If the base currency has appreciated by 8 percent against the price currency, the initial exchange rate between the two currencies was closest to:

A. 1.3340
B. 1.3426
C. 1.5660

## Wrong Output

C. 1.5660 — incorrectly multiplied: 1.45 × 1.08 = 1.566.

## Root Cause

**formula_misuse**: 混淆了 new_rate = old_rate × (1 + r) 中哪个是已知、哪个是未知。题干给 new_rate 和 r，求 old_rate，所以是除法而非乘法。

**Fix Rule**: 基础货币升值/贬值百分比公式：new_rate = old_rate × (1 + r)。解 old_rate 时用除法：old_rate = new_rate / (1 + r)。

## Correct Resolution

Base currency appreciated 8% → 1.4500 / X = 1.08 → X = 1.4500 / 1.08 = 1.3426.

## Linked Module

[[M08-Exchange-Rate-Calculations]] — combines with previous card (card-ccaaee560d08) on depreciation/appreciation asymmetry: this is the "solve for initial rate" variant.

## Related Card

[[card-ccaaee560d08]] — same M08 topic, different variant (depreciation → appreciation percentage vs solving for initial rate)
