---
title: "M07 — Pricing and Valuation of Interest Rates and Other Swaps"
description: "CFA Level I 2026 official module: Pricing and Valuation of Interest Rates and Other Swaps"
module: M07
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 7: Pricing and Valuation of Interest Rates and Other Swaps"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M07: Pricing and Valuation of Interest Rates and Other Swaps

> This file is aligned to the CFA Institute 2026 module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Pricing and Valuation of Interest Rates and Other Swaps
- 7.01 | Introduction
- 7.02 | Swaps vs. Forwards
- 7.03 | Swap Values and Prices

## Learning Outcome Statements

The candidate should be able to:

- describe how swap contracts are similar to but different from a series of forward contracts
- contrast the value and price of swaps

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M07: 互换定价与估值 (Swap Pricing and Valuation)
│
├── 🟢 核心概念：互换是一种 OTC 衍生品
│   └── 本质：一系列远期合约的组合 (strip of forwards)
│
├── ⭐ 互换结构 (Swap Anatomy)
│   ├── 利率互换 (Interest Rate Swap / IRS)
│   │   ├── 固定换浮动 (Fixed-for-Floating)
│   │   ├── 只交换净利息差额，不交换名义本金
│   │   ├── 💡 名义本金仅作为计算基数
│   │   └── 初始固定利率使互换起始价值 ≈ 0
│   └── 货币互换 (Currency Swap)
│       ├── 可能交换本金 (期初和期末)
│       ├── 票息在不同币种间交换
│       └── ⚠️ 与 IRS 核心区别：本金交换
│
├── ⭐ 互换参与方
│   ├── 支付方 (Payer)
│   │   ├── 支付固定利率
│   │   ├── 接收浮动利率
│   │   └── 📉 利率上升 → payer 价值下降
│   └── 接收方 (Receiver)
│       ├── 接收固定利率
│       ├── 支付浮动利率
│       └── 📈 利率上升 → receiver 价值上升
│
├── ⭐ 估值视角 (Valuation Approaches)
│   ├── 债券对 (Bond Pair)
│   │   └── 互换 = 固定利率债券 + 浮动利率债券 (方向相反)
│   ├── FRA Strip
│   │   └── 互换 = 一系列远期利率协议的组合
│   └── 💡 两个视角得出相同结果
│
├── 📐 关键公式
│   ├── 互换净支付 = 名义本金 × (浮动利率 - 固定利率) × 计息因子
│   ├── 支付方价值 = PV(固定端) - PV(浮动端)
│   └── 接收方价值 = - 支付方价值
│
├── 💡 关键洞察
│   ├── 互换不创造全新收益，本质是交换现金流暴露
│   ├── 初始价值为零，但存续期价值可正可负
│   ├── 互换可以分解为更基本的工具来理解和定价
│
└── ⚠️ 考试陷阱
    ├── 名义本金不交换（利率互换）
    ├── Payer vs Receiver 方向不能混淆
    ├── 利率上升时 payer 受损 receiver 受益
    └── 货币互换与利率互换的区别
```

## 📖 知识点详解

### 知识点1：互换的结构与类型 (Swap Anatomy and Types)

**核心概念**：互换是一种 OTC 衍生品合约，约定双方在未来一系列日期交换现金流。互换可视为一系列远期合约的组合（strip of forwards）。利率互换（IRS）是最常见的类型，用于交换固定利率和浮动利率的利息现金流。货币互换则涉及不同币种的本金和利息交换。

- **利率互换 (Interest Rate Swap / IRS)**：固定换浮动（fixed-for-floating）。只交换净利息差额，不交换名义本金。名义本金仅作为计算利息的基数
- **货币互换 (Currency Swap)**：可能交换本金（期初和期末），票息在不同币种间交换。涉及汇率风险，比 IRS 更复杂
- 💡 互换 = 一系列远期合约的组合，但互换的所有"远期"有相同的固定利率，而独立远期合约每个到期日有不同的远期价格
- 📐 互换净支付 = 名义本金 × (浮动利率 - 固定利率) × 计息因子

**考试应用**：区分利率互换和货币互换是高频考点。关键区别：IRS 不交换本金，货币互换可能交换。IRS 同币种净额结算，货币互换全额交换不同币种。常见题型：给定互换描述，判断是 IRS 还是 Currency Swap。

### 知识点2：互换参与方 (Payer vs Receiver)

**核心概念**：互换双方根据支付方向分为支付方（payer）和接收方（receiver）。理解双方的身份和利率变化对双方价值的影响是互换概念的核心。

- **支付方 (Payer)**：支付固定利率，接收浮动利率。当市场利率上升时，payer 收到的浮动利率增加，但支付的固定利率不变，因此 payer 的价值下降
- **接收方 (Receiver)**：接收固定利率，支付浮动利率。当市场利率上升时，receiver 支付的浮动利率增加，但收到的固定利率不变，因此 receiver 的价值上升
- 🎯 **高频考点**：利率上升 → payer 受损 / receiver 受益。不可混淆方向

**考试应用**：方向题是互换最常见的题型。记忆法："Payer 支付固定"——名称中的"支付"指支付固定利率。利率变化对方向的损益：Payer 希望利率下降，Receiver 希望利率上升。

### 知识点3：互换的估值视角 (Swap Valuation Approaches)

**核心概念**：互换估值可以通过两种等价视角来理解：债券对法（bond pair）和远期利率协议组合法（FRA strip）。两种视角得出相同的估值结果，但提供了不同的理解角度。

- **债券对法 (Bond Pair)**：将互换视为固定利率债券多头 + 浮动利率债券空头（或反之）。固定端通过即期利率曲线折现，浮动端在付息日约等于面值（名义本金）
- **FRA Strip 法**：将互换视为一系列远期利率协议的组合。每期现金流对应一个 FRA，各期远期利率的某种平均即为互换的固定利率
- 💡 互换初始固定利率设定为使起始价值约等于零。存续期价值可正可负
- 📐 支付方价值 = PV(固定端) - PV(浮动端)；接收方价值 = -支付方价值

**考试应用**：互换估值通常以概念理解为主，Level I 的计算限于单期净支付。理解 bond pair 和 FRA strip 两种视角有助于回答概念题。不需要掌握完整的多期估值计算。

### 知识点4：互换 vs 远期对比 (Swaps vs Forwards)

**核心概念**：理解互换与远期合约的关系有助于把握互换的本质。互换是一系列远期合约的组合，但存在重要区别——互换的所有"远期"共享一个固定利率，而独立远期合约每期有不同的远期价格。

- **相似性**：远期和互换都是远期承诺，双方均有义务执行。互换可分解为一系列远期
- **区别**：
  - 互换在一系列日期结算多个现金流，远期单次结算
  - 互换的固定利率是各期远期利率的某种加权平均值
  - 互换通常涉及名义本金和计息因子，远期涉及合约规模和交割价
- 💡 互换不创造全新收益，本质是交换现金流暴露。互换是零和博弈

**考试应用**：理解 "互换 = 一系列远期的组合" 这一核心等式。常见题型问互换与远期的相似性和区别，或问互换的固定利率与各期远期利率的关系。

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Net payment = N × (浮动利率 - 固定利率) × (d/360)` | 利率互换一期净支付金额 | 计算单期互换净现金流 | 浮动利率通常为 LIBOR/参考利率，需在期初确定 |
| `Value to payer = PV(fixed leg) - PV(floating leg)` | 支付固定端一方的互换价值 | 互换存续期估值 | 浮动端现值通常接近名义本金 |
| `Value to receiver = - Value to payer` | 接收固定端一方的互换价值 | 互换存续期估值 | 互换是零和博弈 |
| `固定端现值 = Σ (C × dfi)` | 固定利率各期现金流折现和 | 债券对估值法的组成部分 | 使用即期利率曲线折现 |
| `浮动端现值 ≈ 名义本金` | 浮动端在付息日重置为面值 | 简化估值 | 只在付息日成立 |

