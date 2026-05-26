---
title: "M09 — Parametric and Non-Parametric Tests of Independence"
description: "CFA Level I 2026 official module: Parametric and Non-Parametric Tests of Independence"
module: M09
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 9: Parametric and Non-Parametric Tests of Independence"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M09: Parametric and Non-Parametric Tests of Independence

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Parametric and Non-Parametric Tests of Independence
- 9.01 | Introduction
- 9.02 | Tests Concerning Correlation
- 9.03 | Tests of Independence Using Contingency Table Data

## Learning Outcome Statements

The candidate should be able to:

- explain parametric and nonparametric tests of the hypothesis that the population correlation coefficient equals zero, and determine whether the hypothesis is rejected at a given level of significance
- explain tests of independence based on contingency table data

## Local Study Notes

### Migrated from `CFA_tier1/Quantitative_Methods/M09-Tests-of-Independence.md`

_Alignment score: 1.00. Original official module field: Module 9: Parametric and Non-Parametric Tests of Independence._

#### M09: Tests of Independence（独立性检验）

##### 1. 核心知识点

###### 1.1 相关系数检验（Test of Correlation）

**参数检验 — Pearson 相关系数 t 检验**：
`t = r × √[(n-2) / (1-r²)]`
- H₀: ρ = 0 （总体相关系数为零，即两变量无线性关系）
- H₁: ρ ≠ 0 （总体相关系数不为零，两变量存在线性关系）
- 自由度 df = n-2
- 假设条件：两变量服从双变量正态分布（Bivariate Normal Distribution）
- 这个检验与简单线性回归中斜率系数的 t 检验完全等价

**非参数检验 — Spearman 秩相关系数检验**：
- 基于数据的排序（Rank）而非原始数值
- 不要求正态分布假设
- 当数据不满足正态假设或有异常值时，Spearman 相关更可靠
- 适用于有序数据（Ordinal Data）

**两种检验方法对比**：

| 特性 | Pearson 参数检验 | Spearman 非参数检验 |
|------|-----------------|-------------------|
| 数据类型 | 连续变量（区间/比率尺度） | 有序变量或连续变量 |
| 分布假设 | 双变量正态分布 | 无分布假设 |
| 检测关系 | 线性关系 | 单调关系（不要求线性） |
| 异常值影响 | 敏感 | 不敏感 |

###### 1.2 列联表独立性检验（Contingency Table Independence Test）

**卡方独立性检验（Chi-Square Test of Independence）**：
- 用于检验两个分类变量（Categorical Variables）是否独立
- H₀: 两个变量独立
- H₁: 两个变量不独立（存在关联）

**检验统计量**：
`χ² = Σ[(观测频数 - 期望频数)² / 期望频数]`

其中期望频数计算公式为：
`期望频数 = (行合计 × 列合计) / 总样本量`

**自由度**：
`df = (r-1) × (c-1)`
- r = 行数，c = 列数

**注意事项**：
- 所有期望频数应 ≥ 5（否则卡方近似可能不可靠）
- 卡方检验是右尾检验（检验统计量越大越拒绝 H₀）
- 检验结果仅说明变量是否独立，不说明关联的强度或方向

> **注**：本模块 M09 仅包含独立性检验内容。简单线性回归内容已移至 [[M10-Simple-Linear-Regression]]。

##### 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `t = r√[(n-2)/(1-r²)]` | 相关系数 t 检验 | 检验总体相关系数 ρ = 0 |
| `χ² = Σ[(O-E)²/E]` | 卡方检验统计量 | 列联表独立性检验 |
| `E = (行合计×列合计)/n` | 期望频数 | 列联表期望值计算 |
| `df = (r-1)(c-1)` | 卡方检验自由度 | 列联表自由度计算 |
| `df = n-2` | 相关系数 t 检验自由度 | Pearson 相关性检验 |

##### 3. 常见考点与解题思路

**考点一：相关系数 t 检验计算**
- 给定 r 和 n，计算 t 统计量，与 t 临界值比较（自由度 df = n-2）
- 等价于回归中斜率系数的 t 检验（t 统计量完全相等）

**考点二：参数 vs 非参数检验选择**
- 数据满足正态分布且无异常值 → Pearson 参数检验
- 数据不满足正态分布、有序数据、或有异常值 → Spearman 非参数检验
- 注意 Spearman 检测的是单调关系（不一定是线性关系）

**考点三：列联表计算与分析**
- 给定列联表，先计算期望频数 E = (行合计 × 列合计) / n
- 再计算 χ² = Σ[(O-E)² / E]
- 与 χ² 临界值比较（df = (r-1)(c-1)，右尾检验）
- 若 χ² > 临界值 → 拒绝 H₀，变量不独立

**考点四：Spearman 与 Pearson 核心区别总结**
- Pearson：原始值、正态假设、线性关系、异常值敏感
- Spearman：秩（Rank）、无分布假设、单调关系、异常值不敏感

##### 4. 易错点提醒

1. **相关系数 t 检验的自由度 = n-2**，不是 n-1 — 与单样本 t 检验的自由度 n-1 混淆是 CFA 高频陷阱。
2. **Spearman 检验是非参数检验**，不要求正态分布假设。但 Pearson 检验要求双变量正态分布。
3. **卡方检验是右尾检验** — 即使备择假设 H₁ 是"不独立"（相当于双边），仍然只用右尾临界值。
4. **列联表的期望频数基于"独立"假设计算** — 计算方法为（行合计 × 列合计）/ 总样本量，不要与观测频数混淆。
5. **期望频数不能太小** — 通常要求所有期望频数 ≥ 5，否则卡方近似不可靠。
6. **相关 ≠ 因果** — 即使相关系数显著，也不意味着变量之间存在因果关系。
7. **卡方检验不说明关联方向或强度** — 它只判断是否存在关联，不提供关联的度量（如 Cramér's V）。

##### 5. 跨模块关联

- **[[M08-Hypothesis-Testing]]**：本模块是 M08 假设检验框架的直接应用。相关性 t 检验是参数检验的具体实例，Spearman 检验是非参数检验的应用。
- **[[M10-Simple-Linear-Regression]]**：相关系数的 t 检验与简单线性回归中斜率系数的 t 检验完全等价。在简单回归中 R² = r²。
- **[[M03-Statistical-Measures]]**：相关系数的概念在 M03 中引入（correlation intuition），本模块将其扩展为正式的统计检验。
- **[[M05-Portfolio-Mathematics]]**：协方差和相关系数是投资组合数学的核心概念，本模块的检验方法可用于检验资产收益相关性是否显著。
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
