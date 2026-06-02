---
card_id: card-bae4b0369be7
source_layer: question
topic: Quantitative Methods
los: QM.Rates and Returns
root_cause: concept_confusion
question_source: custom_drill
source_type: typed
moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md
fix_rule: 先写出考点定义，再用一句话说明为什么正确选项成立。
next_drill: 24 小时内重做 2 道 Quantitative Methods / QM.Rates and Returns 同类题。
review_due_at: 2026-05-24
linked_patterns: null
correct_resolution: C. 5.00%。正确三步：(1) Net return = 8.46% - 1.60% = 6.86%（trading expenses已在gross
  return中，不重复减）(2) Leveraged return = 6.86% + (2500/7500)*(6.86%-6%) = 7.15% (3) After-tax
  = 7.15%*(1-0.30) = 5.00%
review_status: Reviewed once
---

## Prompt
At the beginning of the year, an investor holds EUR10,000 in a hedge fund. The investor borrowed 25 percent of the purchase price, EUR2,500, at an annual interest rate of 6 percent and expects to pay a 30 percent tax on the return. Hedge fund: Gross return 8.46%, Trading expenses 1.10%, Managerial and administrative expenses 1.60%. Investor's after-tax return is closest to?

## Wrong Output
B. 3.98%. 错误路径：多减了 trading expenses 1.10%。即 (8.46%-1.10%-1.60%) 得 5.76% → 杠杆后 5.68% → 税后 3.98%

## Evidence
typed-q-2026-05-21-quant-3