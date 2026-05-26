---
title: "M05 — Portfolio Mathematics"
description: "CFA Level I 2026 official module: Portfolio Mathematics"
module: M05
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 5: Portfolio Mathematics"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M05: Portfolio Mathematics

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Portfolio Mathematics
- 5.01 | Introduction
- 5.02 | Portfolio Expected Return and Variance of Return
- 5.03 | Forecasting Correlation of Returns: Covariance Given a Joint Probability Function
- 5.04 | Portfolio Risk Measures: Applications of the Normal Distribution

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret the expected value, variance, standard deviation, covariances, and correlations of portfolio returns
- calculate and interpret the covariance and correlation of portfolio returns using a joint probability function for returns
- define shortfall risk, calculate the safety-first ratio, and identify an optimal portfolio using Roy’s safety-first criterion

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M05: Portfolio Mathematics（投资组合数学）
│
├── ⭐ 组合期望收益率 (Portfolio Expected Return)
│   ├── 📐 E(Rₚ) = Σ wᵢE(Rᵢ) — 各资产期望收益的加权平均
│   ├── 权重 wᵢ 之和必须为 1（全额投资组合）
│   └── 🎯 组合期望收益 = 各资产期望收益的线性组合
│
├── ⭐ 两资产组合方差 (Two-Asset Portfolio Variance)
│   ├── 📐 σₚ² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂Cov(R₁,R₂)
│   ├── 📐 相关系数形式: σₚ² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂
│   ├── ⚠️ 协方差项系数为 2，容易遗漏
│   └── 💡 组合风险 ≠ 加权平均风险 — 协方差决定分散化效果
│
├── ⭐ 多资产组合方差 (Matrix Form)
│   ├── 📐 σₚ² = ΣΣ wᵢwⱼCov(Rᵢ,Rⱼ)
│   ├── 对角线 = 各资产方差项
│   └── 非对角线 = 两两协方差项
│
├── ⭐ 联合概率与协方差 (Joint Probability & Covariance)
│   ├── 📐 Cov(R₁,R₂) = Σ pᵢ[R₁ᵢ-E(R₁)][R₂ᵢ-E(R₂)]
│   ├── 📐 ρ₁₂ = Cov(R₁,R₂) / (σ₁σ₂) — 范围 [-1,+1]
│   ├── ρ=+1 → 无分散化；ρ=-1 → 完全对冲
│   └── 🎯 联合概率表 → 边际期望 → 协方差 → 相关系数
│
├── ⭐ 分散化机制 (Diversification Mechanics)
│   ├── ρ < 1 → 协方差项 < 方差项 → 组合风险降低
│   ├── 📐 MVP 权重: w₁* = [σ₂² - Cov₁₂] / [σ₁²+σ₂²-2Cov₁₂]
│   └── ⚠️ 分散化降低风险，不降低预期收益
│
├── ⭐ 短缺风险 (Shortfall Risk)
│   ├── 📐 SFRatio = [E(Rₚ) - R_L] / σₚ
│   ├── SFRatio 越大 → 跌破 R_L 的概率越低
│   └── vs Sharpe Ratio: SR 用 R_f，SFRatio 用自定义 R_L
│
├── 💡 关键洞察
│   ├── 组合收益是线性的，但组合风险不是
│   ├── 低相关 ≠ 低收益 — 可以找到低相关且正期望收益的资产
│   ├── ρ=+1 是组合风险最大情况；ρ=-1 是风险最小情况
│   └── SFRatio 符合风险厌恶投资者的关注点（下行风险）
│
└── ⚠️ 考试陷阱总结
    ├── 协方差公式中的离差乘积符号不要忽略
    ├── 相关系数 ≠ 协方差 — 相关系数是标准化版本
    ├── 组合方差公式协方差项系数 2 容易遗漏
    ├── 权重必须先检查是否和为 1 — 不是则归一化
    └── Roy's safety-first 假设组合收益服从正态分布
