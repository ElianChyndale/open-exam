---
title: "M08 — Hypothesis Testing"
description: 假设检验 — H0/H1, Type I/II, p-value, 置信区间, 参数与非参数检验
module: M08
official_module: "Module 8: Hypothesis Testing"
subject: Quantitative_Methods
los:
  - explain hypothesis testing and its components, including statistical significance, Type I and Type II errors, and the power of a test
  - construct hypothesis tests and determine their statistical significance, the associated Type I and Type II errors, and power of the test given a significance level
  - compare and contrast parametric and nonparametric tests, and describe situations where each is the more appropriate type of test
---

# M08: Hypothesis Testing（假设检验）

## 1. 核心知识点

### 1.1 检验构件（Test Components）

**原假设与备择假设（Null and Alternative Hypothesis）**：
- **原假设 H₀（Null Hypothesis）**：需要检验的"默认"陈述，通常代表"无差异"或"无效果"。是我们希望收集证据来拒绝的假设。
- **备择假设 H₁（Alternative Hypothesis）**：原假设不成立时成立的情况。
- 双边检验（Two-Tailed）：H₀: μ = μ₀ vs H₁: μ ≠ μ₀
- 单边检验（One-Tailed）：H₀: μ ≤ μ₀ vs H₁: μ > μ₀（右尾）；或 H₀: μ ≥ μ₀ vs H₁: μ < μ₀（左尾）

**显著性水平 α（Significance Level）**：
- 第一类错误（Type I Error）的最大容许概率
- 常用 α = 0.05（5%）、0.01（1%）、0.10（10%）
- α 越小，拒绝 H₀ 的标准越严格

**检验统计量（Test Statistic）**：
`z = (x̄ - μ₀) / (σ/√n)` （已知总体方差）
`t = (x̄ - μ₀) / (s/√n)` （未知总体方差，用样本 s 估计）

**拒绝域（Rejection Region / Critical Region）**：
- 检验统计量落在拒绝域 → 拒绝 H₀
- z-test：用标准正态分布的临界值（如 α=0.05 时 z_crit = ±1.96）
- t-test：用 t 分布的临界值（自由度 df = n-1）

**p 值（p-Value）**：
- 在 H₀ 成立的前提下，观察到当前检验统计量（或更极端值）的概率
- p-value < α → 拒绝 H₀
- p-value 越小，反对 H₀ 的证据越强
- **注意**：p-value 不是 H₀ 为真的概率！它是"在 H₀ 下观察到当前样本的极端程度"

### 1.2 错误结构（Error Architecture）

| 决策 \ 真实状态 | H₀ 为真 | H₀ 为假 |
|-----------------|---------|---------|
| 不拒绝 H₀ | 正确决策 (1-α) | 第二类错误 (β) |
| 拒绝 H₀ | 第一类错误 (α) | 正确决策 (Power = 1-β) |

**第一类错误（Type I Error）**：拒绝了一个真实的原假设。概率 = α（显著水平）。

**第二类错误（Type II Error）**：未能拒绝一个错误的原假设。概率 = β。

**检验力（Power of a Test）**：
`Power = 1 - β` = 正确拒绝错误 H₀ 的概率

**影响检验力的因素**：
- 样本量 n ↑ → Power ↑（标准误 ↓，更容易检测到差异）
- 显著性水平 α ↑ → Power ↑（更容易拒绝 H₀，但也增加 Type I Error）
- 效应量（Effect Size）↑ → Power ↑（真实差异越大越容易检测到）

> **【考试核心】** 永远不要说"接受 H₀" — 只能说"不能拒绝 H₀"。两者不是同义词。不拒绝 H₀ 只是证据不足以拒绝，不代表 H₀ 一定成立。

### 1.3 参数与非参数检验（Parametric vs Nonparametric）

**参数检验（Parametric Test）**：
- 依赖关于总体分布的具体假设（如正态分布）
- 更有效率（当假设满足时，检验力更强）
- 例如：z-test、t-test、ANOVA F-test

**非参数检验（Nonparametric Test）**：
- 不做或很少做关于总体分布的假设
- 当参数检验的假设不满足（如严重非正态、序数数据）时使用
- 例如：Wilcoxon Signed-Rank Test、Mann-Whitney U Test

**何时选择非参数检验**：
- 数据是序数（Ordinal）而非区间（Interval）尺度
- 样本量很小，无法依赖 CLT
- 总体分布严重偏离正态，且无法通过变换修正

## 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `z = (x̄-μ₀)/(σ/√n)` | z 检验统计量 | 总体方差已知时的均值检验 |
| `t = (x̄-μ₀)/(s/√n)` | t 检验统计量 | 总体方差未知时的均值检验 |
| `CI: x̄ ± z_(α/2) × σ/√n` | 置信区间（σ 已知） | 总体参数区间估计 |
| `CI: x̄ ± t_(α/2,n-1) × s/√n` | 置信区间（σ 未知） | 参数估计常用方法 |
| `n = (z_α/₂ × σ / E)²` | 所需样本量 | E = margin of error |

## 3. 常见考点与解题思路

**考点一：构建假设检验**
- 步骤 1：写 H₀ 和 H₁（判断单边还是双边）
- 步骤 2：选择检验统计量（z 还是 t）
- 步骤 3：确定拒绝域（查临界值）
- 步骤 4：计算检验统计量
- 步骤 5：比较并做结论

**考点二：p-value 解读**
- p-value 是概率（在 H₀ 为真的条件下）
- p-value ≤ α → reject H₀
- 不能把 p-value 理解为"H₀ 为真的概率"

**考点三：置信区间与假设检验的关系**
- 如果 μ₀ 落在 (1-α)% 置信区间外 → 在 α 水平上拒绝 H₀
- 两者等价 — 置信区间提供了假设检验的图形化方式

**考点四：Type I / Type II Error 权衡**
- 减小 α（更严格）→ β 增大 → Power 减小
- 增大样本量可以同时降低 α 和 β

## 4. 易错点提醒

1. **"不拒绝" ≠ "接受"**：Difference between "not reject" and "accept"。只能说证据不足以拒绝，不能说 H₀ 已被证实。
2. **p-value 误解**：p-value 是"在 H₀ 下观察到该样本的极端概率"，不是"H₀ 为真的概率"。
3. **单边 vs 双边**：选择单边还是双边取决于 H₁ 否含方向。要在确定假设时决定，不能在看到结果后"优化选择"。
4. **检验力忘记检查**：不拒绝 H₀ 可能是因为效应量小或样本量不够，不一定是 H₀ 为真。
5. **z vs t 混淆**：t 检验用于总体方差未知且用样本 s 代替 σ 时。当 n 很大时，t 分布接近 z 分布。

## 5. 跨模块关联

- **[[M07-Sampling-and-Estimation]]**：标准误 SE = σ/√n 是假设检验的基础构件。CLT 为 z-test 和 t-test 的正态近似提供理论依据。
- **[[M09-Correlation-and-Regression]]**：回归系数的 t 检验和整体模型的 F 检验是假设检验框架在回归中的直接推广。
- **[[M03-Statistical-Measures]]**：检验统计量的分布依赖于样本统计量的性质（如样本均值的正态近似）。
- **[[M04-Probability-Concepts]]**：p-value 本质上是概率分布尾部概率的应用。
