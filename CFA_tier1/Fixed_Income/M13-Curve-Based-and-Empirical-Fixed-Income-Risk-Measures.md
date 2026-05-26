---
title: "M13 — Curve-Based and Empirical Fixed-Income Risk Measures"
description: "CFA Level I 2026 official module: Curve-Based and Empirical Fixed-Income Risk Measures"
module: M13
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 13: Curve-Based and Empirical Fixed-Income Risk Measures"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M13: Curve-Based and Empirical Fixed-Income Risk Measures

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Curve-Based and Empirical Fixed-Income Risk Measures
- 13.01 | Introduction
- 13.02 | Curve-Based Interest Rate Risk Measures
- 13.03 | Bond Risk and Return Using Curve-Based Duration and Convexity
- 13.04 | Key Rate Duration as a Measure of Yield Curve Risk
- 13.05 | Empirical Duration

## Learning Outcome Statements

The candidate should be able to:

- explain why effective duration and effective convexity are the most appropriate measures of interest rate risk for bonds with embedded options
- calculate the percentage price change of a bond for a specified change in benchmark yield, given the bond's effective duration and convexity
- define key rate duration and describe its use to measure price sensitivity of fixed-income instruments to benchmark yield curve changes
- describe the difference between empirical duration and analytical duration

## 🌳 核心知识树

