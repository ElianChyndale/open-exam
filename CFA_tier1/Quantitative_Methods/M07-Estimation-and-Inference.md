---
title: "M07 — Estimation and Inference"
description: "CFA Level I 2026 official module: Estimation and Inference"
module: M07
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 7: Estimation and Inference"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M07: Estimation and Inference

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Estimation and Inference
- 7.01 | Introduction
- 7.02 | Sampling Methods
- 7.03 | Central Limit Theorem and Inference
- 7.04 | Bootstrapping and Empirical Sampling Distributions

## Learning Outcome Statements

The candidate should be able to:

- compare and contrast simple random, stratified random, cluster, convenience, and judgmental sampling and their implications for sampling error in an investment problem
- explain the central limit theorem and its importance for the distribution and standard error of the sample mean
- describe the use of resampling (bootstrap, jackknife) to estimate the sampling distribution of a statistic

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M07: Estimation and Inference（抽样与估计）
│
├── ⭐ 抽样方法 (Sampling Methods)
│   ├── 概率抽样 (Probability Sampling)
│   │   ├── 简单随机抽样: 每个成员被抽中概率相等
│   │   ├── 分层抽样: 先分层再每层内随机抽 → 降低抽样误差
│   │   └── 整群抽样: 随机抽群再调查群内全部
│   ├── 非概率抽样 (Non-Probability Sampling)
│   │   ├── 便利抽样: 最易获取 → 速度快但代表性差
│   │   └── 判断抽样: 研究者主观选择 → 易引入偏误
│   └── ⚠️ 概率抽样更具代表性，非概率抽样易引入偏误
│
├── ⭐ 抽样误差与偏误 (Sampling Error & Bias)
│   ├── 📐 抽样误差 = x̄ - μ（随机性自然结果）
│   ├── 抽样偏误: 系统性偏离，来自有缺陷的抽样设计
│   ├── 增大样本量 → 降低抽样误差，但不消除抽样偏误
│   ├── Data Snooping: 反复分析方法数据 → 样本外检验
│   └── Look-Ahead Bias: 使用时点尚不可得的信息
│
├── ⭐ 中心极限定理 (Central Limit Theorem)
│   ├── n 足够大 (n ≥ 30) → 样本均值抽样分布 ≈ 正态
│   ├── 不依赖总体分布形状（即使总体非正态！）
│   ├── 样本均值均值 ≈ μ；样本均值标准差 = σ/√n
│   └── 💡 CLT 是统计推断的基石
│
├── ⭐ 标准误 (Standard Error)
│   ├── 📐 已知总体 σ: SE = σ/√n
│   ├── 📐 未知总体 σ: SE = s/√n（用样本标准差估计）
│   ├── SE 衡量样本均值的"不确定性"
│   ├── 💡 SE < σ（标准差），且随 n↑ 而减小
│   └── ⚠️ 标准误 ≠ 标准差
│
├── ⭐ 重抽样估计量 (Resampling Estimators)
│   ├── Bootstrap: 有放回重抽样 n 个，重复大量次数
│   │   └── 🎯 估标准误 (SE)
│   ├── Jackknife: 每次删除一个观测值，估偏误
│   │   └── 🎯 估偏误 (Bias)
│   └── ⚠️ Bootstrap 估 SE，Jackknife 估 Bias — 用途不同
│
├── 💡 关键洞察
│   ├── CLT 的伟大之处：不依赖总体分布，使得推断普遍可行
│   ├── 标准误 = 标准差 / √n — SE 随 n 增大而减小
│   ├── 扩大样本量不解决系统性偏误 — 代表性比大小更重要
│   ├── Data Snooping 和 Look-Ahead 是回测中最隐蔽的两大 bias
│   └── Probability Sampling > Non-Probability Sampling
│
└── ⚠️ 考试陷阱总结
    ├── 标准误 vs 标准差：SE = σ/√n，不是 σ
    ├── CLT 条件：n ≥ 30，不要求总体正态
    ├── 大样本不解决偏误 — bias 是系统性的
    ├── Bootstrap 估 SE，Jackknife 估 Bias
    ├── Data Snooping → 样本外验证
    └── Sampling Error 定义: 统计量 - 参数
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `SE = σ/√n` | 标准误（已知总体 σ） | CLT 区间估计 | σ 是总体标准差 |
| `SE = s/√n` | 标准误（用样本 s 估计） | 常见考试场景 | s 是样本标准差 |
| `Sampling Error = x̄ - μ` | 抽样误差 | 评估样本估计精度 | 随机性的自然结果 |
| `n = (zσ/E)²` | 所需样本量公式 | E = 期望 margin of error | 先确定 z 和 E |
| **Bootstrap**: 有放回重抽 n 个 | 重抽样估 SE | 统计量抽样分布 | 不解决原始偏误 |
| **Jackknife**: 逐次留一 | 重抽样估 Bias | 统计量偏误估计 | 计算成本比 Bootstrap 低 |

