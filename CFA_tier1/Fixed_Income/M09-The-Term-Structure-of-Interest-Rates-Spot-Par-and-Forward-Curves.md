---
title: "M09: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M09"
official_module: "Module 9: The Term Structure of Interest Rates: Spot, Par, and Forward Curves"
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

# M09: The Term Structure of Interest Rates: Spot, Par, and Forward Curves

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **The Term Structure of Interest Rates: Spot, Par, and Forward Curves**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: The Term Structure of Interest Rates: Spot, Par, and Forward Curves
- 9.01 | Introduction
- 9.02 | Maturity Structure of Interest Rates and Spot Rates
- 9.03 | Par and Forward Rates
- 9.04 | Spot, Par, and Forward Yield Curves and Interpreting Their Relationship

## Learning Outcome Statements

1. define spot rates and the spot curve, and calculate the price of a bond using spot rates
2. define par and forward rates, and calculate par rates, forward rates from spot rates, spot rates from forward rates, and the price of a bond using forward rates
3. compare the spot curve, par curve, and forward curve

---

## 1. 模块定位

### 9.1 学习任务
- **核心问题**：考试希望你用 `The Term Structure of Interest Rates: Spot, Par, and Forward Curves` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 9.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 9.3 关键英文术语
- **The Term Structure of Interest Rates: Spot, Par, and Forward Curves（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **The Term Structure of Interest Rates（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Maturity Structure of Interest Rates and Spot Rates（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Par and Forward Rates（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Spot, Par, and Forward Yield Curves and Interpreting Their Relationship（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Yield（收益率）**：把债券价格与未来现金流连接起来的回报度量。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 9.1 | define spot rates and the spot curve, and calculate the price of a bond using spot rates | 计算并解释数值结果 | 写出结论、依据、公式口径和限制条件。 |
| 9.2 | define par and forward rates, and calculate par rates, forward rates from spot rates, spot rates from forward rates, and the price of a bond using forward rates | 计算并解释数值结果 | 写出结论、依据、公式口径和限制条件。 |
| 9.3 | compare the spot curve, par curve, and forward curve | 比较相似概念的适用条件与差异 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
9. The Term Structure of Interest Rates: Spot, Par, and Forward Curves
├─ 9.1 曲线词典 (Curve Dictionary)
│  ├─ 9.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 9.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 9.2 曲线计算 (Curve Calculations)
│  ├─ 9.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 9.2.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 9.1 曲线词典 (Curve Dictionary)

- **核心公式 (English)**
  - 即期定价公式: `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t`
  - 远期利率推导: `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^(n-m)`
  - 平价利率公式: `Par rate = (1 - DF_N)/Σ_{t=1}^{N} DF_t`
- **即期曲线以各期限匹配的即期利率贴现单笔现金流 (spot curve discounts a single cash flow at each maturity)**：即期利率 (spot rate) 是单一期限的零息收益率，每个期限对应一个即期利率。
- **平价曲线给出使债券价格等于面值的票息率 (par curve gives coupon rate making a bond price equal par)**：平价利率 (par rate) 是使债券按面值交易的票息率，用于构建互换曲线等参考基准。
- **远期曲线隐含从当前曲线推算的未来借贷利率 (forward curve implies future borrowing/lending rates from today's curve)**：远期利率 (forward rate) 是当前即期曲线隐含的未来区间利率，反映无套利条件。

### 9.2 曲线计算 (Curve Calculations)

- **即期定价：每笔现金流使用其期限匹配的即期利率 (spot pricing: each CF gets its maturity-matched spot rate)**：与使用单一 YTM 不同，即期定价将每笔现金流按其到期期限对应的即期利率分别贴现。
- **从即期推导远期；从链式远期推导即期 (forward from spot; spot from chained forwards)**：二者可互为推导。`(1+s_n)^n = (1+s_m)^m x (1+f_{m,n})^(n-m)`。
- **从贴现因子求解平价利率 (par rate solved from discount factors)**：贴现因子 `DF_n = 1/(1+s_n)^n`，平价利率可由贴现因子序列计算得出。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 |
|------|------|
| 即期定价 | `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t` |
| 远期利率 (从即期) | `(1+s_n)^n = (1+s_m)^m x (1+f_{m,n})^(n-m)` |
| 贴现因子 | `DF_t = 1/(1+s_t)^t` |
| 平价利率 | `Par rate_n = (1 - DF_n)/Σ_{t=1}^{n} DF_t` |
| 即期利率 (从远期) | `(1+s_n)^n = (1+f_0,1)(1+f_1,2)...(1+f_{n-1,n})` |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 9.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 9.2 Maturity Structure of Interest Rates and Spot Rates | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 9.3 Par and Forward Rates | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 9.4 Spot, Par, and Forward Yield Curves and Interpreting Their Relationship | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **即期曲线折价计算**：给定即期利率序列，计算债券价格。将每期现金流用对应的即期利率贴现后求和。
- **远期利率计算**：给定 `s_1` 和 `s_2`，计算 `f_1,2`。使用公式 `(1+s_2)^2 = (1+s_1)(1+f_1,2)`。
- **从即期构建平价曲线**：利用贴现因子求解各期限的平价利率。
- **比较不同曲线形态**：即期曲线上升（正常）vs 下降（倒挂）对远期利率的影响。上升曲线中远期利率高于即期利率。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：远期利率是隐含的无套利利率，非确定性预测 (forward rate is an implied no-arbitrage rate, not a guaranteed fore… | ✅ 远期利率是隐含的无套利利率，非确定性预测 (forward rate is an implied no-arbitrage rate, not a guaranteed fore… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Spot rate vs YTM 的区别：YTM 是单一贴现率适用于所有现金流；spot rate 是每期现金流使用匹配期限的贴现率。两者在平坦曲线下相等，但在倾斜曲线下不同。 | ✅ Spot rate vs YTM 的区别：YTM 是单一贴现率适用于所有现金流；spot rate 是每期现金流使用匹配期限的贴现率。两者在平坦曲线下相等，但在倾斜曲线下不同。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Par rate 不是即期利率：平价利率是使债券按面值交易的票息率，通常介于即期利率之间。 | ✅ Par rate 不是即期利率：平价利率是使债券按面值交易的票息率，通常介于即期利率之间。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：曲线间的关系依赖于无套利假设：如果市场存在摩擦或套利限制，实际关系可能偏离理论值。 | ✅ 曲线间的关系依赖于无套利假设：如果市场存在摩擦或套利限制，实际关系可能偏离理论值。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M08-Yield-and-Yield-Spread-Measures-for-Floating-Rate-Instruments]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M10-Interest-Rate-Risk-and-Return]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- Spot/forward 推导 → [[M03-Bond-Valuation]] 的定价框架
- YTM vs spot → [[M04-Yield-and-Spread-Measures]] 的收益率概念
- 远期利率 → [[M07-Interest-Rate-Risk]] 的预期利率路径


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M06-Spot-Par-and-Forward-Curves.md` (high, 0.61)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
