---
title: "M17: Fixed-Income Securitization"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M17"
official_module: "Module 17: Fixed-Income Securitization"
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

# M17: Fixed-Income Securitization

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Fixed-Income Securitization**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Fixed-Income Securitization
- 17.01 | Introduction
- 17.02 | The Benefits of Securitization
- 17.03 | The Securitization Process

## Learning Outcome Statements

1. explain benefits of securitization for issuers, investors, economies, and financial markets
2. describe securitization, including the parties and the roles they play

---

## 1. 模块定位

### 17.1 学习任务
- **核心问题**：考试希望你用 `Fixed-Income Securitization` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 17.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 17.3 关键英文术语
- **Fixed-Income Securitization（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **The Benefits of Securitization（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **The Securitization Process（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Securitization（证券化）**：把资产池现金流重组为可交易证券的过程。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 17.1 | explain benefits of securitization for issuers, investors, economies, and financial markets | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 17.2 | describe securitization, including the parties and the roles they play | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
17. Fixed-Income Securitization
├─ 17.1 Introduction
│  ├─ 17.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 17.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 17.2 The Benefits of Securitization
│  ├─ 17.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 17.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 17.3 The Securitization Process
│  ├─ 17.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 17.3.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 17.1 Introduction

- **中文主线**：围绕 `Introduction` 掌握定义、适用条件、公式/框架和考试判断。
- **对应动作**：解释机制、原因和后果

### 17.2 The Benefits of Securitization

- **中文主线**：围绕 `The Benefits of Securitization` 掌握定义、适用条件、公式/框架和考试判断。
- **对应动作**：描述定义、流程和适用场景

### 17.3 The Securitization Process

- **中文主线**：围绕 `The Securitization Process` 掌握定义、适用条件、公式/框架和考试判断。
- **对应动作**：识别概念并应用到题干。

## 5. 关键公式与计算框架

### 5.1 M06-M09 定价、收益率与曲线

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Coupon Bond Price | `P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N` | `M06` | `y` 与 coupon frequency 必须同口径 |
| Full Price | `Full Price = Clean Price + Accrued Interest` | `M06` | invoice price 看 full |
| Accrued Interest | `AI = Coupon per period x Days since last coupon / Days in coupon period` | `M06` | day-count convention 题先读清 |
| Matrix Pricing Interpolation | `Interpolated yield = y_L + [(T - T_L)/(T_H - T_L)](y_H - y_L)` | `M06` | 【考纲重点】估计非流动债券 required yield |
| Current Yield | `Annual Coupon / Bond Price` | `M07` | 只看 coupon income |
| Yield to Maturity | `P = Σ CF_t/(1 + YTM/m)^t` | `M07` | YTM 是使价格等于现金流现值的 IRR |
| BEY from Periodic Yield | `BEY = periodic yield x number of periods per year` | `M07` | 债券等价收益率惯例 |
| Effective Annual Yield | `EAY = (1 + periodic rate)^m - 1` | `M07` | 年化 conversion 高频 |
| Government Benchmark Spread | `G-spread = YTM_bond - YTM_government benchmark` | `M07` | 【考纲重点】同期限或插值政府基准 |
| Interpolated Spread | `I-spread = YTM_bond - swap rate at same maturity` | `M07` | 若考纲/题目使用 swap curve |
| Zero-volatility Spread | `Z-spread = constant spread added to spot curve to price bond` | `M07` | 【扩展/谨慎】若题目只要求概念，不手算 |
| Discount Yield | `BDY = (FV - P)/FV x 360/t` | `M08` | 分母是 face value |
| Money Market Yield | `MMY = (FV - P)/P x 360/t` | `M08` | 分母换成 purchase price |
| Bond Equivalent Yield | `BEY = (FV - P)/P x 365/t` | `M08` | 与 MMY 的 day basis 区分 |
| Add-on Rate | `(FV - P)/P x 365/t` or stated day-count | `M08` | 以 purchase price 为分母，读题确认 360/365 |
| Quoted Margin | `Coupon rate = Reference rate + Quoted margin` | `M08` | FRN coupon reset |
| Discount Margin | `Required margin that prices FRN at current market price` | `M08` | 【考纲重点】概念判断多于手算 |
| Spot Pricing | `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t` | `M09` | 每笔 cash flow 用匹配 spot |
| Discount Factor | `DF_t = 1/(1+s_t)^t` | `M09` | spot pricing 前置 |
| Forward from Spot | `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^{n-m}` | `M09` | 先对齐区间长度 |
| Par Rate | `Par rate = (1 - DF_N)/Σ_{t=1}^{N} DF_t` | `M09` | discount factor 版最稳 |

