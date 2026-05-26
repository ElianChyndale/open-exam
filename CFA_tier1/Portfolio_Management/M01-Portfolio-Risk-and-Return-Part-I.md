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

### 📐 关键公式表

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
