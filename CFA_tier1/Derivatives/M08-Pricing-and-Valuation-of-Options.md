---
title: "M08 — Pricing and Valuation of Options"
description: "CFA Level I 2026 official module: Pricing and Valuation of Options"
module: M08
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 8: Pricing and Valuation of Options"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M08: Pricing and Valuation of Options

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Pricing and Valuation of Options
- 8.01 | Introduction
- 8.02 | Option Value relative to the Underlying Spot Price
- 8.03 | Option Exercise Value
- 8.04 | Option Moneyness
- 8.05 | Option Time Value
- 8.06 | Arbitrage
- 8.07 | Replication
- 8.08 | Factors Affecting Option Value

## Learning Outcome Statements

The candidate should be able to:

- explain the exercise value, moneyness, and time value of an option
- contrast the use of arbitrage and replication concepts in pricing forward commitments and contingent claims
- identify the factors that determine the value of an option and describe how each factor affects the value of an option

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M08: 期权定价与估值 (Options Pricing and Valuation)
│
├── 🟢 核心概念：期权赋予权利但非义务
│   └── 非线性收益特征 (non-linear payoff) 区别于远期承诺
│
├── ⭐ 期权收益 (Payoff) 与利润 (Profit)
│   ├── Call payoff: max(0, ST - X)
│   ├── Put payoff: max(0, X - ST)
│   ├── Long call profit: max(0, ST - X) - c0
│   ├── Long put profit: max(0, X - ST) - p0
│   └── 🎯 高频考点：payoff ≠ profit
│
├── ⭐ 关键概念
│   ├── 内在价值 (Intrinsic Value / Exercise Value)
│   │   └── 立即行权的经济价值
│   │   └── Call: max(0, S - X)；Put: max(0, X - S)
│   ├── 时间价值 (Time Value)
│   │   ├── 期权价格 - 内在价值
│   │   └── 反映未来标的价格变动的不确定性价值
│   ├── 实值状态 (Moneyness)
│   │   ├── ITM (实值): S > X (call), S < X (put)
│   │   ├── ATM (平值): S = X
│   │   └── OTM (虚值): S < X (call), S > X (put)
│   └── ⚠️ Moneyness 取决于当前价格，非到期价格
│
├── ⭐ 期权价值影响因素 (六因素)
│   ├── 标的资产价格 S ↑ → Call ↑, Put ↓
│   ├── 行权价 X ↑ → Call ↓, Put ↑
│   ├── 到期时间 T ↑ → Call ↑, Put ↑ (美式期权)
│   ├── 波动率 σ ↑ → Call ↑, Put ↑ ⭐ 双向影响
│   ├── 无风险利率 r ↑ → Call ↑, Put ↓
│   └── 持有收益/股利 → Call ↓, Put ↑
│
├── ⭐ 期权价值边界 (European Options)
│   ├── Call 下限: c ≥ max(0, S0 - PV(X))
│   ├── Put 下限: p ≥ max(0, PV(X) - S0)
│   └── 美式期权价值 ≥ 对应欧式期权
│
├── 📐 关键公式
│   ├── Call payoff = max(0, ST - X)
│   ├── Put payoff = max(0, X - ST)
│   ├── Call profit = max(0, ST - X) - c0
│   ├── Put profit = max(0, X - ST) - p0
│   ├── Call 下限: c ≥ max(0, S0 - PV(X))
│   └── Put 下限: p ≥ max(0, PV(X) - S0)
│
├── 💡 关键洞察
│   ├── 期权价格 = 内在价值 + 时间价值
│   ├── 波动率是期权价值的最独特因素 (对远期无影响)
│   ├── 无套利原理同样适用于期权价值边界
│   └── 美式期权 ≥ 欧式期权 (提前行权权利有价值)
│
└── ⚠️ 考试陷阱
    ├── payoff 不是 profit (忘记减权利金)
    ├── 内在价值不是期权价格 (还要加时间价值)
    ├── 波动率上升 → 所有期权价值上升
    └── 美式期权可能有更高价值 (提前行权)
