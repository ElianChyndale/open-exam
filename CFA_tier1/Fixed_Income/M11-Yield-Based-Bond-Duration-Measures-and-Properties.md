---
title: "M11: Yield-Based Bond Duration Measures and Properties"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M11"
official_module: "Module 11: Yield-Based Bond Duration Measures and Properties"
los_count: 2
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M11: Yield-Based Bond Duration Measures and Properties

> **Module job**：把 Macaulay duration 转成 yield-based price sensitivity: modified duration, approximate modified duration, money duration, and PVBP。

## 0. Reading Contract 阅读契约

- **Official LOS**：define, calculate, and interpret modified duration, money duration, and PVBP；explain how maturity, coupon, and yield level affect interest rate risk。
- **Textbook anchors**：Modified Duration；Approximate Modified Duration；Money Duration and PVBP；Yield Duration of Zero-Coupon and Perpetual Bonds；Duration of FRNs and Loans；Properties of Duration。
- **Output standard**：能把 percent price sensitivity and currency price sensitivity 分清。

## 1. Module Brief 模块定位

M11 是 price-yield sensitivity 的核心。它默认 yield curve 平行移动 and cash flows fixed，因此主要适合 option-free fixed-rate bonds。

## 2. Curriculum Spine 教材主线

1. **Modified duration**：percentage price change for a small yield change。
2. **Approximate modified duration**：uses prices when yield increases/decreases。
3. **Money duration / PVBP**：translate percentage sensitivity into currency amount。
4. **Duration drivers**：longer maturity, lower coupon, lower yield usually increase duration。
5. **Special cases**：zero-coupon duration close to maturity; FRN duration low near reset。

## 3. Exam Translation 考试翻译

- If asked percentage price change, use modified duration。
- If asked currency value per bp, use PVBP。
- If price after yield move, apply `-% duration x Δy` approximation。
- If comparing bonds, rank by maturity, coupon, yield, and embedded option/cash-flow structure。

## 4. Formula & Decision Bench 公式与决策台

| Measure | Formula / rule |
|---|---|
| Modified duration | `MacDur / (1 + YTM/m)` |
| Approx modified duration | `(PV_minus - PV_plus) / (2 x Δy x PV_0)` |
| Estimated % price change | `-ModDur x Δy` |
| Money duration | `ModDur x full price` |
| PVBP | `ModDur x full price x 0.0001` |
| Duration up when | maturity longer, coupon lower, yield lower, fewer interim cash flows |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2441-eorq-q.xhtml` / `CFA2441-eorq-a.xhtml`。
- **Evidence to capture**：basis point conversion error；sign error；money duration confused with modified duration；driver ranking reversed。
- **Review tag**：`Fixed Income / duration / yield-based measures`。

## 6. Trap Ledger 陷阱账本

- Duration estimate has negative sign for price-yield relation。
- PVBP is currency price change for 1 bp, not percentage。
- Modified duration assumes small yield changes and fixed cash flows。
- Higher coupon usually lowers duration because cash flows arrive earlier。

## 7. Final Recall Sheet 最终速记

- ModDur = percent sensitivity。
- Money duration/PVBP = currency sensitivity。
- `1 bp = 0.0001`。
- Longer maturity, lower coupon, lower yield -> higher duration。
