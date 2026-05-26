---
title: "M02 — Forward Commitment and Contingent Claim Features and Instruments"
description: "CFA Level I 2026 official module: Forward Commitment and Contingent Claim Features and Instruments"
module: M02
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 2: Forward Commitment and Contingent Claim Features and Instruments"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M02: Forward Commitment and Contingent Claim Features and Instruments

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Forward Commitment and Contingent Claim Features and Instruments
- 2.01 | Introduction
- 2.02 | Forwards, Futures, and Swaps
- 2.03 | Futures
- 2.04 | Swaps
- 2.05 | Options
- 2.06 | Credit Derivatives
- 2.07 | Forward Commitments vs. Contingent Claims

## Learning Outcome Statements

The candidate should be able to:

- define forward contracts, futures contracts, swaps, options (calls and puts), and credit derivatives and compare their basic characteristics
- determine the value at expiration and profit from a long or a short position in a call or put option
- contrast forward commitments with contingent claims

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M02: 远期承诺与或有索取权 (Forward Commitments and Contingent Claims)
│
├── 🟢 两大分类 (Two-Way Classification)
│   ├── 远期承诺 (Forward Commitments)
│   │   └── 双方均有义务在未来执行交易 (both parties obligated)
│   └── 或有索取权 (Contingent Claims)
│       └── 持有人有权利但无义务 (holder has right, no obligation)
│
├── ⭐ 远期承诺 (Forward Commitments)
│   ├── 远期合约 (Forward)
│   │   ├── 定制化条款 (customized)
│   │   ├── OTC 交易
│   │   ├── 到期一次结算
│   │   └── ⚠️ 存在交易对手风险
│   ├── 期货 (Futures)
│   │   ├── 标准化合约 (standardized)
│   │   ├── 交易所交易
│   │   ├── 每日盯市结算 (daily marking-to-market)
│   │   └── 💡 本质：标准化的远期合约 + 每日结算
│   └── 互换 (Swap)
│       ├── OTC 交易
│       ├── 一系列类似远期的现金流交换
│       ├── 利率互换不交换名义本金
│       └── 💡 本质：一系列远期合约的组合 (strip of forwards)
│
├── ⭐ 或有索取权 (Contingent Claims)
│   ├── 看涨期权 (Call)
│   │   ├── 赋予买入权利 (right to buy)
│   │   └── Payoff: max(0, ST - X)
│   ├── 看跌期权 (Put)
│   │   ├── 赋予卖出权利 (right to sell)
│   │   └── Payoff: max(0, X - ST)
│   ├── 期权卖方 (Writer)
│   │   └── 承担或有义务，收取权利金
│   └── 信用衍生品 (Credit Derivatives)
│       └── 仅在信用事件触发条件下支付
│
├── 📐 关键公式
│   ├── 远期承诺 payoff = 标的资产价格变化 × 合约规模 (双边义务)
│   └── 或有索取权 payoff = max(0, ST - X) 或 max(0, X - ST) (单边权利)
│
├── 🎯 高频考点
│   ├── 权利 vs 义务的区分 (每道 payoff 题的第一步判断)
│   ├── 远期 vs 期货的区别 (结算方式、交易场所)
│   └── 互换 = 一系列远期合约的组合
│
└── ⚠️ 考试陷阱
    ├── long forward 和 long call 不一样 (义务 vs 权利)
    ├── 期权持有人不一定会行权 (只有经济上有利时才行使)
    └── 互换名义本金通常不交换
