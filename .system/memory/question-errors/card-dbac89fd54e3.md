---
card_id: card-dbac89fd54e3
source_layer: question
topic: Corporate Issuers
los: M05 Capital Investments and Capital Allocation - NPV cash-flow timing
root_cause: formula_misuse
question_source: CFA Learning Ecosystem
source_type: screenshot
evidence_assets: conversation-image-2026-05-29-npv-q2
moc_target: CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md
fix_rule: 先画结构或时间轴，再代入公式或计算器。
next_drill: 24 小时内重做 2 道 Corporate Issuers / M05 Capital Investments and Capital Allocation - NPV cash-flow timing 同类题。
review_due_at: 2026-06-01
linked_patterns: 
correct_resolution: Correct answer is C. 636. Use CF0 = -1,500, CF1 = 300, CF2 = 600, CF3 = 1,000, CF4 = 200, CF5 = 500, CF6 = 300, I = 10. NPV = -1500 + 300/(1.10)^1 + 600/(1.10)^2 + 1000/(1.10)^3 + 200/(1.10)^4 + 500/(1.10)^5 + 300/(1.10)^6 = 636.32, closest to 636. The wrong answer 578 results from discounting each cash flow by one period too many.
---

## Prompt
Given a discount rate of 10%, the net present value (NPV) of the following investment is closest to: Time 0 1 2 3 4 5 6; Cash flow -1,500, 300, 600, 1,000, 200, 500, 300. A. 578. B. 605. C. 636.

## Wrong Output
A. 578.

## Evidence
chat-screenshot-2026-05-29-npv-cash-flow-timing