```

## 📖 知识点详解

### 知识点1：组合期望收益率与方差（Portfolio Expected Return and Variance）
**核心概念**：组合期望收益率是各资产期望收益率的加权平均，但组合方差不是各资产方差的简单加权平均。协方差项决定了分散化的效果。
- **组合期望收益率**：E(Rₚ) = Σ wᵢE(Rᵢ)，权重之和必须为 1
- **两资产组合方差**：σₚ² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂Cov(R₁,R₂)
- **相关系数形式**：σₚ² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂
- ⚠️ **关键直觉**：组合风险不是资产风险的简单加权平均。协方差项决定了分散化的效果。公式中协方差项系数为 2，容易遗漏

**考试应用**：计算组合期望收益和方差，注意权重和为 1 的前提条件。

### 知识点2：联合概率与协方差（Joint Probability and Covariance）
**核心概念**：通过联合概率函数可以计算各资产的期望收益、协方差和相关系数。这是理解和度量资产间关联性的基础。
- **协方差**：Cov(R₁,R₂) = Σ pᵢ[R₁ᵢ-E(R₁)][R₂ᵢ-E(R₂)]，衡量两变量同向变动程度
- **相关系数**：ρ₁₂ = Cov(R₁,R₂)/(σ₁σ₂)，范围 [-1,+1]，标准化后的协方差
- ρ=+1 → 无分散化效果；ρ=-1 → 完全对冲可能；ρ=0 → 仍有分散化效果
- **从联合概率表导出**：边际概率 → 期望收益 → 协方差 → 相关系数
- ⚠️ 协方差公式中离差乘积的符号不要忽略——同号为正向变动，异号为反向变动

**考试应用**：从联合概率表计算协方差和相关系数，理解分散化的数学本质。

### 知识点3：分散化机制（Diversification Mechanics）
**核心概念**：分散化的数学本质是当相关系数小于 1 时，组合风险低于加权平均风险。最小方差组合（MVP）是整个可行集中风险最小的组合。
- 当 ρ < 1 时，协方差项小于方差项，组合风险降低
- **MVP 权重公式**：w₁* = [σ₂² - Cov₁₂]/[σ₁²+σ₂²-2Cov₁₂]
- ⚠️ 分散化降低风险，不必然降低预期收益——可以找到低相关且正期望收益的资产

**考试应用**：判断不同相关系数下的分散化效果，计算最小方差组合的权重。

### 知识点4：短缺风险与 Safety-First Ratio（Shortfall Risk and Roy's Safety-First Ratio）
**核心概念**：短缺风险衡量组合回报跌破最低可接受水平的概率。Roy's Safety-First Ratio 提供了量化选择工具。
- **SFRatio**：[E(Rₚ) - R_L]/σₚ，其中 R_L 是投资者设定的阈值回报率
- SFRatio 越大，跌破 R_L 的概率越低（假设正态分布）
- 在所有候选组合中选择 SFRatio 最大的组合
- **vs Sharpe Ratio**：Sharpe Ratio 用无风险利率 R_f，SFRatio 用自定义 R_L
- ⚠️ Roy's safety-first 假设组合收益服从正态分布

**考试应用**：计算 SFRatio，比较不同组合并选择最优者。

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `E(Rₚ) = Σ wᵢE(Rᵢ)` | 组合期望收益 | 投资组合预期回报 | 权重和为 1 |
| `σₚ² = w₁²σ₁²+w₂²σ₂²+2w₁w₂Cov₁₂` | 两资产组合方差 | 计算组合风险 | 协方差项系数为 2 |
| `Cov₁₂ = Σ pᵢ[R₁ᵢ-E(R₁)][R₂ᵢ-E(R₂)]` | 协方差 | 两变量同向变动程度 | 注意离差乘积的符号 |
| `ρ₁₂ = Cov₁₂/(σ₁σ₂)` | 相关系数 | 标准化协方差 | 范围 [-1,+1] |
| `SFRatio = [E(Rₚ)-R_L]/σₚ` | 安全优先比率 | 评估跌破阈值风险 | 假设正态分布 |
| `w₁* = (σ₂²-Cov₁₂)/(σ₁²+σ₂²-2Cov₁₂)` | MVP 权重 | 最小方差组合 | 两资产情况 |

### 🛠️ 常见考点与解题思路

**考点1：计算组合期望收益和方差**
- 步骤 1：确认权重和各资产期望收益
- 步骤 2：E(Rₚ) = Σ wᵢE(Rᵢ)
- 步骤 3：代入两资产方差公式，注意协方差项 × 2
- 步骤 4：开方得标准差
- ⚠️ 两资产公式中的协方差项系数为 2 是最高频错误

**考点2：从联合概率表算协方差**
- 步骤 1：从边际概率算各资产期望收益
- 步骤 2：每个情景算离差乘积 × 联合概率
- 步骤 3：加总得协方差
- 步骤 4：代入相关系数公式 ρ = Cov/(σ₁σ₂)

**考点3：分散化效果判断**
- ρ = +1 → 无分散化，组合标准差 = w₁σ₁ + w₂σ₂
- ρ = -1 → 完全对冲可能，组合标准差 = |w₁σ₁ - w₂σ₂|
- ρ 越接近 -1，分散化效果越好

**考点4：最小方差组合 (MVP) 权重计算**
- 代入 w₁* 公式
- w₂ = 1 - w₁*
- 验证：该权重下组合方差最小

**考点5：Safety-First Ratio 选组合**
- 计算所有候选组合的 SFRatio
- 选 SFRatio 最大者（跌破阈值概率最低）
- 区分 SR（用 R_f）和 SFR（用 R_L）

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 组合方差协方差项系数为 1 | 两资产公式协方差项系数为 2 | (a+b)² = a² + b² + 2ab |
| 相关系数 = 协方差 | 相关系数 = 协方差/(标准差乘积) | 相关系数是标准化到 [-1,+1] 的协方差 |
| 低相关 = 低预期收益 | 低相关降低方差，不影响期望收益 | 分散化降低风险，不必然降低收益 |
| 组合风险 = 加权平均风险 | 组合风险 < 加权平均风险（当 ρ < 1） | 协方差项降低了总风险 |
| SFRatio 越大越差 | SFRatio 越大越好 | 越大表示跌破阈值的概率越低 |

### 🔄 跨模块关联

- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 方差、标准差、相关系数概念在 M03 铺好基础；M05 将其扩展到多变量组合场景。
- **[[M04-Probability-Trees-and-Conditional-Expectations]]** — 联合概率函数是概率论在投资组合中的直接应用。
- **[[M01-Rates-and-Returns]]** — 杠杆回报公式与组合权重和杠杆效应相关。
- **[[M09-Parametric-and-Non-Parametric-Tests-of-Independence]]** — 协方差和相关系数在 M09 扩展为正式统计检验。

### 📋 复习与刷题提示

- **核心能力**：熟练两资产方差公式（含协方差项系数 2），掌握联合概率表到协方差的完整计算
- **必考题型**：组合期望收益/方差计算、协方差/相关系数计算、MVP 权重、SFRatio 选组合
- **最常犯错误**：方差公式遗漏协方差项系数 2、权重未归一化、相关系数与协方差混淆
- 记忆口诀：
  - 组合方差：w₁²σ₁² + w₂²σ₂² + 2w₁w₂Cov = (a+b)² 结构
  - 分散化条件：ρ < 1 就有效果
  - Safety-First: 越大越好（越大 = 越安全）
- 刷题建议：联合概率表和组合方差计算题是绝对重点
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
