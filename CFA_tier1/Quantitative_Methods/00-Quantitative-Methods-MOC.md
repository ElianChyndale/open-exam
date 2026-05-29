---
title: "00-Quantitative Methods-MOC"
description: "CFA Level I 2026 Quantitative Methods 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: CFA Level I
exam_year: 2026
exam_weight: "6-9%"
module_count: 11
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Quantitative_Methods
---

# Quantitative Methods MOC

> **一句话核心**: Quant is the exam's translation layer. 它把投资问题翻译成 return, cash flow, probability, inference, regression and model-risk evidence.

## 1. Subject Brief 科目定位

- **Exam weight**: 6-9%.
- **Official scope**: 11 modules, from return measurement and TVM to inference, regression, and Big Data techniques.
- **Core exam job**: identify the variable, choose the correct formula or statistical test, compute if needed, then interpret the investment meaning and limitation.
- **C+ redesign principle**: Formula & Framework Map is the control panel; Module Atlas tells where to study; Curriculum Spine tells why the sequence exists; Evidence Map tells where mistakes should be attached.
- **Reading rule**: official module registry and 2026 textbook index are the structure source. Obsidian pages are projection notes, not source of truth.

## 2. Formula & Framework Map 公式与框架地图

### Return and compounding spine

| Trigger | Formula / Framework | Exam decision |
|---|---|---|
| Holding-period total return | `HPR = (P1 - P0 + D1) / P0`; `Gross return = 1 + HPR = (P1 + D1) / P0` | Use for one holding period. Check whether income is already included in ending value. |
| Arithmetic mean | `AM = sum(R_i) / n` | Best for one-period expected return. It is not the long-run compounded wealth rate. |
| Geometric mean | `GM = [prod(1+R_i)]^(1/n) - 1` | Best for multi-period compound growth. Volatility makes GM <= AM. |
| Harmonic mean | `HM = n / sum(1/x_i)` | Best for averaging price multiples such as P/E. It dampens high multiple outliers. |
| MWRR | Solve `0 = sum(CF_t / (1+r)^t)` | Investor experience; sensitive to amount and timing of external cash flows. |
| TWRR | Split at external cash flows, then `prod(1+HP_i) - 1` | Manager performance; neutralizes investor-controlled cash flow timing. |
| Annualized return | `(1 + R_period)^c - 1` | Use c = periods per year. Do not confuse period return with annual return. |
| Continuously compounded return | `r_cc = ln(1+HPR)`; convert back with `e^(r_cc)-1` | Continuous returns add across periods; ordinary returns compound multiplicatively. |
| Gross/net/tax/leverage | `net = gross - fees`; `leveraged = R_p + (B/E)(R_p-r_D)`; `after-tax = pre-tax x (1-t)` | Order matters: gross -> net -> leverage -> tax. Trading expenses are already reflected in gross return. |

### TVM and cash-flow spine

| Trigger | Formula / Framework | Exam decision |
|---|---|---|
| Single cash flow | `FV = PV(1+r)^n`; `PV = FV/(1+r)^n` | Draw the timeline before pressing the calculator. Match r and n frequency. |
| Continuous compounding / discounting | `FV = PV e^(rt)`; `PV = FV e^(-rt)` | Use only when the rate is explicitly continuously compounded. |
| Ordinary annuity | `PV = A[1 - 1/(1+r)^n]/r`; `FV = A[(1+r)^n - 1]/r` | End-of-period cash flows. |
| Annuity due | ordinary annuity value x `(1+r)` | Beginning-of-period cash flows. |
| Perpetuity | `PV = A/r` | Level infinite cash flow. |
| Growing perpetuity | `PV = A1/(r-g)`, with `r > g` | Equity DDM interface; numerator is next cash flow, not current cash flow. |
| Growing annuity | `PV = [A1/(r-g)][1 - ((1+g)/(1+r))^n]` | Finite growing cash flow stream. |
| Implied return / growth | Bond/YTM as IRR; equity `r = D1/P0 + g`; `g = r - D1/P0` | Given price and cash flows, solve the missing rate or growth input. |
| Cash-flow additivity | portfolio value = sum of component PVs | No-arbitrage interface for forward rates, forward FX, and option payoff replication. |

### Probability, statistics, and portfolio spine

