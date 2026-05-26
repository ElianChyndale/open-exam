---
title: "M10 — Interest Rate Risk and Return"
description: "CFA Level I 2026 official module: Interest Rate Risk and Return"
module: M10
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 10: Interest Rate Risk and Return"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M10: Interest Rate Risk and Return

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Interest Rate Risk and Return
- 10.01 | Introduction
- 10.02 | Sources of Return from Investing in a Fixed-Rate Bond
- 10.03 | Investment Horizon and Interest Rate Risk
- 10.04 | Macaulay Duration

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret the sources of return from investing in a fixed-rate bond
- describe the relationships among a bond's holding period return, its Macaulay duration, and the investment horizon
- define, calculate, and interpret Macaulay duration

## 🌳 核心知识树

```text
🏆 M10: Interest Rate Risk and Return（利率风险与回报）
├─ ⭐ 10.1 回报分解 (Return Decomposition)
│  ├─ 📐 HPR = (票息 + 再投资收入 + 售价 - 买价) / 买价
│  ├─ 💡 回报三来源：
│  │  ├─ 票息收入 (coupon income)
│  │  ├─ 再投资收入 (reinvestment income)
│  │  └─ 价格变动 (price change / capital gain or loss)
│  ├─ 📐 回归面值 (Pull to Par)：折价债价格上升，溢价债价格下降
│  └─ ⚠️ 已实现回报 ≠ YTM（再投资率变化或提前卖出时）
│
├─ ⭐ 10.2 持有期与利率风险
│  ├─ 📐 Horizon < Macaulay Duration → 价格风险主导（利率↑ → 价格↓）
│  ├─ 📐 Horizon > Macaulay Duration → 再投资风险主导（利率↓ → 再投资收益↓）
│  ├─ 📐 Horizon = Macaulay Duration → 价格风险与再投资风险抵消（免疫）
│  └─ 🎯 零息债券：无再投资风险，但价格风险最大
│
└─ ⭐ 10.3 Macaulay 久期
   ├─ 📐 D_mac = Σ[t × PV(CF_t)] / Full Price
   ├─ 💡 = 现金流回收时间的加权平均值（以 PV 为权重）
   ├─ 💡 零息债券 D_mac = 期限；付息债券 D_mac < 期限
   └─ 🎯 衡量债券的利率敏感度
```

## 📖 知识点详解

### 知识点1：回报分解（Return Decomposition）
**核心概念**：投资固定利率债券的总回报由三个来源构成。理解回报的来源有助于分析利率变化对实际投资收益的影响。
- **票息收入（coupon income）**：持有期间收到的所有票息支付，是债券投资的基础回报
- **再投资收入（reinvestment income）**：将收到的票息按市场利率再投资所产生的额外收益。当利率下降时再投资收入减少，利率上升时再投资收入增加
- **价格变动（price change / capital gain or loss）**：卖出债券时的价格与买入价的差额。利率下降时债券价格上升，利率上升时价格下降
- **回归面值（Pull to Par）**：随着到期日临近，折价债券价格逐渐上升趋近面值，溢价债券价格逐渐下降趋近面值。这一效应独立于利率变化
- **持有期回报率（HPR）**：`HPR = (总票息 + 再投资收入 + 售价 - 买价) / 买价`
- ⚠️ 已实现回报 ≠ YTM：如果投资者在到期前卖出债券，或市场利率变化导致再投资收入改变，实际实现的持有期回报将不同于 YTM

**考试应用**：计算持有期回报（注意再投资收入的复利计算），分析利率变化方向对持有者回报的影响。

### 知识点2：持有期与利率风险（Horizon and Interest Rate Risk）
**核心概念**：持有期长度决定了债券投资者面临的主要风险类型——价格风险还是再投资风险。这是利率风险管理的基础概念。
- **价格风险（price risk）**：利率上升导致债券价格下跌的风险。持有期越短，价格风险的影响越大
- **再投资风险（reinvestment risk）**：利率下降导致票息再投资收益减少的风险。持有期越长，再投资风险的影响越大
- **持有期 < Macaulay 久期** → 价格风险占主导（利率上升导致价格下跌的影响超过再投资收入增加）
- **持有期 > Macaulay 久期** → 再投资风险占主导（利率下降导致再投资收益减少的影响超过价格上涨）
- **持有期 = Macaulay 久期** → 价格风险与再投资风险大致抵消（利率免疫）
- **零息债券**：无再投资风险（因为没有期间现金流），但价格风险最大

**考试应用**：利用 Macaulay 久期判断免疫状态——若持有期等于 Macaulay 久期，价格风险与再投资风险大致抵消。

### 知识点3：Macaulay 久期（Macaulay Duration）
**核心概念**：Macaulay 久期是债券现金流回收时间的加权平均值，以每期现金流现值为权重。它是理解和管理利率风险的核心工具。
- **计算公式**：`D_mac = Σ[t × PV(CF_t)] / Full Price`，其中 t 为现金流发生的时间，PV(CF_t) 为该现金流的现值
- **经济含义**：以年为单位表示的加权平均回收期，也是价格风险与再投资风险平衡的临界持有期
- **零息债券**：Macaulay 久期 = 期限（因为只有一笔现金流在到期时发生）
- **付息债券**：Macaulay 久期 < 期限（因为期间票息缩短了平均回收时间）
- **影响因素**：期限越长、票息越低、收益率越低 → Macaulay 久期越大

