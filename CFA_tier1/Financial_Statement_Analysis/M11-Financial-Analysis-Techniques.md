---
title: "M11 — Financial Analysis Techniques"
description: "CFA Level I 2026 official module: Financial Analysis Techniques"
module: M11
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 11: Financial Analysis Techniques"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M11: Financial Analysis Techniques

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Financial Analysis Techniques
- 11.01 | Introduction
- 11.02 | The Financial Analysis Process
- 11.03 | Analytical Tools and Techniques
- 11.04 | Financial Ratio Analysis
- 11.05 | Common Size Balance Sheets and Income Statements
- 11.06 | Cross-Sectional, Trend Analysis, and Relationships in Financial Statements
- 11.07 | The Use of Graphs and Regression Analysis
- 11.08 | Common Ratio Categories, Interpretation, and Context
- 11.09 | Activity Ratios
- 11.10 | Liquidity Ratios
- 11.11 | Solvency Ratios
- 11.12 | Profitability Ratios
- 11.13 | Integrated Financial Ratio Analysis
- 11.14 | DuPont Analysis—The Decomposition of ROE
- 11.15 | Industry-Specific Financial Ratios
- 11.16 | Model Building and Forecasting

## Learning Outcome Statements

The candidate should be able to:

- describe tools and techniques used in financial analysis, including their uses and limitations
- calculate and interpret activity, liquidity, solvency, and profitability ratios
- describe relationships among ratios and evaluate a company using ratio analysis
- demonstrate the application of DuPont analysis of return on equity and calculate and interpret effects of changes in its components
- describe the uses of industry-specific ratios used in financial analysis
- describe how ratio analysis and other techniques can be used to model and forecast earnings

## 🌳 核心知识树

```text
🏆 【财务分析技术】
│
├── 🔷 分析工具四大类 🎯
│   ├── 同比例分析（Common-Size）：消除规模差异
│   ├── 趋势分析（Trend Analysis）：跨期比较方向和幅度
│   ├── 交叉截面分析（Cross-Sectional）：同业比较
│   └── 比率分析（Ratio Analysis）：四大类系统评估
│
├── 🔷 流动性比率（Liquidity Ratios）— 短期偿债 🎯
│   ├── Current Ratio = CA / CL 📐
│   ├── Quick Ratio = (Cash + ST Inv + AR) / CL 📐
│   └── Cash Ratio = (Cash + ST Inv) / CL 📐
│       ⚠️ Current Ratio 高 ≠ 流动性好（存货积压）
│
├── 🔷 营运比率（Activity Ratios）— 运营效率 🎯
│   ├── Inventory Turnover = COGS / Avg Inventory 📐
│   ├── Receivables Turnover = Revenue / Avg AR 📐
│   ├── Payables Turnover = COGS / Avg AP 📐
│   ├── Total Asset Turnover = Revenue / Avg Total Assets 📐
│   └── Cash Conversion Cycle = DOH + DSO - DPO 📐🎯
│
├── 🔷 偿债比率（Solvency Ratios）— 长期偿债 🎯
│   ├── D/E = Total Debt / Total Equity 📐
│   ├── Debt-to-Assets = Total Debt / Total Assets 📐
│   ├── Financial Leverage = Avg Assets / Avg Equity 📐
│   ├── Interest Coverage = EBIT / Interest Expense 📐
│   └── Fixed Charge Coverage = (EBIT + Lease) / (Interest + Lease) 📐
│
├── 🔷 盈利比率（Profitability Ratios）— 盈利能力 🎯
│   ├── Gross / Operating / Net Margin 📐
│   ├── ROA = NI / Avg Total Assets 📐
│   └── ROE = NI / Avg Equity 📐
│
├── 🔷 杜邦分解（DuPont Analysis）📐🎯
│   ├── 三因式：ROE = Net Margin × Asset Turnover × Financial Leverage
│   ├── 五因式：ROE = (NI/EBT) × (EBT/EBIT) × (EBIT/Rev) × (Rev/Assets) × (Assets/Equity)
│   ├── 相同 ROE 可能来自不同策略：高利润率低周转 vs 低利润高周转
│   └── ⚠️ 杠杆驱动的 ROE 增长不可持续
│
│   💡 核心洞察：比率分析必须放在行业背景下解读
│   🎯 高频考点：四大类比率计算、杜邦分解、CCC、比率联动
```

