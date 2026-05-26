---
title: "M06 — Inventory Analysis"
description: "存货分析全面解析：计量基础（成本与可变现净值孰低）、成本流转方法（FIFO/加权平均/LIFO）、通胀通缩效应及存货披露分析"
module: M06
official_module: "M6: Analysis of Inventories"
subject: Financial_Statement_Analysis
---

# M06: 存货分析 (Inventory Analysis)

## 1. 核心知识点

### 6.1 计量基础 (Measurement Basis)

- **成本与可变现净值孰低 (Lower of Cost and Net Realizable Value)**：存货期末计量采用成本与可变现净值(NRV)孰低原则。IFRS 使用 NRV；US GAAP 使用市价(market)即重置成本(replacement cost)
- **减记对报表与比率的影响 (Write-Down Implications for Statements and Ratios)**：存货减记(inventory write-down)同时增加当期 COGS、减少利润、降低存货账面价值和资产总额，从而影响毛利率(gross margin)、流动比率(current ratio)和存货周转率(inventory turnover)
- 减记转回(reversal of write-down)：IFRS 允许在后续期间转回至原成本，US GAAP 不允许转回——这是跨准则比较的重要差异

### 6.2 成本流转方法 (Cost-Flow Methods)

- **FIFO / 加权平均 / LIFO 比较 (FIFO / Weighted Average / LIFO Comparison)**：
  - FIFO（先进先出）：先购入的存货先发出，期末存货反映最近购入成本
  - 加权平均法(weighted average cost)：所有存货成本加权平均计算发出成本
  - LIFO（后进先出）：后购入的存货先发出，期末存货反映最早购入成本（US GAAP 允许，IFRS 禁止）

- **通胀 vs 通缩效应 (Inflation vs Deflation Effects)**：
  - **通胀 (Inflation) 环境下**：FIFO 的 COGS 更低、利润更高、期末存货价值更高、所得税更高；LIFO 相反
  - **通缩 (Deflation) 环境下**：两种方法的效果反转
  - LIFO 储备(LIFO reserve)：US GAAP 要求使用 LIFO 的公司披露 LIFO reserve，用于将 LIFO 存货调整为 FIFO 基础

**【考试陷阱】** 存货计价方法改变(inventory method changes)会影响 COGS、税金(taxes)、利润率(margins)和存货余额(inventory balances)——在跨公司比较时需调整统一。

### 6.3 存货披露与分析师检查点 (Inventory Disclosures and Analyst Checks)

- 检查存货账龄(aging of inventory)以识别潜在的过时(obsolescence)风险
- 关注 LIFO liquidation（LIFO 清算）：当 LIFO 公司消耗旧层存货时，COGS 异常低、利润异常高
- 比较存货增长率与销售增长率：存货增速显著高于销售增速可能是过时或跌价风险的信号

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| Inventory Turnover | `COGS / Average Inventory` | 存货周转率，衡量存货管理效率 |
| Days Inventory on Hand (DOH) | `365 / Inventory Turnover` | 存货持有天数 |
| LIFO Reserve | `FIFO Inventory - LIFO Inventory` | LIFO 储备，用于方法转换调整 |
| Adjusted COGS (FIFO basis) | `LIFO COGS - (LIFO Reserve End - LIFO Reserve Beg)` | 将 LIFO COGS 调整为 FIFO 基础 |
| Gross Margin | `(Revenue - COGS) / Revenue` | 毛利率，受存货方法直接和间接影响 |

## 3. 常见考点与解题思路

- **考点1**：FIFO vs LIFO 在不同经济环境下的财务影响。解题思路：先判断通胀还是通缩，再逐项分析 COGS、利润、存货、税金、现金流的变化方向
- **考点2**：LIFO Reserve 的调整计算。解题思路：利用 LIFO reserve 将 LIFO 财务报表调整为 FIFO 基础进行可比分析
- **考点3**：存货减记的影响。解题思路：减记确认时 COGS 增加、利润减少、存货余额降低；转回时 IFRS 下反向操作
- **考点4**：存货比率分析。解题思路：结合存货周转率和毛利率的变化，判断是效率提升还是潜在的过时风险

## 4. 易错点提醒

- **LIFO 与现金流**: 通胀下 LIFO 的 COGS 较高、利润较低、税负较低，因此经营现金流更高——这是 LIFO 的核心税务优势
- **期末存货与 COGS 的方向关系**: FIFO 下，期末存货余额越高说明 COGS 越低；LIFO 下相反——理解这个反向关系至关重要
- **LIFO liquidation**: 当 LIFO 公司销量大于采购量（消耗旧层）时，COGS 异常下降、利润虚增——这是盈利质量的危险信号
- **减记转回**: IFRS 允许但不强制转回，转回金额以原减记金额为上限

## 5. 跨模块关联

- [[M03-Balance-Sheet|资产负债表]]：存货是流动资产(current assets)的重要组成部分，直接影响 current ratio 和 working capital
- [[M02-Income-Statement|利润表分析]]：存货计价方法直接影响 COGS 和毛利率的计算
- [[M04-Cash-Flow-Statements|现金流量表]]：存货变动(inventory changes)是 CFO 计算中的关键营运资本调整项
- [[M08-Income-Taxes|所得税]]：FIFO vs LIFO 导致不同的税负，影响递延所得税的计算
