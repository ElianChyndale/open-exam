---
title: "M08: Hypothesis Testing"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M08"
official_module: "Module 8: Hypothesis Testing"
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

# M08: Hypothesis Testing

> **模块定位**：把投资问题翻译成收益率、现金流、统计推断和模型检验。 本模块聚焦 **Hypothesis Testing**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Hypothesis Testing
- 8.01 | Introduction
- 8.02 | Hypothesis Tests for Finance
- 8.03 | Tests of Return and Risk in Finance
- 8.04 | Parametric versus Nonparametric Tests

## Learning Outcome Statements

1. explain hypothesis testing and its components, including statistical significance, Type I and Type II errors, and the power of a test
2. construct hypothesis tests and determine their statistical significance, the associated Type I and Type II errors, and power of the test given a significance level
3. compare and contrast parametric and nonparametric tests, and describe situations where each is the more appropriate type of test

---

## 1. 模块定位

### 8.1 学习任务
- **核心问题**：考试希望你用 `Hypothesis Testing` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 8.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 8.3 关键英文术语
- **Hypothesis Testing（假设检验）**：用样本证据判断总体命题是否应被拒绝。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Hypothesis Tests for Finance（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Tests of Return and Risk in Finance（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Parametric versus Nonparametric Tests（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 8.1 | explain hypothesis testing and its components, including statistical significance, Type I and Type II errors, and the power of a test | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 8.2 | construct hypothesis tests and determine their statistical significance, the associated Type I and Type II errors, and power of the test given a significance level | 根据条件判断正确结论 | 写出结论、依据、公式口径和限制条件。 |
| 8.3 | compare and contrast parametric and nonparametric tests, and describe situations where each is the more appropriate type of test | 比较相似概念的适用条件与差异；描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
8. Hypothesis Testing
├─ 8.1 检验构件（Test Components）
│  ├─ 8.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 8.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 8.2 错误结构（Error Architecture）
│  ├─ 8.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 8.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 8.3 参数与非参数检验（Parametric vs Nonparametric）
│  ├─ 8.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 8.3.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 8.4 双样本检验（Two-Sample Tests）
│  ├─ 8.4.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 8.4.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 8.5 单样本方差检验（Chi-Square Test for a Single Variance）
│  ├─ 8.5.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 8.5.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 8.1 检验构件（Test Components）

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

### 8.2 错误结构（Error Architecture）

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

### 8.3 参数与非参数检验（Parametric vs Nonparametric）

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

### 8.4 双样本检验（Two-Sample Tests）

双样本检验是比较两个总体参数是否相等的一类方法。CFA 一级主要考察均值比较和比例比较，并延伸至方差比较。

#### 8.4.1 双样本均值检验 — 方差相等（Pooled Variance t-Test）

**适用条件**：两个总体服从正态分布（或近似正态），方差相等但未知。

**合并估计量 s_p²（Pooled Estimator of Common Variance）**：

`s_p² = [(n₁ - 1)s₁² + (n₂ - 1)s₂²] / (n₁ + n₂ - 2)`

- 将两个样本的方差信息"加权合并"为一个共同方差的估计值
- 权重来自各自的自由度（n₁-1 和 n₂-1）

**检验统计量**：

`t = (x̄₁ - x̄₂ - d₀) / (s_p × √(1/n₁ + 1/n₂))`

- 自由度 df = n₁ + n₂ - 2
- d₀ 是 H₀ 中假设的均值差（通常 d₀ = 0）

#### 8.4.2 双样本均值检验 — 方差不相等（Unequal Variance t-Test / Welch's Approximation）

**适用条件**：两个总体服从正态分布（或近似正态），方差不等。

**特点**：
- **不合并方差**，分别使用各自的样本方差 s₁² 和 s₂²
- 检验统计量近似为 t 分布：

`t = [(x̄₁ - x̄₂) - d₀] / √(s₁²/n₁ + s₂²/n₂)`

- d₀ 是 H₀ 中假设的均值差（通常 d₀ = 0）
- 自由度经 Satterthwaite 公式调整：

`df = (s₁²/n₁ + s₂²/n₂)² / [((s₁²/n₁)²/(n₁-1)) + ((s₂²/n₂)²/(n₂-1))]`

  - df 取整后介于 min(n₁-1, n₂-1) 和 n₁+n₂-2 之间
- 不需要 n₁ = n₂
- 考试中通常用软件输出结果，手动计算较少

> **【场景速判】** 题目条件说"assume equal variances"或"总体方差相等"
> → 用 **Pooled t-test**（1.4.1）；说"variances are not assumed equal"
> 或未提及方差假设 → 用 **Unequal Variance t-test**（1.4.2）。

