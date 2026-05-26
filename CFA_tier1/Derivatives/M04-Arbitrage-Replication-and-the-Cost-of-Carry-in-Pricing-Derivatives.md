---
title: "M04 — Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
description: "CFA Level I 2026 official module: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
module: M04
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 4: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M04: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives
- 4.01 | Introduction
- 4.02 | Arbitrage
- 4.03 | Replication
- 4.04 | Costs and Benefits Associated with Owning the Underlying

## Learning Outcome Statements

The candidate should be able to:

- explain how the concepts of arbitrage and replication are used in pricing derivatives
- explain the difference between the spot and expected future price of an underlying and the cost of carry associated with holding the underlying asset

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M04: 套利、复制与持有成本 (Arbitrage, Replication, and Cost of Carry)
│
├── 🟢 核心思想：衍生品定价的三大支柱
│   ├── 无套利 (No-Arbitrage)
│   ├── 复制 (Replication)
│   └── 持有成本 (Cost of Carry)
│
├── ⭐ 无套利逻辑 (No-Arbitrage Logic)
│   ├── 一价定律 (Law of One Price)
│   │   └── 相同未来现金流的资产应有相同价格
│   │   └── 💡 这是所有衍生品定价的基石
│   ├── 复制组合 (Replication Portfolio)
│   │   ├── 用现货+融资复制衍生品收益
│   │   └── 确定公平价格的核心方法
│   └── 套利行为 (Arbitrage Action)
│       ├── 错误定价时套利者交易 → 价格回到公平关系
│       └── 🎯 高频考点：cash-and-carry / reverse cash-and-carry
│
├── ⭐ 持有成本关系 (Carry Relation)
│   ├── Forward price = Spot + Carry - Benefit
│   ├── Carry = Financing cost - Income/Yield/Convenience
│   ├── ➕ 融资成本 → 提高远期价格
│   ├── ➖ 已知收入 → 减少持有成本
│   └── ➖ 收益率/便利收益 → 减少持有成本
│
├── 📐 三大定价公式
│   ├── 🅰 无收益资产: F0(T) = S0(1+r)^T
│   │   └── 现货以无风险利率增长
│   ├── 🅱 已知收入: F0(T) = [S0 - PV(I)](1+r)^T
│   │   └── 先扣收入现值再前滚 ⚠️ 收入需折现
│   └── 🅲 已知收益率: F0(T) = S0[(1+r)/(1+q)]^T
│       └── 收益率 q 降低持有成本
│
├── ⭐ 套利策略 (Arbitrage Strategies)
│   ├── Cash-and-Carry (价格偏高)
│   │   ├── Short forward + Buy underlying + Borrow
│   │   └── 锁定无风险利润
│   └── Reverse Cash-and-Carry (价格偏低)
│       ├── Long forward + Short underlying + Invest
│       └── 锁定无风险利润
│
├── 💡 关键洞察
│   ├── 期初价格 ≠ 存续期价值（Price ≠ Value）
│   ├── 套利机会在有效市场中转瞬即逝
│   └── 复制组合证明衍生品不存在"额外价值"
│
└── ⚠️ 考试陷阱
    ├── 已知收入要先折现再扣减
    ├── 连续复利与离散复利公式不要混用
    └── 套利需要同时交易所有头寸（无风险）
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `F0(T) = S0(1+r)^T` | 无收益资产远期价格 = 现货 × (1+r)^T | 无股利股票、零息债券的远期定价 | r 为无风险利率，T 以年为单位 |
| `F0(T) = [S0 - PV(I)](1+r)^T` | 已知收入资产远期价格 = (现货 - 收入现值) × (1+r)^T | 付息债券、股利支付股票的远期定价 | 已知收入必须先折现再扣减 |
| `F0(T) = S0[(1+r)/(1+q)]^T` | 已知收益率资产远期价格 | 股指、外汇的远期定价 | 连续复利: `F = S × e^{(r-q)T}` |
| `Forward price = Spot + Carry - Benefit` | 通用持有成本关系 | 理解远期价格的决定因素 | Carry = 融资成本 - 持有收益 |
| `Cash-and-Carry: 利润 = Fmarket - Ffair` | 市场价高于公平价时的套利 | 识别套利机会 | 需同时交易所有头寸 |
| `Reverse Cash-and-Carry: 利润 = Ffair - Fmarket` | 市场价低于公平价时的套利 | 识别套利机会 | 需借入标的资产做空 |

