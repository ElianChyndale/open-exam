---
title: "M04: Probability Trees and Conditional Expectations"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M04"
official_module: "Module 4: Probability Trees and Conditional Expectations"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M04: Probability Trees and Conditional Expectations

## 0. Reading Contract 学习契约

- **Official module**: Module 4: Probability Trees and Conditional Expectations.
- **Official pages**: Learning Outcomes; 4.01 Introduction; 4.02 Expected Value and Variance; 4.03 Probability Trees and Conditional Expectations; 4.04 Bayes' Formula and Updating Probability Estimates.
- **LOS contract**: calculate expected values, variances, and standard deviations; formulate probability trees and conditional expectations; calculate and interpret updated probabilities with Bayes.
- **Evidence rule**: preserve the state table, branch probabilities, and prior/likelihood/posterior labels for every probability miss.

## 1. Module Brief 模块定位

M04 moves from descriptive statistics to probability-weighted investment decisions. 中文上它回答“不同情景下的结果如何加权、路径概率如何合成、新信息如何更新旧概率”。

## 2. Curriculum Spine 教材正文主线

1. **Expected Value and Variance**: expected value is a probability-weighted average; variance can be computed from deviations or from `E(X^2)-[E(X)]^2`.
2. **Probability Trees and Conditional Expectations**: branch probabilities multiply along a path; mutually exclusive terminal paths add; conditional expectation is computed by rolling back from terminal nodes.
3. **Total Probability Rule for Expected Value**: total probability combines likelihoods across all mutually exclusive states.
4. **Bayes' Formula and Updating Probability Estimates**: prior probability becomes posterior probability when new evidence is observed.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| scenario probability and return table | calculate EV and variance | "Expected value is probability-weighted average; variance measures dispersion around EV." |
| staged investment outcome | draw probability tree | "Path probabilities multiply; terminal branches add when mutually exclusive." |
| conditional expectation | roll backward from outcomes | "At each node, use conditional probabilities to compute the node value." |
| new signal, old probability | use Bayes | "Posterior equals prior times likelihood divided by total probability." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `E(X)=sum p_i x_i` | expected value | Not the most likely outcome. |
| `Var(X)=sum p_i[x_i-E(X)]^2` | variance definition | Use all states. |
| `Var(X)=E(X^2)-[E(X)]^2` | variance shortcut | Useful for tables. |
| `sigma=sqrt(Var)` | standard deviation | Same unit as outcome. |
| `P(A|B)=P(A and B)/P(B)` | conditional probability | Condition is denominator. |
| `P(A)=sum P(A|B_i)P(B_i)` | total probability | Include all mutually exclusive states. |
| `P(B_j|A)=P(A|B_j)P(B_j)/P(A)` | Bayes update | Numerator alone is not posterior. |
| `Path probability=prod branch probabilities` | probability tree | Do not add probabilities along one path. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `expected_value`, `variance_shortcut`, `probability_tree`, `conditional_probability`, `bayes_denominator`.
- Future records should include the original probability table/tree because most errors are denominator or path errors.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Treating EV as the most likely result | EV is long-run probability-weighted average. |
| Adding branch probabilities along one path | Multiply along a path; add mutually exclusive paths. |
| Confusing `P(A|B)` and `P(B|A)` | The event after the vertical bar is the condition. |
| Bayes denominator omitted | Use total probability across all states. |
| Choosing highest EV without risk comment | Investment interpretation may also require variance or shortfall context. |

## 7. Final Recall Sheet 最后回忆页

- EV = `sum p x`; variance = `E(X^2)-[E(X)]^2`.
- Probability tree: multiply down, add across mutually exclusive terminal paths, roll back expectations.
- Bayes = prior x likelihood / total probability.
- Posterior probability must be interpreted after the signal, not before.
