---
title: "M08: Pricing and Valuation of Options"
description: "CFA Level I 2026 Derivatives 官方模块笔记：中文主线、英文术语、编号知识树、LOS 对齐"
subject: "Derivatives"
topic_area: "Derivatives"
level: "CFA Level I"
exam_year: 2026
exam_weight: "5-8%"
module: "M08"
official_module: "Module 8: Pricing and Valuation of Options"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Derivatives
---

# M08: Pricing and Valuation of Options

> **模块定位**：用无套利、复制和工具结构理解远期、期货、互换、期权的风险转移。 本模块聚焦 **Pricing and Valuation of Options**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Pricing and Valuation of Options
- 8.01 | Introduction
- 8.02 | Option Value relative to the Underlying Spot Price
- 8.03 | Option Exercise Value
- 8.04 | Option Moneyness
- 8.05 | Option Time Value
- 8.06 | Arbitrage
- 8.07 | Replication
- 8.08 | Factors Affecting Option Value

## Learning Outcome Statements

1. explain the exercise value, moneyness, and time value of an option
2. contrast the use of arbitrage and replication concepts in pricing forward commitments and contingent claims
3. identify the factors that determine the value of an option and describe how each factor affects the value of an option

---

## 1. 模块定位

### 8.1 学习任务
- **核心问题**：考试希望你用 `Pricing and Valuation of Options` 解释什么、计算什么、或判断什么。
- **输入信息**：题干事实、数据、定义、假设、限制条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 8.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；不要在还没识别题型时直接套公式。

### 8.3 关键英文术语
- **Pricing and Valuation of Options（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Option Value relative to the Underlying Spot Price（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Option Exercise Value（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Option Moneyness（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Option Time Value（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Arbitrage（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Replication（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 8.1 | explain the exercise value, moneyness, and time value of an option | 解释机制、原因和后果 | 写出结论、依据和限制条件。 |
| 8.2 | contrast the use of arbitrage and replication concepts in pricing forward commitments and contingent claims | 识别概念、解释机制并应用到题干。 | 写出结论、依据和限制条件。 |
| 8.3 | identify the factors that determine the value of an option and describe how each factor affects the value of an option | 描述定义、流程和适用场景；识别题干中的关键事实和触发条件；根据条件判断正确结论 | 写出结论、依据和限制条件。 |

## 3. 核心知识树

```text
8. Pricing and Valuation of Options
├─ 8.1 Introduction
│  ├─ 8.1.1 定义/识别：掌握题干关键词与适用条件
│  └─ 8.1.2 应用/判断：把概念或公式转成解题动作
├─ 8.2 Option Value relative to the Underlying Spot Price
│  ├─ 8.2.1 定义/识别：掌握题干关键词与适用条件
│  └─ 8.2.2 应用/判断：把概念或公式转成解题动作
├─ 8.3 Option Exercise Value
│  ├─ 8.3.1 定义/识别：掌握题干关键词与适用条件
│  └─ 8.3.2 应用/判断：把概念或公式转成解题动作
├─ 8.4 Option Moneyness
│  ├─ 8.4.1 定义/识别：掌握题干关键词与适用条件
│  └─ 8.4.2 应用/判断：把概念或公式转成解题动作
├─ 8.5 Option Time Value
│  ├─ 8.5.1 定义/识别：掌握题干关键词与适用条件
│  └─ 8.5.2 应用/判断：把概念或公式转成解题动作
```

## 4. 知识点详解

### 8.1 Introduction
- **中文主线**：本节点解决 `Introduction` 在 Derivatives 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：解释机制、原因和后果；官方表述为：`explain the exercise value, moneyness, and time value of an option`。
- **核心词汇**：**Pricing and Valuation of Options（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 8.2 Option Value relative to the Underlying Spot Price
- **中文主线**：本节点解决 `Option Value relative to the Underlying Spot Price` 在 Derivatives 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：识别概念、解释机制并应用到题干。；官方表述为：`contrast the use of arbitrage and replication concepts in pricing forward commitments and contingent claims`。
- **核心词汇**：**Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 8.3 Option Exercise Value
- **中文主线**：本节点解决 `Option Exercise Value` 在 Derivatives 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：描述定义、流程和适用场景；识别题干中的关键事实和触发条件；根据条件判断正确结论；官方表述为：`identify the factors that determine the value of an option and describe how each factor affects the value of an option`。
- **核心词汇**：**Option Value relative to the Underlying Spot Price（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 8.4 Option Moneyness
- **中文主线**：本节点解决 `Option Moneyness` 在 Derivatives 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：解释机制、原因和后果；官方表述为：`explain the exercise value, moneyness, and time value of an option`。
- **核心词汇**：**Option Exercise Value（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 8.5 Option Time Value
- **中文主线**：本节点解决 `Option Time Value` 在 Derivatives 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：解释机制、原因和后果；官方表述为：`explain the exercise value, moneyness, and time value of an option`。
- **核心词汇**：**Option Moneyness（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。


## 5. 关键公式与计算框架

| 工具 / Formula | 公式或框架 | 中文解释与注意点 |
|---|---|---|
| Forward value | `Vt = St - PV(forward price)` | 远期合约价值随标的价格和折现变化。 |
| Option payoff | `call = max(0, S - X), put = max(0, X - S)` | 先画到期收益，再考虑期权费。 |

计算题通用检查：单位一致、时间口径一致、现金流方向一致；解释题要说明结果代表的经济含义。

## 6. 常见考点与解题思路

- **考点 1：定义与边界**。看到英文术语时，先翻译成中文含义，再判断它解决的是收益、风险、估值、披露、治理还是合规问题。
- **考点 2：方向判断**。如果题干改变一个变量，先写出经济直觉，再用公式或框架验证方向。
- **考点 3：比较题**。用“适用条件 - 优点 - 局限 - 典型陷阱”四列比较，不要只背定义。
- **考点 4：解释题**。答案必须包含结果含义，例如“更高/更低意味着什么”，以及是否需要补充假设。

## 7. 易错点与考试陷阱

- **中英文错配**：看到 `Pricing and Valuation of Options` 相关英文词，不要只按中文直觉判断，先回到官方定义。
- **LOS 动词误读**：`calculate` 要算并解释，`compare` 要列差异，`evaluate` 要给判断依据。
- **口径混用**：时间、收益率、现金流、报告期、组合权重或会计口径不一致时，结论很容易反向。
- **孤立背诵**：本模块知识点通常会与前后模块联动，刷题时记录它触发了哪个上游概念。

## 8. 跨模块关联

- **上游模块**：[[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]]。它提供本模块所需的定义、变量或基础框架。
- **下游模块**：[[M09-Option-Replication-Using-Put-Call-Parity]]。它通常会把本模块工具用于更复杂的估值、风险或情境判断。
- **跨科连接**：与 Portfolio Management 的风险收益框架、Financial Statement Analysis 的证据质量、Ethics 的合规判断保持连接。

## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义和用途。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

本次未发现可直接高置信合并的 legacy 内容。中置信候选已记录到 enrichment map：`00-Derivatives-MOC.md` (0.398), `M04-Arbitrage-and-Replication.md` (0.333), `M08-Binomial-Valuation.md` (0.275)。后续如需人工补强，应先核验其是否符合 2026 官方 LOS。