#### 8.4.3 双样本方差检验（F-Test for Equality of Two Variances）

检验两个独立总体的方差是否相等。

**假设形式**：
- H₀: σ₁² = σ₂²
- H₁: σ₁² ≠ σ₂²（双边）或 σ₁² > σ₂²（单边）

**检验统计量**：

`F = s₁² / s₂²`

- 其中 s₁² 和 s₂² 分别是两个样本的样本方差
- **约定**：通常将较大的 s² 放在分子（方便单边比较）

**F 分布**：
- F 统计量服从 F 分布，需要两个自由度：
  - df₁ = n₁ - 1（分子自由度）
  - df₂ = n₂ - 1（分母自由度）
- F 值总是 ≥ 0，分布呈右偏
- F 临界值查 F 分布表（α、df₁、df₂）

**注意事项**：
- F 检验对正态性假设**非常敏感**，总体偏离正态时结果不可靠
- F 检验是双样本 t 检验中判断"是否用 pooled"的前提依据之一
- 在 CFA 一级中通常直接给出方差假设，不需要考生先运行 F 检验再决定

#### 8.4.4 配对比较检验（Paired Comparisons Test / Dependent Samples t-Test）

比较两个**相关（配对）样本**的均值是否存在显著差异。

**适用场景**：
- 同一组对象的前测-后测（before/after）
- 匹配样本（matched pairs），如双胞胎分别接受不同处理
- 本质上是**对差值 dᵢ = X₁ᵢ - X₂ᵢ 做单样本 t 检验**

**假设形式**：
- H₀: μ_d = 0（配对差值的总体均值为零）
- H₁: μ_d ≠ 0（双边）或 μ_d > 0 / μ_d < 0（单边）

**检验统计量**：

`t = d̄ / (s_d / √n)`

- d̄ = 配对差值的样本均值
- s_d = 配对差值的样本标准差
- n = 配对个数（不是样本总量）
- 自由度 df = n - 1

**与独立样本 t 检验的区别**：
- 配对检验消除了个体间差异，只关注组内变化 → 检验力更高
- 独立样本检验需要更大的样本量才能达到相同的检验力
- **考试判断**：如果题目描述是同一组对象在不同条件下（如 before/after），或是显式的"matched pairs"，选 **paired comparisons test**

#### 8.4.5 双样本比例检验（Two-Sample Test of Proportions）

检验两个独立总体的比例是否相等。

`z = (p̂₁ - p̂₂ - d₀) / √[p̂(1-p̂)(1/n₁ + 1/n₂)]`

- 其中 p̂ 是两个样本的**合并比例**：p̂ = (x₁ + x₂) / (n₁ + n₂)
- x₁、x₂ 分别为两个样本中具有某特征的数量
- 使用 z 分布（大样本下近似正态）

#### 8.4.6 双样本检验方法总结

| 检验类型                         | 检验对象    | 检验统计量                                  | 分布            | 关键假设                     |
| ---------------------------- | ------- | -------------------------------------- | ------------- | ------------------------ |
| Pooled t-test                | μ₁ - μ₂ | `t = (x̄₁-x̄₂)/[s_p√(1/n₁+1/n₂)]`      | t(n₁+n₂-2)    | 正态总体、方差**相等**            |
| Unequal Variance t-test      | μ₁ - μ₂ | `t = [(x̄₁-x̄₂)-d₀]/√(s₁²/n₁+s₂²/n₂)` | 近似 t（df 调整） | 正态总体、方差**不等**            |
| Paired Comparisons t-test    | μ_d     | `t = d̄/(s_d/√n)`                      | t(n-1)        | **配对/相关**样本，对差值做单样本 t 检验 |
| F-test                       | σ₁²/σ₂² | `F = s₁²/s₂²`                          | F(n₁-1, n₂-1) | 正态总体，方差相等                |
| Two-Sample Proportion z-test | p₁ - p₂ | `z = (p̂₁-p̂₂)/√[p̂(1-p̂)(1/n₁+1/n₂)]` | z             | 大样本                      |

### 8.5 单样本方差检验（Chi-Square Test for a Single Variance）

检验单个总体的方差是否等于某个特定值。

**卡方分布（Chi-Square Distribution）**：
- 卡方分布是**非对称**的右偏分布（最小值 = 0，无负值）
- 形状由自由度 df 决定，df 越小偏度越大，df 增大时趋近正态分布
- 卡方分布是 t 检验和 F 检验的基础构件：`t²(1) = χ²(1)`，`F = χ²₁/df₁ ÷ χ²₂/df₂`

