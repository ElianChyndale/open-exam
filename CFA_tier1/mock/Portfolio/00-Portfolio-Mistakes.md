---
bucket: Portfolio
question_count: 2
---

# Portfolio Mock Mistakes

## Portfolio Management | unknown_from_screenshot
- error_type: concept_confusion
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: 选择了 C. assumes asset prices are normally distributed。错误点在于把 Roy's safety-first criterion 对 returns 的分布假设，误记成对 asset prices 的分布假设。
- correct_resolution: Roy's safety-first criterion 关注 downside risk / shortfall risk。它讨论的是 portfolio returns 在最低可接受回报率 R_L 之下的概率，并在常见表述中假设 portfolio returns 服从正态分布；不是假设 asset prices 服从正态分布。A 正确，C 错在把 returns 和 asset prices 混了。
- evidence_refs: chat-screenshot-2026-05-25-roy-safety-first
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md

## Portfolio Management | unknown_from_screenshot
- error_type: concept_confusion
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: 选择了 A，把 "black box" 的成因误归为 data biases，而没有识别出题目真正考的是 overfitting。
- correct_resolution: 正确答案是 C。题目考的是 overfitting：ML 模型把 training data 学得过于精确，把噪音也当成真实参数，导致换一个 dataset 后预测反而不准。black box 不是因为 data biases 才被称为 black box；A 的因果关系不成立。
- evidence_refs: chat-screenshot-2026-05-25-ml-overfitting
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md