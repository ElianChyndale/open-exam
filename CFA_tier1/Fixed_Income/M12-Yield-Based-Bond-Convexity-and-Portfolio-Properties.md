---
title: "M12 — Yield-Based Bond Convexity and Portfolio Properties"
description: "CFA Level I 2026 official module: Yield-Based Bond Convexity and Portfolio Properties"
module: M12
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 12: Yield-Based Bond Convexity and Portfolio Properties"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M12: Yield-Based Bond Convexity and Portfolio Properties

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Yield-Based Bond Convexity and Portfolio Properties
- 12.01 | Introduction
- 12.02 | Bond Convexity and Convexity Adjustment
- 12.03 | Bond Risk and Return Using Duration and Convexity
- 12.04 | Portfolio Duration and Convexity

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret convexity and describe the convexity adjustment
- calculate the percentage price change of a bond for a specified change in yield, given the bond's duration and convexity
- calculate portfolio duration and convexity and explain the limitations of these measures

## 🌳 核心知识树

```text
🏆 M12: Yield-Based Bond Convexity and Portfolio Properties（凸性与组合属性）
├─ ⭐ 12.1 凸性 (Convexity)
│  ├─ 📐 Convexity = (P_- + P_+ - 2P_0) / (P_0 × (Δy)^2)
│  ├─ 📐 价格变化（含凸性）：%ΔP ≈ -D_mod × Δy + 0.5 × Convexity × (Δy)^2
│  ├─ 🎯 凸性校正久期遗漏的曲率（二阶效应）
│  ├─ 💡 正凸性：利率↓时价格涨幅 > 利率↑时价格跌幅 → 对投资者有利
│  ├─ 💡 负凸性：常见于可赎回债券和 MBS
│  └─ ⚠️ 凸性在 Δy 较小时 ≈ 0，久期就足够
│
├─ ⭐ 12.2 组合久期与凸性
│  ├─ 📐 D_p = Σ w_i × D_i（价值权重）
│  ├─ 📐 C_p = Σ w_i × C_i
│  ├─ ⚠️ 仅适用于平行收益率曲线移动
│  └─ ⚠️ 假设收益率微小变动
│
└─ ⭐ 12.3 凸性与债券特征关系
   ├─ 💡 票息越低 → 凸性越小（零息债凸性最小）
   ├─ 💡 期限越长 → 凸性越大
   ├─ 💡 收益率越低 → 凸性越大
   └─ 💡 正凸性有价值但非免费
```

## 📖 知识点详解

### 知识点1：凸性（Convexity）
**核心概念**：凸性衡量债券价格与收益率关系曲线的弯曲程度，是对久期线性近似的二阶修正。当收益率变动较大时，凸性校正至关重要。
- **计算公式**：`Convexity = (P_- + P_+ - 2P_0) / (P_0 × (Δy)^2)`，其中 P_- 为利率向下移 Δy 后的价格，P_+ 为利率向上移 Δy 后的价格
- **含凸性的价格变化公式**：`%ΔP ≈ -D_mod × Δy + 0.5 × Convexity × (Δy)^2`
- **正凸性**：利率下降时价格涨幅 > 利率上升时价格跌幅，对投资者有利。大多数无期权固定利率债券具有正凸性
- **负凸性**：常见于可赎回债券和 MBS。利率下降时价格上涨受限（被赎回价或提前还款封顶）
- ⚠️ 凸性在 Δy 很小时 ≈ 0，久期就足够。用于大幅变动估算时必须加入凸性项

**考试应用**：给定 D_mod、Convexity、Δy，计算含凸性的价格变化。注意 Δy 必须用小数形式。

### 知识点2：凸性与债券特征关系（Convexity Properties）
**核心概念**：凸性与债券特征之间存在确定的规律。理解这些关系有助于比较不同债券的凸性大小。
- **票息越低 → 凸性越小**：零息债券的凸性最小（但其久期最大）
- **期限越长 → 凸性越大**
- **收益率越低 → 凸性越大**
- **正凸性有价值但非免费获得**：市场不会免费提供正凸性，获得正凸性通常要付出代价（如放弃部分收益）
- **久期和凸性的权衡**：投资者需要在久期（利率敏感度）和凸性（曲率）之间进行权衡

**考试应用**：比较两只债券的凸性大小，判断给定债券的凸性正负。

### 知识点3：组合久期与凸性（Portfolio Duration and Convexity）
**核心概念**：组合久期和凸性通过各债券的市值权重加权平均计算，是组合层面利率风险管理的核心工具。
- **组合久期**：`D_p = Σ w_i × D_i`，其中 w_i 为债券 i 的市值占组合总市值的比例
- **组合凸性**：`C_p = Σ w_i × C_i`
- ⚠️ **重要局限性**：
  - 仅适用于收益率曲线平行移动
  - 仅对收益率微小变动有效
  - 对于 twist（扭曲）或 butterfly（蝶式）等非平行变动无效
  - 假设各债券收益率同步同幅变动

