---
title: "M02 — Income Statement"
description: "利润表全面解析：收入确认原则、费用配比、非常项目处理、每股收益计算及同比例分析，CFA L1 核心计算模块"
module: M02
official_module: "M2: Analyzing Income Statements"
subject: Financial_Statement_Analysis
---

# M02: 利润表分析 (Income Statement Analysis)

## 1. 核心知识点

### 2.1 收入确认 (Revenue Recognition)

**一般确认原则 (General Recognition Principles)：**
- IFRS 15 / ASC 606 五步模型(five-step model)：识别合同→识别履约义务→确定交易价格→分摊价格→履行义务时确认收入
- 收入在商品或服务控制权(control)转移给客户时确认

**特定应用改变确认时点 (Specific Applications Alter Timing)：**
- 长期工程合同：完工百分比法(percentage-of-completion method) vs 全部完工法(completed-contract method)
- 分期收款销售(installment sales)：按收款进度确认毛利
- 捆绑销售(bundled sales)：需将交易价格分摊至各履约义务

**时点选择影响利润率与趋势解读 (Timing Choices Affect Margins and Trend Interpretation)：**
- 提前确认收入会高估当期利润率和资产，低估未来增长率
- 收入确认激进程度是财务报告质量分析的关键线索

### 2.2 费用确认 (Expense Recognition)

- **配比逻辑 (Matching Logic)**：费用应与所产生的收入在同一期间配比(matching principle)，包括直接费用(direct expenses)和期间费用(period costs)
- **资本化 vs 费用化 (Capitalize vs Expense)**：资本化将支出记为资产并在使用年限内摊销；费用化则在发生当期全额计入费用

**【考试陷阱】** 资本化(capitalization)只是将费用时点后移，并非改变经济实质(economic reality)——前期利润更高但后期面临摊销压力。

### 2.3 非常项目与政策变更 (Unusual Items and Policy Changes)

- **终止经营 (Discontinued Operations)**：已处置或已分类为持有待售的业务单元，其经营成果需与持续经营业务分开列报
- **非常/偶发项目 (Unusual / Infrequent Items)**：性质特殊或不经常发生的交易，需在利润表中单独列示
- **会计政策变更 (Accounting Policy Changes)**：如存货计价方法从 FIFO 改为加权平均，需追溯调整(retrospective application)

### 2.4 每股收益 (EPS)

#### 核心公式 (English)
- `Basic EPS = (NI - Pref Div) / Weighted Avg Shares`
- `Diluted EPS = Adjusted NI Available to Common / Adjusted Weighted Average Shares`

- **简单资本结构 -> 基础每股收益 (Simple Capital Structure -> Basic EPS)**：仅有普通股(common stock)，无潜在稀释证券
- **复杂资本结构 -> 稀释每股收益 (Complex Capital Structure -> Diluted EPS)**：存在可转换债券(convertible bonds)、期权(options)或认股权证(warrants)
- **反稀释证券被排除 (Antidilutive Securities Excluded)**：如果转换后 EPS 反而上升，则该证券不计入稀释计算

### 2.5 同比例利润表与利润表比率 (Common-Size Income Statement and Income-Statement Ratios)

- 将所有项目表示为收入(revenue)的百分比，便于跨公司和跨期间比较
- 核心比率：毛利率(gross margin)、营业利润率(operating margin)、净利润率(net margin)

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| Basic EPS | `(NI - Preferred Dividends) / Weighted Average Shares Outstanding` | 基础每股收益，简单资本结构使用 |
| Diluted EPS | `(NI - Pref Div + Convertible Interest(1-t)) / (Weighted Avg Shares + Dilutive Shares)` | 考虑潜在稀释证券后的每股收益 |
| Gross Margin | `Gross Profit / Revenue` | 毛利率，核心盈利指标 |
| Operating Margin | `Operating Income / Revenue` | 营业利润率，反映经营效率 |
| Net Margin | `Net Income / Revenue` | 净利润率，最终的盈利水平 |

## 3. 常见考点与解题思路

- **考点1**：Basic EPS 和 Diluted EPS 的计算。解题思路：先确定资本结构类型，再应用相应公式；稀释计算时对分子分母同步调整
- **考点2**：收入确认时点对报表的影响。解题思路：分析确认提前/延迟如何影响当期和下期的收入、资产、利润和现金流
- **考点3**：资本化 vs 费用化的比率影响。解题思路：逐项分析对 ROA、ROE、asset turnover、interest coverage 的影响方向
- **考点4**：终止经营的处理。解题思路：注意终止经营的结果需从持续经营中分离，分析时应予以剔除

## 4. 易错点提醒

- **加权平均股数**: 计算 EPS 使用加权平均流通股数(weighted average shares outstanding)，而非期末股数
- **优先股股利**: Basic EPS 中需从净利润扣除优先股股利(preferred dividends)
- **反稀释判断**: 任何导致 EPS 上升而非下降的证券都不应纳入稀释 EPS 计算
- **非常项目分类**: discontinued operations 与 unusual/infrequent items 的性质不同，分类不可混淆

## 5. 跨模块关联

- [[M04-Cash-Flow-Statements|现金流量表]]：净利润是间接法计算 CFO 的起点，非现金费用(如折旧摊销)在利润表中确认
- [[M09-Financial-Reporting-Quality|财务报告质量]]：收入确认激进程度和费用资本化程度是盈利质量(earnings quality)的核心判断依据
- [[M10-Financial-Analysis-Techniques|财务分析技术]]：利润表中的各项数据是计算盈利比率(profitability ratios)的来源
