---
title: "M09 — Parametric and Non-Parametric Tests of Independence"
description: "CFA Level I 2026 official module: Parametric and Non-Parametric Tests of Independence"
module: M09
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 9: Parametric and Non-Parametric Tests of Independence"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M09: Parametric and Non-Parametric Tests of Independence

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Parametric and Non-Parametric Tests of Independence
- 9.01 | Introduction
- 9.02 | Tests Concerning Correlation
- 9.03 | Tests of Independence Using Contingency Table Data

## Learning Outcome Statements

The candidate should be able to:

- explain parametric and nonparametric tests of the hypothesis that the population correlation coefficient equals zero, and determine whether the hypothesis is rejected at a given level of significance
- explain tests of independence based on contingency table data

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M09: Parametric and Non-Parametric Tests of Independence（独立性检验）
│
├── ⭐ 相关系数 t 检验 — Pearson 参数检验
│   ├── 📐 t = r × √[(n-2)/(1-r²)]
│   ├── H₀: ρ = 0（无线性关系）；H₁: ρ ≠ 0（存在线性关系）
│   ├── df = n-2
│   ├── 假设：双变量正态分布 (Bivariate Normal)
│   └── 🔗 与回归斜率系数的 t 检验完全等价
│
├── ⭐ Spearman 秩相关系数检验 — 非参数检验
│   ├── 基于排序 (Rank) 而非原始数值
│   ├── 无分布假设
│   ├── 🎯 适用：数据不满足正态、有 outlier、有序数据
│   └── ⚠️ Spearman 检测单调关系，不一定是线性
│
├── ⭐ Pearson vs Spearman 对比
│   ├── Pearson: 连续变量、双变量正态、线性关系、对 outlier 敏感
│   └── Spearman: 有序/连续变量、无分布假设、单调关系、对 outlier 不敏感
│
├── ⭐ 列联表卡方独立性检验 (Chi-Square Test of Independence)
│   ├── H₀: 两分类变量独立；H₁: 两变量不独立
│   ├── 📐 χ² = Σ[(O-E)²/E]
│   ├── 📐 期望频数 E = (行合计 × 列合计) / n
│   ├── 📐 df = (r-1)(c-1)
│   ├── 卡方检验是右尾检验
│   └── ⚠️ 所有期望频数 ≥ 5（否则卡方近似不可靠）
│
├── 💡 关键洞察
│   ├── 相关性 t 检验与回归斜率 t 检验等价 — 两个视角一个检验
│   ├── Spearman 是 Pearson 的非参数版本 — 适用不同数据条件
│   ├── 卡方独立性检验只判断"是否关联"，不说明关联方向和强度
│   ├── 相关 ≠ 因果 — 显著相关不代表因果关系
│   └── 卡方检验用期望频数（独立假设下），不是观测频数
│
└── ⚠️ 考试陷阱总结
    ├── 相关系数 t 检验 df = n-2，不是 n-1
    ├── 卡方检验是右尾检验
    ├── 期望频数基于独立假设计算，不要用观测频数
    ├── 期望频数 ≥ 5 是卡方检验的适用条件
    └── Spearman 检测单调关系，Pearson 检测线性关系
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `t = r√[(n-2)/(1-r²)]` | 相关系数 t 检验 | 检验 ρ = 0 | df = n-2 |
| `χ² = Σ[(O-E)²/E]` | 卡方检验统计量 | 列联表独立性检验 | 右尾检验 |
| `E = (行合计×列合计)/n` | 期望频数 | 列联表期望值 | 基于独立假设计算 |
| `df = (r-1)(c-1)` | 卡方检验自由度 | 列联表自由度 | r=行数，c=列数 |
| `df = n-2` | 相关系数 t 检验 df | Pearson 检验 | 不是 n-1 |

### 🛠️ 常见考点与解题思路

**考点1：相关系数 t 检验计算（高频）**
- 给定样本相关系数 r 和样本量 n，计算检验统计量:
  - t = r√[(n-2)/(1-r²)]
- H₀: ρ = 0 (总体相关系数为零，无线性关系)
- H₁: ρ ≠ 0 (总体相关系数不为零，存在线性关系)
- 与 t 临界值比较 (df = n-2，双尾检验)
- 若 |t| > t_crit → 拒绝 H₀ → 相关性显著
- ⚠️ df = n-2，不是 n-1 (最容易混淆的自由度陷阱)
- 🔗 等价于回归中斜率系数的 t 检验 (完全相同的 t 统计量)

