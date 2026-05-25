---
title: "M03 — Statistical Measures of Asset Returns"
description: 统计量与分布特征 — 均值, 方差, 偏度, 峰度, 相关系数
module: M03
official_module: "Module 3: Statistical Measures of Asset Returns"
subject: Quantitative_Methods
los:
  - calculate, interpret, and evaluate measures of central tendency and location to address an investment problem
  - calculate, interpret, and evaluate measures of dispersion to address an investment problem
  - interpret and evaluate measures of skewness and kurtosis to address an investment problem
  - interpret correlation between two variables to address an investment problem
---

# M03: Statistical Measures（统计量与分布特征）

## 1. 核心知识点

### 1.1 集中趋势与位置指标（Central Tendency and Location）

**三种均值（Three Types of Mean）**：
- **算术平均（Arithmetic Mean）**：所有观测值之和除以观测个数。最常用的均值，但对极端值（Outliers）敏感。
- **几何平均（Geometric Mean）**：`[(1+R_1)×...×(1+R_n)]^(1/n) - 1`。适用于收益率等比率数据的平均。几何平均 ≤ 算术平均，差值反映波动率。
- **调和平均（Harmonic Mean）**：`n / Σ(1/x_i)`。适用于平均价格倍数，如平均 P/E 或平均速度。调和平均 ≤ 几何平均 ≤ 算术平均。

**中位数（Median）**：数据排序后的中间值。比均值更能抵抗极端值影响。当分布偏斜时，中位数比均值更代表"典型值"。

**众数（Mode）**：出现频率最高的值。
- 单峰分布（Unimodal）：一个众数
- 双峰分布（Bimodal）：两个众数
- 多峰分布（Multimodal）：多个众数

**分位数（Quantiles）**：
- 四分位数（Quartiles）：Q1（25th）、Q2（50th = 中位数）、Q3（75th）
- 百分位数（Percentiles）：第 p 百分位意味着 p% 的数据低于该值
- 分位数位置公式：`L_p = (n+1) × p/100`

> **【考试陷阱】** Outlier 对算术平均的影响远大于对中位数的影响。看到股票收益率包含极端值时，优先考虑中位数。

### 1.2 离散程度（Dispersion）

**极差（Range）**：最大值 - 最小值。最简单的离散度度量，但完全依赖两端极端值。

**平均绝对偏差（Mean Absolute Deviation, MAD）**：`Σ|x_i - x̄| / n`。衡量每个观测值与均值的平均距离，不易受极端值影响。

**方差与标准差（Variance and Standard Deviation）**：
- **总体方差（Population Variance）**：`σ² = Σ(x_i - μ)² / N`
- **样本方差（Sample Variance）**：`s² = Σ(x_i - x̄)² / (n-1)`
- 标准差（Standard Deviation）= √方差，与原始数据单位一致，更直观
- 样本方差用 n-1（而不是 n）做分母是为了无偏估计（Unbiased Estimation）
- 样本方差是无偏的（Unbiased），但样本标准差是有偏的（Biased）

> **【考试陷阱】** 忘掉 n-1 是最常见的错误。题目给的是总体还是样本数据决定了分母是 n 还是 n-1。

**下行偏差（Downside Deviation）**：只考虑低于目标收益率（或均值）的偏差。用于下行风险度量，如 Sortino Ratio。

**变异系数（Coefficient of Variation, CV）**：`CV = s / x̄`
- 衡量单位均值的风险（相对离散度）
- 用于比较不同尺度（不同均值水平）的数据集的离散程度

**夏普比率（Sharpe Ratio）的变体**：
`CV = σ / μ` — 投资中用于比较不同预期收益率的资产的风险调整回报。

### 1.3 分布形态（Distribution Shape）

**偏度（Skewness）**：衡量分布不对称程度。
- **正态分布（Normal Distribution）**：偏度为 0，完全对称
- **右偏/正偏（Positively Skewed）**：长尾在右侧，均值 > 中位数 > 众数
- **左偏/负偏（Negatively Skewed）**：长尾在左侧，均值 < 中位数 < 众数
- 判断左偏还是右偏：看**长尾方向**
- 偏度公式：`Skewness = E[(X - μ)³] / σ³`

