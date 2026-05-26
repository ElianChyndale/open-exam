---
title: "M09 — The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
description: "CFA Level I 2026 official module: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
module: M09
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 9: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M09: The Term Structure of Interest Rates: Spot, Par, and Forward Curves

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: The Term Structure of Interest Rates: Spot, Par, and Forward Curves
- 9.01 | Introduction
- 9.02 | Maturity Structure of Interest Rates and Spot Rates
- 9.03 | Par and Forward Rates
- 9.04 | Spot, Par, and Forward Yield Curves and Interpreting Their Relationship

## Learning Outcome Statements

The candidate should be able to:

- define spot rates and the spot curve, and calculate the price of a bond using spot rates
- define par and forward rates, and calculate par rates, forward rates from spot rates, spot rates from forward rates, and the price of a bond using forward rates
- compare the spot curve, par curve, and forward curve

## Local Study Notes

### Migrated from `CFA_tier1/Fixed_Income/M06-Spot-Par-and-Forward-Curves.md`

_Alignment score: 1.00. Original official module field: Module 9: The Term Structure of Interest Rates: Spot, Par, and Forward Curves._

#### M09: 即期、平价与远期曲线 (Spot, Par, and Forward Curves)

##### 1. 核心知识点

###### 1.1 曲线词典 (Curve Dictionary)

- **核心公式 (English)**
  - 即期定价公式: `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t`
  - 远期利率推导: `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^(n-m)`
  - 平价利率公式: `Par rate = (1 - DF_N)/Σ_{t=1}^{N} DF_t`
- **即期曲线以各期限匹配的即期利率贴现单笔现金流 (spot curve discounts a single cash flow at each maturity)**：即期利率 (spot rate) 是单一期限的零息收益率，每个期限对应一个即期利率。
- **平价曲线给出使债券价格等于面值的票息率 (par curve gives coupon rate making a bond price equal par)**：平价利率 (par rate) 是使债券按面值交易的票息率，用于构建互换曲线等参考基准。
- **远期曲线隐含从当前曲线推算的未来借贷利率 (forward curve implies future borrowing/lending rates from today's curve)**：远期利率 (forward rate) 是当前即期曲线隐含的未来区间利率，反映无套利条件。

###### 1.2 曲线计算 (Curve Calculations)

- **即期定价：每笔现金流使用其期限匹配的即期利率 (spot pricing: each CF gets its maturity-matched spot rate)**：与使用单一 YTM 不同，即期定价将每笔现金流按其到期期限对应的即期利率分别贴现。
- **从即期推导远期；从链式远期推导即期 (forward from spot; spot from chained forwards)**：二者可互为推导。`(1+s_n)^n = (1+s_m)^m x (1+f_{m,n})^(n-m)`。
- **从贴现因子求解平价利率 (par rate solved from discount factors)**：贴现因子 `DF_n = 1/(1+s_n)^n`，平价利率可由贴现因子序列计算得出。

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 即期定价 | `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t` |
| 远期利率 (从即期) | `(1+s_n)^n = (1+s_m)^m x (1+f_{m,n})^(n-m)` |
| 贴现因子 | `DF_t = 1/(1+s_t)^t` |
| 平价利率 | `Par rate_n = (1 - DF_n)/Σ_{t=1}^{n} DF_t` |
| 即期利率 (从远期) | `(1+s_n)^n = (1+f_0,1)(1+f_1,2)...(1+f_{n-1,n})` |

##### 3. 常见考点与解题思路

- **即期曲线折价计算**：给定即期利率序列，计算债券价格。将每期现金流用对应的即期利率贴现后求和。
- **远期利率计算**：给定 `s_1` 和 `s_2`，计算 `f_1,2`。使用公式 `(1+s_2)^2 = (1+s_1)(1+f_1,2)`。
- **从即期构建平价曲线**：利用贴现因子求解各期限的平价利率。
- **比较不同曲线形态**：即期曲线上升（正常）vs 下降（倒挂）对远期利率的影响。上升曲线中远期利率高于即期利率。

##### 4. 易错点提醒

- **远期利率是隐含的无套利利率，非确定性预测 (forward rate is an implied no-arbitrage rate, not a guaranteed forecast)**：远期利率反映了当前市场对未来利率的隐含预期，但并不保证未来实际利率等于远期利率。
- **Spot rate vs YTM 的区别**：YTM 是单一贴现率适用于所有现金流；spot rate 是每期现金流使用匹配期限的贴现率。两者在平坦曲线下相等，但在倾斜曲线下不同。
- **Par rate 不是即期利率**：平价利率是使债券按面值交易的票息率，通常介于即期利率之间。
- **曲线间的关系依赖于无套利假设**：如果市场存在摩擦或套利限制，实际关系可能偏离理论值。

##### 5. 跨模块关联

- Spot/forward 推导 → [[M03-Bond-Valuation]] 的定价框架
- YTM vs spot → [[M04-Yield-and-Spread-Measures]] 的收益率概念
- 远期利率 → [[M07-Interest-Rate-Risk]] 的预期利率路径
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
