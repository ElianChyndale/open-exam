---
title: "M06 — Simulation Methods"
description: "CFA Level I 2026 official module: Simulation Methods"
module: M06
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 6: Simulation Methods"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M06: Simulation Methods

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Simulation Methods
- 6.01 | Introduction
- 6.02 | Lognormal Distribution and Continuous Compounding
- 6.03 | Monte Carlo Simulation
- 6.04 | Bootstrapping

## Learning Outcome Statements

The candidate should be able to:

- explain the relationship between normal and lognormal distributions and why the lognormal distribution is used to model asset prices when using continuously compounded asset returns
- describe Monte Carlo simulation and explain how it can be used in investment applications
- describe the use of bootstrap resampling in conducting a simulation based on observed data in investment applications

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M06: Simulation Methods（模拟方法）
│
├── ⭐ 分布联动关系 (Distribution Link)
│   ├── 连续复利收益率 → 正态分布假设 → 价格 → 对数正态分布
│   ├── 💡 收益率用正态（可负），价格用对数正态（非负）
│   ├── 对数正态分布天然保证价格 ≥ 0，且右偏符合资产价格特征
│   └── ⚠️ 正态分布允许价格为负（经济上不合理），不能用正态建模价格
│
├── ⭐ 蒙特卡洛模拟 (Monte Carlo Simulation)
│   ├── 步骤 1：指定输入分布（如收益率 ~ N(μ, σ²)）
│   ├── 步骤 2：抽取大量随机情景（如 10,000 个）
│   ├── 步骤 3：汇总输出分布（均值、方差、分位数）
│   ├── 📐 P_t = P₀ × e^(rt)，r ~ N(μ, σ²)
│   ├── 🎯 适用：无解析解的复杂问题
│   ├── ⚠️ 非优化方法 — 不告诉你"应该怎么做"
│   └── ⚠️ GIGO: 输入分布准确性决定结果价值
│
├── ⭐ 自助重抽样 (Bootstrap Resampling)
│   ├── 从原始样本中有放回抽取 n 个观测值
│   ├── 重复大量次数 → 得到统计量的经验抽样分布
│   ├── 🎯 适用：解析公式不可用、样本量小、无分布假设
│   ├── 🎯 非参数方法 — 几乎不依赖分布假设
│   └── ⚠️ Bootstrap 继承原始样本的偏误（不解决 bias）
│
├── ⭐ 蒙特卡洛 vs Bootstrap 对比
│   ├── 数据来源：MC = 人为指定分布，Bootstrap = 实际观测数据
│   ├── 抽样方式：MC = 理论分布抽样，Bootstrap = 有放回重抽样
│   ├── 主要用途：MC = 预测未来，Bootstrap = 估计样本统计量精度
│   └── 分布假设：MC = 需要指定，Bootstrap = 几乎无假设
│
├── 💡 关键洞察
│   ├── 正态收益率 → 对数正态价格，这是经典金融建模框架
│   ├── MC 解决"无解析解"问题，但结果质量完全依赖输入假设
│   ├── Bootstrap 是"用数据说话"的方法，但继承数据所有缺陷
│   └── 增加模拟次数只降低抽样误差，不改善输入质量
│
└── ⚠️ 考试陷阱总结
    ├── 蒙特卡洛不是优化方法，也不是分析方法
    ├── GIGO: 错误假设 × 大量模拟 ≠ 正确结果
    ├── Bootstrap 不解决原始样本的偏误问题
    ├── 收益率 ~ 正态，价格 ~ 对数正态 — 不要混淆
    └── 解析解优先于模拟（当解析解存在时）
