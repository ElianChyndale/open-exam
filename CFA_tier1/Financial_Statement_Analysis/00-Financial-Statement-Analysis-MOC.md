---
title: 00-Financial-Statement-Analysis-MOC
description: CFA Level I Financial Statement Analysis master MOC for statements, accounting effects, ratios, formulas, and traps.
subject: Financial Statement Analysis
topic_area: Financial_Statement_Analysis
level: CFA Level I
exam_weight: 11-14%
exam_format: 单选题
difficulty: 三表联动、会计政策方向与比率解释交织
note_type: master_moc
status: 学习中
aliases:
  - Financial Statement Analysis 知识框架
  - FRA MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Financial_Statement_Analysis
  - formulas
---

# 00-Financial-Statement-Analysis-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Financial Statement Analysis - Map of Content |
| description | CFA L1 财务分析科目学习导航：三张表、会计处理、现金流、存货、长期资产、税项、租赁、比率与财务建模 |
| subject | Financial Statement Analysis |
| 权重 | 11-14% |
| 考试形式 | 单选题，概念+计算+情境分析 |
| 难度特点 | 内容多、串联强，最容易在会计处理方向题和 ratio 解释题失分 |
| 学习建议 | 永远先回到三张表联动，再看具体会计政策如何改变利润、资产和现金流 |
| 状态 | 学习中 |
| tags | CFA L1, FRA, MOC |

---

## 最关键：先看交易怎么穿三表，再看会计政策怎样改结果

FRA 的关键不是背条文，而是把“交易→报表→比率→投资判断”连成一条线。

---

## 科目概览

| 模块 | 内容 | 难度 | 必考点 |
|------|------|------|--------|
| M01 | Analysis Framework | 概念 | sources of information, audit role |
| M02 | Income Statement | 概念+计算 | revenue recognition, EPS |
| M03 | Balance Sheet | 概念 | intangibles, liabilities, common-size |
| M04 | Cash Flow Statements I-II | 计算 | direct/indirect, classification, FCFF/FCFE |
| M05 | Inventory Analysis | 概念+计算 | lower of cost and NRV, FIFO/LIFO effects |
| M06 | Long-Term Assets | 概念+策略 | intangibles, impairment, derecognition |
| M07 | Long-Term Liabilities & Equity | 概念 | leases, pensions, stock-based compensation |
| M08 | Income Taxes | 概念+计算 | DTA/DTL, effective/statutory/cash tax rates |
| M09 | Financial Reporting Quality | 策略 | quality spectrum, warning signs, manipulation |
| M10 | Financial Analysis Techniques | 计算+解释 | ratios, DuPont, industry ratios |
| M11 | Financial Statement Modeling | 策略 | sales-based model, forecast horizon, bias |

---

## Financial Statement Analysis 核心知识树

