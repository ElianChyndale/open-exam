---
title: "M03 — Statistical Measures of Asset Returns"
description: "CFA Level I 2026 official module: Statistical Measures of Asset Returns"
module: M03
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 3: Statistical Measures of Asset Returns"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M03: Statistical Measures of Asset Returns

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Statistical Measures of Asset Returns
- 3.01 | Introduction
- 3.02 | Measures of Central Tendency and Location
- 3.03 | Measures of Dispersion
- 3.04 | Measures of Shape of a Distribution
- 3.05 | Correlation between Two Variables

## Learning Outcome Statements

The candidate should be able to:

- calculate, interpret, and evaluate measures of central tendency and location to address an investment problem
- calculate, interpret, and evaluate measures of dispersion to address an investment problem
- interpret and evaluate measures of skewness and kurtosis to address an investment problem
- interpret correlation between two variables to address an investment problem

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M03: Statistical Measures of Asset Returns（统计量与分布特征）
│
├── ⭐ 集中趋势与位置指标 (Central Tendency & Location)
│   ├── 算术平均: Σxᵢ/N — 最常用，但对极端值敏感
│   ├── 几何平均: [Π(1+Rᵢ)]^(1/n)-1 — 收益率平均专用，≤ 算术平均
│   ├── 调和平均: n/Σ(1/xᵢ) — 平均价格倍数专用，≤ 几何平均
│   ├── 中位数: 排序后的中间值 — 抵抗极端值
│   ├── 📐 分位数位置: L_p = (n+1) × p/100
│   └── ⚠️ Outlier 对算术平均影响远大于中位数
│
├── ⭐ 离散程度 (Dispersion)
│   ├── 极差 = Max - Min — 最简单，但完全依赖极端值
│   ├── 📐 MAD = Σ|xᵢ - x̄| / n — 不易受极端值影响
│   ├── 📐 总体方差 σ² = Σ(xᵢ-μ)²/N — 已知总体
│   ├── 📐 样本方差 s² = Σ(xᵢ-x̄)²/(n-1) — 无偏估计
│   ├── 📐 CV = s / x̄ — 比较不同尺度离散度
│   └── ⚠️ 样本方差用 n-1（常见陷阱）；样本标准差有偏
│
├── ⭐ 分布形态 (Distribution Shape)
│   ├── 偏度 (Skewness)：衡量不对称程度
│   │   ├── 📐 Skewness = E[(X-μ)³]/σ³
│   │   ├── 右偏/正偏: 长尾在右，均值>中位数>众数
│   │   └── 左偏/负偏: 长尾在左，均值<中位数<众数
│   ├── 峰度 (Kurtosis)：衡量尾部厚度
│   │   ├── 📐 超额峰度 = 峰度 - 3
│   │   ├── Leptokurtic: 峰度>3, 厚尾, 更多极端值
│   │   └── Platykurtic: 峰度<3, 薄尾
│   └── ⚠️ 左偏/右偏看长尾方向；峰度看尾部不看尖峰
│
├── ⭐ 相关性直觉 (Correlation Intuition)
│   ├── 相关系数范围 [-1, +1]
│   ├── 符号=方向，大小=线性关联强度
│   └── ⚠️ 相关 ≠ 因果
│
├── 💡 关键洞察
│   ├── 三种均值关系: 调和 ≤ 几何 ≤ 算术，差距=波动率
│   ├── 样本方差用 n-1 是因为在估计总体方差时损失一个自由度
│   ├── 偏度符号判断: 看长尾方向，不是数据集中方向
│   └── 峰度只衡量尾部厚度，不受分布尖峰影响
│
└── ⚠️ 考试陷阱总结
    ├── 样本方差用 n-1，不是 n
    ├── 左偏不代表负值多 — 大部分数据可能仍在正值区间
    ├── 峰度看尾部不看尖峰
    ├── CV 的前提是均值不为零
    └── 偏度图先看坐标轴含义（x=变量值，y=频率）
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `μ = Σxᵢ/N` | 总体均值 | 已知总体的数据平均 | N = 总体规模 |
| `x̄ = Σxᵢ/n` | 样本均值 | 样本数据平均 | n = 样本容量 |
| `σ² = Σ(xᵢ-μ)²/N` | 总体方差 | 已知总体离散度 | 分母为 N |
| `s² = Σ(xᵢ-x̄)²/(n-1)` | 样本方差 | 样本估计总体方差 | 分母是 n-1！ |
| `MAD = Σ|xᵢ-x̄|/n` | 平均绝对偏差 | 不易受极端值影响 | 绝对值，不是平方 |
| `CV = s/x̄` | 变异系数 | 比较不同尺度离散度 | 均值不能接近 0 |
| `Skewness = E[(X-μ)³]/σ³` | 偏度 | 判断不对称方向 | 正=右偏，负=左偏 |
| `超额峰度 = 峰度 - 3` | 超额峰度 | 判断尾部厚度 | >0=厚尾，<0=薄尾 |
| `L_p = (n+1)×p/100` | 分位数位置 | 计算第 p 百分位数 | 位置可能是非整数 |