| Trigger                      | Formula / Framework                              | Exam decision                                                                 |                                                               |              |                                                                                  |
| ---------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------- | ------------ | -------------------------------------------------------------------------------- |
| Expected value               | `E(X) = sum(p_i x_i)`                            | Probability-weighted mean, not most likely outcome.                           |                                                               |              |                                                                                  |
| Variance from probabilities  | `Var(X)=sum p_i[x_i-E(X)]^2 = E(X^2)-[E(X)]^2`   | Use shortcut for scenario tables.                                             |                                                               |              |                                                                                  |
| Conditional probability      | `P(A                                             | B)=P(A and B)/P(B)`                                                           | The condition is the denominator.                             |              |                                                                                  |
| Total probability            | `P(A)=sum P(A                                    | B_i)P(B_i)`                                                                   | Required before Bayes; include all mutually exclusive states. |              |                                                                                  |
| Bayes formula                | `P(B_j                                           | A)=P(A                                                                        | B_j)P(B_j)/sum[P(A                                            | B_i)P(B_i)]` | Prior x likelihood / total probability. New information updates old probability. |
| Portfolio expected return    | `E(Rp)=sum w_iE(R_i)`                            | Return is weighted average; risk is not.                                      |                                                               |              |                                                                                  |
| Covariance                   | `Cov12=sum p_i[R1_i-E(R1)][R2_i-E(R2)]`          | Sign gives co-movement direction.                                             |                                                               |              |                                                                                  |
| Correlation                  | `rho12 = Cov12/(sigma1 sigma2)`                  | Standardized strength in `[-1,+1]`; not causation.                            |                                                               |              |                                                                                  |
| Two-asset portfolio variance | `sigma_p^2=w1^2sigma1^2+w2^2sigma2^2+2w1w2Cov12` | Must include covariance term; use `2w1w2sigma1sigma2rho12` when rho is given. |                                                               |              |                                                                                  |
| Roy safety-first             | `SFRatio=[E(Rp)-R_L]/sigma_p`                    | Choose the highest SFRatio when the threshold return is fixed.                |                                                               |              |                                                                                  |

### Simulation and resampling spine

| Trigger | Formula / Framework | Exam decision |
|---|---|---|
| Lognormal price | if `r_cc` is normal, `P_t=P_0e^r` is lognormal | Prices cannot be negative; returns and prices use different distributions. |
| Monte Carlo | specify distributions, parameters, correlations -> draw many scenarios -> summarize output distribution | Useful for nonlinear, complex, or path-dependent investment problems. Garbage in, garbage out. |
| Bootstrap | sample with replacement from observed data, compute statistic repeatedly | Estimates sampling distribution/SE without a strong parametric distribution, but inherits sample bias. |
| Jackknife | leave one observation out repeatedly | Often used to estimate bias/variance; not an outlier-removal method. |

### Estimation, CLT, confidence interval, and hypothesis-testing spine

| Trigger | Formula / Framework | Exam decision |
|---|---|---|
| Standard error | `SE = sigma/sqrt(n)` or `s/sqrt(n)` | SE measures uncertainty of the sample mean; SD measures dispersion of observations. |
| CLT | sample mean approximately normal when n is large | Applies to sample mean, not to raw observations. |
| z confidence interval | `xbar +/- z_(alpha/2)sigma/sqrt(n)` | Use when population sigma is known or problem explicitly gives z conditions. |
| t confidence interval | `xbar +/- t_(alpha/2,n-1)s/sqrt(n)` | Use when sigma is unknown and sample standard deviation estimates it. |
| Required sample size | `n=(z sigma / E)^2` | Margin of error falls with square root of sample size. |
| Hypothesis-test flow | State H0/H1 -> select statistic/distribution -> alpha -> decision rule -> compute -> reject/fail to reject | Never write "accept H0". Interpret statistical and economic significance separately. |
| Type I / Type II / power | Type I = reject true H0 = alpha; Type II = fail to reject false H0 = beta; power = `1-beta` | Lower alpha makes rejection harder and may increase beta. |
| Pooled two-sample t | `s_p^2=[(n1-1)s1^2+(n2-1)s2^2]/(n1+n2-2)`; `t=(xbar1-xbar2-d0)/(s_p sqrt(1/n1+1/n2))` | Independent samples, equal variances assumed. |
| Unequal-variance t | `t=[(xbar1-xbar2)-d0]/sqrt(s1^2/n1+s2^2/n2)` | Do not pool variances. |
| Paired t | `t=dbar/(s_d/sqrt(n))`, df=`n-1` | Same subject before/after or matched pairs. |
| F-test for variances | `F=s1^2/s2^2` | Two population variances; sensitive to normality. |
| Chi-square variance test | `chi^2=(n-1)s^2/sigma0^2`, df=`n-1` | Single population variance; right-skewed distribution. |

### Independence, regression, and ML-risk spine

