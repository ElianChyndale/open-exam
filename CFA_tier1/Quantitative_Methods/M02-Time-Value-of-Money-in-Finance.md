---
title: "M02: Time Value of Money in Finance"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M02"
official_module: "Module 2: Time Value of Money in Finance"
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

# M02: Time Value of Money in Finance

## 0. Reading Contract 学习契约

- **Official module**: Module 2: Time Value of Money in Finance.
- **Official pages**: Learning Outcomes; 2.01 Introduction; 2.02 Time Value of Money in Fixed Income and Equity; 2.03 Implied Return and Growth; 2.04 Cash Flow Additivity.
- **LOS contract**: calculate/interpret PV of fixed-income and equity instruments; calculate/interpret implied return, required return, and implied growth; explain cash-flow additivity and no-arbitrage applications.
- **Evidence rule**: every miss must preserve the cash-flow timeline, rate frequency, and whether the task was valuation or implied-variable solving.

## 1. Module Brief 模块定位

TVM is the valuation grammar. 中文上它不是“按计算器”，而是先把每个现金流放到时间轴上，再决定折现、复利、反求收益率，或者用现金流可加性做无套利复制。

## 2. Curriculum Spine 教材正文主线

1. **Time Value of Money in Fixed Income and Equity**: fixed-income value is coupon annuity plus principal PV; equity value is expected dividends or cash flows discounted to today.
2. **Discount Instruments / Coupon Instruments / Annuity Instruments**: instrument form tells whether the cash flow is single-sum, annuity, or mixed.
3. **Equity Instruments and TVM**: Gordon growth is a growing perpetuity application; required return and growth are linked by price.
4. **Implied Return and Growth**: given PV and cash flows, solve r, YTM, required return, or g.
5. **Cash Flow Additivity**: identical cash-flow packages must have identical value, the basis for no-arbitrage forward rates, forward FX, and option payoff valuation.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| present value of bond | discount each coupon and principal | "Bond value equals coupon annuity PV plus par value PV." |
| stock price with dividend growth | use growing perpetuity | "Value depends on next dividend, required return, and growth." |
| price and cash flows given, rate unknown | solve implied return / IRR / YTM | "The implied return is the rate that equates PV with future cash flows." |
| D1, P0, g | `r=D1/P0+g` | "Required return is dividend yield plus growth." |
| same future cash flows through two packages | apply additivity/no-arbitrage | "Same cash flows must have same price." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `FV=PV(1+r)^n` | single-sum compounding | Match rate period with n. |
| `PV=FV/(1+r)^n` | single-sum discounting | Do not use annual r with monthly n. |
| `FV=PV e^(rt)`; `PV=FV e^(-rt)` | continuous compounding/discounting | Use only for continuous rates. |
| `PV_annuity=A[1-1/(1+r)^n]/r` | ordinary annuity PV | End-of-period cash flow. |
| `FV_annuity=A[(1+r)^n-1]/r` | ordinary annuity FV | End-of-period accumulation. |
| `annuity due = ordinary annuity x (1+r)` | beginning-of-period payments | Rent/premium due at start. |
| `PV_perpetuity=A/r` | level perpetual cash flow | A is the next cash flow. |
| `PV_growing=A1/(r-g)` | growing perpetuity | Requires `r>g`; numerator is `A1` or `D1`. |
| `PV_growing_annuity=[A1/(r-g)][1-((1+g)/(1+r))^n]` | finite growing stream | Check finite vs infinite. |
| `r=D1/P0+g` | implied equity required return | Do not use D0 unless converting to D1. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `timeline_error`, `frequency_mismatch`, `annuity_due`, `growing_perpetuity`, `implied_return`, `cash_flow_additivity`.
- Store a screenshot or typed cash-flow line when recording a miss; most M02 errors are input placement errors before formula errors.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Using `D0` in Gordon formula | Use next dividend `D1`; convert if needed. |
| Treating annuity due as ordinary annuity | Multiply ordinary annuity result by `(1+r)`. |
| Ignoring semiannual or monthly frequency | Adjust both rate and number of periods. |
| Applying one annuity formula to irregular cash flows | Discount each cash flow separately and add. |
| Thinking additivity is optional | It is the no-arbitrage condition for identical cash flows. |

## 7. Final Recall Sheet 最后回忆页

- Draw the timeline first.
- Bond price = coupon annuity PV + principal PV.
- Growing perpetuity: `PV=D1/(r-g)`, with `r>g`.
- Implied return is the discount rate that makes PV equal expected cash flows.
- Additivity: package value equals the sum of component cash-flow values.
