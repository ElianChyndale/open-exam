---
title: "M09 — The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
description: "CFA Level I 2026 official module: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
module: M09
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 9: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M09: The Term Structure of Interest Rates: Spot, Par, and Forward Curves

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: The Term Structure of Interest Rates: Spot, Par, and Forward Curves
- 9.01 | Introduction
- 9.02 | Maturity Structure of Interest Rates and Spot Rates
- 9.03 | Par and Forward Rates
- 9.04 | Spot, Par, and Forward Yield Curves and Interpreting Their Relationship

## Learning Outcome Statements

The candidate should be able to:

- define spot rates and the spot curve, and calculate the price of a bond using spot rates
- define par and forward rates, and calculate par rates, forward rates from spot rates, spot rates from forward rates, and the price of a bond using forward rates
- compare the spot curve, par curve, and forward curve

## 🌳 核心知识树

```text
🏆 M09: Spot, Par, and Forward Curves（即期、平价与远期曲线）
├─ ⭐ 9.1 曲线定义 (Curve Dictionary)
│  ├─ 📐 即期利率 (Spot Rate)：单一期限的零息收益率
│  │  └─ 即期定价：P = Σ CF_t/(1+s_t)^t
│  ├─ 📐 贴现因子：DF_t = 1/(1+s_t)^t
│  ├─ 📐 平价利率 (Par Rate)：使债券按面值交易的票息率
│  │  └─ Par rate_n = (1 - DF_n)/Σ_{t=1}^{n} DF_t
│  ├─ 📐 远期利率 (Forward Rate)：当前曲线隐含的未来借贷利率
│  │  └─ (1+s_n)^n = (1+s_m)^m × (1+f_{m,n})^(n-m)
│  └─ ⚠️ 远期利率是无套利隐含利率，非确定性预测【易错】
│
├─ ⭐ 9.2 曲线计算
│  ├─ 🎯 即期定价：每笔现金流用匹配期限的即期利率贴现
│  ├─ 🎯 Spot → Forward：分解公式推导远期
│  ├─ 🎯 Forward → Spot：链式远期连乘得到即期
│  └─ 🎯 Discount Factor → Par Rate：通过贴现因子求解
│
└─ ⭐ 9.3 曲线比较
   ├─ 💡 正常曲线（上升）：远期 > 即期 > 平价
   ├─ 💡 倒挂曲线（下降）：远期 < 即期 < 平价
   ├─ 💡 平坦曲线：三者相等
   └─ ⚠️ Spot vs YTM：YTM 是单一贴现率，Spot 每期不同
```

## 📖 知识点详解

### 知识点1：曲线定义（Curve Dictionary）
**核心概念**：利率期限结构由即期曲线、平价曲线和远期曲线三种曲线共同描述，三者之间存在内在的数学关系。理解这三种曲线的定义和关系是利率分析的基础。
- **即期利率（Spot Rate）**：单一期限的零息收益率，每个期限对应一个即期利率。即期定价公式：`P = Σ CF_t/(1+s_t)^t`，每笔现金流使用其期限匹配的即期利率分别贴现
- **贴现因子（Discount Factor）**：`DF_t = 1/(1+s_t)^t`，是即期利率的另一种表达形式，用于计算现值
- **平价利率（Par Rate）**：使债券按面值交易的票息率。`Par rate_n = (1 - DF_n)/Σ_{t=1}^{n} DF_t`，用于构建互换曲线等参考基准
- **远期利率（Forward Rate）**：当前即期曲线隐含的未来借贷利率。`(1+s_n)^n = (1+s_m)^m × (1+f_{m,n})^(n-m)`
- ⚠️ 远期利率是无套利隐含利率，反映了当前市场对未来利率的隐含预期，但并不保证未来实际利率等于远期利率

**考试应用**：即期曲线折价计算（每期现金流用对应即期利率贴现），远期利率计算（给定 s1 和 s2，计算 f1,2）。

### 知识点2：曲线计算（Curve Calculations）
**核心概念**：即期、远期和平价利率之间可以互相推导。掌握这些推导关系是理解利率期限结构的关键。
- **即期定价 vs YTM 定价**：与使用单一 YTM 不同，即期定价将每笔现金流按其到期期限对应的即期利率分别贴现。两者在平坦曲线下相等，但在倾斜曲线下不同
- **Spot → Forward**：`f(m,n) = [(1+s_n)^n/(1+s_m)^m]^(1/(n-m)) - 1`，从即期利率推导远期利率
- **Forward → Spot**：`(1+s_n)^n = (1+f_0,1)(1+f_1,2)...(1+f_{n-1,n})`，链式远期连乘得到即期
- **Discount Factor → Par Rate**：先计算各期限贴现因子，再通过平价利率公式求解

**考试应用**：从即期利率推导远期利率（给定 s1 和 s2，计算 f1,2）；从贴现因子求解平价利率。

### 知识点3：曲线比较（Curve Comparison）
**核心概念**：即期、平价和远期三种曲线的相对位置取决于收益率曲线的形态。理解曲线之间的关系对利率预测和估值至关重要。
- **正常曲线（上升）**：远期利率 > 即期利率 > 平价利率。远期利率曲线最陡峭，平价利率曲线最平坦
- **倒挂曲线（下降）**：远期利率 < 即期利率 < 平价利率
- **平坦曲线**：三者相等
- **Spot vs YTM**：YTM 是单一贴现率适用于所有现金流，Spot rate 是每期现金流使用匹配期限的贴现率
- Par rate（平价利率）不是即期利率——它通常介于即期利率之间