| Trigger | Formula / Framework | Exam decision |
|---|---|---|
| Correlation test | `t = r sqrt[(n-2)/(1-r^2)]`, df=`n-2` | Tests `H0: rho=0`; same t as simple regression slope test. |
| Spearman rank correlation | rank-based nonparametric correlation | Use for ordinal, nonnormal, or outlier-prone data; detects monotonic relation. |
| Chi-square independence | `chi^2=sum[(O-E)^2/E]`; `E=(row total x column total)/n`; df=`(r-1)(c-1)` | Tests whether categorical variables are independent. It does not show direction or strength. |
| Simple regression equation | `Y_i=b0+b1X_i+e_i` | Slope is expected change in Y for one-unit X change, not automatic causality. |
| OLS coefficients | `b1=Cov(X,Y)/Var(X)`; `b0=ybar-b1xbar` | Intercept may lack economic meaning when X=0 is outside the relevant range. |
| ANOVA and fit | `SST=SSR+SSE`; `R^2=SSR/SST=1-SSE/SST`; `SEE=sqrt[SSE/(n-2)]` | R2 is sample fit, not proof of causation or out-of-sample stability. |
| Regression tests | slope `t=(b1-beta1,0)/SE(b1)`; `F=MSR/MSE`; simple regression `F=t^2` | t tests slope; F tests model fit. |
| Prediction | `Yhat=b0+b1X`; prediction interval is wider than mean-response confidence interval | Prediction interval includes individual error; farther X from xbar makes interval wider. |
| Functional forms | log-lin, lin-log, log-log | Coefficient interpretation changes with logs. |
| ML model risk | overfitting, data snooping, sample bias, look-ahead bias, poor explainability | More complex models need stronger validation, governance, and out-of-sample evidence. |

## 3. Module Atlas 模块地图

| Module | Official module | Page | Primary exam output |
|---|---|---|---|
| M01 | Rates and Returns | [[M01-Rates-and-Returns]] | Return measure selection, MWRR/TWRR, annualization, continuous compounding. |
| M02 | Time Value of Money in Finance | [[M02-Time-Value-of-Money-in-Finance]] | PV/FV, annuities, implied return/growth, cash-flow additivity. |
| M03 | Statistical Measures of Asset Returns | [[M03-Statistical-Measures-of-Asset-Returns]] | Mean/location/dispersion/shape/correlation interpretation. |
| M04 | Probability Trees and Conditional Expectations | [[M04-Probability-Trees-and-Conditional-Expectations]] | EV/variance, probability trees, Bayes updating. |
| M05 | Portfolio Mathematics | [[M05-Portfolio-Mathematics]] | Portfolio variance/covariance/correlation and Roy safety-first. |
| M06 | Simulation Methods | [[M06-Simulation-Methods]] | Lognormal prices, Monte Carlo, bootstrap use and limits. |
| M07 | Estimation and Inference | [[M07-Estimation-and-Inference]] | Sampling design, CLT, SE, bootstrap/jackknife. |
| M08 | Hypothesis Testing | [[M08-Hypothesis-Testing]] | Test construction, Type I/II/power, z/t/F/chi-square selection. |
| M09 | Parametric and Non-Parametric Tests of Independence | [[M09-Parametric-and-Non-Parametric-Tests-of-Independence]] | Pearson/Spearman correlation tests and chi-square independence. |
| M10 | Simple Linear Regression | [[M10-Simple-Linear-Regression]] | OLS, assumptions, ANOVA, coefficient tests, prediction intervals. |
| M11 | Introduction to Big Data Techniques | [[M11-Introduction-to-Big-Data-Techniques]] | Fintech data, AI/ML categories, investment applications, model governance. |

## 4. Curriculum Spine 教材主线

The official 2026 V1 sequence is intentional:

1. **M01-M02: value translation.** Rates, returns, compounding, PV/FV, and cash-flow additivity create the language for valuation.
2. **M03-M05: uncertainty measurement.** Statistical moments, probability trees, Bayes, covariance, correlation, and portfolio variance convert uncertain outcomes into measurable risk.
3. **M06-M07: model and sample uncertainty.** Simulation, bootstrap, sampling design, CLT, and SE explain how estimates are produced and how fragile they are.
4. **M08-M10: evidence discipline.** Hypothesis tests, independence tests, and regression tell whether a sample pattern is statistically meaningful and how it should be interpreted.
5. **M11: data science governance.** Big Data and ML extend the toolkit but increase validation, bias, privacy, and explainability risk.

