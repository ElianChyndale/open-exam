---
bucket: Quant
question_count: 5
---

# Quant Mock Mistakes

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: official_qbank
- source_type: screenshot
- wrong_choice_or_output: Selected A (Geometric mean return) and confused money-weighted return with time-weighted return / geometric mean.
- correct_resolution: For money-weighted return, build investor cash flows and solve IRR. Here the MWRR is about -2.22%, while TWRR is a separate measure and is positive at about 7.97%.
- evidence_refs: screenshot-session-2026-05-21
- evidence_assets: chat_image_1, chat_image_2
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: custom_drill
- source_type: typed
- wrong_choice_or_output: B. -10.32% (holding period return formula used instead of continuously compounded return)
- correct_resolution: r = ln(186.75/208.25) = ln(0.89676) = -0.10897 ≈ -10.90%. 连续复利收益率必须用 ln(P1/P0)，而非简单收益率 (P1-P0)/P0。
- evidence_refs: typed-q-2026-05-21-quant
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: custom_drill
- source_type: typed
- wrong_choice_or_output: B. the return earned by the manager prior to deduction of trading expenses.
- correct_resolution: C is correct. Gross return 已扣除交易费用（trading expenses 直接贡献于回报计算），但不含管理费/行政费。它是税前、非风险调整的，用于衡量经理投资能力。B 错在 gross return 实际已包含 trading expenses 的扣除（它们属于投资决策的一部分），而 A 错在 gross return 是税前且不调整风险。
- evidence_refs: typed-q-2026-05-21-quant-2
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: custom_drill
- source_type: typed
- wrong_choice_or_output: B. 3.98%. 错误路径：多减了 trading expenses 1.10%。即 (8.46%-1.10%-1.60%) 得 5.76% → 杠杆后 5.68% → 税后 3.98%
- correct_resolution: C. 5.00%。正确三步：(1) Net return = 8.46% - 1.60% = 6.86%（trading expenses已在gross return中，不重复减）(2) Leveraged return = 6.86% + (2500/7500)*(6.86%-6%) = 7.15% (3) After-tax = 7.15%*(1-0.30) = 5.00%
- evidence_refs: typed-q-2026-05-21-quant-3
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_screenshot
- error_type: concept_confusion
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: B. maturity premium
- correct_resolution: C. real risk-free interest rate. The real risk-free rate reflects the time preferences of individuals for current versus future real consumption.
- evidence_refs: chat-screenshot-2026-05-21-q38
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md