---
title: "M06: Fixed-Income Bond Valuation: Prices and Yields"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M06"
official_module: "Module 6: Fixed-Income Bond Valuation: Prices and Yields"
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

# M06: Fixed-Income Bond Valuation: Prices and Yields

> **Module job**：把 promised cash flows discounted at market discount rate 变成 full price，再按 accrued interest 拆成 flat price；同时理解 price, coupon, maturity, and YTM 的关系。

## 0. Reading Contract 阅读契约

- **Official LOS**：calculate price given YTM on or between coupon dates；identify relationships among price, coupon, maturity, and YTM；describe matrix pricing。
- **Textbook anchors**：Bond Pricing with a Market Discount Rate；Yield-to-Maturity；Flat Price, Accrued Interest, Full Price；Inverse Relationship；Coupon Effect；Maturity Effect；Constant-Yield Price Trajectory；Convexity Effect；Matrix Pricing。
- **Output standard**：能在题目中先区分 full price vs flat price, then solve or interpret YTM。

## 1. Module Brief 模块定位

M06 是 fixed income 计算中枢。之后的 spread, spot curve, duration, convexity 都以 price-yield relation 为基础。最重要的是口径：discount rate period, coupon frequency, settlement date, accrued interest。

## 2. Curriculum Spine 教材主线

1. **Pricing engine**：PV all promised cash flows using required yield。
2. **YTM**：single IRR that equates price to promised cash flows。
3. **Full/flat price**：dirty/full includes accrued interest; clean/flat excludes accrued interest。
4. **Price relationships**：price and yield move inversely; lower coupon/longer maturity often more sensitive。
5. **Matrix pricing**：estimate yield/price from comparable bonds when no active quote exists。

## 3. Exam Translation 考试翻译

- If settlement is coupon date, calculate standard PV。
- If settlement is between coupon dates, calculate full price first, then subtract accrued interest for flat price。
- If price is above par, coupon rate > YTM；if below par, coupon rate < YTM。
- If asked matrix pricing, interpolate comparable bond yields/spreads before pricing。

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use |
|---|---|
| `Full price = sum CF_t / (1 + r)^t` | Base pricing engine |
| `Flat price = Full price - Accrued interest` | Quoted clean price |
| `AI = coupon x days since last coupon / days in coupon period` | Between coupon dates |
| `YTM = IRR of promised CFs` | Yield solving |
| Premium bond | Coupon rate > YTM, price moves toward par over time if yield unchanged |
| Discount bond | Coupon rate < YTM, price moves toward par over time if yield unchanged |
| Matrix pricing | Comparable yields/spreads -> estimated required yield -> price |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2436-eorq-q.xhtml` / `CFA2436-eorq-a.xhtml`。
- **Evidence to capture**：full/flat reversed；AI omitted；coupon frequency wrong；premium/discount relation reversed；matrix interpolation mistake。
- **Review tag**：`Fixed Income / bond valuation / price-yield`。

## 6. Trap Ledger 陷阱账本

- Quoted price is usually flat price, not full price。
- YTM is not realized return unless assumptions hold。
- Higher coupon usually means lower duration, not necessarily better investment。
- Maturity effect is strongest for low coupon and low yield bonds。
- Matrix pricing is estimation from comparables, not an exact market quote。

## 7. Final Recall Sheet 最终速记

- Price = PV cash flows；YTM = IRR。
- Full = flat + accrued。
- Premium: coupon > YTM；Discount: coupon < YTM。
- Yield up, price down; convexity makes the curve bent, not linear。
