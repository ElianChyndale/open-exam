---
title: "M06: Fixed-Income Bond Valuation: Prices and Yields"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M06"
official_module: "Module 6: Fixed-Income Bond Valuation: Prices and Yields"
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

# M06: Fixed-Income Bond Valuation: Prices and Yields

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Fixed-Income Bond Valuation: Prices and Yields**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Fixed-Income Bond Valuation: Prices and Yields
- 6.01 | Introduction
- 6.02 | Bond Pricing and the Time Value of Money
- 6.03 | Relationships between Bond Prices and Bond Features
- 6.04 | Matrix Pricing

## Learning Outcome Statements

1. calculate a bond’s price given a yield-to-maturity on or between coupon dates
2. identify the relationships among a bond’s price, coupon rate, maturity, and yield-to-maturity
3. describe matrix pricing

---

## 1. 模块定位

### 6.1 学习任务
- **核心问题**：考试希望你用 `Fixed-Income Bond Valuation: Prices and Yields` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 6.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 6.3 关键英文术语
- **Fixed-Income Bond Valuation: Prices and Yields（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed-Income Bond Valuation（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Bond Pricing and the Time Value of Money（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Relationships between Bond Prices and Bond Features（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Matrix Pricing（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Time Value of Money（货币时间价值）**：今天的一元钱与未来的一元钱价值不同，必须用折现或复利转换。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 6.1 | calculate a bond’s price given a yield-to-maturity on or between coupon dates | 计算并解释数值结果 | 写出结论、依据、公式口径和限制条件。 |
| 6.2 | identify the relationships among a bond’s price, coupon rate, maturity, and yield-to-maturity | 识别题干中的关键事实和触发条件 | 写出结论、依据、公式口径和限制条件。 |
| 6.3 | describe matrix pricing | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
6. Fixed-Income Bond Valuation: Prices and Yields
├─ 6.1 定价引擎 (Pricing Engine)
│  ├─ 6.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 6.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 6.2 交易价格惯例 (Trading Price Conventions)
│  ├─ 6.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 6.2.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 6.1 定价引擎 (Pricing Engine)

- **核心公式 (English)**
  - 债券定价公式: `P = Σ C/(1+y/m)^t + FV/(1+y/m)^N`
  - 全价公式: `Full Price = Clean Price + Accrued Interest`
- **债券价值 = 票息现值 + 本金现值 (bond value = coupon PV + principal PV)**：债券价格等于所有未来现金流（票息+本金）按到期收益率 (YTM) 贴现的现值之和。
- **折价/溢价/平价与票息率及 YTM 的关系 (discount/premium/par relation to coupon rate and YTM)**：票息率 > YTM → 溢价 (premium)；票息率 = YTM → 平价 (par)；票息率 < YTM → 折价 (discount)。
- **期限越长、票息越低 -> 价格对收益率变动越敏感 (longer maturity + lower coupon -> price more sensitive to yield change)**：零息债券对利率变动最敏感。

### 6.2 交易价格惯例 (Trading Price Conventions)

- **全价 = 净价 + 应计利息 (full price = clean price + accrued interest)【考试核心】**：报价时通常使用净价 (clean price)，但实际交易结算使用全价 (full price / dirty price)。
- **票息日间定价使用分数期处理 (between-coupon-date pricing uses fractional period handling)**：在两个票息日之间交易时，需将贴现期调整为分数期（如 0.5 年、0.75 年）。
- **矩阵定价估算非流动性债券的收益率/价格 (matrix pricing estimates yield/price for illiquid bonds)**：对于不活跃交易的债券，利用相似债券（相同信用评级、相近期限）的价格来估算其合理收益率或价格。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 |
|------|------|
| 债券定价 | `P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N` |
| 全价 | `Full Price = Clean Price + Accrued Interest` |
| 应计利息 | `AI = 每期票息 x 上次付息至今天数 / 付息周期天数` |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 6.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 6.2 Bond Pricing and the Time Value of Money | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.3 Relationships between Bond Prices and Bond Features | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.4 Matrix Pricing | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **计算应计利息 (AI)**：先计算上次付息日至结算日的天数占比，再乘以每期票息金额。
- **计算 full price**：先按照票息日定价公计算现值，再复利至结算日（或计算 AI 加到 clean price 上）。
- **判断 premium/discount/par**：比较 coupon rate 与 YTM 的大小，不必精确计算。
- **矩阵定价计算**：利用可比债券的 YTM 估算目标债券的价格。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：Quoted clean price 是报价习惯，不是买方最终现金支付【考试陷阱】：实际结算时买方支付的是 full price（clean price + AI）。 | ✅ Quoted clean price 是报价习惯，不是买方最终现金支付【考试陷阱】：实际结算时买方支付的是 full price（clean price + AI）。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Day-count convention 因市场而异：国债通常用 actual/actual，公司债常用 30/360。计算 AI 时必须先确认 day-count 规则。 | ✅ Day-count convention 因市场而异：国债通常用 actual/actual，公司债常用 30/360。计算 AI 时必须先确认 day-count 规则。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Fractional period 处理容易出错：在票息日间定价时，可先将未来现金流贴现至上一个票息日，再复利至结算日。 | ✅ Fractional period 处理容易出错：在票息日间定价时，可先将未来现金流贴现至上一个票息日，再复利至结算日。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：CFA 考试中注意区分不同市场的报价惯例：美国国债、欧洲债券、公司债的报价方式不同。 | ✅ CFA 考试中注意区分不同市场的报价惯例：美国国债、欧洲债券、公司债的报价方式不同。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M05-Fixed-Income-Markets-for-Government-Issuers]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 定价方法 → [[M04-Yield-and-Spread-Measures]] 的 YTM 计算
- 应计利息 → 与 day-count convention 紧密结合
- 矩阵定价 → [[M02-Issuance-and-Trading]] 的流动性概念


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M03-Bond-Valuation.md` (high, 0.559)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
