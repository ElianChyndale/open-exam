---
title: "M09 — Option Replication Using Put-Call Parity"
description: "CFA Level I 2026 official module: Option Replication Using Put-Call Parity"
module: M09
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 9: Option Replication Using Put-Call Parity"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M09: Option Replication Using Put-Call Parity

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Option Replication Using Put-Call Parity
- 9.01 | Introduction
- 9.02 | Put-Call Parity
- 9.03 | Option Strategies Based on Put-Call Parity
- 9.04 | Put-Call Forward Parity and Option Applications
- 9.05 | Put-Call Forward Parity
- 9.06 | Option Put-Call Parity Applications: Firm Value

## Learning Outcome Statements

The candidate should be able to:

- explain put-call parity for European options
- explain put-call forward parity for European options

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M09: 买卖权平价与期权复制 (Put-Call Parity and Option Replication)
│
├── 🟢 核心公式：c + PV(X) = p + S0
│   └── 适用于：欧式期权（到期日相同、执行价相同）
│   └── 💡 经济含义：保护性看跌 + 股票 = 看涨 + 无风险资产
│
├── ⭐ 标准平价公式 (Standard Put-Call Parity)
│   ├── c + PV(X) = p + S0
│   ├── 左侧：Fiduciary Call (看涨 + 无风险资产)
│   ├── 右侧：Protective Put (看跌 + 标的资产)
│   └── 🎯 本质：无套利关系的体现
│
├── ⭐ 有收入资产的调整
│   ├── 已知现金收入: c + PV(X) + PV(I) = p + S0
│   │   └── 在左侧加入股利现值（资产持有者获得股利）
│   └── 连续收益率: c + PV(X) = p + S0e^{-qT}
│       └── 收益率 q 降低标的资产的现值
│
├── ⭐ 合成头寸 (Synthetic Positions)
│   ├── 合成看涨 (Synthetic Call): c = p + S0 - PV(X)
│   ├── 合成看跌 (Synthetic Put): p = c - S0 + PV(X)
│   ├── 合成股票 (Synthetic Stock): S0 = c + PV(X) - p
│   ├── 合成无风险资产: PV(X) = c + S0 - p
│   └── 🎯 高频考点：平价公式移项得到合成头寸
│
├── ⭐ 买卖权远期平价 (Put-Call Forward Parity)
│   ├── c + PV(X) = p + PV(F)
│   │   └── F 为远期合约价格
│   └── 用远期代替现货：c + PV(X) = p + F0(T)/(1+r)^T
│
├── ⭐ 期权价值边界 (Option Value Bounds)
│   ├── 看涨下限: c ≥ max(0, S0 - PV(X))
│   ├── 看跌下限: p ≥ max(0, PV(X) - S0)
│   └── 💡 可由平价公式推导
│
├── 📐 公式速查
│   ├── c + PV(X) = p + S0               (标准平价)
│   ├── c + PV(X) + PV(I) = p + S0       (有现金收入)
│   ├── c + PV(X) = p + S0e^{-qT}        (有收益率)
│   ├── c + PV(X) = p + PV(F)            (远期平价)
│   └── c ≥ max(0, S0 - PV(X))           (看涨下限)
│
├── 💡 关键洞察
│   ├── PCP 是无套利关系，不是预测模型
│   ├── PCP 是精确等式（忽略交易成本）
│   ├── PCP 可用于检测套利机会
│   ├── 证券可以视为期权的组合 (期权视角看公司价值)
│
└── ⚠️ 考试陷阱
    ├── PCP 仅适用于欧式期权
    ├── 有收入资产必须调整公式
    ├── 合成头寸是 PCP 的移项，不是新概念
    └── Put-call-forward parity 只是用远期替代现货
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `c + PV(X) = p + S0` | 标准买卖权平价（欧式期权） | 期权利率分析和套利识别 | 仅适用于欧式；到期日和行权价相同 |
| `c + PV(X) + PV(I) = p + S0` | 有已知现金收入资产平价 | 股票期权（有股利） | PV(I) 是股利现值 |
| `c + PV(X) = p + S0e^{-qT}` | 有连续收益率资产平价 | 股指期权 | q 为连续股利收益率 |
| `c + PV(X) = p + PV(F)` | 买卖权远期平价 | 用远期替代现货 | F = S0(1+r)^T 代入即为标准平价 |
| `c = p + S0 - PV(X)` | 合成看涨期权 | 用看跌+股票合成看涨 | 检查是否为欧式 |
| `p = c - S0 + PV(X)` | 合成看跌期权 | 用看涨+做空股票合成看跌 | 需做空标的资产 |
| `S0 = c + PV(X) - p` | 合成股票 | 用看涨+看跌合成股票 | 等价于 protective put |
| `c ≥ max(0, S0 - PV(X))` | 欧式看涨下限 | 检测期权是否被低估 | 下限由无套利推导 |

