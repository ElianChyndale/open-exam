---
title: "M15 — Credit Analysis for Government Issuers"
description: "CFA Level I 2026 official module: Credit Analysis for Government Issuers"
module: M15
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 15: Credit Analysis for Government Issuers"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M15: Credit Analysis for Government Issuers

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Credit Analysis for Government Issuers
- 15.01 | Introduction
- 15.02 | Sovereign Credit Analysis
- 15.03 | Non-Sovereign Credit Risk

## Learning Outcome Statements

The candidate should be able to:

- explain special considerations when evaluating the credit of sovereign and non-sovereign government debt issuers and issues

## Local Study Notes

### Migrated from `CFA_tier1/Fixed_Income/M11-Government-and-Corporate-Credit.md`

_Alignment score: 0.54. Original official module field: Module 15: Credit Analysis for Government Issuers, Module 16: Credit Analysis for Corporate Issuers._

#### M14: 政府与公司信用分析 (Government and Corporate Credit Analysis)

##### 1. 核心知识点

###### 1.1 政府发行人 (Government Issuers)

- **货币主权、财政灵活性、外部头寸、政治风险 (monetary sovereignty, fiscal flexibility, external position, political risk)**：主权信用的评估维度：能否自主印钞（货币主权）、财政赤字和债务水平（财政灵活性）、外汇储备和贸易平衡（外部头寸）、治理稳定性和政策连续性（政治风险）。
- **主权与非主权发行人的支持假设不同 (sovereign and non-sovereign issuers do not share identical support assumptions)**：地方政府、市政债等非主权发行人的信用分析需要额外考虑上级政府的支持意愿和能力，不自动等同于主权信用。

###### 1.2 公司发行人 (Corporate Issuers)

- **商业风险 + 财务风险 + 治理结构 (business risk + financial risk + governance/structure)**：公司信用分析的三支柱。商业风险考察行业特征和竞争地位；财务风险考察杠杆、覆盖率和现金流；治理结构考察管理层、所有权结构和关联交易。
- **杠杆率、覆盖率、现金流稳定性、再融资渠道 (leverage, coverage, cash-flow stability, refinancing access)**：核心定量指标：Debt/EBITDA（杠杆率），EBITDA/Interest（利息覆盖率），自由现金流（稳定性），以及银行信贷额度和资本市场融资能力（再融资渠道）。
- **担保 vs 无担保；优先 vs 次级；破产优先级 (secured vs unsecured; senior vs subordinated; bankruptcy priority)**：担保债务以特定资产作为抵押品；优先级债务在破产时比次级债务优先受偿。同一发行人的不同债项可能有不同评级。

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 利息覆盖率 (ICR) | `ICR = EBIT / Interest Expense` 或 `EBITDA / Interest Expense` |
| 杠杆率 | `Debt / EBITDA` |
| 债务资本比 | `Total Debt / (Total Debt + Total Equity)` |
| 自由现金流 | `FCF = CFO - CapEx - 优先股股息` |
| 回收率预期 | 优先级担保 > 优先级无担保 > 次级 |

##### 3. 常见考点与解题思路

- **计算和解读覆盖率**：ICR 越低，信用风险越高。注意题目是否使用 EBIT 还是 EBITDA。
- **区分 issuer rating 与 issue rating**：同一发行人的不同债项可能因担保品和优先级不同而有不同评级。
- **主权信用分析框架**：从货币主权、财政灵活性、外部头寸、政治风险四个维度评估。每个维度下有哪些关键指标。
- **区分 secured 与 unsecured、senior 与 subordinated**：破产清算时，secured creditors 优先于 unsecured，senior 优先于 subordinated。

##### 4. 易错点提醒

- **发行人评级与债项评级在抵押品和清偿顺序不同时可能不同 (issuer rating and issue rating can differ when collateral and ranking differ)**：发行人评级反映整体偿债能力，但具体债项因担保、优先级、契约条款等因素，评级可能更高或更低。
- **Sovereign ceiling 不是绝对的**：传统上认为境内的公司评级不可能高于主权评级，但在某些情况下（如公司有大量海外收入和资产）可能存在例外。
- **ICR 使用 EBIT 还是 EBITDA 影响大**：EBITDA 通常大于 EBIT，因此 EBITDA-based ICR 更高。题目没有明确时，留意上下文提示。
- **Notching（评级差异化）** ：同一发行人的不同债项之间评级相差的级数（notch），主要取决于优先级、担保品和结构支持。

##### 5. 跨模块关联

- 公司信用分析 → [[M10-Credit-Risk]] 的 PD/LGD 框架
- 担保品与优先级 → [[M01-Instrument-Features]] 的合同要素
- 发行人与债项评级 → [[M13-ABS-and-Credit-Enhancement]] 的结构化信用增级
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