### 5.2 M10-M12 回报与利率风险

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Holding Period Return | `HPR = (Coupon income + reinvestment income + sale price - purchase price)/purchase price` | `M10` | return source 要拆开 |
| Macaulay Duration | `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price` | `M10` | cash-flow time weighted average |
| Modified Duration | `D_mod = D_mac/(1+y/m)` | `M11` | fixed cash-flow % price sensitivity |
| Money Duration | `Money Duration = D_mod x Full Price` | `M11` | 货币价格变化基础 |
| PVBP | `PVBP = (P_- - P_+)/2` or `≈ Money Duration x 0.0001` | `M11` | 1 bp shock |
| Duration Price Approx | `%ΔP ≈ -D_mod x Δy` | `M11` | 一阶近似 |
| Convexity | `Convexity = [P_- + P_+ - 2P_0] / (P_0 x (Δy)^2)` | `M11` | 价格重估版常见 |
| Convexity Adjusted Change | `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2` | `M11` | 注意 `Δy` 用小数 |
| Portfolio Duration | `D_p = Σ w_i D_i` | `M11` | 价值权重，曲线非平行时有限 |
| Effective Duration | `EffDur = (P_- - P_+) / (2P_0Δy)` | `M12` | 【考纲重点】现金流可能随利率变化时 |
| Effective Convexity | `EffCon = (P_- + P_+ - 2P_0)/(P_0(Δy)^2)` | `M12` | option-aware convexity |
| Key Rate Duration | `KRD_k = -(1/P)(ΔP/Δy_k)` | `M12` | 非平行曲线移动 |

### 5.3 M13-M19 信用与证券化

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Expected Credit Loss Intuition | `ECL ≈ PD x LGD x Exposure` | `M10` | Level I 重点在三因子方向 |
| Loss Given Default | `LGD = 1 - Recovery Rate` | `M10` | recovery 越高，LGD 越低 |
| Interest Coverage | `EBIT / Interest Expense` 或 `EBITDA / Interest Expense` | `M11` | 看题目指定 numerator |
| Debt to EBITDA | `Total Debt / EBITDA` | `M11` | leverage 越高通常信用越弱 |
| Senior Claim Recovery Logic | `Higher priority -> higher expected recovery` | `M11` | 排名不是公式但常决定答案 |
| Taxable Equivalent Yield | `Tax-exempt yield / (1 - tax rate)` | `M05` | 市政债应税等价收益率 |
| TIPS Adjusted Principal | `Original Principal x (Current CPI / Base CPI)` | `M05` | 通胀挂钩债券 |
| CPR from SMM | `CPR = 1 - (1 - SMM)^12` | `M18` | MBS 提前还款速度 |
| SMM from CPR | `SMM = 1 - (1 - CPR)^(1/12)` | `M18` | CPR/SMM 互转 |
| CMBS DSCR | `NOI / Debt Service` | `M19` | 商业抵押贷款覆盖率 |
| CMBS LTV | `Loan Amount / Property Value` | `M19` | 抵押贷款杠杆 |
| Debt Yield | `NOI / Loan Amount` | `M19` | CMBS 信用品质，不依赖 cap rate |

### 5.4 考纲范围标记

| 标记 | 内容 |
|------|------|
| 【考纲重点】 | Bond price/full-clean/accrued interest、yield/spread/money-market measures、spot/par/forward curves、duration/convexity/effective/key-rate measures、credit metrics、MBS/CMBS core ratios |
| 【考纲内但无核心公式】 | Instrument features、issuance/trading, corporate/government market structure, securitization parties, covenant/seniority concepts |
| 【超纲/扩展】 | OAS 完整模型、结构化产品现金流 waterfall 建模、复杂 prepayment model、信用迁移矩阵定价不作为 Level I 必背公式 |

---

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 17.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 17.2 The Benefits of Securitization | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 17.3 The Securitization Process | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

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

- **上游模块**：[[M16-Credit-Analysis-for-Corporate-Issuers]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M18-Asset-Backed-Security-Instrument-and-Market-Features]]。本模块输出会被后续更复杂题型调用。

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

- **主要 legacy 来源**：`00-Fixed-Income-MOC.md` (high, 0.45)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