```

## 📖 知识点详解

### 知识点1：远期承诺 (Forward Commitments)

**核心概念**：远期承诺是衍生品的一大类别，合约双方均有义务在未来按照约定条件执行交易。无论市场价格如何变化，双方都必须履行合约义务，因此远期承诺的收益/损失是对称的。远期承诺包括远期合约、期货合约和互换合约。

- **远期合约 (Forwards)**：定制化的 OTC 合约，约定在未来某一日期以约定价格买卖标的资产。到期一次结算，存续期未实现盈亏不断累积。定制化程度高但存在交易对手违约风险。
- **期货合约 (Futures)**：在交易所交易的标准化合約，本质是标准化远期合约加上每日盯市结算（daily marking-to-market）。通过保证金制度和中央清算所（CCP）大幅降低交易对手风险。
- **互换合约 (Swaps)**：OTC 合约，约定在未来一系列日期交换现金流。可视为一系列远期合约的组合（strip of forwards）。利率互换是最常见的类型，只交换净利息差额，不交换名义本金。
- 📐 远期承诺的 payoff = 标的资产价格变动 × 合约规模，收益/损失对称

**考试应用**：判断一个合约是否属于远期承诺的关键是看双方是否都有义务执行。远期承诺的 payoff 是对称的。考试中常要求对比远期与期货的区别，以及互换与远期合约的关系。

### 知识点2：或有索取权 (Contingent Claims)

**核心概念**：或有索取权是衍生品的另一大类，合约持有人在未来有权利但没有义务执行交易。期权是最典型的或有索取权，持有人可以根据市场情况选择是否行权。收益/损失是非对称的——损失有限（最多损失权利金），收益潜力巨大。

- **看涨期权 (Call Option)**：赋予买方在未来以约定价格（行权价 X）买入标的资产的权利。Call payoff = max(0, ST - X)。当标的资产价格上涨超过行权价时获利。
- **看跌期权 (Put Option)**：赋予买方在未来以约定价格卖出标的资产的权利。Put payoff = max(0, X - ST)。当标的资产价格下跌低于行权价时获利。
- **期权卖方 (Writer / Seller)**：收取权利金（premium），承担或有义务。当买方行权时，卖方必须履行合约。期权卖方的收益有限（最多为权利金），但损失可能非常大。
- **信用衍生品 (Credit Derivatives)**：仅在触发事件（如违约、降级）发生时支付。信用违约互换（CDS）是最常见的信用衍生品。
- 📐 Call payoff = max(0, ST - X)；Put payoff = max(0, X - ST)

**考试应用**：区分远期承诺与或有索取权是考试的起点。关键判断：双方有义务 → 远期承诺；一方有权利 → 或有索取权。payoff 计算是必考题型，需熟练掌握 max(0, ...) 公式。

### 知识点3：期权收益 vs 利润 (Payoff vs Profit)

**核心概念**：期权的到期收益（payoff）和利润（profit）是两个不同的概念。收益是行权的经济价值，不考虑权利金成本；利润是扣除权利金后的净盈亏。混淆 payoff 和 profit 是考试中最常见的错误之一。

- **Long call payoff**: max(0, ST - X)；**Long call profit**: max(0, ST - X) - c0
- **Long put payoff**: max(0, X - ST)；**Long put profit**: max(0, X - ST) - p0
- **Short call profit**: c0 - max(0, ST - X)（卖方收入权利金，承担义务）
- **Short put profit**: p0 - max(0, X - ST)
- 🎯 高频考点：payoff ≠ profit，payoff 不包括权利金

**考试应用**：payoff/profit 计算是 Derivatives 科目必考题。解题步骤：先判断 call/put → 判断 long/short → 代入 payoff 公式 → 若求 profit 则加减权利金。小心题目问的是 payoff 还是 profit。

### 知识点4：远期 vs 期货的核心区别 (Forwards vs Futures)

**核心概念**：远期和期货在本质上都是锁定未来价格的合约，但在交易场所、标准化程度、结算机制和风险管理方面有显著差异。理解这些差异是 Derivatives 科目的核心能力之一。

- **交易场所**：远期在 OTC 市场交易，期货在交易所交易
- **标准化**：远期定制化，期货标准化（合约规模、到期日统一）
- **结算机制**：远期到期一次结算，期货每日盯市结算
- **对手风险**：远期存在双边交易对手风险，期货通过 CCP 消除对手风险
- **保证金**：远期通常无保证金，期货有初始和维持保证金
- 💡 **核心理解**：期货是标准化远期 + 每日盯市结算 + 中央清算

**考试应用**：远期 vs 期货对比是高频考点。考试通常从 4-5 个维度要求对比，或给出一组特征判断属于远期还是期货。常见陷阱：认为期初价格不同（实际相同）、认为期货价值存续期波动（实际每日归零）。

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Call payoff = max(0, ST - X)` | 看涨期权到期收益，标的价格高于行权价时行权 | 计算 call 多头到期价值 | 收益 ≠ 利润，未扣除权利金 |
| `Put payoff = max(0, X - ST)` | 看跌期权到期收益，标的价格低于行权价时行权 | 计算 put 多头到期价值 | 收益 ≠ 利润，未扣除权利金 |
| `Long forward payoff = ST - K` | 远期多头到期收益 = 标的到期价 - 交割价 | 远期合约到期价值 | 负债可能无限大 (ST 下跌时) |
| `Short forward payoff = K - ST` | 远期空头到期收益 = 交割价 - 标的到期价 | 远期空头到期价值 | 负债可能无限大 (ST 上涨时) |
| `Forward commitment payoff = ΔUnderlying × Contract Size` | 远期承诺的收益与标的价格变动成比例 | 理解远期承诺的对称收益特征 | 双边义务，收益/损失对称 |
| `Contingent claim payoff = max(0, ...)` | 或有索取权的收益具有非对称性 | 理解期权的非线性收益 | 单边权利，损失有限(权利金) |

