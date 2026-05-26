---
title: "M02: Fixed-Income Cash Flows and Types"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M02"
official_module: "Module 2: Fixed-Income Cash Flows and Types"
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

# M02: Fixed-Income Cash Flows and Types

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Fixed-Income Cash Flows and Types**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Fixed-Income Cash Flows and Types
- 2.01 | Introduction
- 2.02 | Fixed-Income Cash Flow Structures
- 2.03 | Fixed-Income Contingency Provisions
- 2.04 | Legal, Regulatory, and Tax Considerations

## Learning Outcome Statements

1. describe common cash flow structures of fixed-income instruments and contrast cash flow contingency provisions that benefit issuers and investors
2. describe how legal, regulatory, and tax considerations affect the issuance and trading of fixed-income securities

---

## 1. 模块定位

### 2.1 学习任务
- **核心问题**：考试希望你用 `Fixed-Income Cash Flows and Types` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 2.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 2.3 关键英文术语
- **Fixed-Income Cash Flows and Types（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed-Income Cash Flow Structures（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed-Income Contingency Provisions（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Legal, Regulatory, and Tax Considerations（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Cash Flow（现金流）**：企业现金流入和流出的真实资金轨迹。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 2.1 | describe common cash flow structures of fixed-income instruments and contrast cash flow contingency provisions that benefit issuers and investors | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 2.2 | describe how legal, regulatory, and tax considerations affect the issuance and trading of fixed-income securities | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
2. Fixed-Income Cash Flows and Types
├─ 2.1 票息结构 (Coupon Structures)
│  ├─ 2.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 2.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 2.2 特殊票息与本金结构 (Special Coupon and Principal Structures)
│  ├─ 2.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 2.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 2.3 或有条款 (Contingency Provisions)
│  ├─ 2.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 2.3.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 2.1 票息结构 (Coupon Structures)

- **固定利率债券 (fixed-rate bonds)**：票息率在债券存续期内保持不变，每期支付固定金额的利息。是最常见的债券类型，适合预期利率稳定的环境。
- **浮动利率债券 (floating-rate notes, FRNs)**：票息定期重置，等于参考利率（如 SOFR、EURIBOR）+ 报价利差 (quoted margin)。重置机制缓释利率风险，但报价利差固定使信用风险暴露持续存在。
- **零息债券 (zero-coupon bonds)**：不支付票息，以面值折价发行 (discount issuance)，到期按面值偿还。投资者的全部回报来自买入价与面值之间的价差。零息债券对利率变动最敏感（久期最大）。
- **递延票息债券 (deferred coupon bonds)**：初期（如3-5年）不支付票息，票息累积并后期一次性或在约定时间开始支付。常见于高收益债券或特定项目融资。

### 2.2 特殊票息与本金结构 (Special Coupon and Principal Structures)

- **递增票息债券 (step-up coupon bonds)**：票息率按预设时间表递增。例如前3年利率4%，后3年利率5%，最后2年利率6%。递增票息补偿投资者应对未来利率上升的预期，但债券通常含有可赎回条款。
- **摊还债券 (amortizing bonds)**：每期同时支付利息和本金，现金流稳定递减。典型代表包括汽车贷款ABS、住房抵押贷款和个人分期贷款。
- **通胀挂钩债券 (inflation-linked bonds)**：本金随通货膨胀指数（如CPI）调整，票息按调整后的本金支付。保护投资者购买力免受通胀侵蚀。典型产品为TIPS (Treasury Inflation-Protected Securities)。
- **信用联结票据 (credit-linked notes, CLNs)**：嵌入信用衍生品的债务工具，本金和票息与参考实体的信用事件挂钩。若参考实体发生违约等信用事件，投资者可能损失部分或全部本金。
- **实物支付债券 (payment-in-kind bonds, PIK bonds)**：允许发行人选择以实物（通常是额外债券）而非现金支付票息。PIK债券常见于杠杆收购和高收益融资，会加剧发行人债务负担。

### 2.3 或有条款 (Contingency Provisions)

