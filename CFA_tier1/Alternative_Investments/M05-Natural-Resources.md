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
