---
title: "M04 — Analyzing Statements of Cash Flows I"
description: "CFA Level I 2026 official module: Analyzing Statements of Cash Flows I"
module: M04
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 4: Analyzing Statements of Cash Flows I"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M04: Analyzing Statements of Cash Flows I

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Analyzing Statements of Cash Flows I
- 4.01 | Introduction
- 4.02 | Linkages between the Financial Statements
- 4.03 | The Direct Method for Cash Flows from Operating Activities
- 4.04 | The Indirect Method for Cash Flows from Operating Activities
- 4.05 | Conversion from the Indirect to Direct Method
- 4.06 | Cash Flows from Investing Activities
- 4.07 | Cash Flows from Financing Activities
- 4.08 | Differences in Cash Flow Statements Prepared under US GAAP versus IFRS

## Learning Outcome Statements

The candidate should be able to:

- describe how the cash flow statement is linked to the income statement and the balance sheet
- describe the steps in the preparation of direct and indirect cash flow statements, including how cash flows can be computed using income statement and balance sheet data
- demonstrate the conversion of cash flows from the indirect to direct method
- contrast cash flow statements prepared under International Financial Reporting Standards (IFRS) and US generally accepted accounting principles (US GAAP)

## 🌳 核心知识树

```text
🏆 【现金流量表分析 I】
│
├── 🔷 三大报表联动（Three-Statement Linkage）🎯
│   ├── 现金增减 = 利润表经营活动 + 资产负债表项目变动
│   ├── 净利润 + 非现金调整 + 营运资本变动 = CFO
│   └── 资产负债科目的跨期变化体现在现金流各分类中
│
├── 🔷 现金流量三大分类
│   ├── CFO（经营活动）：日常经营产生的现金流 🎯
│   ├── CFI（投资活动）：购买/出售长期资产、投资 🎯
│   └── CFF（融资活动）：债务发行/偿还、股权融资、股利 🎯
│
├── 🔷 间接法（Indirect Method）📐
│   ├── 从净利润出发
│   ├── 加回非现金费用：折旧、摊销、减值损失
│   ├── 减去非现金收益：资产出售利得
│   └── 调整营运资本变动：
│       ├── 流动资产增加（用现金）→ 减项 ⚠️
│       └── 流动负债增加（收到现金）→ 加项 ⚠️
│
├── 🔷 直接法（Direct Method）📐
│   ├── 直接列示现金收入和现金支出
│   ├── IFRS 鼓励，US GAAP 两种均可
│   ├── 现金收款 = 收入 - 应收增加额
│   └── 现金付款 = 费用 + 应付减少额
│
├── 🔶 IFRS vs US GAAP 分类差异 🎯
│   ├── 利息支付：IFRS 可选经营/融资；US GAAP → 经营
│   ├── 股利支付：IFRS 可选经营/融资；US GAAP → 融资
│   ├── 利息/股利收入：IFRS 可选经营/投资；US GAAP → 经营
│   └── 银行透支：IFRS → 现金等价物；US GAAP → 融资
│
│   💡 核心洞察：直接法和间接法 CFO 金额**完全相同**，只是列示方式不同
│   🎯 高频考点：间接法调整项、IFRS vs US GAAP 分类、营运资本符号
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `CFO = NI + Noncash Charges - Noncash Gains +/- WC Changes` | 间接法 CFO | 从利润表出发编制 | **双向调整**：加回费用，减去收益 |
| `Cash Collected = Revenue - Increase in AR` | 直接法 - 现金收款 | 从收入推算现金收款 | AR 减少则加回 |
| `Cash Paid to Suppliers = COGS + Increase in Inv - Increase in AP` | 直接法 - 现金付款 | 从 COGS 推算现金付款 | 存货和应付同时调整 |
| `CFO (Direct) = Cash Collected - Cash Paid - Cash OpEx` | 直接法 CFO | 直接列示 | 结果应等于间接法 CFO |
| `FCF = CFO - Capital Expenditures` | 自由现金流 | 初步估值输入 | 在 M05 中深入展开 |
| `Interest Paid (US GAAP) = Operating; Interest Paid (IFRS) = Operating or Financing` | 利息分类 | 准则差异 | IFRS 允许管理层选择 |

## 🛠️ 常见考点与解题思路

### 主题1：间接法 CFO 计算（🎯 必考）
- **题型**：给出 NI、折旧、资产出售利得、AR/Inv/AP 变动等数据，求 CFO
- **解题步骤**：
  1. 从 NI 开始
  2. 加回所有非现金费用（折旧、摊销、减值损失、股票期权费用）
  3. 减去非现金收益（固定资产出售利得、投资利得）
  4. 调整营运资本：
     - **流动资产增加** → 现金减少 → CFO 中减去
     - **流动资产减少** → 现金增加 → CFO 中加回
     - **流动负债增加** → 现金增加 → CFO 中加回
     - **流动负债减少** → 现金减少 → CFO 中减去
  5. 汇总 = CFO

### 主题2：间接法 → 直接法转换
- **题型**：要求将间接法 CFO 转换为直接法格式
- **解题步骤**：
  1. 拆解间接法中的每个调整项
  2. 从利润表项目出发：收入 → 现金收款（调整 AR）；COGS → 现金付款（调整 Inv 和 AP）
  3. 分别列示现金收入和各现金支出类别

### 主题3：IFRS vs US GAAP 分类判断
- **解题方法**：记住"IFRS 灵活，US GAAP 固定"
  - US GAAP：利息 = 经营；股利支付 = 融资；股利收入 = 经营
  - IFRS：利息和股利均可选经营或融资/投资

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 间接法 CFO 是从现金收入开始计算 | 间接法从**净利润**出发，调整为现金基础 | 间接法是应计制 → 现金制的转换 |
| 只有非现金费用需加回 | 非现金**收益**也需调整（减去），双向调整 | 资产出售利得增加了 NI 但未增加现金 |
| AR 增加 → CFO 加回 | AR 增加 → CFO 中**减去** | 收入已确认但未收到现金 |
| AP 增加 → CFO 减去 | AP 增加 → CFO 中**加回** | 费用已确认但尚未支付现金 |
| 直接法和间接法 CFO 可能不同 | 两者 CFO 金额**必须相同** | 仅是列示格式不同，现金流量本质不变 |
| 银行透支总是融资活动 | IFRS 下银行透支可视为现金等价物的一部分 | 计入现金及现金等价物而非融资活动 |
| 折旧产生现金 | 折旧是**非现金费用**，不产生也不消耗现金 | 折旧在间接法中加回仅是为了消除其对 NI 的影响 |

## 🔄 跨模块关联

- **[[M02-Analyzing-Income-Statements]]** — 净利润是间接法 CFO 的起点；非现金费用（折旧、摊销）来源于利润表；非常项目需单独调整
- **[[M03-Analyzing-Balance-Sheets]]** — 资产负债表科目的变动（AR、Inv、AP、Accrued Liabilities）是 CFO 计算的关键调整项；资产购买/出售是 CFI 的基础
- **[[M05-Analyzing-Statements-of-Cash-Flows-II]]** — 本模块的 CFO 计算是 M05 自由现金流（FCFF/FCFE）和现金流比率分析的基础
- **[[M07-Analysis-of-Long-Term-Assets]]** — PP&E 的购买和出售记录在 CFI 中；折旧费用在间接法中加回
- **[[M09-Analysis-of-Income-Taxes]]** — 所得税支付在现金流表中的分类；递延所得税变动影响 CFO 调整

## 📋 复习与刷题提示

- **计算题必考**：间接法 CFO 的计算是 CFA L1 财务分析最高频题型之一。务必牢记营运资本调整的方向规则
- **分类题**：能够正确将交易分类至 CFO / CFI / CFF。注意 US GAAP 的规则性更强
- **陷阱题**：题干可能包含干扰项（如股票发行费用、可转债转换等非现金交易），需要识别哪些项目不涉及现金流
- **转换题**：间接法 → 直接法的转换是常见题型，理解每个调整项的对应关系
- **对比记忆**：IFRS vs US GAAP 分类差异可以用表格对比记忆，重点关注利息和股利的处理差异
- **常见干扰**：折旧是 CFO 的加回项；资产出售利得是 CFO 的减项；资产出售收入是 CFI 的流入
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
