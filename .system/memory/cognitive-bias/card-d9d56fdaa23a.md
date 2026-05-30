---
card_id: card-d9d56fdaa23a
source_layer: bias
topic: Corporate Issuers
los: M05 Capital Investments and Capital Allocation - table-heavy decision criterion scan
root_cause: table_overload_constraint_miss
bias_signal: table_overload_constraint_miss
question_source: user_reflection
source_type: screenshot_reflection
evidence_assets: conversation-image-2026-05-29-roic-criterion-q18
moc_target: CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md
fix_rule: 图表信息过载时先做 10 秒门槛扫描：minimum、target、required、criterion、constraint、hurdle，再读项目数据。
next_drill: 下次学习 Corporate Issuers 前先口述纠偏规则，再开始做题。
review_due_at: 2026-06-01
linked_patterns: 
correct_resolution: Before comparing project outputs, first identify the governing decision criterion in the stem: management criterion, hurdle rate, minimum ROIC, required return, constraint, or ranking rule. Then test each project against that criterion before using NPV/IRR as supporting evidence.
---

## Prompt
In a table-heavy capital allocation question, the decision criterion was ROIC-based and required checking a minimum target of 9.20 percent before choosing based on NPV.

## Wrong Output
Focused on Project B positive/higher NPV and ignored the minimum ROIC/IRR hurdle because the chart contained too much information.

## Evidence
chat-screenshot-2026-05-29-roic-criterion-irr-npv-projects
