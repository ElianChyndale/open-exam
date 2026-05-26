---
title: "M05 — Analyzing Statements of Cash Flows II"
description: "CFA Level I 2026 official module: Analyzing Statements of Cash Flows II"
module: M05
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 5: Analyzing Statements of Cash Flows II"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M05: Analyzing Statements of Cash Flows II

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Analyzing Statements of Cash Flows II
- 5.01 | Introduction
- 5.02 | Evaluating Sources and Uses of Cash
- 5.03 | Ratios and Common-Size Analysis
- 5.04 | Free Cash Flow Measures
- 5.05 | Cash Flow Statement Analysis: Cash Flow Ratios

## Learning Outcome Statements

The candidate should be able to:

- analyze and interpret both reported and common-size cash flow statements
- calculate and interpret free cash flow to the firm, free cash flow to equity, and performance and coverage cash flow ratios

## Local Study Notes

### Migrated from `CFA_tier1/Financial_Statement_Analysis/M04-Cash-Flow-Statements.md`

_Alignment score: 0.45. Original official module field: M4: Analyzing Statements of Cash Flows I / M5: Analyzing Statements of Cash Flows II._

#### M04: 现金流量表分析 (Cash Flow Statement Analysis)

##### 1. 核心知识点

###### 4.1 三大报表联动 (Three-Statement Linkage)

- **现金流量表连接利润表与资产负债表变动 (Cash Flow Statement Links Income Statement to Balance Sheet Changes)**：现金的增减变化源于利润表中的经营活动以及资产负债表项目的变动
- **CFO/CFI/CFF 分类现金变动来源 (CFO / CFI / CFF Classify the Source of Cash Movement)**：经营活动现金流(CFO)、投资活动现金流(CFI)、融资活动现金流(CFF)三大分类反映企业现金循环的不同侧面
- 三表联动的核心逻辑：净利润 + 非现金调整 + 营运资本变动 = CFO；资产负债科目的跨期变化体现在现金流量表的各个分类中

###### 4.2 直接法与间接法编制 (Direct vs Indirect Preparation)

**间接法 (Indirect Method)：**
- 从净利润出发，调整非现金项目(noncash charges)和营运资本变动(working capital changes)
- 非现金项目加回：折旧(depreciation)、摊销(amortization)、减值损失(impairment losses)
- 营运资本调整：应收账款增加减少现金，应付账款增加增加现金

**直接法 (Direct Method)：**
- 直接列示现金收入(cash collected from customers)和现金支出(cash paid to suppliers, employees, etc.)
- IFRS 鼓励直接法，US GAAP 两种均可但在实务中间接法更常见
- 注意：NI-to-CFO 桥接是调节表(reconciliation)，而非现金流量的定义

####### 核心公式 (English)
- `CFO = NI + Noncash Charges - Noncash Gains/Losses +/- WC Changes`
- `FCFF = CFO + Interest(1 - T) - FCInv`
- `FCFE = CFO - FCInv + Net Borrowing`

**从利润表和资产负债表数据计算现金流 (Compute Cash Flows from Income Statement and Balance Sheet Data)：**
- 通过应收账款的变动来推算现金收款：现金收款 = 收入 - 应收账款增加额
- 通过应付账款的变动来推算现金付款：现金付款 = 费用 + 应付账款减少额

**将间接法 CFO 转换为直接法 (Convert Indirect CFO to Direct Method)：**
- 逐项将应计制(accrual basis)下的收入和费用调整为收付实现制(cash basis)
- 需要利润表项目和对应资产负债表科目的期初期末余额

###### 4.3 IFRS vs US GAAP 现金流分类差异 (Cash Flow Classification)

- 利息支付(interest paid)：IFRS 可选经营或融资；US GAAP 要求归于经营
- 股利支付(dividends paid)：IFRS 可选经营或融资；US GAAP 归于融资
- 利息和股利收入(interest and dividends received)：IFRS 可选经营或投资；US GAAP 归于经营
- 银行透支(bank overdrafts)：IFRS 可视为现金等价物的一部分；US GAAP 通常归类为融资

