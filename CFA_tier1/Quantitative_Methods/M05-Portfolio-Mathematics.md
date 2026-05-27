---
title: "M05: Portfolio Mathematics"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M05"
official_module: "Module 5: Portfolio Mathematics"
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

# M05: Portfolio Mathematics

## 0. Reading Contract 学习契约

- **Official module**: Module 5: Portfolio Mathematics.
- **Official pages**: Learning Outcomes; 5.01 Introduction; 5.02 Portfolio Expected Return and Variance of Return; 5.03 Forecasting Correlation of Returns: Covariance Given a Joint Probability Function; 5.04 Portfolio Risk Measures: Applications of the Normal Distribution.
- **LOS contract**: calculate and interpret portfolio expected return, variance, standard deviation, covariance, correlation; use joint probability functions; define shortfall risk and apply Roy's safety-first criterion.
- **Evidence rule**: every miss must state whether the failed input was weight, covariance/correlation, joint probability, or threshold return.

## 1. Module Brief 模块定位

M05 turns single-asset risk into portfolio risk. 中文上它的核心不是“收益加权平均”，而是“风险为什么不能简单加权平均”：covariance and correlation determine diversification.

## 2. Curriculum Spine 教材正文主线

1. **Portfolio Expected Return and Variance of Return**: expected return is weighted average; variance includes own-risk and cross-risk terms.
2. **Covariance and Correlation**: covariance measures co-movement with units; correlation standardizes it into `[-1,+1]`.
3. **Joint Probability Function**: joint probabilities are the raw evidence for covariance/correlation when scenario returns for two assets are given.
4. **Portfolio Risk Measures: Applications of the Normal Distribution**: shortfall risk and Roy's safety-first ratio compare portfolios against a minimum acceptable return.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| weights and expected returns | calculate `E(Rp)` | "Portfolio expected return is weighted average." |
| two assets with SD and correlation | calculate variance using correlation form | "Portfolio risk includes covariance term." |
| joint probability table | compute each asset EV, covariance, correlation | "Use joint probabilities, not only marginal probabilities." |
| correlation lower than +1 | explain diversification benefit | "Risk falls below weighted average risk when rho is below +1." |
| threshold return `R_L` | calculate Roy safety-first ratio | "Choose the portfolio with the highest safety-first ratio." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `E(Rp)=sum w_iE(R_i)` | portfolio expected return | Weights should sum to 1 unless leverage/cash is stated. |
| `sigma_p^2=w1^2sigma1^2+w2^2sigma2^2+2w1w2Cov12` | two-asset variance | Do not omit the `2w1w2` covariance term. |
| `sigma_p^2=w1^2sigma1^2+w2^2sigma2^2+2w1w2sigma1sigma2rho12` | correlation form | Use when rho is given. |
| `Cov12=sum p_i[R1_i-E(R1)][R2_i-E(R2)]` | joint-probability covariance | Use joint probabilities for each paired state. |
| `rho12=Cov12/(sigma1 sigma2)` | correlation | Standardized co-movement; unitless. |
| `SFRatio=[E(Rp)-R_L]/sigma_p` | Roy safety-first | Highest value is preferred for fixed threshold. |
| `rho=+1 / 0 / -1` | diversification interpretation | +1 no benefit; -1 may hedge fully depending on weights. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `portfolio_variance`, `covariance_term`, `joint_probability`, `correlation_interpretation`, `safety_first`.
- Future records should include weights, standard deviations, covariance/correlation, and the threshold return if safety-first is involved.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Portfolio risk treated as weighted average of SDs | Portfolio variance includes covariance/correlation terms. |
| Correlation sign interpreted as risk level | Sign shows direction; risk effect depends on weight and volatility too. |
| Joint probability table replaced by marginal probabilities | Covariance needs paired outcomes and joint probabilities. |
| SFRatio compared with Sharpe ratio | SFRatio uses threshold `R_L`, not necessarily risk-free rate. |
| Low correlation treated as low-risk asset | Low correlation helps diversification but does not make the asset safe. |

## 7. Final Recall Sheet 最后回忆页

- Return is weighted average; variance is not.
- Covariance sign = co-movement; correlation magnitude = standardized linear strength.
- `rho < +1` creates diversification benefit.
- Joint probability table -> EVs -> covariance -> correlation.
- Roy: maximize `[E(Rp)-R_L]/sigma_p`.
