---
title: "M01 — Derivative Instrument and Derivative Market Features"
description: "CFA Level I 2026 official module: Derivative Instrument and Derivative Market Features"
module: M01
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 1: Derivative Instrument and Derivative Market Features"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M01: Derivative Instrument and Derivative Market Features

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Derivative Instrument and Derivative Market Features
- 1.01 | Introduction
- 1.02 | Derivative Features
- 1.03 | Derivative Underlyings
- 1.04 | Derivative Markets

## Learning Outcome Statements

The candidate should be able to:

- define a derivative and describe basic features of a derivative instrument
- describe the basic features of derivative markets, and contrast over-the-counter and exchange-traded derivative markets

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M01: 衍生品工具与市场特征 (Derivative Instrument and Market Features)
│
├── 🟢 衍生品定义
│   └── 价值衍生自标的资产 (value derives from underlying)
│   └── 用于风险管理、投机、套利 (hedge, speculate, arbitrage)
│
├── ⭐ 合约要素 (Contract Elements)
│   ├── 标的资产 (Underlying)
│   │   └── 股票、利率、外汇、信用、大宗商品及其他参照物
│   ├── 多头与空头 (Long vs Short)
│   │   ├── 多头：在未来买入资产的权利/义务
│   │   └── 空头：在未来卖出资产的权利/义务
│   ├── 结算方式 (Settlement)
│   │   ├── 实物交割 (physical delivery)
│   │   └── 现金结算 (cash settlement)
│   └── ⚠️ 名义金额 (Notional Amount)
│       └── 放大风险敞口但不等于实际在险现金
│       └── 🎯 高频考点：名义金额 ≠ 最大损失
│
├── ⭐ 市场结构 (Market Structure)
│   ├── 交易所交易 (Exchange-Traded)
│   │   ├── 标准化合约 (standardized)
│   │   ├── 中央清算所 (clearinghouse)
│   │   ├── 保证金制度 (margin)
│   │   └── 每日盯市 (daily marking-to-market)
│   └── 场外交易 (OTC)
│       ├── 定制化条款 (customization)
│       ├── 双边交易对手风险 (bilateral counterparty risk)
│       └── 无中央清算 (no central clearing)
│
├── 📐 价值关系
│   ├── 衍生品价值 < 名义敞口 (derivative value < notional exposure)
│   └── 合约价值 ∝ 标的资产价格变化
│
├── 💡 关键洞察
│   ├── 衍生品是零和博弈 (zero-sum) 的误解：实际降低交易成本
│   ├── 交易所 vs OTC 风险类型不同，没有绝对"更安全"
│   └── 名义金额是规模参照，不是实际投资
│
└── ⚠️ 考试陷阱
    ├── 衍生品当前价值很小但经济敞口可能非常大
    ├── 不要混淆名义金额与最大损失概念
    └── OTC ≠ 更危险，只是风险类型不同
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `衍生品价值 < 名义敞口` | 衍生品只需少量保证金即可控制大额名义敞口 | 理解杠杆效应 | 名义金额不是实际投入资金 |
| `合约价值 ∝ Δ标的资产价格` | 衍生品价值随标的资产价格变化而变化 | 理解衍生品定价基础 | 不同类型的衍生品对标的变动的敏感度不同 |

*注：M01 以概念为主，无核心计算公式。上述关系是理解后续定价模块的基础。*

### 🛠️ 常见考点与解题思路

**考点1：区分交易所 vs OTC 市场**
- **步骤**：对比标准化程度、清算机制、保证金要求、交易对手风险
- **关键判断**：
  - 标准化 + 清算所 + 保证金 → 交易所
  - 定制化 + 双边 + 无清算所 → OTC
- **常见题型**：给出市场描述，判断是 exchange-traded 还是 OTC

**考点2：判断结算方式**
- **步骤**：看合约类型和资产类别
- **实物交割**：多用于商品、外汇、国债期货
- **现金结算**：多用于指数衍生品、利率衍生品

**考点3：名义金额的理解**
- **步骤**：名义金额是计算回报的基数，不是实际投资额
- **陷阱**：不要认为名义金额是最大损失或实际风险敞口上限

**考点4：衍生品定义判断**
- **步骤**：判断一个工具是否属于衍生品 → 看其价值是否衍生自其他资产
- **常见题型**：给定一个金融工具，判断是否为衍生品

**考点5：多头 vs 空头的理解**
- **步骤**：
  1. 确定交易方向（买或卖未来资产）
  2. Long (多头)：在未来买入资产，预期价格上涨
  3. Short (空头)：在未来卖出资产，预期价格下跌
- **常见混淆**：Long 不一定是"看涨"的预期——如 long forward 是义务买入，但当远期价格低于预期时仍可能获利

**考点6：结算方式的应用判断**
- **步骤**：
  1. 分析标的资产的类型和特点
  2. 实物结算要求交易双方有能力交付/接收实物
  3. 现金结算更简便，适用于指数衍生品和无实物交割的利率合约
- **高频陷阱**：不要默认所有衍生品都使用实物交割，现金结算在金融衍生品中更为常见

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 衍生品当前价值小=风险小 | 衍生品经济敞口可能非常大 | 杠杆效应使少量资金控制大额名义敞口 |
| 名义金额=最大可能损失 | 名义金额是计算回报的参照基数 | 衍生品的损失取决于价格变动方向和幅度 |
| OTC 衍生品更危险 | OTC 风险类型不同（对手风险），但交易所也有流动性风险 | 风险维度不同，不可简单比较 |
| 远期合约必须在交易所交易 | 远期合约是 OTC 产品 | 远期是定制化合约，不在交易所交易 |
| 期货和远期一样到期结算 | 期货每日盯市结算，远期到期一次结算 | 结算机制的根本区别 |

### 🔄 跨模块关联

- **[[M02-Forward-Commitment-and-Contingent-Claim-Features-and-Instruments]]** — 合约分类（远期承诺 vs 或有索取权）建立在 M01 的基础概念之上
- **[[M06-Pricing-and-Valuation-of-Futures-Contracts]]** — 交易所标准化的保证金制度是期货定价的独特因素
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- 本模块为 Derivatives 的开篇概念模块，所有后续模块都依赖 M01 的基础术语
- 重点掌握：交易所 vs OTC 的区别、名义金额的含义、结算方式
- 刷题策略：概念题为主，不需要复杂计算，但概念混淆会导致整个科目后续题目失分
- 易混淆概念：long position（多头）≠ 看涨 (call) 预期；notional amount 与市场价值
- 常见组合题：可能结合 M02 中的合约分类出题（给出市场结构 → 判断交易场所 → 判断合约类型）
- 高频考点频率：
  - ⭐⭐⭐ 交易所 vs OTC 对比（几乎每年必考）
  - ⭐⭐ 名义金额概念（常见于混淆选项）
  - ⭐⭐ 结算方式判断
  - ⭐ 衍生品定义的边界问题
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
