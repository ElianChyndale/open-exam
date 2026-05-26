---
title: "M09 — Analysis of Income Taxes"
description: "CFA Level I 2026 official module: Analysis of Income Taxes"
module: M09
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 9: Analysis of Income Taxes"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M09: Analysis of Income Taxes

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Analysis of Income Taxes
- 9.01 | Introduction
- 9.02 | Differences between Accounting Profit and Taxable Income
- 9.03 | Deferred Tax Assets and Liabilities
- 9.04 | Corporate Income Tax Rates
- 9.05 | Presentation and Disclosure

## Learning Outcome Statements

The candidate should be able to:

- contrast accounting profit, taxable income, taxes payable, and income tax expense and temporary versus permanent differences between accounting profit and taxable income
- explain how deferred tax liabilities and assets are created and the factors that determine how a company’s deferred tax liabilities and assets should be treated for the purposes of financial analysis
- calculate, interpret, and contrast an issuer’s effective tax rate, statutory tax rate, and cash tax rate
- analyze disclosures relating to deferred tax items and the effective tax rate reconciliation and explain how information included in these disclosures affects a company’s financial statements and financial ratios

## Local Study Notes

### Migrated from `CFA_tier1/Financial_Statement_Analysis/M08-Income-Taxes.md`

_Alignment score: 0.53. Original official module field: M9: Analysis of Income Taxes._

#### M09: 所得税分析 (Income Taxes Analysis)

##### 1. 核心知识点

###### 9.1 会计利润 vs 应税所得 (Accounting Profit vs Taxable Income)

- **应付税款 vs 所得税费用 (Taxes Payable vs Income Tax Expense)**：
  - 应付税款(taxes payable) = 应税所得(taxable income) x 法定税率，是实际应缴给税务局的金额
  - 所得税费用(income tax expense) = 会计利润(accounting profit) x 法定税率基础上的调整，是财报中确认的费用
  - 两者的差异源于会计准则与税法规则的不同——这就产生了递延所得税

- **暂时性差异 (Temporary Differences)**：
  - 当资产或负债的账面价值(carrying amount)与计税基础(tax base)不同时产生
  - 预期在未来转回(reversal)，产生 DTA 或 DTL
  - 常见来源：折旧方法差异、收入确认时点差异、准备金的税前扣除差异
  - 例子：税法加速折旧(accelerated depreciation)导致前期计税基础低于账面价值 → 产生 DTL

- **永久性差异 (Permanent Differences)**：
  - 不会在未来期间转回，因此不影响递延所得税
  - 常见来源：罚款(fines and penalties)、某些免税收入(tax-exempt income)
  - 影响有效税率(effective tax rate)但不产生 DTA/DTL

###### 9.2 递延所得税资产与负债 (Deferred Tax Assets and Liabilities)

**递延所得税负债 (Deferred Tax Liability, DTL)：**
- 产生原因：会计利润 > 应税所得（当期少交税，未来多交税）
- 常见场景：固定资产加速折旧、收入分期确认

**递延所得税资产 (Deferred Tax Asset, DTA)：**
- 产生原因：会计利润 < 应税所得（当期多交税，未来少交税）
- 常见场景：保修费用(warranty expense)计提、坏账准备(bad debt provision)、经营亏损结转(operating loss carryforward)
- DTA 的估价备抵(valuation allowance)：若未来很可能没有足够应税收入实现 DTA，需计提估价备抵

**分类与列报：**
- IFRS：DTA/DTL 通常分类为非流动(non-current)
- US GAAP：按相关资产/负债的分类确定流动性
- DTA/DTL 不能简单以净额列示(netting)，需满足特定条件

###### 9.3 有效/法定/现金税率 (Effective / Statutory / Cash Tax Rates)

- **有效税率 (Effective Tax Rate)** = `Income Tax Expense / Pretax Income`——财报中呈现的实际税率
- **法定税率 (Statutory Tax Rate)** = 公司所在司法管辖区的企业法定税率——用于计算所得税费用的基准
- **现金税率 (Cash Tax Rate)** = `Cash Taxes Paid / Pretax Income`——实际现金缴税率

三者差异的分析意义：有效税率与法定税率的差异提示永久性差异的存在；现金税率低于有效税率可能说明大量 DTL 转回或存在税务优惠

###### 9.4 税务披露与有效税率调节 (Tax Disclosures and Effective-Rate Reconciliation)

- 公司需要提供有效税率与法定税率的调节表(reconciliation)
- 调节项目包括：永久性差异、不同税率辖区的影响、税率变动、DTA 估价备抵变动
- 分析师应关注：有效税率趋势异常、税率波动巨大、DTA 估价备抵的突然变动

##### 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| DTL (当期) | `Taxable Temporary Difference x Future Tax Rate` | 递延所得税负债 |
| DTA (当期) | `Deductible Temporary Difference x Future Tax Rate` | 递延所得税资产 |
| Effective Tax Rate | `Income Tax Expense / Pretax Income` | 有效税率 |
| Cash Tax Rate | `Cash Taxes Paid / Pretax Income` | 现金税率 |
| Income Tax Expense | `Taxes Payable + DTL Increase - DTA Increase` | 所得税费用构成 |

##### 3. 常见考点与解题思路

- **考点1**：判断交易产生 DTA 还是 DTL。解题思路：比较会计处理与税务处理的时间差异——会计提前确认费用则产生 DTA（未来可抵扣），会计提前确认收入则产生 DTL（未来应纳税）
- **考点2**：有效税率计算和调节。解题思路：从法定税率出发，逐项加减永久性差异的影响，得到有效税率
- **考点3**：DTA 估价备抵的变化影响。解题思路：估价备抵增加 = DTA 减少 = 当期所得税费用增加
- **考点4**：跨期差异对现金流的影响。解题思路：应付税款（实际缴纳的税）影响现金流，而非所得税费用

##### 4. 易错点提醒

- **DTA/DTL 的方向**: 这是最常见的混淆点——DTL 意味着"未来要多交税"(现在享受了税收优惠)，而不是相反
- **折旧方法差异**: 税法使用加速折旧(前期折旧高) → 应税所得低 → 当期少交税 → 但未来多交税 → 这是 DTL
- **估价备抵**: DTA 的实现取决于未来是否有足够的应税收入——估价备抵的计提具有很大管理层判断空间
- **永久性差异不影响递延税**: 永久性差异(如罚款)影响当期的有效税率，但不产生 DTA/DTL
- **税率变动**: 如果未来税率预期变动，DTA/DTL 需要按新税率重新计量，变动计入当期损益

##### 5. 跨模块关联

- [[M02-Income-Statement|利润表分析]]：所得税费用是利润表的重要组成部分，影响净利润
- [[M03-Balance-Sheet|资产负债表]]：DTA 和 DTL 分别列示在资产和负债方
- [[M04-Cash-Flow-Statements|现金流量表]]：应付税款(taxes paid)是 CFO 的重要组成部分
- [[M06-Long-Term-Assets|长期资产]]：资产的账面价值与计税基础差异是 DTL 的主要来源之一
- [[M10-Financial-Analysis-Techniques|财务分析技术]]：有效税率分析是盈利质量评估的重要维度
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