### 🛠️ 常见考点与解题思路

**考点1：CLT 的应用条件**
- 问：何时样本均值的抽样分布为正态？
- 答：(1) 总体本身就是正态分布，或 (2) n ≥ 30
- CLT 不要求总体服从正态分布 — 这是核心考点
- ⚠️ CLT 仍然需要独立同分布 (i.i.d.) 抽样

**考点2：计算标准误**
- 给总体 σ 和 n → SE = σ/√n
- 给样本 s 和 n → SE = s/√n
- ⚠️ 区分总体标准差和样本标准差

**考点3：判断抽样方法优劣**
- Convenience sample → 指出代表性不足的偏误
- 推荐改进 → Stratified Random Sampling（保证各层代表性）
- Probability vs Non-Probability → 考试必考分类题

**考点4：标准误与样本量的关系**
- SE 与 √n 成反比
- SE 减半 → 需要 4 倍样本量
- n → 4n → SE → SE/2

**考点5：Bootstrap vs Jackknife 区分**
- Bootstrap：有放回重抽 → 估 SE
- Jackknife：留一法 → 估 Bias
- ⚠️ 考试可能将两者对比出题

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 标准误 = 样本标准差 | 标准误 = 样本标准差/√n | 标准误是样本均值的标准差 |
| CLT 要求总体正态分布 | CLT 在 n≥30 时适用于任何分布 | CLT 的伟大之处就是不需要总体正态 |
| 大样本可以消除抽样偏误 | 大样本降低抽样误差，不消除偏误 | 偏误是系统性的，不是随机性的 |
| Bootstrap 估 Bias，Jackknife 估 SE | Bootstrap 估 SE，Jackknife 估 Bias | 两者用途正好相反 |
| Sampling Error = x̄ 与 μ 的比值 | Sampling Error = x̄ - μ（差值） | 是差不是比 |
| 大样本 = 好样本 | 代表性比大小更重要 | 有偏的大样本不如随机的小样本 |

### 🔄 跨模块关联

- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 样本方差 s² = Σ(xᵢ-x̄)²/(n-1) 的标准误概念在此应用。
- **[[M06-Simulation-Methods]]** — Bootstrap 作为重抽样估计量，与 M06 的模拟方法形成完整方法链条。
- **[[M08-Hypothesis-Testing]]** — 标准误是假设检验中检验统计量的分母。CLT 使 z-test 和 t-test 成为可能。
- **[[M10-Simple-Linear-Regression]]** — 回归系数的标准误 SE(b₁) 是 M07 标准误概念在回归框架中的推广。

### 📋 复习与刷题提示

- **核心能力**：区分五种抽样方法，掌握 CLT 的条件和含义，熟练计算标准误
- **必考题型**：CLT 条件判断、标准误计算、抽样方法分类、Bootstrap vs Jackknife
- **最常犯错误**：标准误与标准差混淆、CLT 误认为需要总体正态、大样本与偏误的关系理解偏差
- 记忆口诀：
  - 标准误 = 标准差 ÷ √n
  - CLT：n ≥ 30，不挑分布
  - 分层抽样 = 层内随机，保证代表性
  - Bootstrap 估 SE，Jackknife 估 Bias
- 刷题建议：重点做抽样方法分类题和标准误计算题
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
