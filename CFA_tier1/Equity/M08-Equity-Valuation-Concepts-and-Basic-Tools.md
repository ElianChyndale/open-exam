---
title: "M08 — Equity Valuation: Concepts and Basic Tools"
description: "CFA Level I 2026 official module: Equity Valuation: Concepts and Basic Tools"
module: M08
subject: "Equity Investments"
topic_area: Equity
curriculum_year: 2026
official_module: "Module 8: Equity Valuation: Concepts and Basic Tools"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Equity
  - official_2026
---

# M08: Equity Valuation: Concepts and Basic Tools

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Equity Valuation: Concepts and Basic Tools
- 8.01 | Introduction
- 8.02 | Estimated Value and Market Price
- 8.03 | Categories of Equity Valuation Models
- 8.04 | Background for the Dividend Discount Model
- 8.05 | Dividend Discount Model (DDM) and Free-Cash-Flow-to-Equity Model (FCFE)
- 8.06 | Preferred Stock Valuation
- 8.07 | The Gordon Growth Model
- 8.08 | Multistage Dividend Discount Models
- 8.09 | Multipler Models and Relationship Among Price Multiples, Present Value Models, and Fundamentals
- 8.10 | Method of Comparables and Valuation Based on Price Multiples
- 8.11 | Enterprise Value
- 8.12 | Asset-Based Valuation
- 8.13 | Summary

## Learning Outcome Statements

The candidate should be able to:

- evaluate whether a security, given its current market price and a value estimate, is overvalued, fairly valued, or undervalued by the market
- describe major categories of equity valuation models
- describe regular cash dividends, extra dividends, stock dividends, stock splits, reverse stock splits, and share repurchases
- describe dividend payment chronology
- explain the rationale for using present value models to value equity and describe the dividend discount and free-cash-flow-to-equity models
- explain advantages and disadvantages of each category of valuation model
- calculate the intrinsic value of a non-callable, non-convertible preferred stock
- calculate and interpret the intrinsic value of an equity security based on the Gordon (constant) growth dividend discount model or a two-stage dividend discount model, as appropriate
- identify characteristics of companies for which the constant growth or a multistage dividend discount model is appropriate
- explain the rationale for using price multiples to value equity, how the price to earnings multiple relates to fundamentals, and the use of multiples based on comparables
- calculate and interpret the following multiples: price to earnings, price to an estimate of operating cash flow, price to sales, and price to book value
- describe enterprise value multiples and their use in estimating equity value
- describe asset-based valuation models and their use in estimating equity value

## Local Study Notes

### Migrated from `CFA_tier1/Equity/M08-Equity-Valuation-Concepts.md`

_Alignment score: 1.00. Original official module field: Module 8: Equity Valuation: Concepts and Basic Tools._

#### M08: 权益估值概念与工具 (Equity Valuation Concepts and Tools)

##### 1. 核心知识点

###### 内在价值 (Intrinsic value)
- **现值逻辑 (present value logic)**：资产价值 = 未来现金流按**必要收益率 (required return)** 折现
- **戈登增长模型 (Gordon Growth Model, GGM)**：适用于**稳定永续股息增长 (stable perpetual dividend growth)** 的公司
- **合理倍数 (justified multiples)**：将**基本面 (fundamentals)** 与价格比率联系起来 — 如合理市盈率 = `Payout Ratio / (r - g)`

