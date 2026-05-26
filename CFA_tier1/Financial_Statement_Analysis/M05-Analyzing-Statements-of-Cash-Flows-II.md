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

### 🌳 核心知识树

```text
🏆 FSA M04: Cash Flow Statement Analysis（现金流量表分析）
│
├── ⭐ 三大报表联动
│   ├── 现金增减源于利润表和资产负债表变动
│   ├── CFO: 经营活动 — 核心经营现金流
│   ├── CFI: 投资活动 — 资本支出和资产买卖
│   ├── CFF: 融资活动 — 负债和股权变动
│   └── 净利润 + 非现金调整 + 营运资本变动 = CFO
│
├── ⭐ 间接法 (Indirect Method)
│   ├── 从 NI 出发，调整非现金项目和营运资本变动
│   ├── 加回: 折旧、摊销、减值损失
│   ├── 营运资本: 应收↑ → 现金↓；应付↑ → 现金↑
│   └── ⚠️ NI-to-CFO 桥接是调节表，非现金流量定义
│
├── ⭐ 直接法 (Direct Method)
│   ├── 直接列示现金收入和支出
│   ├── IFRS 鼓励；US GAAP 两者均可
│   └── 现金收款 = 收入 - 应收增加；现金付款 = 费用 + 应付减少
│
├── ⭐ IFRS vs US GAAP 分类差异
│   ├── 利息支付: IFRS 可选经营/融资；US GAAP 经营
│   ├── 股利支付: IFRS 可选经营/融资；US GAAP 融资
│   ├── 利息和股利收入: IFRS 可选经营/投资；US GAAP 经营
│   └── 银行透支: IFRS 可视为现金等价物；US GAAP 融资
│
├── ⭐ 分析产出
│   ├── 📐 CFO = NI + 折旧/摊销 - 利得/损失 +/- WC
│   ├── 📐 FCFF = CFO + Interest(1-T) - FCInv
│   ├── 📐 FCFE = CFO - FCInv + Net Borrowing
│   └── 同比例分析: 各项目表示为收入或总现金流的%
│
├── 💡 关键洞察
│   ├── 直接法和间接法 CFO 金额相同
│   ├── 营运资本变动方向最易出错
│   ├── FCFF 给所有资本提供者；FCFE 只给股东
│   └── NI 到 CFO 桥接不是现金流量定义
│
└── ⚠️ 考试陷阱总结
    ├── 非现金项目加回费用也要减去收益
    ├── 流动资产增加是减项，流动负债增加是加项
    ├── FCFF 加回税后利息；FCFE 不再加回
    └── 注意 IFRS vs US GAAP 分类差异
```

### 📐 关键公式表

| 指标 | 公式 | 说明 |
|------|------|------|
| CFO (间接法) | `NI + 折旧/摊销 - 利得/损失 +/- WC 变动` | 核心现金流公式 |
| FCFF | `CFO + Interest(1-T) - FCInv` | 公司自由现金流 |
| FCFE | `CFO - FCInv + Net Borrowing` | 股权自由现金流 |
| CFO / CL | `CFO / Current Liabilities` | 经营现金流比率 |

### 🛠️ 常见考点与解题思路

**考点1：间接法下 CFO 计算**
- 从 NI 出发，加回非现金费用，调整营运资本变动。

**考点2：FCFF/FCFE 计算与区别**
- FCFF 给所有资本提供者，FCFE 只给股东。

**考点3：IFRS vs US GAAP 分类差异**
- 记住利息和股利的分类差异，IFRS 更灵活。

**考点4：直接法编制**
- 利用利润表和对应资产负债表科目倒推现金收付。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| 只加回非现金费用 | 非现金收益也要减去 |
| 所有资产增加 = 现金增加 | 流动资产增加是减项（用现金）|
| FCFF 和 FCFE 相同 | FCFF 加回税后利息；FCFE 不加回 |
| 直接法和间接法 CFO 不同 | 两者 CFO 金额应当相同 |
| 营运资本变动方向全凭感觉 | 资产↑ 现金↓；负债↑ 现金↑ |

### 🔄 跨模块关联

