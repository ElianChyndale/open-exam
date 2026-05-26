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

### 🌳 核心知识树

```text
🏆 FSA M09: Analysis of Income Taxes（所得税分析）
│
├── ⭐ 会计利润 vs 应税所得
│   ├── 应付税款 = 应税所得 × 法定税率（实际缴税）
│   ├── 所得税费用 = 会计利润调整（财报确认费用）
│   └── 两者差异 → 递延所得税
│
├── ⭐ 暂时性差异 (Temporary Differences)
│   ├── 账面价值与计税基础不同时产生
│   ├── 未来会转回 → 产生 DTA 或 DTL
│   ├── 折旧方法差异 → DTL
│   └── ⚠️ 永久性差异不影响 DTA/DTL
│
├── ⭐ DTL（递延所得税负债）
│   ├── 会计利润 > 应税所得 → 当期少交税，未来多交税
│   ├── 📐 DTL = 应纳税暂差 × 未来税率
│   └── 常见: 加速折旧、收入分期确认
│
├── ⭐ DTA（递延所得税资产）
│   ├── 会计利润 < 应税所得 → 当期多交税，未来少交税
│   ├── 📐 DTA = 可抵扣暂差 × 未来税率
│   ├── 常见: 保修费用、坏账准备、经营亏损结转
│   └── ⚠️ 估价备抵: 若未来无足够应税收入需计提
│
├── ⭐ 三种税率
│   ├── 📐 有效税率 = Income Tax Expense / Pretax Income
│   ├── 📐 法定税率: 企业法定税率
│   ├── 📐 现金税率 = Cash Taxes Paid / Pretax Income
│   └── 三者差异分析: 永久性差异 → 有效≠法定；DTL 转回 → 现金<有效
│
├── ⭐ 税务披露与调节
│   ├── 有效税率与法定税率调节表
│   ├── 调节项目: 永久性差异、税率变动、估价备抵变动
│   └── 分析师关注: 税率趋势异常、波动巨大、估价备抵突变
│
├── 💡 关键洞察
│   ├── DTL = 未来多交税（现在享受了税收优惠）
│   ├── 折旧: 税法加速 → 前期少税 → DTL
│   ├── 估价备计提具有很大管理层判断空间
│   └── 永久性差异影响有效税率但不产生 DTA/DTL
│
└── ⚠️ 考试陷阱总结
    ├── DTL 方向: 未来多交税，不是额外税收优惠
    ├── 永久性差异不影响递延税
    ├── 估价备抵增加 = DTA 减少 = 所得税费用增加
    └── 税率变动时 DTA/DTL 需按新税率重计量
```

## 📖 知识点详解

### 知识点1：会计利润 vs 应税所得（Accounting Profit vs Taxable Income）

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

### 知识点2：递延所得税资产与负债（Deferred Tax Assets and Liabilities）

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

### 知识点3：有效/法定/现金税率（Effective / Statutory / Cash Tax Rates）

- **有效税率 (Effective Tax Rate)** = `Income Tax Expense / Pretax Income`——财报中呈现的实际税率
- **法定税率 (Statutory Tax Rate)** = 公司所在司法管辖区的企业法定税率——用于计算所得税费用的基准
- **现金税率 (Cash Tax Rate)** = `Cash Taxes Paid / Pretax Income`——实际现金缴税率

三者差异的分析意义：有效税率与法定税率的差异提示永久性差异的存在；现金税率低于有效税率可能说明大量 DTL 转回或存在税务优惠

### 知识点4：税务披露与有效税率调节（Tax Disclosures and Effective-Rate Reconciliation）

- 公司需要提供有效税率与法定税率的调节表(reconciliation)
- 调节项目包括：永久性差异、不同税率辖区的影响、税率变动、DTA 估价备抵变动
- 分析师应关注：有效税率趋势异常、税率波动巨大、DTA 估价备抵的突然变动

### 📐 关键公式表

| 指标 | 公式 | 说明 |
|------|------|------|
| DTL (当期) | `Taxable Temporary Difference x Future Tax Rate` | 递延所得税负债 |
| DTA (当期) | `Deductible Temporary Difference x Future Tax Rate` | 递延所得税资产 |
| Effective Tax Rate | `Income Tax Expense / Pretax Income` | 有效税率 |
| Cash Tax Rate | `Cash Taxes Paid / Pretax Income` | 现金税率 |
| Income Tax Expense | `Taxes Payable + DTL Increase - DTA Increase` | 所得税费用构成 |

### 🛠️ 常见考点与解题思路

