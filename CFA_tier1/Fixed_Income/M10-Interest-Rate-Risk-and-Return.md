---
title: "M10 — Interest Rate Risk and Return"
description: "CFA Level I 2026 official module: Interest Rate Risk and Return"
module: M10
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 10: Interest Rate Risk and Return"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M10: Interest Rate Risk and Return

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Interest Rate Risk and Return
- 10.01 | Introduction
- 10.02 | Sources of Return from Investing in a Fixed-Rate Bond
- 10.03 | Investment Horizon and Interest Rate Risk
- 10.04 | Macaulay Duration

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret the sources of return from investing in a fixed-rate bond;
- describe the relationships among a bond’s holding period return, its Macaulay duration, and the investment horizon;
- define, calculate, and interpret Macaulay duration.

## Local Study Notes

### Migrated from `CFA_tier1/Fixed_Income/M07-Interest-Rate-Risk.md`

_Alignment score: 1.00. Original official module field: Module 10: Interest Rate Risk and Return._

#### M10: 利率风险与回报 (Interest Rate Risk and Return)

##### 1. 核心知识点

###### 1.1 回报分解 (Return Decomposition)

- **核心公式 (English)**
  - 持有期回报率: `HPR = (coupon + reinvestment income + sale price - purchase price)/purchase price`
  - Macaulay 久期: `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price`
- **票息收入 + 再投资收入 + 价格变动 (coupon income + reinvestment income + price change)**：债券的持有期回报由三部分构成：收到的票息、票息再投资产生的收益、以及卖出时的资本利得/损失。
- **回归面值与持有期效应 (pull to par and horizon effect)**：随着到期日临近，折价债券价格逐渐上升趋近面值（回归面值）；溢价债券价格逐渐下降趋近面值。这一效应独立于利率变化。
- **当卖出收益率或再投资率变化时，已实现回报不同 (realized return differs when sale yield or reinvestment rate changes)**：如果投资者在到期前卖出债券，或市场利率变化导致再投资收入改变，实际实现的持有期回报将不同于 YTM。

###### 1.2 持有期与 Macaulay 久期 (Horizon and Macaulay Duration)

- **投资期限 < Macaulay 久期 -> 价格风险占主导 (investment horizon < Macaulay duration -> price risk dominates)**：久期大于持有期意味着价格风险（利率上升导致价格下跌）超过再投资风险。
- **投资期限 > Macaulay 久期 -> 再投资风险占主导 (investment horizon > Macaulay duration -> reinvestment risk dominates)**：久期小于持有期意味着再投资风险（利率下降导致再投资收益减少）占主导。
- **Macaulay 久期 = 现金流的时间加权平均 (Macaulay duration = weighted average time to cash flows)**：以每期现金流现值为权重，计算现金流回收时间的加权平均。

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 持有期回报率 (HPR) | `HPR = (总票息 + 再投资收入 + 售价 - 买价) / 买价` |
| Macaulay 久期 | `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price` |
| 价格风险 vs 再投资风险 | `Horizon < D_mac → 价格风险主导`；`Horizon > D_mac → 再投资风险主导` |

##### 3. 常见考点与解题思路

- **计算持有期回报**：给定买入价格、卖出价格、票息收入和再投资利率，计算 HPR。注意再投资收入的复利计算。
- **利用 Macaulay 久期判断免疫状态**：若投资者的持有期等于 Macaulay 久期，价格风险与再投资风险大致抵消（利率免疫）。
- **Pull-to-par 效应分析**：给定折价/溢价债券和固定的市场利率，计算到期前某时点的价格。
- **判断利率变化方向对债券持有者回报的影响**：利率下降 → 价格上升但再投资收入减少；利率上升 → 价格下降但再投资收入增加。

##### 4. 易错点提醒

- **Duration 匹配是关于平衡价格和再投资效应，而非冻结价格 (duration matching is about balancing price and reinvestment effects, not freezing price)**：Macaulay 久期匹配使价格效应和再投资效应相互抵消，不等于债券价格不变化。
- **持有期回报 ≠ YTM**：YTM 假设持有至到期且再投资率等于 YTM。如果提前卖出或再投资率不同，实际回报会偏离 YTM。
- **Pull-to-par 速度不是线性的**：折价债券的价格向面值回归的速度随着到期日临近而加快。
- **零息债券没有再投资风险**：因为没有期间现金流，所以再投资风险为零，但价格风险最大。

##### 5. 跨模块关联

- Macaulay 久期 → [[M08-Duration-and-Convexity]] 的修正久期
- 持有期回报 → [[M04-Yield-and-Spread-Measures]] 的 YTM 比较
- 利率风险 → [[M09-Curve-Based-and-Empirical-Risk]] 的 curve-based 风险
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
