---
title: "M18: Asset-Backed Security (ABS) Instrument and Market Features"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M18"
official_module: "Module 18: Asset-Backed Security (ABS) Instrument and Market Features"
los_count: 4
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M18: Asset-Backed Security (ABS) Instrument and Market Features

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Asset-Backed Security (ABS) Instrument and Market Features**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Asset-Backed Security (ABS) Instrument and Market Features
- 18.01 | Introduction
- 18.02 | Covered Bonds
- 18.03 | ABS Structures to Address Credit Risk
- 18.04 | Non-Mortgage Asset-Backed Securities
- 18.05 | Collateralized Debt Obligations

## Learning Outcome Statements

1. describe characteristics and risks of covered bonds and how they differ from other asset-backed securities
2. describe typical credit enhancement structures used in securitizations
3. describe types and characteristics of non-mortgage asset-backed securities, including the cash flows and risks of each type
4. describe collateralized debt obligations, including their cash flows and risks

---

## 1. 模块定位

### 18.1 学习任务
- **核心问题**：考试希望你用 `Asset-Backed Security (ABS) Instrument and Market Features` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 18.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 18.3 关键英文术语
- **Asset-Backed Security (ABS) Instrument and Market Features（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Covered Bonds（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **ABS Structures to Address Credit Risk（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Non-Mortgage Asset-Backed Securities（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Collateralized Debt Obligations（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Credit Risk（信用风险）**：发行人无法按时足额履约的风险。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 18.1 | describe characteristics and risks of covered bonds and how they differ from other asset-backed securities | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 18.2 | describe typical credit enhancement structures used in securitizations | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 18.3 | describe types and characteristics of non-mortgage asset-backed securities, including the cash flows and risks of each type | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 18.4 | describe collateralized debt obligations, including their cash flows and risks | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
18. Asset-Backed Security (ABS) Instrument and Market Features
├─ 18.1 ABS 类型 (ABS Families)
│  ├─ 18.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 18.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 18.2 信用增级 (Credit Enhancement)
│  ├─ 18.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 18.2.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 18.1 ABS 类型 (ABS Families)

- **汽车贷款、信用卡、应收账款、其他非抵押担保品 (auto loans, credit cards, receivables, other non-mortgage collateral)**：ABS (asset-backed securities) 的抵押品范围广泛。汽车贷款 ABS 有明确的摊销计划；信用卡 ABS 通常为循环结构（本金可重新投资于新应收账款）；应收账款 ABS 依赖商业交易的付款周期。
- **担保品现金流模式决定摊还与触发风险 (collateral cash flow pattern determines amortization and trigger risk)**：不同类型 ABS 的现金流模式不同。摊还型 (amortizing) 如汽车贷款有固定还款计划；循环型 (revolving) 如信用卡允许借款人在额度内循环使用。
- **有担保债券保持双重追索权，不同于典型 ABS 隔离 (covered bond keeps dual recourse unlike typical ABS isolation)**：Covered bond（有担保债券）与 ABS 的关键区别：covered bond 投资者同时拥有对担保池和发行人的双重追索权 (dual recourse)；而 ABS 投资者仅对 SPV 中的资产池有追索权。

### 18.2 信用增级 (Credit Enhancement)

- **分层、超额抵押、超额利差、准备金账户 (subordination, overcollateralization, excess spread, reserve accounts)**：内部增级方式。分层 (subordination/tranching) 让优先级吸收次级层的保护；超额抵押 (overcollateralization) 指资产池价值超过发行的债券金额；超额利差 (excess spread) 是资产池收益超过证券支付和费用的部分；准备金账户 (reserve account) 作为现金缓冲。
- **担保/保险作为外部支持 (guarantees/insurance as external support)**：外部增级来自第三方机构，如保险公司提供的债券保险 (bond insurance)、银行开立的信用证 (letter of credit) 或公司担保 (corporate guarantee)。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式/概念 |
|------|-----------|
| 超额抵押 | `Overcollateralization = (资产池面值 - 证券面值) / 证券面值` |
| 超额利差 | `Excess Spread = 资产池加权平均利率 - 证券加权平均利率 - 费用` |
| 信用增级水平 | `Credit Enhancement Level = 次级层 + 准备金 + 超额利差现值` |
| 双重追索权 | `Covered Bond: 资产池 + 发行人信用` |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 18.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 18.2 Covered Bonds | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 18.3 ABS Structures to Address Credit Risk | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 18.4 Non-Mortgage Asset-Backed Securities | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐ | 18.5 Collateralized Debt Obligations | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **区分内部与外部信用增级**：内部（分层、超额抵押、超额利差、准备金账户）vs 外部（保险、信用证、第三方担保）。
- **理解 covered bond 的双重追索权**：covered bond 投资者在发行人违约时，既可以追索担保资产池，也可以追索发行人的其他资产。这与 ABS 的单一追索权不同。
- **ABS 的摊销类型判断**：给定抵押品特征（如汽车贷款、信用卡应收款），判断是摊还型还是循环型结构。
- **分析超额利差的缓冲作用**：当资产池中部分贷款违约时，超额利差可以吸收损失，保护优先级证券投资者。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：信用增级重新分配损失吸收，而非免费收益 (credit enhancement reallocates loss absorption; it is not free yield… | ✅ 信用增级重新分配损失吸收，而非免费收益 (credit enhancement reallocates loss absorption; it is not free yield… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Covered bond 不是 ABS：两者最大区别在于法律结构——covered bond 不出售资产给 SPV，资产仍留在发行人资产负债表上，投资者有双重追索权。 | ✅ Covered bond 不是 ABS：两者最大区别在于法律结构——covered bond 不出售资产给 SPV，资产仍留在发行人资产负债表上，投资者有双重追索权。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Excess spread 不是永久性保护：如果资产池中的贷款大规模违约，超额利差可能迅速耗尽。 | ✅ Excess spread 不是永久性保护：如果资产池中的贷款大规模违约，超额利差可能迅速耗尽。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Trigger events（触发事件） ：许多 ABS 设有信用触发机制（如超额利差降至阈值以下），一旦触发会改变现金流分配方式，如强制提前摊还。 | ✅ Trigger events（触发事件） ：许多 ABS 设有信用触发机制（如超额利差降至阈值以下），一旦触发会改变现金流分配方式，如强制提前摊还。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M17-Fixed-Income-Securitization]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 信用增级 → [[M12-Securitization-Foundations]] 的 SPV 结构
- 分层设计 → [[M14-MBS-and-CMO]] 的 CMO 分层
- Covered bond → [[M11-Government-and-Corporate-Credit]] 的发行人信用分析


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M13-ABS-and-Credit-Enhancement.md` (medium, 0.401)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
