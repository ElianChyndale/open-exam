---
title: "M06 — Fixed-Income Bond Valuation: Prices and Yields"
description: "CFA Level I 2026 official module: Fixed-Income Bond Valuation: Prices and Yields"
module: M06
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 6: Fixed-Income Bond Valuation: Prices and Yields"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M06: Fixed-Income Bond Valuation: Prices and Yields

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Fixed-Income Bond Valuation: Prices and Yields
- 6.01 | Introduction
- 6.02 | Bond Pricing and the Time Value of Money
- 6.03 | Relationships between Bond Prices and Bond Features
- 6.04 | Matrix Pricing

## Learning Outcome Statements

The candidate should be able to:

- calculate a bond’s price given a yield-to-maturity on or between coupon dates
- identify the relationships among a bond’s price, coupon rate, maturity, and yield-to-maturity
- describe matrix pricing

## Local Study Notes

### Migrated from `CFA_tier1/Fixed_Income/M03-Bond-Valuation.md`

_Alignment score: 1.00. Original official module field: Module 6: Fixed-Income Bond Valuation: Prices and Yields._

#### M06: 债券估值：价格与收益率 (Bond Valuation: Prices and Yields)

##### 1. 核心知识点

###### 1.1 定价引擎 (Pricing Engine)

- **核心公式 (English)**
  - 债券定价公式: `P = Σ C/(1+y/m)^t + FV/(1+y/m)^N`
  - 全价公式: `Full Price = Clean Price + Accrued Interest`
- **债券价值 = 票息现值 + 本金现值 (bond value = coupon PV + principal PV)**：债券价格等于所有未来现金流（票息+本金）按到期收益率 (YTM) 贴现的现值之和。
- **折价/溢价/平价与票息率及 YTM 的关系 (discount/premium/par relation to coupon rate and YTM)**：票息率 > YTM → 溢价 (premium)；票息率 = YTM → 平价 (par)；票息率 < YTM → 折价 (discount)。
- **期限越长、票息越低 -> 价格对收益率变动越敏感 (longer maturity + lower coupon -> price more sensitive to yield change)**：零息债券对利率变动最敏感。

###### 1.2 交易价格惯例 (Trading Price Conventions)

- **全价 = 净价 + 应计利息 (full price = clean price + accrued interest)【考试核心】**：报价时通常使用净价 (clean price)，但实际交易结算使用全价 (full price / dirty price)。
- **票息日间定价使用分数期处理 (between-coupon-date pricing uses fractional period handling)**：在两个票息日之间交易时，需将贴现期调整为分数期（如 0.5 年、0.75 年）。
- **矩阵定价估算非流动性债券的收益率/价格 (matrix pricing estimates yield/price for illiquid bonds)**：对于不活跃交易的债券，利用相似债券（相同信用评级、相近期限）的价格来估算其合理收益率或价格。

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 债券定价 | `P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N` |
| 全价 | `Full Price = Clean Price + Accrued Interest` |
| 应计利息 | `AI = 每期票息 x 上次付息至今天数 / 付息周期天数` |

##### 3. 常见考点与解题思路

- **计算应计利息 (AI)**：先计算上次付息日至结算日的天数占比，再乘以每期票息金额。
- **计算 full price**：先按照票息日定价公计算现值，再复利至结算日（或计算 AI 加到 clean price 上）。
- **判断 premium/discount/par**：比较 coupon rate 与 YTM 的大小，不必精确计算。
- **矩阵定价计算**：利用可比债券的 YTM 估算目标债券的价格。

##### 4. 易错点提醒

- **Quoted clean price 是报价习惯，不是买方最终现金支付【考试陷阱】**：实际结算时买方支付的是 full price（clean price + AI）。
- **Day-count convention 因市场而异**：国债通常用 actual/actual，公司债常用 30/360。计算 AI 时必须先确认 day-count 规则。
- **Fractional period 处理容易出错**：在票息日间定价时，可先将未来现金流贴现至上一个票息日，再复利至结算日。
- **CFA 考试中注意区分不同市场的报价惯例**：美国国债、欧洲债券、公司债的报价方式不同。

##### 5. 跨模块关联

- 定价方法 → [[M04-Yield-and-Spread-Measures]] 的 YTM 计算
- 应计利息 → 与 day-count convention 紧密结合
- 矩阵定价 → [[M02-Issuance-and-Trading]] 的流动性概念
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