```text
FRA (M01-M11)
│
├── M01: Analysis Framework
│   ├── 1.1 Framework steps【考试核心】↔ Topic Outline P10
│   │   ├── articulate purpose and context
│   │   ├── collect data / process data / analyze data
│   │   └── update conclusions and recommendations
│   ├── 1.2 Information hierarchy【考试核心】
│   │   ├── annual and interim statements
│   │   ├── regulatory filings, notes, supplementary information
│   │   ├── management commentary and audit reports
│   │   └── other analyst sources beyond reports
│   └── 1.3 Reporting systems【考试核心】
│       ├── standards differences alter comparability
│       └── 注意：附注与 reporting choices 常是答案来源【考试陷阱】
│
├── M02: Income Statement
│   ├── 2.1 Revenue recognition【考试核心】↔ Topic Outline P10-P11
│   │   ├── general recognition principles
│   │   ├── specific applications alter timing
│   │   └── timing choices affect margins and trend interpretation
│   ├── 2.2 Expense recognition【考试核心】
│   │   ├── matching logic
│   │   ├── capitalize vs expense
│   │   └── 注意：capitalization shifts expense timing, not economic reality【考试陷阱】
│   ├── 2.3 Unusual items and policy changes【考试核心】
│   │   ├── discontinued operations
│   │   ├── unusual / infrequent items
│   │   └── accounting policy changes
│   ├── 2.4 EPS【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `Basic EPS = (NI - Pref Div) / Weighted Avg Shares`
│   │   │   └── `Diluted EPS = Adjusted NI / Adjusted weighted shares`
│   │   ├── simple capital structure -> basic EPS
│   │   ├── complex capital structure -> diluted EPS
│   │   └── antidilutive securities excluded
│   └── 2.5 Common-size income statement and income-statement ratios【考试核心】
│
├── M03: Balance Sheet
│   ├── 3.1 Intangible assets【考试核心】↔ Topic Outline P11
│   │   ├── purchased vs internally generated
│   │   └── finite-life vs indefinite-life analysis implications
│   ├── 3.2 Goodwill【考试核心】
│   │   ├── acquisition residual
│   │   └── impairment risk
│   ├── 3.3 Financial instruments and non-current liabilities【考试核心】
│   └── 3.4 Common-size balance sheet and related ratios【考试核心】
│
├── M04: Cash Flow Statements I-II
│   ├── 4.1 Three-statement linkage【考试核心】↔ Topic Outline P11
│   │   ├── cash flow statement links income statement to balance sheet changes
│   │   └── CFO / CFI / CFF classify the source of cash movement
│   ├── 4.2 Direct vs indirect preparation【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `CFO = NI + Noncash Charges - Noncash Gains/Losses ± WC Changes`
│   │   │   ├── `FCFF = CFO + Interest(1-T) - FCInv`
│   │   │   └── `FCFE = CFO - FCInv + Net Borrowing`
│   │   ├── compute cash flows from income statement and balance sheet data
│   │   ├── convert indirect CFO to direct method
│   │   └── 注意：NI-to-CFO bridge is a reconciliation, not a definition【考试陷阱】
│   ├── 4.3 IFRS vs US GAAP cash flow classification【考试核心】
│   └── 4.4 Analysis outputs【考试核心】
│       ├── reported vs common-size cash flow statements
│       ├── FCFF and FCFE
│       └── performance and coverage cash flow ratios
│
├── M05: Inventory Analysis
│   ├── 5.1 Measurement basis【考试核心】↔ Topic Outline P11
│   │   ├── lower of cost and net realizable value
│   │   └── write-down implications for statements and ratios
│   ├── 5.2 Cost-flow methods【考试核心】
│   │   ├── FIFO / weighted average / LIFO comparison
│   │   ├── inflation vs deflation effects
│   │   └── 注意：inventory method changes COGS, taxes, margins, inventory balances【考试陷阱】
│   └── 5.3 Inventory disclosures and analyst checks【考试核心】
│
├── M06: Long-Term Assets
│   ├── 6.1 Intangible asset origin【考试核心】↔ Topic Outline P11-P12
│   │   ├── purchased
│   │   ├── internally developed
│   │   └── acquired in business combination
│   ├── 6.2 PP&E and intangible impairment / derecognition【考试核心】
│   └── 6.3 Disclosure analysis【考试核心】
│
├── M07: Long-Term Liabilities and Equity
│   ├── 7.1 Lease reporting: lessor vs lessee【考试核心】↔ Topic Outline P12
│   ├── 7.2 Defined contribution vs defined benefit plans【考试核心】
│   ├── 7.3 Stock-based compensation【考试核心】
│   └── 注意：liability / equity presentation choices change leverage reading【考试陷阱】
│
├── M08: Income Taxes
│   ├── 8.1 Accounting profit vs taxable income【考试核心】↔ Topic Outline P12
│   │   ├── taxes payable vs income tax expense
│   │   ├── temporary differences
│   │   └── permanent differences
│   ├── 8.2 Deferred tax assets and liabilities【考试核心】
│   ├── 8.3 Effective / statutory / cash tax rates【考试核心】
│   └── 8.4 Tax disclosures and effective-rate reconciliation【考试核心】
│
├── M09: Financial Reporting Quality
│   ├── 9.1 Reporting quality vs quality of reported results【考试核心】↔ Topic Outline P12
│   ├── 9.2 Conservative vs aggressive accounting【考试核心】
│   ├── 9.3 Motivation, opportunity, discipline mechanisms【考试核心】
│   ├── 9.4 Non-GAAP presentation choices and accounting estimates【考试核心】
│   └── 9.5 Warning signs and manipulation detection【考试核心】
│
├── M10: Financial Analysis Techniques
│   ├── 10.1 Tools and limitations【考试核心】↔ Topic Outline P12-P13
│   ├── 10.2 Activity / liquidity / solvency / profitability ratios【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `Current ratio = CA / CL`
│   │   │   ├── `Quick ratio = (Cash + ST Inv + Receivables) / CL`
│   │   │   ├── `Inventory turnover = COGS / Avg Inventory`
│   │   │   └── `ROE = NI / Avg Equity`
│   ├── 10.3 Ratio relationships and industry-specific ratios【考试核心】
│   ├── 10.4 DuPont decomposition【考试核心】
│   │   ├── 核心公式
│   │   │   └── `ROE = Net Margin x Asset Turnover x Financial Leverage`
│   └── 10.5 Ratio analysis for modeling and forecasting【考试核心】
│
└── M11: Financial Statement Modeling
    ├── 11.1 Sales-based pro forma model【考试核心】↔ Topic Outline P13
    ├── 11.2 Analyst forecast bias and remedies【考试核心】
    ├── 11.3 Porter effects on prices and costs【考试核心】
    ├── 11.4 Inflation / deflation in sales and cost forecasts【考试核心】
    └── 11.5 Explicit forecast horizon and terminal projection choices【考试核心】
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报/用途 | 相关性 | 费用/代价 |
|--------|------|------|-----------|--------|-----------|
| FIFO vs LIFO | 先购先销 vs 后购先销 | inflation 下利润与库存方向不同 | 分析盈利质量和税负 | 与 inventory turnover / gross margin 强相关 | 税负与盈利波动不同 |
| Capitalize vs Expense | 成本递延 vs 当期确认 | 利润时点被重分配 | 资本化前期利润高、后期折旧摊销压力大 | 与 ROA/ROE/asset turnover 强相关 | 代价是后期利润受压 |
| CFO vs Net Income | 现金流 vs 权责利润 | earnings quality 可能失真 | CFO 更贴近现金创造 | 与 accrual quality 强相关 | 代价是计算重构复杂 |
| Basic EPS vs Diluted EPS | 基础股数 vs 稀释后股数 | 忽略稀释会高估每股盈利 | 更真实地反映潜在索取权 | 与 convertibles/options 相关 | 稀释风险 |
| Current Ratio vs Quick Ratio | 含存货 vs 剔除低流动项目 | current 可能高估短期偿债 | quick 更保守 | 与 working capital structure 相关 | 代价是忽视某些可变现存货情形 |

---

## 跨模块关联

```text
Income Statement
├── flows into Balance Sheet via retained earnings
├── links to Cash Flow via non-cash adjustments
└── drives Ratio Analysis
    ├── profitability
    ├── activity
    └── solvency
        └── Modeling
            └── Forecast assumptions
