---
card_id: card-54dfb9b2969c
source_layer: question
topic: Portfolio Management
los: unknown_from_screenshot
root_cause: concept_confusion
question_source: unknown_from_screenshot
source_type: screenshot
evidence_assets: chat_image_1
moc_target: CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md
fix_rule: 先写出考点定义，再用一句话说明为什么正确选项成立。
next_drill: 24 小时内重做 2 道 Portfolio Management / unknown_from_screenshot 同类题。
review_due_at: 2026-05-28
linked_patterns: 
correct_resolution: 正确答案是 C。题目考的是 overfitting：ML 模型把 training data 学得过于精确，把噪音也当成真实参数，导致换一个 dataset 后预测反而不准。black box 不是因为 data biases 才被称为 black box；A 的因果关系不成立。
---

## Prompt
Which of the following statements is true in the use of ML: 你选了 A. some techniques are termed "black box" due to data biases. 题目给出的正确答案是 C. training data can be learned too precisely, resulting in inaccurate predictions when used with different datasets.

## Wrong Output
选择了 A，把 "black box" 的成因误归为 data biases，而没有识别出题目真正考的是 overfitting。

## Evidence
chat-screenshot-2026-05-25-ml-overfitting