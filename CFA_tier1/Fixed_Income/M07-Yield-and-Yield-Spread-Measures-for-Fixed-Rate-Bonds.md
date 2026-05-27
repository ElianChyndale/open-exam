---
title: "M07: Yield and Yield Spread Measures for Fixed-Rate Bonds"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M07"
official_module: "Module 7: Yield and Yield Spread Measures for Fixed-Rate Bonds"
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

# M07: Yield and Yield Spread Measures for Fixed-Rate Bonds

> **Module job**：把 fixed-rate bond 的收益率和利差口径分清：periodicity, annualization, YTM, current yield, YTC/YTP/YTW, benchmark spread, G-spread, I-spread, Z-spread, and OAS。

## 0. Reading Contract 阅读契约

- **Official LOS**：calculate annual yield for varying compounding periods；compare, calculate, and interpret yield and spread measures for fixed-rate bonds。
- **Textbook anchors**：Periodicity and Annualized Yields；Other Yield Measures and Conventions；Bonds with Embedded Options；Yield Spreads over Benchmark Rates；Yield Spreads over Benchmark Yield Curve。
- **Output standard**：每个 yield/spread 必须说清 numerator, benchmark, compounding, and embedded-option treatment。

## 1. Module Brief 模块定位

M07 从 price-yield 扩展到 yield quote and spread quote。考试重点是同一只债可以有多个 yield measures，不同 measure 回答不同问题。

## 2. Curriculum Spine 教材主线

1. **Periodicity**：periodic yield must be annualized consistently。
2. **Other yield measures**：current yield, simple yield, street convention, yield to call/put/worst。
3. **Embedded options**：callable and putable bonds require option-aware interpretation。
4. **Spread measures**：benchmark spread, G-spread, I-spread, Z-spread, OAS。

## 3. Exam Translation 考试翻译

- If yields use different compounding, convert before comparing。
- If callable bond appears, compute or identify yield to call and yield to worst。
- If spread is over one benchmark point, use benchmark spread/G-spread style logic。
- If spread is over full spot curve, think Z-spread；if option-adjusted, think OAS。

## 4. Formula & Decision Bench 公式与决策台

| Measure | Formula / rule | Interpretation |
|---|---|---|
| Effective annual yield | `(1 + periodic rate)^m - 1` | Comparable annual compound yield |
| Current yield | `annual coupon / flat price` | Income only, ignores capital gain/loss |
| Yield to call | IRR to call date and call price | Callable scenario |
| Yield to worst | Lowest yield among valid redemption scenarios | Conservative callable/putable lens |
| Benchmark spread | `bond yield - benchmark yield` | Single benchmark comparison |
| Z-spread | Constant spread added to each spot rate | Curve-wide spread |
| OAS | Z-spread minus option cost | Spread after embedded option adjustment |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2437-eorq-q.xhtml` / `CFA2437-eorq-a.xhtml`。
- **Evidence to capture**：compounding mismatch；current yield used as YTM；YTW direction wrong；Z-spread/OAS confused。
- **Review tag**：`Fixed Income / yield spread measures / fixed-rate bonds`。

## 6. Trap Ledger 陷阱账本

- Higher nominal annual yield may be lower effective yield if compounding differs。
- Current yield ignores redemption value。
- Yield to worst is usually lower, not higher。
- OAS is not just another name for Z-spread; it removes option effect。
- Callable bond spread includes compensation for call risk unless option-adjusted。

## 7. Final Recall Sheet 最终速记

- Convert compounding before compare。
- YTW = worst investor yield among feasible scenarios。
- Z-spread = spot curve + constant spread。
- OAS = option-adjusted spread after separating embedded option value。