- [[M02-Income-Statement]]：净利润是间接法起点
- [[M03-Balance-Sheet]]：资产负债科目变动是 CFO 关键调整项
- [[M10-Financial-Analysis-Techniques]]：现金流比率是偿债能力和盈利质量分析工具

### Migrated from `CFA_tier1/Financial_Statement_Analysis/M05-Analyzing-Cash-Flows-II.md`

_Alignment score: 0.61. Original official module field: M5: Analyzing Statements of Cash Flows II._

#### M05: 现金流量表分析 II (Analyzing Statements of Cash Flows II)

### 🌳 核心知识树

```text
🏆 FSA M05: Analyzing Statements of Cash Flows II（现金流量表分析 II）
│
├── ⭐ 报告式 vs 同比例现金流量表
│   ├── 报告式: CFO / CFI / CFF 三大分类
│   ├── 同比例: 各项目表示为收入或总现金流的%
│   └── 经营现金流占比持续下降 → 盈利质量恶化信号
│
├── ⭐ FCFF（公司自由现金流）
│   ├── 📐 FCFF = CFO + Interest(1-T) - FCInv
│   ├── 衡量对所有资本提供者的可供现金流
│   └── 用途: 企业价值评估 DCF 模型输入
│
├── ⭐ FCFE（股权自由现金流）
│   ├── 📐 FCFE = CFO - FCInv + Net Borrowing
│   ├── 衡量对普通股股东的可供现金流
│   └── 用途: 股权价值评估输入
│
├── ⭐ 现金流比率
│   ├── CFO / CL: 经营现金流覆盖短期债务
│   ├── CFO / Total Debt: 债务覆盖
│   ├── 现金流利润率: CFO / Revenue
│   └── ⚠️ 现金流比率不易被会计操纵，但波动更大
│
├── ⭐ 现金流趋势分析
│   ├── CFO 增长应匹配利润增长 — 背离暗示盈利质量下降
│   ├── CFO > NI → 盈利质量较高
│   └── FCFF/FCFE 长期为负 → 可能需要外部融资
│
├── 💡 关键洞察
│   ├── FCFF vs FCFE: FCFF 加回税后利息，FCFE 不加回
│   ├── FCInv 在 FCFF 和 FCFE 中都需扣减
│   ├── Net Borrowing 为正增加 FCFE，为负减少 FCFE
│   └── CFO 与 NI 背离是盈利质量分析重要线索
│
└── ⚠️ 考试陷阱总结
    ├── FCFF 加回税后利息；FCFE 不再加回
    ├── FCInv 是必需资本支出，两者都需扣减
    ├── 净借款方向: +新债 → +FCFE；-还债 → -FCFE
    └── 现金流比率 vs 利润比率: 不易操纵但波动大
```

### 📐 关键公式表

| 指标 | 公式 | 说明 |
|------|------|------|
| FCFF | `CFO + Interest(1-T) - FCInv` | 公司自由现金流 |
| FCFE | `CFO - FCInv + Net Borrowing` | 股权自由现金流 |
| CFO / CL | `CFO / Current Liabilities` | 经营现金流比率，短期偿债 |
| Cash Flow Margin | `CFO / Revenue` | 现金流利润率 |

### 🛠️ 常见考点与解题思路

**考点1：FCFF/FCFE 计算与区别**
- FCFF 给所有资本提供者，FCFE 只给股东。

**考点2：现金流比率的计算与解读**
- CFO 比率比利润比率更真实，不易被操纵。

**考点3：同比例现金流量表分析**
- 关注各分类现金流占比趋势，尤其是经营现金流。

**考点4：现金流与盈利质量**
- CFO 与 NI 长期背离是盈利质量分析的重要线索。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| FCFF 和 FCFE 调整相同 | FCFF 加回税后利息；FCFE 不加回 |
| FCInv 只在 FCFF 中扣减 | 两者都需扣减 FCInv |
| Net Borrowing 总是增加 FCFE | 偿还借款减少 FCFE |
| 现金流比率和利润比率相同 | 现金流比率不易操纵但波动更大 |

### 🔄 跨模块关联

- [[M04-Analyzing-Cash-Flows-I]]：FCFF/FCFE 以 CFO 为基础
- [[M11-Financial-Analysis-Techniques]]：现金流比率与 DuPont 分析互为补充
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
