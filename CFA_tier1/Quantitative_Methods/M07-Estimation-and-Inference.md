---
title: "M07: Estimation and Inference"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M07"
official_module: "Module 7: Estimation and Inference"
los_count: 3
difficulty: "概念+案例判断"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M07: Estimation and Inference

> **模块定位**：把投资问题翻译成收益率、现金流、统计推断和模型检验。 本模块聚焦 **Estimation and Inference**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Estimation and Inference
- 7.01 | Introduction
- 7.02 | Sampling Methods
- 7.03 | Central Limit Theorem and Inference
- 7.04 | Bootstrapping and Empirical Sampling Distributions

## Learning Outcome Statements

1. compare and contrast simple random, stratified random, cluster, convenience, and judgmental sampling and their implications for sampling error in an investment problem
2. explain the central limit theorem and its importance for the distribution and standard error of the sample mean
3. describe the use of resampling (bootstrap, jackknife) to estimate the sampling distribution of a statistic

---

## 1. 模块定位

### 7.1 学习任务
- **核心问题**：考试希望你用 `Estimation and Inference` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 7.2 考试角色
- **难度类型**：概念+案例判断。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 7.3 关键英文术语
- **Estimation and Inference（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Sampling Methods（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Central Limit Theorem and Inference（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Bootstrapping and Empirical Sampling Distributions（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 7.1 | compare and contrast simple random, stratified random, cluster, convenience, and judgmental sampling and their implications for sampling error in an investment problem | 比较相似概念的适用条件与差异 | 写出结论、依据、公式口径和限制条件。 |
| 7.2 | explain the central limit theorem and its importance for the distribution and standard error of the sample mean | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 7.3 | describe the use of resampling (bootstrap, jackknife) to estimate the sampling distribution of a statistic | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
7. Estimation and Inference
├─ 7.1 抽样方法（Sampling Methods）
│  ├─ 7.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 7.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 7.2 CLT 和标准误（Central Limit Theorem and Standard Error）
│  ├─ 7.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 7.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 7.3 重抽样估计量（Resampling Estimators）
│  ├─ 7.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 7.3.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 7.1 抽样方法（Sampling Methods）

**概率抽样（Probability Sampling）**：每个总体成员有已知的非零概率被抽中。

- **简单随机抽样（Simple Random Sampling）**：每个成员被抽中的概率相等。最基础的方法，但不一定总适用。
- **分层抽样（Stratified Random Sampling）**：先将总体分成若干层（Stratum，如按行业、市值分组），再在每层内随机抽样。**优势**：保证每层都有代表性，降低抽样误差。
- **整群抽样（Cluster Sampling）**：将总体分成若干群（如地理区域），随机抽取几个群，对群内全部成员调查。

**非概率抽样（Non-Probability Sampling）**：某些成员被选中的概率未知或为零。

- **便利抽样（Convenience Sampling）**：选取最容易获得的样本。速度快但代表性差。
- **判断抽样（Judgmental Sampling）**：基于研究者的主观判断选择样本。容易引入个人偏误。

**抽样误差与偏误（Sampling Error and Bias）**：
- 抽样误差（Sampling Error）：样本统计量与总体参数之间的差异，是随机性的自然结果
- 抽样偏误（Sampling Bias）：系统性的偏离，通常来自有缺陷的抽样设计
- 增大样本量可以降低抽样误差，但不能消除抽样偏误

**数据 snooping（Data Snooping / Data Mining Bias）**：
- 反复分析同一数据集直到发现"显著"模式 — 本质上是在挖掘随机噪声
- 解决方法：样本外检验（Out-of-Sample Test）

**前视偏误（Look-Ahead Bias）**：
- 使用在分析时点尚不可得的信息进行回测
- 例：用全年财务数据在年中做策略回测（Q2 时 Q4 数据尚未公布）

### 7.2 CLT 和标准误（Central Limit Theorem and Standard Error）

**中心极限定理（Central Limit Theorem, CLT）**：
- 如果样本容量 n 足够大（一般 n ≥ 30），样本均值的抽样分布近似服从正态分布
- 这个结论**不依赖于总体分布的形状**（即使总体是非正态的！）
- 样本均值的均值 ≈ 总体均值 μ
- 样本均值的标准差（即标准误）= σ / √n

**标准误（Standard Error of the Mean）**：
`SE = σ / √n` （已知总体标准差时）
`SE = s / √n` （未知总体标准差时，用样本标准差估计）

