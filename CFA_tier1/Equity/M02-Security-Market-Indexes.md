---
title: "M02 — Security Market Indexes"
description: "CFA Level I 2026 official module: Security Market Indexes"
module: M02
subject: "Equity Investments"
topic_area: Equity
curriculum_year: 2026
official_module: "Module 2: Security Market Indexes"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Equity
  - official_2026
---

# M02: Security Market Indexes

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Security Market Indexes
- 2.01 | Introduction
- 2.02 | Index Definition and Calculations of Value and Returns
- 2.03 | Index Construction
- 2.04 | Index Management: Rebalancing and Reconstitution
- 2.05 | Uses of Market Indexes
- 2.06 | Equity indexes
- 2.07 | Fixed-income indexes
- 2.08 | Indexes for Alternative Investments
- 2.09 | Summary

## Learning Outcome Statements

The candidate should be able to:

- describe a security market index
- calculate and interpret the value, price return, and total return of an index
- describe the choices and issues in index construction and management
- compare the different weighting methods used in index construction
- calculate and analyze the value and return of an index given its weighting method
- describe rebalancing and reconstitution of an index
- describe uses of security market indexes
- describe types of equity indexes
- compare types of security market indexes
- describe types of fixed-income indexes
- describe indexes representing alternative investments

## Local Study Notes

### Migrated from `CFA_tier1/Equity/M02-Security-Market-Indexes.md`

_Alignment score: 1.00. Original official module field: Module 2: Security Market Indexes._

#### M02: 证券市场指数 (Security Market Indexes)

##### 1. 核心知识点

###### 指数构建 (Index construction)
- **流程五步**：定义**目标市场 (target market)** → **成分选择 (constituent selection)** → **加权 (weighting)** → **再平衡 (rebalancing)** → **指数重构 (reconstitution)**
- **加权方法对比**：
  - **价格加权 (price-weighted)**：高价股影响力大，需**除数调整 (divisor adjustment)** 应对拆股
  - **等权 (equal-weighted)**：每只成分股权重相同，换手率高
  - **市值加权 (market-cap-weighted)**：大市值公司主导，最接近市场整体
  - **基本面加权 (fundamental-weighted)**：按营收、盈利等基本面指标加权

###### 指数收益 (Index return)
- **价格收益 (price return)** 仅反映价格变化；**总收益 (total return)** 再投资股息/利息收入
- **等权指数**因需频繁再平衡至等权重，产生较高**换手率 (turnover)**
- **指数用途 (index use)**：业绩基准 (benchmark)、市场代理 (market proxy)、ETF 等产品标的 (product underlying)

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 价格加权指数 (Price-weighted Index) | `Σ Price_i / Divisor` |
| 等权指数收益率 (Equal-weighted Return) | `Σ_{i=1}^{N} R_i / N` |
| 市值加权指数收益率 (Value-weighted Return) | `Σ_{i=1}^{N} w_i R_i` |
| 总收益率 (Total Return) | `(Ending Value + Income - Beginning Value) / Beginning Value` |

##### 3. 常见考点与解题思路

- **除数调整计算**：拆股前后指数值应连续 → 调整 divisor
- **识别加权方法**：题目给股价求和 → 价格加权；给市值加总 → 市值加权
- **区分 price return vs total return**：看题目是否提到分红 reinvestment

##### 4. 易错点提醒

- **加权方法改变表现特征**：同一成分组合用不同加权方法，收益率和风险特征都不同【考试陷阱】
- **价格加权指数不代表市场整体**：高价股被过度代表
- **等权指数的高换手率**：再平衡需求导致交易成本高于市值加权

##### 5. 跨模块关联

- **指数作为基准用于估值比较** → [[M08-Equity-Valuation-Concepts]]
- **指数选择影响市场效率检验** → [[M03-Market-Efficiency]]
- **指数加权与交易执行成本有关** → [[M01-Market-Organization-and-Structure]]
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