###### 相对估值 (Relative valuation)
- **常用倍数**：**市盈率 (P/E)**、**市净率 (P/B)**、**市销率 (P/S)**、**市现率 (P/CF)**、**企业价值/EBITDA (EV/EBITDA)**
- **领先 vs trailing 分母**：**领先 (forward)** 使用预期盈利，**trailing** 使用历史盈利 — 周期性与会计可比性影响选择
- **估值信号检验**：低倍数可能是真便宜（价值股）、也可能是合理的（高风险/低增长）、或两者兼有 — 必须对照**增长 (growth)**、**风险 (risk)**、**质量 (quality)** 三重检验

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 戈登增长模型 (GGM) | `P_0 = D_1 / (r - g)`，必须 `r > g` |
| 隐含必要收益率 | `r = D_1 / P_0 + g` |
| 隐含增长率 | `g = r - D_1/P_0` |
| 可持续增长率 | `g = Retention Ratio × ROE` |
| 合理领先市盈率 (Justified Leading P/E) | `P_0 / E_1 = Payout Ratio / (r - g)` |
| 合理 trailing 市盈率 | `P_0 / E_0 = Payout Ratio(1 + g) / (r - g)` |
| 合理市净率 (Justified P/B) | `P_0/B_0 = (ROE - g)/(r - g)` |
| 合理市销率 (Justified P/S) | `P_0/S_0 = Net Profit Margin × P_0/E_0` |
| 企业价值 (EV) | `Equity + Debt + Preferred + Minority Interest - Cash` |
| P/B 市净率 | `Price per Share / BVPS` |
| P/S 市销率 | `Price per Share / Sales per Share` |
| P/CF 市现率 | `Price per Share / Cash Flow per Share` |
| EV/EBITDA | `Enterprise Value / EBITDA` |

**考纲标记**：
- 【考纲重点】GGM、implied return/growth、sustainable growth、justified P/E/P/B/P/S、EV/EBITDA。
- 【考纲内但无核心公式】估值模型选择、可比公司筛选、估值信号解释。
- 【超纲/扩展】多阶段 DDM、FCFF/FCFE 完整估值、残余收益模型不作为 Level I 必背公式。

##### 3. 常见考点与解题思路

- **GGM 计算**：先确认 r > g → 代入 `D_1/(r-g)` → 检查答案合理性
- **justified P/E 推导**：从 GGM 变形得到 — 理解 payout ratio、r、g 如何影响倍数
- **相对估值步骤**：选同类可比公司 → 计算行业平均倍数 → 对比目标公司 → 调整增长/风险差异

##### 4. 易错点提醒

- **低市盈率可能是真便宜，也可能是应得的，或两者兼有**【考试陷阱】
- **DDM 不适用于所有公司**：股息政策不稳定的公司（如高增长不分红公司）不适合
- **高增长不一定等于高价值**：还要看必要收益率和可持续性
- **EV/EBITDA 并非总是优于 P/E**：只是适用场景不同 — EBITDA 为正但盈利为负的公司更适用
- **trailing 与 forward 倍数不可直接比较**：口径不同，预期也不同

##### 5. 跨模块关联

- **估值依赖盈利预测** → [[M07-Company-Analysis-Forecasting]]
- **公司质量与竞争优势支撑估值倍数** → [[M05-Company-Analysis-Past-and-Present]]
- **行业特征影响估值参数选择** → [[M06-Industry-and-Competitive-Analysis]]
- **指数作为估值比较基准** → [[M02-Security-Market-Indexes]]
### 🌳 核心知识树

