---
title: "M06: Simulation Methods"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M06"
official_module: "Module 6: Simulation Methods"
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

# M06: Simulation Methods

> **模块定位**：把投资问题翻译成收益率、现金流、统计推断和模型检验。 本模块聚焦 **Simulation Methods**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Simulation Methods
- 6.01 | Introduction
- 6.02 | Lognormal Distribution and Continuous Compounding
- 6.03 | Monte Carlo Simulation
- 6.04 | Bootstrapping

## Learning Outcome Statements

1. explain the relationship between normal and lognormal distributions and why the lognormal distribution is used to model asset prices when using continuously compounded asset returns
2. describe Monte Carlo simulation and explain how it can be used in investment applications
3. describe the use of bootstrap resampling in conducting a simulation based on observed data in investment applications

---

## 1. 模块定位

### 6.1 学习任务
- **核心问题**：考试希望你用 `Simulation Methods` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 6.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 6.3 关键英文术语
- **Simulation Methods（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Lognormal Distribution and Continuous Compounding（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Monte Carlo Simulation（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Bootstrapping（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 6.1 | explain the relationship between normal and lognormal distributions and why the lognormal distribution is used to model asset prices when using continuously compounded asset returns | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 6.2 | describe Monte Carlo simulation and explain how it can be used in investment applications | 描述定义、流程和适用场景；解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 6.3 | describe the use of bootstrap resampling in conducting a simulation based on observed data in investment applications | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
6. Simulation Methods
├─ 6.1 分布联动（Distribution Link）
│  ├─ 6.1.1 连续复利收益率：若 `r_cc ~ N(μ,σ²)`，价格由 `P_t=P_0e^r` 推出
│  ├─ 6.1.2 价格对数正态：价格非负、右偏，适合资产价格建模
│  └─ 6.1.3 判断陷阱：收益率可近似正态，不代表价格可用正态分布
├─ 6.2 蒙特卡洛模拟（Monte Carlo Simulation）
│  ├─ 6.2.1 输入：指定变量分布、参数、相关结构和模型关系
│  ├─ 6.2.2 抽样：生成大量随机情景，尤其适合复杂、非线性、路径依赖问题
│  ├─ 6.2.3 输出：汇总结果分布、均值、方差、分位数和 shortfall probability
│  └─ 6.2.4 风险：garbage in garbage out，模型假设错会使结果精密但错误
├─ 6.3 自助重抽样（Bootstrap Resampling）
│  ├─ 6.3.1 数据来源：从历史样本有放回抽取 n 个观测，重复多次
│  ├─ 6.3.2 用途：估计统计量抽样分布、标准误或置信区间
│  └─ 6.3.3 限制：继承原始样本偏差，不能凭空创造未出现过的尾部结构
```

## 4. 知识点详解

### 6.1 分布联动（Distribution Link）

一个重要的分布关系链：

**连续复利收益率 → 正态分布假设 → 价格 → 对数正态分布**

- **连续复利收益率（Continuously Compounded Returns）** 通常假设服从正态分布（Normal Distribution）。这是蒙特卡洛模拟的基础假设。
- 由正态收益率导出的**价格呈对数正态分布（Lognormal Distribution）**，意味着价格恒为非负（Nonnegative）。
- 对数正态分布有右偏特征，符合资产价格的典型表现：价格不能为负，且更可能出现大涨（右侧长尾）。

**为什么用对数正态而不用正态来建模价格？**
- 正态分布允许价格为负（虽然概率很小），这在经济上不合理
- 对数正态分布天然保证价格非负
- 收益率用正态，价格用对数正态 — 这是经典的金融建模框架

### 6.2 蒙特卡洛模拟（Monte Carlo Simulation）

蒙特卡洛模拟是一种通过生成大量随机样本来近似复杂系统行为的计算方法。

**三个核心步骤（Three Core Steps）**：

1. **指定输入分布（Specify Input Distribution）**：确定关键变量的概率分布及其参数（如回报率服从 μ=8%，σ=15% 的正态分布）。
2. **抽取随机情景（Draw Random Scenarios）**：从输入分布中随机抽样，生成大量（如 10,000 个）可能的未来情景。
3. **汇总输出分布（Summarize Output Distribution）**：将所有情景的结果汇总为分布，计算均值、方差、分位数等统计量。

**蒙特卡洛模拟的价值（Why Monte Carlo Matters）**：
- 可以处理没有解析解（Closed-Form Solution）的复杂问题
- 例如：复杂的退休储蓄规划、路径依赖型衍生品定价、含多个不确定因素的资本预算分析
- 输出是所有可能结果的全部分布，而不仅仅是"最好的估计"

**蒙特卡洛模拟的局限性（Limitations）**：
- 不提供因果解释（What-If 分析），只给出"如果输入如此，输出可能如此"
- 结果的质量取决于输入分布假设的正确性（Garbage In, Garbage Out）
- 计算量大，需要大量随机抽样才能获得稳定结果
- 抽样误差（Sampling Error）随模拟次数增加而降低，但永远不能完全消除

### 6.3 自助重抽样（Bootstrap Resampling）

自助法是一种从已有数据中通过有放回重复抽样来估计统计量分布的方法。

**自助法的核心思想**：
- 原始样本容量为 n
- 从原始样本中**有放回地（with Replacement）**抽取 n 个观测值 → 得到一个自助样本（Bootstrap Sample）
- 重复这个过程大量次数（如 10,000 次），对每个自助样本计算目标统计量
- 这些统计量的分布即为抽样分布（Sampling Distribution）的近似

**自助法的适用场景**：
- 当解析公式不可用或不准确时（如中位数的抽样分布）
- 当样本容量较小时
- 不需要对总体分布做强的假设（属于非参数方法）

> **【考试陷阱】** Bootstrap 不能克服原始样本本身的局限性。如果原始样本有偏（Selection Bias）或不是随机样本，自助法会**继承（Inherit）**这些偏误。

**自助法 vs 蒙特卡洛模拟**：
| 对比项 | 蒙特卡洛模拟 | 自助法 |
|--------|-------------|--------|
| 数据来源 | 人为指定的概率分布 | 实际观测数据 |
| 抽样方式 | 从理论分布中抽样 | 从经验分布中有放回抽样 |
| 主要用途 | 预测未知的未来情景 | 估计已知样本的统计量精度 |
| 分布假设 | 需要指定分布形式和参数 | 几乎无分布假设（非参数） |

## 5. 关键公式与计算框架

### 5.1 核心内容

本模块以概念理解为主，不涉及复杂公式。

| 概念 | 解释 | 使用场景 |
|------|------|----------|
| 连续复利收益率 ~ N(μ, σ²) | 收益率正态假设 | 蒙特卡洛输入分布 |
| 价格 ~ Lognormal | 价格对数正态 | 资产价格建模 |
| 有放回重抽样 n 次 | Bootstrap 抽样 | 估计统计量分布 |
| `P_t = P_0e^r` | 连续复利价格映射 | 从正态收益率得到对数正态价格 |
| `Simulation SE ↓ as trials ↑` | 模拟误差随次数下降 | 增加模拟次数提高稳定性但不修正模型错设 |

### 5.2 方法选择框架

| 题干条件 | 选择 | 对应节点 | 判断句 |
|---|---|---|---|
| 有清晰解析解 | analytical solution | `6.2` | 通常更快更精确。 |
| 多变量、非线性、路径依赖 | Monte Carlo | `6.2` | 输出完整分布而非单点预测。 |
| 没有总体分布假设，但有历史样本 | Bootstrap | `6.3` | 从经验分布有放回抽样。 |
| 原始样本有偏或太短 | 不盲信 bootstrap | `6.3.3` | 重抽样会复制偏差。 |
| 建模价格 | lognormal price | `6.1` | 正态价格可能出现负值。 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 6.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 6.2 Lognormal Distribution and Continuous Compounding | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.3 Monte Carlo Simulation | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.4 Bootstrapping | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

**考点一：正态回报 → 对数正态价格的关系**
- 给定连续复利收益率的均值和标准差
- 价格 P_t = P_0 × e^(rt)，其中 r ~ N(μ, σ²)
- P_t 服从参数 μ 和 σ 的对数正态分布

**考点二：蒙特卡洛 vs 分析解（Analytical Solution）的选择**
- 有解析解时（如简单期权的 Black-Scholes），解析解更精确
- 无解析解时（如路径依赖期权、复杂多资产组合），选择蒙特卡洛模拟

**考点三：Bootstrap 的优缺点**
- 优点：不依赖分布假设、适用于复杂统计量
- 缺点：继承原始数据局限、不适用于小样本的极端情况

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 只背 Simulation Methods 的英文名，不解释中文含义 | ✅ 用中文说清定义、适用条件和考试动作 | 术语题和情境题都会考定义边界。 |
| ❌ 看到公式就直接套，不检查口径 | ✅ 先检查时间、单位、现金流方向、会计口径或统计假设 | CFA 常把错误藏在输入口径里。 |
| ❌ 把显著性、相关性或高分数直接当成好结论 | ✅ 还要看经济含义、限制条件和跨模块证据 | 数量结果必须回到投资解释。 |

## 8. 跨模块关联

| 输出节点 | 连接模块/科目 | 如何被调用 | 易错接口 |
|---|---|---|---|
| `6.1` 正态收益/对数正态价格 | [[M01-Rates-and-Returns]]、Derivatives | 连续复利和期权/价格模拟 | 收益率分布和价格分布不要混。 |
| `6.2` Monte Carlo | Risk Management、Derivatives、Corporate Issuers | 压力场景、复杂项目、路径依赖 payoff | 模拟次数不能修复错误输入分布。 |
| `6.2` 输出分布 | [[M03-Statistical-Measures-of-Asset-Returns]]、PM | 均值、波动、分位数和 shortfall | 只看平均值会漏掉尾部风险。 |
| `6.3` Bootstrap | [[M07-Estimation-and-Inference]]、[[M08-Hypothesis-Testing]] | 标准误、经验置信区间、非参数推断 | 原样本偏差会被继承。 |

### Legacy 关联补充

- **[[M01-Rates-and-Returns]]**：连续复利收益率 `r_cc = ln(1+HPR)` 是分布联动基础的起点。
- **[[M03-Statistical-Measures]]**：模拟输出的分布分析（均值、方差、偏度、峰度）是 M03 统计量的直接应用。
- **[[M04-Probability-Concepts]]**：蒙特卡洛模拟的本质就是概率论的迭代扩展 — 从已知分布抽样并汇总。
- **[[M07-Sampling-and-Estimation]]**：Bootstrap 是重抽样估计的核心方法，与 CLT 提供互补的推断路径。
- **[[M08-Hypothesis-Testing]]**：Bootstrap 可以用于构建非参数假设检验（如 Bootstrap Confidence Interval）。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M06-Simulation-Methods.md` (high, 0.9)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
