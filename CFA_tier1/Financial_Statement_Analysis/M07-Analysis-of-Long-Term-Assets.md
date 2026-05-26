---
title: "M07 — Analysis of Long-Term Assets"
description: "CFA Level I 2026 official module: Analysis of Long-Term Assets"
module: M07
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 7: Analysis of Long-Term Assets"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M07: Analysis of Long-Term Assets

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Analysis of Long-Term Assets
- 7.01 | Introduction
- 7.02 | Acquisition of Intangible Assets
- 7.03 | Impairment and Derecognition of Assets
- 7.04 | Presentation and Disclosure
- 7.05 | Using Disclosures in Analysis

## Learning Outcome Statements

The candidate should be able to:

- compare the financial reporting of the following types of intangible assets: purchased, internally developed, and acquired in a business combination
- explain and evaluate how impairment and derecognition of property, plant, and equipment and intangible assets affect the financial statements and ratios
- analyze and interpret financial statement disclosures regarding property, plant, and equipment and intangible assets

## 🌳 核心知识树

```text
🏆 【长期资产分析】
│
├── 🔷 无形资产来源（Intangible Asset Origin）🎯
│   ├── 外购（Purchased）
│   │   └── 按购买成本确认入账
│   ├── 内部开发（Internally Developed）⚠️
│   │   ├── US GAAP：研发通常全部费用化
│   │   │   └── 仅软件开发成本在技术可行性后资本化
│   │   ├── IFRS：研究阶段费用化，开发阶段有条件资本化
│   │   └── 内部品牌、客户名单不得确认为无形资产
│   └── 企业合并取得（Business Combination）
│       └── 按公允价值确认，通常高于被收购方账面值
│
├── 🔷 PP&E 减值（Impairment）📐🎯
│   ├── IFRS 模型：
│   │   ├── 账面价值 > 可收回金额 → 确认减值
│   │   ├── 可收回金额 = max(公允价值-出售成本, 使用价值)
│   │   └── 允许转回减值 ⚠️
│   └── US GAAP 模型：
│       ├── 第一步：比较账面价值 vs 未折现现金流
│       ├── 第二步：账面价值 > 公允价值 → 确认减值
│       └── 不允许转回 ⚠️
│
├── 🔷 无形资产减值
│   ├── 有限寿命 → 类似 PP&E 减值
│   └── 无限寿命 + 商誉 → 每年减值测试
│
├── 🔷 终止确认（Derecognition）📐
│   ├── 出售：损益 = 出售收入 - 账面价值
│   └── 报废：剩余账面价值一次性计入费用
│
├── 🔷 折旧方法 📐🎯
│   ├── 直线法（SL）：(成本-残值) / 使用年限 → 各期相同
│   ├── 双倍余额递减法（DDB）：2/寿命 × 期初账面值 → 前期高后期低
│   └── 产量法（Units of Production）：按实际使用量
│
├── 🔷 披露分析要点
│   ├── 折旧政策和方法选择
│   ├── 使用寿命和残值估计 ⚠️
│   └── 会计估计变更 → 未来适用法
│
│   💡 核心洞察：折旧是**非现金费用**，在 CFO 间接法中加回
│   🎯 高频考点：资本化条件、IFRS vs US GAAP 减值差异、折旧方法影响
```

## 📖 知识点详解

### 知识点1：无形资产来源（Intangible Asset Origin）

无形资产的会计处理取决于其来源，不同来源的确认条件差异显著：

**外购 (Purchased)：**
- 按购买成本(purchase cost)确认入账，符合资产确认条件(probable future economic benefits and reliable measurement)
- 外购无形资产的成本包括购买价格和直接归属于使资产达到预定用途的支出

**内部开发 (Internally Developed)：**
- US GAAP：研发支出(research and development, R&D)通常全部费用化，仅有特定的软件开发成本(software development costs)在技术可行性确立后资本化
- IFRS：研究阶段(research phase)支出费用化，开发阶段(development phase)支出在满足六项条件时资本化——分析师需注意这种准则差异导致的可比性问题
- 内部开发品牌、客户名单等不得确认为无形资产

**企业合并取得 (Acquired in Business Combination)：**
- 在企业合并(business combination)中，可辨认无形资产按公允价值(fair value)确认
- 这些资产包括客户关系(customer relationships)、技术(technology)、品牌(brands)等
- 合并中确认的无形资产往往比被收购方账面金额更高

### 知识点2：PP&E 与无形资产减值/终止确认（PP&E and Intangible Impairment / Derecognition）

- **PP&E 减值**：当资产的账面价值(carrying amount)超过可收回金额(recoverable amount)时确认减值损失
  - IFRS：可收回金额为公允价值减出售成本与使用价值(value in use)两者中的较高者
  - US GAAP：分两步测试——先比较账面价值与未折现现金流(un-discounted cash flows)，若低于则进行第二步测量减值金额
  - IFRS 允许转回减值(reversal of impairment)，US GAAP 不允许

- **无形资产减值**：有限寿命无形资产减值的处理与 PP&E 类似；无限寿命无形资产和商誉需每年进行减值测试(annual impairment test)

- **终止确认 (Derecognition)**：
  - 出售(disposal)：差额 = 出售收入 - 账面价值，计入利润表
  - 报废(abandonment)：剩余账面价值一次性计入费用

### 知识点3：披露分析（Disclosure Analysis）