**考试应用**：计算 Macaulay 久期，比较不同债券的久期大小，利用久期判断利率敏感度。

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `HPR = (总票息 + 再投资收入 + 售价 - 买价) / 买价` | 持有期回报率 | 计算实际回报 | 再投资收入需复利计算 |
| `D_mac = Σ[t × PV(CF_t)] / Full Price` | Macaulay 久期 | 衡量利率敏感度 | 现金流时间加权平均 |
| `Horizon < D_mac → 价格风险主导` | 久期 vs 持有期 | 判断风险类型 | Horizon > D_mac → 再投资风险主导 |
| `Pull to Par: 折价↑/溢价↓ → Par` | 回归面值 | 到期前价格分析 | 速度非线性，到期前加快 |

## 🛠️ 常见考点与解题思路

### 考点 1：计算持有期回报 (HPR)
- **步骤**：
  1. 计算持有期间收到的所有票息
  2. 计算票息再投资收入（按再投资利率复利）
  3. 计算卖出时的资本利得/损失
  4. HPR = (总票息 + 再投资收入 + 售价 - 买价) / 买价
- **注意**：再投资收入的复利计算是易错点

### 考点 2：利用 Macaulay 久期判断免疫状态
- **思路**：投资者的持有期 = Macaulay Duration → 价格风险与再投资风险大致抵消
- **应用**：保险公司等负债驱动型投资者使用久期匹配进行免疫

### 考点 3：Pull-to-Par 效应分析
- **题型**：给定折价/溢价债券和固定市场利率，计算到期前某时点的价格
- **思路**：折价债券随时间推移价格上升趋近面值；溢价债券价格下降趋近面值
- **速度**：非线性的，到期前加速

### 考点 4：利率变化对回报的影响
- **利率下降** → 价格上升但再投资收入减少（price effect dominates short-term）
- **利率上升** → 价格下降但再投资收入增加（reinvestment effect dominates long-term）

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| Duration 匹配冻结价格 | 平衡价格和再投资效应，非冻结价格 | 两者抵消而非价格不变 |
| 持有期回报 = YTM | YTM 假设持有至到期且再投资率=YTM | 提前卖出或再投资率不同时偏离 |
| Pull-to-par 是线性的 | 速度随到期临近加快 | 价格路径是凸的 |
| 零息债券无风险 | 没有再投资风险，但价格风险最大 | 久期最长 |

## 🔄 跨模块关联

- **Macaulay 久期** → [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] 的修正久期
- **持有期回报** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的 YTM 比较
- **利率风险** → [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] 的 curve-based 风险
- **凸性** → [[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]] 的凸性调整

## 📋 复习与刷题提示

- **核心重点**：Macaulay 久期的计算及其与持有期的关系
- **回报分解**：理解 HPR 的三部分来源
  - 票息收入 + 再投资收入 + 价格变动 = 持有期回报
  - 再投资收入计算需注意复利
- **免疫概念**：持有期 = Macaulay Duration 时的风险抵消机制
  - Horizon < D_mac → 价格风险主导
  - Horizon > D_mac → 再投资风险主导
  - Horizon = D_mac → 免疫（大致抵消）
- **Pull-to-par 分析**：
  - 折价债券：价格随时间上升（C 形路径）
  - 溢价债券：价格随时间下降（倒 C 形路径）
  - 速度非线性，到期前加速
- **Macaulay Duration 计算**：
  - D_mac = Σ[t × PV(CF_t)] / Full Price
  - 零息债券 D_mac = maturity
  - 付息债券 D_mac < maturity
  - 高票息 → 更短的久期
- **典型计算流程**：
  1. 计算每期现金流 PV
  2. 计算 PV 权重
  3. 权重 × 时间求和
- **刷题建议**：
  - 重点做 HPR 计算题（含再投资收入的复利计算）
  - 久期-持有期关系分析题（判断风险主导类型）
  - Pull-to-par 路径分析题
- **易混淆点**：
  - 持有期回报 ≠ YTM
  - Duration 匹配不冻结价格（平衡价格和再投资效应）
  - 零息债券：无再投资风险但有最大价格风险

- **关键数值记忆**：
  - D_mac 零息债券 = 期限
  - D_mac 付息债券 < 期限
  - 票息越高 → D_mac 越短
  - Yield 越高 → D_mac 越短
- **考试技巧**：
  - HPR 计算中再投资收入需要用再投资利率复利计算（非 YTM）
  - 免疫条件：Horizon = Macaulay Duration
  - Pull-to-Par 路径不对称：折价 C 形 vs 溢价倒 C 形
  - 零息债券的 Pull-to-Par 是指数型增长路径
