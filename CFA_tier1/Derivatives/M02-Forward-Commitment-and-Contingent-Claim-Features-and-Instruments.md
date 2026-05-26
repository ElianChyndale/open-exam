---
title: "M02 — Forward Commitment and Contingent Claim Features and Instruments"
description: "CFA Level I 2026 official module: Forward Commitment and Contingent Claim Features and Instruments"
module: M02
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 2: Forward Commitment and Contingent Claim Features and Instruments"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M02: Forward Commitment and Contingent Claim Features and Instruments

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Forward Commitment and Contingent Claim Features and Instruments
- 2.01 | Introduction
- 2.02 | Forwards, Futures, and Swaps
- 2.03 | Futures
- 2.04 | Swaps
- 2.05 | Options
- 2.06 | Credit Derivatives
- 2.07 | Forward Commitments vs. Contingent Claims

## Learning Outcome Statements

The candidate should be able to:

- define forward contracts, futures contracts, swaps, options (calls and puts), and credit derivatives and compare their basic characteristics
- determine the value at expiration and profit from a long or a short position in a call or put option
- contrast forward commitments with contingent claims

## Local Study Notes

### Migrated from `CFA_tier1/Derivatives/M02-Forward-Commitments-and-Contingent-Claims.md`

_Alignment score: 0.58. Original official module field: Forward Commitment and Contingent Claim Features and Instruments._

#### M02: 远期承诺与或有索取权 (Forward Commitments and Contingent Claims)

##### 1. 核心知识点

**远期承诺 (Forward Commitments)** —— 双方均有义务在未来执行交易 (both parties obligated to transact in the future)

| 合约类型 | 特征 | 交易场所 |
|---------|------|---------|
| 远期合约 (Forward) | 定制化、到期一次结算 (customized, single settlement at maturity) | OTC |
| 期货 (Futures) | 标准化、每日盯市结算 (standardized, daily marking-to-market) | 交易所 |
| 互换 (Swap) | 一系列类似远期的现金流交换 (series of forward-like exchanges) | OTC |

**或有索取权 (Contingent Claims)** —— 持有人有权利但无义务 (holder has right but no obligation)

- **看涨期权 (Call)**：赋予买入权利 (right to buy)
- **看跌期权 (Put)**：赋予卖出权利 (right to sell)
- **期权卖方 (Writer)**：承担或有义务，收取权利金 (bears contingent obligation, receives premium)
- **信用衍生品及其他**：仅在触发条件下支付 (pay only if trigger/state occurs)

##### 2. 关键公式

该模块以概念为主，核心区别在于：

```
远期承诺 payoff = 标的资产价格变化 x 合约规模  (双边义务)
或有索取权 payoff = max(0, 标的资产价格 - 行权价) 或 max(0, 行权价 - 标的资产价格)  (单边权利)
```

##### 3. 常见考点与解题思路

- **权利 vs 义务 (Right vs Obligation)**：这是每道 payoff 题的第一步判断 (the first fork before every payoff question)
- **远期 vs 期货**：同样锁定未来价格，但期货有每日结算和保证金
- **互换本质**：一系列远期合约的组合 (strip of forwards)

##### 4. 易错点提醒

- long forward 和 long call 不一样 —— 一个是义务 (obligation)，一个是权利 (right)
- 期权持有人不一定会行权，只有经济上有利时才行权
- 互换的名义本金通常不交换，只在利率互换中作为计算利息的基数

##### 5. 跨模块关联

- [[M01-Instruments-and-Markets]]：市场结构是合约分类的基础
- [[M05-Forward-and-Futures-Pricing]]：远期和期货的定价估值
- [[M06-Swap-Pricing]]：互换定价与估值
- [[M07-Options-and-Put-Call-Parity]]：期权的深入定价
- [[M00-Derivatives-MOC]]：返回科目总览
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
