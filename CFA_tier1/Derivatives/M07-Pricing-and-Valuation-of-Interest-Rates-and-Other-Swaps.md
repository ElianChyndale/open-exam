---
title: "M07 — Pricing and Valuation of Interest Rates and Other Swaps"
description: "CFA Level I 2026 official module: Pricing and Valuation of Interest Rates and Other Swaps"
module: M07
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 7: Pricing and Valuation of Interest Rates and Other Swaps"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M07: Pricing and Valuation of Interest Rates and Other Swaps

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Pricing and Valuation of Interest Rates and Other Swaps
- 7.01 | Introduction
- 7.02 | Swaps vs. Forwards
- 7.03 | Swap Values and Prices

## Learning Outcome Statements

The candidate should be able to:

- describe how swap contracts are similar to but different from a series of forward contracts
- contrast the value and price of swaps

## Local Study Notes

### Migrated from `CFA_tier1/Derivatives/M06-Swap-Pricing.md`

_Alignment score: 0.43. Original official module field: Pricing and Valuation of Interest Rates and Other Swaps._

#### M06: 互换定价与估值 (Swap Pricing and Valuation)

##### 1. 核心知识点

**互换结构 (Swap Anatomy)**

- **固定换浮动利率互换 (Fixed-for-Floating IRS)**：交换净利息现金流，不交换名义本金 (exchanges net interest cash flows; notional is not exchanged)
- **货币互换 (Currency Swap)**：本金和票息可能在期初和期末交换 (may exchange principal and coupon currencies at inception and maturity)
- **初始固定利率设定**：使互换起始价值约等于零 (initial fixed rate chosen so inception value is approximately zero)

**核心公式**
```
互换净支付 = 名义本金 x (浮动利率 - 固定利率) x 计息因子
Net swap payment = Notional x (Floating rate - Fixed rate) x accrual factor
```

**估值直觉 (Valuation Intuition)**

| 视角 | 描述 |
|------|------|
| 债券对 (Bond Pair) | 互换 = 固定利率债券多头 + 浮动利率债券空头 (或反之) |
| 远期利率协议组合 (FRA Strip) | 互换 = 一系列远期利率协议的组合 |
| 价值变化 | 市场互换曲线变动 → 固定端现值变动 → 互换价值变化 |

- **支付方 (Payer)**：支付固定利率，接收浮动利率
- **接收方 (Receiver)**：接收固定利率，支付浮动利率

##### 2. 关键公式

```
Net swap payment = Notional x (Floating rate - Fixed rate) x (days/period)

Value to payer = PV(fixed leg) - PV(floating leg)   [通常浮动端约等于名义本金]
Value to receiver = - Value to payer
```

##### 3. 常见考点与解题思路

1. **定性题**：区分 interest rate swap vs currency swap（是否交换本金）
2. **计算题**：计算某一期净支付金额（注意 accrual factor）
3. **估值题**：用 bond pair 或 FRA strip 方法计算互换价值变动
4. **方向题**：payer 在利率上升时受益还是受损？（payer 支付固定，利率上升时浮动端支付增加，payer 受损）

##### 4. 易错点提醒

- 名义本金 (notional) 在普通利率互换中**不交换**，仅作为计算利息的基数 (notional is reference amount, not exchanged principal)
- Payer vs Receiver 的方向：**payer 支付固定利率**，利率上升时 payer 价值下降
- 互换不创造全新收益，本质是**交换现金流暴露**
- 初始互换价值为零，但存续期价值可正可负

##### 5. 跨模块关联

- [[M02-Forward-Commitments-and-Contingent-Claims]]：互换是远期承诺的一种
- [[M05-Forward-and-Futures-Pricing]]：FRA strip 视角连接远期定价
- [[M00-Derivatives-MOC]]：返回科目总览
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
