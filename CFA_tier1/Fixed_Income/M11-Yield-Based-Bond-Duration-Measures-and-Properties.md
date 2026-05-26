---
title: "M11: Yield-Based Bond Duration Measures and Properties"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M11"
official_module: "Module 11: Yield-Based Bond Duration Measures and Properties"
los_count: 2
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M11: Yield-Based Bond Duration Measures and Properties

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Yield-Based Bond Duration Measures and Properties**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Yield-Based Bond Duration Measures and Properties
- 11.01 | Introduction
- 11.02 | Modified Duration
- 11.03 | Money Duration and Price Value of a Basis Point
- 11.04 | Properties of Duration

## Learning Outcome Statements

1. define, calculate, and interpret modified duration, money duration, and the price value of a basis point (PVBP)
2. explain how a bond’s maturity, coupon, and yield level affect its interest rate risk

---

## 1. 模块定位

### 11.1 学习任务
- **核心问题**：考试希望你用 `Yield-Based Bond Duration Measures and Properties` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 11.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 11.3 关键英文术语
- **Yield-Based Bond Duration Measures and Properties（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Modified Duration（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Money Duration and Price Value of a Basis Point（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Properties of Duration（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Yield（收益率）**：把债券价格与未来现金流连接起来的回报度量。
- **Duration（久期）**：衡量债券价格对利率变化敏感度的核心指标。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 11.1 | define, calculate, and interpret modified duration, money duration, and the price value of a basis point (PVBP) | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |
| 11.2 | explain how a bond’s maturity, coupon, and yield level affect its interest rate risk | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
11. Yield-Based Bond Duration Measures and Properties
├─ 11.1 久期家族 (Duration Family)
│  ├─ 11.1.1 Modified duration = Macaulay duration/(1+y/m)；估计小幅平行 YTM 变动下的 % price change
│  ├─ 11.1.2 Money duration = modified duration x full price；把百分比敏感度转成货币金额
│  └─ 11.1.3 PVBP ≈ money duration x 0.0001；也可用 (P_- - P_+)/2 估计 1bp price value
├─ 11.2 凸性 (Convexity)
│  ├─ 11.2.1 Duration-only approximation：%ΔP ≈ -D_mod x Δy；Δy 用小数
│  ├─ 11.2.2 Duration drivers：maturity 越长、coupon 越低、yield 越低，duration 通常越高
│  └─ 11.2.3 Yield-based measures 假设现金流固定；含期权债券需转向 effective duration
```

## 4. 知识点详解

### 11.1 久期家族 (Duration Family)

- **核心公式 (English)**
  - 修正久期: `D_mod = D_mac/(1+y/m)`
  - 货币久期: `Money Duration = D_mod x Full Price`
  - PVBP: `PVBP ≈ Money Duration x 0.0001`
  - 价格变化近似: `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2`
- **修正久期估计价格对收益率变动的百分比敏感度 (modified duration estimates % price sensitivity to yield)**：修正久期 = Macaulay 久期 / (1 + y/m)，表示收益率变动 1% 时债券价格变动的百分比。
- **货币久期估计每单位收益率变动的货币价格变化 (money duration estimates currency price change per yield unit)**：货币久期 = 修正久期 x 全价，以货币金额（而非百分比）表示利率敏感度。
- **PVBP = 收益率变动 1bp 的价格变化 (PVBP = price change for 1 bp yield shift)**：PVBP (price value of a basis point) 也称为 DV01。

### 11.2 凸性 (Convexity)

- **凸性修正久期遗漏的曲率 (convexity corrects curvature missed by duration)**：久期是一阶线性近似，凸性补偿二阶曲率效应。当收益率变动较大时，凸性校正至关重要。
- **正凸性有利于对称收益率变动 (positive convexity helps for symmetric yield moves)**：正凸性债券在利率下降时价格上升的幅度大于在利率等幅上升时价格下降的幅度。
- **组合久期/凸性使用价值权重但有局限性 (portfolio duration/convexity use value weights with limitations)**：组合久期 = Σ 债券权重 x 债券久期，但仅适用于平行收益率曲线移动。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 |
|------|------|
| 修正久期 | `D_mod = D_mac / (1 + y/m)` |
| 货币久期 | `Money Duration = D_mod x Full Price` |
| PVBP | `PVBP = (P_- - P_+)/2` 或 `≈ Money Duration x 0.0001` |
| 价格变化（含凸性） | `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2` |
| 凸性计算 | `Convexity = (P_- + P_+ - 2P_0) / (P_0 x (Δy)^2)` |
| 组合久期 | `D_p = Σ w_i x D_i`（价值权重） |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 11.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 11.2 Modified Duration | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 11.3 Money Duration and Price Value of a Basis Point | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 11.4 Properties of Duration | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **用修正久期估计价格变化**：给定 D_mod 和 Δy，计算 `%ΔP ≈ -D_mod x Δy`。
- **用凸性改进估计**：收益率变动较大时（如 > 100bp），必须加入凸性项。
- **计算 PVBP/DV01**：可用近似公式 `Money Duration x 0.0001`，或直接计算收益率上下移 1bp 后的价格差。
- **组合久期计算**：以各债券市场价值占组合总价值的比例为权重，加权平均各债券的久期。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：久期是局部的、基于收益率的；勿将其视为完整曲线压力测试 (duration is local and yield-based; do not treat it as a full… | ✅ 久期是局部的、基于收益率的；勿将其视为完整曲线压力测试 (duration is local and yield-based; do not treat it as a full… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Duration 和 maturity 不是一回事：零息债券的 Macaulay duration = maturity；但付息债券的 duration < maturity。高… | ✅ Duration 和 maturity 不是一回事：零息债券的 Macaulay duration = maturity；但付息债券的 duration < maturity。高… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：正凸性对投资者有利：但获得正凸性通常要付出代价（如放弃部分收益），市场不会免费提供正凸性。 | ✅ 正凸性对投资者有利：但获得正凸性通常要付出代价（如放弃部分收益），市场不会免费提供正凸性。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：凸性用 decimals 计算时 Δy 也要用小数：Δy = 0.01 表示 1%（不是 1）。常见错误是忘记将百分比转换为小数。 | ✅ 凸性用 decimals 计算时 Δy 也要用小数：Δy = 0.01 表示 1%（不是 1）。常见错误是忘记将百分比转换为小数。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 接口 | 连接模块 | 本模块输出 | 做题用途 |
|---|---|---|---|
| Price sensitivity | [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] | modified duration、PVBP | 估计 yield change 下的价格变化 |
| Convexity correction | [[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]] | duration-only approximation | 大幅 yield move 时加 convexity |
| Curve limitation | [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] | yield-based duration assumptions | 非平行曲线或含期权时改用 KRD/effective duration |
| Portfolio risk | Portfolio Management | money duration/PVBP | 组合利率风险预算 |

- **上游模块**：[[M10-Interest-Rate-Risk-and-Return]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- D_mod 来自 D_mac → [[M07-Interest-Rate-Risk]] 的 Macaulay 久期
- 有效久期 → [[M09-Curve-Based-and-Empirical-Risk]] 的 option-aware 风险
- 组合久期 → [[M04-Yield-and-Spread-Measures]] 的收益率分析


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M08-Duration-and-Convexity.md` (high, 0.59)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