```

## 📖 知识点详解

### 知识点1：期权收益与利润 (Option Payoff and Profit)

**核心概念**：期权的到期收益（payoff）和利润（profit）是理解期权价值的基础。Payoff 是行权时的经济价值，不包括权利金成本；profit 是扣除权利金后的净盈亏。考生必须严格区分这两者，因为考试中混淆 payoff 和 profit 是最常见的错误之一。

- **Call payoff** = max(0, ST - X)：当标的价格 ST 高于行权价 X 时行权，收益为 ST - X；否则不行权，收益为零
- **Put payoff** = max(0, X - ST)：当标的价格 ST 低于行权价 X 时行权，收益为 X - ST；否则不行权，收益为零
- **Long call profit** = max(0, ST - X) - c0：payoff 减去支付的权利金
- **Long put profit** = max(0, X - ST) - p0：payoff 减去支付的权利金
- **Short position profit** 与 long 对称相反：short call profit = c0 - max(0, ST - X)
- 🎯 **高频考点**：payoff ≠ profit。Payoff 不包括权利金，考试中经常故意混淆

**考试应用**：计算 payoff/profit 是 Derivatives 科目必考题。解题步骤：① 判断 call/put；② 判断 long/short；③ 代入 payoff 公式 max(0, ...)；④ 若求 profit 则加减权利金。注意 short call 的 payoff 是 -max(0, ST-X)，不是 max(0, X-ST)。

### 知识点2：期权的内在价值、时间价值与实值状态 (Intrinsic Value, Time Value, and Moneyness)

**核心概念**：期权价格由内在价值和时间价值两部分组成。内在价值是立即行权的经济价值，时间价值反映未来不确定性的价值。实值状态（moneyness）描述当前标的价格与行权价的关系，决定期权是否处于有利可图的状态。

- **内在价值 (Intrinsic Value / Exercise Value)**：Call 的内在价值 = max(0, S - X)；Put 的内在价值 = max(0, X - S)。深度实值期权的价格接近内在价值
- **时间价值 (Time Value)** = 期权价格 - 内在价值。到期时间越长、波动率越高，时间价值越大。到期时时间价值归零
- **实值状态 (Moneyness)**：
  - ITM (实值, In-the-Money)：Call 的 S > X；Put 的 S < X
  - ATM (平值, At-the-Money)：S = X
  - OTM (虚值, Out-of-the-Money)：Call 的 S < X；Put 的 S > X
- 💡 ITM 不一定盈利（profit 还需考虑已支付的权利金）。Moneyness 取决于当前价格，非到期价格

**考试应用**：判断 moneyness 是期权的基本功。给定 S 和 X，判断是 ITM/ATM/OTM。注意：Call 和 Put 的 ITM 条件相反。常见陷阱：ITM 期权 = 行权有利，但 profit 可能仍为负（因已支付权利金）。

### 知识点3：影响期权价值的六因素 (Six Factors Affecting Option Value)

**核心概念**：期权价值受六个因素的影响，其中标的资产价格、行权价、到期时间、波动率、无风险利率和持有收益/股利。理解每个因素对看涨和看跌期权的不同影响方向是期权定价的核心。

- **标的资产价格 S**：S↑ → Call↑, Put↓（Call 随标的价格上涨而增值）
- **行权价 X**：X↑ → Call↓, Put↑（高价行权价降低 Call 价值）
- **到期时间 T**：T↑ → Call↑, Put↑（美式期权；欧式期权不确定，因股利可能降低价值）
- **波动率 σ**：σ↑ → Call↑, Put↑ ⭐ 波动率是唯一对 Call 和 Put 都有正向影响的因素
- **无风险利率 r**：r↑ → Call↑, Put↓（高利率降低行权价现值）
- **持有收益/股利**：div↑ → Call↓, Put↑（股利降低持有标的资产的吸引力）
- 🎯 **高频考点**：波动率对 Call 和 Put 都是正向影响，其他因素方向相反

**考试应用**：六因素分析是高频概念题。给定因素变化方向，判断对 Call/Put 价值的影响。记忆口诀：Call 六因素 S↑(+) X↑(-) T↑(+) σ↑(+) r↑(+) div(-)；Put 与 Call 在 S、X、r、div 方向相反。波动率 σ 是唯一双向正向的因素。

### 知识点4：期权价值边界 (Option Value Bounds)

**核心概念**：欧式期权的价格存在理论下限。如果市场价格低于下限，就存在套利机会。价值边界由无套利条件推导得出，是理解和应用 put-call parity 的基础。

- **欧式看涨下限**：c ≥ max(0, S0 - PV(X))。看涨期权的价格至少不低于标的资产现价减去行权价现值
- **欧式看跌下限**：p ≥ max(0, PV(X) - S0)。看跌期权的价格至少不低于行权价现值减去标的资产现价
- 美式期权的价值通常不低于对应欧式期权，因为提前行权的权利不会降低价值
- 💡 如果市场价格低于理论下限，套利者可以买入期权并卖空标的资产/无风险资产，锁定无风险利润

**考试应用**：价值边界题通常要求比较市场价格与理论下限，判断是否存在套利机会。注意：下限仅适用于欧式期权。常见陷阱：忘记期权价格包含时间价值，价格高于内在价值是正常的，但低于理论下限则不正常。

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Call payoff = max(0, ST - X)` | 看涨期权到期收益 | 计算 call 持有人的到期价值 | payoff 不是 profit |
| `Put payoff = max(0, X - ST)` | 看跌期权到期收益 | 计算 put 持有人的到期价值 | payoff 不是 profit |
| `Long call profit = max(0, ST - X) - c0` | 多头看涨期权利润 | 计算净盈亏（含权利金） | 空头利润对称相反 |
| `Long put profit = max(0, X - ST) - p0` | 多头看跌期权利润 | 计算净盈亏（含权利金） | 注意权利金方向 |
| `c ≥ max(0, S0 - PV(X))` | 欧式看涨下限 | 识别套利机会（价格低于下限时） | 仅适用于欧式期权 |
| `p ≥ max(0, PV(X) - S0)` | 欧式看跌下限 | 识别套利机会（价格低于下限时） | 仅适用于欧式期权 |
| `期权价格 = 内在价值 + 时间价值` | 期权定价分解 | 理解期权价格构成 | 深度 ITM 期权的 time value ≈ 0 |

