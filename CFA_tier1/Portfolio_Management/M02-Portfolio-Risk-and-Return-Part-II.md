---
title: "M02: Portfolio Risk and Return: Part II"
description: "CFA Level I 2026 Portfolio Management 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Portfolio Management"
topic_area: "Portfolio_Management"
level: "CFA Level I"
exam_year: 2026
exam_weight: "8-12%"
module: "M02"
official_module: "Module 2: Portfolio Risk and Return: Part II"
los_count: 9
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Portfolio_Management
---

# M02: Portfolio Risk and Return: Part II

## 0. Reading Contract 阅读契约

- **Official spine**：Risk-free plus risky assets, CAL/CML, leveraged portfolios, systematic and nonsystematic risk, return models, beta, CAPM/SML, CAPM applications, performance appraisal.
- **LOS contract**：explain risk-free/risky combinations, CAL/CML, systematic risk, return models, beta, CAPM/SML, CAPM expected return, SML applications and performance measures.
- **Evidence rule**：错题标 `cal_cml`, `beta`, `capm_required_return`, `sml_mispricing`, or `performance_metric`。

## 1. Module Brief 模块定位

Part II prices risk. 本模块把 M01 的 diversification 推到结论：market only compensates systematic risk, so beta and CAPM become the required-return engine。

## 2. Curriculum Spine 教材主线

| Spine | English trigger | 中文任务 |
|---|---|---|
| Risk-free + risky | capital allocation line, borrowing/lending | 计算目标组合收益和风险。 |
| CML | market portfolio, Sharpe slope | 判断最优风险组合与配置线。 |
| Systematic risk | diversifiable vs nondiversifiable | 解释为什么非系统风险不被补偿。 |
| Return models | market model, alpha, beta | 连接回归和预期收益。 |
| CAPM/SML | required return, beta, market risk premium | 计算 required return and mispricing。 |
| Performance | Sharpe, Treynor, Jensen alpha, M-squared | 选对风险口径。 |

## 3. Exam Translation 考试翻译

1. 给 risk-free plus risky portfolio：用 `y` 权重和 CAL。
2. 给 beta/covariance：算 systematic risk, not total risk。
3. 给 expected return and required return：高于 SML required return = undervalued/positive alpha。
4. Performance metric：Sharpe 用 total risk；Treynor/Jensen 用 beta。

## 4. Formula & Decision Bench 公式与决策台

| Item | Formula / rule | Use |
|---|---|---|
| CAL return | `E(R_C)=R_f + y[E(R_P)-R_f]` | Combined portfolio return. |
| CAL risk | `sigma_C = y sigma_P` | Risk-free asset has zero standard deviation. |
| Risky weight | `y=[E(R_C)-R_f]/[E(R_P)-R_f]` | Target return allocation. |
| Beta | `beta_i = Cov(R_i,R_M)/Var(R_M)` | Systematic risk. |
| Portfolio beta | `beta_p=sum w_i beta_i` | Portfolio systematic risk. |
| CAPM | `E(R_i)=R_f + beta_i[E(R_M)-R_f]` | Required return. |
| Sharpe | `(R_p-R_f)/sigma_p` | Total-risk performance. |
| Treynor | `(R_p-R_f)/beta_p` | Systematic-risk performance. |
| Jensen alpha | `R_p-[R_f+beta_p(R_M-R_f)]` | CAPM abnormal return. |
| M-squared | `R_f + Sharpe_p x sigma_M - R_M` | Sharpe in return units. |

## 5. Practice & Mock Evidence 题库证据

- Track `beta_total_risk` when beta is interpreted as total volatility.
- Track `sharpe_treynor_swap` when metric risk denominator is wrong.
- Track `sml_direction` when over/undervaluation sign is reversed.
- Track `leveraged_cal` when `y > 1` borrowing is missed.

## 6. Trap Ledger 陷阱账本

| Trap | Fix rule |
|---|---|
| Investors are paid for all risk | Only systematic risk earns expected compensation in CAPM. |
| CML and SML are interchangeable | CML uses total risk for efficient portfolios; SML uses beta for any asset. |
| High beta means high total risk | Beta is market sensitivity only. |
| Positive alpha equals high raw return | Alpha is return above CAPM required return. |

## 7. Final Recall Sheet 最终回忆单

- CAL: combine risk-free asset and risky portfolio.
- CML: efficient portfolios with market portfolio.
- SML/CAPM: required return by beta.
- Sharpe = total risk; Treynor/Jensen = beta risk.
- Expected return above required return = undervalued / positive alpha.
