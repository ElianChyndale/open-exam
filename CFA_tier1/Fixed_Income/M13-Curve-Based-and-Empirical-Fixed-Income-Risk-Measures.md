---
title: "M13: Curve-Based and Empirical Fixed-Income Risk Measures"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、LOS 对齐"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M13"
official_module: "Module 13: Curve-Based and Empirical Fixed-Income Risk Measures"
los_count: 4
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M13: Curve-Based and Empirical Fixed-Income Risk Measures

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Curve-Based and Empirical Fixed-Income Risk Measures**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Curve-Based and Empirical Fixed-Income Risk Measures
- 13.01 | Introduction
- 13.02 | Curve-Based Interest Rate Risk Measures
- 13.03 | Bond Risk and Return Using Curve-Based Duration and Convexity
- 13.04 | Key Rate Duration as a Measure of Yield Curve Risk
- 13.05 | Empirical Duration

## Learning Outcome Statements

1. explain why effective duration and effective convexity are the most appropriate measures of interest rate risk for bonds with embedded options
2. calculate the percentage price change of a bond for a specified change in benchmark yield, given the bond’s effective duration and convexity
3. define key rate duration and describe its use to measure price sensitivity of fixed-income instruments to benchmark yield curve changes
4. describe the difference between empirical duration and analytical duration

---

## 1. 模块定位

### 13.1 学习任务
- **核心问题**：考试希望你用 `Curve-Based and Empirical Fixed-Income Risk Measures` 解释什么、计算什么、或判断什么。
- **输入信息**：题干事实、数据、定义、假设、限制条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 13.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；不要在还没识别题型时直接套公式。

### 13.3 关键英文术语
- **Curve-Based and Empirical Fixed-Income Risk Measures（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Curve-Based Interest Rate Risk Measures（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Bond Risk and Return Using Curve-Based Duration and Convexity（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Key Rate Duration as a Measure of Yield Curve Risk（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Empirical Duration（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Yield（收益率）**：把债券价格与未来现金流连接起来的回报度量。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 13.1 | explain why effective duration and effective convexity are the most appropriate measures of interest rate risk for bonds with embedded options | 解释机制、原因和后果 | 写出结论、依据和限制条件。 |
| 13.2 | calculate the percentage price change of a bond for a specified change in benchmark yield, given the bond’s effective duration and convexity | 计算并解释数值结果 | 写出结论、依据和限制条件。 |
| 13.3 | define key rate duration and describe its use to measure price sensitivity of fixed-income instruments to benchmark yield curve changes | 描述定义、流程和适用场景 | 写出结论、依据和限制条件。 |
| 13.4 | describe the difference between empirical duration and analytical duration | 描述定义、流程和适用场景 | 写出结论、依据和限制条件。 |

## 3. 核心知识树

```text
13. Curve-Based and Empirical Fixed-Income Risk Measures
├─ 13.1 Introduction
│  ├─ 13.1.1 定义/识别：掌握题干关键词与适用条件
│  └─ 13.1.2 应用/判断：把概念或公式转成解题动作
├─ 13.2 Curve-Based Interest Rate Risk Measures
│  ├─ 13.2.1 定义/识别：掌握题干关键词与适用条件
│  └─ 13.2.2 应用/判断：把概念或公式转成解题动作
├─ 13.3 Bond Risk and Return Using Curve-Based Duration and Convexity
│  ├─ 13.3.1 定义/识别：掌握题干关键词与适用条件
│  └─ 13.3.2 应用/判断：把概念或公式转成解题动作
├─ 13.4 Key Rate Duration as a Measure of Yield Curve Risk
│  ├─ 13.4.1 定义/识别：掌握题干关键词与适用条件
│  └─ 13.4.2 应用/判断：把概念或公式转成解题动作
├─ 13.5 Empirical Duration
│  ├─ 13.5.1 定义/识别：掌握题干关键词与适用条件
│  └─ 13.5.2 应用/判断：把概念或公式转成解题动作
```

## 4. 知识点详解

