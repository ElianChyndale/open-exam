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
### 🌳 核心知识树

```text
🏆 M05: Natural Resources（自然资源）
│
├── ⭐ 商品期货定价 (Commodity Futures Pricing) 🎯超高頻
│   ├── 📐 持有成本模型: F = S × e^{(r+s-y)T}
│   │   ├── r: 无风险利率
│   │   ├── s: 存储成本
│   │   └── y: 便利收益 ⚠️ 是持有成本的对冲项
│   └── 便利收益: 持有实物的好处（防供应中断）
│
├── ⭐ 期货市场状态 (Market States) 🎯超高頻
│   ├── Contango (正向市场): F > S
│   │   └── Roll Yield为负（展期亏损）⚠️
│   └── Backwardation (反向市场): F < S
│       └── Roll Yield为正（展期获利）⚠️
│
├── ⭐ Roll Yield (展期收益) 🎯高频
│   ├── 📐 Roll Yield = (Near - Far) / Near
│   ├── Contango: Near < Far → 负Roll Yield
│   └── Backwardation: Near > Far → 正Roll Yield
│
├── ⭐ 自然资源投资形式
│   ├── 商品实物 (Physical): 持有现货
│   ├── 期货 (Futures): 最常用的投资方式
│   ├── ETF/ETN: 商品指数跟踪
│   └── 股票: 自然资源公司股票
│
├── ⭐ 各类自然资源特征
│   ├── 农业用地 (Farmland): 租金+增值
│   ├── 林地 (Timberland): 木材生长+价格变动
│   ├── 未开发土地 (Raw Land): 纯增值潜力
│   └── 大宗商品 (Commodities): 供需驱动、周期性强
│
└── ⭐ 风险收益特征
    ├── 高波动、通胀对冲属性
    ├── 与传统资产低到中等相关性
    └── 商品周期影响显著
```

## 📖 知识点详解

### 知识点1：商品期货定价——持有成本模型（Cost of Carry Model）
**核心概念**：商品期货的理论价格由持有成本模型决定：F = S × e^{(r+s-y)T}，其中S是现货价格，r是无风险利率，s是存储成本，y是便利收益（Convenience Yield），T是到期时间。便利收益是持有实物商品而非期货合约的额外好处——如防止供应中断、满足生产需求等。便利收益越高，期货价格相对于现货越低。与金融期货不同，商品期货的定价包含存储成本和便利收益这两个实物商品特有的因素。
- 📐 F = S × e^{(r+s-y)T}
- r：无风险利率（融资成本）
- s：存储成本（仓储、保险、运输）
- y：便利收益（持有实物的好处，降低期货价格）
- 便利收益是持有成本的对冲项：y越高 → F越低
**考试应用**：持有成本模型的计算和成分分析。注意y在公式中是减项——便利收益增加会降低期货价格。给定现货价和期货价可以反推隐含便利收益。

### 知识点2：Contango与Backwardation（市场状态）
**核心概念**：期货市场的两种状态决定展期收益的方向。Contango（正向市场）是期货价格高于现货价格的正常状态——当存储成本高或便利收益低时出现，此时展期收益（Roll Yield）为负，长期持有期货会产生展期亏损。Backwardation（反向市场）是期货价格低于现货价格的罕见状态——当前现货稀缺、便利收益高时出现，此时展期收益为正，长期持有期货获得展期收益。从投资者角度看，在Backwardation市场中长期持有多头仓位有利，Contango中不利。
- Contango（正向市场）：F > S，Roll Yield为负（展期亏损）
- Backwardation（反向市场）：F < S，Roll Yield为正（展期获利）
- Contango驱动因素：存储成本高、便利收益低、供给充足
- Backwardation驱动因素：便利收益高、现货稀缺、供需紧张
**考试应用**：Contango vs Backwardation的判断和Roll Yield的方向是最高频考点。记住：Contango（F>S）= 负Roll Yield；Backwardation（F<S）= 正Roll Yield。

### 知识点3：Roll Yield（展期收益）
**核心概念**：Roll Yield是期货投资总回报的一个重要组成部分，由期货期限结构决定。当投资者持有商品期货多头时，需要在期货到期前将头寸"展期"到下一个月的合约。Roll Yield = (近期期货价格 - 远期期货价格) / 近期期货价格。在Contango市场中，远期价格高于近期价格，展期时卖出低价近期合约买入高价远期合约产生亏损（负Roll Yield）。在Backwardation市场中则相反，产生正Roll Yield。商品期货总回报来自三个部分：现货价格变动（Spot Return）+ 展期收益（Roll Yield）+ 抵押品收益（Collateral Yield）。
- 📐 Roll Yield = (F_near - F_far) / F_near
- Contango：F_near < F_far → 负Roll Yield
- Backwardation：F_near > F_far → 正Roll Yield
- 总回报三来源：现货收益 + 展期收益 + 抵押品收益
**考试应用**：Roll Yield计算和方向判断。记住Contango = 负展期收益，Backwardation = 正展期收益。总回报三来源的概念也是常考点。