### 🛠️ 常见考点与解题思路

**考点1：计算 fair forward price**
- **步骤**：
  1. 判断资产的收益类型 (无收益 / 已知收入 / 已知收益率)
  2. 选择对应的 carry 公式
  3. 代入已知数值计算
  4. 注意复利频率（离散 vs 连续）
- **常见陷阱**：已知收入必须用 PV(I) 而非未来值 I

**考点2：识别和构建套利策略**
- **步骤**：
  1. 比较市场价 Fmarket 与公平价 Ffair
  2. Fmarket > Ffair → 价格偏高 → Cash-and-Carry: Short forward + Buy spot + Borrow
  3. Fmarket < Ffair → 价格偏低 → Reverse Cash-and-Carry: Long forward + Short spot + Invest
  4. 验证所有头寸在期初净现金流为零
- **关键**：套利必须在期初净投资为零且期末获得确定的正利润

**考点3：区分 Price vs Value**
- **步骤**：
  - Price (F0(T))：新合约的公平交割价，使合约初始价值为零
  - Value (Vt)：现有合约当前值多少钱，可正可负
- **陷阱**：期初价格与存续期价值不是同一概念

**考点4：连续 vs 离散复利的选择**
- **步骤**：看题目给出的利率类型
  - 年利率 → 离散复利 `(1+r)^T`
  - 连续利率 → 连续复利 `e^{rT}`
- **陷阱**：两种公式不可混用

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 期初价格 = 存续期价值 | 期初 Price 是使价值为零的交割价，存续期 Value 可正可负 | Price 与 Value 的定义不同 |
| 已知收入直接用未来值扣减 | 已知收入需先折现到当前再扣减 | 现金流时间价值不同 |
| 离散和连续复利公式可互换 | 两种公式对应不同利率口径，需严格对应 | 数学形式不同，结果不同 |
| 套利需要初始资金 | 无风险套利期初净现金流量为零 | 套利定义要求零初始投资 |
| Forward price 是预期未来现货价格 | Forward price 由无套利决定，不是预期 | 预期用远期利率/价格反映的是无套利关系 |
| 套利机会长期存在 | 套利机会转瞬即逝，套利者会迅速消除价差 | 有效市场中套利是自我校正机制 |

### 🔄 跨模块关联

- **[[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]]** — M04 的 carry 关系是 M05 远期定价的基础
- **[[M06-Pricing-and-Valuation-of-Futures-Contracts]]** — 期货定价同样沿用无套利框架，但需考虑每日盯市
- **[[M08-Pricing-and-Valuation-of-Options]]** — 无套利逻辑同样适用于期权价值边界
- **[[M09-Option-Replication-Using-Put-Call-Parity]]** — Put-call parity 本质是无套利关系的体现
- **[[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]]** — 二项式模型本质也是无套利复制
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M04 是整个 Derivatives 定价的**理论基础**，后续所有定价模块都依赖这里的概念
- **核心能力**：掌握三种资产类型的 carry 公式，理解 cash-and-carry 套利
- **必考题型**：远期 fair price 计算、套利策略识别、Price vs Value 区别
- 记忆重点：无套利 → 复制 → 定价；三种资产类型对应三种公式
- 套利策略记忆法：
  - 价格偏高 → 卖远期/买现货/借钱 (Cash-and-Carry)
  - 价格偏低 → 买远期/卖现货/投资 (Reverse Cash-and-Carry)
- 最重要的习惯：确认复利频率再代入公式
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
