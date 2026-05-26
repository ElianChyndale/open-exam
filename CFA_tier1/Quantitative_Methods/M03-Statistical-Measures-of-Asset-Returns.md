---
title: "M03: Statistical Measures of Asset Returns"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M03"
official_module: "Module 3: Statistical Measures of Asset Returns"
los_count: 4
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M03: Statistical Measures of Asset Returns

> **模块定位**：把投资问题翻译成收益率、现金流、统计推断和模型检验。 本模块聚焦 **Statistical Measures of Asset Returns**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Statistical Measures of Asset Returns
- 3.01 | Introduction
- 3.02 | Measures of Central Tendency and Location
- 3.03 | Measures of Dispersion
- 3.04 | Measures of Shape of a Distribution
- 3.05 | Correlation between Two Variables

## Learning Outcome Statements

1. calculate, interpret, and evaluate measures of central tendency and location to address an investment problem
2. calculate, interpret, and evaluate measures of dispersion to address an investment problem
3. interpret and evaluate measures of skewness and kurtosis to address an investment problem
4. interpret correlation between two variables to address an investment problem

---

## 1. 模块定位

### 3.1 学习任务
- **核心问题**：考试希望你用 `Statistical Measures of Asset Returns` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 3.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 3.3 关键英文术语
- **Statistical Measures of Asset Returns（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Measures of Central Tendency and Location（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Measures of Dispersion（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Measures of Shape of a Distribution（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Correlation between Two Variables（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Statistical Measures（统计度量）**：用均值、离散程度、偏度和峰度描述收益分布。
- **Correlation（相关系数）**：衡量两个变量线性同向或反向变化的程度。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 3.1 | calculate, interpret, and evaluate measures of central tendency and location to address an investment problem | 计算并解释数值结果；解释结果的投资含义；评价优缺点、限制和决策含义 | 写出结论、依据、公式口径和限制条件。 |
| 3.2 | calculate, interpret, and evaluate measures of dispersion to address an investment problem | 计算并解释数值结果；解释结果的投资含义；评价优缺点、限制和决策含义 | 写出结论、依据、公式口径和限制条件。 |
| 3.3 | interpret and evaluate measures of skewness and kurtosis to address an investment problem | 解释结果的投资含义；评价优缺点、限制和决策含义 | 写出结论、依据、公式口径和限制条件。 |
| 3.4 | interpret correlation between two variables to address an investment problem | 解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
3. Statistical Measures of Asset Returns
├─ 3.1 集中趋势与位置指标（Central Tendency and Location）
│  ├─ 3.1.1 Arithmetic mean：`Σx_i/n`，适合单期期望或对称分布中心
│  ├─ 3.1.2 Geometric mean：`[Π(1+R_i)]^(1/n)-1`，适合多期复合收益
│  ├─ 3.1.3 Harmonic mean：`n/Σ(1/x_i)`，适合 P/E 等价格倍数平均
│  ├─ 3.1.4 Median / mode：偏态或 outlier 场景中 median 更代表 typical value
│  └─ 3.1.5 Quantile：`L_p=(n+1)p/100`，用于 percentile、quartile、VaR 直觉
├─ 3.2 离散程度（Dispersion）
│  ├─ 3.2.1 Range / MAD：直观但 range 对极端值最敏感
│  ├─ 3.2.2 Population variance：`Σ(x_i-μ)^2/N`
│  ├─ 3.2.3 Sample variance：`Σ(x_i-x̄)^2/(n-1)`，看到 sample 用 `n-1`
│  ├─ 3.2.4 Standard deviation：与原数据同单位，是常用风险尺度
│  ├─ 3.2.5 Downside deviation：只看低于目标收益的偏差，连接 Sortino/downside risk
│  └─ 3.2.6 CV：`s/x̄`，比较不同均值水平的相对离散度
├─ 3.3 分布形态（Distribution Shape）
│  ├─ 3.3.1 Skewness：看长尾方向；右偏 mean > median > mode，左偏相反
│  ├─ 3.3.2 Kurtosis：看尾部厚度；normal kurtosis=3，excess kurtosis=kurtosis-3
│  └─ 3.3.3 Investment judgment：负偏和厚尾意味着极端损失风险更高
├─ 3.4 相关性直觉（Correlation Intuition）
│  ├─ 3.4.1 Correlation range：`[-1,+1]`，符号是方向，绝对值是线性强度
│  ├─ 3.4.2 Portfolio use：低相关资产降低组合方差
│  └─ 3.4.3 判断陷阱：相关不是因果，高相关也不保证回归模型可用
```

## 4. 知识点详解

### 3.1 集中趋势与位置指标（Central Tendency and Location）

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

### 3.2 离散程度（Dispersion）

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

### 3.3 分布形态（Distribution Shape）

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

### 3.4 相关性直觉（Correlation Intuition）

- **相关系数（Correlation Coefficient）**范围 [-1, +1]
- 符号 = 方向（+ 同向变化，- 反向变化）
- 大小 = 线性关联强度（绝对值越大，线性关系越强）
- **相关 ≠ 因果（Correlation ≠ Causation）**：两个变量相关不代表一个导致另一个

## 5. 关键公式与计算框架

### 5.1 核心内容

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `μ = Σx_i/N` | 总体均值 | 已知总体的数据平均 |
| `x̄ = Σx_i/n` | 样本均值 | 样本数据平均 |
| `σ² = Σ(x_i-μ)²/N` | 总体方差 | 已知总体的离散度 |
| `s² = Σ(x_i-x̄)²/(n-1)` | 样本方差 | 样本估计总体方差 |
| `CV = s / x̄` | 变异系数 | 比较不同尺度的离散度 |
| `Skewness = E[(X-μ)³]/σ³` | 偏度 | 判断分布不对称方向 |
| `Excess Kurtosis = Kurtosis - 3` | 超额峰度 | 判断尾部厚度 |
| `Geometric Mean = [Π(1+R_i)]^(1/n)-1` | 几何平均 | 多期复合收益 |
| `Harmonic Mean = n/Σ(1/x_i)` | 调和平均 | 价格倍数平均 |
| `L_p = (n+1)p/100` | 百分位位置 | 排序数据分位数 |
| `MAD = Σ|x_i-x̄|/n` | 平均绝对偏差 | 相对稳健的离散度 |
| `Chebyshev lower bound = 1 - 1/k²` | 切比雪夫下界 | 任意分布，k 个标准差内至少比例 |

### 5.2 指标选择框架

| 题干目标 | 首选指标 | 对应节点 | 判断句 |
|---|---|---|---|
| 单期期望中心 | arithmetic mean | `3.1.1` | 对 outlier 敏感。 |
| 多期复合增长 | geometric mean | `3.1.2` | 波动越大，几何均值越低于算术均值。 |
| 平均估值倍数 | harmonic mean | `3.1.3` | 适合 P/E、P/B 等 ratio。 |
| typical value 且偏态 | median | `3.1.4` | 比均值更抗 outlier。 |
| 样本风险 | sample variance / s | `3.2.3` | 分母用 `n-1`。 |
| 相对风险比较 | CV | `3.2.6` | 均值不同的资产可比。 |
| 尾部风险 | skewness + kurtosis | `3.3` | 负偏/厚尾更危险。 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 3.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 3.2 Measures of Central Tendency and Location | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 3.3 Measures of Dispersion | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 3.4 Measures of Shape of a Distribution | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐ | 3.5 Correlation between Two Variables | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

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

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：1. 样本方差用 n-1：考试最常见的统计陷阱 — 看到"sample"字样就要用 n-1。 | ✅ 1. 样本方差用 n-1：考试最常见的统计陷阱 — 看到"sample"字样就要用 n-1。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 输出节点 | 连接模块/科目 | 如何被调用 | 易错接口 |
|---|---|---|---|
| `3.1` 均值 | [[M01-Rates-and-Returns]]、Performance reporting | 算术/几何/调和均值分别对应单期、多期、倍数 | 不要用 arithmetic mean 描述长期复合财富增长。 |
| `3.2` 方差/标准差 | [[M05-Portfolio-Mathematics]]、PM | 单资产风险扩展成组合方差 | 样本方差分母不是 n。 |
| `3.2` downside/CV | Portfolio Management、Risk Management | 下行风险和单位收益风险比较 | CV 在均值接近 0 时解释不稳。 |
| `3.3` skew/kurtosis | Alternatives、Risk Management | 非正态资产的尾部风险识别 | Fat tails 对应 kurtosis，不是 skewness。 |
| `3.4` correlation | [[M09-Parametric-and-Non-Parametric-Tests-of-Independence]]、Regression | 后续检验相关性和建立回归 | 相关不等于因果，也不说明模型没有遗漏变量。 |

### Legacy 关联补充

- **[[M01-Rates-and-Returns]]**：三种均值（算术/几何/调和）在 M01 收益率度量中首次出现。
- **[[M04-Probability-Concepts]]**：统计量的概率版本 — 期望值 E(X) 是概率加权均值，Var(X) 是概率加权方差。
- **[[M05-Portfolio-Mathematics]]**：组合方差公式是 M03 方差概念的延伸 — 从单变量到双变量。
- **[[M09-Correlation-and-Regression]]**：相关系数在此引入直觉，在 M09 中扩展到回归框架的正式检验。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M03-Statistical-Measures.md` (high, 0.906)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
