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

### 📐 关键公式表

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
