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
### 🌳 核心知识树

```text
🏆 M02: Security Market Indexes（证券市场指数）
│
├── ⭐ 指数的定义与计算 (Definition & Calculation) 🎯高频
│   ├── 价格收益 (Price Return): 仅价格变化
│   ├── 总收益 (Total Return): 价格 + 再投资收入
│   └── 📐 指数价值 = Σ(成分价格 × 权重) / 除数
│
├── ⭐ 指数构建五步 (Construction Steps)
│   ├── 1. 定义目标市场 (Target Market)
│   ├── 2. 成分选择 (Constituent Selection)
│   ├── 3. 加权方法 (Weighting Method) 🎯高频
│   ├── 4. 再平衡 (Rebalancing)
│   └── 5. 指数重构 (Reconstitution)
│
├── ⭐ 四种加权方法 (Weighting Methods) 🎯高频
│   ├── 价格加权 (Price-Weighted) ⚠️ 高价股影响过大
│   │   └── 📐 除权调整 (Divisor Adjustment) 🎯高频
│   ├── 等权 (Equal-Weighted) ⚠️ 高换手率
│   │   └── 📐 收益率 = 各成分收益率算术平均
│   ├── 市值加权 (Market-Cap-Weighted) ⚠️ 大盘股主导
│   │   └── 📐 收益率 = Σ w_i × R_i
│   └── 基本面加权 (Fundamental-Weighted) ⚠️ 价值倾向
│       └── 按营收/盈利/股息/账面值加权
│
├── ⭐ 指数管理 (Index Management)
│   ├── 再平衡 (Rebalancing): 恢复目标权重
│   └── 重构 (Reconstitution): 调整成分股 ⚠️ 引发价格效应
│
├── ⭐ 指数用途 (Uses)
│   ├── 业绩基准 (Benchmark)
│   ├── 市场代理 (Market Proxy)
│   ├── 产品标的 (ETF/Index Fund/Futures)
│   └── 资产配置模型输入
│
└── ⭐ 指数类型 (Types)
    ├── 权益指数 (Equity Indexes): 全球/国家/行业/风格
    ├── 固收指数 (Fixed-Income): 复杂（品种多、交易少）
    └── 另类投资指数 (Alternative): 对冲基金/商品/房地产
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| 价格加权指数 = Σ Price_i / Divisor | 各成分股价格之和/除数 | 道指等价格加权指数 | 拆股后需调整除数 |
| 等权指数收益 = (1/N) × Σ R_i | 各成分收益率算术平均 | 小盘股代表性更好的指数 | 再平衡换手率高 |
| 市值加权收益 = Σ w_i × R_i | 按市值权重加权 | 最常用的指数方法（标普500） | 大盘股主导 |
| 总收益 = (End Value + Income - Begin) / Begin | 含再投资收入的收益 | 衡量投资者真实回报 | 需确认dividend reinvestment |
| 除数调整: New Divisor = Σ New Prices / Old Index Value | 拆股后除数 | 保持指数连续性 | 只调除数，不调成分股 |
| Price Return = (V₁ - V₀) / V₀ | 仅价格变化的回报 | 不含分红 | 低估实际投资者回报 |
| Total Return = (V₁ + Income - V₀) / V₀ | 含分红再投资回报 | 较全面的回报衡量 | 分红再投资假设 |

### 🛠️ 常见考点与解题思路

**Topic 1: 除数调整计算**
- 拆股前：Index = Σ Prices / Old Divisor
- 拆股后：以拆股前指数值为目标，反推新除数
- New Divisor = Σ(New Prices) / Old Index Value
- 本质：拆股不改变指数值，只调除数

**Topic 2: 加权方法识别**
- 给股价求和 → 价格加权
- 给收益率算术平均 → 等权
- 给市值加总 → 市值加权
- 给基本面指标 → 基本面加权

**Topic 3: Price Return vs Total Return**
- Price Return：不含分红，V₁/V₀ - 1
- Total Return：(V₁ + Dividends)/V₀ - 1
- 关键：题目是否提到分红 reinvestment

**Topic 4: 四种加权方法对比**
- 哪种偏向大盘股？→ 市值加权
- 哪种换手率最高？→ 等权
- 哪种受拆股影响？→ 价格加权
- 哪种有价值倾向？→ 基本面加权

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 价格加权指数代表市场整体 | 高价股过度代表，不代表市场整体 | 权重由价格决定非经济规模 |
| 同一成分用不同加权方法结果相同 | 加权方法不同，收益和风险特征完全不同 | 权重分配不同 |
| 等权指数换手率低 | 等权指数需频繁再平衡，换手率高 | 股价涨跌导致权重偏离 |
| 指数重构只影响指数本身 | 重构导致被纳入股票价格上涨、被剔除股票下跌 | 被动资金跟踪效应 |
| 固定收益指数和权益指数一样容易构建 | 固收品种多、交易频率低，构建更复杂 | 流动性差异 |
| 市值加权就一定是好基准 | 若指数与投资者风格不匹配，不是好基准 | 需考虑投资策略一致性 |

### 🔄 跨模块关联

- **指数作为估值比较基准** → [[M08-Equity-Valuation-Concepts-and-Basic-Tools]]（Justified P/E vs 行业平均P/E）
- **指数选择影响市场效率检验** → [[M03-Market-Efficiency]]（异常收益检验依赖基准选择）
- **加权方法与交易成本** → [[M01-Market-Organization-and-Structure]]（等权指数高换手产生更多交易成本）
- **指数作为资产配置工具** → [[M05-Company-Analysis-Past-and-Present]]（行业配置的基准）
- **套利与指数期货** → [[M01-Market-Organization-and-Structure]]（指数套利交易策略）
- **另类投资指数特征** → AI模块（对冲基金指数偏差问题）

### 📋 复习与刷题提示

- **除数调整计算是必考题**：掌握拆股前后指数值不变的核心逻辑
- **加权方法对比**：价格加权/等权/市值加权/基本面加权的优缺点对比是高概率考点
- **Price Return vs Total Return**：注意题目中的分红假设
- **指数用途辨析**：benchmark vs market proxy vs product underlying
- **Rebalancing vs Reconstitution**：再平衡（调整权重）vs 重构（调整成分股）的区别
- **刷题重点**：除数调整计算、加权方法特征辨析、指数收益计算
- **联系实际**：标普500（市值加权）、道指（价格加权）、纳斯达克100（修正市值加权）

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
