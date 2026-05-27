---
title: "00-Financial Statement Analysis-MOC"
description: "CFA Level I 2026 Financial Statement Analysis 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Financial Statement Analysis"
topic_area: "Financial_Statement_Analysis"
level: CFA Level I
exam_year: 2026
exam_weight: "11-14%"
module_count: 12
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Financial_Statement_Analysis
---

# Financial Statement Analysis MOC

> **一句话核心 One-line core**: FSA converts accounting reports into comparable, forecastable, and challengeable business evidence.

## 1. Subject Brief 科目定位

Financial Statement Analysis 是 CFA Level I 中连接会计、估值、信用、组合与职业判断的证据科目。考试权重为 **11-14%**，不是单纯背会计规则，而是要求你判断某个会计选择如何改变 income statement, balance sheet, cash flow statement, ratios, quality of earnings, and forecast drivers.

本学科的答题顺序固定为三步：

1. **Identify the reporting object 识别报表对象**: revenue, expense, asset, liability, tax, lease, inventory, cash flow, ratio, or forecast driver.
2. **Translate accounting into analysis 把会计处理翻成分析影响**: NI, CFO, assets, liabilities, equity, margins, turnover, leverage, ROA/ROE, FCFF/FCFE.
3. **Question quality 质疑质量**: sustainability, comparability, classification choices, nonrecurring items, estimates, disclosures, and manipulation warning signs.

## 2. Formula & Framework Map 公式与框架地图

### 2.1 Income Statement 收入、费用与 EPS

| Cluster | Must Know | Exam Move |
|---|---|---|
| Revenue recognition five-step model | identify contract -> identify performance obligations -> determine transaction price -> allocate price -> recognize revenue when/as obligations are satisfied | 看到 long-term contract, multiple deliverables, variable consideration，先问 revenue timing and amount |
| Expense matching/capitalization | match expenses with related revenue; capitalize when future economic benefits are expected | Capitalize -> current expense lower, NI/assets/equity higher, future depreciation/amortization higher |
| Capitalization of interest/development cost | capitalize eligible interest or development cost when criteria are met | 比较 firms 时调整 expense timing, asset base, margins, ROA |
| Non-recurring items | unusual/infrequent items, discontinued operations, accounting policy changes, changes in scope/FX | Normalize earnings; distinguish persistent operating performance from one-off noise |
| Basic EPS | `(Net income - preferred dividends) / weighted-average common shares` | 注意 preferred dividends and weighted average shares |
| Diluted EPS | adjust numerator and denominator for dilutive convertibles/options/warrants | If-converted for convertibles; treasury stock method for options/warrants |
| Antidilutive securities | exclude securities that increase EPS or reduce loss per share | Diluted EPS cannot be higher than basic EPS |
| Common-size income statement | each line item / revenue | Margin diagnosis: gross, operating, pretax, net |

### 2.2 Balance Sheet 资产、负债与权益

| Cluster | Must Know | Exam Move |
|---|---|---|
| Intangibles | purchased intangibles capitalized; internally generated usually expensed except qualifying development under IFRS | 先分 purchased / internally developed / business combination |
| Goodwill | recognized only in business combinations; tested for impairment, not amortized | Goodwill impairment reduces assets, equity, NI; no reversal under US GAAP/IFRS for goodwill |
| Financial instruments | measurement depends on classification and standard; fair value changes may affect profit or equity | 题目问 ratio impact 时先定位 measurement basis and where gain/loss flows |
| Non-current liabilities | debt, leases, deferred tax liabilities, pensions/share-based compensation | Translate liability recognition into leverage, coverage, and future cash claims |
| Common-size balance sheet | each line item / total assets | 资产结构、融资结构、working capital intensity |

### 2.3 Cash Flow 现金流

| Cluster | Must Know | Exam Move |
|---|---|---|
| Direct CFO | cash collected from customers - cash paid to suppliers/employees/other operating items - cash taxes/interest if classified operating | Use balance sheet changes to convert accruals into cash |
| Indirect CFO | net income + noncash charges - gains + losses +/- working capital changes | Inventory/AR increase usually subtract; AP increase usually add |
| Indirect to direct conversion | derive cash collected, cash paid, cash taxes, cash interest from accrual lines and balance sheet changes | Do not mix revenue/expense signs with asset/liability change signs |
| IFRS vs US GAAP classification | interest/dividends paid/received classification flexibility differs; US GAAP is stricter | Classification changes CFO/CFI/CFF, not total cash flow |
| FCFF | `NI + NCC + Int(1 - tax rate) - FCInv - WCInv` or `CFO + Int(1 - tax rate) - FCInv` | Cash available to all capital providers |
| FCFE | `CFO - FCInv + net borrowing` | Cash available to common equity holders |
| Cash flow ratios | CFO / revenue, CFO / average assets, CFO / debt, cash interest coverage, cash reinvestment | Quality check: CFO should support earnings and debt service |

