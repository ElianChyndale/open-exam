---
title: "M02 — Analyzing Income Statements"
description: "CFA Level I 2026 official module: Analyzing Income Statements"
module: M02
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 2: Analyzing Income Statements"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M02: Analyzing Income Statements

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Analyzing Income Statements
- 2.01 | Introduction
- 2.02 | Revenue Recognition
- 2.03 | Expense Recognition
- 2.04 | Non-Recurring Items
- 2.05 | Earnings per Share
- 2.06 | Income Statement Ratios and Common-Size Analysis

## Learning Outcome Statements

The candidate should be able to:

- describe general principles of revenue recognition, specific revenue recognition applications, and implications of revenue recognition choices for financial analysis
- describe general principles of expense recognition, specific expense recognition applications, implications of expense recognition choices for financial analysis and contrast costs that are capitalized versus those that are expensed in the period in which they are incurred
- describe the financial reporting treatment and analysis of non-recurring items (including discontinued operations, unusual or infrequent items) and changes in accounting policies
- describe how earnings per share is calculated and calculate and interpret a company’s basic and diluted earnings per share for companies with simple and complex capital structures including those with antidilutive securities
- evaluate a company’s financial performance using common-size income statements and financial ratios based on the income statement

## 🌳 核心知识树

```text
🏆 【利润表分析】
│
├── 🔷 收入确认（Revenue Recognition）
│   ├── IFRS 15 / ASC 606 五步模型 🎯
│   │   ├── 识别合同 → 识别履约义务 → 确定交易价格
│   │   └── 分摊价格 → 履行义务时确认收入
│   ├── 控制权转移（control transfer）是确认时点
│   ├── 特定应用：
│   │   ├── 长期工程合同：完工百分比法 vs 全部完工法
│   │   ├── 分期收款销售：按收款进度确认毛利
│   │   └── 捆绑销售：分摊交易价格至各履约义务
│   └── ⚠️ 提前确认收入 → 高估当期利润、低估未来增长
│
├── 🔷 费用确认（Expense Recognition）
│   ├── 配比原则（Matching Principle）：费用与收入的同期配比
│   ├── 资本化 vs 费用化 🎯
│   │   ├── 资本化：记为资产 → 使用年限内摊销
│   │   └── 费用化：发生当期全额计入费用
│   └── ⚠️ 资本化只是费用时点后移，不改变经济实质
│       └── 前期利润更高 → 后期面临摊销压力
│
├── 🔷 非常项目与政策变更（Unusual Items）
│   ├── 终止经营：与持续经营分开列报 🎯
│   ├── 非常/偶发项目：性质特殊且不经常发生
│   └── 会计政策变更：追溯调整（retrospective）
│       └── 会计估计变更：未来适用法（prospective）⚠️
│
├── 🔷 每股收益（EPS）📐
│   ├── Basic EPS = (NI - Pref Div) / Weighted Avg Shares
│   ├── Diluted EPS 考虑可转债、期权、权证
│   ├── 简单结构 → Basic EPS；复杂结构 → Diluted EPS
│   └── ⚠️ 反稀释证券不纳入计算（转换后 EPS 上升则排除）
│
├── 🔷 同比例分析与利润表比率
│   ├── 所有项目表示为收入的百分比 → 消除规模差异
│   ├── 核心比率：毛利率 / 营业利润率 / 净利润率 📐
│   └── 跨公司和跨期间比较的基础工具
│
│   💡 核心洞察：利润表的应计制性质意味着利润 ≠ 现金流
│   🎯 高频考点：EPS 计算、收入确认时点、资本化 vs 费用化
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Basic EPS = (NI - Pref Div) / Weighted Avg Shares` | 基础每股收益 | 简单资本结构 | 使用**加权平均**流通股数，非期末数 |
| `Diluted EPS = (NI - Pref Div + Conv. Interest(1-t)) / (WAS + Dilutive Shares)` | 稀释每股收益 | 复杂资本结构 | 分子分母**同步调整**；仅纳入稀释性证券 |
| `Gross Margin = Gross Profit / Revenue` | 毛利率 | 核心盈利能力 | 受存货计价方法直接影响 |
| `Operating Margin = Operating Income / Revenue` | 营业利润率 | 经营效率 | 排除融资和税务影响 |
| `Net Margin = Net Income / Revenue` | 净利润率 | 最终盈利水平 | 包含所有项目（含非常项目） |
| `Revenue - COGS = Gross Profit` | 毛利计算 | 基础盈利分析 | COGS 取决于存货方法（FIFO/LIFO） |
| `EBIT = Revenue - COGS - Operating Expenses` | 息税前利润 | 利息覆盖率和经营分析 | 不包括利息和所得税 |

## 🛠️ 常见考点与解题思路

