---
title: "M08 — Topics in Long-Term Liabilities and Equity"
description: "CFA Level I 2026 official module: Topics in Long-Term Liabilities and Equity"
module: M08
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 8: Topics in Long-Term Liabilities and Equity"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M08: Topics in Long-Term Liabilities and Equity

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Topics in Long-Term Liabilities and Equity
- 8.01 | Introduction
- 8.02 | Leases
- 8.03 | Financial Reporting for Postemployment and Share-Based Compensation Plans
- 8.04 | Presentation and Disclosure

## Learning Outcome Statements

The candidate should be able to:

- explain the financial reporting of leases from the perspectives of lessors and lessees
- explain the financial reporting of defined contribution, defined benefit, and stock-based compensation plans
- describe the financial statement presentation of and disclosures relating to long-term liabilities and share-based compensation

## Local Study Notes

### Migrated from `CFA_tier1/Financial_Statement_Analysis/M07-Long-Term-Liabilities-and-Equity.md`

_Alignment score: 0.47. Original official module field: M8: Topics in Long-Term Liabilities and Equity._

#### M08: 长期负债与权益分析 (Long-Term Liabilities and Equity Analysis)

##### 1. 核心知识点

###### 8.1 租赁会计：出租人与承租人 (Lease Reporting: Lessor vs Lessee)

**承租人会计 (Lessee Accounting)：**
- US GAAP (ASC 842) / IFRS 16：两类租赁均要求承租人在资产负债表确认使用权资产(right-of-use asset)和租赁负债(lease liability)
- 融资租赁(finance lease)：承租人同时确认折旧费用(depreciation expense)和利息费用(interest expense)，总费用前期更高
- 经营租赁(operating lease)：承租人确认单一租赁费用(straight-line lease expense)
- 对利润表的影响：融资租赁前期费用更高、后期费用更低；经营租赁费用在各期相对均匀

**出租人会计 (Lessor Accounting)：**
- 融资租赁(finance/sales-type lease) vs 经营租赁(operating lease)
- 出租人分类取决于所有权风险报酬是否转移给承租人
- 销售型租赁(sales-type lease)在租赁开始日确认销售利润

###### 8.2 确定缴费 vs 确定给付计划 (Defined Contribution vs Defined Benefit Plans)

**确定缴费计划 (Defined Contribution Plan)：**
- 雇主按固定比例缴费(contribution)，员工承担投资风险(investment risk)
- 会计处理简单：当期缴费确认为费用，无后续养老金负债(pension liability)

**确定给付计划 (Defined Benefit Plan)：**
- 雇主义务按预定公式支付退休福利，雇主承担投资风险和精算风险(actuarial risk)
- 关键概念：养老金负债(PBO, projected benefit obligation)、计划资产公允价值(fair value of plan assets)、净养老金融资状况(net pension funded status)
- 定期养老金成本(periodic pension cost)包括服务成本(service cost)、利息成本(interest cost)、计划资产预期回报(expected return on plan assets)

**分析注意事项：**
- DB 计划对财务报表的影响复杂，分析师需关注精算假设(actuarial assumptions)（折现率、工资增长率、死亡率）的变化
- 计划资产与 PBO 之间的缺口(gap)即净负债或净资产

###### 8.3 股权激励薪酬 (Stock-Based Compensation)

- 员工期权(employee stock options, ESOs)和限制性股票(restricted stock units, RSUs)
- 确认原则：按授予日公允价值(fair value at grant date)确认薪酬费用(compensation expense)，在服务期(vesting period)内分摊
- 对分析师的意义：期权费用降低报告利润，但不会减少现金流；稀释(dilution)影响 EPS 计算
- 注意：股权激励费用是 non-cash charge，在间接法 CFO 中应加回

**【考试陷阱】** 负债/权益列报方式的选择(liability/equity presentation choices)会改变杠杆解读(leverage reading)——例如优先股的分类直接影响 debt-to-equity 比率的计算。

##### 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| Lease Liability (期初) | `Present Value of Lease Payments` | 租赁负债初始计量 |
| Right-of-Use Asset (期初) | `Lease Liability + Initial Direct Costs + Prepayments - Incentives` | 使用权资产初始计量 |
| Funded Status | `Fair Value of Plan Assets - PBO` | 养老金融资状况，正值=资产，负值=负债 |
| Periodic Pension Cost | `Service Cost + Interest Cost - Expected Return on Plan Assets` | 定期养老金成本 |
| Compensation Expense | `Fair Value of Option at Grant Date / Vesting Period` | 股权激励费用 |

##### 3. 常见考点与解题思路

- **考点1**：融资租赁 vs 经营租赁的报表影响对比。解题思路：两者区别在于费用的时间分布——融资租赁前期总费用高，经营租赁各期均匀
- **考点2**：DB 养老金计划的会计处理。解题思路：理解 PBO 和计划资产的关系，掌握 funded status 的计算
- **考点3**：股权激励对 EPS 的影响。解题思路：确认费用降低净利润 → 基本 EPS 下降；期权行权增加股数 → 稀释 EPS 进一步下降
- **考点4**：负债 vs 权益分类对比率的影响。解题思路：优先股分类为负债时增加杠杆，分类为权益时不影响杠杆

##### 4. 易错点提醒

- **使用权资产也是资产**: 经营租赁上表后，资产负债表同时确认资产和负债，导致 asset turnover 和 ROA 恶化
- **养老金假设是分析重点**: 折现率(discount rate)每变动 1% 会显著改变 PBO 和定期养老金成本——管理层可能通过假设操纵利润
- **期权费用非现金**: 尽管期权费用降低报告利润，但它是非现金费用(non-cash expense)，不影响 CFO
- **DB vs DC 的核心区别**: DB 由雇主承担投资和长寿风险(longevity risk)，DC 由员工承担——这个本质差异决定了会计处理的复杂性

##### 5. 跨模块关联

- [[M03-Balance-Sheet|资产负债表]]：租赁负债和养老金负债是非流动负债的重要组成部分
- [[M02-Income-Statement|利润表分析]]：融资租赁前期的利息和折旧费用影响利润；养老金成本影响营业利润
- [[M04-Cash-Flow-Statements|现金流量表]]：租赁付款和养老金缴费归类于融资或经营活动现金流，取决于具体安排
- [[M10-Financial-Analysis-Techniques|财务分析技术]]：租赁和养老金义务影响 solvency 比率的计算和解释
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