```

### 📐 关键公式表

| 概念 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| 连续复利收益率 ~ N(μ, σ²) | 收益率正态假设 | MC 输入分布设定 | 收益率可负，符合正态 |
| 价格 ~ 对数正态 | 价格恒为非负 | 资产价格建模 | 右偏分布，无负值 |
| `P_t = P₀ × e^(rt)` | 价格路径公式 | MC 模拟价格路径 | r 从 N(μ,σ²) 抽样 |
| Bootstrap: 有放回重抽样 n 次 | 从经验分布抽样 | 估计统计量抽样分布 | 不解决原始样本偏误 |
| MC 三步骤: 设定 → 抽样 → 汇总 | 模拟流程 | 无解析解场景 | 不是优化方法 |

### 🛠️ 常见考点与解题思路

**考点1：正态回报 → 对数正态价格的关系**
- 给定连续复利收益率的 μ 和 σ，r ~ N(μ, σ²)
- P_t = P₀ × e^(rt)，其中 r 从 N(μ, σ²) 中抽样
- P_t 服从参数 μ 和 σ 的对数正态分布 (Lognormal)
- 对数正态分布特征：恒非负、右偏、符合资产价格典型表现
- ⚠️ 收益率用正态，价格用对数正态 — 两者对应关系是考试核心
- 💡 正态允许负值（收益率可以负），对数正态保证非负（价格不能负）

**考点2：蒙特卡洛 vs 解析解的选择**
- 有解析解时（如 Black-Scholes 期权定价、简单债券定价）→ 解析解更精确、计算更快
- 无解析解时（路径依赖期权、复杂多资产组合、退休储蓄规划）→ MC 模拟
- MC 输出 = 全部可能结果的分布（不仅是点估计）
- ⚠️ MC 不优于解析解，只是在无解析解时的替代方案
- 💡 解析解提供精确公式，MC 提供数值近似

**考点3：蒙特卡洛模拟三步骤流程**
- 步骤 1：指定输入分布 (Specify Input Distribution)
  - 确定关键变量的概率分布及其参数
  - 例：回报率 ~ N(μ=8%, σ=15%)
- 步骤 2：抽取随机情景 (Draw Random Scenarios)
  - 从输入分布中大量随机抽样（如 10,000 次）
  - 每次抽样 = 一个可能的未来情景
- 步骤 3：汇总输出分布 (Summarize Output Distribution)
  - 计算均值、方差、分位数等统计量
  - 分析各种结果的发生概率
- ⚠️ MC 不是优化方法 — 不告诉你"应该怎么做"

**考点4：Bootstrap 的优缺点**
- 优点：
  - 不依赖分布假设（非参数方法）
  - 适用于复杂统计量（中位数、分位数等）
  - 实现简单（有放回抽样即可）
- 缺点：
  - 继承原始样本的所有局限（有偏样本 → 有偏结果）
  - 小样本时结果不可靠
  - 计算量大（需要大量重抽样）
- ⚠️ Bootstrap 不解决原始样本的偏误问题

**考点5：MC vs Bootstrap 核心区别**
- 数据来源：MC = 人为指定的概率分布；Bootstrap = 实际观测数据
- 抽样方式：MC = 从理论分布中抽样；Bootstrap = 从经验分布中有放回抽样
- 主要用途：MC = 预测未知的未来情景；Bootstrap = 估计已知样本的统计量精度
- 分布假设：MC = 需要指定分布形式和参数；Bootstrap = 几乎无分布假设

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 正态分布可建模资产价格 | 资产价格用对数正态分布 | 正态允许负价格，经济上不合理 |
| MC 是优化方法 | MC 是模拟方法，不是优化 | MC 只回答"如果...会怎样"，不告诉"该怎么做" |
| Bootstrap 能消除样本偏误 | Bootstrap 继承原始样本偏误 | 有放回抽样不改变样本的分布特征 |
| 增加模拟次数提高结果准确性 | 增加模拟次数降低抽样误差，但不改善输入质量 | GIGO：错误假设 × 大量模拟 ≠ 正确 |
| MC 优于解析解 | 有解析解时解析解优于 MC | 解析解更精确，计算更快 |

### 🔄 跨模块关联

- **[[M01-Rates-and-Returns]]** — 连续复利收益率 `r_cc = ln(1+HPR)` 是分布联动基础的起点。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 模拟输出的分布分析（均值、方差、偏度、峰度）是 M03 统计量的直接应用。
- **[[M04-Probability-Trees-and-Conditional-Expectations]]** — MC 模拟本质是概率论的迭代扩展。
- **[[M07-Estimation-and-Inference]]** — Bootstrap 是重抽样估计的核心方法，与 CLT 形成互补推断路径。
- **[[M08-Hypothesis-Testing]]** — Bootstrap 可用于构建非参数假设检验（Bootstrap 置信区间）。

### 📋 复习与刷题提示

- **核心能力**：理解正态→对数正态推导逻辑，区分 MC 与 Bootstrap 的适用场景
- **必考题型**：MC vs 解析解选择、Bootstrap 优缺点判断、正态/对数正态区分
- **最常犯错误**：用正态建模价格、认为 MC 优于解析解、认为 Bootstrap 能消除偏误
- 记忆口诀：
  - 正态收益率，对数正态价格 — 经典搭配
  - MC 模拟未来，Bootstrap 评估过去
  - GIGO：垃圾进，垃圾出
- 刷题建议：本模块概念题为主，重点掌握 MC 和 Bootstrap 的适用场景对比
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
