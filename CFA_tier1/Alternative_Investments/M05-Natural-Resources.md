---
title: "M05 — Natural Resources"
description: "CFA Level I 2026 official module: Natural Resources"
module: M05
subject: "Alternative Investments"
topic_area: Alternative_Investments
curriculum_year: 2026
official_module: "Module 5: Natural Resources"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Alternative_Investments
  - official_2026
---

# M05: Natural Resources

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Natural Resources
- 5.01 | Introduction
- 5.02 | Natural Resources Investment Features
- 5.03 | Commodity Investment Forms
- 5.04 | Natural Resource Investment Risk, Return, and Diversification

## Learning Outcome Statements

The candidate should be able to:

- explain features of raw land, timberland, and farmland and their investment characteristics
- describe features of commodities and their investment characteristics
- analyze sources of risk, return, and diversification among natural resource investments

## Local Study Notes

### Migrated from `CFA_tier1/Alternative_Investments/M05-Natural-Resources.md`

_Alignment score: 0.40. Original official module field: Natural Resources._

#### M05: 自然资源 (Natural Resources)

##### 1. 核心知识点

###### 5.1 商品期货 (Commodity Futures)【考试核心】

####### 期货定价理论

**持有成本模型 (Cost of Carry)**:

期货价格 (Futures Price) = 现货价格 × e^{((r + s - y) × T)}

| 变量 | 含义 |
|------|------|
| r | 无风险利率 (Risk-Free Rate) |
| s | 存储成本 (Storage Cost) |
| y | 便利收益 (Convenience Yield) |
| T | 到期时间 |

**便利收益 (Convenience Yield)**: 持有实物商品的额外好处（如防止供应中断），是持有成本的对冲项

####### Contango (正向市场) vs Backwardation (反向市场)

| 维度 | Contango (正向市场) | Backwardation (反向市场) |
|------|--------------------|------------------------|
| 价格关系 | 期货价格 > 现货价格 | 期货价格 < 现货价格 |
| Roll Yield | 负 (不利) | 正 (有利) |
| 驱动因素 | 存储成本高 / 便利收益低 | 便利收益高（现货稀缺） |
| 投资者影响 | 长期持期货有损耗（展期亏损） | 长期持期货有收益（展期获利） |
| 市场状态 | 期货溢价，远期贴水预期 | 期货贴水，现货稀缺 |

####### Roll Yield (展期收益)

Roll Yield = (近期期货 - 远期期货) / 近期期货

- **Contango下**: 近期期货 < 远期期货 → Roll Yield为负
- **Backwardation下**: 近期期货 > 远期期货 → Roll Yield为正

**本质**: 展期收益/成本，由期货期限结构 (Term Structure) 决定

####### 商品期货投资策略

- **被动投资 (Passive)**: 指数跟踪，需考虑期限结构影响
- **主动投资 (Active)**: 期限结构套利、现货-期货套利

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 期货定价 | F_0(T) = S_0 × e^{((r + s - y) × T)} |
| Roll Yield | (近期期货 - 远期期货) / 近期期货 |
| 持有成本率 | ln[F_0(T)/S_0] / T = r + s - y |

##### 3. 常见考点与解题思路

1. **Contango vs Backwardation判断**: 给定近期和远期期货价格，判断市场状态。**思路**: 远期 > 近期 = Contango；近期 > 远期 = Backwardation。
2. **Roll Yield计算**: 给定近期和远期期货价格，计算Roll Yield。**思路**: Roll Yield = (Near - Far) / Near。Contango下为负，Backwardation下为正。
3. **便利收益影响分析**: 现货稀缺时便利收益高，导致Backwardation。**思路**: 便利收益高 → Backwardation → 正Roll Yield。
4. **期货定价计算**: 给定现货价格、利率、存储成本、便利收益和期限，计算期货价格。**思路**: 使用持有成本公式F = S × e^{(r+s-y)T}。

##### 4. 易错点提醒

- **Contango ≠ 正Roll Yield**: Contango（期货>现货）= 负Roll Yield（展期亏损）
- **Backwardation ≠ 负Roll Yield**: Backwardation（期货<现货）= 正Roll Yield（展期获利）
- **便利收益是持有成本的对冲项**: 公式中便利收益(y)降低期货价格，而非增加
- **商品现货实物持有**: 商品期货定价基础是实物商品的持有成本，与金融期货不同
- **被动投资也有主动决策**: 即使是被动指数跟踪，也需要考虑展期策略

##### 5. 跨模块关联

- 商品期货 → [[M01-Features-and-Structure.md]] (另类投资特征)
- 商品周期 → [[M04-Real-Estate-and-Infrastructure.md]] (房地产周期对比)
- 期限结构 → 可与 Derivatives 科目联动
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