> **【考试陷阱】** 左偏/右偏的判断常考：左偏意味着大量极端负值（左侧长尾），但 majority of data 在右侧。长尾方向决定了偏度的符号。

**峰度（Kurtosis）**：衡量尾部厚度（Tail Thickness）。
- **正态分布峰度 = 3**（超额峰度 Excess Kurtosis = 0）
- **尖峰厚尾（Leptokurtic）**：峰度 > 3，更多极端值，fat tails
- **低峰薄尾（Platykurtic）**：峰度 < 3，更少极端值
- 超额峰度（Excess Kurtosis）= 峰度 - 3
- 厚尾（Fat Tails）意味着极端事件（损失或收益）的概率高于正态分布

### 1.4 相关性直觉（Correlation Intuition）

- **相关系数（Correlation Coefficient）**范围 [-1, +1]
- 符号 = 方向（+ 同向变化，- 反向变化）
- 大小 = 线性关联强度（绝对值越大，线性关系越强）
- **相关 ≠ 因果（Correlation ≠ Causation）**：两个变量相关不代表一个导致另一个

## 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `μ = Σx_i/N` | 总体均值 | 已知总体的数据平均 |
| `x̄ = Σx_i/n` | 样本均值 | 样本数据平均 |
| `σ² = Σ(x_i-μ)²/N` | 总体方差 | 已知总体的离散度 |
| `s² = Σ(x_i-x̄)²/(n-1)` | 样本方差 | 样本估计总体方差 |
| `CV = s / x̄` | 变异系数 | 比较不同尺度的离散度 |
| `Skewness = E[(X-μ)³]/σ³` | 偏度 | 判断分布不对称方向 |
| `Excess Kurtosis = Kurtosis - 3` | 超额峰度 | 判断尾部厚度 |

## 3. 常见考点与解题思路

**考点一：均值与中位数的选择**
- 如果分布对称 → Mean = Median
- 如果分布右偏 → Mean > Median
- 如果分布左偏 → Mean < Median
- 题目通常会问哪个统计量更能代表"typical value"

**考点二：Chebyshev's Inequality（切比雪夫不等式）**
- 任何分布中，至少有 1 - 1/k² 的数据落在均值 k 个标准差内
- k=2：至少 75%；k=3：至少 89%

**考点三：标准差 vs 半标准差**
- 标准差衡量总波动（双侧）
- 半标准差只衡量下行波动（单侧）
- 考点：风险厌恶投资者更关注下行偏差

## 4. 易错点提醒

1. **样本方差用 n-1**：考试最常见的统计陷阱 — 看到"sample"字样就要用 n-1。
2. **左偏≠负值多**：左偏分布中大部分数据仍在正值区间，只是左侧长尾有极端负值。
3. **峰度看尾部不看尖峰**：高峰度 = 厚尾 + 更多极端值，不是简单"尖"。
4. **CV 要有意义的前提是均值不为零**：均值接近或等于零时 CV 失去意义。
5. **分位数位置 = (n+1)×p/100**：考试可能让你计算第 k 百分位数的位置和数值。
6. **最大可能中位数用法**：open-ended 分布（无上限或下限）只能用中位数，不能用均值。

## 5. 跨模块关联

- **[[M01-Rates-and-Returns]]**：三种均值（算术/几何/调和）在 M01 收益率度量中首次出现。
- **[[M04-Probability-Concepts]]**：统计量的概率版本 — 期望值 E(X) 是概率加权均值，Var(X) 是概率加权方差。
- **[[M05-Portfolio-Mathematics]]**：组合方差公式是 M03 方差概念的延伸 — 从单变量到双变量。
- **[[M09-Correlation-and-Regression]]**：相关系数在此引入直觉，在 M09 中扩展到回归框架的正式检验。
