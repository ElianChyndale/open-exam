---
title: "M07: Estimation and Inference"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M07"
official_module: "Module 7: Estimation and Inference"
los_count: 3
difficulty: "概念+案例判断"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M07: Estimation and Inference

## 0. Reading Contract 学习契约

- **Official module**: Module 7: Estimation and Inference.
- **Official pages**: Learning Outcomes; 7.01 Introduction; 7.02 Sampling Methods; 7.03 Central Limit Theorem and Inference; 7.04 Bootstrapping and Empirical Sampling Distributions.
- **LOS contract**: compare sampling methods and sampling error; explain CLT and standard error; describe bootstrap/jackknife resampling.
- **Evidence rule**: tag misses by sample design, CLT scope, SE/SD confusion, or resampling method.

## 1. Module Brief 模块定位

M07 is the bridge from sample evidence to population claims. 中文上它先问“样本是否能代表总体”，再问“样本均值有多不确定”，最后问“没有解析公式时如何重抽样估计”。

## 2. Curriculum Spine 教材正文主线

1. **Sampling Methods**: simple random, stratified random, cluster, convenience, and judgmental sampling differ in representativeness, cost, and bias risk.
2. **Sampling from Different Distributions**: population shape matters, but inference often focuses on the sampling distribution of the mean.
3. **Central Limit Theorem and Inference**: for sufficiently large samples, the sample mean is approximately normal even if the population is not.
4. **Bootstrapping and Empirical Sampling Distributions**: bootstrap and jackknife estimate sampling distributions, standard errors, and bias when analytical formulas are difficult.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| every member equal known chance | simple random sampling | "Probability sample supports inference if implemented correctly." |
| population divided into strata | stratified random sampling | "Improves representation of key subgroups." |
| groups sampled first | cluster sampling | "Cost efficient but may raise sampling error." |
| easy-to-access observations | convenience sampling | "Fast but high bias risk." |
| expert-selected observations | judgmental sampling | "Subjective and not strongly generalizable." |
| sample mean uncertainty | use SE | "SE measures dispersion of sample means." |
| complex statistic, no analytic SE | bootstrap/jackknife | "Use empirical resampling distribution." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `SE=sigma/sqrt(n)` | known population sigma | SE is not SD. |
| `SE=s/sqrt(n)` | sigma unknown, sample s used | Common exam setting. |
| CLT | sample mean approximately normal for large n | Applies to `xbar`, not raw observations. |
| `n=(z sigma/E)^2` | required sample size | E is margin of error; halving E needs 4x n. |
| Bootstrap | resample with replacement | Inherits bias in the original sample. |
| Jackknife | leave-one-out resampling | Often estimates bias/variance; not outlier deletion. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `sampling_method`, `sampling_bias`, `standard_error`, `clt_scope`, `bootstrap`, `jackknife`.
- Future records should quote the sample-design language because terms like convenience, stratified, and cluster drive the answer.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Increasing n assumed to remove bias | Larger n lowers sampling error, not systematic bias. |
| CLT applied to raw data | CLT concerns the sampling distribution of the sample mean. |
| SE and SD used interchangeably | SD is individual observation dispersion; SE is sample-mean uncertainty. |
| Convenience sample treated as strong evidence | Non-probability sampling limits inference. |
| Jackknife described as outlier removal | Jackknife recalculates statistics after deleting one observation at a time. |

## 7. Final Recall Sheet 最后回忆页

- Probability sampling supports stronger inference than convenience/judgmental sampling.
- Stratified improves subgroup representation; cluster saves cost but may increase error.
- `SE = s/sqrt(n)`; SE halves only when sample size quadruples.
- CLT: sample mean, not observations, becomes approximately normal.
- Bootstrap estimates SE/distribution; jackknife often estimates bias/variance.
