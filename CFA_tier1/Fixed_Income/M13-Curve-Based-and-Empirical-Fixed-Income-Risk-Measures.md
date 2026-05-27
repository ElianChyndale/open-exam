---
title: "M13: Curve-Based and Empirical Fixed-Income Risk Measures"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M13"
official_module: "Module 13: Curve-Based and Empirical Fixed-Income Risk Measures"
los_count: 4
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M13: Curve-Based and Empirical Fixed-Income Risk Measures

> **Module job**：从 yield-based risk 进阶到 curve-based and empirical risk。核心是 effective duration/convexity for embedded options, key rate duration for non-parallel curve moves, empirical duration for observed market behavior。

## 0. Reading Contract 阅读契约

- **Official LOS**：explain why effective duration/convexity suit embedded-option bonds；calculate price change using effective duration/convexity；define key rate duration；describe empirical vs analytical duration。
- **Textbook anchors**：Curve-Based Interest Rate Risk Measures；Bond Risk and Return Using Curve-Based Duration and Convexity；Key Rate Duration；Empirical Duration。
- **Output standard**：看到 embedded option or benchmark curve shift, 不再机械套 modified duration。

## 1. Module Brief 模块定位

M13 修正 M11-M12 的限制。Yield-based measures assume fixed cash flows; option bonds need effective measures because cash flows can change when rates move。

## 2. Curriculum Spine 教材主线

1. **Effective duration**：price sensitivity to benchmark curve shift, including cash-flow changes。
2. **Effective convexity**：curve-based second-order sensitivity。
3. **Key rate duration**：sensitivity to a specific maturity point on the curve。
4. **Empirical duration**：estimated from observed price and rate changes。

## 3. Exam Translation 考试翻译

- If bond has embedded option, use effective duration/convexity。
- If yield curve shift is non-parallel, use key rate duration language。
- If observed historical behavior is mentioned, think empirical duration。
- If asked price effect from benchmark shift, apply effective duration and convexity。

## 4. Formula & Decision Bench 公式与决策台

| Measure | Formula / rule |
|---|---|
| Effective duration | `(PV_minus - PV_plus) / (2 x Δcurve x PV_0)` |
| Effective convexity | `(PV_minus + PV_plus - 2PV_0) / ((Δcurve)^2 x PV_0)` |
| Effective price change | `-EffDur x Δcurve + 0.5 x EffConv x (Δcurve)^2` |
| Key rate duration | Sensitivity to one maturity node, holding other nodes constant |
| Sum of KRDs | Approximates duration for a parallel shift |
| Empirical duration | Estimated from actual price/yield observations |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2443-eorq-q.xhtml` / `CFA2443-eorq-a.xhtml`。
- **Evidence to capture**：modified duration used for callable bond；key-rate vs parallel shift confused；empirical treated as model formula only。
- **Review tag**：`Fixed Income / curve-based risk / effective duration`。

## 6. Trap Ledger 陷阱账本

- Effective duration is option-aware; modified duration is yield-based。
- Key rate duration is about curve shape, not just total rate level。
- Empirical duration can differ from analytical duration because markets move with changing spreads, options, and behavior。
- For callable bonds, upside price gain may be capped as rates fall。

## 7. Final Recall Sheet 最终速记

- Embedded option -> effective duration。
- Non-parallel curve -> key rate duration。
- Observed market behavior -> empirical duration。
- Effective measures use `PV_minus`, `PV_plus`, and benchmark curve shifts。
