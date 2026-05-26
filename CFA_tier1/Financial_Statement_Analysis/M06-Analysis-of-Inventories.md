---
title: "M06 — Analysis of Inventories"
description: "CFA Level I 2026 official module: Analysis of Inventories"
module: M06
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 6: Analysis of Inventories"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M06: Analysis of Inventories

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Analysis of Inventories
- 6.01 | Introduction
- 6.02 | Inventory Valuation
- 6.03 | The Effects of Inflation and Deflation on Inventories, Costs of Sales, and Gross Margin
- 6.04 | Presentation and Disclosure

## Learning Outcome Statements

The candidate should be able to:

- describe the measurement of inventory at the lower of cost and net realisable value and its implications for financial statements and ratios
- calculate and explain how inflation and deflation of inventory costs affect the financial statements and ratios of companies that use different inventory valuation methods
- describe the presentation and disclosures relating to inventories and explain issues that analysts should consider when examining a company’s inventory disclosures and other sources of information

## 🌳 核心知识树

```text
🏆 【存货分析】
│
├── 🔷 计量基础：成本与可变现净值孰低 🎯
│   ├── IFRS → NRV（可变现净值）
│   ├── US GAAP → Market（市场价/重置成本）
│   ├── 减记确认：增加 COGS、减少利润、降低存货余额
│   └── ⚠️ 减记转回：IFRS 允许（至原成本），US GAAP 禁止
│
├── 🔷 成本流转方法 📐🎯
│   ├── FIFO（先进先出）
│   │   ├── 期末存货反映最近购入成本
│   │   └── 通胀时：COGS 低、利润高、税金高
│   ├── 加权平均法
│   │   └── 所有成本加权平均，折中方案
│   └── LIFO（后进先出）
│       ├── 仅 US GAAP 允许，IFRS 禁止 ⚠️
│       ├── 期末存货反映最早购入成本
│       ├── 通胀时：COGS 高、利润低、税金低、CFO 高 🎯
│       └── LIFO Reserve：FIFO Inventory - LIFO Inventory
│
├── 🔷 通胀 vs 通缩效应
│   ├── 通胀：FIFO → 利润↑ 存货↑ 税金↑; LIFO → 相反
│   └── 通缩：两种方法的效果反转
│
├── 🔷 LIFO Liquidation（LIFO 清算）⚠️🎯
│   ├── 销量 > 采购量 → 消耗旧层低成本存货
│   ├── COGS 异常下降 → 利润虚增
│   └── 盈利质量的**危险信号**
│
├── 🔷 存货披露与分析师检查点
│   ├── 检查存货账龄 → 识别过时风险
│   ├── 比较存货增长率 vs 销售增长率
│   └── ⚠️ 存货增速显著高于销售增速 → 跌价风险信号
│
│   💡 核心洞察：存货方法选择影响 COGS、净利润、现金流和税金
│   🎯 高频考点：FIFO vs LIFO 对比、LIFO Reserve 调整、减记影响
```

## 📖 知识点详解

### 知识点1：计量基础（Measurement Basis）

- **成本与可变现净值孰低 (Lower of Cost and Net Realizable Value)**：存货期末计量采用成本与可变现净值(NRV)孰低原则。IFRS 使用 NRV；US GAAP 使用市价(market)即重置成本(replacement cost)
- **减记对报表与比率的影响 (Write-Down Implications for Statements and Ratios)**：存货减记(inventory write-down)同时增加当期 COGS、减少利润、降低存货账面价值和资产总额，从而影响毛利率(gross margin)、流动比率(current ratio)和存货周转率(inventory turnover)
- 减记转回(reversal of write-down)：IFRS 允许在后续期间转回至原成本，US GAAP 不允许转回——这是跨准则比较的重要差异

### 知识点2：成本流转方法（Cost-Flow Methods）

- **FIFO / 加权平均 / LIFO 比较 (FIFO / Weighted Average / LIFO Comparison)**：
  - FIFO（先进先出）：先购入的存货先发出，期末存货反映最近购入成本
  - 加权平均法(weighted average cost)：所有存货成本加权平均计算发出成本
  - LIFO（后进先出）：后购入的存货先发出，期末存货反映最早购入成本（US GAAP 允许，IFRS 禁止）

- **通胀 vs 通缩效应 (Inflation vs Deflation Effects)**：
  - **通胀 (Inflation) 环境下**：FIFO 的 COGS 更低、利润更高、期末存货价值更高、所得税更高；LIFO 相反
  - **通缩 (Deflation) 环境下**：两种方法的效果反转
  - LIFO 储备(LIFO reserve)：US GAAP 要求使用 LIFO 的公司披露 LIFO reserve，用于将 LIFO 存货调整为 FIFO 基础

**【考试陷阱】** 存货计价方法改变(inventory method changes)会影响 COGS、税金(taxes)、利润率(margins)和存货余额(inventory balances)——在跨公司比较时需调整统一。

### 知识点3：存货披露与分析师检查点（Inventory Disclosures and Analyst Checks）