### 13.1 Introduction
- **中文主线**：本节点解决 `Introduction` 在 Fixed Income 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：解释机制、原因和后果；官方表述为：`explain why effective duration and effective convexity are the most appropriate measures of interest rate risk for bonds with embedded options`。
- **核心词汇**：**Curve-Based and Empirical Fixed-Income Risk Measures（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 13.2 Curve-Based Interest Rate Risk Measures
- **中文主线**：本节点解决 `Curve-Based Interest Rate Risk Measures` 在 Fixed Income 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：计算并解释数值结果；官方表述为：`calculate the percentage price change of a bond for a specified change in benchmark yield, given the bond’s effective duration and convexity`。
- **核心词汇**：**Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 13.3 Bond Risk and Return Using Curve-Based Duration and Convexity
- **中文主线**：本节点解决 `Bond Risk and Return Using Curve-Based Duration and Convexity` 在 Fixed Income 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：描述定义、流程和适用场景；官方表述为：`define key rate duration and describe its use to measure price sensitivity of fixed-income instruments to benchmark yield curve changes`。
- **核心词汇**：**Curve-Based Interest Rate Risk Measures（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 13.4 Key Rate Duration as a Measure of Yield Curve Risk
- **中文主线**：本节点解决 `Key Rate Duration as a Measure of Yield Curve Risk` 在 Fixed Income 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：描述定义、流程和适用场景；官方表述为：`describe the difference between empirical duration and analytical duration`。
- **核心词汇**：**Bond Risk and Return Using Curve-Based Duration and Convexity（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 13.5 Empirical Duration
- **中文主线**：本节点解决 `Empirical Duration` 在 Fixed Income 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。
- **对应 LOS 动作**：解释机制、原因和后果；官方表述为：`explain why effective duration and effective convexity are the most appropriate measures of interest rate risk for bonds with embedded options`。
- **核心词汇**：**Key Rate Duration as a Measure of Yield Curve Risk（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。

### 13.9 Legacy 补强要点
- 来自 `M09-Curve-Based-and-Empirical-Risk.md`：description: 曲线与实证风险度量——有效久期、有效凸性、关键利率久期与曲线非平行移动（中英双语 CFA 备考）; ## 1. 核心知识点; **关键利率久期隔离期限区间的敏感度 (key rate duration isolates maturity-bucket sensitivity)**：关键利率久期 (key rate duration / partial duration) 衡量收益率曲线上特定期限点的利率变动对债券价格的影响，帮助识别非平行移动的风险暴露。。
- 来自 `00-Fixed-Income-MOC.md`：## 最关键：先贴现现金流，再拆收益率，再量化利率和信用风险; ## Fixed Income 核心知识树 (Core Knowledge Tree); ├── M01: 工具特征 (Instrument Features)【考试核心】↔ 2026 Outline P18。


## 5. 关键公式与计算框架

| 工具 / Formula | 公式或框架 | 中文解释与注意点 |
|---|---|---|
| Bond price | `P = Σ C/(1+y)^t + FV/(1+y)^N` | 债券价格等于未来现金流现值。 |
| Full price | `full price = clean price + accrued interest` | 报价通常是 clean price，结算用 full price。 |
| Modified duration | `ModDur = MacDur / (1 + y/m)` | 近似衡量收益率变化 1 单位时价格百分比变化。 |
| Approximate convexity | `(V- + V+ - 2V0) / (V0 × Δy²)` | 凸性修正久期的一阶近似误差。 |

计算题通用检查：单位一致、时间口径一致、现金流方向一致；解释题要说明结果代表的经济含义。

## 6. 常见考点与解题思路

- **考点 1：定义与边界**。看到英文术语时，先翻译成中文含义，再判断它解决的是收益、风险、估值、披露、治理还是合规问题。
- **考点 2：方向判断**。如果题干改变一个变量，先写出经济直觉，再用公式或框架验证方向。
- **考点 3：比较题**。用“适用条件 - 优点 - 局限 - 典型陷阱”四列比较，不要只背定义。
- **考点 4：解释题**。答案必须包含结果含义，例如“更高/更低意味着什么”，以及是否需要补充假设。

## 7. 易错点与考试陷阱

