---
title: "M02 — Security Market Indexes"
description: 证券市场指数：指数构建方法、加权方式、再平衡与指数重构、价格收益与总收益
module: M02
subject: Equity
---

# M02: 证券市场指数 (Security Market Indexes)

## 1. 核心知识点

### 指数构建 (Index construction)
- **流程五步**：定义**目标市场 (target market)** → **成分选择 (constituent selection)** → **加权 (weighting)** → **再平衡 (rebalancing)** → **指数重构 (reconstitution)**
- **加权方法对比**：
  - **价格加权 (price-weighted)**：高价股影响力大，需**除数调整 (divisor adjustment)** 应对拆股
  - **等权 (equal-weighted)**：每只成分股权重相同，换手率高
  - **市值加权 (market-cap-weighted)**：大市值公司主导，最接近市场整体
  - **基本面加权 (fundamental-weighted)**：按营收、盈利等基本面指标加权

### 指数收益 (Index return)
- **价格收益 (price return)** 仅反映价格变化；**总收益 (total return)** 再投资股息/利息收入
- **等权指数**因需频繁再平衡至等权重，产生较高**换手率 (turnover)**
- **指数用途 (index use)**：业绩基准 (benchmark)、市场代理 (market proxy)、ETF 等产品标的 (product underlying)

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| 价格加权指数 (Price-weighted Index) | `Σ Price_i / Divisor` |
| 等权指数收益率 (Equal-weighted Return) | `Σ_{i=1}^{N} R_i / N` |
| 市值加权指数收益率 (Value-weighted Return) | `Σ_{i=1}^{N} w_i R_i` |
| 总收益率 (Total Return) | `(Ending Value + Income - Beginning Value) / Beginning Value` |

## 3. 常见考点与解题思路

- **除数调整计算**：拆股前后指数值应连续 → 调整 divisor
- **识别加权方法**：题目给股价求和 → 价格加权；给市值加总 → 市值加权
- **区分 price return vs total return**：看题目是否提到分红 reinvestment

## 4. 易错点提醒

- **加权方法改变表现特征**：同一成分组合用不同加权方法，收益率和风险特征都不同【考试陷阱】
- **价格加权指数不代表市场整体**：高价股被过度代表
- **等权指数的高换手率**：再平衡需求导致交易成本高于市值加权

## 5. 跨模块关联

- **指数作为基准用于估值比较** → [[M08-Equity-Valuation-Concepts]]
- **指数选择影响市场效率检验** → [[M03-Market-Efficiency]]
- **指数加权与交易执行成本有关** → [[M01-Market-Organization-and-Structure]]
