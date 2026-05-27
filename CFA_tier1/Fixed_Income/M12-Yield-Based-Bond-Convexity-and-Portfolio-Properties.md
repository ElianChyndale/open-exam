---
title: "M12: Yield-Based Bond Convexity and Portfolio Properties"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M12"
official_module: "Module 12: Yield-Based Bond Convexity and Portfolio Properties"
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

# M12: Yield-Based Bond Convexity and Portfolio Properties

> **Module job**：用 convexity 修正 duration 的线性近似，并把单债 duration/convexity 汇总到 portfolio level。

## 0. Reading Contract 阅读契约

- **Official LOS**：calculate and interpret convexity and convexity adjustment；calculate percentage price change using duration and convexity；calculate portfolio duration and convexity and explain limitations。
- **Textbook anchors**：Bond Convexity and Convexity Adjustment；Bond Risk and Return Using Duration and Convexity；Portfolio Duration and Convexity。
- **Output standard**：能在 yield change 较大时同时使用 duration and convexity term。

## 1. Module Brief 模块定位

M12 解释 price-yield curve 为什么不是直线。Duration 给斜率，convexity 给弯曲度；组合层面用 market-value weights 汇总。

## 2. Curriculum Spine 教材主线

1. **Convexity**：second-order sensitivity of price to yield。
2. **Convexity adjustment**：improves duration-only estimate for larger yield changes。
3. **Risk/return estimate**：duration term plus convexity term。
4. **Portfolio measures**：weighted average duration/convexity。
5. **Limitations**：parallel shift, small/regular moves, fixed cash-flow assumptions。

## 3. Exam Translation 考试翻译

- If yield change is not tiny, include convexity。
- If asked price percentage change, use duration term plus half convexity term。
- If asked portfolio duration/convexity, weight by market value。
- If comparing positive convexity, price gains from yield decreases exceed losses from equal yield increases。

## 4. Formula & Decision Bench 公式与决策台

| Measure | Formula / rule |
|---|---|
| Approx convexity | `(PV_minus + PV_plus - 2PV_0) / ((Δy)^2 x PV_0)` |
| Convexity adjustment | `0.5 x Convexity x (Δy)^2` |
| % price change | `-Duration x Δy + 0.5 x Convexity x (Δy)^2` |
| Portfolio duration | `sum(weight_i x duration_i)` |
| Portfolio convexity | `sum(weight_i x convexity_i)` |
| Positive convexity | Helps both up/down rate move approximation relative to duration-only |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2442-eorq-q.xhtml` / `CFA2442-eorq-a.xhtml`。
- **Evidence to capture**：forgot 0.5；used bp instead of decimal yield change；portfolio weights not market value；convexity sign misunderstood。
- **Review tag**：`Fixed Income / convexity / portfolio risk`。

## 6. Trap Ledger 陷阱账本

- Convexity term is usually positive for option-free bonds whether rates rise or fall because `(Δy)^2` is positive。
- Duration-only estimate overstates price loss when yields rise and understates price gain when yields fall for positive convexity bonds。
- Portfolio duration is not a simple arithmetic average unless positions have equal market value。
- Yield-based convexity still assumes parallel yield shift and stable cash flows。

## 7. Final Recall Sheet 最终速记

- Duration = first-order slope；Convexity = second-order bend。
- Use decimal yield change, not bp count。
- `%ΔP ≈ -DΔy + 0.5C(Δy)^2`。
- Portfolio measures use market-value weights。