```

---

## 通用分析框架

### 框架1：会计处理方向题 SOP

1. 先识别处理：capitalize / expense / FIFO / LIFO / lease class
2. 再问影响哪三块：income statement / balance sheet / cash flow
3. 再问方向：利润、资产、现金流上升还是下降
4. 最后问比率怎么变

### 框架2：现金流分析 SOP

1. 从 net income 出发
2. 加回 non-cash items
3. 调整 working capital changes
4. 得到 CFO
5. 再推 FCFF / FCFE

### 框架3：ratio 分析 SOP

1. 先分组：liquidity / activity / solvency / profitability
2. 再看同比趋势
3. 再看行业横向比较
4. 最后回到具体会计政策解释变化

---

## 核心公式速查

### Income Statement and Cash Flow

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Basic EPS | `(NI - Preferred Dividends) / Weighted Average Shares` | `2.4` | EPS 基础式 |
| Diluted EPS | `Adjusted NI Available to Common / Adjusted Weighted Average Shares` | `2.4` | 先排除 antidilutive instruments |
| CFO (Indirect) | `NI + Noncash Charges - Noncash Gains/Losses ± WC Changes` | `4.2` | 现金流重构核心 |
| FCFF | `FCFF = CFO + Interest(1 - T) - FCInv` | `4.2` | 公司自由现金流 |
| FCFE | `CFO - FCInv + Net Borrowing` | `4.2` | 股权自由现金流 |

### Liquidity and Activity

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Current Ratio | `Current Assets / Current Liabilities` | `10.2` | 流动性 |
| Quick Ratio | `(Cash + ST Inv + Receivables) / CL` | `10.2` | 更保守流动性 |
| Inventory Turnover | `COGS / Average Inventory` | `10.2` | 存货效率 |
| Days Inventory | `365 / Inventory Turnover` | `10.2` | DIO 常与 CCC 联动 |
| Receivables Turnover | `Revenue / Average Receivables` | `10.2` | 回款效率 |
| DSO | `365 / Receivables Turnover` | `10.2` | 应收账款天数 |
| Total Asset Turnover | `Revenue / Average Total Assets` | `10.2` | 资产效率 |

### Profitability and Solvency

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Gross Margin | `Gross Profit / Revenue` | `10.2` | revenue/COGS choice 的敏感点 |
| Operating Margin | `Operating Income / Revenue` | `10.2` | 经营盈利能力 |
| Net Margin | `NI / Revenue` | `10.4` | DuPont 第一段 |
| ROA | `NI / Average Total Assets` | `10.2` | 资产盈利能力 |
| ROE | `NI / Average Equity` | `10.4` | 股东回报 |
| Financial Leverage | `Average Assets / Average Equity` | `10.4` | DuPont 杠杆段 |
| Debt-to-Equity | `Total Debt / Total Equity` | `10.2` | 偿债结构 |
| Interest Coverage | `EBIT / Interest Expense` | `10.2` | 信用分析常用 |
| DuPont | `Net Margin x Asset Turnover x Financial Leverage` | `10.4` | ROE 分解 |

### Tax and Cash Quality

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Effective Tax Rate | `Income Tax Expense / Pretax Income` | `8.3` | 与 statutory rate 对比 |
| Cash Tax Rate | `Cash Taxes Paid / Pretax Income` | `8.3` | cash vs accrual tax lens |
| Operating Cash Flow Ratio | `CFO / Current Liabilities` | `10.2` | 覆盖短期负债 |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| 净利润高说明经营质量高 | 还要看 CFO 和 accrual quality |
| FIFO/LIFO 只影响存货，不影响利润 | 会直接影响 COGS、税、利润和 ratios |
| capitalizing cost 一定更好 | 只是把费用后移，不是凭空创造价值 |
| CFO 就是 cash receipts - cash payments 的简单差 | indirect method 需要从 NI 系统调整 |
| FCFF 和 FCFE 本质一样 | 一个给所有资本提供者，一个只给股东 |
| diluted EPS 一定比 basic EPS 大 | 稀释通常让 EPS 更低或相同 |
| goodwill 一定会摊销 | IFRS/US GAAP 现行更关注 impairment |
| current ratio 高一定更稳健 | 也可能说明营运资本占用低效 |
| DuPont 只是记公式 | 它是解释 ROE 来源的逻辑框架 |
| ratio 只要会算就够了 | 真正丢分点通常在“如何解释变化” |