### 🛠️ 常见考点与解题思路

**考点1：检查 PCP 是否成立 / 识别套利机会**
- **步骤**：
  1. 写出标准平价公式
  2. 代入已知数值计算左侧和右侧
  3. 若左侧 ≠ 右侧 → 存在套利机会
  4. 买低卖高 (buy the cheap side, sell the expensive side)
  5. 检查是否需调整股利/收入
- **陷阱**：必须确认是欧式期权，否则套利不成立

**考点2：推导合成头寸**
- **步骤**：
  1. 从标准平价公式出发: c + PV(X) = p + S0
  2. 将要合成的头寸移到等式左侧
  3. 其余项移到右侧
- **示例**：要合成 call → c = p + S0 - PV(X)

**考点3：有股利/收益的 PCP 调整**
- **步骤**：
  1. 确定标的资产是否有已知现金收益或连续收益率
  2. 已知现金收入 → 左侧加 PV(I)
  3. 连续收益率 → 右侧 S0 乘以 e^{-qT}
- **高频陷阱**：忘记调整股利/收益是做 PCP 题最常见的错误

**考点4：Put-Call Forward Parity**
- **步骤**：
  1. 标准 PCP: c + PV(X) = p + S0
  2. 已知远期价格 F = S0(1+r)^T
  3. PV(F) = S0
  4. 代入: c + PV(X) = p + PV(F)
- **本质**：远期合约替代标的资产，概念和公式相同

**考点5：期权价值边界判断**
- **步骤**：
  1. 从 PCP 推导看涨下限
  2. 因为 p ≥ 0，所以 c + PV(X) ≥ S0
  3. 移项: c ≥ S0 - PV(X)
  4. 又因为 c ≥ 0，所以 c ≥ max(0, S0 - PV(X))

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| PCP 适用于所有期权 | PCP 仅适用于欧式期权 | 美式期权可提前行权，严格等式不成立 |
| 忘记股利调整直接用标准公式 | 有股利时必须用调整版公式 | 股利影响标的资产的持有成本 |
| Put-call-forward parity 是新概念 | 是标准 PCP 的变形，用远期替代现货 | 公式形式相同，只是代入不同 |
| 合成头寸需要完全相同的 payoff | 合成头寸的 payoff 理论上与目标一致 | PCP 保证复制精确性 |
| PCP 是预测工具 | PCP 是无套利恒等式，不是预测模型 | PCP 必须精确成立（无摩擦市场） |
| p + S0 = c + PV(X) 永远成立 | 仅对相同到期日和执行价的欧式期权成立 | 条件不同公式不同 |

### 🔄 跨模块关联

- **[[M08-Pricing-and-Valuation-of-Options]]** — 期权利润和 moneyness 是 PCP 的前置知识
- **[[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]]** — 无套利原则和复制定价是 PCP 的理论基础
- **[[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]]** — 二叉树模型也可以推导平价关系
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M09 是 Derivatives 科目中公式精确度要求最高的模块
- **核心能力**：熟练运用 PCP 公式，能在有/无股利场景之间切换
- **必考题型**：PCP 套利识别、合成头寸推导、期权价值边界判断
- **最常犯错误**：忘记股利调整、没确认欧式期权条件、PCP 等式方向搞反
- 记忆口诀：
  - "c + PV(X) = p + S0" — 左侧是 fiduciary call，右侧是 protective put
  - 合成头寸：移项使目标在左侧
  - 有股利：左侧加 PV(I) 或右侧乘 e^{-qT}
- 刷题建议：多做 PCP 套利和合成头寸题，这些是考试高频题
