---
title: "M10: Interest Rate Risk and Return"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M10"
official_module: "Module 10: Interest Rate Risk and Return"
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

# M10: Interest Rate Risk and Return

> **Module job**：把 holding-period return 拆成 coupon income, reinvestment income, and sale price effect，并用 Macaulay duration 判断 price risk vs reinvestment risk。

## 0. Reading Contract 阅读契约

- **Official LOS**：calculate and interpret sources of return；describe relationships among holding period return, Macaulay duration, and investment horizon；define, calculate, and interpret Macaulay duration。
- **Textbook anchors**：Sources of Return from Investing in a Fixed-Rate Bond；Investment Horizon and Interest Rate Risk；Macaulay Duration。
- **Output standard**：能解释为什么同样的 rate change 对不同 horizon 的 investor 影响不同。

## 1. Module Brief 模块定位

M10 把价格静态估值转成 holding-period outcome。核心是 interest rate risk has two sides: price risk and reinvestment risk。

## 2. Curriculum Spine 教材主线

1. **Sources of return**：coupon income, reinvestment income, capital gain/loss from sale price。
2. **Investment horizon**：short horizon cares more about price risk; long horizon cares more about reinvestment risk。
3. **Macaulay duration**：weighted average time to receive cash flows。
4. **Immunization intuition**：when horizon equals Macaulay duration, price and reinvestment effects offset more closely for small parallel shifts。

## 3. Exam Translation 考试翻译

- If holding period < Macaulay duration, rising rates usually hurt because price loss dominates。
- If holding period > Macaulay duration, rising rates may help because reinvestment gain dominates。
- If asked Macaulay duration, compute PV-weighted time of cash flows。
- If asked return source, separate coupon, reinvestment, and ending price。

## 4. Formula & Decision Bench 公式与决策台

| Item | Formula / rule |
|---|---|
| Holding period return | `(ending value + interim cash flows - beginning price) / beginning price` |
| Sources of return | coupon income + reinvestment income + price change |
| Macaulay duration | `sum(t x PV(CF_t)) / full price` |
| Horizon < MacDur | Price risk dominates |
| Horizon > MacDur | Reinvestment risk dominates |
| Horizon ≈ MacDur | Offset intuition, not perfect guarantee |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2440-eorq-q.xhtml` / `CFA2440-eorq-a.xhtml`。
- **Evidence to capture**：horizon vs duration relation reversed；ignored reinvestment income；used modified duration when Macaulay was asked。
- **Review tag**：`Fixed Income / interest rate risk and return / Macaulay duration`。

## 6. Trap Ledger 陷阱账本

- Macaulay duration is time-weighted PV average, not price sensitivity directly。
- Rising rates are not always bad for long-horizon investors。
- Holding-period return includes reinvested coupons and ending price。
- Duration matching intuition assumes small, parallel shifts and no default/option disruption。

## 7. Final Recall Sheet 最终速记

- HPR = income + reinvestment + price change。
- MacDur = weighted average cash-flow timing。
- Horizon < MacDur: price risk dominates。
- Horizon > MacDur: reinvestment risk dominates。