- **可赎回债券 (callable bonds)【考试核心】**：发行人有权在约定时间按约定价格（赎回价）提前赎回债券。利率下降时发行人可通过赎回并用更低利率再融资来获益。可赎回债券收益率通常高于不可赎回债券，以补偿投资者的再投资风险和价格上行限制。
- **可回售债券 (putable bonds)**：投资者有权在约定时间将债券按约定价格回售给发行人。利率上升时投资者可回售债券以收回资金投入更高收益工具。可回售债券收益率通常低于不可回售债券，投资者为这种保护付出溢价。
- **偿债基金条款 (sinking fund provisions)**：要求发行人定期回购部分流通债券或存入资金以备到期偿付。降低信用风险但也影响投资者的再投资计划。
- **回售条款 (put provisions)**：允许持有人在特定日期以特定价格将债券卖回给发行人。回售价格通常是面值。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 | 说明 |
|------|------|------|
| FRN 票息率 | `Coupon = Reference Rate + Quoted Margin` | 重置日的参考利率 + 固定的报价利差 |
| 零息债券价格 | `P = FV / (1 + y)^n` | 零息债券在到期前不产生现金流 |
| 通胀调整本金 | `Adjusted Principal = Par × (Current CPI / Base CPI)` | 通胀挂钩债券的本金调整 |
| 摊还债券每期现金流 | `PMT = P × [r(1+r)^n] / [(1+r)^n - 1]` | 每期相同，含本金和利息 |
| 递增票息债券 | `Coupon(t) = Coupon_0 + Step × t` | 票息率随时间按计划递增 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 2.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 2.2 Fixed-Income Cash Flow Structures | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 2.3 Fixed-Income Contingency Provisions | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 2.4 Legal, Regulatory, and Tax Considerations | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **比较 fixed-rate vs floating-rate 债券在不同利率环境下的表现**：利率上升时FRN更具吸引力（票息随之上升），利率下降时固定利率债券更优（锁定高票息）。
- **识别 step-up coupon 债券的使用场景**：当发行人信用质量预期改善时可以使用 step-up coupon 结构，因为未来更高的票息补偿了早期的较低票息。
- **区分 amortizing 与 non-amortizing 债券的投资特点**：摊销债券现金流更可预测但再投资风险更高；零息债券收入完全来自价格增值。
- **理解 callable bond 的 yield-to-call 计算**：当市场价格高于赎回价时，YTC通常比YTM更相关。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：FRN 的浮动票息缓释利率风险但未消除【考试陷阱】：重置间的利率变化仍会导致FRN价格波动，且credit spread的变动始终影响价格。 | ✅ FRN 的浮动票息缓释利率风险但未消除【考试陷阱】：重置间的利率变化仍会导致FRN价格波动，且credit spread的变动始终影响价格。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：零息债券虽无票息，仍需纳税（美国对 accrued interest 征税）：投资者需为每年隐含的应计利息纳税，尽管未实际收到现金。 | ✅ 零息债券虽无票息，仍需纳税（美国对 accrued interest 征税）：投资者需为每年隐含的应计利息纳税，尽管未实际收到现金。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：PIK bonds 的利息支付不是真正的"免费"：以债券付息增加了总债务和杠杆，未来违约风险更高。 | ✅ PIK bonds 的利息支付不是真正的"免费"：以债券付息增加了总债务和杠杆，未来违约风险更高。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：通胀挂钩债券的调整可能包含通缩保护或存在调整上限：不同产品的条款差异显著，需仔细阅读发行文件。 | ✅ 通胀挂钩债券的调整可能包含通缩保护或存在调整上限：不同产品的条款差异显著，需仔细阅读发行文件。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Callable bond 在利率下降时出现价格上限（negative convexity）：价格被赎回价封顶，这是callable bond投资者面临的核心风险。 | ✅ Callable bond 在利率下降时出现价格上限（negative convexity）：价格被赎回价封顶，这是callable bond投资者面临的核心风险。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M01-Fixed-Income-Instrument-Features]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M03-Fixed-Income-Issuance-and-Trading]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 现金流类型 → [[M03-Bond-Valuation]] 不同现金流的定价方法
- 浮动利率 → [[M05-Floating-Rate-and-Money-Market]] FRN定价与贴现利差
- FRN 风险度量 → [[M04-Yield-and-Spread-Measures]] 浮动利率利差度量
- 或有条款 → [[M09-Curve-Based-and-Empirical-Risk]] 有效久期与有效凸性
- 摊销结构 → [[M14-MBS-and-CMO]] MBS的提前还款与摊销风险


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M02-Fixed-Income-Cash-Flows.md` (high, 0.463)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