- **中英文错配**：看到 `Curve-Based and Empirical Fixed-Income Risk Measures` 相关英文词，不要只按中文直觉判断，先回到官方定义。
- **LOS 动词误读**：`calculate` 要算并解释，`compare` 要列差异，`evaluate` 要给判断依据。
- **口径混用**：时间、收益率、现金流、报告期、组合权重或会计口径不一致时，结论很容易反向。
- **孤立背诵**：本模块知识点通常会与前后模块联动，刷题时记录它触发了哪个上游概念。

## 8. 跨模块关联

- **上游模块**：[[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]]。它提供本模块所需的定义、变量或基础框架。
- **下游模块**：[[M14-Credit-Risk]]。它通常会把本模块工具用于更复杂的估值、风险或情境判断。
- **跨科连接**：与 Portfolio Management 的风险收益框架、Financial Statement Analysis 的证据质量、Ethics 的合规判断保持连接。

## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义和用途。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

以下内容来自高置信 legacy 映射，已作为补强入口保留；若与官方 2026 LOS 冲突，以官方内容为准。
### 来源：M09-Curve-Based-and-Empirical-Risk.md（confidence 0.529）
- **可复用结构**：M12: 曲线与实证风险度量 (Curve-Based and Empirical Risk Measures)；1. 核心知识点；1.1 期权感知风险 (Option-Aware Risk)；1.2 曲线风险 (Curve Risk)；2. 关键公式；3. 常见考点与解题思路
- **高价值要点**：description: 曲线与实证风险度量——有效久期、有效凸性、关键利率久期与曲线非平行移动（中英双语 CFA 备考）；## 1. 核心知识点；**关键利率久期隔离期限区间的敏感度 (key rate duration isolates maturity-bucket sensitivity)**：关键利率久期 (key rate duration / partial duration) 衡量收益率曲线上特定期限点的利率变动对债券价格的影响，帮助识别非平行移动的风险暴露。；## 2. 关键公式
- **公式/计算线索**：**分析久期可能与观察到的经验久期不同 (analytical duration may differ from observed empirical duration)**：基于模型的久期（分析久期）可能不同于从历史数据回归得出的经验久期 (empirical duration)，原因包括模型假设误差、市场摩擦等。；**关键利率久期隔离期限区间的敏感度 (key rate duration isolates maturity-bucket sensitivity)**：关键利率久期 (key rate duration / partial duration) 衡量收益率曲线上特定期限点的利率变动对债券价格的影响，帮助识别非平行移动的风险暴露。；**非平行曲线移动打破单一久期直觉 (non-parallel curve shifts break single-duration intuition)**：实际收益率曲线变动往往不是平行的（如长端上升幅度大于短端），此时单一久期指标无法准确描述风险。
- **易错提示**：## 4. 易错点提醒

### 来源：00-Fixed-Income-MOC.md（confidence 0.43）
- **可复用结构**：00-Fixed-Income-MOC；笔记属性；最关键：先贴现现金流，再拆收益率，再量化利率和信用风险；科目概览；Fixed Income 核心知识树 (Core Knowledge Tree)；核心对比专题
- **高价值要点**：## 最关键：先贴现现金流，再拆收益率，再量化利率和信用风险；## Fixed Income 核心知识树 (Core Knowledge Tree)；├── M01: 工具特征 (Instrument Features)【考试核心】↔ 2026 Outline P18；├── M02: 现金流类型 (Cash Flows and Types)【考试核心】↔ 2026 Outline P18
- **公式/计算线索**：description: CFA Level I Fixed Income master MOC for bond pricing, yield measures, duration, credit, structured products, and traps.；│ ├── 回购 = 附抵押融资，含 haircut 和交易对手风险 (repo = collateralized financing with haircut and counterparty exposure) (回购融资)；│ └── 注意：高收益的"高收益"不等于高回报 (high-yield is not necessarily high-return)
- **易错提示**：│ │ └── 肯定性契约 vs 否定性契约 (affirmative covenants vs negative covenants)【考试陷阱】(契约类型)；│ └── 注意：coupon 的确定性不等于回报确定，价格、再投资和信用仍会变；│ └── 注意：高收益的"高收益"不等于高回报 (high-yield is not necessarily high-return)