**考点2：参数 vs 非参数检验选择标准**
- 选择 Pearson (参数检验) 的条件:
  - 数据为连续变量 (区间/比率尺度)
  - 服从双变量正态分布 (Bivariate Normal)
  - 无显著异常值
  - 关注线性关系
- 选择 Spearman (非参数检验) 的条件:
  - 数据不满足正态分布
  - 存在异常值
  - 数据为有序变量 (Ordinal)
  - 关注单调关系 (不一定是线性)
- ⚠️ Spearman 检测单调关系，Pearson 检测线性关系 — 这是核心区别

**考点3：列联表卡方检验全流程（必考）**
- 步骤 1：建立假设
  - H₀: 两个分类变量独立 (无关联)
  - H₁: 两个分类变量不独立 (存在关联)
- 步骤 2：计算期望频数
  - E = (行合计 × 列合计) / 总样本量 n
  - 每个单元格的 E 在"独立"假设下的理论频数
- 步骤 3：计算卡方统计量
  - χ² = Σ[(O-E)²/E]，对所有单元格求和
- 步骤 4：确定拒绝域
  - df = (r-1)(c-1)，其中 r=行数, c=列数
  - 卡方检验是右尾检验 (χ² 越大越拒绝 H₀)
- 步骤 5：比较并做结论
  - χ² > 临界值 → 拒绝 H₀ → 变量不独立
- ⚠️ 所有期望频数 ≥ 5 (否则卡方近似不可靠)
- ⚠️ 仅判断是否存在关联，不说明关联方向或强度

**考点4：Pearson vs Spearman 核心区别总结**
- Pearson:
  - 数据: 原始值
  - 假设: 双变量正态分布
  - 检测: 线性关系
  - 异常值: 敏感
  - 类型: 参数检验
- Spearman:
  - 数据: 秩 (Rank) / 排序
  - 假设: 无分布假设
  - 检测: 单调关系
  - 异常值: 不敏感
  - 类型: 非参数检验
- ⚠️ 考试常考: 给定场景选择正确方法

**考点5：卡方独立性检验的注意事项**
- 期望频数不能太小 (≥ 5 是经验规则)
- 检验结果仅说明有无关联，不说明关联强度或方向
- 如果是 2×2 表，可使用 Yates' correction (但 CFA 一级一般不要求)
- 相关 ≠ 因果 — χ² 显著不代表一个变量导致另一个
- ⚠️ 不要将期望频数与观测频数混淆 — 期望频数基于"独立"假设

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 相关系数 t 检验 df = n-1 | df = n-2 | 回归有两个参数（截距和斜率），损失两个自由度 |
| 卡方检验是双尾检验 | 卡方检验是右尾检验 | χ² 统计量总是非负，越远离 0 越拒绝 H₀ |
| 期望频数 = 观测频数 | 期望频数基于独立假设计算 | 期望频数是"如果独立"的理论值 |
| Spearman 检测线性关系 | Spearman 检测单调关系（不一定是线性） | 基于秩相关，检测秩的单调趋势 |
| 卡方检验说明关联方向 | 卡方检验只判断是否关联，不说明方向或强度 | 如需方向强度用 Cramér's V 等指标 |

### 🔄 跨模块关联

- **[[M08-Hypothesis-Testing]]** — 本模块是 M08 假设检验框架的直接应用。相关性 t 检验是参数检验的具体实例，Spearman 检验是非参数检验的应用。
- **[[M10-Simple-Linear-Regression]]** — 相关系数的 t 检验与简单线性回归中斜率系数的 t 检验完全等价。简单回归中 R² = r²。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 相关系数的概念在 M03 中引入，本模块将其扩展为正式统计检验。
- **[[M05-Portfolio-Mathematics]]** — 协方差和相关系数是投资组合数学的核心概念，本模块的检验方法可用于检验资产收益相关性是否显著。

### 📋 复习与刷题提示

- **核心能力**：区分 Pearson（参数、线性）和 Spearman（非参数、单调）的适用场景
- **公式记忆**：相关系数 t 统计量公式和列联表 χ² 公式必须能默写
- **易混点**：自由度注意是 n-2（相关系数检验）还是 (r-1)(c-1)（列联表检验）
- **最常犯错误**：自由度记错、卡方检验方向弄反、期望频数与观测频数混淆
- **跨科目接口**：检验方法与 Quant M08 假设检验框架、Equity 市场效率检验关联
- 记忆口诀：
  - Pearson 用原始值，Spearman 用秩
  - 卡方右尾检验：χ² 越大越拒绝
  - 期望频数 = 行合计 × 列合计 / n
  - 相关系数 df = n-2
- 刷题建议：重点做 Pearson/Spearman 场景判断题和列联表 χ² 计算题

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