**假设形式**：
- H₀: σ² = σ₀²
- H₁: σ² ≠ σ₀²（双边）或 σ² > σ₀²（右尾）或 σ² < σ₀²（左尾）

**检验统计量**：

`χ² = (n - 1)s² / σ₀²`

- n = 样本量，s² = 样本方差，σ₀² = 原假设中的总体方差
- 自由度 df = n - 1
- 在 H₀ 成立时服从 χ²(n-1) 分布

**确定拒绝域**：

- **右尾检验**（H₁: σ² > σ₀²）：`χ² > χ²_α(n-1)`
- **左尾检验**（H₁: σ² < σ₀²）：`χ² < χ²_(1-α)(n-1)`
- **双边检验**（H₁: σ² ≠ σ₀²）：`χ² < χ²_(1-α/2)(n-1)` 或 `χ² > χ²_(α/2)(n-1)`

**注意事项**：

- 卡方方差检验对正态性假设**极其敏感**——总体偏离正态时结果不可靠
- 与 F 检验（比较两个总体方差）不同，卡方检验针对**单个**总体方差
- CFA 一级考试中，卡方检验出现频率低于 z/t 检验，但属于常考知识点

## 5. 关键公式与计算框架

### 5.1 核心内容

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `z = (x̄-μ₀)/(σ/√n)` | z 检验统计量 | 总体方差已知时的均值检验 |
| `t = (x̄-μ₀)/(s/√n)` | t 检验统计量 | 总体方差未知时的均值检验 |
| `CI: x̄ ± z_(α/2) × σ/√n` | 置信区间（σ 已知） | 总体参数区间估计 |
| `CI: x̄ ± t_(α/2,n-1) × s/√n` | 置信区间（σ 未知） | 参数估计常用方法 |
| `n = (z_α/₂ × σ / E)²` | 所需样本量 | E = margin of error |
| `s_p² = [(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)` | 合并估计量 | 两总体方差相等时的双样本 t 检验 |
| `t = (x̄₁-x̄₂-d₀)/(s_p·√(1/n₁+1/n₂))` | 双样本 t 检验统计量 | df = n₁+n₂-2，比较两个独立总体均值 |
| `t = [(x̄₁-x̄₂)-d₀]/√(s₁²/n₁+s₂²/n₂)` | 方差不等双样本 t 检验统计量 | 不合并方差，df 使用 Satterthwaite 调整 |
| `F = s₁²/s₂²` | F 检验统计量 | 检验两个总体方差是否相等，df₁=n₁-1, df₂=n₂-1 |
| `t = d̄/(s_d/√n)` | 配对比较 t 检验统计量 | df = n-1，n 为配对个数，d̄ 为差值均值 |
| `χ² = (n-1)s²/σ₀²` | 卡方检验统计量 | 检验单个总体方差是否等于特定值，df = n-1 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 8.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 8.2 Hypothesis Tests for Finance | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 8.3 Tests of Return and Risk in Finance | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 8.4 Parametric versus Nonparametric Tests | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

**考点一：构建假设检验**
- 步骤 1：写 H₀ 和 H₁（判断单边还是双边）
- 步骤 2：选择检验统计量（z 还是 t）choose a arefa
- 步骤 3：确定拒绝域（查临界值）choose critical value/decision rule
- 步骤 4：计算检验统计量test statistic
- 步骤 5：比较并做结论reject/fail to reject

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

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 只背 Hypothesis Testing 的英文名，不解释中文含义 | ✅ 用中文说清定义、适用条件和考试动作 | 术语题和情境题都会考定义边界。 |
| ❌ 看到公式就直接套，不检查口径 | ✅ 先检查时间、单位、现金流方向、会计口径或统计假设 | CFA 常把错误藏在输入口径里。 |
| ❌ 把显著性、相关性或高分数直接当成好结论 | ✅ 还要看经济含义、限制条件和跨模块证据 | 数量结果必须回到投资解释。 |

## 8. 跨模块关联

- **上游模块**：[[M07-Estimation-and-Inference]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M09-Parametric-and-Non-Parametric-Tests-of-Independence]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- **[[M07-Sampling-and-Estimation]]**：标准误 SE = σ/√n 是假设检验的基础构件。CLT 为 z-test 和 t-test 的正态近似提供理论依据。
- **[[M09-Correlation-and-Regression]]**：回归系数的 t 检验和整体模型的 F 检验是假设检验框架在回归中的直接推广。
- **[[M03-Statistical-Measures]]**：检验统计量的分布依赖于样本统计量的性质（如样本均值的正态近似）。
- **[[M04-Probability-Concepts]]**：p-value 本质上是概率分布尾部概率的应用。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M08-Hypothesis-Testing.md` (high, 0.872)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
