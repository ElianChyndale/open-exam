---
title: "M08 — Hypothesis Testing"
description: "CFA Level I 2026 official module: Hypothesis Testing"
module: M08
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 8: Hypothesis Testing"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M08: Hypothesis Testing

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Hypothesis Testing
- 8.01 | Introduction
- 8.02 | Hypothesis Tests for Finance
- 8.03 | Tests of Return and Risk in Finance
- 8.04 | Parametric versus Nonparametric Tests

## Learning Outcome Statements

The candidate should be able to:

- explain hypothesis testing and its components, including statistical significance, Type I and Type II errors, and the power of a test
- construct hypothesis tests and determine their statistical significance, the associated Type I and Type II errors, and power of the test given a significance level
- compare and contrast parametric and nonparametric tests, and describe situations where each is the more appropriate type of test

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M08: Hypothesis Testing（假设检验）
│
├── ⭐ 检验构件 (Test Components)
│   ├── H₀ (原假设): 默认陈述，希望收集证据拒绝
│   ├── H₁ (备择假设): H₀ 不成立时成立的情况
│   ├── 📐 z = (x̄-μ₀)/(σ/√n) — 已知总体方差
│   ├── 📐 t = (x̄-μ₀)/(s/√n) — 未知总体方差
│   ├── p-value: H₀ 下观察到当前统计量的概率
│   └── ⚠️ p-value 不是 H₀ 为真的概率
│
├── ⭐ 错误结构 (Error Architecture)
│   ├── Type I Error (α): 拒绝真实 H₀
│   ├── Type II Error (β): 未能拒绝错误 H₀
│   ├── 📐 Power = 1 - β: 正确拒绝错误 H₀ 的概率
│   ├── n↑ → Power↑; α↑ → Power↑; Effect Size↑ → Power↑
│   └── ⚠️ 不能说"接受 H₀" — 只能说"不能拒绝 H₀"
│
├── ⭐ 参数 vs 非参数检验
│   ├── 参数检验: 依赖分布假设（正态），效率更高
│   └── 非参数检验: 少做或不做分布假设（序数数据、小样本）
│
├── ⭐ 双样本均值检验 (Two-Sample Mean Tests)
│   ├── Pooled t-test (方差相等)
│   │   ├── 📐 sₚ² = [(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)
│   │   ├── 📐 t = (x̄₁-x̄₂-d₀) / [sₚ√(1/n₁+1/n₂)], df=n₁+n₂-2
│   │   └── 🎯 适用：两总体正态、方差相等但未知
│   ├── Unequal Variance t-test (Welch, 方差不等)
│   │   ├── 📐 t = [(x̄₁-x̄₂)-d₀] / √(s₁²/n₁+s₂²/n₂)
│   │   └── 🎯 df 经 Satterthwaite 调整，介于 min(n₁-1,n₂-1) 和 n₁+n₂-2 之间
│   ├── Paired Comparisons t-test (配对样本)
│   │   ├── 📐 t = d̄ / (s_d/√n), df = n-1
│   │   └── 💡 本质：对配对差值 dᵢ = X₁ᵢ-X₂ᵢ 做单样本 t 检验
│   └── ⚠️ 配对检验 df = n-1（n=配对个数），不是 n₁+n₂-2
│
├── ⭐ 双样本方差与比例检验
│   ├── F-test (方差齐性检验)
│   │   ├── 📐 F = s₁²/s₂², df₁=n₁-1, df₂=n₂-1
│   │   ├── H₀: σ₁²=σ₂²; 通常将较大 s² 放分子
│   │   └── ⚠️ F 分布右偏、非负，对正态假设非常敏感
│   └── 双样本比例 z-test
│       ├── 📐 z = (p̂₁-p̂₂-d₀) / √[p̂(1-p̂)(1/n₁+1/n₂)]
│       ├── p̂ = (x₁+x₂)/(n₁+n₂) 为合并比例
│       └── 🎯 大样本近似正态
│
├── ⭐ 单样本方差检验 (Chi-Square Test)
│   ├── 📐 χ² = (n-1)s²/σ₀², df = n-1
│   ├── H₀: σ²=σ₀² (单总体方差等于某值)
│   ├── 卡方分布右偏、非负、df↑→趋近正态
│   ├── 🎯 拒绝域：右尾 χ²>χ²_α; 左尾 χ²<χ²_(1-α); 双边取两个临界值
│   └── ⚠️ 对正态性假设极其敏感，偏离正态时结果不可靠
│
├── ⭐ 双样本检验方法总结表
│   ├── Pooled t-test: μ₁-μ₂, t 分布, df=n₁+n₂-2, 方差相等
│   ├── Welch t-test: μ₁-μ₂, 近似 t, df 调整, 方差不等
│   ├── Paired t-test: μ_d, t(n-1), 配对样本
│   ├── F-test: σ₁²/σ₂², F(n₁-1,n₂-1), 正态假设
│   └── Proportion z-test: p₁-p₂, z, 大样本
│
├── 💡 关键洞察
│   ├── 假设检验五步法: H₀/H₁ → 检验统计量 → 拒绝域 → 计算 → 结论
│   ├── 置信区间与假设检验等价: μ₀ 在 CI 外 = 拒绝 H₀
│   ├── Type I 和 Type II 是 trade-off: 减小 α → β↑ → Power↓
│   ├── 增大样本量可同时降低 α 和 β（改善 Power）
│   ├── p-value 越小，反对 H₀ 的证据越强
│   ├── "assume equal variances" → Pooled; 未提及 → Welch (Unequal Variance)
│   └── 配对检验比独立样本检验力更高（消除个体间差异）
│
└── ⚠️ 考试陷阱总结
    ├── "不能拒绝" ≠ "接受" H₀ — 不拒绝只是证据不足
    ├── p-value 不是 H₀ 为真的概率
    ├── 单边/双边在假设阶段决定，不可事后优化
    ├── z vs t: σ 已知用 z，σ 未知用 t
    ├── 配对检验 df = n-1（n=配对个数），不是 n₁+n₂-2
    ├── F 检验和 χ² 检验对正态假设极其敏感
    └── 双样本比例检验用 z 分布（大样本近似正态）
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `z = (x̄-μ₀)/(σ/√n)` | z 检验统计量 | 总体方差已知的均值检验 | σ 必须已知 |
| `t = (x̄-μ₀)/(s/√n)` | t 检验统计量 | 总体方差未知的均值检验 | df = n-1 |
| `CI: x̄ ± z_(α/2) × σ/√n` | 置信区间（σ 已知） | 总体参数区间估计 | z 临界值查表 |
| `CI: x̄ ± t_(α/2,n-1) × s/√n` | 置信区间（σ 未知） | 参数估计常用方法 | df = n-1 |
| `sₚ² = [(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)` | 合并方差估计量 | 方差相等的双样本 t 检验 | df = n₁+n₂-2 |
| `t = (x̄₁-x̄₂-d₀)/(sₚ√(1/n₁+1/n₂))` | 双样本 t 检验（方差相等） | 比较两独立总体均值 | 确认方差相等条件 |
| `t = [(x̄₁-x̄₂)-d₀]/√(s₁²/n₁+s₂²/n₂)` | 双样本 t 检验（方差不等） | 方差不等的均值比较 | df 需 Satterthwaite 调整 |
| `t = d̄/(s_d/√n)` | 配对 t 检验 | 配对/相关样本均值比较 | df = n-1（n=配对个数） |
| `F = s₁²/s₂²` | F 检验统计量 | 两总体方差是否相等 | 对正态假设敏感 |
| `z = (p̂₁-p̂₂)/√[p̂(1-p̂)(1/n₁+1/n₂)]` | 双样本比例检验 | 两总体比例比较 | 大样本下近似正态 |
| `χ² = (n-1)s²/σ₀²` | 卡方检验统计量 | 单总体方差检验 | df = n-1，对正态敏感 |

### 🛠️ 常见考点与解题思路

**考点1：构建假设检验（五步法）**
- 步骤 1：写 H₀ 和 H₁（判断单边还是双边）
  - 双边: H₀: μ=μ₀ vs H₁: μ≠μ₀
  - 右尾: H₀: μ≤μ₀ vs H₁: μ>μ₀
  - 左尾: H₀: μ≥μ₀ vs H₁: μ<μ₀
- 步骤 2：选择检验统计量（总体 σ 已知 → z；未知 → t）
- 步骤 3：确定拒绝域（查临界值 — z_crit 或 t_crit, df=n-1）
- 步骤 4：计算检验统计量值
- 步骤 5：比较统计量与临界值 → reject (若在拒绝域) / fail to reject H₀
- ⚠️ 单边/双边在步骤 1 决定，不可在看到数据后"优化选择"

**考点2：p-value 解读**
- p-value 是在 H₀ 成立的条件下，观察到当前样本结果的概率
- p-value ≤ α → 拒绝 H₀
- p-value 越小，反对 H₀ 的证据越强
- ⚠️ 不能把 p-value 理解为"H₀ 为真的概率"

**考点3：置信区间与假设检验的关系**
- μ₀ 落在 (1-α)% 置信区间外 → 在 α 水平上拒绝 H₀
- CI: x̄ ± z_(α/2) × σ/√n (σ 已知) 或 x̄ ± t_(α/2,n-1) × s/√n (σ 未知)
- 两者等价 — 置信区间是假设检验的图形化方式
- ⚠️ 置信区间和假设检验使用相同的临界值

**考点4：Type I / Type II Error 权衡**
- Type I Error (α): 拒绝真实 H₀ — 由显著性水平控制
- Type II Error (β): 未能拒绝错误 H₀ — 取决于效应量和样本量
- Power = 1-β: 正确拒绝错误 H₀ 的概率
- n↑ → SE↓ → Power↑; α↑ → 拒绝域变宽 → Power↑ (但 α 也↑)
- Effect Size↑ → 真实差异更易检测 → Power↑
- 💡 增大样本量是同时降低 α 和 β 的唯一方法

**考点5：双样本均值检验方法选择**
- 判断顺序：
  1. 样本是否独立？ → 否 → Paired t-test (配对检验)
  2. 方差是否相等？ → 是 → Pooled t-test (合并方差)
  3. 方差不相等 → Unequal Variance t-test (Welch)
- ⚠️ 判断依据："assume equal variances" → Pooled；未提及或不相等 → Welch

**考点6：Pooled t-test (合并方差双样本 t 检验)**
- 步骤 1：计算 sₚ² = [(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)
- 步骤 2：计算 t = (x̄₁-x̄₂-d₀) / [sₚ√(1/n₁+1/n₂)]
- 步骤 3：查 t 临界值，df = n₁+n₂-2
- 步骤 4：比较并做结论
- ⚠️ 前提条件：两总体方差相等

**考点7：Paired Comparisons t-test (配对比较检验)**
- 步骤 1：计算每对差值 dᵢ = X₁ᵢ - X₂ᵢ
- 步骤 2：计算差值的均值 d̄ 和标准差 s_d
- 步骤 3：计算 t = d̄ / (s_d/√n)，df = n-1 (n=配对个数)
- 步骤 4：与 t 临界值比较
- ⚠️ df = n-1，不是 n₁+n₂-2 (高频陷阱！)
- 💡 配对检验消除个体间差异 → 检验力高于独立样本检验

**考点8：F-test (双样本方差齐性检验)**
- H₀: σ₁² = σ₂²；H₁: σ₁² ≠ σ₂² (双边) 或 σ₁² > σ₂² (单边)
- F = s₁²/s₂² (通常较大的 s² 放分子)
- df₁ = n₁-1 (分子), df₂ = n₂-1 (分母)
- F 分布右偏、非负，临界值查 F 分布表
- ⚠️ F 检验对正态假设极其敏感

**考点9：卡方单样本方差检验**
- H₀: σ² = σ₀²；H₁: 取决于问题 (σ²≠σ₀²/σ²>σ₀²/σ²<σ₀²)
- χ² = (n-1)s²/σ₀², df = n-1
- 右尾检验: χ² > χ²_α；左尾: χ² < χ²_(1-α)；双边: 两个临界值
- ⚠️ 对正态假设极其敏感
- 💡 不同于 F 检验 (F 检验比较两个方差)

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 假设检验中"接受 H₀" | "不能拒绝 H₀" — 证据不足以拒绝，不代表 H₀ 为真 | 统计检验只能反驳，不能证实 |
| p-value = H₀ 为真的概率 | p-value = 在 H₀ 下观测到当前样本的极端概率 | p-value 是条件概率，不是 H₀ 的后验概率 |
| z-test 和 t-test 可任意选择 | σ 已知 → z-test；σ 未知 → t-test | t 分布比 z 分布有更厚的尾部（小样本补偿） |
| 配对检验 df = n₁+n₂-2 | 配对检验 df = n-1 (n=配对个数) | 本质是单样本 t 检验在差值上 |
| 单边/双边可事后选择 | 必须在假设阶段决定 | 数据驱动选择会 inflate Type I error |
| 大 n 时 t ≈ z 所以用 z | 即使 n 很大，σ 未知仍用 t | t 分布在大 n 时趋近正态，但理论正确性重要 |

### 🔄 跨模块关联

- **[[M07-Estimation-and-Inference]]** — 标准误 SE = σ/√n 是假设检验的基础构件。CLT 为 z-test 和 t-test 的正态近似提供理论依据。
- **[[M09-Parametric-and-Non-Parametric-Tests-of-Independence]]** — 回归系数的 t 检验和整体 F 检验是假设检验框架的直接推广。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 检验统计量的分布依赖于样本统计量的性质。
- **[[M04-Probability-Trees-and-Conditional-Expectations]]** — p-value 本质上是概率分布尾部概率的应用。
- **[[M10-Simple-Linear-Regression]]** — 回归斜率的 t 检验是假设检验在回归中的具体应用。

### 📋 复习与刷题提示

- **核心能力**：掌握假设检验五步法，熟练区分 z/t/F/χ² 四种检验的适用场景
- **必考题型**：单样本 z/t 检验、双样本检验方法选择、Type I/II Error 辨析、p-value 解读
- **最常犯错误**："接受 H₀" 的表述、p-value 误解、配对检验自由度记错、z vs t 选择错误
- 记忆口诀：
  - 五步法：假设 → 统计量 → 拒绝域 → 计算 → 结论
  - z vs t：σ 已知用 z，σ 未知用 t
  - 配对做差：差值 dᵢ = X₁ᵢ - X₂ᵢ，对 d̄ 做 t 检验
  - Pooled vs Unequal: 方差相等用 pooled，不等用 Welch
- 刷题建议：重点多做假设检验全流程题（五步法）和双样本检验方法选择题
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
