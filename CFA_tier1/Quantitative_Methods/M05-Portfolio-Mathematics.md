---
title: "M05 — Portfolio Mathematics"
description: 投资组合数学 — 期望收益, 方差, 协方差, 相关系数, 分散化, 短缺风险
module: M05
official_module: "Module 5: Portfolio Mathematics"
subject: Quantitative_Methods
los:
  - calculate and interpret the expected value, variance, standard deviation, covariances, and correlations of portfolio returns
  - calculate and interpret the covariance and correlation of portfolio returns using a joint probability function for returns
  - define shortfall risk, calculate the safety-first ratio, and identify an optimal portfolio using Roy's safety-first criterion
---

# M05: Portfolio Mathematics（投资组合数学）

## 1. 核心知识点

### 1.1 收益率矩（Return Moments）

**组合期望收益率（Portfolio Expected Return）**：
`E(R_p) = w_1 × E(R_1) + w_2 × E(R_2) + ... + w_n × E(R_n)`
- 组合期望收益率为各资产期望收益率的加权平均
- 权重 w_i 之和必须为 1（全额投资组合，Fully Invested Portfolio）

**两资产组合方差（Two-Asset Portfolio Variance）**：
`σ_p² = w_1²σ_1² + w_2²σ_2² + 2w_1w_2Cov(R_1, R_2)`
- 或者用相关系数形式：`σ_p² = w_1²σ_1² + w_2²σ_2² + 2w_1w_2σ_1σ_2ρ_12`
- 组合标准差 = `√σ_p²`

**关键直觉**：组合风险不是资产风险的简单加权平均。协方差项 Cov(R_1, R_2) 决定了分散化的效果。

**多资产组合方差（列成矩阵形式）**：
`σ_p² = ΣΣ w_iw_jCov(R_i, R_j)`
- 对角线上是各资产自身的方差项
- 非对角线上是资产两两之间的协方差项

### 1.2 联合概率函数（Joint Probability Function）

**协方差（Covariance）**：衡量两个变量同向变动的程度。
`Cov(R_1, R_2) = Σ p_i × [R_1,i - E(R_1)] × [R_2,i - E(R_2)]`
- Cov > 0：同向变动
- Cov < 0：反向变动
- Cov = 0：没有线性关系

**相关系数（Correlation Coefficient）**：
`ρ_12 = Cov(R_1, R_2) / (σ_1 × σ_2)`
- 范围 [-1, +1]，标准化后的协方差
- ρ = +1：完全正相关，无分散化效果
- ρ = -1：完全负相关，可完全消除风险
- ρ = 0：无线性相关，仍有分散化效果

**联合概率表（Joint Probability Table）**：考试常用 2×2 或 3×3 概率表给出不同情景下两只股票的收益率和概率。从这张表可以算出：
- 各资产的期望收益（边际概率加权）
- 协方差（联合概率加权交叉乘积）
- 相关系数

### 1.3 分散化机制（Diversification Mechanics）

**分散化的数学本质**：当 ρ < 1 时，组合方差的协方差项 2w_1w_2Cov_12 小于 2w_1w_2σ_1σ_2，组合风险低于加权平均风险。

**极端情况**：
- ρ = +1：组合标准差 = w_1σ_1 + w_2σ_2（无分散化）
- ρ = -1：组合标准差 = |w_1σ_1 - w_2σ_2|（完全对冲可能）
- ρ = 0：组合方差 = w_1²σ_1² + w_2²σ_2²（有限度分散）

**最小方差组合（Minimum Variance Portfolio, MVP）**：整个组合可行集（Feasible Set）中风险最小的权重组合。对于两资产组合：
`w_1* = [σ_2² - Cov_12] / [σ_1² + σ_2² - 2Cov_12]`

> **【考试陷阱】** 低 correlation 不等于负 expected return。可以找到低相关甚至负相关的资产，各自都有正的期望收益。

### 1.4 短缺风险（Shortfall Risk）

**罗伊安全优先比率（Roy's Safety-First Ratio, SFRatio）**：
`SFRatio = [E(R_p) - R_L] / σ_p`
- R_L = 阈值回报率（Threshold Return），投资者设定的最低可接受回报
- SFRatio 衡量组合期望回报超出阈值多少个标准差
- 在收益服从正态分布的假设下，SFRatio 越大的组合，跌破 R_L 的概率越低

**选择规则**：在所有候选组合中，选择 SFRatio 最大的组合。这等价于最小化跌破 R_L 的概率。

**与夏普比率（Sharpe Ratio）的区别**：
- Sharpe Ratio 使用无风险利率 R_f 作为基准
- Safety-First Ratio 使用投资者自定义的阈值 R_L（可能不等于 R_f）

## 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `E(R_p) = Σ w_iE(R_i)` | 组合期望收益 | 投资组合的预期回报 |
| `σ_p² = w_1²σ_1²+w_2²σ_2²+2w_1w_2Cov_12` | 两资产组合方差 | 计算组合风险 |
| `Cov_12 = Σ p_i[R_1,i-E(R_1)][R_2,i-E(R_2)]` | 协方差 | 衡量两变量同向变动 |
| `ρ_12 = Cov_12/(σ_1σ_2)` | 相关系数 | 标准化协方差范围 [-1,+1] |
| `SFRatio = [E(R_p)-R_L]/σ_p` | 安全优先比率 | 评估组合跌破阈值风险 |

## 3. 常见考点与解题思路

**考点一：计算组合期望收益和方差**
- 步骤 1：确认权重（权重和为 1）
- 步骤 2：算 E(R_p) = 加权平均
- 步骤 3：代入方差公式，注意协方差项乘以 2
- 步骤 4：开方得标准差

**考点二：从联合概率表算协方差**
- 步骤 1：从边际概率算各资产期望收益
- 步骤 2：对每个情景，算离差乘积 × 联合概率
- 步骤 3：加总

**考点三：分散化效果判断**
- 给定相关系数，判断组合风险 vs 加权平均风险
- 计算最小方差组合的权重

**考点四：Safety-First Ratio 选组合**
- 所有候选组合用 SFRatio 排序
- 选最大者

## 4. 易错点提醒

1. **协方差公式中的符号**：离差乘积为正表示同向，负表示反向 — 不要忽略符号。
2. **相关系数 ≠ 协方差**：相关系数标准化到 [-1, +1]，协方差无上下界。
3. **分散化降低的是风险不是收益**：低相关降低组合方差，但不必然降低期望收益。
4. **组合方差公式的双倍协方差项**：两资产公式中协方差项系数为 2，容易遗漏。
5. **权重和为 1**：考试会给权重比例，检查是否和为 1。若不是，需要先归一化。

## 5. 跨模块关联

- **[[M03-Statistical-Measures]]**：方差、标准差、相关系数的概念在 M03 中铺好基础；M05 将其扩展到多变量的组合场景。
- **[[M04-Probability-Concepts]]**：联合概率函数是概率论在投资组合中的直接应用 — 期望值框架从单变量扩展到双变量。
- **[[M01-Rates-and-Returns]]**：杠杆回报公式 `R_p + (B/E)(R_p - r_D)` 在理解组合权重和杠杆效应时是重要扩展。
- **Portfolio Management**：M05 的组合数学是 Markowitz 有效前沿和资产配置的理论基础。