- 检查存货账龄(aging of inventory)以识别潜在的过时(obsolescence)风险
- 关注 LIFO liquidation（LIFO 清算）：当 LIFO 公司消耗旧层存货时，COGS 异常低、利润异常高
- 比较存货增长率与销售增长率：存货增速显著高于销售增速可能是过时或跌价风险的信号

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Inventory Turnover = COGS / Average Inventory` | 存货周转率 | 衡量存货管理效率 | 使用平均存货，而非期末数 |
| `DOH = 365 / Inventory Turnover` | 存货持有天数 | 衡量存货销售速度 | 周转率越高 → 持有天数越短 |
| `LIFO Reserve = FIFO Inventory - LIFO Inventory` | LIFO 储备 | 将 LIFO 调整为 FIFO | US GAAP 要求披露 |
| `Adj. COGS (FIFO) = LIFO COGS - (LIFO Reserve_End - LIFO Reserve_Beg)` | COGS 调整 | LIFO → FIFO 转换 | Reserve 增加 → COGS 减少 |
| `Adj. Inventory (FIFO) = LIFO Inventory + LIFO Reserve` | 存货调整 | LIFO → FIFO 转换 | 直接加回 LIFO Reserve |
| `Gross Margin = (Revenue - COGS) / Revenue` | 毛利率 | 盈利能力 | 存货方法直接影响 |
| `Write-Down = Cost - NRV (or Market)` | 减记金额 | 存货减值 | 当成本 > 可变现净值时 |

## 🛠️ 常见考点与解题思路

### 主题1：FIFO vs LIFO 财务影响对比（🎯 必考）
- **解题框架**：通胀环境下
  | 项目 | FIFO | LIFO |
  |------|:----:|:----:|
  | COGS | 更低 | **更高** |
  | 净利润 | **更高** | 更低 |
  | 所得税 | 更高 | **更低** |
  | 期末存货 | **更高** | 更低 |
  | CFO | 更低 | **更高**（税少） |
  | 营运资本 | **更高** | 更低 |
- **解题思路**：先判断经济环境（通胀/通缩），再逐项推导变化方向

### 主题2：LIFO Reserve 调整计算
- **题型**：给出 LIFO 下的报表数据和 LIFO Reserve，要求调整为 FIFO 基础
- **步骤**：
  1. FIFO Inventory = LIFO Inventory + LIFO Reserve
  2. FIFO COGS = LIFO COGS - (LIFO Reserve_End - LIFO Reserve_Beg)
  3. Adj. Retained Earnings = LIFO Retained Earnings + LIFO Reserve × (1 - t)
  4. 调整后做比率分析

### 主题3：存货减记影响
- **题型**：存货减记对当期和未来报表的影响
- **解题步骤**：
  - 确认减记时：COGS ↑、NI ↓、Inventory ↓、Ratios 恶化
  - 后续转回（IFRS 仅）：COGS ↓、NI ↑、Inventory ↑
  - US GAAP 下转回**不允许** → 一旦减值永久影响账面价值

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| LIFO 在通胀下利润更高 | LIFO 在通胀下**利润更低**（COGS 高） | 后购入的高价存货先发出 → COGS 高 |
| LIFO 在通胀下 CFO 更低 | LIFO 在通胀下**CFO 更高**（税负低） | 利润低 → 所得税低 → 现金流出少 |
| LIFO Reserve 是永久差异 | LIFO Reserve 随价格变化而波动 | 通胀扩大 Reserve，通缩缩小 |
| 存货减记对所有比率产生同向影响 | 减记使存货周转率**上升**（COGS↑/Inv↓）但毛利率**下降** | 不同比率方向可能相反，需逐一分析 |
| IFRS 和 US GAAP 的存货减值规则相同 | IFRS 使用 NRV 且允许转回，US GAAP 使用市场价且禁止转回 | 跨准则比较时需调整 |
| LIFO liquidation 总是好事情 | LIFO liquidation 导致利润虚增，掩盖真实业绩 | 消耗旧层低成本存货不可持续 |
| 加权平均法介于 FIFO 和 LIFO 之间 | 加权平均的效果确实介于 FIFO 和 LIFO 之间 | 适用于价格波动不大的情况 |

## 🔄 跨模块关联

- **[[M03-Analyzing-Balance-Sheets]]** — 存货是流动资产的重要组成部分，直接影响 Current Ratio 和 Working Capital；LIFO Reserve 影响存货账面价值
- **[[M02-Analyzing-Income-Statements]]** — 存货计价方法直接影响 COGS、毛利率和净利润；存货减记影响非经常性项目
- **[[M04-Analyzing-Statements-of-Cash-Flows-I]]** — 存货变动（Inventory Changes）是间接法 CFO 中的关键营运资本调整项
- **[[M07-Analysis-of-Long-Term-Assets]]** — 存货减值的概念逻辑与长期资产减值类似，但存货适用不同的准则（成本与可变现净值孰低）
- **[[M09-Analysis-of-Income-Taxes]]** — FIFO vs LIFO 导致不同的所得税负，影响递延所得税资产/负债的计算（存货账面价值与计税基础的差异）
- **[[M11-Financial-Analysis-Techniques]]** — 存货周转率（Inventory Turnover）和 DOH 是营运比率分析的核心指标

## 📋 复习与刷题提示

- **对比分析**：FIFO vs LIFO 在通胀/通缩下的全部影响对比是必考内容。用矩阵表格系统记忆
- **LIFO Reserve 计算**：掌握 LIFO Reserve 的期初期末变化如何影响 COGS 调整和存货调整。这是高频计算题
- **减记转回**：IFRS 允许 vs US GAAP 禁止转回 — 这是跨准则比较的核心差异点
- **LIFO 清算**：理解什么情况下发生（销量>采购量）、对报表的影响（COGS 下降、利润虚增）、为什么是危险信号
- **比率联动**：理解存货方法变化如何连锁影响毛利率、存货周转率、流动比率、ROA 等关键指标
- **综合分析**：高存货周转率 + 高毛利率通常是好信号；高存货周转率 + 低毛利率可能意味着低价促销策略
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
