---
title: "M10: Interest Rate Risk and Return"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M10"
official_module: "Module 10: Interest Rate Risk and Return"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M10: Interest Rate Risk and Return

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Interest Rate Risk and Return**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Interest Rate Risk and Return
- 10.01 | Introduction
- 10.02 | Sources of Return from Investing in a Fixed-Rate Bond
- 10.03 | Investment Horizon and Interest Rate Risk
- 10.04 | Macaulay Duration

## Learning Outcome Statements

1. calculate and interpret the sources of return from investing in a fixed-rate bond;
2. describe the relationships among a bond’s holding period return, its Macaulay duration, and the investment horizon;
3. define, calculate, and interpret Macaulay duration.

---

## 1. 模块定位

### 10.1 学习任务
- **核心问题**：考试希望你用 `Interest Rate Risk and Return` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 10.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 10.3 关键英文术语
- **Interest Rate Risk and Return（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Sources of Return from Investing in a Fixed-Rate Bond（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Investment Horizon and Interest Rate Risk（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Macaulay Duration（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Duration（久期）**：衡量债券价格对利率变化敏感度的核心指标。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 10.1 | calculate and interpret the sources of return from investing in a fixed-rate bond; | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |
| 10.2 | describe the relationships among a bond’s holding period return, its Macaulay duration, and the investment horizon; | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 10.3 | define, calculate, and interpret Macaulay duration. | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
10. Interest Rate Risk and Return
├─ 10.1 回报分解 (Return Decomposition)
│  ├─ 10.1.1 HPR = (coupon income + reinvestment income + sale price - purchase price)/purchase price
│  ├─ 10.1.2 Return sources：coupon income、reinvestment income、price change；YTM 不等于 realized return
│  └─ 10.1.3 Pull to par：discount bond 随到期趋向 par 上行，premium bond 趋向 par 下行，前提是 yield 不变
├─ 10.2 持有期与 Macaulay 久期 (Horizon and Macaulay Duration)
│  ├─ 10.2.1 Macaulay duration = Σ[t x PV(CF_t)]/full price；现金流时间加权平均
│  ├─ 10.2.2 Horizon < MacDur：price risk dominates；Horizon > MacDur：reinvestment risk dominates
│  └─ 10.2.3 Immunization intuition：让投资期限接近 MacDur，用价格效应抵消再投资效应
```

## 4. 知识点详解

### 10.1 回报分解 (Return Decomposition)

- **核心公式 (English)**
  - 持有期回报率: `HPR = (coupon + reinvestment income + sale price - purchase price)/purchase price`
  - Macaulay 久期: `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price`
- **票息收入 + 再投资收入 + 价格变动 (coupon income + reinvestment income + price change)**：债券的持有期回报由三部分构成：收到的票息、票息再投资产生的收益、以及卖出时的资本利得/损失。
- **回归面值与持有期效应 (pull to par and horizon effect)**：随着到期日临近，折价债券价格逐渐上升趋近面值（回归面值）；溢价债券价格逐渐下降趋近面值。这一效应独立于利率变化。
- **当卖出收益率或再投资率变化时，已实现回报不同 (realized return differs when sale yield or reinvestment rate changes)**：如果投资者在到期前卖出债券，或市场利率变化导致再投资收入改变，实际实现的持有期回报将不同于 YTM。

### 10.2 持有期与 Macaulay 久期 (Horizon and Macaulay Duration)

- **投资期限 < Macaulay 久期 -> 价格风险占主导 (investment horizon < Macaulay duration -> price risk dominates)**：久期大于持有期意味着价格风险（利率上升导致价格下跌）超过再投资风险。
- **投资期限 > Macaulay 久期 -> 再投资风险占主导 (investment horizon > Macaulay duration -> reinvestment risk dominates)**：久期小于持有期意味着再投资风险（利率下降导致再投资收益减少）占主导。
- **Macaulay 久期 = 现金流的时间加权平均 (Macaulay duration = weighted average time to cash flows)**：以每期现金流现值为权重，计算现金流回收时间的加权平均。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 |
|------|------|
| 持有期回报率 (HPR) | `HPR = (总票息 + 再投资收入 + 售价 - 买价) / 买价` |
| Macaulay 久期 | `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price` |
| 价格风险 vs 再投资风险 | `Horizon < D_mac → 价格风险主导`；`Horizon > D_mac → 再投资风险主导` |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 10.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 10.2 Sources of Return from Investing in a Fixed-Rate Bond | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 10.3 Investment Horizon and Interest Rate Risk | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 10.4 Macaulay Duration | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **计算持有期回报**：给定买入价格、卖出价格、票息收入和再投资利率，计算 HPR。注意再投资收入的复利计算。
- **利用 Macaulay 久期判断免疫状态**：若投资者的持有期等于 Macaulay 久期，价格风险与再投资风险大致抵消（利率免疫）。
- **Pull-to-par 效应分析**：给定折价/溢价债券和固定的市场利率，计算到期前某时点的价格。
- **判断利率变化方向对债券持有者回报的影响**：利率下降 → 价格上升但再投资收入减少；利率上升 → 价格下降但再投资收入增加。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：Duration 匹配是关于平衡价格和再投资效应，而非冻结价格 (duration matching is about balancing price and reinvestm… | ✅ Duration 匹配是关于平衡价格和再投资效应，而非冻结价格 (duration matching is about balancing price and reinvestm… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：持有期回报 ≠ YTM：YTM 假设持有至到期且再投资率等于 YTM。如果提前卖出或再投资率不同，实际回报会偏离 YTM。 | ✅ 持有期回报 ≠ YTM：YTM 假设持有至到期且再投资率等于 YTM。如果提前卖出或再投资率不同，实际回报会偏离 YTM。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Pull-to-par 速度不是线性的：折价债券的价格向面值回归的速度随着到期日临近而加快。 | ✅ Pull-to-par 速度不是线性的：折价债券的价格向面值回归的速度随着到期日临近而加快。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：零息债券没有再投资风险：因为没有期间现金流，所以再投资风险为零，但价格风险最大。 | ✅ 零息债券没有再投资风险：因为没有期间现金流，所以再投资风险为零，但价格风险最大。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 接口 | 连接模块 | 本模块输出 | 做题用途 |
|---|---|---|---|
| Realized return | [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] | HPR vs YTM | 解释承诺收益率和实际持有期收益差异 |
| Macaulay duration | [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] | cash-flow weighted average time | 修正久期的前置概念 |
| Reinvestment risk | [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] | future/reinvestment rate assumption | 连接 forward/curve 变化 |
| Immunization intuition | Portfolio Management | horizon vs MacDur | 资产负债匹配与利率风险控制 |

- **上游模块**：[[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M11-Yield-Based-Bond-Duration-Measures-and-Properties]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- Macaulay 久期 → [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] 的修正久期
- 持有期回报 → [[M04-Yield-and-Spread-Measures]] 的 YTM 比较
- 利率风险 → [[M09-Curve-Based-and-Empirical-Risk]] 的 curve-based 风险


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M07-Interest-Rate-Risk.md` (high, 0.478)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