### 🛠️ 常见考点与解题思路

**考点1：区分远期承诺 vs 或有索取权**
- **步骤**：看双方是否有义务执行
  - 双方均有义务 → 远期承诺 (forward, futures, swap)
  - 一方有权利一方有义务 → 或有索取权 (option, credit derivative)
- **关键判断**：远期承诺的 payoff 对称；或有索取权的 payoff 非对称

**考点2：远期 vs 期货对比**
- **步骤**：从 4 个维度对比——交易场所、标准化程度、结算方式、风险类型
- **关键点**：期货是标准化的远期合约，但每日盯市结算改变了现金流模式

**考点3：计算期权到期 payoff**
- **步骤**：
  1. 判断是 call 还是 put
  2. 判断是 long 还是 short
  3. 代入公式：call/put 分别用 max(0, ST-X) 或 max(0, X-ST)
  4. 若是 short position，取负值
- **陷阱**：short call 的 payoff 是 -max(0, ST-X)，不是 max(0, X-ST)

**考点4：计算期权到期 profit**
- **步骤**：在 payoff 基础上减去权利金 (premium)
- **公式**：`Profit = Payoff - Premium` (long)；`Profit = Premium - Payoff` (short)
- **高频陷阱**：payoff 和 profit 混淆后整题方向全错

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| long forward 和 long call 都是看涨 | long forward 是义务必须买入，long call 是权利可以选择买入 | 义务与权利的本质区别 |
| swap 会交换名义本金 | 利率互换不交换名义本金，只交换净利息差额 | 名义本金只是计算基数 |
| 期权到期一定会行权 | 只有经济上有利时 (in-the-money) 才会行权 | 虚值期权到期自动失效 |
| 期货和远期完全相同 | 期货每日盯市结算，远期到期一次结算 | 结算机制不同导致现金流和信用风险不同 |
| short call 的 payoff 是 max(0, X-ST) | short call 的 payoff 是 -max(0, ST-X) | 卖方义务与买方权利对称相反 |

### 🔄 跨模块关联

- **[[M01-Derivative-Instrument-and-Derivative-Market-Features]]** — 市场结构 (交易所 vs OTC) 是合约分类的基础
- **[[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]]** — 远期合约的定价与估值
- **[[M06-Pricing-and-Valuation-of-Futures-Contracts]]** — 期货的定价与期货-远期价格差异
- **[[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]]** — 互换定价与估值
- **[[M08-Pricing-and-Valuation-of-Options]]** — 期权的深入定价与价值边界
- **[[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]]** — 二叉树模型为期权提供估值框架
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M02 是整个 Derivatives 科目中概念最密集的模块，几乎所有后续模块都依赖这里的分类
- **核心能力**：能快速区分一个工具属于远期承诺还是或有索取权
- **必考题型**：期权 payoff/profit 计算、远期/期货对比、互换的特点
- 记忆口诀：远期承诺有义务 (obligation)，或有索取权有权利 (right)
- 期货是标准化的远期合约，每日盯市结算
- 互换是一系列远期合约的组合
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
