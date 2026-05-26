---
title: "M11 — Yield-Based Bond Duration Measures and Properties"
description: "CFA Level I 2026 official module: Yield-Based Bond Duration Measures and Properties"
module: M11
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 11: Yield-Based Bond Duration Measures and Properties"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M11: Yield-Based Bond Duration Measures and Properties

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Yield-Based Bond Duration Measures and Properties
- 11.01 | Introduction
- 11.02 | Modified Duration
- 11.03 | Money Duration and Price Value of a Basis Point
- 11.04 | Properties of Duration

## Learning Outcome Statements

The candidate should be able to:

- define, calculate, and interpret modified duration, money duration, and the price value of a basis point (PVBP)
- explain how a bond's maturity, coupon, and yield level affect its interest rate risk

## 🌳 核心知识树

```text
🏆 M11: Yield-Based Bond Duration Measures and Properties（基于收益率的久期）
├─ ⭐ 11.1 修正久期 (Modified Duration)
│  ├─ 📐 D_mod = D_mac / (1 + y/m)
│  ├─ 🎯 估计收益率变动 1% 时债券价格变动的百分比
│  ├─ 📐 %ΔP ≈ -D_mod × Δy（一阶近似）
│  └─ ⚠️ 久期是局部的、基于收益率的，假设曲线平行移动
│
├─ ⭐ 11.2 货币久期 (Money Duration)
│  ├─ 📐 Money Duration = D_mod × Full Price
│  ├─ 🎯 以货币金额（而非百分比）表示利率敏感度
│  └─ 💡 用于计算预期价格变化的具体金额
│
├─ ⭐ 11.3 PVBP / DV01
│  ├─ 📐 PVBP ≈ Money Duration × 0.0001
│  ├─ 📐 PVBP = (P_- - P_+)/2（精确计算）
│  └─ 🎯 收益率变动 1bp 时的价格变化
│
└─ ⭐ 11.4 久期影响因素
   ├─ 💡 期限越长 → 久期越大
   ├─ 💡 票息越低 → 久期越大（零息债券久期最大）
   ├─ 💡 收益率水平越高 → 久期越小
   └─ ⚠️ Duration ≠ Maturity（付息债券 Duration < Maturity）
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `D_mod = D_mac / (1 + y/m)` | 修正久期 | 百分比价格敏感度 | 来源 Macaulay 久期 |
| `Money Duration = D_mod × Full Price` | 货币久期 | 金额价格变化 | 需用 Full Price |
| `PVBP ≈ Money Duration × 0.0001` | 基点价值 | 1bp 敏感度 | 近似公式 |
| `%ΔP ≈ -D_mod × Δy` | 价格变化近似 | 快速估计 | 仅小幅变动准确 |
| `D_p = Σ w_i × D_i` | 组合久期 | 组合风险管理 | 仅平行移动有效 |

## 🛠️ 常见考点与解题思路

### 考点 1：用修正久期估计价格变化
- **题型**：给定 D_mod 和 Δy，求 %ΔP
- **公式**：`%ΔP ≈ -D_mod × Δy`
- **注意**：Δy 用小数表示（如 1% = 0.01），符号为负（收益率↑ → 价格↓）

### 考点 2：计算 PVBP / DV01
- **方法一**（近似）：`PVBP ≈ Money Duration × 0.0001`
- **方法二**（精确）：`PVBP = (P_- - P_+)/2`（收益率 ±1bp 后的价格差除以 2）
- **题型**：问收益率变动 1bp 时价格变化多少

### 考点 3：组合久期计算
- **公式**：以各债券市场价值占组合总值的比例为权重，加权平均各债券的久期
- **局限性**：仅适用于收益率曲线平行移动

### 考点 4：久期影响因素分析
- **题型**：比较两只债券的久期大小
- **思路**：期限长 > 短；票息低 > 高；收益率低 > 高；零息债券久期最大

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| Duration = Maturity | 零息债券相等，付息债券 Duration < Maturity | 期间现金流缩短回收时间 |
| 久期对所有变动都准确 | 仅小幅平行移动有效 | 大幅变动需凸性修正 |
| PVBP 对所有债券相同 | 取决于久期和价格 | 不同债券 PVBP 不同 |
| 组合久期无局限性 | 只适用于平行移动 | 非平行移动不准确 |

## 🔄 跨模块关联

- **D_mod 来自 D_mac** → [[M10-Interest-Rate-Risk-and-Return]] 的 Macaulay 久期
- **有效久期** → [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] 的 option-aware 风险
- **组合久期** → [[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]] 的凸性调整
- **收益率分析** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的收益率概念

## 📋 复习与刷题提示

- **核心重点**：修正久期和 PVBP 的计算是最高频考点
- **久期属性**：掌握期限、票息、收益率水平对久期的影响方向
  - 期限 ↑ → 久期 ↑
  - 票息 ↓ → 久期 ↑（零息债券久期最大）
  - 收益率 ↓ → 久期 ↑
- **三个概念区分**：
  - Macaulay Duration：现金流回收时间的加权平均（年）
  - Modified Duration：收益率变动 1% 的价格变动百分比
  - Money Duration：收益率变动 1% 的价格变动金额
- **PVBP 计算**：
  - 近似：PVBP ≈ Money Duration × 0.0001
  - 精确：PVBP = (P_- - P_+)/2
  - PVBP = 收益率变动 1bp 的价格变化
- **组合久期**：
  - 公式：D_p = Σ w_i × D_i（价值权重）
  - 局限性：仅适用于平行收益率曲线移动
- **典型计算流程**：
  1. 已知 D_mac = 7.5，y = 6%，m = 2
  2. D_mod = 7.5 / (1 + 0.06/2) = 7.5 / 1.03 = 7.28
  3. 若 Δy = 0.5%（上升50bp），%ΔP ≈ -7.28 × 0.005 = -3.64%
- **刷题建议**：
  - 重点做久期计算题（D_mod、Money Duration、PVBP）
  - 久期属性分析题（比较两只债券的久期）
  - 组合久期计算题
- **易混淆点**：
  - Duration ≠ Maturity（零息债除外）
  - 久期是局部、一阶近似
  - PVBP 因债券不同而不同

- **关键数值记忆**：
  - 修正久期 ≈ Macaulay 久期 / (1 + y/m)
  - Money Duration = 修正久期 × Full Price
  - PVBP ≈ Money Duration × 0.0001
  - 精确 PVBP = (P_- - P_+) / 2（收益率 ±1bp）
- **久期影响因素对比**：
  - 期限 ↑ → 久期 ↑
  - 票息 ↓ → 久期 ↑（零息债久期最大）
  - 收益率 ↓ → 久期 ↑
  - 零息债券的修正久期 = Macaulay 久期（因为 y = 0 时不影响）
- **典型计算示例**：
  - 已知 D_mac = 7.5，y = 6%，m = 2
  - D_mod = 7.5 / (1 + 0.06/2) = 7.5/1.03 = 7.28
  - Δy = +0.5%（上升 50bp）
  - %ΔP ≈ -7.28 × 0.005 = -3.64%
  - 若 Δy = -0.5%（下降 50bp），%ΔP ≈ +3.64%（对称，但实际因凸性不对称）
- **考试技巧**：
  - 比较久期大小看期限、票息、收益率三个维度
  - PVBP 对小幅变动精确，对大幅变动需要凸性修正
  - 组合久期只适用于平行移动