```text
🏆 M13: Curve-Based and Empirical Fixed-Income Risk Measures（曲线与实证风险度量）
├─ ⭐ 13.1 有效久期与有效凸性 (Option-Aware Risk)
│  ├─ 📐 EffDur = (P_- - P_+) / (2 × P_0 × Δy)
│  ├─ 📐 EffCon = (P_- + P_+ - 2P_0) / (P_0 × (Δy)^2)
│  ├─ 🎯 适用于含嵌入期权债券（可赎回、可回售、MBS）
│  ├─ 🎯 现金流随利率变化时使用（修正久期不适用）
│  ├─ 💡 可赎回债券：利率↓时价格上涨受限（负凸性）
│  └─ ⚠️ 有效久期 ≠ 修正久期（仅当现金流不随利率变化时才相等）
│
├─ ⭐ 13.2 关键利率久期 (Key Rate Duration)
│  ├─ 📐 KRD_k = -(1/P) × (ΔP/Δy_k)（仅移动第 k 个期限点）
│  ├─ 🎯 隔离单个期限区间的敏感度
│  ├─ 💡 用于非平行曲线移动分析
│  └─ ⚠️ 非平行移动是常态，不是例外
│
└─ ⭐ 13.3 实证久期 (Empirical Duration)
   ├─ 📐 从历史数据回归得出
   ├─ 💡 可能低于分析久期（利率变动与信用利差反向变动）
   ├─ 💡 反映实际市场行为
   └─ 📐 Δy_bond = Δy_benchmark + Δy_spread（收益率分解）
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `EffDur = (P_- - P_+) / (2 × P_0 × Δy)` | 有效久期 | 含期权债券 | 考虑现金流变化 |
| `EffCon = (P_- + P_+ - 2P_0) / (P_0 × (Δy)^2)` | 有效凸性 | 含期权债券 | 考虑现金流变化 |
| `KRD_k = -(1/P) × (ΔP/Δy_k)` | 关键利率久期 | 非平行移动 | 仅移动第 k 个期限 |
| `Δy_bond = Δy_benchmark + Δy_spread` | 收益率分解 | 风险归因 | benchmark vs spread 分开分析 |

## 🛠️ 常见考点与解题思路

### 考点 1：判断使用有效久期 vs 修正久期
- **含嵌入期权**（可赎回、可回售、MBS）→ 有效久期
- **无期权固定利率债券** → 修正久期
- **判断标准**：现金流是否随利率变化而变化

### 考点 2：计算有效久期
- **步骤**：
  1. 计算利率向上移 Δy 后的价格 P_+
  2. 计算利率向下移 Δy 后的价格 P_-
  3. 代入公式 EffDur = (P_- - P_+) / (2 × P_0 × Δy)
- **注意**：P_- 和 P_+ 的计算需考虑嵌入期权对现金流的影响

### 考点 3：非平行移动分析
- **题型**：给定曲线变化情境（flattening、steepening），判断哪只债券受影响最大
- **思路**：长端上升多 → 长久期债券受影响大；短端上升多 → 短久期债券受影响大
- **工具**：Key Rate Duration 用于定量分析

### 考点 4：Benchmark vs Spread Shift 区分
- **Benchmark shift**：由宏观经济和货币政策驱动
- **Spread shift**：由信用状况、流动性等因素驱动
- **考试常考**：区分两种变动的驱动因素

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| 可赎回债券可用修正久期 | 修正久期高估利率↓时价格上涨 | 价格被 call price 封顶 |
| Effective duration = modified duration | 仅当现金流不随利率变化时相等 | 含期权债券不相等 |
| 平行移动是常态 | 非平行移动是常态 | 组合久期只有限适用 |
| 分析久期 = 实证久期 | 实证久期可能更低 | 利率和利差常反向变动 |

## 🔄 跨模块关联

- **有效久期 vs 修正久期** → [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] 的修正久期对比
- **嵌入期权** → [[M01-Fixed-Income-Instrument-Features]] 的或有条款
- **Spread shift** → [[M14-Credit-Risk]] 的信用利差分析
- **负凸性 MBS** → [[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]] 的提前还款风险

## 📋 复习与刷题提示

- **核心重点**：何时使用有效久期 vs 修正久期的判断
  - 含嵌入期权（可赎回、可回售、MBS）→ 有效久期
  - 无期权固定利率债券 → 修正久期
  - 判断标准：现金流是否随利率变化
- **有效久期计算步骤**：
  1. 计算利率向上移 Δy 后的价格 P_+（含期权对现金流的影响）
  2. 计算利率向下移 Δy 后的价格 P_-（含期权对现金流的影响）
  3. EffDur = (P_- - P_+) / (2 × P_0 × Δy)
- **关键利率久期**：
  - 用途：分析非平行曲线移动
  - 如 steepening（短端↓+长端↑）：短 KRD 多头和长 KRD 空头
  - 如 flattening（短端↑+长端↓）：短 KRD 空头和长 KRD 多头
- **实证久期 vs 分析久期**：
  - 分析久期：基于模型的理论值
  - 实证久期：基于历史数据回归
  - 差异原因：利率变动常伴随信用利差反向变动
- **收益率分解**：
  - Δy_bond = Δy_benchmark + Δy_spread
  - Benchmark shift：宏观经济和货币政策驱动
  - Spread shift：信用状况、流动性等因素驱动
- **刷题建议**：
  - 重点做有效久期计算题
  - Curve risk 分析题（非平行移动的影响）
  - 有效久期 vs 修正久期适用场景判断
- **易混淆点**：
  - 有效久期 ≠ 修正久期
  - 非平行移动是常态
  - 实证久期可能低于分析久期

- **关键数值记忆**：
  - EffDur = (P_- - P_+) / (2 × P_0 × Δy)
  - EffCon = (P_- + P_+ - 2P_0) / (P_0 × (Δy)^2)
  - KRD_k = -(1/P) × (ΔP/Δy_k) — 仅移动第 k 个期限点
  - Δy_bond = Δy_benchmark + Δy_spread（收益率分解）
- **考试技巧**：
  - 含嵌入期权 → 用有效久期（现金流随利率变化）
  - 无期权 → 用修正久期
  - KRD 适用于非平行移动分析（如 steepener / flattener）
  - 实证久期 < 分析久期 → 利率和利差可能反向变动
  - 含期权债券的有效久期可能远小于修正久期
