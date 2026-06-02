---
bucket: FRA
question_count: 4
---

# FRA Mock Mistakes

## Financial Statement Analysis | FSA.Diluted EPS calculation using if-converted and treasury stock methods (approximate LOS from screenshot)
- error_type: formula_misuse
- question_source: unknown_screenshot_source
- source_type: screenshot
- wrong_choice_or_output: Selected C. $7.19, which includes both the convertible bonds and options in diluted EPS.
- correct_resolution: Basic EPS = 32,000,000 / 4,500,000 = $7.11. If-converted EPS for the bonds = (32,000,000 + 15,000,000 * 0.12 * (1 - 0.30)) / (4,500,000 + 50,000) = 33,260,000 / 4,550,000 = $7.31, which is above basic EPS, so exclude the anti-dilutive bonds. Under the treasury stock method, option proceeds are 200,000 * $50 = $10,000,000; hypothetical repurchase shares are $10,000,000 / $80 = 125,000; incremental shares are 200,000 - 125,000 = 75,000. Diluted EPS = 32,000,000 / (4,500,000 + 75,000) = $6.99.
- evidence_refs: chat-screenshot-2026-06-02-q20
- evidence_assets: chat-uploaded-screenshot-2026-06-02-q20
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md

## Financial Statement Analysis | FSA.Common-size income statements and comparison use cases (approximate LOS from screenshot)
- error_type: concept_confusion
- question_source: unknown_screenshot_source
- source_type: screenshot
- wrong_choice_or_output: Selected C. A comparison of similarly sized companies from different industries.
- correct_resolution: Correct answer: B. A time-series analysis of a rapidly expanding single company. A common-size income statement expresses each line item as a percentage of revenue, removing the effect of company size. This is especially useful when comparing the same rapidly growing company across periods because operating efficiencies and margin changes become easier to see. It is less useful for liquidity analysis because income statements are not the primary source for liquidity, and less useful for similarly sized companies across different industries because the size effect is already less important while industry differences remain.
- evidence_refs: chat-screenshot-2026-06-02-q24
- evidence_assets: chat-uploaded-screenshot-2026-06-02-q24
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md

## Financial Statement Analysis | FSA.Available-for-sale financial assets: unrealized gains and losses in OCI/AOCI (approximate LOS from screenshot)
- error_type: concept_confusion
- question_source: unknown_screenshot_source
- source_type: screenshot
- wrong_choice_or_output: Selected B. They flow through retained earnings.
- correct_resolution: Correct answer: C. They are a component of accumulated other comprehensive income. For available-for-sale financial assets, unrealized gains and losses are not recorded in net income and therefore do not flow through retained earnings. They are recognized in other comprehensive income and accumulated in AOCI, which is a component of shareholders equity.
- evidence_refs: chat-screenshot-2026-06-02-q4-afs-aoci
- evidence_assets: chat-uploaded-screenshot-2026-06-02-q4-afs-aoci
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md

## Financial Statement Analysis | FSA.Long-lived asset impairment effects on leverage and activity ratios (approximate LOS from screenshot)
- error_type: concept_confusion
- question_source: unknown_screenshot_source
- source_type: screenshot
- wrong_choice_or_output: Selected B. The total asset turnover but not the debt-to-equity ratio.
- correct_resolution: Correct answer: C. Both the debt-to-equity ratio and total asset turnover. An impairment write-down reduces long-lived assets and reduces equity through the loss, while debt and revenue are unchanged all else equal. Debt-to-equity increases because its denominator, equity, falls. Total asset turnover increases because its denominator, average total assets, falls while revenue is unchanged.
- evidence_refs: chat-screenshot-2026-06-02-impairment-ratios
- evidence_assets: chat-uploaded-screenshot-2026-06-02-impairment-ratios
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md