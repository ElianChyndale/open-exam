---
title: "M06 — Pricing and Valuation of Futures Contracts"
description: "CFA Level I 2026 official module: Pricing and Valuation of Futures Contracts"
module: M06
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 6: Pricing and Valuation of Futures Contracts"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M06: Pricing and Valuation of Futures Contracts

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Pricing and Valuation of Futures Contracts
- 6.01 | Introduction
- 6.02 | Pricing of Futures Contracts at Inception
- 6.03 | MTM Valuation: Forwards versus Futures
- 6.04 | Interest Rate Futures versus Forward Contracts
- 6.05 | Forward and Futures Price Differences
- 6.06 | Interest Rate Forward and Futures Price Differences
- 6.07 | Effect of Central Clearing of OTC Derivatives

## Learning Outcome Statements

The candidate should be able to:

- compare the value and price of forward and futures contracts
- explain why forward and futures prices differ

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M06: 期货合约定价与估值 (Futures Pricing and Valuation)
│
├── 🟢 核心主题：期货 vs 远期的全面对比
│   └── 定价框架相同，结算机制不同
│
├── ⭐ 期货的核心特征
│   ├── 标准化合约 (Standardized)
│   ├── 交易所交易 (Exchange-Traded)
│   ├── 每日盯市结算 (Daily Marking-to-Market)
│   ├── 保证金制度 (Margin)
│   │   ├── 初始保证金 (Initial Margin)
│   │   └── 维持保证金 (Maintenance Margin)
│   └── 中央清算所 (Central Counterparty / CCP)
│       └── 🎯 高频考点：CCP 消除交易对手风险
│
├── ⭐ 期货定价
│   ├── 期初公平价格 = 远期公平价格 (假设相同标的和到期日)
│   │   ├── 无收益: F0(T) = S0(1+r)^T
│   │   ├── 已知收入: F0(T) = [S0 - PV(I)](1+r)^T
│   │   └── 已知收益率: F0(T) = S0[(1+r)/(1+q)]^T
│   └── 💡 期货与远期的期初公平价格一致
│
├── ⭐ 期货 vs 远期价格差异
│   ├── 原因: 利率与标的资产价格的相关性
│   │   ├── 正相关 (利率↑→标的价↑)
│   │   │   └── 期货价格 > 远期价格
│   │   │   └── 多头每日获利可再投资于更高利率
│   │   └── 负相关 (利率↑→标的价↓)
│   │       └── 期货价格 < 远期价格
│   └── 🎯 高频考点：相关性方向决定价格差异
│
├── ⭐ 利率期货 vs FRA
│   ├── 欧洲美元期货 (Eurodollar Futures)
│   │   └── 报价: 100 - 年化远期利率
│   ├── 期货每日结算 vs FRA 到期一次结算
│   └── 凸性调整 (Convexity Adjustment)
│       └── 解决利率期货与 FRA 的定价差异
│
├── ⭐ MTM 估值对比
│   ├── 远期: 存续期价值 Vt = St - PVt(K)，到期前价值波动
│   ├── 期货: 每日结算 → 存续期价值每日归零
│   └── 💡 核心区别：远期有未实现盈亏，期货已实现盈亏
│
├── 💡 关键洞察
│   ├── 期货的 MTM 机制降低了对手风险，但改变了现金流模式
│   ├── 相关性假设是期货-远期价差的理论基础
│   └── CCP 不仅用于期货，也覆盖 OTC 衍生品
│
└── ⚠️ 考试陷阱
    ├── 期初价格一致，不是价格不同
    ├── 相关性方向不能搞反
    ├── 欧洲美元期货报价 = 100 - 利率
    └── 期货价值存续期归零，不是不变
