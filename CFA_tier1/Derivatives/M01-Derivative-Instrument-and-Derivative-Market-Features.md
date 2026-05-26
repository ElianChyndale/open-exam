---
title: "M01: Derivative Instrument and Derivative Market Features"
description: "CFA Level I 2026 Derivatives 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Derivatives"
topic_area: "Derivatives"
level: "CFA Level I"
exam_year: 2026
exam_weight: "5-8%"
module: "M01"
official_module: "Module 1: Derivative Instrument and Derivative Market Features"
los_count: 2
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Derivatives
---

# M01: Derivative Instrument and Derivative Market Features

> **模块定位**：用无套利、复制和工具结构理解远期、期货、互换、期权的风险转移。 本模块聚焦 **Derivative Instrument and Derivative Market Features**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Derivative Instrument and Derivative Market Features
- 1.01 | Introduction
- 1.02 | Derivative Features
- 1.03 | Derivative Underlyings
- 1.04 | Derivative Markets

## Learning Outcome Statements

1. define a derivative and describe basic features of a derivative instrument
2. describe the basic features of derivative markets, and contrast over-the-counter and exchange-traded derivative markets

---

## 1. 模块定位

### 1.1 学习任务
- **核心问题**：考试希望你用 `Derivative Instrument and Derivative Market Features` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 1.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 1.3 关键英文术语
- **Derivative Instrument and Derivative Market Features（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Derivative Features（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Derivative Underlyings（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Derivative Markets（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 1.1 | define a derivative and describe basic features of a derivative instrument | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 1.2 | describe the basic features of derivative markets, and contrast over-the-counter and exchange-traded derivative markets | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
1. Derivative Instrument and Derivative Market Features
├─ 1.1 核心内容
│  ├─ 1.1.1 Derivative definition：价值来自 underlying，合约可用于转移/重塑风险
│  ├─ 1.1.2 Contract terms：underlying、notional、long/short、settlement date、delivery/cash settlement
│  ├─ 1.1.3 Market venues：exchange-traded 标准化/清算/保证金；OTC 定制化/双边信用风险
│  └─ 1.1.4 考试判断：notional 是敞口规模参照，不是初始投资额或最大损失
```

## 4. 知识点详解

### 1.1 核心内容

**合约要素 (Contract Elements)**
- **标的资产 (Underlying)**：股票、利率、外汇、信用、大宗商品及其他参照物 (equity, rate, FX, credit, commodity, other reference)
- **多头与空头 (Long vs Short)**：多头在未来买入资产，空头在未来卖出资产；收益取决于标的资产未来状态 (long buys, short sells; payoff depends on future state of underlying)
- **结算方式 (Settlement)**：实物交割 (physical delivery) 或现金结算 (cash settlement)

**市场结构 (Market Structure)**
- **交易所交易 (Exchange-Traded)**：标准化合约、中央清算所、保证金制度、每日盯市 (standardized, clearinghouse, margin, daily marking-to-market)
- **场外交易 (OTC)**：定制化条款、双边交易对手风险、无中央清算 (customization, counterparty exposure, bilateral terms)
- **名义金额 (Notional Amount)**：放大风险敞口但不等于实际在险现金 (scales exposure but not automatically cash at risk)

## 5. 关键公式与计算框架

### 5.1 核心内容

| 节点 | 框架 | 使用条件 | 考试判断 |
|---|---|---|---|
| 1.1.1 | `Derivative value = function(underlying state)` | 定义题 | 合约本身不是标的资产所有权，价值随参照物变化。 |
| 1.1.2 | Long/short map | 多空题 | long 受益方向取决于工具；long call 与 long forward 不同。 |
| 1.1.2 | Notional vs market value | 风险敞口题 | market value 可很小，但 economic exposure 可能很大。 |
| 1.1.3 | Exchange vs OTC table | 市场结构题 | exchange 降低 counterparty risk 但牺牲定制化；OTC 反之。 |
| 1.1.3 | Settlement: physical vs cash | 交割题 | 指数类常现金结算，商品/外汇可实物或现金结算。 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 1.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 1.2 Derivative Features | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 1.3 Derivative Underlyings | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 1.4 Derivative Markets | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **区分交易所 vs OTC**：标准化 vs 定制化；清算所 vs 双边风险；保证金 vs 信用风险
- **判断结算方式**：实物交割多用于商品/外汇；现金结算多用于指数/利率
- **名义金额的理解**：名义金额不是实际投入资金，而是计算回报的参照基数

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：【考试陷阱】衍生品当前价值很小，但经济敞口可能非常大 (derivative value can be small today while exposure is economi… | ✅ 【考试陷阱】衍生品当前价值很小，但经济敞口可能非常大 (derivative value can be small today while exposure is economi… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：不要将名义金额 (notional) 误认为最大损失 —— 名义金额是规模参照，不是风险上限 | ✅ 不要将名义金额 (notional) 误认为最大损失 —— 名义金额是规模参照，不是风险上限 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：OTC 衍生品不意味着"更危险"，而是风险类型不同（交易对手风险 vs 流动性风险） | ✅ OTC 衍生品不意味着"更危险"，而是风险类型不同（交易对手风险 vs 流动性风险） | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 连接 | 传递内容 | 做题用途 |
|---|---|---|
| `M01 -> M02` | underlying、long/short、settlement、venue | 分类 forward commitments 与 contingent claims。 |
| `M01 -> M03` | notional、leverage、counterparty risk | 判断收益、风险和使用者目的。 |
| `M01 -> M06` | exchange trading、margin、daily settlement | 解释 futures 与 forwards 的现金流时点差异。 |
| `M01 -> PM/Risk Management` | exposure vs cash invested | 防止把 notional 当实际投入或最大亏损。 |


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M01-Instruments-and-Markets.md` (high, 0.502)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
