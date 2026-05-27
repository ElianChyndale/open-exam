---
title: "M01: Portfolio Risk and Return: Part I"
description: "CFA Level I 2026 Portfolio Management 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Portfolio Management"
topic_area: "Portfolio_Management"
level: "CFA Level I"
exam_year: 2026
exam_weight: "8-12%"
module: "M01"
official_module: "Module 1: Portfolio Risk and Return: Part I"
los_count: 7
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Portfolio_Management
---

# M01: Portfolio Risk and Return: Part I

## 0. Reading Contract 阅读契约

- **Official spine**：Historical return/risk, asset characteristics, risk aversion, utility, two risky assets, many risky assets, diversification, efficient frontier.
- **LOS contract**：describe asset classes; explain risk aversion and optimal portfolios; calculate/interpret mean, variance, covariance/correlation and portfolio standard deviation; describe diversification and efficient frontier.
- **Evidence rule**：错题标 `return_measure`, `real_nominal`, `portfolio_variance`, `utility`, or `diversification`。

## 1. Module Brief 模块定位

Part I builds the risk-return toolkit before CAPM. 本模块必须掌握：return can be averaged by weights, but risk depends on covariance and correlation; real return answers purchasing power; utility connects expected return to risk aversion。

## 2. Curriculum Spine 教材主线

| Spine | English trigger | 中文任务 |
|---|---|---|
| Historical return/risk | arithmetic, geometric, nominal, real | 判断收益口径。 |
| Asset characteristics | liquidity, volatility, inflation exposure | 连接资产类别特征。 |
| Risk aversion | utility, indifference curves | 判断更高风险需要更高收益补偿。 |
| Two risky assets | covariance, correlation, portfolio variance | 计算组合风险。 |
| Many risky assets | diversification, efficient frontier, GMV | 解释低相关和有效组合。 |

## 3. Exam Translation 考试翻译

1. 问 purchasing power：用 real return，不用 nominal return。
2. 给 weights and returns：`E(R_p)` 直接加权。
3. 给 risk/correlation：使用 variance formula，不把标准差直接加权。
4. 给 risk aversion `A`：算 utility 并选择最高 utility。
5. 问 diversification：重点是 `rho < +1`，不是资产数量本身。

## 4. Formula & Decision Bench 公式与决策台

| Item | Formula / rule | Use |
|---|---|---|
| Real return exact | `(1+nominal)/(1+inflation)-1` | Purchasing power. |
| Real return approx | `nominal - inflation` | Quick estimate when rates small. |
| Portfolio return | `E(R_p)=sum w_iE(R_i)` | Weighted average return. |
| Covariance | `Cov_12 = rho_12 sigma_1 sigma_2` | Link correlation to variance. |
| Two-asset variance | `w_1^2sigma_1^2 + w_2^2sigma_2^2 + 2w_1w_2rho_12sigma_1sigma_2` | Core risk calculation. |
| Utility | `U = E(R) - 0.5 A sigma^2` | Risk-aversion choice. |
| Diversification | lower `rho` lowers portfolio risk | Risk reduction framework. |

## 5. Practice & Mock Evidence 题库证据

- Track `risk_weighted_average` when standard deviation is incorrectly averaged.
- Track `real_return` when inflation adjustment is skipped.
- Track `correlation_effect` when `rho=+1` and `rho<+1` are treated alike.
- Track `utility_units` when returns/variance are mixed in percent vs decimal units.

## 6. Trap Ledger 陷阱账本

| Trap | Fix rule |
|---|---|
| Portfolio risk = weighted average standard deviation | Only true under special perfect-correlation cases; use variance formula. |
| More assets always means diversification | Low correlation is the source of diversification. |
| Highest expected return is optimal | Check risk and investor utility. |
| Nominal return answers all return questions | Real return answers purchasing power. |

## 7. Final Recall Sheet 最终回忆单

- Return weighted average; risk covariance-driven.
- Exact real return = `(1+nominal)/(1+inflation)-1`.
- Two-asset variance formula is the core calculation.
- `rho < +1` creates diversification benefit.
- Utility = expected return minus risk penalty.
