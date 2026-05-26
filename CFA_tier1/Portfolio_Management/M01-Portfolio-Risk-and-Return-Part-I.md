---
title: "M01 — Portfolio Risk and Return: Part I"
description: "CFA Level I 2026 official module: Portfolio Risk and Return: Part I"
module: M01
subject: "Portfolio Management"
topic_area: Portfolio_Management
curriculum_year: 2026
official_module: "Module 1: Portfolio Risk and Return: Part I"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Portfolio_Management
  - official_2026
---

# M01: Portfolio Risk and Return: Part I

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Portfolio Risk and Return: Part I
- 1.01 | Introduction
- 1.02 | Historical Return and Risk
- 1.03 | Other Investment Characteristics
- 1.04 | Risk Aversion and Portfolio Selection
- 1.05 | Utility Theory and Indifference Curves
- 1.06 | Application of Utility Theory to Portfolio Selection
- 1.07 | Portfolio Risk & Portfolio of Two Risky Assets
- 1.08 | Portfolio of Many Risky Assets
- 1.09 | The Power of Diversification
- 1.10 | Efficient Frontier: Investment Opportunity Set & Minimum Variance Portfolios
- 1.11 | Efficient Frontier: A Risk-Free Asset and Many Risky Assets
- 1.12 | Efficient Frontier: Optimal Investor Portfolio
- 1.13 | Summary

## Learning Outcome Statements

The candidate should be able to:

- describe characteristics of the major asset classes that investors consider in forming portfolios
- explain risk aversion and its implications for portfolio selection
- explain the selection of an optimal portfolio, given an investor's utility (or risk aversion) and the capital allocation line
- calculate and interpret the mean, variance, and covariance (or correlation) of asset returns based on historical data
- calculate and interpret portfolio standard deviation
- describe the effect on a portfolio's risk of investing in assets that are less than perfectly correlated
- describe and interpret the minimum-variance and efficient frontiers of risky assets and the global minimum-variance portfolio

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M01: 组合风险与收益 Part I (Portfolio Risk and Return: Part I)
│
├── 🟢 核心主题：从单资产到组合的扩展
│   └── 组合风险 ≠ 各资产风险的加权平均
│
├── ⭐ 组合期望收益 (Portfolio Expected Return)
│   └── E(Rp) = Σ wi × E(Ri)
│   └── 💡 权重加权平均，权重和为 1
│
├── ⭐ 组合方差与风险 (Portfolio Variance & Risk)
│   ├── 两资产方差: σp² = w1²σ1² + w2²σ2² + 2w1w2Cov(R1,R2)
│   ├── 协方差: Cov(R1,R2) = E[(R1-E(R1))(R2-E(R2))]
│   ├── 相关系数: ρ12 = Cov(R1,R2) / (σ1×σ2)
│   │   ├── ρ = +1: 无分散化
│   │   ├── ρ = -1: 完全对冲（可构建无风险组合）
│   │   └── -1 < ρ < +1: 存在分散化收益
│   └── 🎯 高频考点：组合方差计算（永远不要忽略协方差项）
│
├── ⭐ 分散化 (Diversification)
│   ├── 核心：分散化来自低相关性，不是数量本身
│   ├── 非系统性风险 → 可通过分散化消除
│   ├── 系统性风险 → 无法通过分散化消除
│   └── 💡 增加资产数量时，σp 收敛于系统性风险水平
│
├── ⭐ 效用函数与无差异曲线
│   ├── U = E(Rp) - 0.5 × A × σp²
│   ├── A > 0: 风险厌恶 (risk averse)
│   ├── A = 0: 风险中性 (risk neutral)
│   ├── A < 0: 风险偏好 (risk seeking)
│   └── 无差异曲线越陡峭 → 越厌恶风险
│
├── ⭐ 资本配置线 (CAL)
│   ├── E(Rc) = Rf + [(E(Rp)-Rf)/σp] × σc
│   ├── 斜率 = Sharpe Ratio (夏普比率)
│   └── 最优组合 = 无差异曲线与 CAL 的切点
│
├── ⭐ 有效前沿 (Efficient Frontier)
│   ├── 最小方差组合 (GMV) 以上部分
│   ├── 理性投资者持有有效前沿上的某个组合
│   └── 引入无风险资产 → 有效前沿变为 CAL
│
├── 💡 关键洞察
│   ├── 分散化降低的是特定风险，不是所有风险
│   ├── 相关系数是分散化效果的决定因素
│   ├── 效用函数连接了风险偏好和组合选择
│
└── ⚠️ 考试陷阱
    ├── 组合方差不是加权平均方差
    ├── ρ 范围绝不超出 [-1, +1]
    ├── 有效前沿仅包含最小方差组合以上的部分
    └── 不同风险偏好的投资者选择有效前沿上不同位置
