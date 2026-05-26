---
title: "M08: Yield and Yield Spread Measures for Floating-Rate Instruments"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M08"
official_module: "Module 8: Yield and Yield Spread Measures for Floating-Rate Instruments"
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

# M08: Yield and Yield Spread Measures for Floating-Rate Instruments

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Yield and Yield Spread Measures for Floating-Rate Instruments**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Yield and Yield Spread Measures for Floating-Rate Instruments
- 8.01 | Introduction
- 8.02 | Yield and Yield Spread Measures for Floating-Rate Notes
- 8.03 | Yield Measures for Money Market Instruments

## Learning Outcome Statements

1. calculate and interpret yield spread measures for floating-rate instruments
2. calculate and interpret yield measures for money market instruments

---

## 1. 模块定位

### 8.1 学习任务
- **核心问题**：考试希望你用 `Yield and Yield Spread Measures for Floating-Rate Instruments` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 8.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 8.3 关键英文术语
- **Yield and Yield Spread Measures for Floating-Rate Instruments（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Yield and Yield Spread Measures for Floating-Rate Notes（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Yield Measures for Money Market Instruments（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Yield（收益率）**：把债券价格与未来现金流连接起来的回报度量。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 8.1 | calculate and interpret yield spread measures for floating-rate instruments | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |
| 8.2 | calculate and interpret yield measures for money market instruments | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
8. Yield and Yield Spread Measures for Floating-Rate Instruments
├─ 8.1 Introduction
│  ├─ 8.1.1 FRN coupon = reference rate + quoted margin；reset date 重新确定 coupon
│  ├─ 8.1.2 Price near par 的前提是 required margin ≈ quoted margin；信用恶化会使 price < par
│  └─ 8.1.3 Discount margin 是使 FRN 现金流现值等于 market price 的 required spread
├─ 8.2 Yield and Yield Spread Measures for Floating-Rate Notes
│  ├─ 8.2.1 Quoted margin 固定，reference rate 浮动；两者合成下一期 coupon
│  ├─ 8.2.2 Required margin 上升 -> price 下降；required margin 低于 quoted margin -> price 高于 par
│  └─ 8.2.3 Reset lag 与 credit spread 变化解释为什么 FRN 仍有价格波动
├─ 8.3 Yield Measures for Money Market Instruments
│  ├─ 8.3.1 BDY = (FV-P)/FV x 360/t；分母是 face value
│  ├─ 8.3.2 MMY = (FV-P)/P x 360/t；分母是 purchase price
│  └─ 8.3.3 BEY/add-on rate 用 purchase price，day basis 按题干 365 或指定口径
```

## 4. 知识点详解

### 8.1 Introduction

- **中文主线**：围绕 `Introduction` 掌握定义、适用条件、公式/框架和考试判断。
- **对应动作**：计算并解释数值结果；解释结果的投资含义

### 8.2 Yield and Yield Spread Measures for Floating-Rate Notes

- **中文主线**：围绕 `Yield and Yield Spread Measures for Floating-Rate Notes` 掌握定义、适用条件、公式/框架和考试判断。
- **对应动作**：计算并解释数值结果；解释结果的投资含义

### 8.3 Yield Measures for Money Market Instruments

- **中文主线**：围绕 `Yield Measures for Money Market Instruments` 掌握定义、适用条件、公式/框架和考试判断。
- **对应动作**：识别概念并应用到题干。

## 5. 关键公式与计算框架

### 5.1 FRN 票息与利差框架

| 指标 | 公式/框架 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| FRN coupon rate | `Reference rate + quoted margin` | `8.1.1` | coupon 在 reset date 按参考利率重置 |
| Required margin | `Market required spread over reference rate` | `8.1.2` | required margin 上升会压低 FRN price |
| Discount margin | `Margin that makes PV of projected FRN cash flows = market price` | `8.1.3` | price 偏离 par 时的核心利差概念 |
| Par intuition | `Quoted margin ≈ required margin -> price ≈ par` | `8.2.2` | 信用风险变化会打破 par 附近定价 |

### 5.2 货币市场收益率选择框架

| 指标 | 公式 | 知识树节点 | 分母/天数陷阱 |
|------|------|------------|----------|
| Bank discount yield (BDY) | `(FV - P)/FV x 360/t` | `8.3.1` | 分母是 face value |
| Money market yield (MMY) | `(FV - P)/P x 360/t` | `8.3.2` | 分母是 purchase price，仍用 360 |
| Bond equivalent yield (BEY) | `(FV - P)/P x 365/t` | `8.3.3` | 分母是 purchase price，年基准 365 |
| Add-on rate | `(Interest/P) x days in year/t` | `8.3.3` | 读题确认 360/365 或市场惯例 |

### 5.3 做题顺序

1. 先判断工具是 FRN 还是 pure discount money market instrument。
2. FRN 题先比较 `quoted margin` 与 `required/discount margin`，再判断 price relative to par。
3. Money market 题先圈出 `FV`、`P`、`t`、`360/365`，再选择 BDY/MMY/BEY。
4. 解释题不要说“浮动利率无风险”；正确说法是 reset 缓释 benchmark rate risk，但 credit/liquidity spread 仍会影响价格。

---

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 8.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 8.2 Yield and Yield Spread Measures for Floating-Rate Notes | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 8.3 Yield Measures for Money Market Instruments | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ clean price 就是付款价 | ✅ 实际付款价是 full price | 按官方定义和 LOS 口径核验。 |
| ❌ current yield 就是总回报 | ✅ 它忽略 price change 和 reinvestment | 按官方定义和 LOS 口径核验。 |
| ❌ YTM 就是每期现金流真实折现率 | ✅ 更精确时应使用 spot curve | 按官方定义和 LOS 口径核验。 |
| ❌ duration 越大收益越高 | ✅ duration 衡量的是利率敏感度，不是回报 | 按官方定义和 LOS 口径核验。 |
| ❌ convexity 只是锦上添花 | ✅ yield move 大时很关键 | 按官方定义和 LOS 口径核验。 |
| ❌ callable bond 对投资者更好 | ✅ callable 通常有利发行人 | 按官方定义和 LOS 口径核验。 |
| ❌ spread 变宽只可能是 default 风险上升 | ✅ 也可能是 liquidity 或 option factors | 按官方定义和 LOS 口径核验。 |
| ❌ MBS 提前还款一定利好投资者 | ✅ 再投资风险和负 convexity 可能伤害投资者 | 按官方定义和 LOS 口径核验。 |
| ❌ high coupon bond 一定 duration 更高 | ✅ 通常反而 duration 更低 | 按官方定义和 LOS 口径核验。 |
| ❌ 债券题都先算 YTM 就够了 | ✅ spot/forward/option-adjusted 场景不能偷懒 | 按官方定义和 LOS 口径核验。 |

## 8. 跨模块关联

| 接口 | 连接模块 | 本模块输出 | 做题用途 |
|---|---|---|---|
| Short-rate market | [[M03-Fixed-Income-Issuance-and-Trading]] / [[M04-Fixed-Income-Markets-for-Corporate-Issuers]] | money market quote、CP、repo、FRN | 判断短端融资成本 |
| FRN credit spread | [[M14-Credit-Risk]] | quoted margin vs required margin | 区分 reference rate reset 和 credit deterioration |
| Yield conversion | [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] | BEY/MMY/EAY 口径 | 与固定利率债收益率口径统一 |
| Curve input | [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] | short-term rates | 连接短端曲线和 forward rate |

- **上游模块**：[[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

```text
工具特征 (Instrument Features)
├── 或有条款 -> 有效久期/凸性 (Contingency provisions -> Effective duration / convexity)
├── 优先级与抵押品 -> 信用分析 (Seniority and collateral -> Credit analysis)
└── 现金流类型 -> 不同票息结构的定价 (Cash-flow types -> Pricing of different coupon structures)
现金流与市场 (Cash Flows and Markets)
├── 浮动利率 -> FRN 定价与贴现利差 (Floating rate -> FRN pricing and discount margin)
├── 公司融资工具 -> 公司信用分析 (Corporate funding instruments -> Corporate credit analysis)
└── 政府发行人 -> 主权信用分析 (Government issuers -> Sovereign credit analysis)
定价与收益率 (Pricing and Yield)
├── YTM -> 固定利率利差度量 (YTM -> fixed-rate spread measures)
├── 即期曲线 -> 平价曲线 -> 远期曲线 (Spot curve -> par curve -> forward curve)
└── 持有期回报 -> 持有期 vs Macaulay 久期 (Holding-period return -> horizon vs Macaulay duration)
风险分层 (Risk Layer)
├── 基于收益率的久期 -> 凸性 -> 组合聚合 (Yield-based duration -> convexity -> portfolio aggregation)
├── 基于曲线的风险 -> 关键利率久期 -> 非平行移动 (Curve-based risk -> key rate duration -> non-parallel shifts)
└── 信用利差 -> 主权/公司分析 -> 债项排名 (Credit spread -> sovereign/corporate analysis -> issue ranking)
证券化 (Securitization)
├── SPV 结构 -> ABS 增级 -> RMBS 提前还款 -> CMO 分层 -> CMBS 气球风险 (SPV structure -> ABS enhancement -> RMBS prepayment -> CMO tranching -> CMBS balloon risk)
└── RMBS 提前还款概念 vs CMBS 提前还款保护 (RMBS prepayment risk vs CMBS prepayment protection)
```

---


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`00-Fixed-Income-MOC.md` (high, 0.645)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