**考试应用**：计算组合久期和凸性（以市值加权），理解其局限性，特别是仅适用于平行移动。

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Convexity = (P_- + P_+ - 2P_0) / (P_0 × (Δy)^2)` | 凸性计算 | 计算凸性值 | Δy 用小数（如 0.01） |
| `%ΔP ≈ -D_mod × Δy + 0.5 × Convexity × (Δy)^2` | 价格变化（含凸性） | 精确估计 | Δy 较大时必须用 |
| `D_p = Σ w_i × D_i` | 组合久期 | 组合管理 | 仅平行移动有效 |
| `C_p = Σ w_i × C_i` | 组合凸性 | 组合管理 | 仅平行移动有效 |

## 🛠️ 常见考点与解题思路

### 考点 1：含凸性的价格变化估计
- **题型**：给定 D_mod、Convexity、Δy，计算 %ΔP
- **步骤**：
  1. 久期项：`-D_mod × Δy`
  2. 凸性项：`0.5 × Convexity × (Δy)^2`
  3. 总变化：久期项 + 凸性项
- **注意**：Δy 必须用小数形式（如 50bp = 0.005）

### 考点 2：判断凸性类型
- **正凸性**：大多数无期权固定利率债券
- **负凸性**：可赎回债券（利率↓时价格被 cap）、MBS（利率↓时提前还款↑）
- **考试常考**：给定债券特征判断凸性正负

### 考点 3：组合久期/凸性计算
- **步骤**：计算各债券权重（市值占比）→ 加权平均久期/凸性
- **局限性**：仅适用于小幅平行移动，对于 twist/butterfly 变动无效

### 考点 4：比较两只债券的凸性
- **思路**：期限越长凸性越大；票息越低凸性越小；收益率越低凸性越大

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| 所有债券凸性都为正 | 可赎回债券和 MBS 可能负凸性 | 现金流随利率变化 |
| 凸性总是重要 | Δy 很小时凸性项 ≈ 0 | 1bp 变动时久期就够 |
| 高凸性免费 | 正凸性需付出代价（低收益率） | 市场不会免费提供 |
| Δy = 1 表示 1% | Δy = 0.01 表示 1% | 小数 vs 百分数混淆 |

## 🔄 跨模块关联

- **修正久期** → [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] 前置知识
- **Macaulay 久期** → [[M10-Interest-Rate-Risk-and-Return]] 的久期基础
- **MBS 负凸性** → [[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]] 提前还款风险
- **有效凸性** → [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] 期权感知风险

## 📋 复习与刷题提示

- **核心重点**：含凸性的价格变化计算是最核心考点
- **凸性属性**：
  - 正凸性：大多数无期权固定利率债券（利率↓时价格↑更多）
  - 负凸性：可赎回债券和 MBS（利率↓时价格↑受限）
  - 零息债券凸性最小
  - 期限越长凸性越大
  - 收益率越低凸性越大
- **组合计算**：
  - D_p = Σ w_i × D_i
  - C_p = Σ w_i × C_i
  - 局限性：仅平行移动有效
- **何时需要凸性修正**：
  - Δy < 50bp：久期近似足够
  - Δy > 100bp：必须加入凸性项
  - Δy = 200bp 时凸性项可贡献 0.5% 以上的修正
- **典型计算流程**：
  1. 已知 D_mod = 7.28，Convexity = 65，Δy = +1%（上升100bp）
  2. 久期项：-7.28 × 0.01 = -7.28%
  3. 凸性项：0.5 × 65 × (0.01)^2 = 0.5 × 65 × 0.0001 = 0.325%
  4. 总变化：-7.28% + 0.325% = -6.955%
  5. 单独用久期：-7.28%（高估了跌幅）
- **刷题建议**：
  - 重点做含凸性的价格变化计算题
  - 凸性正负判断分析题
  - 组合凸性计算题
- **易混淆点**：
  - 凸性不总是正的（可赎回/MBS 负凸性）
  - Δy 必须用小数（1% = 0.01，不是 1）
  - 高凸性需要付出代价（低收益率）

- **关键数值记忆**：
  - 正凸性：利率↓时价格涨更快；利率↑时价格跌更慢
  - 负凸性：利率↓时价格涨受限；利率↑时价格跌加速
  - 零息债券凸性最小（票息效应），但期限最长凸性最大
  - 凸性 vs 久期：久期一阶近似，凸性二阶修正
- **考试技巧**：
  - 含凸性估计比纯久期估计更精确（尤其 Δy > 100bp）
  - 组合久期/凸性仅适用于平行移动检验
  - 可赎回债券的负凸性在利率下降时最明显
  - Δy 为 1% 时，凸性项 = 0.5 × C × 0.0001
