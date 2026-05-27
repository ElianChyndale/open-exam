---
title: "M10: Simple Linear Regression"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M10"
official_module: "Module 10: Simple Linear Regression"
los_count: 6
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M10: Simple Linear Regression

## 0. Reading Contract 学习契约

- **Official module**: Module 10: Simple Linear Regression.
- **Official pages**: Learning Outcomes; 10.01 Introduction; 10.02 Estimation of the Simple Linear Regression Model; 10.03 Assumptions of the Simple Linear Regression Model; 10.04 Hypothesis Tests in the Simple Linear Regression Model; 10.05 Prediction in the Simple Linear Regression Model; 10.06 Functional Forms for Simple Linear Regression.
- **LOS contract**: describe model and OLS; explain assumptions/residual diagnostics; calculate and interpret fit and coefficient tests; interpret ANOVA/SEE; predict Y and prediction interval; describe functional forms.
- **Evidence rule**: record whether the miss was coefficient interpretation, assumption diagnosis, ANOVA/fits, hypothesis test, prediction interval, or log functional form.

## 1. Module Brief 模块定位

M10 turns correlation into a predictive linear model. 中文上它要求你分清 X/Y、解释 slope、不把 regression 当 causality，并用 residuals/ANOVA/tests/prediction interval 管理模型证据。

## 2. Curriculum Spine 教材正文主线

1. **Estimation of the Simple Linear Regression Model**: define `Y_i=b0+b1X_i+e_i`; OLS chooses coefficients that minimize SSE.
2. **Interpreting Regression Coefficients**: slope is expected change in Y for a one-unit change in X; intercept is predicted Y when X=0 and may lack economic meaning.
3. **Cross-Sectional versus Time-Series Regressions**: data structure affects diagnostics and interpretation, especially independence.
4. **Assumptions of the Simple Linear Regression Model**: linearity, homoskedasticity, independence, and normal errors are checked with residual patterns.
5. **Hypothesis Tests and ANOVA**: `SST=SSR+SSE`, R2/SEE/F/t statistics summarize fit and significance.
6. **Prediction and Functional Forms**: point prediction and prediction intervals depend on X value, SEE, and model form; log-lin/lin-log/log-log alter coefficient meaning.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| interpret slope | state change in expected Y for one-unit X | "Not causality unless design supports causal claim." |
| estimate coefficients | use covariance/variance and sample means | "OLS minimizes squared residuals." |
| residual funnel | diagnose heteroskedasticity | "Standard errors and tests may be unreliable." |
| residual curve | diagnose nonlinearity | "Linear functional form may be misspecified." |
| ANOVA table | compute R2, SEE, F | "R2 is sample explanatory power." |
| slope significance | use t-test | "Reject/fail to reject beta1 condition." |
| predicted Y | plug X into `Yhat=b0+b1X` | "Prediction interval is wider than confidence interval for mean response." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `Y_i=b0+b1X_i+e_i` | simple regression model | Name dependent and independent variables. |
| `b1=Cov(X,Y)/Var(X)` | slope estimate | Slope has units. |
| `b0=ybar-b1xbar` | intercept estimate | X=0 may be outside meaningful range. |
| `SSE=sum(Y_i-Yhat_i)^2` | OLS objective | OLS minimizes SSE. |
| `SST=SSR+SSE` | ANOVA decomposition | Total = explained + unexplained. |
| `R^2=SSR/SST=1-SSE/SST` | goodness of fit | Fit, not causality. |
| `SEE=sqrt[SSE/(n-2)]` | residual standard error | Same units as Y. |
| `t=(b1-beta1,0)/SE(b1)` | slope test | df=`n-2`. |
| `F=MSR/MSE` | model F-test | In simple regression, `F=t^2`. |
| `Yhat=b0+b1X` | point prediction | Prediction is conditional on model assumptions. |
| Prediction interval | `Yhat +/- t_c x SEE x sqrt(1+1/n+(X-Xbar)^2/((n-1)s_X^2))` | Wider than mean confidence interval; wider when X is far from Xbar. |
| Simple regression links | `b1=r(s_Y/s_X)`; `R^2=r^2` | Only for one independent variable. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `slope_interpretation`, `residual_diagnostics`, `anova`, `r_squared`, `see`, `prediction_interval`, `functional_form`.
- Future records should preserve the regression output table, not just the final answer.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Slope interpreted as causality | Slope is conditional association unless causal design exists. |
| Error normality stated as Y normality | Assumption concerns errors/residuals. |
| High R2 treated as good model automatically | Check significance, diagnostics, economic meaning, and out-of-sample risk. |
| Prediction interval confused with confidence interval | Prediction interval for individual Y is wider. |
| F and t relation forgotten | In simple regression, slope `t^2 = F`. |

## 7. Final Recall Sheet 最后回忆页

- Model: `Y=b0+b1X+e`.
- OLS minimizes SSE; slope = `Cov/Var`; intercept = `ybar-b1xbar`.
- Assumptions: linearity, homoskedasticity, independence, normal errors.
- ANOVA: `SST=SSR+SSE`; `R2=SSR/SST`; `SEE=sqrt(SSE/(n-2))`.
- Slope t-test df = `n-2`; simple regression `F=t^2`.
- Prediction interval is wider than mean-response confidence interval.