```text
🏆 M08: Equity Valuation: Concepts and Basic Tools（权益估值概念与工具）
│
├── ⭐ 价值基础 (Value Foundations)
│   ├── Intrinsic Value vs Market Price
│   │   ├── IV > MP → Undervalued → Buy
│   │   ├── IV < MP → Overvalued → Sell/Sell Short
│   │   └── IV = MP → Fairly Valued → Hold
│   ├── Required Return (r): CAPM-based, opportunity cost
│   └── 📐 Present Value Logic: Asset Value = Σ CFₜ / (1+r)ᵗ
│
├── ⭐ 现值模型 (Present Value Models) 🎯高频
│   ├── DDM (Dividend Discount Model)
│   │   ├── 单期: V₀ = D₁/(1+r) + P₁/(1+r)
│   │   ├── 📐 GGM: V₀ = D₁/(r-g), 要求 r > g ⚠️
│   │   └── 两阶段 DDM: 高增长期 + 永续期
│   ├── FCFE Model: 替代DDM用于不分红公司
│   └── Preferred Stock: V₀ = D/r（永续年金）
│
├── ⭐ 乘数模型 (Multiplier Models) 🎯高频
│   ├── P/E: Justified Leading = Payout/(r-g)
│   ├── P/B: Justified = (ROE-g)/(r-g)
│   ├── P/S: Justified = Net Margin × P/E
│   ├── P/CF: Price / Cash Flow per Share
│   └── 📐 EV/EBITDA: Enterprise Value / EBITDA 🎯高频
│
├── ⭐ 企业价值 (Enterprise Value) 🎯高频
│   └── EV = Market Cap + Debt + Preferred + Minority Interest - Cash
│       ⚠️ 注意：EV反映整个公司的价值，包括债权人
│
├── ⭐ 资产基础估值 (Asset-Based Valuation)
│   └── V₀ = Fair Value of Assets - Fair Value of Liabilities
│       ⚠️ 适用于金融、自然资源公司，不适用于轻资产科技公司
│
├── ⭐ 可比公司分析 (Method of Comparables)
│   ├── 选可比公司 → 算行业平均倍数 → 对比目标公司
│   └── ⚠️ 需调整增长、风险、质量差异
│
└── 📐 核心参数关系
    ├── g (可持续增长率) = Retention Ratio × ROE
    ├── r (隐含收益率) = D₁/P₀ + g
    └── Payout Ratio = 1 - Retention Ratio
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `V₀ = D₁ / (r - g)` | GGM：永续增长DDM | 稳定派息、稳定增长的公司 | 必须 r > g；g 不能超过长期GDP增速 |
| `r = D₁/P₀ + g` | 隐含必要收益率 | 已知股价和增长率时反推要求回报率 | 结果对 g 高度敏感 |
| `g = Retention Ratio × ROE` | 可持续增长率 | 预测公司长期增长能力 | 假设ROE和派息率不变 |
| `g = b × ROE` | 同上（b为留存比率） | 计算再投资能支撑的增长 | 若ROE变化，g也会变 |
| `Justified Leading P/E = Payout / (r - g)` | 合理领先市盈率 | 估值是否合理的基本面检验 | payout ratio须可持续 |
| `Justified Trailing P/E = Payout(1+g) / (r - g)` | 合理 trailing 市盈率 | 用历史盈利检验估值 | trailing含已实现盈利 |
| `Justified P/B = (ROE - g) / (r - g)` | 合理市净率 | 银行/保险等重资产公司估值 | ROE须反映未来盈利能力 |
| `Justified P/S = Net Profit Margin × P₀/E₀` | 合理市销率 | 盈利为负的公司（成长型） | 利润率须可持续 |
| `EV = Market Cap + Debt + Pfd + MI - Cash` | 企业价值 | 跨资本结构公司比较 | 现金须从EV中扣除 |
| `EV/EBITDA` | 企业价值/EBITDA | 资本密集行业比较 | EBITDA不能替代FCF |
| `P₀ = D/(1+r) + P₁/(1+r)` | 单期DDM | 已知下期股息和股价 | 简单但很少单期使用 |
| `V₀(preferred) = D/r_p` | 优先股估值（永续年金） | 不可赎回、不可转换优先股 | 假设股息持续永续 |

### 🛠️ 常见考点与解题思路

**Topic 1: GGM基本计算**
- 确认 r > g（否则公式不成立）
- 确认 D₁（下期预期股息）已经给出或可从D₀×(1+g)算出
- 代入 V₀ = D₁/(r-g)
- 与当前市价比较判断估值状态

**Topic 2: 隐含参数反推**
- 已知价格求隐含r：r = D₁/P₀ + g
- 已知价格求隐含g：g = r - D₁/P₀
- 解题关键：先确定哪些是已知，哪些是未知

**Topic 3: Justified Multiples计算**
- Justified P/E: P₀/E₁ = Payout/(r-g)，先算payout ratio
- Justified P/B: P₀/B₀ = (ROE-g)/(r-g)，检验ROE是否可持续
- 解题关键：将基本面指标与市场倍数对比判断低估/高估

**Topic 4: 两阶段DDM**
- 第一阶段：逐年折现高增长期股息
- 第二阶段：GGM计算终值并折现
- 加总两阶段现值

**Topic 5: EV/EBITDA应用**
- 先计算EV = Market Cap + Debt + Preferred + MI - Cash
- 再计算EV/EBITDA ratio
- 与可比公司对比：低值可能被低估

**Topic 6: 资产基础估值**
- 资产负债表调整：账面值→公允价值
- 识别表外资产和负债
- 适用于：金融、自然资源、控股公司
- 不适用于：轻资产、无形资产密集型公司

**Topic 7: 估值模型选择逻辑**
- 稳定派息 → DDM/GGM
- 不分红但有FCF → FCFE模型
- 有可比公司 → 乘数法
- 资产重 → 资产基础法
- 并购场景 → EV/EBITDA

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| g > r时GGM仍可用 | g > r时GGM失效（V₀为负值或无意义） | GGM数学前提是r > g |
| DDM适用于所有公司 | DDM只适用于稳定派息的公司 | 不分红或派息波动大的公司不能用DDM |
| 低P/E一定被低估 | 低P/E可能反映高风险或低增长 | 需对照Justified P/E检验 |
| EV/EBITDA永远比P/E好 | 不同场景不同工具 | EBITDA为正但盈利为负时EV/EBITDA更适用 |
| Trailing P/E和Forward P/E可直接比 | 口径不同不可直接比较 | Trailing用历史盈利，Forward用预期盈利 |
| 高增长=高价值 | 高增长需高r补偿，价值取决于(r-g)之差 | 增长需盈利质量支撑 |
| 账面价值等于市场价值 | 账面价值是历史成本，与市场价值差异大 | 尤其无形资产多的公司 |
| Justified P/E是精确值 | 是估计值，对假设敏感 | 改变g或r假设会大幅改变结果 |
| 股息收益率高 = 好投资 | 高股息收益率可能来自股价下跌 | 高股息未必可持续 |
| 两阶段DDM第一阶段增长率必须是常数 | 通常假设常数，但考试也可能给每年不同增长率 | 逐年代入计算即可 |

### 🔄 跨模块关联

- **估值依赖盈利预测输入** → [[M07-Company-Analysis-Forecasting]]（增长率和现金流预测）
- **公司质量影响估值倍数** → [[M05-Company-Analysis-Past-and-Present]]（ROE、利润率分析）
- **行业特征决定估值参数选择** → [[M06-Industry-and-Competitive-Analysis]]（生命周期的估值含义）
- **指数作为估值比较基准** → [[M02-Security-Market-Indexes]]（行业平均P/E对比）
- **市场效率影响估值方法可靠性** → [[M03-Market-Efficiency]]（有效市场中估值差异的持续性）
- **权益类型影响估值模型选择** → [[M04-Overview-of-Equity-Securities]]（普通股vs优先股）
- **交易成本影响套利活动** → [[M01-Market-Organization-and-Structure]]（估值偏差能否被套利纠正）
- **FCFE与公司资本结构关联** → [[M05-Company-Analysis-Past-and-Present]]
- **GGM中g的确定** → [[M07-Company-Analysis-Forecasting]]（可持续增长率与ROE×b的关系）

### 📋 复习与刷题提示

- **计算类题目必练**：GGM和Justified P/E是计算题最高频考点。建议掌握从V₀=D₁/(r-g)到反推r、g的变形
- **概念辨析重点**：trailing vs forward P/E、DDM vs FCFE使用条件、EV vs Market Cap的区别
- **两阶段DDM**：掌握分步折现逻辑，第一步折现高增长期的D₁...Dₙ，第二步折现终值（Terminal Value via GGM）
- **Justified Multiples逻辑链**：从GGM出发推导P/E、P/B、P/S，理解基本面变量如何影响倍数
- **FRM/CFA考试特点**：选择估值模型类型的题目出现频率高于纯计算
- **刷题建议**：mock exam中GGM计算、P/E对比、EV/EBITDA计算是必考组合
- **易混淆点专项练**：区分justified vs actual multiples；区分leading vs trailing P/E

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
