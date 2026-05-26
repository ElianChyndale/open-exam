---
title: "M01: Fixed-Income Instrument Features"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M01"
official_module: "Module 1: Fixed-Income Instrument Features"
los_count: 2
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M01: Fixed-Income Instrument Features

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Fixed-Income Instrument Features**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Fixed-Income Instrument Features
- 1.01 | Introduction
- 1.02 | Features of Fixed-Income Securities
- 1.03 | Bond Indentures and Covenants

## Learning Outcome Statements

1. describe the features of a fixed-income security
2. describe the contents of a bond indenture and contrast affirmative and negative covenants

---

## 1. 模块定位

### 1.1 学习任务
- **核心问题**：考试希望你用 `Fixed-Income Instrument Features` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 1.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 1.3 关键英文术语
- **Fixed-Income Instrument Features（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Features of Fixed-Income Securities（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Bond Indentures and Covenants（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 1.1 | describe the features of a fixed-income security | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 1.2 | describe the contents of a bond indenture and contrast affirmative and negative covenants | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
1. Fixed-Income Instrument Features
├─ 1.1 合同解剖 (Contract Anatomy)
│  ├─ 1.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 1.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 1.2 债券契约 (Bond Indenture)
│  ├─ 1.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 1.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 1.3 或有条款 (Contingency Provisions)
│  ├─ 1.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 1.3.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 1.1 合同解剖 (Contract Anatomy)

- **发行人/面值/票息/期限/货币/优先级 (issuer/par/coupon/maturity/currency/seniority)**：债券合同的基本要素。面值 (par value) 是到期偿还的本金金额；票息率 (coupon rate) 决定每期利息支付；优先级 (seniority) 影响破产时的受偿顺序。
- **债券契约：法律承诺、支付条款、契约条款 (bond indenture: legal promises, payment terms, covenants)**：契约是发行人与持有人之间的法律合同，包含支付时间表、提前赎回条款、财务约束等。
- **肯定性契约 vs 否定性契约 (affirmative covenants vs negative covenants)【考试陷阱】**：肯定性契约要求发行人做某事（如按时披露财报），否定性契约禁止发行人做某事（如限制新增债务）。考试常混淆两者的分类。

### 1.2 债券契约 (Bond Indenture)

- **法律承诺 (legal promises)**：包括按时支付利息和本金、提供财务报表、维持抵押品等。这些承诺构成发行人的法律义务。
- **支付条款 (payment terms)**：明确票息支付时间和金额、本金偿还方式、计息基准 (day-count convention) 等。
- **契约条款 (covenants)**：保护投资者利益的约定。肯定性契约 (affirmative covenants) 要求发行人做某事（如按时披露财报、支付税负）；否定性契约 (negative covenants) 限制发行人做某事（如限制新增债务、限制资产出售、限制股息支付）。

### 1.3 或有条款 (Contingency Provisions)

- **可赎回债券 (callable bond)【考试核心】**：发行人在约定时间按约定价格赎回债券，有利于发行人（利率下行时可再融资）。
- **可回售债券 (putable bond)【考试核心】**：投资者在约定时间按约定价格将债券回售给发行人，有利于投资者（利率上升时可收回资金）。
- **偿债基金条款 (sinking fund provision)**：要求发行人定期偿还部分本金，降低信用风险但影响投资者再投资计划。

## 5. 关键公式与计算框架

### 5.1 核心内容

本模块以概念为主，不涉及复杂计算。核心关系为：

- `债券价值 = Σ 票息现值 + 本金现值` ——将在 M03 中详细展开
- `票息率 > YTM → 溢价债券 (premium bond)`；`票息率 < YTM → 折价债券 (discount bond)`

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 1.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 1.2 Features of Fixed-Income Securities | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 1.3 Bond Indentures and Covenants | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **区分 affirmative vs negative covenants**：肯定性（affirmative） = 必须做；否定性（negative） = 不能做。题目给出具体条款，让考生判断属于哪一类。
- **识别 embedded option 的受益人**：callable → 发行人受益（利率下降时可低成本再融资）；putable → 投资者受益（利率上升时可提前收回资金）。
- **区分债券类型**：根据描述判断是 fixed-rate、floating-rate、zero-coupon 还是 amortizing 债券。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：票息的确定性不等于回报的确定性：即使固定票息债券的现金流金额确定，价格变动和再投资利率的不确定性仍会导致实际回报波动。 | ✅ 票息的确定性不等于回报的确定性：即使固定票息债券的现金流金额确定，价格变动和再投资利率的不确定性仍会导致实际回报波动。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：可赎回债券在利率下降时价格上升有限：因为发行人会选择赎回，价格被 cap 在赎回价附近。 | ✅ 可赎回债券在利率下降时价格上升有限：因为发行人会选择赎回，价格被 cap 在赎回价附近。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：sinking fund provision 要求发行人定期偿还部分本金，这降低了信用风险但也可能影响投资者的再投资计划。 | ✅ sinking fund provision 要求发行人定期偿还部分本金，这降低了信用风险但也可能影响投资者的再投资计划。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：本科目起点。先用它提供定义、变量或基础框架。
- **下游模块**：[[M02-Fixed-Income-Cash-Flows-and-Types]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 现金流结构 → [[M02-Fixed-Income-Cash-Flows]] 的完整现金流分类
- 或有条款 → [[M09-Curve-Based-and-Empirical-Risk]] 的有效久期与凸性
- 优先级与抵押品 → [[M11-Government-and-Corporate-Credit]] 的信用分析


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M01-Instrument-Features.md` (high, 0.623)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