Textbook anchors are integrated into each module's **Curriculum Spine 教材正文主线**. Use those sections to return to official subsections such as `Money-Weighted and Time-Weighted Return`, `Cash Flow Additivity`, `Bayes' Formula`, `Monte Carlo Simulation`, `The Central Limit Theorem`, `The Process of Hypothesis Testing`, `Tests Concerning Correlation`, `Prediction in the Simple Linear Regression Model`, and `Advanced Analytical Tools`.

## 5. Exam Routes 做题路线

- **Return route**: identify holding period vs multi-period average -> choose HPR/AM/GM/HM -> check cash flows -> choose MWRR/TWRR -> annualize/convert compounding -> interpret.
- **TVM route**: draw timeline -> identify single sum/annuity/perpetuity/growing cash flow/irregular cash flows -> match rate and period -> solve PV/FV/r/g/PMT/n -> apply additivity if cash flows are replicated.
- **Probability route**: list states -> attach probabilities -> compute EV/variance -> use tree if staged -> use Bayes if new information updates prior beliefs.
- **Portfolio route**: calculate expected returns -> calculate covariance/correlation -> build variance with covariance terms -> interpret diversification -> apply safety-first when a threshold return is given.
- **Inference route**: identify estimation vs test -> inspect sampling design -> choose SE and distribution -> run z/t/F/chi-square if required -> conclude reject/fail to reject with economic meaning.
- **Regression route**: name Y and X -> interpret slope/intercept -> check residual assumptions -> read ANOVA/R2/SEE -> test coefficients/F -> predict and explain interval width.
- **ML route**: ask whether labels exist -> choose supervised/unsupervised/reinforcement -> map investment use -> audit data quality, overfitting, sample bias, and explainability.

## 6. Practice & Mock Evidence Map 题库证据地图

| Evidence type | Where it should attach | Decision value |
|---|---|---|
| Official practice miss | Module page `## 5. Practice & Mock Evidence 题库证据` and `.system/events/question/` | Shows which formula or decision route failed. |
| Repeated same `topic + los + error_type` | `.system/memory/patterns/` after threshold | Converts individual misses into pattern mining evidence. |
| Process error, such as rushing p-value language | `.system/events/bias/` and module Trap Ledger | Separates knowledge gap from exam-process bias. |
| Agent explanation error | `.system/events/agent/` and validation memory if misleading | Prevents incorrect formula summaries from becoming study rules. |
| MOC gap, such as missing formula comparison | `.system/memory/strategy/moc-gap-review.md` first | MOC patching should follow review, not automatic pattern mining. |

Current official practice availability from the 2026 textbook index: all Quant modules M01-M11 have textbook practice/solutions anchors available. Local practice pages are outside this Worker Quant write scope, so this MOC only maps evidence destinations and does not rewrite practice assets.

## 7. Review Routes 复习路线

- **Daily quick loop**: MOC Formula Map -> one target module Final Recall Sheet -> 5-10 practice questions -> record any miss as event.
- **Weekly pattern loop**: run `mine-patterns`; check whether errors cluster in return measurement, TVM timelines, probability/Bayes, test selection, regression interpretation, or ML model-risk language.
- **Pre-mock loop**: spend 20 minutes on M01-M02 formulas, 20 minutes on M03-M05 risk/probability, 25 minutes on M07-M10 inference/regression, and 10 minutes on M11 concepts.
- **Post-mock loop**: classify every Quant miss as formula selection, input reading, distribution/test choice, interpretation language, or data/model-governance confusion.
- **Last recall loop**: use each module's `## 7. Final Recall Sheet 最后回忆页`; if a recall item cannot be spoken in one minute, return to that module's Curriculum Spine and Formula Bench.

## 8. Cross-Subject Interfaces 跨科目接口

| Quant output | Downstream subject | Interface risk |
|---|---|---|
| Required return, discount rate, HPR, continuous compounding | Fixed Income, Equity, Derivatives | Coupon/YTM/required return/continuous rate are not interchangeable without matching frequency and definition. |
| PV/FV, annuity, growing perpetuity, cash-flow additivity | Fixed Income, Equity, Corporate Issuers, Derivatives | Valuation errors often start with timing errors, not algebra errors. |
| Mean, variance, covariance, correlation, skew, kurtosis | Portfolio Management, Alternatives, Risk Management | Correlation is linear association, not causation; tail risk needs skew/kurtosis language. |
| EV, probability tree, Bayes | Fixed Income credit, Derivatives payoff, Risk scenarios | Updating probability requires the full denominator, not the attractive numerator. |
| Simulation and bootstrap | Risk Management, Derivatives, Portfolio analytics | Simulation precision does not fix wrong inputs or biased historical samples. |
| CLT, CI, hypothesis tests, p-value | Economics, Equity research, PM performance | Statistical significance is not economic significance; fail to reject is not proof. |
| Regression and ANOVA | Equity, Economics, Portfolio analytics, Big Data | High R2 and significant slope do not prove causality or out-of-sample stability. |
| AI/ML/data governance | Ethics, Quant investing, Risk governance | Data permission, privacy, model explainability, and validation are part of the investment conclusion. |
