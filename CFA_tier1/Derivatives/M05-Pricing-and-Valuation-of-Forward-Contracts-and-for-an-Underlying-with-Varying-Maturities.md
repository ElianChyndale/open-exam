---
title: "M05 — Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities"
description: "CFA Level I 2026 official module: Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities"
module: M05
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 5: Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M05: Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities
- 5.01 | Introduction
- 5.02 | Pricing and Valuation of Forward Contracts
- 5.03 | Pricing and Valuation of Interest Rate Forward Contracts

## Learning Outcome Statements

The candidate should be able to:

- explain how the value and price of a forward contract are determined at initiation, during the life of the contract, and at expiration
- explain how forward rates are determined for interest rate forward contracts and describe the uses of these forward rates.

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M05: 远期合约定价与估值 (Forward Pricing and Valuation)
│
├── 🟢 核心区分：Price (价格) vs Value (价值)
│   ├── Price (F0(T))：新合约的公平交割价，期初价值为零
│   └── Value (Vt)：现有合约的当前价值，可正可负
│
├── ⭐ 三种资产的远期定价 (Forward Pricing)
│   ├── 🅰 无收益资产 (No-Income)
│   │   └── F0(T) = S0(1+r)^T
│   │   └── 💡 现货以无风险利率增长
│   ├── 🅱 已知收入 (Known Income)
│   │   └── F0(T) = [S0 - PV(I)](1+r)^T
│   │   └── ⚠️ 收入必须先折现再扣减
│   └── 🅲 已知收益率 (Known Yield)
│       └── F0(T) = S0[(1+r)/(1+q)]^T 或 S0e^{(r-q)T}
│       └── 💡 收益率 q 降低持有成本
│
├── ⭐ 合约价值 (Contract Value)
│   ├── 期初价值 V0 = 0 (公平价格定义)
│   ├── 存续期多头价值 Vt = St - PVt(K)
│   │   └── 🎯 高频考点：区分期初 vs 存续期
│   ├── 到期多头收益 = ST - K
│   └── 到期空头收益 = K - ST
│
├── ⭐ 利率远期 (Interest Rate Forward / FRA)
│   ├── FRA 是锁定未来借款/贷款利率的协议
│   ├── 基于隐含远期利率 (implied forward rate)
│   └── 结算基于 LIBOR 替代参考利率
│
├── 📐 公式速查
│   ├── 无收益: F0(T) = S0(1+r)^T
│   ├── 已知收入: F0(T) = [S0 - PV(I)](1+r)^T
│   ├── 已知收益率: F0(T) = S0[(1+r)/(1+q)]^T
│   ├── 存续期价值: Vt = St - PVt(K)
│   ├── 多头到期收益: ST - K
│   └── 空头到期收益: K - ST
│
├── 💡 关键洞察
│   ├── Forward Price 不是预期未来价格，是无套利结果
│   ├── FRA 的定价基础是隐含远期利率
│   └── 三种资产类型覆盖 Level I 所有远期场景
│
└── ⚠️ 考试陷阱
    ├── Forward Price ≠ Forward Value
    ├── 已知收入必须折现
    ├── 连续/离散复利不可混用
    └── FRA 是 OTC 合约，不是交易所产品
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `F0(T) = S0(1+r)^T` | 无收益资产远期公平价格 | 零息债券、无股利股票的远期定价 | r 为无风险利率，T 以年为单位 |
| `F0(T) = [S0 - PV(I)](1+r)^T` | 已知收入资产远期公平价格 | 付息债券、股利支付股票的远期定价 | PV(I) = I/(1+r)^t，收入时间可能不等同于合约到期 |
| `F0(T) = S0[(1+r)/(1+q)]^T` | 已知收益率资产（离散）远期价格 | 股指远期（股利收益率 q） | q 为连续或离散收益率 |
| `F0(T) = S0 × e^{(r-q)T}` | 已知收益率资产（连续）远期价格 | 外汇远期 (r 和 q 为两国利率) | 连续复利版本 |
| `Vt(long) = St - PVt(K)` | 无收益资产多头存续期价值 | 评估远期合约当前价值 | PVt(K) = K/(1+r)^{T-t} |
| `Long payoff = ST - K` | 多头远期到期收益 | 计算合约到期价值 | K 为合约约定的交割价 |
| `Short payoff = K - ST` | 空头远期到期收益 | 计算空头到期价值 | 与多头对称相反 |

### 🛠️ 常见考点与解题思路

**考点1：定价题 (计算 fair forward price)**
- **步骤**：
  1. 识别标的资产类型（无收益/已知收入/已知收益率）
  2. 选择对应公式
  3. 确认复利频率（离散 `(1+r)^T` 或连续 `e^{rT}`）
  4. 代入数值计算
- **常见陷阱**：已知收入必须用现值 PV(I) 而不是未来值 I

**考点2：估值题 (计算存续期合约价值)**
- **步骤**：
  1. 区分是期初还是存续期
  2. 若是存续期，用当前现货价格 St
  3. 计算交割价 K 的现值 PVt(K)
  4. Vt(long) = St - PVt(K)
- **关键**：估值时用当前时间 t 的折现因子，不是期初的

**考点3：远期 vs 期货差异**
- **步骤**：关注每日盯市的影响
  - 远期：到期一次结算，存续期价值波动
  - 期货：每日结算，存续期价值每日归零
- **注意**：Level I 主要考概念区别，不要求期货估值计算

**考点4：利率远期 (FRA) 理解**
- **步骤**：
  1. FRA 锁定未来一段时间的利率
  2. 隐含远期利率基于无套利关系
  3. 到期现金结算，基于市场利率与合约利率的差额
- **常见题型**：给定即期利率曲线，计算隐含远期利率

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| Forward Price = Forward Value | Price 是新合约的交割价，Value 是现有合约的当前价值 | 定义不同，Price 使初始 Value=0 |
| Forward Price 是预期未来价格 | Forward Price 是由无套利关系决定的 | 预期未来价格受风险偏好影响 |
| 已知收入直接用未来值减 | 已知收入必须先折现再扣减 | 时间价值差异 |
| 连续和离散公式可互换 | 两种公式对应不同利率口径，不能混用 | 数学形式不同 |
| 存续期多头价值 = ST - K | 存续期多头价值 = St - PVt(K)，到期才是 ST - K | Vt 用当前 spot，到期用到期 spot |
| FRA 的 fixed rate 是预期未来利率 | FRA 的 fixed rate 由无套利决定 | 远期利率不是预测，是无套利结果 |

### 🔄 跨模块关联

- **[[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]]** — M04 的 carry 关系是 M05 所有定价公式的基础
- **[[M06-Pricing-and-Valuation-of-Futures-Contracts]]** — 期货与远期定价框架相同，但结算机制不同导致价格可能差异
- **[[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]]** — 利率互换可视为一系列 FRA 的組合
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M05 是 Derivatives 科目中计算题最密集的模块之一
- **核心能力**：熟练掌握三种资产类型的定价公式，区分 Price 与 Value
- **必考题型**：计算 fair forward price、计算存续期合约价值、区分远期 vs 期货
- **最常犯错误**：忘记已知收入需折现、混淆 Price 和 Value、复利频率用错
- 记忆技巧：将所有定价公式统一为 `F = S + Carry - Benefit`，再推导具体公式
- 估值公式 `Vt = St - PVt(K)` 适用于无收益资产，有收益资产需加回收入的现值
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