###### 4.4 分析产出 (Analysis Outputs)

- **报告式 vs 同比例现金流量表 (Reported vs Common-Size Cash Flow Statements)**：同比例分析可将各项目表示为收入或总现金流的百分比
- **FCFF 与 FCFE (FCFF and FCFE)**：公司自由现金流(FCFF)衡量公司对所有资本提供者的现金流；股权自由现金流(FCFE)衡量对股东的可供现金流
- **业绩与覆盖现金流比率 (Performance and Coverage Cash Flow Ratios)**：如经营现金流比率(CFO / Current Liabilities)、现金流覆盖比率(cash flow coverage ratio)

##### 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| CFO (间接法) | `NI + Depreciation/Amortization - Gains/Losses +/- WC Changes` | 核心现金流公式 |
| FCFF | `CFO + Interest(1 - T) - FCInv` | 公司自由现金流 |
| FCFE | `CFO - FCInv + Net Borrowing` | 股权自由现金流 |
| CFO / CL | `CFO / Current Liabilities` | 经营现金流比率，衡量短期偿债能力 |

##### 3. 常见考点与解题思路

- **考点1**：间接法下 CFO 的计算。解题思路：从 NI 出发，加回非现金费用，调整营运资本变动（资产增加为现金流出、负债增加为现金流入）
- **考点2**：FCFF/FCFE 的计算与区别。解题思路：FCFF 给所有资本提供者，FCFE 只给股东；两者关系为 FCFF - Interest(1-T) + Net Borrowing = FCFE
- **考点3**：IFRS vs US GAAP 分类差异。解题思路：记住利息和股利的分类差异，注意 IFRS 更灵活
- **考点4**：直接法编制。解题思路：利用利润表项目和对应资产负债科目的期初期末余额倒推现金收付

##### 4. 易错点提醒

- **非现金项目的双向调整**: 不仅要加回费用(折旧)，还要减去非现金收益(如资产出售利得)
- **营运资本变动的符号**: 流动资产增加(用现金)是减项，流动负债增加(收到现金)是加项——方向最易出错
- **FCFF vs FCFE**: 计算 FCFF 时加回税后利息，FCFE 不再加回——很多考生在调整细节上丢分
- **NI 到 CFO 桥接**: 这是调节表(reconciliation)而非现金流量定义——直接法和间接法的 CFO 金额应当相同

##### 5. 跨模块关联

- [[M02-Income-Statement|利润表分析]]：净利润(NI)是间接法编制现金流量的起点，非现金费用来源于利润表
- [[M03-Balance-Sheet|资产负债表]]：资产负债科目的变动(应收账款、存货、应付账款)是计算 CFO 的关键调整项
- [[M10-Financial-Analysis-Techniques|财务分析技术]]：现金流比率(CFO ratios)是偿债能力和盈利质量分析的重要工具

### Migrated from `CFA_tier1/Financial_Statement_Analysis/M05-Analyzing-Cash-Flows-II.md`

_Alignment score: 0.61. Original official module field: M5: Analyzing Statements of Cash Flows II._

#### M05: 现金流量表分析 II (Analyzing Statements of Cash Flows II)

##### 1. 核心知识点

###### 5.1 报告式与同比例现金流量表 (Reported vs Common-Size Cash Flow Statements)

- **报告式现金流量表 (Reported Cash Flow Statement)**：按 CFO、CFI、CFF 三大分类列示现金收支，反映企业现金的实际来源与运用
- **同比例现金流量表 (Common-Size Cash Flow Statement)**：可将各项目表示为收入(revenue)或总现金流入/流出的百分比，便于跨期和跨公司比较
- 同比例分析有助于识别现金流结构的异常变化，如经营现金流占比持续下降可能是盈利质量恶化的信号

###### 5.2 自由现金流 (Free Cash Flow)