```

## 📖 知识点详解

### 知识点1：期货的核心机制 (Futures Core Mechanisms)

**核心概念**：期货合约在交易所交易，具有标准化、每日盯市结算、保证金制度和中央清算四大核心特征。这些机制共同作用，使期货的交易对手风险远低于 OTC 远期合约。理解这些机制是理解期货定价和期货-远期价差的基础。

- **标准化合约 (Standardized Contracts)**：交易所统一规定合约规模、到期日、交割等级和质量标准。标准化降低了交易成本但牺牲了灵活性
- **每日盯市结算 (Daily Marking-to-Market)**：每个交易日结束时，交易所根据当日结算价调整交易双方的保证金账户。盈利方可提取超额保证金，亏损方需补足保证金。这使得期货的存续期价值每日归零
- **保证金制度 (Margin System)**：初始保证金（initial margin）是开仓时需存入的最低资金；维持保证金（maintenance margin）是账户允许的最低余额，低于此水平需追加保证金（margin call）
- **中央清算所 (Central Counterparty / CCP)**：作为所有交易的共同对手方，消除双边交易对手风险。CCP 还通过违约基金（default fund）分摊极端情况下的损失
- 💡 **核心理解**：期货的 MTM 机制使未实现盈亏变为已实现现金流，这与远期根本不同

**考试应用**：期货的四大机制（标准化、MTM、保证金、CCP）是高频考点。常见题型包括：给出一组特征判断是期货还是远期；解释保证金制度如何降低对手风险；MTM 对期货价格和估值的影响。

### 知识点2：期货与远期的价格差异 (Price Difference between Futures and Forwards)

**核心概念**：虽然期货和远期的期初公平价格相同（都由无套利条件决定），但由于期货的每日盯市结算创造了一系列中间现金流，当利率与标的资产价格相关时，期货价格会偏离远期价格。这是 Level I 考试的重要概念点。

- **期初价格相同**：期货和远期的初始公平价格都由相同的无套利公式决定
- **价格差异的根本原因**：利率与标的资产价格之间的相关性
  - **正相关**（利率↑ 标的价↑）：期货多头每日获利可再投资于更高利率 → 期货价格 > 远期价格
  - **负相关**（利率↑ 标的价↓）：期货多头每日亏损需以更高利率融资 → 期货价格 < 远期价格
  - **不相关**：期货价格 = 远期价格
- 🎯 高频考点：相关性方向决定价格差异方向，不能搞反

**考试应用**：给定利率与标的价格的相关性方向，判断期货价格与远期价格的大小关系。记忆法：正相关 → 期货 > 远期。考试中常以概念题形式出现，要求理解差异的原因而不是计算差异大小。

### 知识点3：欧洲美元期货 (Eurodollar Futures)

**核心概念**：欧洲美元期货是交易最活跃的利率期货合约之一，基于 3 个月期 LIBOR（或替代参考利率）。其报价方式独特：报价 = 100 - 年化远期利率。报价与利率呈反向关系——利率上升则报价下降，利率下降则报价上升。

- **报价机制**：Eurodollar Futures Price = 100 - Annualized Forward Rate
- **利率与报价反向变动**：利率从 2% 上升到 3%，报价从 98 下降到 97
- **凸性调整 (Convexity Adjustment)**：由于期货每日盯市结算而 FRA 到期一次结算，利率期货与 FRA 之间存在定价差异，需通过凸性调整修正
- 💡 欧洲美元期货是利率互换市场的重要对冲和定价工具

**考试应用**：理解欧洲美元期货报价与利率的反向关系。常见陷阱：将报价直接当作利率。记住报价下降意味着利率上升。考试中可能出现报价转换计算题。

### 知识点4：期货 vs 远期的 MTM 估值对比 (MTM Valuation: Forwards vs Futures)

**核心概念**：远期和期货在存续期的估值方式根本不同。远期的未实现盈亏在存续期内不断累积，只在到期时一次性结算；期货的未实现盈亏每日结算，存续期价值每日归零。

- **远期估值**：存续期价值 Vt = St - PVt(K)，到期前价值不断波动。远期存在未实现盈亏
- **期货估值**：每日 MTM 结算后，保证金账户反映已实现盈亏，合约本身的价值每日归零
- **到期收益相同**：忽略 MTM 再投资收益，远期和期货的到期总收益相同
- 💡 核心区别：远期有未实现盈亏（账面价值），期货已实现盈亏（现金价值）

**考试应用**：对比远期和期货的 MTM 估值是高频概念题。注意：期初价格相同、存续期价值不同（期货每日归零）、到期收益相同。不要混淆期货价值"每日归零"与"价值不变"。

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `F0(T) = S0(1+r)^T` | 无收益资产期货期初价格 | 期货公平价格计算（同远期） | 期初与远期相同 |
| `F0(T) = [S0 - PV(I)](1+r)^T` | 已知收入资产期货期初价格 | 有分红股票期货 | 收入需折现 |
| `F0(T) = S0[(1+r)/(1+q)]^T` | 已知收益率资产期货期初价格 | 股指期货 | 连续: S0e^{(r-q)T} |
| `Eurodollar Futures Price = 100 - Annualized Forward Rate` | 欧洲美元期货报价 | 利率期货价格理解 | 价格与利率反向变动 |
| `期货 MTM: 每日盈亏 = ΔF × Contract Size` | 期货每日浮动盈亏 | 保证金账户计算 | 日终结算至账户 |
| `期货 > 远期 (r与S正相关)` | 利率上升标的价格也上升，多头每日获利可再投资 | 判断期货-远期价差方向 | 记住相关性方向的影响 |

### 🛠️ 常见考点与解题思路

**考点1：期货 vs 远期对比**
- **步骤**：从 5 个维度对比——交易场所、标准化、结算方式、对手风险、价格
- **关键点**：
  - 期初价格一致
  - 存续期价值不同（期货每日归零）
  - 到期收益相同（忽略 MTM 再投资收益）

**考点2：判断期货 vs 远期价格大小**
- **步骤**：
  1. 判断利率与标的资产价格的相关性方向
  2. 正相关 → 期货价格 > 远期价格
  3. 负相关 → 期货价格 < 远期价格
  4. 不相关 → 价格相同
- **推理**：正相关时，多头每日获利（标的涨）可再投资于更高利率，多头愿意出更高价格

**考点3：欧洲美元期货报价理解**
- **步骤**：
  1. 报价 = 100 - 年化远期利率
  2. 利率上升 → 报价下降
  3. 利率下降 → 报价上升
- **陷阱**：报价变动方向与利率变动方向相反

**考点4：中央清算所 (CCP) 的作用**
- **步骤**：理解 CCP 如何降低系统性风险
  - 成为所有交易的中央对手方
  - 要求保证金
  - 每日盯市结算
  - 违约基金 (default fund) 分摊风险

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 期货价格总是不等于远期价格 | 期初公平价格相同，存续期才可能因 MTM 产生差异 | 定价公式一致，结算机制不同导致差异 |
| 利率与标的价格正相关时远期 > 期货 | 正相关时期货 > 远期 | 多头每日盈利可再投资于更高利率 |
| 欧洲美元期货报价直接是利率 | 报价 = 100 - 年化利率 | 报价与利率反向变动 |
| 期货存续期价值与远期一样波动 | 期货每日 MTM 结算，存续期价值每日归零 | 每日盈亏已实现，无未实现损益 |
| CCP 只用于期货 | CCP 也被用于 OTC 衍生品中央清算 | 金融危机后 OTC 也被要求中央清算 |
| 保证金 = 首付 | 保证金是履约保证，不是部分付款 | 保证金是信用风险缓释工具 |

### 🔄 跨模块关联

- **[[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]]** — 远期定价公式是期货定价的基础，两模块定价公式相同
- **[[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]]** — 利率互换可视为一系列 FRA 组合，FRA 与利率期货密切相关
- **[[M01-Derivative-Instrument-and-Derivative-Market-Features]]** — 交易所市场的保证金和清算制度在 M01 中介绍
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M06 在 Derivatives 科目中规模较小，但概念对比很重要
- **核心能力**：能清晰对比期货与远期的异同，理解价格差异的原因
- **必考题型**：期货 vs 远期对比、价格差异方向判断、欧洲美元期货报价
- 记忆要点：
  - 期初价格相同 / 存续期不同 / 到期收益相同
  - 正相关 = 期货 > 远期
  - 欧洲美元期货价格 = 100 - 利率
- 理解 MTM 的影响：远期合约的未实现盈亏成为期货的已实现现金流
- 不要混淆：期货与远期的差异是**结算机制**的差异，不是定价逻辑的差异
