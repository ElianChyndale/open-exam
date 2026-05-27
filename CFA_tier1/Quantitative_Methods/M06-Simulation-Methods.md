---
title: "M06: Simulation Methods"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M06"
official_module: "Module 6: Simulation Methods"
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

# M06: Simulation Methods

## 0. Reading Contract 学习契约

- **Official module**: Module 6: Simulation Methods.
- **Official pages**: Learning Outcomes; 6.01 Introduction; 6.02 Lognormal Distribution and Continuous Compounding; 6.03 Monte Carlo Simulation; 6.04 Bootstrapping.
- **LOS contract**: explain normal/lognormal relationship; describe Monte Carlo and investment applications; describe bootstrap resampling from observed data.
- **Evidence rule**: classify misses as distribution mapping, Monte Carlo purpose/limits, bootstrap mechanics, or sample-bias interpretation.

## 1. Module Brief 模块定位

M06 explains how to approximate investment outcome distributions when a single closed-form answer is insufficient. 中文上它把“一个答案”改成“很多可能结果的分布”，并要求你知道输入假设会控制输出质量。

## 2. Curriculum Spine 教材正文主线

1. **Lognormal Distribution and Continuous Compounding**: continuously compounded returns can be modeled as normal; asset prices implied by exponentiating those returns are lognormal and nonnegative.
2. **Monte Carlo Simulation**: specify input distributions, parameters, and correlations; generate many random scenarios; summarize the output distribution.
3. **Bootstrapping**: resample observed data with replacement to build an empirical sampling distribution for a statistic.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| continuously compounded return is normal | infer price is lognormal | "Price is nonnegative and right-skewed." |
| complex, nonlinear, path-dependent payoff | choose Monte Carlo | "Simulation produces an outcome distribution, not one guaranteed result." |
| historical sample, no parametric distribution | choose bootstrap | "Bootstrap samples with replacement from observed data." |
| model input assumptions questionable | warn about model risk | "More trials reduce simulation noise, not model misspecification." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `r_cc=ln(P_t/P_0)` | continuously compounded return | Additive over time. |
| `P_t=P_0e^r` | price from continuous return | Normal return implies lognormal price. |
| Monte Carlo flow | set distribution -> random draws -> model outcome -> summarize distribution | Output quality depends on assumptions. |
| Bootstrap flow | sample n observations with replacement -> compute statistic -> repeat | Does not create information absent from original sample. |
| Simulation output | mean, variance, quantiles, shortfall probability | Do not focus only on average. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `lognormal_price`, `continuous_return`, `monte_carlo_use`, `bootstrap_resampling`, `model_input_risk`.
- Record whether the question asked for method selection, limitation, or distribution relationship.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Modeling price as normal | Price should not be negative; lognormal is the asset-price model when cc returns are normal. |
| Monte Carlo treated as exact answer | It approximates an output distribution. |
| More trials assumed to fix bad assumptions | More trials reduce random simulation error, not wrong inputs. |
| Bootstrap assumed to remove sample bias | Bootstrap inherits original sample bias. |
| Bootstrap confused with Monte Carlo | Bootstrap draws from observed empirical data; Monte Carlo draws from specified theoretical distributions. |

## 7. Final Recall Sheet 最后回忆页

- If continuous return is normal, price is lognormal.
- Monte Carlo = theoretical inputs -> many simulated scenarios -> output distribution.
- Bootstrap = observed sample -> resample with replacement -> empirical statistic distribution.
- Simulation is only as good as distribution, parameter, and correlation assumptions.