**考点1：判断交易产生 DTA 还是 DTL**
- 会计提前确认费用 → DTA（未来可抵扣）
- 会计提前确认收入 → DTL（未来应纳税）

**考点2：有效税率计算和调节**
- 从法定税率出发，逐项加减永久性差异的影响。

**考点3：DTA 估价备抵的变化影响**
- 估价备抵增加 = DTA 减少 = 当期所得税费用增加。

**考点4：跨期差异对现金流的影响**
- 应付税款影响现金流，而非所得税费用。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| DTL 是额外税收优惠 | DTL 意味着未来要多交税 |
| 永久性差异影响递延税 | 永久性差异不影响 DTA/DTL |
| 估价备抵无关紧要 | 估价备抵计提具有很大管理层判断空间 |
| 所有差异都产生递延税 | 永久性差异不产生 DTA/DTL |

### 🔄 跨模块关联

- [[M02-Analyzing-Income-Statements]]：所得税费用影响净利润
- [[M03-Analyzing-Balance-Sheets]]：DTA 和 DTL 列示在资产负债方
- [[M04-Analyzing-Statements-of-Cash-Flows-I]]：应付税款是 CFO 组成部分
- [[M07-Analysis-of-Long-Term-Assets]]：资产账面价值与计税基础差异是 DTL 来源
- [[M11-Financial-Analysis-Techniques]]：有效税率分析是盈利质量评估维度

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.

## 📋 复习与刷题提示

- **核心公式**：DTL = 应纳税暂差 × 税率；DTA = 可抵扣暂差 × 税率
- **高频陷阱**：永久性差异不影响DTA/DTL；⚠️ DTL≠欠税
- **跨科目**：递延税→Corp M06 WACC计算中的税盾；有效税率→Equity M08 FCF估值
- **IFRS vs US GAAP差异**：IFRS下DTA/DTL分类为流动资产/非流动；US GAAP同样分类但另有valuation allowance规则

### 跨科目学习链接
- **Corporate Issuers M06**: MM 定理中的税盾（tD）直接源于本模块的递延税概念
- **Equity M08**: FCFE 计算中的净借款和税后利息依赖本模块的税务处理
- **Fixed Income M14-M16**: 信用分析中的税前/税后 ICR 计算需要理解税务影响
- CF方向提示：经营租赁利息的税务处理与资本化租赁不同，需区分账面vs税务处理
- 永久性差异经典案例：政府罚款、国债利息收入、商誉减值（IFRS下不可转回）
- 反例学习：某分析师给风险承受低的客户推荐高风险产品→违反III(C) Suitability，根本原因在于未进行充分KYC
- 时间差异示例：加速折旧产生DTL（账面折旧<税务折旧），保修费用产生DTA（账面计提>税务扣除）

### 💡 记忆技巧
- DTL（递延税负债）= 会计利润>税务利润 → 未来多交税
- DTA（递延税资产）= 会计利润<税务利润 → 未来少交税

### 🔢 计算示例速查

| 项目 | 会计处理 | 税务处理 | 差异类型 | DTA/DTL |
|------|----------|----------|----------|---------|
| 加速折旧 | 直线折旧 | 加速折旧 | 暂时性 | DTL（前期） |
| 保修费用 | 计提时确认 | 实际发生时扣除 | 暂时性 | DTA |
| 坏账准备 | 计提时确认 | 实际核销时扣除 | 暂时性 | DTA |
| 国债利息 | 确认收入 | 免税 | 永久性 | 无 |
| 政府罚款 | 确认费用 | 不可扣除 | 永久性 | 无 |

> **考试陷阱提示**：永久性差异不影响递延税项，仅影响有效税率。遇到永久性差异选项时，立即排除DTA/DTL变化选项。

### 🧠 IFRS vs US GAAP 关键差异

1. **DTA/DTL分类**：IFRS下DTA/DTL通常列为非流动；US GAAP按相关资产负债的流动性分类
2. **估价备抵(Valuation Allowance)**：IFRS下DTA需评估可收回性并作减值（减记可转回）；US GAAP同样设valuation allowance但标准略有不同
3. **未分配利润的递延税**：IFRS要求确认子公司未分配利润的递延税（除非满足控制条件）；US GAAP不要求确认（indefinite reversal criterion）

### 📎 综合案例分析要点

- 税率变动时：DTA/DTL需按**新税率**重新计量，差额计入**当期损益**
- 企业合并中：DTA/DTL的确认影响**商誉(goodwill)**计算
- 经营亏损结转(Operating Loss Carryforward)：产生DTA —— 若有valuation allowance，说明管理层认为未来盈利不确定性高
