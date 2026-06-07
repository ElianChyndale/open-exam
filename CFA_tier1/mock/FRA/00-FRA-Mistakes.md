---
bucket: FRA
question_count: 10
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

## Financial Statement Analysis | M04 Analyzing Statements of Cash Flows I - cash paid to suppliers from COGS, inventory, and accounts payable
- error_type: formula_misuse
- question_source: unknown_screenshot_source
- source_type: screenshot
- wrong_choice_or_output: Selected C. USD83 million.
- correct_resolution: Correct answer: A. USD67 million. First derive purchases from suppliers: COGS 75 minus the inventory decline of 6 equals purchases of 69. Then adjust for the increase in accounts payable of 2: because payables increased, not all purchases were paid in cash, so cash paid to suppliers is 69 minus 2 = 67.
- evidence_refs: chat-screenshot-2026-06-03-fsa-cash-paid-to-suppliers-q7
- evidence_assets: chat-uploaded-screenshot-2026-06-03-fsa-cash-paid-to-suppliers-q7
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md

## Financial Statement Analysis | FSA.M05
- error_type: formula_misuse
- question_source: user_screenshot
- source_type: screenshot
- wrong_choice_or_output: C. Deduct both after-tax interest payments and capital expenditures from operating cash flows.
- correct_resolution: B. Add operating cash flows to after-tax interest payments and deduct capital expenditures.
- evidence_refs: user-screenshot-1
- evidence_assets: 
- moc_target: 

## Financial Statement Analysis | FSA.M05
- error_type: concept_confusion
- question_source: user_screenshot
- source_type: screenshot
- wrong_choice_or_output: B. 73
- correct_resolution: A. 70. Because interest is classified as financing cash flow, FCFF = CFO - CapEx = 120 - 50 = 70.
- evidence_refs: user-screenshot-2
- evidence_assets: 
- moc_target: 

## Financial Statement Analysis | calculate and interpret common-size balance sheets and related financial ratios (approximate from screenshot)
- error_type: formula_misuse
- question_source: unknown
- source_type: screenshot
- wrong_choice_or_output: Unknown from screenshot evidence; likely denominator confusion in vertical common-size balance sheet.
- correct_resolution: Correct answer: B. 25%. For a vertical common-size balance sheet, each balance-sheet line item is expressed as a percentage of total assets. Total assets = 125 + 35 = 160, so cash and cash equivalents = 40 / 160 = 25%.
- evidence_refs: chat-2026-06-05, screenshot-question
- evidence_assets: chat_upload:screenshot:2026-06-05-common-size-balance-sheet
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md

## Financial Statement Analysis | inventory write-down risk under US GAAP with rising inventory costs (approximate from screenshot)
- error_type: concept_confusion
- question_source: unknown
- source_type: screenshot
- wrong_choice_or_output: A. FIFO
- correct_resolution: Correct answer: B. LIFO. In a period of stable inventory quantities and rising unit costs, LIFO ending inventory is carried at relatively older, lower costs, making it less likely that carrying value will exceed market and trigger a write-down under US GAAP.
- evidence_refs: chat-2026-06-05, batch-3q-1-wrong
- evidence_assets: chat_upload:screenshot:2026-06-05-inventory-write-down-lifo
- moc_target: CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md

## Financial Statement Analysis | impairment measurement for long-lived assets under IFRS versus US GAAP (approximate from screenshot)
- error_type: accounting_standard_confusion
- question_source: unknown
- source_type: screenshot
- wrong_choice_or_output: C. EUR20,000
- correct_resolution: Correct answer: B. EUR17,400. Under IFRS, impairment is measured using recoverable amount = higher of value in use and fair value less costs to sell. Fair value less costs to sell = 19,100 - 1,900 = 17,200, so recoverable amount = max(17,400, 17,200) = 17,400. Because carrying value 20,000 exceeds recoverable amount 17,400, the asset is written down to 17,400. The undiscounted expected future cash flows figure is a US GAAP trigger-style input, not the measurement amount used for the IFRS answer here.
- evidence_refs: chat-2026-06-07, screenshot-impairment-equipment-ifrs-vs-usgaap
- evidence_assets: chat_upload:screenshot:2026-06-07-impairment-equipment-ifrs-vs-usgaap
- moc_target: CFA_tier1/Financial_Statement_Analysis/M07-Analysis-of-Long-Term-Assets.md