### 知识点4：自然资源投资形式（Natural Resource Investment Forms）
**核心概念**：投资自然资源有多种方式。实物持有（Physical）直接持有商品现货，但面临存储、保险和运输成本。期货（Futures）是最常用的方式——通过持有期货合约获得商品价格敞口，无需处理实物。ETF/ETN跟踪商品指数，提供便捷的分散化投资渠道。自然资源公司股票（如矿业、石油公司股票）提供间接敞口，但包含公司特有的运营风险和股票市场风险。此外还有 farmland（农业用地——租金+增值）、timberland（林地——木材生长+价格变动）和 raw land（未开发土地——纯增值潜力）等直接土地投资形式。
- 实物持有：直接持有现货，有存储成本
- 期货：最常用方式，需考虑展期收益
- ETF/ETN：跟踪商品指数，费用较低
- 自然资源股票：间接敞口，有公司特有风险
- Farmland/Timberland/Raw Land：各有不同的收益驱动因素
**考试应用**：了解不同投资形式的特征。被动商品投资也需要主动的展期策略——展期时机的选择会影响收益。

### 知识点5：自然资源风险收益特征（Risk, Return, and Diversification）
**核心概念**：自然资源投资具有高波动性和通胀对冲属性——商品价格在通胀上升时期通常上涨。与传统资产（股票、债券）呈低到中等相关性，提供组合分散化价值。但商品周期性强，受供需变化、地缘政治和天气等不可预测因素影响显著。商品周期的不同阶段（供给过剩→供给短缺）驱动现货价格的大幅摆动。投资自然资源时需要注意：商品总回报的三个来源（现货、展期、抵押品收益）在不同市场环境下贡献差异很大。
- 高波动：商品价格波动远高于股票和债券
- 通胀对冲：通胀期商品价格通常上涨
- 低到中等相关性：与股债相关性低，提供分散化
- 商品周期：供需变化导致价格大幅波动
- ⚠️ 短期通胀对冲效果可能不理想
**考试应用**：理解商品投资的通胀对冲属性和组合分散化价值。注意总回报三来源的区分——尤其是展期收益在不同市场环境下的差异。

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| F_0(T) = S_0 × e^{(r+s-y)T} | 期货定价（连续复利） | 计算理论期货价格 | 便利收益(y)降低期货价 |
| Roll Yield = (F_near - F_far) / F_near | 展期收益率 | 衡量展期成本/收益 | Contango下为负 |
| 持有成本率 = ln(F_0/S_0) / T = r + s - y | 隐含持有成本 | 从期货价格反推便利收益 | 可分解各成分 |
| Contango: F > S | 期货溢价 | 存储成本高/便利收益低时 | 展期亏损 |
| Backwardation: F < S | 期货贴水 | 现货稀缺/便利收益高时 | 展期获利 |

### 🛠️ 常见考点与解题思路

**Topic 1: Contango vs Backwardation判断**
- 给定近期和远期期货价格
- 远期价格 > 近期 → Contango（正向市场）
- 近期价格 > 远期 → Backwardation（反向市场）
- 解题：比较期货与现货价格方向

**Topic 2: Roll Yield计算**
- Roll Yield = (Near - Far) / Near
- Contango下为负，Backwardation下为正
- 注意：Roll Yield的方向与市场状态相反

**Topic 3: 便利收益影响分析**
- 便利收益高（现货稀缺）→ Backwardation → 正Roll Yield
- 便利收益低（供给充足）→ Contango → 负Roll Yield
- 解题：判断便利收益高低反向推导市场状态

**Topic 4: 持有成本模型计算**
- F = S × e^{(r+s-y)T}
- 注意y是对冲项（降低期货价格）
- 反推y：y = r + s - ln(F/S)/T

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| Contango = 正Roll Yield | Contango（F>S）= 负Roll Yield（展期亏损） | 概念混淆 |
| Backwardation = 负Roll Yield | Backwardation（F<S）= 正Roll Yield（展期获利） | 概念混淆 |
| 便利收益增加期货价格 | 便利收益降低期货价格（对冲项） | 公式中y是减项 |
| 商品期货定价与金融期货相同 | 商品期货有存储成本和便利收益 | 实物商品有持有成本 |
| 被动商品投资完全被动 | 展期策略需要主动决策 | 期货到期需展期 |
| 商品投资总是好的通胀对冲 | 商品价格与通胀正相关，但波动大 | 短期可能背离 |
| Roll Yield是总回报的主要来源 | 还有现货价格变动和抵押品收益 | 总回报有三个来源 |

### 🔄 跨模块关联

- **商品期货** → [[M01-Alternative-Investment-Features-Methods-and-Structures]]（另类投资六大特征）
- **商品周期** → [[M04-Real-Estate-and-Infrastructure]]（房地产周期与商品周期对比）
- **期限结构** → Derivatives科目（期货定价与套利）
- **通胀对冲** → Economics M04（货币政策与通胀）
- **大宗商品投资** → Equity M02（商品指数构建）
- **地缘政治与商品** → Economics M05（地缘风险影响能源/粮食价格）
- **自然资源公司估值** → Equity M08（资产基础法适用）

### 📋 复习与刷题提示

- **Contango vs Backwardation判断和Roll Yield方向是绝对高频考点**
- **持有成本模型计算**：F=S×e^{(r+s-y)T}的代入计算
- **便利收益的理解**：是什么、在公式中的位置、对期货价格的影响方向
- **商品总回报三来源**：价格变动(Spot Return) + 展期收益(Roll Yield) + 抵押品收益(Collateral Yield)
- **各类自然资源特征**：Farmland/Timberland/Raw Land/Commodities
- **风险分散化**：商品与股票债券的低相关性
- **刷题建议**：mock中Contango/Backwardation判断和Roll Yield计算最高频

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
