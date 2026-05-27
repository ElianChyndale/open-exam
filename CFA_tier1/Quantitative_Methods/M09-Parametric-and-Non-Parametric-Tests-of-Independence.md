---
title: "M09: Parametric and Non-Parametric Tests of Independence"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M09"
official_module: "Module 9: Parametric and Non-Parametric Tests of Independence"
los_count: 2
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M09: Parametric and Non-Parametric Tests of Independence

## 0. Reading Contract 学习契约

- **Official module**: Module 9: Parametric and Non-Parametric Tests of Independence.
- **Official pages**: Learning Outcomes; 9.01 Introduction; 9.02 Tests Concerning Correlation; 9.03 Tests of Independence Using Contingency Table Data.
- **LOS contract**: explain Pearson/Spearman tests of `rho=0` and determine rejection; explain independence tests from contingency tables.
- **Evidence rule**: record variable type first: continuous-continuous, ordinal/rank, or categorical-categorical.

## 1. Module Brief 模块定位

M09 tests whether variables are associated or independent. 中文上它不再只描述 correlation，而是问“这个样本关联是否足以拒绝总体无关联/独立的原假设”。

## 2. Curriculum Spine 教材正文主线

1. **Tests Concerning Correlation**: Pearson parametric test evaluates whether population correlation is zero under distribution assumptions.
2. **Parametric Test of a Correlation**: the t statistic uses sample correlation r and df = `n-2`.
3. **Non-Parametric Test of Correlation: Spearman Rank Correlation Coefficient**: ranks handle ordinal, nonnormal, or outlier-heavy data and evaluate monotonic association.
4. **Tests of Independence Using Contingency Table Data**: chi-square test compares observed categorical counts with expected counts under independence.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| two continuous variables, sample r, n | Pearson correlation t-test | "Test H0: rho = 0 with df = n-2." |
| ordinal data or outliers | Spearman rank correlation | "Use rank-based nonparametric correlation." |
| contingency table | chi-square independence test | "Compare observed and expected frequencies." |
| significant correlation | interpret association carefully | "Rejecting rho=0 does not prove causality." |
| significant chi-square | state not independent | "The test does not show direction or strength." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `t = r sqrt[(n-2)/(1-r^2)]` | Pearson test of `rho=0` | df is `n-2`, not `n-1`. |
| Spearman rank correlation | nonparametric correlation | Detects monotonic association, not necessarily linear relation. |
| `E=(row total x column total)/n` | expected cell frequency | Compute before chi-square statistic. |
| `chi^2=sum[(O-E)^2/E]` | contingency-table independence test | Right-tail test; larger statistic rejects independence. |
| `df=(r-1)(c-1)` | chi-square independence df | r = rows, c = columns. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `correlation_t_test`, `df_n_minus_2`, `spearman`, `contingency_table`, `expected_frequency`, `chi_square_independence`.
- Future records should preserve table row/column totals or the sample correlation and n.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Correlation t-test df set to `n-1` | Use `n-2`. |
| Spearman treated as linear correlation | Spearman tests rank/monotonic association. |
| Chi-square test interpreted as strength/direction | It only tests independence vs association. |
| Expected cell frequency skipped | Compute `E=(row total x column total)/n` first. |
| Statistical association treated as causal | Association is not causality. |

## 7. Final Recall Sheet 最后回忆页

- Pearson correlation test: `t=r sqrt[(n-2)/(1-r^2)]`, df=`n-2`.
- Spearman = rank-based nonparametric test.
- Chi-square independence: expected frequency first, then `sum(O-E)^2/E`, df=`(r-1)(c-1)`.
- Rejecting independence does not tell direction, strength, or causality.
