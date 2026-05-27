---
title: "M08: Equity Valuation: Concepts and Basic Tools"
description: "CFA Level I 2026 Equity Investments 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Equity Investments"
topic_area: "Equity"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M08"
official_module: "Module 8: Equity Valuation: Concepts and Basic Tools"
los_count: 13
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Equity
---

# M08: Equity Valuation: Concepts and Basic Tools

## 0. Reading Contract 阅读契约

- **Official scope**: estimated value vs market price, valuation model categories, dividends and repurchases, DDM, FCFE, preferred stock, Gordon growth, multistage DDM, multiples, EV, asset-based valuation.
- **C+ output**: 能选模型、写公式、检查 assumptions、把 intrinsic value 与 market price 比较成 investment conclusion。
- **Evidence anchor**: V5 Module 8, practice and solutions available in the 2026 ePub index.

## 1. Module Brief 模块定位

This is the Equity payoff module. 所有 company/industry/forecast inputs 最终进入 valuation model。考试最常见错误是 D0/D1、r/g、terminal value timing、equity vs enterprise numerator mismatch。

## 2. Curriculum Spine 教材主线

1. Estimated value and market price: overvalued/fairly valued/undervalued.
2. Model categories: present value, multiplier, asset-based.
3. Dividend background: regular, extra, stock dividend, split, reverse split, repurchase, chronology.
4. Present value models: DDM and FCFE.
5. Preferred stock valuation.
6. Gordon growth and multistage DDM.
7. Multiples and comparables.
8. Enterprise value and asset-based valuation.

## 3. Exam Translation 考试转译

- `estimated value > market price` -> undervalued by market; potential buy.
- `stable mature dividend payer` -> Gordon growth can fit.
- `dividends not linked to capacity` -> FCFE may be more appropriate.
- `non-callable, non-convertible preferred` -> perpetuity.
- `peer comparable` -> multiples, but match business/risk/growth/accounting.
- `enterprise value multiple` -> match EV with pre-debt operating measure.

## 4. Formula & Decision Bench 公式与决策台

| Trigger | Formula / Decision rule | Check |
|---|---|---|
| Value-price call | `V > P` undervalued; `V < P` overvalued | State from market's perspective. |
| General DDM | `V0 = sum Dt/(1+r)^t` | Dividends are cash flow to shareholders. |
| FCFE model | `V0 = sum FCFEt/(1+r)^t` | Use cost of equity, not WACC. |
| Preferred stock | `V0 = Dp / rp` | Perpetuity assumption. |
| Gordon growth | `V0 = D1/(r - g)` | `D1 = D0(1+g)` and `r > g`. |
| Implied return | `r = D1/P0 + g` | Constant-growth assumption required. |
| Two-stage DDM | PV of stage-1 dividends + PV of terminal value | Terminal value occurs at start of stable stage, then discount back. |
| P/E fundamentals | justified P/E rises with payout/growth, falls with required return | Use consistent earnings base. |
| Multiples | `P/E`, `P/CF`, `P/S`, `P/B` | Equity price with equity denominator. |
| EV | `EV = market value equity + market value debt - cash/investments` | EV/EBITDA is enterprise-to-pre-debt measure. |
| Asset-based | market value assets - liabilities | Stronger for asset-heavy firms. |

## 5. Practice & Mock Evidence 题库证据

- Expected item types: Gordon growth calculation, preferred stock value, two-stage DDM, model selection, multiples interpretation, EV calculation.
- Review tag: `Equity-M08-valuation`.
- Miss log fields: cash flow type, discount rate, growth rate, timing, numerator/denominator match, conclusion direction.

## 6. Trap Ledger 易错账本

- Gordon uses next dividend `D1`, not current dividend `D0`。
- `r` must be greater than `g`; otherwise Gordon value is invalid。
- FCFE and DDM are equity models discounted at cost of equity。
- Terminal value timing in multistage DDM must be discounted back to today。
- EV includes debt and equity claims and subtracts cash; do not pair EV with net income。

## 7. Final Recall Sheet 终局速记

- Value > price = undervalued.
- Preferred = dividend / required return.
- Gordon = D1 / (r - g).
- Two-stage = interim dividends + discounted terminal value.
- Multiples need comparable firms and matched numerator/denominator.