```

## 📖 知识点详解

### 知识点1：组合期望收益与方差 (Portfolio Expected Return and Variance)

**核心概念**：投资组合的期望收益是各资产期望收益的简单加权平均，但组合方差不是各资产方差的加权平均——需要加入协方差项来反映资产间的联动关系。这是现代投资组合理论（MPT）的基石。

- **组合期望收益**：E(Rp) = Σ wi × E(Ri)，收益率加权平均，权重之和为 1
- **两资产组合方差**：σp² = w1²σ1² + w2²σ2² + 2w1w2Cov(R1,R2)。其中协方差项是分散化收益的来源
- **相关系数**：ρ12 = Cov(R1,R2) / (σ1×σ2)，取值范围 [-1, +1]。ρ = +1 时无分散化效果；ρ = -1 时可完全对冲；-1 < ρ < +1 时有分散化收益
- 📐 组合方差中协方差项的数量随资产数量增加而迅速增加（N(N-1)/2 个），当 N 很大时组合风险主要取决于协方差而非方差

**考试应用**：计算组合期望收益和方差是必考题型。关键陷阱：忘记协方差项、资产权重之和不为 1、相关系数正负号弄反。组合方差公式的展开和化简也是常见题型。

### 知识点2：分散化效应 (Diversification Effect)

**核心概念**：分散化是投资组合中唯一的"免费午餐"——在不降低期望收益的情况下降低风险。分散化的效果来源于资产间的不完全正相关。随着组合中资产数量增加，非系统性风险逐渐被分散，但系统性风险无法消除。

- **非系统性风险 (Unsystematic Risk)**：公司特有风险，可通过分散化消除。也称为可分散风险、特有风险
- **系统性风险 (Systematic Risk)**：市场整体风险，无法通过分散化消除。也称为市场风险、不可分散风险
- 💡 分散化降低风险的边际收益递减：前 10-20 只股票的分散化效果最显著，此后增加资产的边际收益迅速下降
- 🎯 **高频考点**：分散化消除的是非系统性风险，不是系统性风险

**考试应用**：分散化概念是 PM 科目的核心思想。常见题型包括：给定相关系数判断分散化程度、解释为什么多买资产不一定能完全分散化（关键是低相关性）、区分系统性和非系统性风险。

### 知识点3：有效前沿与最小方差组合 (Efficient Frontier and Minimum-Variance Portfolio)

**核心概念**：有效前沿代表了所有可行组合中给定风险水平下的最高期望收益的集合。最小方差组合（MVP）是整个机会集中风险最低的点。有效前沿是从 MVP 向上的部分——理性投资者只持有有效前沿上的组合。

- **最小方差组合 (Minimum-Variance Portfolio)**：在给定资产集下风险（方差/标准差）最小的组合
- **有效前沿 (Efficient Frontier)**：从 MVP 向上延伸到最高收益组合的曲线段，每个点代表给定风险下的最高期望收益
- **机会集 (Opportunity Set / Feasible Set)**：所有可能的风险-收益组合的集合
- 💡 加入无风险资产后，有效前沿被资本配置线（CAL）替代，最优组合变为 CAL 与有效前沿的切点组合
- 📐 两资产最小方差权重：w1_min = (σ2² - Cov12) / (σ1² + σ2² - 2Cov12)

**考试应用**：有效前沿图形题是常见题型。理解有效前沿的形状（弯曲程度取决于相关系数）、MVP 的位置、以及加入无风险资产后如何改变有效前沿。常见陷阱：认为有效前沿上的所有组合都适合所有投资者（实际取决于风险偏好）。

### 知识点4：风险厌恶与效用函数 (Risk Aversion and Utility Function)

**核心概念**：投资者的风险厌恶程度决定了其在风险-收益权衡中的最优选择。效用函数将风险厌恶量化，使投资者可以在不同组合之间进行理性比较。

- **效用函数**：U = E(Rp) - 0.5 × A × σp²。A 是风险厌恶系数，A 越大对波动的惩罚越重
- **风险厌恶系数 A**：A > 0 为风险厌恶（risk averse），A = 0 为风险中性（risk neutral），A < 0 为风险偏好（risk seeking）
- **无差异曲线 (Indifference Curve)**：相同效用的风险-收益组合的轨迹。风险厌恶程度越高，曲线越陡峭
- 💡 投资者选择无差异曲线与 CAL（或有效前沿）的切点作为最优组合

**考试应用**：效用函数计算题：给定 E(Rp)、σp、A，计算效用值。比较不同组合的效用值确定最优选择。注意 A 的不同水平对配置的影响——A 越高，配置到无风险资产越多。

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `E(Rp) = Σ wi × E(Ri)` | 组合期望收益 = 各资产加权平均 | 计算组合期望回报 | 权重之和必须为 1 |
| `σp² = w1²σ1² + w2²σ2² + 2w1w2Cov12` | 两资产组合方差公式 | 计算双资产组合风险 | 协方差项不可省略 |
| `Cov(R1,R2) = Σ p(R1-E(R1))(R2-E(R2))` | 协方差定义 / 计算 | 衡量资产同向变动程度 | 有概率加权和无概率两种版本 |
| `ρ12 = Cov12 / (σ1×σ2)` | 相关系数 = 协方差 / 两标准差之积 | 标准化风险度量 | 范围绝不超出 [-1, +1] |
| `U = E(Rp) - 0.5×A×σp²` | 效用函数 | 量化投资者偏好、选最优组合 | A 越大风险惩罚越重 |
| `E(Rc) = Rf + Sharpe × σc` | 资本配置线 (CAL) | 无风险+风险组合的收益-风险关系 | Sharpe = (E(Rp)-Rf)/σp |
| `wGMV = (σ2²-Cov12)/(σ1²+σ2²-2Cov12)` | 最小方差组合权重 (N=2) | 求全局最小方差组合 | 公式只适用于两资产情形 |

### 🛠️ 常见考点与解题思路

**考点1：计算组合期望收益和方差**
- **步骤**：
  1. 先算加权平均收益
  2. 算组合方差（别忘了协方差项）
  3. 开方得组合标准差
- **常见陷阱**：权重加起来不等于 1

**考点2：判断分散化效果**
- **步骤**：
  1. 给定相关系数 ρ
  2. ρ 越接近 -1 → 分散化效果越强
  3. ρ = -1 → 可以构建无风险组合
  4. ρ = +1 → 无分散化效果
- **关键**：分散化来自低相关性，不是资产数量

**考点3：效用函数与最优组合选择**
- **步骤**：
  1. 给定 A 值和候选组合
  2. 代入 U = E(Rp) - 0.5×A×σp²
  3. 选择 U 最大的组合
- **判断**：A 越高 → 越厌恶风险 → 选择更保守的组合

**考点4：计算最小方差组合 (两资产)**
- **步骤**：
  1. 使用公式 w1 = (σ2² - Cov12) / (σ1² + σ2² - 2Cov12)
  2. w2 = 1 - w1
  3. 代入方差公式计算最小方差

**考点5：有效前沿判断**
- **步骤**：
  - 有效前沿 = 最小方差组合以上的部分
  - 曲线以下和最小方差组合以下的点都无效

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 组合方差 = 各资产方差加权平均 | 组合方差包含协方差项 | 资产间联动影响整体波动 |
| 多买几个资产就算分散化 | 关键是低相关性不是数量 | 相关性决定分散化效果 |
| ρ=0 就能完全分散化 | ρ=0 只是部分分散化，ρ=-1 才能完全对冲 | 相关系数决定程度 |
| 有效前沿上所有点都适合所有人 | 不同 A 的投资者选择不同点 | 风险偏好决定位置 |
| 分散化消除所有风险 | 系统性风险无法分散化 | 市场风险始终存在 |
| 无差异曲线可相交 | 同一投资者的无差异曲线不相交 | 效用函数的数学性质 |

### 🔄 跨模块关联

- **[[M02-Portfolio-Risk-and-Return-Part-II]]** — M01 的风险收益框架是 CAPM 和 Beta 的基础
- **[[M04-Basics-of-Portfolio-Planning-and-Construction]]** — 有效前沿和最优组合选择指导资产配置
- **[[M06-Introduction-to-Risk-Management]]** — 风险概念延伸至更广泛的风险管理框架
- **[[M01-Portfolio-Risk-and-Return-Part-I]]** — 组合方差和协方差的概念贯穿所有后续模块
- **[[00-Portfolio-Management-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M01 是 Portfolio Management 的**最重要的基础模块**，所有后续模块都依赖这里的概念
- **核心能力**：组合期望收益和方差的计算、理解分散化原理、效用函数应用
- **必考题型**：组合方差计算、相关系数判断、CAL 分析、最优组合选择
- **最常犯错误**：组合方差忘记协方差项、相关系数范围误解、有效前沿范围判断错误
- 对考试影响：M01 的概念在 M02 CAPM 中被大量使用
