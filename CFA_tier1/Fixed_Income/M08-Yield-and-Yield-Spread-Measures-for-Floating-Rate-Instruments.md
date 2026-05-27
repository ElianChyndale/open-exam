---
title: "M08: Yield and Yield Spread Measures for Floating-Rate Instruments"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M08"
official_module: "Module 8: Yield and Yield Spread Measures for Floating-Rate Instruments"
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

# M08: Yield and Yield Spread Measures for Floating-Rate Instruments

> **Module job**：处理 FRN spread measures and money market yield conventions。重点是 quoted margin, required margin, discount margin, and money-market denominator/day-count differences。

## 0. Reading Contract 阅读契约

- **Official LOS**：calculate and interpret yield spread measures for floating-rate instruments；calculate and interpret yield measures for money market instruments。
- **Textbook anchors**：Yield and Yield Spread Measures for Floating-Rate Notes；Yield Measures for Money Market Instruments。
- **Output standard**：FRN 题先分 coupon reset logic；money-market 题先分 price/par denominator and 360/365 day count。

## 1. Module Brief 模块定位

M08 把 fixed-rate yield language 转成 floating and short-term instrument language。FRN price near par is conditional on required margin matching quoted margin, not a universal law。

## 2. Curriculum Spine 教材主线

1. **FRN coupon**：reference rate + quoted margin。
2. **Required margin / discount margin**：market-required compensation over reference rate。
3. **FRN price**：required margin > quoted margin -> price below par；required margin < quoted margin -> price above par。
4. **Money-market yields**：BDY, HPY, money market yield, effective annual yield。

## 3. Exam Translation 考试翻译

- If FRN price differs from par, compare quoted margin and required margin。
- If asked discount margin, solve margin that prices FRN at observed price。
- If asked money-market yield, inspect whether discount is divided by par or price。
- If asked annualization, check 360 vs 365 and simple vs compound。

## 4. Formula & Decision Bench 公式与决策台

| Measure | Formula / rule | Key trap |
|---|---|---|
| FRN coupon | `reference rate + quoted margin` | Coupon resets, margin fixed |
| FRN price relation | quoted margin vs required margin | Required > quoted means below par |
| Bank discount yield | `(D / F) x (360 / t)` | Denominator is face value |
| Holding period yield | `(P1 - P0 + income) / P0` | Period return, not annual by itself |
| Money market yield | `HPY x 360 / t` | Denominator is price via HPY |
| Effective annual yield | `(1 + HPY)^(365/t) - 1` | Compounded annual rate |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2438-eorq-q.xhtml` / `CFA2438-eorq-a.xhtml`。
- **Evidence to capture**：BDY denominator error；360/365 mistake；quoted vs required margin reversed；FRN assumed always par。
- **Review tag**：`Fixed Income / floating-rate and money market yields`。

## 6. Trap Ledger 陷阱账本

- BDY uses face value, making it lower than price-denominator yields for discount instruments。
- FRN has low interest-rate reset risk, but not no credit spread risk。
- Quoted margin is contractual; required margin is market-driven。
- Effective annual yield compounds; money market yield is simple annualization。

## 7. Final Recall Sheet 最终速记

- FRN coupon = reference + quoted margin。
- Price below par when required margin exceeds quoted margin。
- Money-market questions = denominator + day count + compounding。
- BDY uses discount over face value。