### 🛠️ 常见考点与解题思路

**考点1：利率互换 vs 货币互换**
- **步骤**：从以下维度对比
  - 本金交换：IRS 不交换，Currency Swap 可能交换
  - 现金流：IRS 同币种净额结算，Currency Swap 全额交换
  - 定价：IRS 用利率曲线，Currency Swap 用两国利率 + 汇率
- **常见题型**：描述一个互换情景，判断是 IRS 还是 Currency Swap

**考点2：计算单期净支付**
- **步骤**：
  1. 确认名义本金 N
  2. 获取当期浮动利率（通常在期初确定）
  3. 获取固定利率
  4. 计算净差额 = N × (浮动 - 固定) × 计息因子
  5. 确定支付方向（正值为 payer 付给 receiver，反之亦然）
- **陷阱**：计息因子 (d/360 或 d/365) 取决于合约约定

**考点3：互换方向判断**
- **步骤**：
  - Payer：支付固定 → 期望利率下降（因为支付固定、收浮动）
  - Receiver：收固定 → 期望利率上升（因为收固定、支浮动）
- **关键**：利率变化对方向的损益影响

**考点4：互换 vs 远期对比**
- **步骤**：
  - 互换 = 一系列远期合约的组合
  - 但互换的所有"远期"有相同的固定利率
  - 而独立远期合约每个到期日有不同的远期价格
- **理解**：互换的固定利率是各期远期利率的某种平均值

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 利率互换交换名义本金 | IRS 不交换名义本金，只交换净利息差额 | 名义本金仅作为计算利息的基数 |
| Payer 支付浮动利率 | Payer 支付固定利率，接收浮动利率 | 名称本身暗示"支付固定" |
| 利率上升时 payer 受益 | 利率上升时 payer 受损（浮动端支出增加） | Payer 支付固定，利率上升时浮动端成本上升 |
| 互换创造全新收益 | 互换只是交换现金流暴露，不创造新价值 | 互换是零和博弈 |
| 初始互换价值不为零 | 固定利率设定为使初始价值约等于零 | 定价原则 |
| 货币互换和利率互换一样 | 货币互换可能交换本金，涉及汇率风险 | 跨币种增加了复杂性 |

### 🔄 跨模块关联

- **[[M02-Forward-Commitment-and-Contingent-Claim-Features-and-Instruments]]** — 互换是远期承诺的一种，M02 介绍了互换的基本特征
- **[[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]]** — FRA strip 视角将互换估值与远期定价连接
- **[[M06-Pricing-and-Valuation-of-Futures-Contracts]]** — 欧洲美元期货为利率互换定价提供市场数据
- **[[M00-Derivatives-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M07 在 Derivatives 科目中属于中低计算量模块，以概念理解为主
- **核心能力**：理解互换的结构、方向、估值原理
- **必考题型**：IRS vs Currency Swap 对比、净支付计算、方向判断
- 记忆要点：
  - 互换 = 一系列远期合约
  - IRS 不交换本金，货币互换可能交换
  - Payer 支付固定、收浮动；利率上升 → Payer 受损
- 两个估值视角：债券对法 (bond pair) 和 FRA strip 法
- 考试中以概念题为主，计算仅限于单期净支付