### 2.4 Inventories and Long-Term Assets 存货与长期资产

| Cluster | Must Know | Exam Move |
|---|---|---|
| Inventory methods | FIFO, weighted average; LIFO may appear in US GAAP contexts | In rising prices, FIFO COGS lower and ending inventory higher than LIFO |
| Inventory write-downs | lower of cost and NRV; reversals allowed under IFRS, prohibited under US GAAP for inventory | Write-down reduces inventory, NI, equity; affects gross margin and turnover |
| Inventory ratios | inventory turnover = COGS / average inventory; DOH = 365 / turnover | Rising DOH can signal obsolete inventory or demand weakness |
| Depreciation | straight-line, accelerated, units-of-production | Higher depreciation lowers NI/assets/equity, can raise future ROA if asset base falls |
| Impairment | carrying value exceeds recoverable amount/fair value rules | Impairment reduces assets, NI, equity; ignore tax unless stated |
| Derecognition | gain/loss on sale = proceeds - carrying amount | Remove asset and accumulated depreciation; classify cash proceeds as investing |

### 2.5 Leases, Taxes, Quality, Ratios, Modeling 租赁、税、质量、比率、建模

| Cluster | Must Know | Exam Move |
|---|---|---|
| Leases | lessee recognizes right-of-use asset and lease liability; classification affects expense pattern and cash flow labels | Add lease obligations to leverage analysis; separate accounting expense from cash payment |
| Deferred taxes | taxable temporary difference -> DTL; deductible temporary difference -> DTA | DTL often future tax payment; DTA depends on realizability |
| Tax rates | effective tax rate = income tax expense / pretax income; cash tax rate = taxes paid / pretax income | Reconcile statutory vs effective vs cash; isolate permanent vs temporary differences |
| Reporting quality | reporting quality vs quality of results; conservative vs aggressive accounting; GAAP departures | Look for incentives, opportunities, weak controls, non-GAAP presentation, estimates |
| Ratio analysis | activity, liquidity, solvency, profitability, DuPont | Always interpret trend, peer, business model, accounting policy, and industry context |
| DuPont | ROE = net profit margin x asset turnover x financial leverage | Determine whether ROE change comes from margin, efficiency, or leverage |
| Modeling drivers | sales growth, price/volume, COGS, SG&A, tax, capex, depreciation, working capital, shares | Sales-based model: forecast operating drivers first, then statements link |

## 3. Module Atlas 模块地图

| Module | Official Module | Role in FSA System |
|---|---|---|
| [[M01-Introduction-to-Financial-Statement-Analysis|M01]] | Introduction to Financial Statement Analysis | 分析框架、信息来源、监管文件、审计与管理层讨论 |
| [[M02-Analyzing-Income-Statements|M02]] | Analyzing Income Statements | 收入确认、费用确认、非经常项目、EPS、利润表比率 |
| [[M03-Analyzing-Balance-Sheets|M03]] | Analyzing Balance Sheets | 无形资产、商誉、金融工具、非流动负债、资产负债表比率 |
| [[M04-Analyzing-Statements-of-Cash-Flows-I|M04]] | Analyzing Statements of Cash Flows I | 三表联动、直接法/间接法 CFO、IFRS vs US GAAP 分类 |
| [[M05-Analyzing-Statements-of-Cash-Flows-II|M05]] | Analyzing Statements of Cash Flows II | 现金来源用途、common-size cash flow、FCFF/FCFE、现金流比率 |
| [[M06-Analysis-of-Inventories|M06]] | Analysis of Inventories | 存货计量、通胀/通缩、披露、存货周转与 DOH |
| [[M07-Analysis-of-Long-Term-Assets|M07]] | Analysis of Long-Term Assets | 无形资产来源、长期资产减值、终止确认、披露分析 |
| [[M08-Topics-in-Long-Term-Liabilities-and-Equity|M08]] | Topics in Long-Term Liabilities and Equity | 租赁、养老金、股份支付、长期负债与权益披露 |
| [[M09-Analysis-of-Income-Taxes|M09]] | Analysis of Income Taxes | 税会差异、DTA/DTL、税率调节、披露分析 |
| [[M10-Financial-Reporting-Quality|M10]] | Financial Reporting Quality | 报告质量、盈余质量、操纵动机、会计估计、预警信号 |
| [[M11-Financial-Analysis-Techniques|M11]] | Financial Analysis Techniques | 比率体系、common-size/trend/cross-sectional analysis、DuPont、预测 |
| [[M12-Introduction-to-Financial-Statement-Modeling|M12]] | Introduction to Financial Statement Modeling | 销售驱动模型、预测偏差、竞争因素、通胀/通缩、预测期 |

