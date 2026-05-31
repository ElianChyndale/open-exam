---
card_id: card-4ef0b4d89e69
source_layer: question
topic: Quantitative Methods
los: unknown_from_screenshot
root_cause: formula_misuse
question_source: unknown_from_screenshot
source_type: screenshot
evidence_assets: chat_image_1
moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md
fix_rule: 先画结构或时间轴，再代入公式或计算器。
next_drill: 24 小时内重做 2 道 Quantitative Methods / unknown_from_screenshot 同类题。
review_due_at: 2026-05-28
linked_patterns: 
correct_resolution: 若收益率按小数表示，则 target 2% 必须写成 0.02。低于 2% 的回报分别用 (0.015-0.02)^2、(-0.02-0.02)^2、(0-0.02)^2，合计 0.002025，再按题目口径开方得到 1.50%。核心不是公式变了，而是 percent 与 decimal 必须全程统一单位。
review_status: Reviewed once
---

## Prompt
The target semideviation of the returns over 10 years, if the target is 2 percent, is closest to? 错因集中在 target semideviation 计算时没有统一单位，把 2% 当成 2 使用，而前面的 return 已按小数口径处理。

## Wrong Output
选择了 A. 1.42 percent。错误路径：在计算低于 target 的偏差时，没有把 target 2% 转成 0.02，导致 deviation 和 squared deviation 口径错误。

## Evidence
chat-screenshot-2026-05-25-target-semideviation