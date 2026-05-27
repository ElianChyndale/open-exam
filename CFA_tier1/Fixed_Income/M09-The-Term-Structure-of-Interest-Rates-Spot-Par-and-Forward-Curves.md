---
title: "M09: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M09"
official_module: "Module 9: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M09: The Term Structure of Interest Rates: Spot, Par, and Forward Curves

> **Module job**：把一条 yield curve 拆成 spot, par, and forward 三种语言。考试要你知道哪个 curve 用来 price cash flows, 哪个 curve 是 par coupon, 哪个 curve 是 implied future rate。

## 0. Reading Contract 阅读契约

- **Official LOS**：define spot rates and price a bond using spot rates；define par and forward rates and calculate among par, forward, and spot rates；compare spot, par, and forward curves。
- **Textbook anchors**：Maturity Structure and Spot Rates；Bond Pricing Using Spot Rates；Par Rates from Spot Rates；Forward Rates from Spot Rates；Spot Rates from Forward Rates；Curve Comparisons。
- **Output standard**：能从题目 wording 选择 spot pricing, par coupon solving, or forward rate extraction。

## 1. Module Brief 模块定位

M09 是固定收益曲线模块。它把单一 YTM 拆成 maturity-specific discount rates，连接 Quant 的 no-arbitrage and cash-flow additivity。

## 2. Curriculum Spine 教材主线

1. **Spot curve**：zero-coupon rates by maturity。
2. **Bond pricing with spot rates**：each cash flow discounted at matching spot rate。
3. **Par curve**：coupon rates that price bonds at par。
4. **Forward curve**：future rates implied by current spot rates。
5. **Curve interpretation**：upward/downward shape affects relative spot, par, and forward rates。

## 3. Exam Translation 考试翻译

- If pricing coupon bond with spot rates, discount each cash flow separately。
- If solving par rate, set price equal to par and solve coupon。
- If deriving forward rate, connect cumulative spot returns across maturities。
- If comparing curves, upward spot curve usually implies forward rates above spot rates for longer maturities。

## 4. Formula & Decision Bench 公式与决策台

| Task | Formula / rule |
|---|---|
| Spot pricing | `P = sum CF_t / (1 + s_t)^t` |
| Par rate | Coupon rate that makes `P = par` |
| Forward from spots | `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^(n-m)` |
| Spot from forwards | Chain one-period forward rates into cumulative discount rate |
| Bootstrap | Use known short spot rates, solve next spot from coupon bond price |
| Curve role | Spot prices, par quotes at par, forward implies future rates |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2439-eorq-q.xhtml` / `CFA2439-eorq-a.xhtml`。
- **Evidence to capture**：used YTM instead of spot rates；par/spot/forward definitions swapped；forward exponent wrong；bootstrap order wrong。
- **Review tag**：`Fixed Income / term structure / spot par forward`。

## 6. Trap Ledger 陷阱账本

- Spot rate is not coupon bond YTM unless special conditions hold。
- Par curve is not the same as spot curve。
- Forward rate is implied by no-arbitrage, not a guaranteed future spot rate。
- Always match cash-flow date to discount rate maturity。

## 7. Final Recall Sheet 最终速记

- Spot = zero rate；Par = coupon makes price par；Forward = implied future rate。
- Price with spot curve cash flow by cash flow。
- Bootstrap moves from short maturity to long maturity。
