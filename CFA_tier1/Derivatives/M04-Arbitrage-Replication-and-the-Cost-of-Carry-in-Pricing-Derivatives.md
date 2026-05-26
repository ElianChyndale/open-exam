---
title: "M04 — Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
description: "CFA Level I 2026 official module: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
module: M04
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 4: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M04: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives
- 4.01 | Introduction
- 4.02 | Arbitrage
- 4.03 | Replication
- 4.04 | Costs and Benefits Associated with Owning the Underlying

## Learning Outcome Statements

The candidate should be able to:

- explain how the concepts of arbitrage and replication are used in pricing derivatives
- explain the difference between the spot and expected future price of an underlying and the cost of carry associated with holding the underlying asset

## Local Study Notes

### Migrated from `CFA_tier1/Derivatives/M04-Arbitrage-and-Replication.md`

_Alignment score: 0.46. Original official module field: Arbitrage/Replication/Cost of Carry._

#### M04: 套利、复制与持有成本 (Arbitrage, Replication, and Cost of Carry)

##### 1. 核心知识点

**无套利逻辑 (No-Arbitrage Logic)**
- **一价定律 (Law of One Price)**：相同未来现金流的资产应有相同价格 (identical future cash flows must have the same price)
- **复制组合 (Replication Portfolio)**：用现货+融资复制衍生品收益，确定公平价格 (replication portfolio pins fair derivative price)
- **套利行为 (Arbitrage Action)**：错误定价时，套利者交易将价格推回公平关系 (arbitrage pushes mispriced contract back to fair relation)

**持有成本关系 (Carry Relation)**

| 因素 | 对远期价格的影响 |
|------|-----------------|
| 融资成本 (Financing Cost) | 提高远期价格 (raises forward price) |
| 已知收入 (Known Income) | 减少持有成本 (reduces net carry) |
| 收益率/便利收益 (Yield/Convenience) | 减少持有成本 (reduces net carry) |

**关键公式**
- `Forward price = Spot + Carry - Benefit`
- `Carry = Financing cost - Income/Yield/Convenience`

##### 2. 关键公式

无收益资产远期价格：
```
F0(T) = S0(1+r)^T
```

已知收入资产远期价格：
```
F0(T) = [S0 - PV(I)](1+r)^T
```

已知收益率资产远期价格：
```
F0(T) = S0[(1+r)/(1+q)]^T    或连续口径：S0e^((r-q)T)
```

##### 3. 常见考点与解题思路

1. 先判断资产的收益类型（无收益 / 已知收入 / 已知收益率）
2. 代入对应 carry 公式计算 fair forward price
3. 若市场价格偏离公平价格，设计套利策略：
   - 价格偏高 → short forward + buy underlying + borrow (cash-and-carry)
   - 价格偏低 → long forward + short underlying + invest (reverse cash-and-carry)
4. 验证复制组合的现金流是否匹配

##### 4. 易错点提醒

- 【考试陷阱】**期初价格 (price at initiation) 与存续期价值 (value during life) 并非同一概念** —— 价格是使初始价值为零的公平交割价，价值可正可负
- 已知收入要先折现再扣除，不能直接用未来值相减
- 连续复利与离散复利公式不要混用，注意题目给的是年利率还是连续利率

##### 5. 跨模块关联

- [[M05-Forward-and-Futures-Pricing]]：M04 的 carry 关系是 M05 定价的基础
- [[M07-Options-and-Put-Call-Parity]]：无套利逻辑同样适用于期权平价关系
- [[M08-Binomial-Valuation]]：二项式模型本质也是无套利复制
- [[M00-Derivatives-MOC]]：返回科目总览
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