### 主题1：EPS 计算（🎯 高频计算题）
- **题型**：给出 NI、优先股股利、期初期末股数、可转债等数据，求 Basic/Diluted EPS
- **解题步骤（Basic EPS）**：
  1. 确认分子：NI - 优先股股利
  2. 计算分母：期初和期末流通股数的**加权平均**（注意时间权重）
  3. 分子 / 分母 = Basic EPS
- **解题步骤（Diluted EPS）**：
  1. 从 Basic EPS 出发
  2. 对分子：加回可转债的税后利息（Interest × (1-t)）
  3. 对分母：加回因期权/权证/可转债转换增加的股数（库藏股法）
  4. 先**单独测试**每种潜在稀释证券 — 若转换后 EPS 上升则为反稀释，**排除**
  5. 计算 Diluted EPS

### 主题2：收入确认时点的影响
- **题型**：描述收入确认政策变化，问对报表和比率的影响
- **解题思路**：
  - 提前确认 → 当期收入↑、资产↑、利润↑ → 下期收入↓、增长放缓
  - 延迟确认 → 当期收入↓、资产↓、利润↓ → 下期收入↑（累积释放）
  - 对现金流：收入确认时点**不直接影响现金流**（仅影响应计项目）

### 主题3：资本化 vs 费用化的比率影响
- **解题框架**：
  | 比率 | 资本化（前期）| 费用化 |
  |------|:----------:|:-----:|
  | ROA / ROE | 更高 | 更低 |
  | Asset Turnover | 更低 | 更高 |
  | Interest Coverage | 更高 | 更低 |
  | CFO | 更高（利息归类经营）| 不影响 |

### 主题4：终止经营的分析处理
- **题型**：问应如何分析包含终止经营的利润表
- **解题思路**：持续经营业务和终止经营必须分开分析 — 估值时**仅使用**持续经营数据

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 计算 EPS 使用期末流通股数 | 使用**加权平均**流通股数 | 股数在全年的变动需按时间权重调整 |
| 所有稀释证券都纳入 Diluted EPS | 仅**稀释性**证券纳入，反稀释证券排除 | 反稀释证券转换后 EPS 反而上升 |
| 资本化的费用比费用化的"更好" | 资本化仅延迟费用确认，不改变经济实质 | 后期面临更高的折旧/摊销费用 |
| 终止经营的损失应计入估值模型 | 终止经营的业绩应从持续经营分析中**剔除** | 终止经营不代表未来持续业绩 |
| 非常项目与终止经营可互换使用 | 两者性质不同 — 分类不可混淆 | 终止经营已处置/待售；非常项目偶发但仍在持续经营中 |
| 收入确认时点影响现金流 | 收入确认是应计制概念，不直接影响现金流 | 现金流取决于实际收付，而非确认时点 |

## 🔄 跨模块关联

- **[[M03-Analyzing-Balance-Sheets]]** — 利润表中的净利润通过留存收益连接资产负债表；资本化/费用化决策影响资产账面价值
- **[[M04-Analyzing-Statements-of-Cash-Flows-I]]** — 净利润是间接法计算 CFO 的起点；非现金费用（折旧摊销）在利润表中确认后在现金流量表中加回
- **[[M06-Analysis-of-Inventories]]** — 存货计价方法（FIFO/LIFO）直接影响 COGS 和毛利率；存货减记影响当期利润
- **[[M07-Analysis-of-Long-Term-Assets]]** — 资本化的资产通过折旧/摊销影响各期利润；减值损失直接计入利润表
- **[[M10-Financial-Reporting-Quality]]** — 收入确认激进程度和费用资本化程度是盈利质量（earnings quality）的核心判断依据
- **[[M11-Financial-Analysis-Techniques]]** — 利润表数据是盈利比率（profitability ratios）的输入；同比例利润表是跨期比较的基础工具

## 📋 复习与刷题提示

- **计算题优先**：Basic EPS 和 Diluted EPS 的计算是必考题型，务必熟练掌握加权平均股数的计算方法和稀释调整
- **概念辨析**：区分 discontinued operations（终止经营）、unusual/infrequent items（非常项目）、accounting policy changes（会计政策变更）和 accounting estimate changes（会计估计变更）的处理方式差异
- **比率分析**：掌握毛利率、营业利润率、净利润率的计算和解读，理解同比例利润表的编制方法
- **情境判断**：能够判断收入确认政策是否激进、资本化决策对关键财务比率的影响方向
- **跨准对比**：虽然本模块不强调 IFRS vs US GAAP 差异，但在收入确认（合同履约义务）和研发费用资本化方面存在差异
- **反稀释测试**：务必理解"每项潜在稀释证券单独测试，反稀释则排除"的原则
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