**公司自由现金流 (FCFF — Free Cash Flow to the Firm)：**
- 定义：衡量公司对所有资本提供者（股东和债权人）的可供现金流
- 特点：在满足经营和投资需求后，可供分配给所有资本提供者的剩余现金流
- 用途：企业价值评估(DCF 模型)的输入变量

**股权自由现金流 (FCFE — Free Cash Flow to Equity)：**
- 定义：衡量公司对普通股股东的可供现金流
- 特点：在满足经营、投资和偿债需求后，可供分配给股东的剩余现金流
- 用途：股权价值评估的输入变量

####### 核心公式 (English)
- `FCFF = CFO + Interest(1 - T) - FCInv`
- `FCFE = CFO - FCInv + Net Borrowing`

###### 5.3 现金流比率分析 (Cash Flow Ratio Analysis)

**业绩现金流比率 (Performance Cash Flow Ratios)：**
- 经营现金流比率 (CFO / Current Liabilities)：衡量经营现金流覆盖短期债务的能力
- 现金流覆盖比率 (Cash Flow Coverage Ratio)：衡量经营现金流覆盖总债务的能力
- 现金流利润率 (Cash Flow Margin)：CFO / Revenue，衡量每单位收入转化为经营现金流的效率

**覆盖现金流比率 (Coverage Cash Flow Ratios)：**
- 债务覆盖比率 (Debt Coverage Ratio)：CFO / Total Debt
- 利息覆盖比率 (Cash Interest Coverage)：(CFO + Interest Paid + Taxes Paid) / Interest Paid

**现金流趋势分析 (Cash Flow Trend Analysis)：**
- 多期 CFO 趋势：CFO 增长应与利润增长趋势基本一致，显著背离可能暗示盈利质量下降
- CFO 与 NI 的关系：CFO > NI 通常意味着盈利质量较高；CFO 持续低于 NI 可能反映激进的收入确认或营运资本恶化
- 自由现金流趋势：FCFF/FCFE 长期为负可能表明公司需要外部融资

##### 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| FCFF | `CFO + Interest(1 - T) - FCInv` | 公司自由现金流 |
| FCFE | `CFO - FCInv + Net Borrowing` | 股权自由现金流 |
| CFO / CL | `CFO / Current Liabilities` | 经营现金流比率，衡量短期偿债能力 |

##### 3. 常见考点与解题思路

- **考点1**：FCFF/FCFE 的计算与区别。解题思路：FCFF 给所有资本提供者，FCFE 只给股东；两者关系为 FCFF - Interest(1-T) + Net Borrowing = FCFE
- **考点2**：现金流比率的计算与解读。解题思路：CFO 比率衡量的是现金流层面的偿债能力，比利润层面的比率更真实
- **考点3**：同比例现金流量表分析。解题思路：关注各分类现金流的占比趋势，尤其注意经营现金流占比的持续变化
- **考点4**：现金流与盈利质量的判断。解题思路：CFO 与 NI 的长期背离是盈利质量分析的重要线索

##### 4. 易错点提醒

- **FCFF vs FCFE 的调整差异**: 计算 FCFF 时加回税后利息，FCFE 不再加回——很多考生在调整细节上丢分
- **FCInv (资本支出) 的扣减**: 计算 FCFF 和 FCFE 时都需扣减 FCInv，这是维持经营所必需的现金支出
- **Net Borrowing 的方向**: 净借款为正(新增借款)增加 FCFE，为负(偿还借款)减少 FCFE
- **现金流比率 vs 利润比率**: 现金流比率基于已实现现金，不易被会计政策操纵，但波动性可能更大

##### 5. 跨模块关联

- [[M04-Analyzing-Cash-Flows-I|现金流量表分析 I]]：FCFF/FCFE 的计算以 CFO 为基础，需先掌握间接法编制
- [[M11-Financial-Analysis-Techniques|财务分析技术]]：现金流比率是偿债能力和盈利质量分析的重要工具，与 DuPont 分析互为补充
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
