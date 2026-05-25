---
title: "M11 — Financial Analysis Techniques"
description: "财务分析技术全面解析：流动性/营运/偿债/盈利四大类比率、杜邦分解、比率联动与行业比率、建模预测中的比率应用及分析工具与局限"
module: M11
official_module: "M11: Financial Analysis Techniques"
subject: Financial_Statement_Analysis
---

# M11: 财务分析技术 (Financial Analysis Techniques)

## 1. 核心知识点

### 11.1 分析工具与局限 (Tools and Limitations)

**主要分析工具：**
- **同比例分析 (Common-Size Analysis)**：将报表各项目表示为基准（收入或总资产）的百分比，消除规模影响
- **趋势分析 (Trend Analysis)**：分析同一公司跨期财务数据的变化方向和幅度
- **交叉截面分析 (Cross-Sectional Analysis)**：比较同行业不同公司的财务指标
- **比率分析 (Ratio Analysis)**：通过财务比率衡量公司的各个方面表现

**局限性 (Limitations)：**
- 历史数据导向(historical orientation)——比率反映过去，不保证未来
- 会计政策差异影响可比性(comparability)
- 行业多样性使得行业平均未必代表正常水平
- 单一比率无法反映全貌，需要综合运用

### 11.2 营运/流动性/偿债/盈利比率 (Activity / Liquidity / Solvency / Profitability Ratios)

**流动性比率 (Liquidity Ratios)——短期偿债能力：**

| 比率 | 公式 | 说明 |
|------|------|------|
| Current Ratio | `Current Assets / Current Liabilities` | 流动比率，衡量短期偿债能力 |
| Quick Ratio | `(Cash + ST Investments + Receivables) / Current Liabilities` | 速动比率，排除存货影响 |
| Cash Ratio | `(Cash + ST Investments) / Current Liabilities` | 现金比率，最保守的流动性指标 |

**营运比率 (Activity Ratios)——运营效率：**

| 比率 | 公式 | 说明 |
|------|------|------|
| Inventory Turnover | `COGS / Average Inventory` | 存货周转率 |
| Days of Inventory on Hand (DOH) | `365 / Inventory Turnover` | 存货持有天数 |
| Receivables Turnover | `Revenue / Average Receivables` | 应收账款周转率 |
| Days of Sales Outstanding (DSO) | `365 / Receivables Turnover` | 应收账款天数 |
| Payables Turnover | `COGS / Average Payables` | 应付账款周转率 |
| Total Asset Turnover | `Revenue / Average Total Assets` | 总资产周转率 |

**偿债比率 (Solvency Ratios)——长期偿债和资本结构：**

| 比率 | 公式 | 说明 |
|------|------|------|
| Debt-to-Equity | `Total Debt / Total Equity` | 债务权益比 |
| Debt-to-Assets | `Total Debt / Total Assets` | 债务资产比 |
| Financial Leverage | `Average Total Assets / Average Equity` | 财务杠杆 |
| Interest Coverage | `EBIT / Interest Expense` | 利息覆盖倍数 |
| Fixed Charge Coverage | `(EBIT + Lease Payments) / (Interest + Lease Payments)` | 固定费用覆盖 |

**盈利比率 (Profitability Ratios)——盈利能力：**

| 比率 | 公式 | 说明 |
|------|------|------|
| Gross Profit Margin | `Gross Profit / Revenue` | 毛利率 |
| Operating Margin | `Operating Income / Revenue` | 营业利润率 |
| Net Profit Margin | `Net Income / Revenue` | 净利润率 |
| ROA | `Net Income / Average Total Assets` | 资产收益率 |
| ROE | `Net Income / Average Total Equity` | 权益收益率 |
| Return on Common Equity | `(NI - Preferred Dividends) / Average Common Equity` | 普通股权益收益率 |

#### 核心公式 (English)
- `Current ratio = CA / CL`
- `Quick ratio = (Cash + ST Inv + Receivables) / CL`
- `Inventory turnover = COGS / Avg Inventory`
- `ROE = NI / Avg Equity`

### 11.3 比率联动与行业比率 (Ratio Relationships and Industry-Specific Ratios)

