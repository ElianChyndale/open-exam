---
title: "M05: Portfolio Mathematics"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M05"
official_module: "Module 5: Portfolio Mathematics"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M05: Portfolio Mathematics

> **模块定位**：把投资问题翻译成收益率、现金流、统计推断和模型检验。 本模块聚焦 **Portfolio Mathematics**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Portfolio Mathematics
- 5.01 | Introduction
- 5.02 | Portfolio Expected Return and Variance of Return
- 5.03 | Forecasting Correlation of Returns: Covariance Given a Joint Probability Function
- 5.04 | Portfolio Risk Measures: Applications of the Normal Distribution

## Learning Outcome Statements

1. calculate and interpret the expected value, variance, standard deviation, covariances, and correlations of portfolio returns
2. calculate and interpret the covariance and correlation of portfolio returns using a joint probability function for returns
3. define shortfall risk, calculate the safety-first ratio, and identify an optimal portfolio using Roy’s safety-first criterion

---

## 1. 模块定位

### 5.1 学习任务
- **核心问题**：考试希望你用 `Portfolio Mathematics` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 5.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 5.3 关键英文术语
- **Portfolio Mathematics（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Portfolio Expected Return and Variance of Return（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Forecasting Correlation of Returns: Covariance Given a Joint Probability Function（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Forecasting Correlation of Returns（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Portfolio Risk Measures: Applications of the Normal Distribution（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Portfolio Risk Measures（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Correlation（相关系数）**：衡量两个变量线性同向或反向变化的程度。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 5.1 | calculate and interpret the expected value, variance, standard deviation, covariances, and correlations of portfolio returns | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |
| 5.2 | calculate and interpret the covariance and correlation of portfolio returns using a joint probability function for returns | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |
| 5.3 | define shortfall risk, calculate the safety-first ratio, and identify an optimal portfolio using Roy’s safety-first criterion | 计算并解释数值结果；识别题干中的关键事实和触发条件 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
5. Portfolio Mathematics
├─ 5.1 收益率矩（Return Moments）
│  ├─ 5.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 5.2 联合概率函数（Joint Probability Function）
│  ├─ 5.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 5.3 分散化机制（Diversification Mechanics）
│  ├─ 5.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.3.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 5.4 短缺风险（Shortfall Risk）
│  ├─ 5.4.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.4.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 5.1 收益率矩（Return Moments）

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

### 5.2 联合概率函数（Joint Probability Function）

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

### 5.3 分散化机制（Diversification Mechanics）

**分散化的数学本质**：当 ρ < 1 时，组合方差的协方差项 2w_1w_2Cov_12 小于 2w_1w_2σ_1σ_2，组合风险低于加权平均风险。

**极端情况**：
- ρ = +1：组合标准差 = w_1σ_1 + w_2σ_2（无分散化）
- ρ = -1：组合标准差 = |w_1σ_1 - w_2σ_2|（完全对冲可能）
- ρ = 0：组合方差 = w_1²σ_1² + w_2²σ_2²（有限度分散）

**最小方差组合（Minimum Variance Portfolio, MVP）**：整个组合可行集（Feasible Set）中风险最小的权重组合。对于两资产组合：
`w_1* = [σ_2² - Cov_12] / [σ_1² + σ_2² - 2Cov_12]`

> **【考试陷阱】** 低 correlation 不等于负 expected return。可以找到低相关甚至负相关的资产，各自都有正的期望收益。

### 5.4 短缺风险（Shortfall Risk）

**罗伊安全优先比率（Roy's Safety-First Ratio, SFRatio）**：
`SFRatio = [E(R_p) - R_L] / σ_p`
- R_L = 阈值回报率（Threshold Return），投资者设定的最低可接受回报
- SFRatio 衡量组合期望回报超出阈值多少个标准差
- 在收益服从正态分布的假设下，SFRatio 越大的组合，跌破 R_L 的概率越低

**选择规则**：在所有候选组合中，选择 SFRatio 最大的组合。这等价于最小化跌破 R_L 的概率。

**与夏普比率（Sharpe Ratio）的区别**：
- Sharpe Ratio 使用无风险利率 R_f 作为基准
- Safety-First Ratio 使用投资者自定义的阈值 R_L（可能不等于 R_f）

## 5. 关键公式与计算框架

### 5.1 核心内容

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `E(R_p) = Σ w_iE(R_i)` | 组合期望收益 | 投资组合的预期回报 |
| `σ_p² = w_1²σ_1²+w_2²σ_2²+2w_1w_2Cov_12` | 两资产组合方差 | 计算组合风险 |
| `Cov_12 = Σ p_i[R_1,i-E(R_1)][R_2,i-E(R_2)]` | 协方差 | 衡量两变量同向变动 |
| `ρ_12 = Cov_12/(σ_1σ_2)` | 相关系数 | 标准化协方差范围 [-1,+1] |
| `SFRatio = [E(R_p)-R_L]/σ_p` | 安全优先比率 | 评估组合跌破阈值风险 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 5.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 5.2 Portfolio Expected Return and Variance of Return | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.3 Forecasting Correlation of Returns: Covariance Given a Joint Probability Function | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.4 Portfolio Risk Measures: Applications of the Normal Distribution | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

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

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 只背 Portfolio Mathematics 的英文名，不解释中文含义 | ✅ 用中文说清定义、适用条件和考试动作 | 术语题和情境题都会考定义边界。 |
| ❌ 看到公式就直接套，不检查口径 | ✅ 先检查时间、单位、现金流方向、会计口径或统计假设 | CFA 常把错误藏在输入口径里。 |
| ❌ 把显著性、相关性或高分数直接当成好结论 | ✅ 还要看经济含义、限制条件和跨模块证据 | 数量结果必须回到投资解释。 |

## 8. 跨模块关联

- **上游模块**：[[M04-Probability-Trees-and-Conditional-Expectations]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M06-Simulation-Methods]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- **[[M03-Statistical-Measures]]**：方差、标准差、相关系数的概念在 M03 中铺好基础；M05 将其扩展到多变量的组合场景。
- **[[M04-Probability-Concepts]]**：联合概率函数是概率论在投资组合中的直接应用 — 期望值框架从单变量扩展到双变量。
- **[[M01-Rates-and-Returns]]**：杠杆回报公式 `R_p + (B/E)(R_p - r_D)` 在理解组合权重和杠杆效应时是重要扩展。
- **Portfolio Management**：M05 的组合数学是 Markowitz 有效前沿和资产配置的理论基础。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M05-Portfolio-Mathematics.md` (high, 0.86)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
