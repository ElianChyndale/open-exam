---
title: "M08: Hypothesis Testing"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M08"
official_module: "Module 8: Hypothesis Testing"
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

# M08: Hypothesis Testing

## 0. Reading Contract 学习契约

- **Official module**: Module 8: Hypothesis Testing.
- **Official pages**: Learning Outcomes; 8.01 Introduction; 8.02 Hypothesis Tests for Finance; 8.03 Tests of Return and Risk in Finance; 8.04 Parametric versus Nonparametric Tests.
- **LOS contract**: explain components, significance, Type I/II errors, power; construct and determine statistical significance; compare parametric and nonparametric tests.
- **Evidence rule**: preserve H0/H1, alpha, test statistic, distribution, df, p-value or critical value, and final language.

## 1. Module Brief 模块定位

M08 is the decision discipline for sample evidence. 中文上它要求你先写清“默认命题是什么”，再决定用哪个分布、哪个临界规则，最后只说 reject 或 fail to reject。

## 2. Curriculum Spine 教材正文主线

1. **Hypothesis Tests for Finance**: define H0/H1, choose statistic and distribution, set significance level, state decision rule.
2. **The Process of Hypothesis Testing**: p-value and critical value methods are equivalent when used correctly.
3. **Tests of Return and Risk in Finance**: paired t, pooled/unequal t, F tests, proportion tests, and chi-square variance tests map different finance questions to different distributions.
4. **Parametric versus Nonparametric Tests**: parametric tests rely on distribution assumptions; nonparametric tests help when data are ordinal, nonnormal, or outlier-prone.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| "at 5% significance" | set alpha = 0.05 | "Reject only if statistic falls in rejection region or p <= alpha." |
| H1 says "not equal" | two-tailed test | "Split alpha across two tails." |
| p-value smaller than alpha | reject H0 | "Evidence is statistically significant at alpha." |
| p-value larger than alpha | fail to reject H0 | "Evidence is insufficient to reject H0." |
| before/after same entities | paired t | "Run test on differences." |
| two independent means, equal variances | pooled t | "Use pooled variance estimator." |
| variance test | F or chi-square | "F for two variances; chi-square for one variance." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `z=(xbar-mu0)/(sigma/sqrt(n))` | mean test, sigma known | Confirm sigma is population sigma. |
| `t=(xbar-mu0)/(s/sqrt(n))` | mean test, sigma unknown | df usually `n-1`. |
| `Power=1-beta` | test power | Higher n usually increases power. |
| Type I / Type II | reject true H0 / fail to reject false H0 | Type I probability is alpha. |
| `s_p^2=[(n1-1)s1^2+(n2-1)s2^2]/(n1+n2-2)` | pooled t | Equal variances assumed. |
| `t=(xbar1-xbar2-d0)/(s_p sqrt(1/n1+1/n2))` | independent two-sample pooled t | df=`n1+n2-2`. |
| `t=[(xbar1-xbar2)-d0]/sqrt(s1^2/n1+s2^2/n2)` | unequal-variance t | Do not pool. |
| `t=dbar/(s_d/sqrt(n))` | paired t | df=`n-1`, n is number of pairs. |
| `F=s1^2/s2^2` | two-variance test | Sensitive to normality. |
| `chi^2=(n-1)s^2/sigma0^2` | one-variance test | df=`n-1`; chi-square is right-skewed. |
| `z=(p1hat-p2hat)/sqrt[phat(1-phat)(1/n1+1/n2)]` | two-proportion test | Use pooled proportion under H0. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `hypothesis_language`, `tail_direction`, `p_value`, `type_error`, `test_selection`, `df`, `parametric_nonparametric`.
- Future records should include the rejected/failed-to-reject sentence exactly, because language errors are common even when math is right.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Saying "accept H0" | Say "fail to reject H0". |
| p-value treated as probability H0 is true | p-value is probability of sample or more extreme result assuming H0. |
| One-tailed and two-tailed alpha mixed | H1 direction determines tail structure. |
| Paired data tested as independent samples | Same subject or matched pair -> paired t on differences. |
| Parametric tests used despite ordinal/non-normal data | Consider nonparametric test when assumptions are weak. |

## 7. Final Recall Sheet 最后回忆页

- Steps: H0/H1 -> statistic/distribution -> alpha -> rule -> compute -> reject/fail to reject -> interpret.
- Type I = reject true H0 = alpha. Type II = fail to reject false H0 = beta. Power = `1-beta`.
- p <= alpha rejects H0.
- z/t for means; F for two variances; chi-square for one variance; paired t for before/after.
- Statistical significance is not automatically economic significance.
