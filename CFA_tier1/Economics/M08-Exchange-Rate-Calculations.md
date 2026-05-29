---
title: "M08: Exchange Rate Calculations"
description: "CFA Level I 2026 Economics 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Economics"
topic_area: "Economics"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M08"
official_module: "Module 8: Exchange Rate Calculations"
los_count: 2
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Economics
---

# M08: Exchange Rate Calculations

## 0. Reading Contract 阅读契约

- **Official spine**：Cross-rate calculations, forward-rate calculations, arbitrage relationships, forward discounts and premiums.
- **LOS contract**：calculate and interpret currency cross-rates; calculate and interpret forward rates, forward points and forward premium/discount.
- **Evidence rule**：错题标 `cross_rate`, `bid_ask`, `forward_premium`, `cip`, or `arbitrage_cashflow`。

## 1. Module Brief 模块定位

This is the calculation endpoint of Economics. 本模块所有题都先从 quote convention 开始：如果报价方向写错，cross rate, forward premium and arbitrage 全部会反。

## 2. Curriculum Spine 教材主线

| Spine | English trigger | 中文任务 |
|---|---|---|
| Cross rates | `A/B`, `B/C`, triangular relation | 排列货币使中间货币约掉。 |
| Bid/ask | buy/sell base currency, invert quote | 倒数报价 bid/ask 换边。 |
| Forward rates | spot, forward points, maturity | 计算 forward rate and premium/discount。 |
| Arbitrage relationships | no-arbitrage, CIP | 用利率和 spot 推 forward。 |
| Interpretation | premium, discount, annualized | 区分定价关系与预测。 |

## 3. Exam Translation 考试翻译

1. 每题第一行写 `A/B = 1 A costs B`。
2. Cross rate：把两个报价排成能相乘或相除后留下目标货币。
3. Bid/ask：你要买的货币用 dealer ask；你要卖的货币得到 dealer bid。
4. Forward premium：先确认 `F-S` 是针对 base currency 的 premium/discount。
5. Arbitrage：写现金流，不靠直觉判断。

## 4. Formula & Decision Bench 公式与决策台

| Item | Formula / rule | Use |
|---|---|---|
| Cross rate | `A/C = (A/B) x (B/C)` | Middle currency cancels. |
| Inversion | `B/A = 1/(A/B)` | Bid/ask inversion: bid becomes `1/ask`, ask becomes `1/bid`. |
| Forward points | `F - S` | Positive/negative depends on quote direction. |
| Forward premium / interest rate | `F > S` → base at forward premium → `i_price > i_base` (base has lower rate) | CIP 核心推论：远期升水的货币利率更低。 |
| Annualized premium | `[(F - S) / S] x periods per year` | Match question maturity. |
| Covered interest parity | `F = S x (1+i_price)/(1+i_base)` | No-arbitrage forward. |
| Arbitrage test | quoted F vs CIP F | Borrow low, convert, invest high, lock forward; verify cash flows. |

## 5. Practice & Mock Evidence 题库证据

- Track `quote_first_line_missing` when the solution starts calculating before defining the quote.
- Track `bid_ask_inversion` when inversion fails to swap bid/ask.
- Track `premium_direction` when forward premium is interpreted for the wrong currency.
- Track `cip_domestic_foreign` when domestic/foreign rates are reversed.

## 6. Trap Ledger 陷阱账本

| Trap | Fix rule |
|---|---|
| Forward premium means future appreciation guaranteed | It is no-arbitrage pricing, not a forecast guarantee. |
| Bid/ask can be averaged | Use executable bid/ask; no mid unless question asks. |
| High interest currency has forward premium | Under CIP, high interest currency usually trades at forward discount. Base at forward premium → base has lower rate. |
| Cross rate can be multiplied in any order | Currency units must cancel. |

## 7. Final Recall Sheet 最终回忆单

- Define quote first.
- Cross: arrange units to cancel.
- Invert: bid = `1/ask`, ask = `1/bid`.
- Premium = `(F-S)/S`; annualize by period.
- CIP = `F = S(1+i_price)/(1+i_base)`.
- **Base at forward premium → base has lower interest rate**（F>S → i_price > i_base）。