### 🛠️ 常见考点与解题思路

**考点1：计算期权 payoff 和 profit**
- **步骤**：
  1. 确定是 call 还是 put
  2. 确定是 long 还是 short
  3. Payoff: 代入 max(0, ...) 公式
  4. Profit: payoff - 权利金 (long)；权利金 - payoff (short)
- **高频陷阱**：payoff 和 profit 混淆导致整题全错

**考点2：判断期权实值状态 (Moneyness)**
- **步骤**：
  1. 比较当前标的价 S 与行权价 X
  2. Call: S > X → ITM；S = X → ATM；S < X → OTM
  3. Put: S < X → ITM；S = X → ATM；S > X → OTM
- **关键**：ITM 不一定盈利（还需考虑已支付的权利金）

**考点3：分析影响期权价值的因素**
- **步骤**：给定因素的变化方向 → 判断对 call/put 的影响
- **记忆口诀**：
  - Call 六因素：S↑(+) X↑(-) T↑(+) σ↑(+) r↑(+) div(-)
  - Put 六因素：S↑(-) X↑(+) T↑(+) σ↑(+) r↑(-) div(+)
- **注意**：所有因素对欧式和美式期权的影响方向相同，但美式的 T 效应更强

**考点4：期权价值边界判断**
- **步骤**：
  1. 计算下限 (low bound)
  2. 如果市场价格低于下限 → 存在套利机会
  3. 买入期权、卖空标的/无风险资产
- **陷阱**：下限仅适用于欧式期权，美式期权下限可能更高

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| Payoff = Profit | Payoff 不包括权利金，Profit 包括 | Profit = Payoff - Premium (long) |
| 内在价值 = 期权价格 | 期权价格 = 内在价值 + 时间价值 | 时间价值反映未来不确定性 |
| 波动率上升只影响 call | 波动率上升 → 所有期权价值均上升 | 波动率增加两端可能性 |
| ITM 期权一定盈利 | ITM 表示行权有利，但 profit 可能仍为负 | 因已支付权利金 |
| 到期时间越长期权价值一定越高 | 美式期权如此，欧式不一定（股利可能降低价值） | 提前行权权差异 |
| 所有期权都有时间价值 | 深度 ITM 且快到期的期权时间价值 ≈ 0 | 时间价值在到期时归零 |

### 🔄 跨模块关联

- **[[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]]** — 无套利原理用于期权价值边界，复制用于合成期权
- **[[M09-Option-Replication-Using-Put-Call-Parity]]** — Put-call parity 是期权价值关系的重要体现
- **[[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]]** — 二叉树模型为期权提供估值框架
- **[[M02-Forward-Commitment-and-Contingent-Claim-Features-and-Instruments]]** — 期权作为或有索取权的基本概念在 M02 中介绍
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M08 是 Derivatives 科目中非常重要的模块，引入期权这一核心衍生品类别
- **核心能力**：计算 payoff/profit、判断 moneyness、理解六因素影响
- **必考题型**：期权 payoff/profit 计算、六因素分析、价值边界判断
- **最常犯错误**：payoff 和 profit 的区分、六因素中 r 和 div 对 call/put 的相反影响
- 记忆技巧：
  - 六因素用"一表记"：S, X, T, σ, r, div
  - 波动率 σ 对 call 和 put 都是正向影响
  - 其他因素方向相反 (call 和 put)
- 期权价值边界题：比较市场价格和理论下限