- **比率联动关系**：各比率之间存在内在逻辑联动——例如存货周转率下降(效率恶化)可能导致毛利率上升(可能因提价或产品组合变化)，需综合解读
- **行业特定比率 (Industry-Specific Ratios)**：银行业关注净息差(net interest margin)；零售业关注同店销售增长(same-store sales growth)和每平方英尺销售额(sales per square foot)
- **比率分析的三角验证**：单个比率的变化应与其他相关比率的变化一致，否则可能存在操纵或误解

### 11.4 杜邦分解 (DuPont Decomposition)

**三因式杜邦分解：**
```
ROE = Net Profit Margin x Total Asset Turnover x Financial Leverage
ROE = (NI / Revenue) x (Revenue / Avg Assets) x (Avg Assets / Avg Equity)
```

- **净利率 (Net Profit Margin)**：反映经营效率(efficiency)和成本控制
- **资产周转率 (Asset Turnover)**：反映资产使用效率(utilization)
- **财务杠杆 (Financial Leverage)**：反映资本结构风险(risk)

**分析意义：**
- 分解 ROE 的来源，判断增长驱动因素
- 相同 ROE 的背后可能是完全不同的商业策略（高利润率低周转 vs 低利润高周转）
- 财务杠杆驱动的 ROE 增长不可持续——分析师需要关注盈利增长的"质量"

### 11.5 建模与预测中的比率分析 (Ratio Analysis for Modeling and Forecasting)

- 历史比率是构建财务预测模型(forecasting model)的基础输入
- 关键假设：未来的比率预计会维持、改善还是恶化？
- 比率趋势分析帮助识别拐点(turning point)和异常
- 一个比率的预测需与其他比率保持一致——例如预测毛利率上升的同时预测资产周转率不变需要合理解释

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| Current Ratio | `Current Assets / Current Liabilities` | 流动性代表指标 |
| Quick Ratio | `(Cash + ST Inv + Receivables) / CL` | 更保守的流动性 |
| Inventory Turnover | `COGS / Average Inventory` | 存货效率 |
| DSO | `365 / Receivables Turnover` | 应收账款天数 |
| Total Asset Turnover | `Revenue / Average Total Assets` | 资产使用效率 |
| Debt-to-Equity | `Total Debt / Total Equity` | 杠杆率代表指标 |
| Interest Coverage | `EBIT / Interest Expense` | 偿债能力 |
| ROE | `NI / Average Equity` | 股东回报核心指标 |
| DuPont ROE | `Net Margin x Asset Turnover x Financial Leverage` | ROE 三因子分解 |

## 3. 常见考点与解题思路

- **考点1**：特定比率计算。解题思路：先确定比率类别（流动性/营运/偿债/盈利），再应用相应公式——注意分子分母的"匹配"原则
- **考点2**：DuPont 分解计算和分析。解题思路：将 ROE 拆解为三个因子——识别哪些因子在驱动 ROE 变化，判断这种驱动是否可持续
- **考点3**：会计政策变化对比率的影响。解题思路：先判断政策变化对报表的具体影响，再追踪到特定比率的分子和分母
- **考点4**：跨公司比率比较的调整。解题思路：识别会计政策和财务年度差异，调整统一后再进行比较

## 4. 易错点提醒

- **比率公式的记忆**: 流动性比率用流动资产(current assets)作分子，偿债比率用债务(debt)作分子——注意分母通常是 current liabilities 或 total equity
- **平均值的运用**: 计算周转率(turnover ratios)时应使用平均余额(average balance)，而非期末余额
- **季节性影响**: 对于季节性强的行业，使用年终余额可能严重扭曲周转率——应使用季度平均数据
- **DuPont 的分解逻辑**: 不要只记公式——理解三个因子分别代表经营效率(efficiency)、资产使用(utilization)和风险(risk)
- **比率解释的上下文**: 同一比率值在不同行业有完全不同的含义——永远在行业背景(context)下解读

## 5. 跨模块关联

- [[M02-Income-Statement|利润表分析]]：盈利比率的数据来源，净利率和 EPS 是关键输入
- [[M03-Balance-Sheet|资产负债表]]：流动性、营运和偿债比率的计算依赖于资产负债表数据
- [[M04-Cash-Flow-Statements|现金流量表]]：现金流比率（CFO / Current Liabilities）提供现金流维度的偿债分析
- [[M05-Inventory-Analysis|存货分析]]：存货计价方法直接影响存货周转率和毛利率
- [[M11-Financial-Statement-Modeling|财务报表建模]]：比率分析结果是构建 pro forma 模型和预测的核心输入
