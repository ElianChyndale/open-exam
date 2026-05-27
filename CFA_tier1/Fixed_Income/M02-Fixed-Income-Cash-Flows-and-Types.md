---
title: "M02: Fixed-Income Cash Flows and Types"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M02"
official_module: "Module 2: Fixed-Income Cash Flows and Types"
los_count: 2
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M02: Fixed-Income Cash Flows and Types

> **Module job**：把 fixed-income instruments 拆成 cash-flow pattern。考试常让你判断 amortizing, floating, zero-coupon, deferred coupon, callable, putable, convertible 的现金流和风险谁承担。

## 0. Reading Contract 阅读契约

- **Official LOS**：describe common cash flow structures and contrast contingency provisions that benefit issuers and investors；describe legal, regulatory, and tax considerations。
- **Textbook anchors**：Amortizing Debt；Variable Interest Debt；Zero-Coupon Structures；Deferred Coupon Structures；Callable Bonds；Putable Bonds；Convertible Bonds；Legal, Regulatory, and Tax Considerations。
- **Output standard**：每种结构必须能回答 cash flow amount, timing, uncertainty, and beneficiary。

## 1. Module Brief 模块定位

M02 是估值前的现金流地图。后面价格、YTM、duration、credit spread 都依赖你先判断 cash flows are fixed, floating, amortizing, delayed, optional, or equity-linked。

## 2. Curriculum Spine 教材主线

1. **Amortizing debt**：principal repaid over time, reducing outstanding balance。
2. **Variable interest debt**：coupon resets with reference rate, reducing interest-rate price risk after reset。
3. **Zero/deferred structures**：cash flow delayed, increasing discounting sensitivity。
4. **Contingency provisions**：issuer call, investor put, investor conversion。
5. **Legal/tax layer**：issuance and trading may be shaped by regulation, tax status, and jurisdiction。

## 3. Exam Translation 考试翻译

- If cash flows decline with principal repayment, think **amortizing**。
- If coupon resets to market reference, think **FRN** and lower price volatility near reset。
- If coupon is absent or delayed, focus on discount and maturity value。
- If option exists, identify **who chooses** and **who benefits** before choosing yield measure。

## 4. Formula & Decision Bench 公式与决策台

| Structure | Cash-flow implication | Risk implication |
|---|---|---|
| Bullet bond | Coupons then principal at maturity | Higher final principal exposure |
| Fully amortizing | Principal repaid each period | Shorter average life |
| Zero-coupon | No interim coupon | High duration and reinvestment risk absent |
| Deferred coupon | Low/no coupon early, higher later | Higher timing sensitivity |
| Floating-rate | Coupon = reference + margin | Less price sensitivity near reset |
| Callable | Issuer may redeem | Reinvestment risk for investor |
| Putable | Investor may sell back | Downside price support |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2432-eorq-q.xhtml` / `CFA2432-eorq-a.xhtml`。
- **Evidence to capture**：misidentified option beneficiary；ignored amortization；treated FRN coupon as fixed；missed tax/legal language。
- **Review tag**：`Fixed Income / cash-flow structure / contingency provisions`。

## 6. Trap Ledger 陷阱账本

- Floating coupon does not mean no credit risk。
- Callable bond is not investor-friendly just because investor receives call price。
- Zero-coupon has no reinvestment income, but high price sensitivity。
- Amortizing principal changes both price and duration intuition。

## 7. Final Recall Sheet 最终速记

- Cash-flow first, yield second。
- Call = issuer option；Put/convert = investor option。
- FRN resets coupon; credit spread can still move price。
- Amortization shortens effective exposure relative to final maturity。