**标准误的含义**：标准误衡量的是样本均值的"不确定性" — 如果从同一总体重复抽样，样本均值之间的波动幅度。

> **【考试核心】** CLT 是统计推断的基石：它让我们即使在总体分布未知的情况下，也可以用正态分布进行区间估计和假设检验。

**标准误 vs 标准差**：
- 标准差（σ）：衡量单个观测值的离散度
- 标准误（σ/√n）：衡量样本均值的离散度
- 标准误 < 标准差，且随 n 增大而减小

### 7.3 重抽样估计量（Resampling Estimators）

**自助法（Bootstrap）**：
- 从样本中有放回重复抽样，每次抽取 n 个观测值，重复大量次数
- 对每个自助样本计算统计量，形成该统计量的经验抽样分布
- 详见 [[M06-Simulation-Methods]] 中 1.3 节的展开

**刀切法（Jackknife）**：
- 每次从样本中**剔除一个观测值**（Leave-One-Out），计算统计量
- 对所有 n 个可能的剔除组合做平均
- 主要用于估计统计量的偏误（Bias）和方差
- 计算成本比 Bootstrap 低（只需要 n 次计算），但信息量较少

> **【Bootstrap vs Jackknife 辨析】**
> - **Bootstrap**：有放回重抽原始数据（每次抽取 n 个），用各次重抽样本的 mean 的分布来估计标准误（Standard Error），而非直接从原始数据计算 SD。
> - **Jackknife**：逐次删除一个观测值，重新计算统计量，通过 n 次结果的变化幅度估计偏误（Bias），不是用于去除异常值。
> - **区分要点**：Bootstrap 估标准误（SE）；Jackknife 估偏误（Bias）。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `SE = σ/√n` | 标准误（已知总体 σ） | CLT 应用 |
| `SE = s/√n` | 标准误（用样本 s 估计） | 常见考试场景 |
| `Sampling Error = x̄ - μ` | 抽样误差 | 评估样本估计精度 |
| `n = (zσ/E)²` | 所需样本量 | E = 期望的 margin of error |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 7.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 7.2 Sampling Methods | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 7.3 Central Limit Theorem and Inference | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 7.4 Bootstrapping and Empirical Sampling Distributions | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

**考点一：CLT 的应用条件**
- 问：何时样本均值的抽样分布为正态？
- 答：(1) 总体本身就是正态分布，或 (2) 样本容量足够大（n ≥ 30）
- 注意：CLT 不要求总体服从正态分布

**考点二：计算标准误**
- 给总体标准差 σ 和样本大小 n → SE = σ/√n
- 给样本标准差 s 和样本大小 n → SE = s/√n
- 注意区分总体标准差 σ 和样本标准差 s

**考点三：判断抽样方法优劣**
- 一个研究采用了 convenience sample → 指出潜在的偏误
- 怎样的样本设计可以减少偏误 → 推荐 stratified random sampling

**考点四：标准误与样本量的关系**
- SE 与 √n 成反比
- 要将 SE 减半，需要将样本量增至 4 倍

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 只背 Estimation and Inference 的英文名，不解释中文含义 | ✅ 用中文说清定义、适用条件和考试动作 | 术语题和情境题都会考定义边界。 |
| ❌ 看到公式就直接套，不检查口径 | ✅ 先检查时间、单位、现金流方向、会计口径或统计假设 | CFA 常把错误藏在输入口径里。 |
| ❌ 把显著性、相关性或高分数直接当成好结论 | ✅ 还要看经济含义、限制条件和跨模块证据 | 数量结果必须回到投资解释。 |

## 8. 跨模块关联

- **上游模块**：[[M06-Simulation-Methods]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M08-Hypothesis-Testing]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- **[[M03-Statistical-Measures]]**：样本方差 `s² = Σ(x_i-x̄)²/(n-1)` 的标准误概念在这里应用。
- **[[M06-Simulation-Methods]]**：Bootstrap 在此作为重抽样估计量出现，与 M06 的模拟方法形成完整的方法链条。
- **[[M08-Hypothesis-Testing]]**：标准误是假设检验中检验统计量的分母。CLT 使 z-test 和 t-test 成为可能。
- **[[M09-Correlation-and-Regression]]**：回归系数的标准误（SE of slope coefficient）是 M07 标准误概念在回归框架中的推广。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M07-Sampling-and-Estimation.md` (high, 0.787)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
