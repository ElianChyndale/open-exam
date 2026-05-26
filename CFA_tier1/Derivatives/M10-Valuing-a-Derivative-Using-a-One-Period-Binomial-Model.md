---
title: "M10 — Valuing a Derivative Using a One-Period Binomial Model"
description: "CFA Level I 2026 official module: Valuing a Derivative Using a One-Period Binomial Model"
module: M10
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 10: Valuing a Derivative Using a One-Period Binomial Model"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M10: Valuing a Derivative Using a One-Period Binomial Model

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Valuing a Derivative Using a One-Period Binomial Model
- 10.01 | Introduction
- 10.02 | Binomial Valuation
- 10.03 | The Binomial Model
- 10.04 | Pricing a European Call Option
- 10.05 | Risk Neutrality

## Learning Outcome Statements

The candidate should be able to:

- explain how to value a derivative using a one-period binomial model
- describe the concept of risk neutrality in derivatives pricing

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M10: 单期二叉树模型估值 (One-Period Binomial Model)
│
├── 🟢 核心思想：通过两种等价方法为期权定价
│   ├── 复制法 (Replication Approach)
│   └── 风险中性法 (Risk-Neutral Approach)
│   └── 💡 两种方法得出相同结果
│
├── ⭐ 复制法 (Replication Approach)
│   ├── 构建复制组合: Δ 份标的资产 + 无风险借贷
│   ├── 对冲比率 (Hedge Ratio / Delta)
│   │   └── h = (Cu - Cd) / (Su - Sd)
│   │   └── 💡 每份期权所需标的资产份数
│   ├── 复制组合价值: V0 = h × S0 + B
│   ├── 借贷头寸 B: B = (Cd - h × Sd) / (1+r)
│   │   └── B 可为正（贷出）或负（借入）
│   └── 🎯 高频考点：计算 h, B, V0
│
├── ⭐ 风险中性法 (Risk-Neutral Approach)
│   ├── 上涨因子 u (up factor)
│   ├── 下跌因子 d (down factor)
│   │   └── 通常 u > 1 > d > 0, 且 u×d = 1
│   ├── 风险中性概率 p*
│   │   └── p* = [(1+r) - d] / (u - d)
│   │   └── ⚠️ 不是真实世界概率！
│   ├── 期权价值: V0 = [p* × Vu + (1-p*) × Vd] / (1+r)
│   └── 🎯 高频考点：计算 p*, 期望值, 贴现
│
├── ⭐ 关键关系
│   ├── 复制法和风险中性法等价
│   ├── 风险中性概率与投资者风险偏好无关
│   ├── 波动率影响: σ↑ → 状态价差↑ → 期权价值↑
│   └── u 和 d 的关系: u = e^{σ√T}, d = e^{-σ√T} (连续)
│
├── 📐 完整计算流程
│   ├── ① 给定 S0, u, d, r → 计算 Su = S0×u, Sd = S0×d
│   ├── ② 计算期权在上涨/下跌状态的 payoff
│   │   ├── Call: Cu = max(0, Su-X), Cd = max(0, Sd-X)
│   │   └── Put: Pu = max(0, X-Su), Pd = max(0, X-Sd)
│   ├── ③ 复制法: 计算 h = (Cu-Cd)/(Su-Sd), B, V0
│   └── ④ 风险中性法: 计算 p*, V0 = [p*Vu+(1-p*)Vd]/(1+r)
│
├── 💡 关键洞察
│   ├── 二叉树核心 = 无套利复制
│   ├── 风险中性概率是定价工具，不是预测
│   ├── 单期可扩展到多期（Level I 只考单期）
│   └── 波动率是唯一不在二叉树直接可见的影响因素
│
└── ⚠️ 考试陷阱
    ├── p* 不是真实概率 (不可用于预测)
    ├── 不要忘记贴现步骤
    ├── h 必须与状态收益匹配
    └── B 可为正（贷出）或负（借入）
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `h = (Cu - Cd) / (Su - Sd)` | 对冲比率 = 期权利润差 / 股价差 | 复制法第一步 | 需先计算 Su, Sd 和期权 payoff |
| `B = (Cd - h×Sd) / (1+r)` | 无风险借贷头寸 | 复制法第二步 | B 可正可负 |
| `V0 = h×S0 + B` | 复制组合价值 = 期权公平价格 | 复制法最终结果 | 与风险中性法结果一致 |
| `p* = [(1+r) - d] / (u - d)` | 风险中性上涨概率 | 风险中性法第一步 | 不是真实概率 |
| `V0 = [p*×Vu + (1-p*)×Vd] / (1+r)` | 风险中性期权价值 = 期望现值 | 风险中性法最终结果 | 必须先计算 p* 和 Vu, Vd |
| `Su = S0 × u` | 上涨状态股价 | 计算状态价格 | u 通常 > 1 |
| `Sd = S0 × d` | 下跌状态股价 | 计算状态价格 | d 通常 < 1 |