**考试应用**：比较不同曲线形态下三种利率的相对大小关系，通常以选择题形式出现。

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t` | 即期定价 | 用即期利率计算债券价格 | 每期用不同的 s_t |
| `(1+s_n)^n = (1+s_m)^m × (1+f_{m,n})^(n-m)` | 远期利率推导 | 从即期算远期 | 无套利条件 |
| `DF_t = 1/(1+s_t)^t` | 贴现因子 | 计算现值 | 基础计算单元 |
| `Par rate_n = (1 - DF_n)/Σ DF_t` | 平价利率 | 构建平价曲线 | 非即期利率 |
| `(1+s_n)^n = ∏(1+f_{i-1,i})` | 即期利率（从远期） | 远期链推导即期 | 连乘所有前期远期 |

## 🛠️ 常见考点与解题思路

### 考点 1：即期曲线折价计算
- **题型**：给定即期利率序列，计算债券价格
- **步骤**：每期现金流用对应的即期利率分别贴现 → 求和
- **对比**：与使用单一 YTM 贴现的结果不同（除非曲线平坦）

### 考点 2：远期利率计算
- **题型**：给定 s1 和 s2，计算 f(1,2)
- **公式**：`(1+s2)^2 = (1+s1)(1+f1,2)` → `f1,2 = (1+s2)^2/(1+s1) - 1`
- **推广**：`f(m,n) = [(1+s_n)^n/(1+s_m)^m]^(1/(n-m)) - 1`

### 考点 3：从即期构建平价曲线
- **步骤**：1. 计算各期限贴现因子 → 2. 使用公式求解各期限平价利率
- **注意**：平价利率通常介于即期利率之间

### 考点 4：曲线形态比较
- **正常曲线（上升）**：远期利率 > 即期利率 > 平价利率
- **倒挂曲线（下降）**：远期利率 < 即期利率 < 平价利率
- **记忆**：远期利率曲线最陡峭，平价利率曲线最平坦

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| 远期利率 = 未来实际利率 | 远期利率是当前隐含的无套利利率 | 不是预测，是数学推导 |
| Spot rate = YTM | YTM 单一，Spot 每期不同 | 仅平坦曲线下相等 |
| Par rate = spot rate | 平价利率使债券按面值交易 | 通常介于即期利率之间 |
| 曲线关系总是成立 | 依赖于无套利假设 | 市场摩擦导致可能偏离 |

## 🔄 跨模块关联

- **Spot/forward 推导** → [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] 的定价框架
- **YTM vs spot** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的收益率概念
- **远期利率** → [[M10-Interest-Rate-Risk-and-Return]] 的预期利率路径
- **收益率曲线** → [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] 的久期分析

## 📋 复习与刷题提示

- **核心重点**：远期利率计算（从即期推导）是最高频计算考点
- **概念区分**：Spot rate vs YTM
  - YTM：单一贴现率用于所有现金流（假设曲线平坦）
  - Spot rate：每期现金流用对应期限的即期利率贴现
  - 两者仅在平坦收益率曲线下相等
- **三类曲线的关系**：
  - 正常（上升）曲线：远期 > 即期 > 平价
  - 倒挂（下降）曲线：远期 < 即期 < 平价
  - 平坦曲线：三者相等
- **典型计算流程**：
  1. 给定 s₁ = 2%，s₂ = 3%，求 f(1,2)
  2. `(1+s₂)² = (1+s₁)(1+f₁,₂)`
  3. `(1.03)² = (1.02)(1+f₁,₂)`
  4. `f₁,₂ = 1.0609/1.02 - 1 = 4.01%`
- **贴现因子**应用：
  - DF_t = 1/(1+s_t)^t
  - Par rate_n = (1 - DF_n)/ΣDF_t
  - 贴现因子序列是构建曲线的核心工具
- **刷题建议**：
  - 重点做远期利率计算题（s₁,s₂ → f₁,₂）
  - 即期定价题（用即期利率序列计算债券价格）
  - 曲线关系比较题（正常 vs 倒挂曲线下的三者关系）
- **易混淆点**：
  - 远期利率 ≠ 未来实际利率（只是当前曲线隐含的无套利利率）
  - Spot rate ≠ YTM（曲线倾斜时差异显著）
  - Par rate 介于即期利率之间

- **曲线关系记忆**：
  - 正常（上升）曲线：远期 > 即期 > 平价
  - 倒挂（下降）曲线：远期 < 即期 < 平价
  - 平坦曲线：三者相等
  - 远期曲线最陡峭，平价曲线最平坦
- **计算模板**：
  - 给定 s₁ = 2%，s₂ = 3%，求 f(1,2)
  - (1+s₂)² = (1+s₁)(1+f₁,₂)
  - f₁,₂ = (1.03)²/(1.02) - 1 = 4.01%
- **关键公式变体**：
  - 从远期求即期：(1+s_n)ⁿ = ∏(1+f_{i-1,i})
  - 从贴现因子求平价利率：Par rate_n = (1 - DF_n) / ∑DF_t
  - 贴现因子 DF_t = 1/(1+s_t)^t
- **曲线构建**：
  - 即期曲线通常从国债票息剥离（bootstrapping）获得
  - 平价曲线用于发行定价
  - 远期曲线用于利率预期分析
- **考试技巧**：
  - 远期利率不是预测，是纯数学推导
  - 即期定价比 YTM 定价更精确
  - 曲线倾斜度影响三类曲线的排序
