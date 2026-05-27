---
title: "M01: Rates and Returns"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M01"
official_module: "Module 1: Rates and Returns"
los_count: 5
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M01: Rates and Returns

## 0. Reading Contract 学习契约

- **Official module**: Module 1: Rates and Returns.
- **Official pages**: Learning Outcomes; 1.01 Introduction; 1.02 Interest Rates and Time Value of Money; 1.03 Rates of Return; 1.04 Money-Weighted and Time-Weighted Return; 1.05 Annualized Return; 1.06 Other Major Return Measures and Their Applications.
- **LOS contract**: interpret interest rates; calculate/interpret return measures; compare MWRR and TWRR; calculate/interpret annualized and continuously compounded returns; calculate/interpret major return measures.
- **Evidence rule**: when a miss comes from return measure choice, record the exact trigger: `HPR`, `arithmetic/geometric/harmonic`, `MWRR/TWRR`, `annualized/continuous`, or `gross/net/leverage/tax`.

## 1. Module Brief 模块定位

This module turns investment performance into standardized return language. 中文上先问“这题到底要衡量什么”：单期持有收益、长期复合增长、投资者现金流体验、经理表现，还是税费杠杆后的实际回报。

The module feeds M02 TVM, Fixed Income yield language, Equity required return, and Portfolio Management performance measurement.

## 2. Curriculum Spine 教材正文主线

1. **Interest Rates and Time Value of Money**: an interest rate can be a required return, discount rate, or opportunity cost. The nominal rate is decomposed into real risk-free rate plus inflation, default, liquidity, maturity, and other premiums.
2. **Rates of Return**: HPR is the base one-period return. Arithmetic mean supports one-period expectation; geometric mean supports multi-period compounding; harmonic mean supports price multiple averages.
3. **Money-Weighted and Time-Weighted Return**: MWRR is IRR and is cash-flow-timing sensitive. TWRR splits the evaluation at external cash flows and links subperiod returns, so it is better for manager performance.
4. **Annualized Return**: period returns convert to annual form with compounding frequency. Continuously compounded returns use logs and are additive over time.
5. **Other Major Return Measures and Their Applications**: gross/net, pre-tax/after-tax, real, and leveraged returns are not interchangeable; order of adjustments matters.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| required return / discount rate / opportunity cost | explain the same interest rate from three perspectives | "This rate compensates time value and risk and is used to discount cash flows." |
| price, beginning value, ending value, dividend | calculate HPR | "The holding-period return is total income plus price change divided by beginning price." |
| average return over one future period | use arithmetic mean | "Best estimate of single-period expected return." |
| long-term compound growth | use geometric mean | "Historical compound wealth growth rate." |
| average P/E or price multiple | use harmonic mean | "Ratio average that limits high-multiple distortion." |
| investor deposits/withdrawals | use MWRR | "Investor experience, affected by cash-flow timing." |
| evaluate portfolio manager | use TWRR | "Manager performance, external cash flow neutralized." |
| continuously compounded | use `ln(1+R)` or `e^r-1` | "Continuous return is additive; ordinary return is multiplicative." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `HPR=(P1-P0+D1)/P0` | one holding period total return | Confirm whether D1 is separate or embedded in ending value. |
| `Gross return=(P1+D1)/P0=1+HPR` | gross wealth relative | Do not subtract trading expense again if price already reflects it. |
| `Arithmetic mean=sum(R_i)/n` | one-period expected return | Not the compound growth rate. |
| `Geometric mean=[prod(1+R_i)]^(1/n)-1` | multi-period compound return | Convert each return to gross return first. |
| `Harmonic mean=n/sum(1/x_i)` | average price multiples | Inputs must be positive ratios. |
| `MWRR: 0=sum(CF_t/(1+r)^t)` | IRR of investor cash flows | Cash-flow signs and timing drive result. |
| `TWRR=prod(1+HP_i)-1` | linked subperiod performance | Split at external cash flows. |
| `Annualized=(1+R_period)^c-1` | convert period to annual return | c is number of periods per year. |
| `r_cc=ln(1+HPR)`; `HPR=e^(r_cc)-1` | continuous/ordinary conversion | Do not mix continuous and periodic rates. |
| `Leveraged return=R_p+(B/E)(R_p-r_D)` | return on equity with borrowing | Calculate after net portfolio return, before tax if tax is given afterward. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available for this module.
- Attach misses here when the wrong answer came from **return measure selection**, not from algebra.
- Evidence tags to use: `return_measure`, `cash_flow_timing`, `annualization`, `continuous_compounding`, `gross_net_tax`, `leverage`.
- Current local page does not contain official question-level evidence; future events should point back to the formula row that failed.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Arithmetic mean used for long-run wealth | Use geometric mean for compound growth. |
| MWRR judged as manager skill | MWRR reflects investor cash-flow timing; TWRR is the manager-performance measure. |
| Gross return reduced by trading expenses again | Trading expenses are already reflected in gross return; net return subtracts management/admin fees. |
| Continuous return annualized like periodic return | Use log/exponential conversion for continuous compounding. |
| Tax applied before leverage | Follow the stated economics; common route is gross -> net -> leverage -> tax. |

## 7. Final Recall Sheet 最后回忆页

- Interest rate = required return = discount rate = opportunity cost, depending on context.
- Nominal rate = real risk-free + inflation + default + liquidity + maturity + other premiums.
- HPR is one-period total return; arithmetic is one-period average; geometric is compound growth; harmonic is ratio average.
- MWRR = IRR, cash-flow sensitive. TWRR = subperiod linked, manager-performance focused.
- Continuous return: `ln(1+R)`; ordinary return from continuous: `e^r-1`.
- Always state the interpretation after the calculation: what return, whose return, over what period, under what fee/tax/leverage convention.