## 4. Curriculum Spine 教材主线

官方教材主线不是按“报表名称”孤立展开，而是从证据收集到预测建模逐层加深：

1. **M01 Evidence setup**: purpose, context, data collection, regulated filings, notes, MD&A, audit reports, other information.
2. **M02-M05 Three-statement engine**: income statement accruals -> balance sheet recognition -> cash flow conversion -> free cash flow and cash quality.
3. **M06-M09 Accounting policy impact**: inventories, long-term assets, leases/compensation/equity, and income taxes create comparability and ratio traps.
4. **M10 Quality overlay**: reported numbers are not automatically high-quality; evaluate incentives, estimates, presentation choices, and warning signs.
5. **M11-M12 Analysis to forecast**: convert ratios and disclosures into driver-based forecasts and valuation inputs.

Use the textbook index as section anchors: every module page now absorbs official textbook signals into `Curriculum Spine` rather than keeping a separate mechanical source-list block.

## 5. Exam Routes 做题路线

| Route | When To Use | Steps |
|---|---|---|
| Accounting effect route | 题目问 policy choice or accounting treatment impact | Identify account -> adjust NI/assets/liabilities/equity/CFO -> translate ratio effect |
| Ratio route | 题目给 financial statements or ratio table | Classify ratio -> compute if required -> compare trend/peer -> explain driver |
| Cash flow route | 题目给 accrual data and balance sheet changes | Decide direct/indirect method -> apply sign discipline -> check CFO/CFI/CFF classification |
| Quality route | 题目描述 management behavior, estimates, or non-GAAP measures | Separate GAAP compliance from reporting quality -> identify warning sign -> state analyst response |
| Forecast route | 题目问 pro forma or modeling | Start with sales/volume/price -> forecast operating costs, capex, working capital, taxes -> link statements |

Exam default: if a question asks for interpretation, do not stop at formula output. State whether the metric improved or worsened, why, and whether the change is sustainable.

## 6. Practice & Mock Evidence Map 题库证据地图

| Evidence Source | How To Use |
|---|---|
| End-of-reading questions for M01-M12 | 用来验证每个 module 的 LOS 是否能落到动作；错题必须回填 module `Practice & Mock Evidence` |
| Mock item sets / standalone FSA questions | 按 route 标记：accounting effect, ratio, cash flow, quality, forecast |
| `.system/events/question/` | 原始错题证据源；不要直接从记忆总结推断高频错因 |
| `.system/memory/question-errors/` | 单题错因卡；记录 formula miss, sign error, classification error, interpretation gap |
| `.system/memory/patterns/` | 同一 topic + LOS + error_type 至少 3 次后升级为 pattern |
| `.system/memory/strategy/moc-gap-review.md` | 如果 repeated mistake 带有 `moc_target`，先生成 MOC gap review，再决定是否补 MOC |

Evidence tagging suggestion:

- `FSA-M02-revenue-recognition`
- `FSA-M04-direct-indirect-CFO`
- `FSA-M05-FCFF-FCFE`
- `FSA-M06-inventory-inflation`
- `FSA-M09-DTA-DTL`
- `FSA-M10-reporting-quality`
- `FSA-M11-DuPont-ratio`
- `FSA-M12-model-driver`

## 7. Review Routes 复习路线

1. **Fast pass 90 minutes**: MOC formula map -> M02 EPS/revenue -> M04 CFO -> M05 FCFF/FCFE -> M11 ratios.
2. **Accounting policy pass**: M06 inventory -> M07 long-term assets -> M08 leases/pensions/share-based comp -> M09 taxes.
3. **Quality pass**: M10 warning signs plus M02 non-recurring items, M04/M05 cash quality, M11 ratio limitations.
4. **Mock repair pass**: collect wrong questions -> classify into question/bias/agent layer -> mine patterns -> only then update strategy.
5. **Final recall pass**: recite five-step revenue model, EPS dilution rules, direct/indirect CFO signs, FCFF/FCFE, inventory inflation effects, DTA/DTL logic, DuPont.

## 8. Cross-Subject Interfaces 跨科目接口

| Interface | FSA Contribution |
|---|---|
| Equity | Normalized earnings, ROE drivers, free cash flow, pro forma forecasts feed valuation models |
| Fixed Income | Leverage, coverage, cash flow stability, lease liabilities, deferred taxes affect credit risk |
| Corporate Issuers | Capital structure, working capital, capex, payout, and financial policy decisions rely on FSA metrics |
| Quantitative Methods | Trend, cross-sectional comparison, regression, and forecasting require ratio interpretation discipline |
| Portfolio Management | Security selection and portfolio monitoring use accounting quality and fundamental drivers |
| Ethics | Analyst must distinguish facts, estimates, opinions, and disclosure limitations when communicating recommendations |