## 📖 知识点详解

### 知识点1：分析工具与局限（Tools and Limitations）

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

### 知识点2：营运/流动性/偿债/盈利比率（Activity / Liquidity / Solvency / Profitability Ratios）

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

### 知识点3：比率联动与行业比率（Ratio Relationships and Industry-Specific Ratios）

- **比率联动关系**：各比率之间存在内在逻辑联动——例如存货周转率下降(效率恶化)可能导致毛利率上升(可能因提价或产品组合变化)，需综合解读
- **行业特定比率 (Industry-Specific Ratios)**：银行业关注净息差(net interest margin)；零售业关注同店销售增长(same-store sales growth)和每平方英尺销售额(sales per square foot)
- **比率分析的三角验证**：单个比率的变化应与其他相关比率的变化一致，否则可能存在操纵或误解

### 知识点4：杜邦分解（DuPont Decomposition）

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

### 知识点5：建模与预测中的比率分析（Ratio Analysis for Modeling and Forecasting）

- 历史比率是构建财务预测模型(forecasting model)的基础输入
- 关键假设：未来的比率预计会维持、改善还是恶化？
- 比率趋势分析帮助识别拐点(turning point)和异常
- 一个比率的预测需与其他比率保持一致——例如预测毛利率上升的同时预测资产周转率不变需要合理解释

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Current Ratio = CA / CL` | 流动比率 | 短期偿债能力概览 | 包含存货，可能高估流动性 |
| `Quick Ratio = (Cash + ST Inv + AR) / CL` | 速动比率 | 更保守的流动性 | 排除存货，更严格 |
| `Cash Ratio = (Cash + ST Inv) / CL` | 现金比率 | 最保守的流动性 | 很少单独使用 |
| `Inventory Turnover = COGS / Avg Inventory` | 存货周转率 | 存货管理效率 | 使用平均余额 |
| `Receivables Turnover = Revenue / Avg AR` | 应收周转率 | 收款效率 | 分子用收入，非赊销额 |
| `DSO = 365 / Receivables Turnover` | 应收账款天数 | 平均收款期 | 越高说明收款越慢 |
| `Payables Turnover = COGS / Avg AP` | 应付周转率 | 付款效率 | 越高说明付款越快 |
| `CCC = DOH + DSO - DPO` | 现金转换周期 | 营运资本效率 | 越短越好，负值更优 |
| `Total Asset Turnover = Revenue / Avg TA` | 总资产周转率 | 资产使用效率 | 越低说明资产越重 |
| `D/E = Total Debt / Total Equity` | 债务权益比 | 财务杠杆 | 越高风险越大 |
| `Interest Coverage = EBIT / Interest Expense` | 利息覆盖倍数 | 偿债能力 | 越高越安全 |
| `Fixed Charge Coverage = (EBIT + Lease) / (Interest + Lease)` | 固定费用覆盖 | 含租赁的偿债 | 比 ICR 更全面 |
| `ROE = NI / Avg Equity` | 权益收益率 | 股东回报 | 杜邦分解揭示驱动因素 |
| `DuPont ROE = Net Margin × Asset Turnover × Financial Leverage` | 杜邦三因式 | ROE 归因分析 | 识别增长质量 |

## 🛠️ 常见考点与解题思路

### 主题1：四大类比率计算（🎯 必考）
- **题型**：给定财务报表数据，要求计算特定比率
- **解题步骤**：
  1. 识别比率类别（流动性/营运/偿债/盈利）
  2. 确认分子分母的来源（利润表 vs 资产负债表）
  3. 资产负债表项目用**平均余额**（期初+期末）/2
  4. 代入公式计算并解释含义

### 主题2：杜邦分解（🎯 高频）
- **题型**：给出 ROE 的三个驱动因子或财务报表，要求分析 ROE 变化的原因
- **解题框架**：
  1. 计算三因子：净利率（经营效率）、资产周转率（使用效率）、财务杠杆（风险）
  2. 比较各因子的变化方向和幅度
  3. 判断：净利率和周转率驱动是高质量的；仅杠杆驱动是高风险的
- **五因式扩展**：税负效应（NI/EBT）+ 利息负担（EBT/EBIT）+ 经营利润率（EBIT/Revenue）

### 主题3：现金转换周期分析
- **题型**：计算 CCC 并解释其含义
- **解题步骤**：
  1. DOH = 365 / Inventory Turnover
  2. DSO = 365 / Receivables Turnover
  3. DPO = 365 / Payables Turnover（分母用 Purchases 或 COGS）
  4. CCC = DOH + DSO - DPO
  5. 解读：CCC 越短越好；负的 CCC 是优质信号（先收钱后付款）

### 主题4：比率联动分析
- **类型**：综合分析多个比率的变化趋势
- **解题思路**：
  - 毛利率上升 + 存货周转率下降 → 可能是提价但存货积压
  - ROE 上升 + 杠杆率下降 → 高质量增长
  - ROE 上升 + 杠杆率大幅上升 → 风险驱动型增长，不可持续

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| Current Ratio 高 = 流动性好 | Current Ratio 高可能是存货积压或应收款账期过长 | 需结合存货质量和应收账款账龄分析 |
| Quick Ratio 排除存货 = 更准确 | Quick Ratio 排除存货但也依赖应收款的变现能力 | 应收款也可能存在坏账风险 |
| ROE 高 = 公司好 | ROE 高可能是高杠杆的结果，需要用杜邦分解验证 | 杠杆放大了 ROE 也放大了风险 |
| 比率分析是客观的 | 会计政策差异（FIFO vs LIFO、折旧方法）影响可比性 | IFRS vs US GAAP 差异需调整 |
| 过去比率预测未来 | 比率是历史导向的，不保证未来表现 | 需结合前瞻性分析和行业趋势 |
| CCC 越短越好 | CCC 过短可能意味着过度挤压供应商或收紧信用 | 可能损害供应商关系或失去销售 |
| 财务杠杆总是坏事 | 适当杠杆可提升 ROE，但过度杠杆增加破产风险 | 关键在于杠杆是否可持续 |

## 🔄 跨模块关联

- **[[M02-Analyzing-Income-Statements]]** — 盈利比率（毛利率、净利率、营业利润率）的数据来源于利润表；EPS 计算涉及稀释和基本概念
- **[[M03-Analyzing-Balance-Sheets]]** — 流动性比率和偿债比率的计算依赖于资产负债表项目；同比例资产负债表是跨期比较的基础
- **[[M04-Analyzing-Statements-of-Cash-Flows-I]]** — CFO、CFI、CFF 数据用于现金流比率（CFO/CL、FCF/Revenue 等）的计算
- **[[M06-Analysis-of-Inventories]]** — 存货计价方法（FIFO/LIFO）直接影响存货周转率和毛利率，跨公司比较时需调整统一
- **[[M08-Topics-in-Long-Term-Liabilities-and-Equity]]** — 租赁负债和养老金负债影响 D/E 比率和偿债比率；负债/权益分类影响杠杆计算
- **[[M05-Analyzing-Statements-of-Cash-Flows-II]]** — 自由现金流比率是盈利比率的重要补充，评估盈利的现金质量
- **[[M12-Introduction-to-Financial-Statement-Modeling]]** — 历史比率是构建 Pro Forma 预测模型的核心输入；比率趋势帮助识别拐点

## 📋 复习与刷题提示

- **计算题优先级最高**：四大类比率的计算是 CFA L1 最高频题型。熟练所有公式，特别注意分子分母的匹配
- **杜邦分解**：三因式和五因式都是常考内容。重点不是计算数字，而是**解读每个因子代表的商业含义**
- **CCC 计算**：DOH、DSO、DPO 的计算及其与 CCC 的逻辑关系是必考
- **比率解读**：同一比率在不同行业的含义不同（如零售业的高资产周转率 vs 制造业的低资产周转率）
- **交叉验证**：学会用多个比率相互验证判断（如毛利率和存货周转率的联动分析）
- **Limitations Awareness**：会计政策差异、季节性影响、历史导向性、行业多样性等局限性也是考点
- **考试判断速查**：
  - 短期偿债 → 流动性比率
  - 运营效率 → 营运比率
  - 长期偿债 → 偿债比率
  - 盈利能力 → 盈利比率
  - 拆分 ROE → 杜邦分解
  - 消除规模差异 → 同比例分析
  - 同行业比较 → 交叉截面分析

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
