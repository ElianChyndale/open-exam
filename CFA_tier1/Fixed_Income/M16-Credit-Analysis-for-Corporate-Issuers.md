---
title: "M16 — Credit Analysis for Corporate Issuers"
description: "CFA Level I 2026 official module: Credit Analysis for Corporate Issuers"
module: M16
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 16: Credit Analysis for Corporate Issuers"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M16: Credit Analysis for Corporate Issuers

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Credit Analysis for Corporate Issuers
- 16.01 | Introduction
- 16.02 | Assessing Corporate Creditworthiness
- 16.03 | Financial Ratios in Corporate Credit Analysis
- 16.04 | Seniority Rankings, Recovery Rates, and Credit Ratings

## Learning Outcome Statements

The candidate should be able to:

- describe the qualitative and quantitative factors used to evaluate a corporate borrower's creditworthiness
- calculate and interpret financial ratios used in credit analysis
- describe the seniority rankings of debt, secured versus unsecured debt and the priority of claims in bankruptcy, and their impact on credit ratings

## 🌳 核心知识树

```text
🏆 M16: Credit Analysis for Corporate Issuers（公司发行人信用分析）
├─ ⭐ 16.1 三支柱框架 (Three Pillars)
│  ├─ 📐 商业风险 (Business Risk)
│  │  ├─ 行业特征：周期型 vs 防御型、进入壁垒、监管环境
│  │  └─ 竞争地位：市场份额、定价能力、产品多元化
│  ├─ 📐 财务风险 (Financial Risk)
│  │  ├─ 杠杆率：Debt/EBITDA
│  │  ├─ 覆盖率：EBITDA/Interest, EBIT/Interest
│  │  └─ 现金流稳定性：FCF、营运资金管理
│  └─ 📐 治理与结构 (Governance & Structure)
│     ├─ 管理层质量、所有权结构
│     └─ 关联交易、股东友好度（股息政策）
│
├─ ⭐ 16.2 核心定量指标
│  ├─ 📐 ICR = EBIT (或 EBITDA) / Interest Expense
│  ├─ 📐 Leverage = Debt / EBITDA
│  ├─ 📐 Debt/Capital = Total Debt / (Total Debt + Total Equity)
│  ├─ 📐 FCF = CFO - CapEx - Preferred Dividends
│  └─ ⚠️ ICR 用 EBIT 还是 EBITDA 影响大（EBITDA 更高）
│
├─ ⭐ 16.3 优先级与清偿顺序
│  ├─ 📐 担保债务 (Secured) > 优先无担保 > 次级 (Subordinated)
│  ├─ 🎯 回收率：优先级担保 > 优先级无担保 > 次级
│  └─ ⚠️ 同一发行人的不同债项可能有不同评级
│
└─ ⭐ 16.4 评级差异化 (Notching)
   ├─ 💡 根据担保、优先级、回收率预期调整 1-3 级
   ├─ 💡 Issue rating ≠ Issuer rating
   └─ ⚠️ 为投资者提供更精细的信用风险区分
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `ICR = EBIT / Interest Expense` | 利息覆盖率 | 衡量偿债能力 | EBITDA 版本更高 |
| `Leverage = Debt / EBITDA` | 杠杆率 | 衡量债务负担 | 越低越好 |
| `Debt/Capital = TD / (TD + TE)` | 债务资本比 | 衡量资本结构 | 行业差异大 |
| `FCF = CFO - CapEx - Preferred Div` | 自由现金流 | 衡量财务灵活性 | 负值可能预示问题 |

## 🛠️ 常见考点与解题思路

### 考点 1：计算和解读覆盖率
- **ICR 越低 → 信用风险越高**
- **注意**：题目是否使用 EBIT 还是 EBITDA
  - EBITDA-based ICR > EBIT-based ICR（因为 EBITDA > EBIT）
  - **判断规则**：如果题目同时给出两者，留意上下文提示哪个更相关

### 考点 2：区分 Issuer Rating vs Issue Rating
- **Issuer rating**：发行人的整体偿债能力评级
- **Issue rating**：具体债项的评级（因担保、优先级不同而不同）
- **Notching**：在同一发行人评级基础上调整 1-3 级

### 考点 3：区分 Secured vs Unsecured、Senior vs Subordinated
- **Secured**：有特定资产作为抵押品，破产时优先从该资产受偿
- **Senior unsecured**：无抵押，但破产时优先于次级
- **Subordinated**：次于所有高级债务受偿

### 考点 4：回收率预期
- **破产清算顺序**：有担保债权人 → 优先无担保 → 次级 → 股东
- **回收率**：优先级担保（50-80%）> 优先无担保（30-60%）> 次级（10-30%）

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| ICR 用 EBIT 还是 EBITDA 一样 | EBITDA 更大，ICR 更高 | 折旧摊销差异 |
| 发行人评级 = 所有债项评级 | 不同债项可能因担保和优先级不同 | Issue rating 可调整 |
| Secured 一定安全 | 抵押品价值可能不足 | 需关注 LTV 和抵押品质量 |
| Subordinated 一定无法回收 | 回收率低但仍有部分回收可能 | 非完全损失 |

## 🔄 跨模块关联

- **PD/LGD 框架** → [[M14-Credit-Risk]] 信用风险度量基础
- **政府信用对比** → [[M15-Credit-Analysis-for-Government-Issuers]] 政府与公司信用分析对比
- **担保/契约/优先级** → [[M01-Fixed-Income-Instrument-Features]] 基本概念
- **信用增级** → [[M18-Asset-Backed-Security-Instrument-and-Market-Features]] 结构化信用增级
- **融资市场** → [[M04-Fixed-Income-Markets-for-Corporate-Issuers]] 公司发行人融资背景

## 📋 复习与刷题提示

- **核心重点**：ICR 和杠杆率的计算与解读
  - ICR = EBIT (或 EBITDA) / Interest Expense
  - Leverage = Debt / EBITDA
  - Debt/Capital = TD / (TD + TE)
  - FCF = CFO - CapEx - Preferred Dividends
- **三支柱框架**：
  1. 商业风险：行业周期型/防御型、竞争地位、定价能力
  2. 财务风险：杠杆、覆盖率、现金流稳定性、再融资渠道
  3. 治理与结构：管理层质量、所有权、关联交易
- **优先级与清偿顺序**：
  - 担保债务 (Secured) → 回收率 50-80%
  - 优先无担保 (Senior Unsecured) → 回收率 30-60%
  - 次级 (Subordinated) → 回收率 10-30%
  - 股东权益 → 通常不回收
- **评级区分**：
  - Issuer rating：发行人整体偿债能力
  - Issue rating：具体债项评级（可因担保品调整 1-3 notch）
  - Notching：在同一发行人评级基础上差异化调整
- **典型计算流程**：
  1. EBIT = $500M，Interest = $100M
  2. ICR = 500/100 = 5.0x（安全，通常 > 3x 为投资级水平）
  3. Debt = $2B，EBITDA = $800M
  4. Leverage = 2000/800 = 2.5x（较低，通常 < 3x 为投资级水平）
- **刷题建议**：
  - 重点做财务比率计算题（ICR、Leverage 等）
  - 清偿优先级分析题（破产时谁先受偿）
  - Issuer vs Issue rating 辨析题
- **易混淆点**：
  - ICR 用 EBIT vs EBITDA 差异很大
  - Secured 不保证全额回收（抵押品价值可能不足）
  - 同一发行人不同债项评级可能不同

- **关键数值记忆**：
  - ICR = EBIT / Interest Expense（> 3x 为 IG 水平）
  - Leverage = Debt / EBITDA（< 3x 为 IG 水平）
  - Debt/Capital = TD / (TD + TE)
  - FCF = CFO - CapEx - Preferred Dividends
- **财务比率行业差异**：
  - 防御型行业（公用事业）可接受更高杠杆
  - 周期型行业（制造）需要更低的杠杆和更高的覆盖率
  - 科技/医药行业：高利润率但轻资产，杠杆通常较低
- **评级 Notching 规则**：
  - Secured 担保债：Issuer rating + 1-2 notches
  - Senior Unsecured：Issuer rating（基准）
  - Subordinated：Issuer rating - 1-2 notches
  - 极端情况下差 3 个 notch 以上
- **商业风险 vs 财务风险**：
  - 商业风险高（强周期行业）= 需要财务风险低（低杠杆）
  - 商业风险低（公用事业）= 可接受财务风险高（高杠杆）
  - 两者互补决定总信用风险
- **考试技巧**：
  - ICR 计算注意 EBIT vs EBITDA 
  - 担保 ≠ 无风险（抵押品价值可能不足）
  - 同一公司不同债项评级可能因担保和优先级差异大