- **折旧政策 (Depreciation Policy)**：折旧方法（直线法 straight-line、双倍余额递减法 DDB、产量法 units of production）的选择影响各期利润
- **使用寿命估计 (Useful Life Estimates)**：管理层对使用寿命的估计直接影响年度折旧费用
- **残值估计 (Residual Value Estimates)**：残值越高，年度折旧费用越低
- **分析师调整**：当可比公司的折旧政策存在差异时，分析师需进行调整以实现同口径比较

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `SL Depreciation = (Cost - Residual Value) / Useful Life` | 直线法折旧 | 各期折旧相同 | 残值和使用寿命是**估计值** |
| `DDB Depreciation = (2 / Useful Life) × NBV_Begin` | 双倍余额递减法 | 加速折旧 | 前期折旧高、后期低 |
| `Units of Production = (Cost - RV) × (Actual Output / Total Est. Output)` | 产量法 | 按使用量折旧 | 适合与使用量相关的资产 |
| `Carrying Amount = Historical Cost - Accum. Depr. - Impairment` | 账面价值 | 资产当前价值 | 不计提折旧的土地账面值 = 成本 |
| `Recoverable Amount (IFRS) = max(FV - Selling Cost, Value in Use)` | 可收回金额 | IFRS 减值测试 | Value in Use 是**折现后**现金流 |
| `Impairment Loss = CA - Recoverable Amount (or FV)` | 减值损失 | 资产减值确认 | IFRS 可转回；US GAAP 不可 |
| `Gain/Loss on Disposal = Sale Proceeds - CA at Disposal` | 处置损益 | 资产出售 | 计入利润表 |

## 🛠️ 常见考点与解题思路

### 主题1：内部开发无形资产的资本化（🎯 必考）
- **题型**：判断某项研发支出应资本化还是费用化
- **IFRS 解题框架**：
  1. 判断所处阶段 → 研究阶段（全部费用化）or 开发阶段（有条件资本化）
  2. 开发阶段六条件：技术可行性、意图完成、有能力使用/出售、产生经济利益、资源充足、可靠计量
  3. 满足全部六项 → 资本化；否则费用化
- **US GAAP 解题框架**：
  - 一般研发支出 → 全部费用化
  - 例外：软件开发成本 → 技术可行性确立后资本化

### 主题2：资产减值测试（🎯 高频）
- **IFRS**：一步法。比较 CA 与 Recoverable Amount（取 FV - Selling Cost 与 Value in Use 孰高）
- **US GAAP**：两步法。先比较 CA 与 Undiscounted CF；若 CA > UCF，再计算减值金额 = CA - FV

### 主题3：折旧方法对报表的影响
- **解题思路**：
  | 特征 | 直线法 | 加速折旧法 |
  |------|:------:|:----------:|
  | 前期折旧 | 较低 | **较高** |
  | 前期利润 | **较高** | 较低 |
  | 后期利润 | 较低 | **较高** |
  | 总折旧额 | 相同 | 相同 |
  | 对 CFO 影响 | 无差异 | 无差异（折旧是非现金） |

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 所有研发支出都可能资本化 | IFRS 要求区分研究/开发阶段；US GAAP 大部分研发需费用化 | 准则差异是关键考点 |
| 减值测试中 IFRS 和 US GAAP 方法相同 | IFRS 用可收回金额（折现），US GAAP 先用未折现现金流测试 | US GAAP 两步法，IFRS 一步法 |
| IFRS 不允许减值转回 | IFRS **允许**减值转回（但商誉减值不可转回），US GAAP 不允许 | 跨准则对比的重要差异 |
| 折旧方法改变是会计政策变更 | 折旧方法改变**通常是会计估计变更**，使用未来适用法 | 仅追溯调整政策变更 |
| 所有无形资产都摊销 | 无限寿命无形资产和商誉**不摊销**，每年做减值测试 | 有限寿命才摊销 |
| 折旧产生现金 | 折旧是**非现金费用**，不产生现金 | 折旧加回 CFO 是为了消除对 NI 的影响 |

## 🔄 跨模块关联

- **[[M03-Analyzing-Balance-Sheets]]** — 长期资产是资产负债表非流动资产的核心组成部分；累计折旧和减值影响资产总额
- **[[M02-Analyzing-Income-Statements]]** — 折旧和摊销费用直接影响营业利润和净利润；资产处置损益属于非常/偶发项目
- **[[M04-Analyzing-Statements-of-Cash-Flows-I]]** — 折旧加回是间接法 CFO 的关键调整项；资产购买（CFI 流出）和出售（CFI 流入）记录在投资活动中
- **[[M06-Analysis-of-Inventories]]** — 存货减值的概念类似但准则不同（存货按成本与可变现净值孰低，长期资产用可收回金额测试）
- **[[M09-Analysis-of-Income-Taxes]]** — 资产账面价值与计税基础的差异产生递延所得税；加速折旧法在税务上的使用（MACRS）与会计折旧不同
- **[[M08-Topics-in-Long-Term-Liabilities-and-Equity]]** — 融资租赁的使用权资产折旧处理与本模块的 PP&E 折旧逻辑相同

## 📋 复习与刷题提示

- **概念辨析**：区分研究阶段 vs 开发阶段（IFRS）、费用化 vs 资本化的条件、外购 vs 内部开发无形资产的确认差异
- **计算方法**：直线法、DDB、产量法折旧计算是基础题型。注意 DDB 不考虑残值直到最后一年
- **减值两步法**：US GAAP 的两步法减值测试是常考内容，特别注意第一步使用**未折现**现金流
- **跨准则比较**：IFRS vs US GAAP 在减值、研发资本化、转回机制三方面的差异是核心考点
- **会计估计变更**：使用寿命和残值的变更是会计估计变更（未来适用法），不是政策变更（追溯调整）
- **常见陷阱**：折旧不产生现金流、加速折旧法总折旧额与直线法相同、减值转回仅 IFRS 允许
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