### 🛠️ 常见考点与解题思路

**考点1：均值与中位数的选择**
- 分布对称 → Mean = Median — 两者皆可
- 右偏 → Mean > Median — 少数极大值拉高均值
- 左偏 → Mean < Median — 少数极小值拉低均值
- 题目问"typical value"且数据偏斜 → 选中位数
- ⚠️ 偏度方向判断：看长尾方向，不是看数据集中在哪边

**考点2：Chebyshev's Inequality**
- 任何分布中，至少 1 - 1/k² 的数据在均值 k 个标准差内
- k=2：至少 75%；k=3：至少 89%
- 用于未知分布形状时的保守估计

**考点3：标准差 vs 半标准差**
- 标准差衡量总波动（双侧）
- 半标准差只衡量下行波动（单侧）
- 风险厌恶投资者更关注下行偏差

**考点4：样本方差计算与区分**
- 看到 "sample" → 用 n-1
- 看到 "population" → 用 N
- 题目给样本数据要求算方差 → 无论题目是否明确说明"sample"，只要是从总体中抽取的数据就用 n-1

**考点5：偏度和峰度的解读**
- 偏度：正 = 右尾长，负 = 左尾长
- 峰度 > 3 = 厚尾(Leptokurtic)，极端值概率大于正态分布
- 尖峰 ≠ 高峰度 — 高峰度是厚尾的体现

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 样本方差用 n 做分母 | 样本方差用 n-1 做分母（无偏估计） | 损失一个自由度估计均值，修正偏差 |
| 左偏分布 = 负值多 | 左偏指左侧长尾，大部分数据可能仍在正值区间 | 长尾方向决定偏度符号，不是数据集中位置 |
| 高峰度 = 尖峰分布 | 高峰度 = 厚尾 + 更多极端值 | 峰度衡量尾部厚度，不是尖峰程度 |
| 右偏时中位数 > 均值 | 右偏时均值 > 中位数 | 少数极大值将均值拉向右尾 |
| 相关系数大 = 因果关系 | 相关 ≠ 因果 | 可能存在遗漏变量或反向因果 |

### 🔄 跨模块关联

- **[[M01-Rates-and-Returns]]** — 三种均值（算术/几何/调和）在 M01 收益率度量中首次出现。
- **[[M04-Probability-Trees-and-Conditional-Expectations]]** — 统计量的概率版本：期望值是概率加权均值，方差是概率加权方差。
- **[[M05-Portfolio-Mathematics]]** — 组合方差公式是 M03 方差概念的延伸 — 从单变量到双变量。
- **[[M09-Parametric-and-Non-Parametric-Tests-of-Independence]]** — 相关系数在此引入直觉，在 M09 中扩展到正式统计检验。
- **[[M07-Estimation-and-Inference]]** — 样本方差的自由度概念在标准误和 CLT 中继续使用。

### 📋 复习与刷题提示

- **核心能力**：准确区分总体 vs 样本统计量公式，理解偏度/峰度的含义
- **必考题型**：样本方差计算、均值选择（算术/几何/调和）、偏度方向判断、CV 计算
- **最常犯错误**：样本方差忘记 n-1、偏度/峰度概念混淆、峰度误判为"尖峰"
- 记忆口诀：
  - 样本方差 n-1：减一是因为估计了一个参数（均值）
  - 三种均值：调和 ≤ 几何 ≤ 算术
  - 偏度判断：长尾在哪边，偏度就朝哪边
  - 峰度看尾不是看尖
- 刷题建议：多做样本 vs 总体区分题、偏度峰度概念题
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
