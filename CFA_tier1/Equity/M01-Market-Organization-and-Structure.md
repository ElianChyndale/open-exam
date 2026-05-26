---
title: "M01 — Market Organization and Structure"
description: "CFA Level I 2026 official module: Market Organization and Structure"
module: M01
subject: "Equity Investments"
topic_area: Equity
curriculum_year: 2026
official_module: "Module 1: Market Organization and Structure"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Equity
  - official_2026
---

# M01: Market Organization and Structure

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Market Organization and Structure
- 1.01 | Introduction
- 1.02 | The Functions of the Financial System
- 1.03 | Assets and Contracts
- 1.04 | Securities
- 1.05 | Currencies, Commodities, and Real Assets
- 1.06 | Contracts
- 1.07 | Financial Intermediaries
- 1.08 | Securitizers, Depository Institutions and Insurance Companies
- 1.09 | Settlement and Custodial Services and Summary
- 1.10 | Positions and Short Positions
- 1.11 | Leveraged Positions
- 1.12 | Orders and Execution Instructions
- 1.13 | Validity Instructions and Clearing Instructions
- 1.14 | Primary Security Markets
- 1.15 | Secondary Security Market and Contract Market Structures
- 1.16 | Well-functioning Financial Systems
- 1.17 | Market Regulation
- 1.18 | Summary

## Learning Outcome Statements

The candidate should be able to:

- explain the main functions of the financial system
- describe classifications of assets and markets
- describe the major types of securities, currencies, contracts, commodities, and real assets that trade in organized markets, including their distinguishing characteristics and major subtypes
- describe types of financial intermediaries and services that they provide
- compare positions an investor can take in an asset
- calculate and interpret the leverage ratio, the rate of return on a margin transaction, and the security price at which the investor would receive a margin call
- compare execution, validity, and clearing instructions
- compare market orders with limit orders
- define primary and secondary markets and explain how secondary markets support primary markets
- describe how securities, contracts, and currencies are traded in quote-driven, order-driven, and brokered markets
- describe characteristics of a well-functioning financial system
- describe objectives of market regulation

## Local Study Notes

### Migrated from `CFA_tier1/Equity/M01-Market-Organization-and-Structure.md`

_Alignment score: 1.00. Original official module field: Module 1: Market Organization and Structure._

#### M01: 市场组织与结构 (Market Organization and Structure)

##### 1. 核心知识点

###### 市场管道 (Market plumbing)
- **初级市场 (primary market)** 筹集资本，公司通过 IPO/SEO 发行新证券；**二级市场 (secondary market)** 转让所有权，投资者之间交易已发行证券
- **做市商 (broker/dealer)**、**拍卖市场 (auction)**、**报价驱动市场 (quote-driven)**、**订单驱动市场 (order-driven)** 四种结构决定价格发现机制
- **流动性维度 (liquidity dimensions)**：**紧度 (tightness)** — 买卖价差大小；**深度 (depth)** — 大额订单对价格的影响；**弹性 (resiliency)** — 价格偏离后恢复速度

###### 订单与交易 (Orders and trading)
- **指令类型 (instruction types)**：**市价单 (market order)** 追求立即执行，**限价单 (limit order)** 控制价格，**止损单 (stop order)** 触发后转为市价单；**执行指令 (execution instructions)** 与**有效期限指令 (validity instructions)** 约束订单行为
- **交易成本 (transaction costs)**：**显性成本 (explicit cost)** 如佣金税费；**隐性成本 (implicit cost)** 如**买卖价差 (bid-ask spread)** 与**价格影响 (price impact)**
- **杠杆与风险 (leverage and risk)**：**保证金买入 (margin purchase)** 与**卖空 (short sale)** 放大收益的同时增加**清算风险 (liquidation risk)**

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 杠杆比率 (Leverage Ratio) | `Value of Position / Investor Equity` |
| 初始保证金率 (Initial Margin) | `Investor Equity / Purchase Value` |
| 保证金追缴价格 (Margin Call Price, Long) | `Loan / [Shares x (1 - Maintenance Margin)]` |
| 卖空收益率 (Short Sale Return) | `(Initial Proceeds - Repurchase Cost - Costs) / Initial Equity` |

##### 3. 常见考点与解题思路

- **区分市场类型**：先判断是一级还是二级市场交易 — IPO 属于一级，二级市场买卖已发行股票
- **保证金计算**：分清 equity 与 loan，用公式 `Margin Call Price = Loan / [Shares × (1 - MM%)]`，注意 maintenance margin 是下限
- **卖空题**：三步走 — 初始保证金存入、卖空所得款项、回购结算

##### 4. 易错点提醒

- **限价单并非更"安全"**：它只控制价格，不保证成交（未成交风险）
- **best price instruction ≠ best execution outcome**：最佳价格指令追求最优报价，但最佳执行结果还考虑速度、隐蔽性等
- **卖空亏损无上限**：股价理论上可以无限上涨，因此卖空风险远大于多头头寸

##### 5. 跨模块关联

- **市场结构影响指数构建** → [[M02-Security-Market-Indexes]]
- **交易成本与流动性影响市场效率** → [[M03-Market-Efficiency]]
- **margin 交易影响资本结构** → [[M05-Company-Analysis-Past-and-Present]]
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
