---
title: "M04 — Probability Trees and Conditional Expectations"
description: "CFA Level I 2026 official module: Probability Trees and Conditional Expectations"
module: M04
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 4: Probability Trees and Conditional Expectations"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M04: Probability Trees and Conditional Expectations

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Probability Trees and Conditional Expectations
- 4.01 | Introduction
- 4.02 | Expected Value and Variance
- 4.03 | Probability Trees and Conditional Expectations
- 4.04 | Bayes' Formula and Updating Probability Estimates

## Learning Outcome Statements

The candidate should be able to:

- calculate expected values, variances, and standard deviations and demonstrate their application to investment problems
- formulate an investment problem as a probability tree and explain the use of conditional expectations in investment application
- calculate and interpret an updated probability in an investment setting using Bayes’ formula

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M04: Probability Trees and Conditional Expectations（概率基础与条件期望）
│
├── ⭐ 期望值 / 方差 / 标准差 (Expected Value / Variance / SD)
│   ├── 📐 E(X) = Σ p(xᵢ) × xᵢ — 概率加权平均，不是最可能结果
│   ├── 📐 Var(X) = Σ p(xᵢ)[xᵢ-E(X)]²（定义式）
│   ├── 📐 Var(X) = E(X²) - [E(X)]²（计算式 — 更快）
│   └── ⚠️ E(X²) ≠ [E(X)]²，两者之差 = 方差
│
├── ⭐ 概率树 (Probability Tree)
│   ├── 从根节点出发，每个分支 = 一种可能路径
│   ├── 分支概率 = 路径上各节点概率的乘积
│   ├── 终端收益 = 走完整条路径的最终结果
│   └── 🎯 递归求期望 (Recursive Expectation)：从叶节点往回推
│
├── ⭐ 条件概率 (Conditional Probability)
│   ├── 📐 P(A|B) = P(A∩B) / P(B) — 在 B 范围内看 A 的比例
│   ├── 📐 P(A∩B) = P(A|B) × P(B) — 联合概率
│   └── ⚠️ 条件概率分母永远是 P(B)，不是 P(A)
│
├── ⭐ 全概率公式 (Total Probability Rule)
│   ├── 📐 P(A) = Σ P(A|Bᵢ) × P(Bᵢ)
│   └── 🎯 将复杂事件拆解为条件路径的概率加权和
│
├── ⭐ 贝叶斯更新 (Bayes' Formula)
│   ├── 先验概率 → 新证据 → 后验概率
│   ├── 📐 P(Bⱼ|A) = P(A|Bⱼ)P(Bⱼ) / ΣP(A|Bᵢ)P(Bᵢ)
│   └── ⚠️ 分母 = P(A) = 全概率，不是分子单独
│
├── 💡 关键洞察
│   ├── 期望值不是"最可能的结果"，而是概率加权平均水平
│   ├── 概率树本质是递归条件期望的可视化
│   ├── 贝叶斯公式 = 先验×似然/全概率 — 直觉比公式重要
│   └── 所有后验概率之和必须为 1（验证计算正确性）
│
└── ⚠️ 考试陷阱总结
    ├── 条件概率分母永远是 P(B)
    ├── 贝叶斯分母 = 全概率，不能漏
    ├── E(X²) ≠ [E(X)]² — 混淆会导致方差错误
    ├── 后验概率之和必须为 1（验证方法）
    └── 联合概率 = 条件概率 × 边际概率
```

## 📖 知识点详解

### 知识点1：期望值/方差/标准差（Expected Value / Variance / Standard Deviation）
**核心概念**：期望值是在概率分布下的加权平均，反映随机变量的长期平均水平。方差衡量离散度。
- **期望值**：E(X) = Σ p(xᵢ) × xᵢ，概率加权平均，不是最可能的结果
- **方差（定义式）**：Var(X) = Σ p(xᵢ)[xᵢ - E(X)]²
- **方差（计算式）**：Var(X) = E(X²) - [E(X)]²，计算式通常更快
- 离散概率要求每个结果概率在 [0,1] 之间，所有概率之和为 1
- ⚠️ E(X²) ≠ [E(X)]²，两者之差就是方差

**考试应用**：根据概率分布表计算期望值和方差，考试常以情景分析形式出现。

### 知识点2：概率树（Probability Tree）
**核心概念**：概率树用于分解复杂概率问题，通过图示化的分支结构清晰地展示各条概率路径及其终端结果。
- **分支概率**：沿着概率树某一支路走到底的概率，各分支概率乘积
- **终端收益**：走完整条概率路径的最终结果
- **递归求期望（Recursive Expectation）**：从叶节点往回推，在每个决策节点计算期望值用于决策
- 概率树的核心思路是从叶节点往回推，在每个决策节点处计算期望值

**考试应用**：用概率树分解多阶段决策问题，计算条件期望并选择最优路径。

### 知识点3：条件概率与全概率（Conditional Probability and Total Probability Rule）
**核心概念**：条件概率是在给定条件下事件发生的概率。全概率公式将复杂事件拆解为条件路径的概率加权和。
- **条件概率**：P(A|B) = P(A∩B)/P(B)，在 B 的范围内看 A 的比例
- **联合概率**：P(A∩B) = P(A|B) × P(B)，不要混淆联合概率与条件概率
- **全概率公式**：P(A) = Σ P(A|Bᵢ) × P(Bᵢ)，将复杂事件拆解为条件路径的概率加权和
- ⚠️ 条件概率分母永远是 P(B)，不是 P(A)

**考试应用**：给定 2×2 列联表计算条件概率，利用全概率公式计算复杂事件概率。

### 知识点4：贝叶斯更新（Bayes' Formula）
**核心概念**：贝叶斯公式的核心思想是用新信息更新旧概率。先验概率结合新证据的似然得到后验概率。
- **先验概率**：在获知新信息前对事件的初始判断
- **条件似然**：新信息在事件发生条件下的概率
- **贝叶斯公式**：P(Bⱼ|A) = P(A|Bⱼ)P(Bⱼ) / ΣP(A|Bᵢ)P(Bᵢ)
- 分母 = P(A) = 全概率，不是分子单独
- ⚠️ 常见错误：算了分子就忘了除以 P(A)。所有后验概率之和必须为 1

**考试应用**：代入贝叶斯公式计算后验概率，考试常给出先验概率和条件似然，要求计算更新后的概率。

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `E(X) = Σ p(xᵢ)xᵢ` | 期望值 | 概率加权平均结果 | 不是"最可能的结果" |
| `Var(X) = Σ p(xᵢ)[xᵢ-E(X)]²` | 方差定义式 | 概率加权离散度 | 直接代入定义 |
| `Var(X) = E(X²) - [E(X)]²` | 方差计算式 | 快速计算方差 | E(X²) ≠ [E(X)]² |
| `P(A\|B) = P(A∩B)/P(B)` | 条件概率 | 给定 B 下 A 的概率 | 分母是 P(B) |
| `P(A) = Σ P(A\|Bᵢ)P(Bᵢ)` | 全概率公式 | 拆解复杂事件 | 各分支互斥完备 |
| `P(Bⱼ\|A) = P(A\|Bⱼ)P(Bⱼ)/P(A)` | 贝叶斯公式 | 新信息更新概率 | 分母是 P(A) = 全概率 |

### 🛠️ 常见考点与解题思路

**考点1：计算期望值和方差（基础必考）**
- 步骤 1：确认概率分布表（各情景概率和对应收益率/结果）
- 步骤 2：E(R) = Σ pᵢ × Rᵢ — 情景概率加权的平均结果
- 步骤 3：方差可选用两种方法：
  - 定义式: Var(R) = Σ pᵢ × [Rᵢ - E(R)]² (更保险)
  - 计算式: Var(R) = E(R²) - [E(R)]² (更快)
- 步骤 4：SD = √Var(R) — 和原始数据单位一致
- ⚠️ E(X²) ≠ [E(X)]²，两者之差就是方差
- ⚠️ 期望值是概率加权平均，不是"最可能的结果"

**考点2：条件概率计算（列联表法）**
- 给定 2×2 列联表 (Contingency Table):
  - 行合计、列合计、总样本量
  - P(A|B) = P(A∩B) / P(B) — 分母是条件事件 B 的概率
  - P(A∩B) = P(A|B) × P(B) — 联合概率公式
- ⚠️ 不要将 P(A|B) 和 P(B|A) 混淆 — 分母不同
- ⚠️ 条件概率分母永远是 P(B)，不是 P(A) 也不是 P(A∩B)
- 💡 联合概率 = 条件概率 × 边际概率

**考点3：贝叶斯更新（必考）**
- 三步法：
  - 步骤 1：确定先验概率 P(Bⱼ) — 新信息前的初始判断
  - 步骤 2：确定条件似然 P(A|Bⱼ) — 新信息在各状态下的出现概率
  - 步骤 3：计算全概率 P(A) = Σ P(A|Bᵢ)P(Bᵢ) — 新信息的总概率
  - 步骤 4：代入贝叶斯公式求后验: P(Bⱼ|A) = [P(A|Bⱼ)P(Bⱼ)] / P(A)
  - 步骤 5：验证后验概率之和为 1
- 💡 贝叶斯 = 先验 × 似然 / 全概率 — 直觉比公式重要
- ⚠️ 最大错误：分子除以 P(A|Bⱼ) 而不是除以 P(A) (全概率)
- ⚠️ 算完后验概率立即验证是否和为 1

**考点4：概率树构建与决策**
- 构建概率树：
  - 根节点 → 分支（如好经济/差经济）
  - 每个分支再分叉（如好结果/差结果）
  - 终端节点 = 路径概率 × 最终收益
- 决策步骤：
  - 从叶节点往回推算各分支的条件期望值
  - 在每个决策节点选择期望值最高的分支
  - 递归求期望 (Recursive Expectation)
- 💡 概率树是复杂概率问题的可视化分解工具
- ⚠️ 路径概率 = 分支上各节点概率的乘积

**考点5：全概率公式应用**
- P(A) = Σ P(A|Bᵢ) × P(Bᵢ)
- 将复杂事件 A 的概率拆解为各条件路径的概率加权和
- 常见于贝叶斯更新和信用风险分析
- ⚠️ 各条件事件 Bᵢ 必须互斥且完备（之和为 1）

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 条件概率 P(A|B) 的分母是 P(A∩B) 或 P(A) | 分母永远是 P(B) | 条件概率是在 B 的范围内看 A 的比例 |
| 贝叶斯后验 = 分子不除分母 | 后验 = 分子 / 全概率 P(A) | 需要归一化到 [0,1] 区间 |
| E(X²) = [E(X)]² | E(X²) ≠ [E(X)]²，差值为方差 | 平方的期望 ≠ 期望的平方 |
| P(A∩B) = P(A)×P(B) 总是成立 | 仅当 A 与 B 独立时才成立 | 不独立时必须用 P(A|B)×P(B) |
| 期望值 = 最可能结果 | 期望值是概率加权平均，通常不等于众数 | 期望是长期平均概念 |

### 🔄 跨模块关联

- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 概率版本的统计量：期望值对应均值，方差概念延续。
- **[[M05-Portfolio-Mathematics]]** — 组合期望收益和协方差全部基于概率框架（联合概率函数）。
- **[[M02-Time-Value-of-Money-in-Finance]]** — 概率加权现金流的期望现值是风险中性定价的直觉基础。
- **[[M11-Introduction-to-Big-Data-Techniques]]** — 贝叶斯方法在 ML 中有广泛应用（朴素贝叶斯分类器）。

### 📋 复习与刷题提示

- **核心能力**：熟练运用方差两种公式互推，掌握贝叶斯更新四步法
- **必考题型**：期望值/方差计算、贝叶斯后验概率、条件概率、概率树决策
- **最常犯错误**：贝叶斯分母遗漏、E(X²) 和 [E(X)]² 混淆、条件概率分母搞错
- 记忆口诀：
  - 贝叶斯四步：先验 → 似然 → 全概率 → 后验
  - 方差公式二选一：算 E(X²) 减 [E(X)]² 最快
  - 概率之和为 1：算完后验立即验证
- 刷题建议：贝叶斯题目和条件概率是 CFA 一级 Quant 高频题
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
