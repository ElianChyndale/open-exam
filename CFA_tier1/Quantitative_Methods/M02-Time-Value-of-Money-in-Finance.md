---
title: "M02 — Time Value of Money in Finance"
description: "CFA Level I 2026 official module: Time Value of Money in Finance"
module: M02
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 2: Time Value of Money in Finance"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M02: Time Value of Money in Finance

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Time Value of Money in Finance
- 2.01 | Introduction
- 2.02 | Time Value of Money in Fixed Income and Equity
- 2.03 | Implied Return and Growth
- 2.04 | Cash Flow Additivity

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret the present value (PV) of fixed-income and equity instruments based on expected future cash flows
- calculate and interpret the implied return of fixed-income instruments and required return and implied growth of equity instruments given the present value (PV) and cash flows
- explain the cash flow additivity principle, its importance for the no-arbitrage condition, and its use in calculating implied forward interest rates, forward exchange rates, and option values

## Local Study Notes

### Migrated from `CFA_tier1/Quantitative_Methods/M02-Time-Value-of-Money.md`

_Alignment score: 1.00. Original official module field: Module 2: Time Value of Money in Finance._

#### M02: Time Value of Money（货币时间价值）

##### 1. 核心知识点

###### 1.1 现金流时间轴（Cash-Flow Map）

TVM（Time Value of Money）的核心前提：**今天的 1 元钱比未来的 1 元钱更值钱**，因为今天的钱可以投资生息。

**核心关系（Core Relationship）**：
`FV = PV × (1 + r)^n`

- PV = 现值（Present Value）：今天投资的本金
- FV = 终值（Future Value）：未来某一时点的本利和
- r = 每期利率（Periodic Interest Rate）
- n = 期数（Number of Periods）

**四种基本现金流模式（Four Basic Cash Flow Patterns）**：

1. **单笔现金流（Single Sum）**：一笔资金，一个现值对应一个终值。最简单的 TVM 题型，直接代入公式。
2. **等额年金（Ordinary Annuity）**：每期末支付等额现金流。考试常见 — 如等额本息还款、固定票息债券。
3. **永续年金（Perpetuity）**：等额现金流无限持续。公式最简单：`PV = A / r`，但注意必须分子为第一个现金流。
4. **增长现金流（Growing Stream）**：现金流按固定增长率增长。增长率 g 低于折现率 r 时可用永续增长公式。

**先付年金（Annuity Due）vs 普通年金（Ordinary Annuity）**：
- 先付年金每期期初支付，普通年金每期期末支付
- 先付年金现值 = 普通年金现值 × (1 + r)
- 先付年金终值 = 普通年金终值 × (1 + r)

###### 1.2 工具现值应用（Instrument PV Applications）

TVM 最基本的应用就是将未来现金流折现。无论债券还是股票，估值工作的本质都是**把未来现金流折现到今天**：

- **固定收益（Fixed Income）**：债券价格 = 未来各期票息现值 + 到期本金现值
- **股权（Equity）**：股票内在价值 = 预期未来股利的现值（DDM）
- 实际考试中，先识别现金流的时点和模式，再选择合适的公式。

> **【考试陷阱】** 不要一上来就套公式 — 先画现金流时间轴，判断是单笔、年金还是混合模式。

###### 1.3 隐含变量求解（Implied Quantities）

已知部分变量（PV、FV、PMT 等），反求未知变量（r、n、A）：

**戈登增长模型（Gordon Growth Model）形式的隐含回报率**：
`r = D_1 / P_0 + g`
- 这是将 Perpetuity 与 TVM 结合的经典公式
- 常见于 Equity 和 Quant 交叉考点

**隐含求解方法论**：
- 债券：已知价格、票息、期限 → 反求到期收益率（YTM）
- 股权：已知价格、股利、增长率 → 反求要求回报率
- 贷款：已知贷款额、还款额、期数 → 反求隐含利率

###### 1.4 现金流可加性（Cash-Flow Additivity）

CFA 考试中一个重要但容易被忽视的原则：

**一个投资组合的现值 = 各组成部分现值的和**
- 这是套利定价逻辑的基础
- 意味着同一现金流不应因不同的"拆分方式"而得到不同的现值
- 为远期利率、远期汇率和期权定价提供直觉

> **【考试陷阱】** 考试会给你多个不同的现金流序列，要求你分别折现再加总，而不是直接套单一的年金公式。

##### 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `FV = PV(1+r)^n` | 终值公式 | 单笔投资未来价值 |
| `PV = FV/(1+r)^n` | 现值公式 | 未来单笔现金流的现值 |
| `PV_annuity = A[1-1/(1+r)^n]/r` | 普通年金现值 | 等额分期现金流的现值 |
| `PV_perpetuity = A/r` | 永续年金现值 | 永续等额现金流的现值 |
| `PV_annuity_due = PV_ordinary × (1+r)` | 先付年金现值 | 每期期初等额支付 |
| `PV_growing_perpetuity = A_1/(r-g)` | 永续增长年金现值 | 股利折现模型（DDM）基础 |
| `PV_growing_annuity = A_1/(r-g)[1-((1+g)/(1+r))^n]` | 增长年金现值 | 有限期增长现金流 |
| `r = D_1/P_0 + g` | 戈登增长模型 | 从股价反推要求回报率 |

##### 3. 常见考点与解题思路

**考点一：固定收益债券定价**
- 债券价格 = 票息年金现值 + 本金单笔现值
- 注意票息频率（半年付息时折半率、加倍期数）

**考点二：隐含利率反推**
- 给定贷款金额、月还款额和期数，计算隐含月利率和年化利率
- 用金融计算器或 TVM 公式的反向求解

**考点三：不同计息频率的比较**
- 给定 nominal annual rate 和 compounding frequency，计算 EAR
- `EAR = (1 + r_nominal / m)^m - 1`

**考点四：年金模式识别**
- 期初支付 → Annuity Due（每月 1 号交租）
- 期末支付 → Ordinary Annuity（月底发工资）
- 无限期 → Perpetuity（永续债）

##### 4. 易错点提醒

1. **Perpetuity 公式的分子一定要用第一期现金流**：`PV = A_1 / r` 而不是 A_0 / r
2. **增长年金/永续年金必须满足 r > g**：否则现值无穷大，经济上不合理
3. **先付年金 vs 后付年金**：后付年金多了一个"再乘 (1+r)"的步骤，考试常故意混淆
4. **计息频率和支付频率不一致**：必须先统一利率口径再做计算
5. **画时间轴**：最有效的纠错手段 — 把每个现金流标在时间轴上

##### 5. 跨模块关联

- **[[M01-Rates-and-Returns]]**：MWRR 本质就是 TVM 的 IRR 应用，"折现率"的概念从 M01 的利率解释延续而来。
- **[[M03-Statistical-Measures]]**：几何平均收益率与 TVM 中的复合增长概念相通 — geometric mean 就是平均每年复合增长率。
- **Fixed Income**：债券定价 = TVM 最直接的应用场景（票息年金 + 本金单笔现值）。
- **Equity**：戈登增长模型（Gordon Growth Model）是 TVM 在股利折现中的核心应用：
  `V_0 = D_1 / (r - g)`，本质就是永续增长年金的现值公式（分母有 r-g 而不是 r）。
- **Corporate Issuers**：资本预算中的 NPV、IRR、Payback Period 全部基于 TVM 框架。
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