### 🛠️ 常见考点与解题思路

**考点1：复制法完整计算**
- **步骤**：
  1. 计算 Su = S0 × u, Sd = S0 × d
  2. 计算期权 payoff: 上涨状态 Vu, 下跌状态 Vd
  3. 计算 h = (Vu - Vd) / (Su - Sd)
  4. 计算 B = (Vd - h × Sd) / (1+r)
  5. V0 = h × S0 + B
- **验证**：上涨状态下 h×Su + B×(1+r) 应等于 Vu

**考点2：风险中性法完整计算**
- **步骤**：
  1. 计算 Su, Sd 和期权 payoff
  2. 计算 p* = [(1+r) - d] / (u - d)
  3. V0 = [p* × Vu + (1-p*) × Vd] / (1+r)
- **关键理解**：p* 是确保无套利的数学权重

**考点3：对冲比率的意义**
- **步骤**：
  - h 表示每份期权需要多少份标的资产来复制
  - h > 0 表示买入标的资产可复制 call
  - h < 0 表示做空标的资产可复制 put (实际上 put 的 h 为负)
- **常见题型**：给定期权和标的参数，计算 h，再问买卖方向

**考点4：波动率对二叉树的影响**
- **步骤**：
  - u = e^{σ√T}, d = e^{-σ√T}
  - 波动率 ↑ → u ↑, d ↓ → 状态价差扩大 → 期权价值 ↑
- **关键**：二叉树中波动率通过 u/d 影响定价

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| p* 是真实股票上涨概率 | p* 是无套利定价的数学工具 | 风险中性概率与真实概率无关 |
| 风险中性期望值就是期权价值 | 期望值需贴现到当前：V0 = E[V]/(1+r) | 时间价值需折现 |
| 对冲比率固定不变 | 每期的 h 可能不同（多期二叉树） | Delta 随价格变化 |
| B 一定是借入资金（负值） | B 可为正（贷出）或负（借入） | 复制组合需要融资或投资 |
| 复制法和风险中性法结果不同 | 两种方法数学等价，结果相同 | 自然对偶关系 |
| 二叉树只适用于看涨期权 | 二叉树可对任何衍生品估值 | 只需调整 payoff 函数 |

### 🔄 跨模块关联

- **[[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]]** — 二叉树复制法是无套利定价的直接应用
- **[[M08-Pricing-and-Valuation-of-Options]]** — 二叉树为期权提供具体的估值方法
- **[[M09-Option-Replication-Using-Put-Call-Parity]]** — 二叉树可推导或验证 put-call parity
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M10 是 Derivatives 科目的**最后一个模块**，也是计算题较密集的模块
- **核心能力**：熟练掌握复制法和风险中性法两种方法
- **必考题型**：对冲比率计算、风险中性概率计算、期权价值计算
- **最常犯错误**：忘记贴现步骤、p* 公式中分子计算错误、认为 p* 是真实概率
- 记忆技巧：
  - 复制法三步骤：h → B → V0
  - 风险中性法两步骤：p* → V0
  - 两种方法结果相同，可作为验算
- 核心理解：二叉树 = 无套利 + 复制，所有衍生品都可由此定价
- 不需要记忆 u 和 d 的公式（题目会给出），只需理解波动率对 u/d 的影响
