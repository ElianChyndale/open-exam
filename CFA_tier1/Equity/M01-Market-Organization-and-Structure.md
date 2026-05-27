---
title: "M01: Market Organization and Structure"
description: "CFA Level I 2026 Equity Investments 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Equity Investments"
topic_area: "Equity"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M01"
official_module: "Module 1: Market Organization and Structure"
los_count: 12
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Equity
---

# M01: Market Organization and Structure

## 0. Reading Contract 阅读契约

- **Official scope**: financial system functions, assets/contracts, intermediaries, positions, leveraged positions, orders, primary/secondary markets, market structures, market quality, regulation.
- **C+ output**: 能把交易机制题转成 `position -> order/market type -> execution/price/liquidity consequence`。
- **Evidence anchor**: V5 Module 1, practice and solutions available in the 2026 ePub index.

## 1. Module Brief 模块定位

本模块解释 price discovery and capital allocation 如何依赖金融系统、交易场所、订单和监管。考试喜欢把定义、方向和公式混在一起：先判断 investor position，再判断 order instruction，最后解释 market quality。

## 2. Curriculum Spine 教材主线

1. Financial system functions: saving, borrowing, raising equity, risk management, spot trading, information trading.
2. Assets and contracts: securities, currencies, commodities, real assets, forwards, futures, swaps, options.
3. Intermediaries: brokers, exchanges, ATS, dealers, arbitrageurs, securitizers, depositories, insurers, custodians.
4. Positions: long, short, leveraged, margin account.
5. Orders: execution instructions, validity instructions, clearing instructions.
6. Markets: primary vs secondary; quote-driven, order-driven, brokered.
7. Quality and regulation: liquidity, transparency, assurity of completion, low costs, investor protection.

## 3. Exam Translation 考试转译

- `market order` -> execution certainty high, price uncertainty high.
- `limit order` -> price protection, execution uncertainty.
- `stop order` -> becomes active after stop price is reached; often used to protect or enter momentum positions.
- `quote-driven` -> dealers provide liquidity from inventory; bid-ask spread compensates risk/cost.
- `order-driven` -> public limit order book; matching and trade pricing rules matter.
- `brokered` -> broker searches counterparty for unique or illiquid assets.

## 4. Formula & Decision Bench 公式与决策台

| Trigger | Formula / Decision rule | Check |
|---|---|---|
| Leverage | `leverage ratio = asset value / equity` | Higher leverage magnifies gains and losses. |
| Long margin return | `(sale proceeds + income - loan repayment - initial equity) / initial equity` | Include borrowing cost if given. |
| Short sale return | `(initial proceeds + margin - repurchase cost - costs) / initial equity` | Price increase hurts short seller. |
| Long margin call | `P = P0(1 - initial margin)/(1 - maintenance margin)` | Below this price triggers call. |
| Short margin call | `P = P0(1 + initial margin)/(1 + maintenance margin)` | Above this price triggers call. |
| Market quality | liquidity + transparency + low costs + assurity + integrity | Do not equate high volume alone with quality. |

## 5. Practice & Mock Evidence 题库证据

- Expected item types: margin call, order selection, market structure identification, primary/secondary market role, regulation objective.
- Review tag: `Equity-M01-market-organization`.
- Miss log fields: position direction, order instruction, price trigger, market structure, quality dimension.

## 6. Trap Ledger 易错账本

- 把 limit order 当成 guaranteed execution；limit only guarantees worst acceptable price if executed。
- Long and short margin call price directions反了：long跌到触发，short涨到触发。
- Primary market sells new securities; secondary market provides liquidity that supports primary issuance。
- Brokered market is not the same as broker acting inside an order-driven exchange。

## 7. Final Recall Sheet 终局速记

- Market order = execution now; limit order = price discipline.
- Quote-driven = dealer quotes; order-driven = order book; brokered = search.
- Good market = liquid, transparent, low-cost, complete, fair.
- Financial system purpose = move capital/risk/information to highest-valued use.
