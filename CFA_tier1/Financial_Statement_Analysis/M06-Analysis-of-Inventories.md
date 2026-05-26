---
title: "M06: Analysis of Inventories"
description: "CFA Level I 2026 Financial Statement Analysis 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Financial Statement Analysis"
topic_area: "Financial_Statement_Analysis"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M06"
official_module: "Module 6: Analysis of Inventories"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Financial_Statement_Analysis
---

# M06: Analysis of Inventories

> **模块定位**：把三张报表转成可比较、可预测、可质疑的经营证据。 本模块聚焦 **Analysis of Inventories**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Analysis of Inventories
- 6.01 | Introduction
- 6.02 | Inventory Valuation
- 6.03 | The Effects of Inflation and Deflation on Inventories, Costs of Sales, and Gross Margin
- 6.04 | Presentation and Disclosure

## Learning Outcome Statements

1. describe the measurement of inventory at the lower of cost and net realisable value and its implications for financial statements and ratios
2. calculate and explain how inflation and deflation of inventory costs affect the financial statements and ratios of companies that use different inventory valuation methods
3. describe the presentation and disclosures relating to inventories and explain issues that analysts should consider when examining a company’s inventory disclosures and other sources of information

---

## 1. 模块定位

### 6.1 学习任务
- **核心问题**：考试希望你用 `Analysis of Inventories` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 6.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 6.3 关键英文术语
- **Analysis of Inventories（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Inventory Valuation（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **The Effects of Inflation and Deflation on Inventories, Costs of Sales, and Gross Margin（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Presentation and Disclosure（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Inventories（存货）**：企业用于销售或生产的库存资产。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 6.1 | describe the measurement of inventory at the lower of cost and net realisable value and its implications for financial statements and ratios | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 6.2 | calculate and explain how inflation and deflation of inventory costs affect the financial statements and ratios of companies that use different inventory valuation methods | 计算并解释数值结果；解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 6.3 | describe the presentation and disclosures relating to inventories and explain issues that analysts should consider when examining a company’s inventory disclosures and other sources of information | 描述定义、流程和适用场景；解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
6. Analysis of Inventories
├─ 6.1 计量基础 (Measurement Basis)
│  ├─ 6.1.1 Lower of cost and NRV：carrying value 高于 NRV 时确认 write-down
│  ├─ 6.1.2 Write-down 影响：COGS/loss 增加、NI 降低、inventory/assets 降低、current ratio 降低
│  └─ 6.1.3 准则判断：IFRS 允许有限转回，US GAAP 通常不允许转回
├─ 6.2 成本流转方法 (Cost-Flow Methods)
│  ├─ 6.2.1 FIFO / weighted average / LIFO：IFRS 禁止 LIFO，US GAAP 允许
│  ├─ 6.2.2 通胀：FIFO COGS 低、gross profit/NI/inventory 高、tax 高；LIFO 相反且 CFO 高
│  ├─ 6.2.3 通缩：上述方向反转；weighted average 介于 FIFO 与 LIFO 之间
│  └─ 6.2.4 LIFO reserve：FIFO inventory = LIFO inventory + LIFO reserve；用于可比性调整
├─ 6.3 存货披露与分析师检查点 (Inventory Disclosures and Analyst Checks)
│  ├─ 6.3.1 披露：cost-flow method、carrying amount、write-down/reversal、LIFO reserve
│  ├─ 6.3.2 风险信号：inventory growth > sales growth、DOH 上升、LIFO liquidation、obsolete inventory
│  └─ 6.3.3 判断：inventory turnover 改善必须结合 gross margin，避免把减记后的低存货误判为效率提升
```

## 4. 知识点详解

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

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 | 说明 |
|------|------|------|
| Inventory Turnover | `COGS / Average Inventory` | 存货周转率，衡量存货管理效率 |
| Days Inventory on Hand (DOH) | `365 / Inventory Turnover` | 存货持有天数 |
| LIFO Reserve | `FIFO Inventory - LIFO Inventory` | LIFO 储备，用于方法转换调整 |
| Adjusted COGS (FIFO basis) | `LIFO COGS - (LIFO Reserve End - LIFO Reserve Beg)` | 将 LIFO COGS 调整为 FIFO 基础 |
| Gross Margin | `(Revenue - COGS) / Revenue` | 毛利率，受存货方法直接和间接影响 |
| FIFO Inventory | `LIFO Inventory + LIFO Reserve` | LIFO 转 FIFO 资产口径 |
| FIFO Retained Earnings | `LIFO Retained Earnings + LIFO Reserve x (1 - Tax Rate)` | 可比性调整时影响权益 |
| Inventory Write-down | `Carrying Value - NRV` | NRV 低于成本时确认损失 |
| Current Ratio Impact | `Current Assets / Current Liabilities` | 存货减记降低流动资产和流动比率 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 6.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 6.2 Inventory Valuation | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.3 The Effects of Inflation and Deflation on Inventories, Costs of Sales, and Gross Margin | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.4 Presentation and Disclosure | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **考点1**：FIFO vs LIFO 在不同经济环境下的财务影响。解题思路：先判断通胀还是通缩，再逐项分析 COGS、利润、存货、税金、现金流的变化方向
- **考点2**：LIFO Reserve 的调整计算。解题思路：利用 LIFO reserve 将 LIFO 财务报表调整为 FIFO 基础进行可比分析
- **考点3**：存货减记的影响。解题思路：减记确认时 COGS 增加、利润减少、存货余额降低；转回时 IFRS 下反向操作
- **考点4**：存货比率分析。解题思路：结合存货周转率和毛利率的变化，判断是效率提升还是潜在的过时风险

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：LIFO 与现金流: 通胀下 LIFO 的 COGS 较高、利润较低、税负较低，因此经营现金流更高——这是 LIFO 的核心税务优势 | ✅ LIFO 与现金流: 通胀下 LIFO 的 COGS 较高、利润较低、税负较低，因此经营现金流更高——这是 LIFO 的核心税务优势 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：期末存货与 COGS 的方向关系: FIFO 下，期末存货余额越高说明 COGS 越低；LIFO 下相反——理解这个反向关系至关重要 | ✅ 期末存货与 COGS 的方向关系: FIFO 下，期末存货余额越高说明 COGS 越低；LIFO 下相反——理解这个反向关系至关重要 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：LIFO liquidation: 当 LIFO 公司销量大于采购量（消耗旧层）时，COGS 异常下降、利润虚增——这是盈利质量的危险信号 | ✅ LIFO liquidation: 当 LIFO 公司销量大于采购量（消耗旧层）时，COGS 异常下降、利润虚增——这是盈利质量的危险信号 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：减记转回: IFRS 允许但不强制转回，转回金额以原减记金额为上限 | ✅ 减记转回: IFRS 允许但不强制转回，转回金额以原减记金额为上限 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **连接 M02**：inventory method 通过 COGS 改变 gross profit、NI 和 margins。
- **连接 M03**：inventory 是 current asset，减记或 LIFO/FIFO 选择改变 current ratio、working capital、total assets。
- **连接 M04/M05**：inventory 增加是 CFO 减项；通胀下 LIFO 税负低，因此 CFO 可能高于 FIFO。
- **连接 M09**：账面与税务成本流转差异会改变 taxes payable，并可能影响 deferred tax 分析。
- **连接 M10/M11**：LIFO liquidation、存货增速超过销售、减记转回都可能是质量或可比性问题。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M05-Inventory-Analysis.md` (medium, 0.41)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
