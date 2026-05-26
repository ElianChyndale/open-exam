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

## 📖 知识点详解

### 知识点1：指数的定义与计算（Index Definition and Calculation）
**核心概念**：证券市场指数是代表一组证券整体表现的投资组合，通过追踪成分证券的价格或总收益来反映某一市场或细分领域的表现。指数价值通过加权方法计算，总收益（Total Return）包含价格变化和股息/利息再投资，而价格收益（Price Return）仅反映价格变化。指数价值的基本公式为各成分价格乘以权重之和再除以除数。
- 价格收益（Price Return）：仅反映指数成分价格变化带来的回报
- 总收益（Total Return）：在价格收益基础上加回股息、利息等再投资收入
- 📐 指数价值 = Σ(成分价格 × 权重) / 除数
**考试应用**：计算指数价值时注意区分价格收益和总收益。题目中若提到分红 reinvestment，则用总收益公式。

### 知识点2：指数构建五步（Construction Steps）
**核心概念**：指数构建是一个系统的五步过程。首先需要定义目标市场（如美国大盘股），然后从该市场中筛选符合条件的成分证券。接着确定加权方法，之后定期对指数进行再平衡以恢复目标权重，最后通过指数重构定期调整成分股名单。每一步的选择都会显著影响指数的表现特征和用途。
1. 目标市场：明确指数覆盖的资产类别、地域和规模范围
2. 成分选择：确定纳入/排除标准（如市值门槛、流动性要求）
3. 加权方法：决定各成分在指数中的权重分配方式
4. 再平衡（Rebalancing）：定期恢复各成分的目标权重
5. 重构（Reconstitution）：定期更新成分股名单，剔除不再符合条件的、纳入新符合条件的
**考试应用**：区分再平衡和重构——再平衡调整权重不换成分，重构更换成分股。重构引起价格效应（新纳入股票上涨、被剔除股票下跌）。

### 知识点3：四种加权方法对比（Weighting Methods）
**核心概念**：不同的加权方法导致同一组成分呈现出截然不同的风险和收益特征。价格加权指数受高价股主导，简单易懂但存在拆股偏差；等权指数给予小盘股更高权重但换手率高；市值加权指数最接近市场整体表现，是大盘股指数的首选方法，但大盘股过度代表；基本面加权按营收、盈利、股息等经济规模指标加权，具有价值倾向。
- 价格加权（Price-Weighted）：📐 指数 = Σ价格 / 除数，高价股影响过大，拆股需调整除数
- 等权（Equal-Weighted）：📐 收益率 = (1/N) × ΣR_i，小盘代表性好，再平衡换手率高
- 市值加权（Market-Cap-Weighted）：📐 收益率 = Σw_i × R_i，最常用，大盘股主导
- 基本面加权（Fundamental-Weighted）：按营收、盈利、账面值等加权，有内在价值倾向
**考试应用**：给定指数特征判断加权方法——股价求和计算的是价格加权，算术平均收益率是等权，市值加权用市值比例算权重。除数调整计算是必考计算题。

### 知识点4：指数管理——再平衡与重构（Rebalancing and Reconstitution）
**核心概念**：再平衡是指将指数中各成分的权重恢复至目标水平的过程，目的是维持指数的投资风格和风险暴露不变。重构则是定期更新成分股名单——剔除不再符合纳入标准的公司，加入新符合条件的公司。重构过程本身可能引发价格效应，因为被动跟踪指数的基金需要买入新纳入的股票、卖出被剔除的股票。
- 再平衡：恢复权重，等权指数再平衡频率最高
- 重构：更换成分股，被纳入股票通常上涨，被剔除股票通常下跌
- 影响：重构可能导致短期价格压力和交易量异常
**考试应用**：对比再平衡和重构的概念。等权指数的再平衡频率最高、换手率最高，这是重要的考点。

### 知识点5：指数的多种用途（Uses of Market Indexes）
**核心概念**：指数在投资领域有广泛用途，主要包括作为业绩基准来衡量投资组合的相对表现、作为市场代理来反映整体市场走势、作为指数基金和ETF等被动投资产品的标的资产、以及作为资产配置模型的输入参数。不同的使用目的对指数构建方法有不同的要求——作为业绩基准需要与投资风格匹配，作为产品标的需要有可投资性。
- 业绩基准（Benchmark）：衡量主动管理基金相对于市场的表现
- 市场代理（Market Proxy）：反映市场整体趋势，用于学术研究
- 产品标的（Product Underlying）：ETF、指数基金、指数期货的跟踪目标
- 资产配置输入：提供给资产配置模型使用的各类资产回报率数据
**考试应用**：判断指数是否适合作为某个基金的业绩基准——关键在于指数风格是否与基金的投资策略一致。

### 知识点6：指数类型（Types of Indexes）
**核心概念**：指数不仅覆盖权益市场，还涵盖固收、另类投资等多个领域。权益指数可按地域（全球、国家）、行业（GICS板块）、风格（成长/价值、大盘/小盘）细分。固收指数构建比权益指数更复杂，因为债券品种繁多、交易频率低。另类投资指数（如对冲基金指数、商品指数）面临更多挑战，包括幸存者偏差和收益平滑等问题。
- 权益指数：全球指数、国家指数、行业指数、风格指数
- 固收指数：政府债、公司债、高收益债等，构建更复杂
- 另类投资指数：对冲基金指数、商品指数、房地产指数
- 挑战：固收品种多交易少，另类投资存在数据偏差
**考试应用**：了解不同类型指数的特点和构建难点。注意另类投资指数存在幸存者偏差和选择性偏差问题。

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
