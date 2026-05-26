---
title: "M06 — Capital Structure"
description: "CFA Level I 2026 official module: Capital Structure"
module: M06
subject: "Corporate Issuers"
topic_area: Corporate_Issuers
curriculum_year: 2026
official_module: "Module 6: Capital Structure"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Corporate_Issuers
  - official_2026
---

# M06: Capital Structure

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Capital Structure
- 6.01 | Introduction
- 6.02 | The Cost of Capital
- 6.03 | Factors Affecting Capital Structure
- 6.04 | Modigliani–Miller Capital Structure Propositions
- 6.05 | Optimal Capital Structure

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret the weighted-average cost of capital for a company
- explain factors affecting capital structure and the weighted-average cost of capital
- explain the Modigliani-Miller propositions regarding capital structure
- describe optimal and target capital structures

## Local Study Notes

### Migrated from `CFA_tier1/Corporate_Issuers/M06-Capital-Structure-and-Leverage.md`

_Alignment score: 1.00. Original official module field: Module 6: Capital Structure._

#### M07: Capital Structure and Leverage（资本结构与杠杆）

### 🌳 核心知识树

```text
🏆 Corp M06: Capital Structure（资本结构与杠杆）
│
├── ⭐ 经营杠杆 (Operating Leverage)
│   ├── 来自固定经营成本 → 销售变化放大 EBIT 变化
│   ├── 📐 DOL = %ΔEBIT / %ΔSales
│   ├── 📐 DOL = (Sales - VC) / EBIT
│   └── 高 DOL → 盈亏平衡点高，销售波动显著影响利润
│
├── ⭐ 财务杠杆 (Financial Leverage)
│   ├── 来自固定融资成本（债务利息）
│   ├── 📐 DFL = %ΔEPS / %ΔEBIT
│   ├── 📐 DFL = EBIT / (EBIT - Interest)
│   └── EBIT 变化被固定利息放大为 EPS 更大变化
│
├── ⭐ 总杠杆 (Total Leverage)
│   ├── 📐 DTL = DOL × DFL
│   ├── 📐 DTL = %ΔEPS / %ΔSales
│   └── 销售端波动经两级杠杆传导至 EPS
│
├── ⭐ 经营风险 vs 财务风险
│   ├── 经营风险: 行业特性和成本结构（与融资无关）
│   ├── 财务风险: 资本结构中的债务比例
│   └── 两者叠加 = 公司整体风险
│
├── ⭐ 结构权衡
│   ├── 债务税盾: 利息可税前扣除 → 增加公司价值
│   ├── 财务困境成本: 违约风险 → 直接+间接成本
│   ├── 灵活性损失: 高债务限制市场机会响应
│   └── ⚠️ 债务税盾不是只有好处
│
├── ⭐ MM 理论
│   ├── MM 无税: 资本结构不影响公司价值（理想世界）
│   ├── MM 有税: 债务税盾增加公司价值 (VL = VU + tD)
│   ├── 权衡理论: 平衡税盾与财务困境成本
│   └── 优序融资理论: 内源 > 债务 > 股权
│
├── 💡 关键洞察
│   ├── 高 ROE 可能只是高风险的伪装
│   ├── DOL 来自成本结构，DFL 来自融资结构
│   ├── DTL = DOL × DFL（乘法而非加法）
│   └── 真实世界税收、破产成本、代理成本使资本结构至关重要
│
└── ⚠️ 考试陷阱总结
    ├── 杠杆推高的 ROE 不代表更好的经营表现
    ├── DOL 和 DFL 不可混淆
    ├── MM 无税是理想基准，现实不同
    ├── 债务税盾同时带来困境风险和灵活性损失
    └── 总杠杆是乘数效应 — DTL = DOL × DFL
```

## 📖 知识点详解

### 知识点1：杠杆机制 (Leverage Mechanics)

**核心概念**：杠杆是使用固定成本放大收益和亏损的机制。经营杠杆来自固定经营成本，财务杠杆来自固定融资成本（债务利息）。总杠杆是两者的叠加乘数效应，将销售端的波动传导至每股收益（EPS）。

- **经营杠杆度 (DOL)** = %ΔEBIT / %ΔSales，衡量销售额变动对EBIT的放大效应。高固定成本→高DOL→盈亏平衡点高
- **财务杠杆度 (DFL)** = %ΔEPS / %ΔEBIT，衡量EBIT变动对EPS的放大效应。债务利息固定→EBIT变动被放大为更大的EPS变动
- **总杠杆度 (DTL)** = DOL × DFL = %ΔEPS / %ΔSales。两级杠杆的乘数叠加效应
- 📐 DOL = (Sales - VC) / EBIT；DFL = EBIT / (EBIT - Interest)；DTL = DOL × DFL
- 💡 **核心区分**：DOL来自成本结构（卖什么、怎么卖），DFL来自融资结构（钱哪来的）。两者不可混淆

**考试应用**：计算DOL/DFL/DTL是必考题型。给定财务数据，用公式计算各级杠杆度。注意：高ROE可能只是高风险的伪装（杠杆推高ROE伴随更高风险）。

### 知识点2：结构权衡 (Structure Trade-Offs)

**核心概念**：最优资本结构不存在统一公式，需要在债务税盾、财务困境成本和灵活性损失之间权衡。MM理论提供了基准框架——无税时资本结构不影响公司价值，有税时债务税盾增加价值。

- **债务税盾 (Debt Tax Shield)**：利息可税前扣除，减少税负，增加公司价值
- **财务困境成本 (Financial Distress Cost)**：债务过高导致违约风险上升，产生直接（法律费用）和间接（客户流失、供应商收紧）成本
- **灵活性损失 (Loss of Flexibility)**：高债务限制公司响应市场机会的能力
- **MM理论**：
  - MM无税：资本结构不影响公司价值（理想世界基准）
  - MM有税：债务税盾增加公司价值
  - 权衡理论 (Trade-Off Theory)：最优资本结构平衡税盾收益与困境成本
  - 优序融资理论 (Pecking Order Theory)：公司偏好内部融资>债务>股权
- 🎯 **高频考点**：影响债务容量的因素——经营风险越低、有形资产越多、盈利越稳定，债务容量越大

**考试应用**：给定公司特征（如高税率、低经营风险），判断应多用债务还是权益。高税率→税盾价值大→适合债务；低经营风险→债务容量大→适合债务。

### 📐 关键公式表

| 指标 | 公式 | 说明 |
|------|------|------|
| 经营杠杆度 (DOL) | `%ΔEBIT / %ΔSales` 或 `(Sales-VC)/EBIT` | 衡量经营杠杆 |
| 财务杠杆度 (DFL) | `%ΔEPS / %ΔEBIT` 或 `EBIT/(EBIT-Interest)` | 衡量财务杠杆 |
| 总杠杆度 (DTL) | `DOL × DFL` 或 `%ΔEPS / %ΔSales` | 两级杠杆总效应 |
| 盈亏平衡点 | `Fixed Costs / (Price - VC per unit)` | 利润为零的销售量 |

### 🛠️ 常见考点与解题思路

**考点1：计算 DOL、DFL、DTL**
- 先算 EBIT = 销售额 - 变动成本 - 固定成本
- DOL = (Sales - VC) / EBIT，DFL = EBIT / (EBIT - Interest)

**考点2：判断杠杆类型**
- 销售→EBIT 的变化 = DOL；EBIT→EPS 的变化 = DFL

**考点3：理解 MM 理论**
- MM 无税：资本结构不影响公司价值
- MM 有税：债务税盾增加价值

**考点4：债务 vs 权益选择**
- 高税率 → 税盾价值大 → 适合债务
- 低经营风险 → 债务容量大 → 适合债务

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| 高 ROE = 经营好 | 杠杆推高的 ROE 可能伴随更高风险 |
| DOL 和 DFL 概念相同 | DOL 来自成本结构，DFL 来自融资结构 |
| 现实与 MM 无税世界一致 | 税收/破产/代理等摩擦使资本结构重要 |
| 债务税盾只有好处 | 同时带来困境风险和灵活性损失 |
| 总杠杆是加法效应 | DTL = DOL × DFL（乘法效应）|

### 🔄 跨模块关联

- 资本结构影响 WACC → [[M05-Cost-of-Capital]]
- DOL 与商业模式 → [[M07-Business-Models]]
- 杠杆与资本预算 → [[M04-Capital-Investments]]
- 治理影响杠杆选择 → [[M02-Corporate-Governance-and-ESG]]
- 资本结构整合 → [[M08-Capital-Allocation-Integration]]
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.

## 📋 复习与刷题提示

- **核心公式**：WACC = wd·rd(1-t) + we·re；MM有税VL=VU+tD
- **高频考点**：MM定理（无税vs有税）、WACC计算、最优杠杆权衡
- **跨科目链接**：权益成本Re→Quant M10 CAPM；税盾→FI M14 信用风险
- **⏱ 时间管理**：WACC和MM定理相关计算题平均耗时3-5分钟，建议先做简单概念题
- **考试策略**：MM命题多为概念理解题（无税VU=VL，有税VL=VU+tD），计算WACC时可交叉验证Quant M10的Beta推算

### 跨科目学习链接
- **Quantitative Methods M10**: 回归中的 Beta 用于估算权益成本 Re（CAPM）
- **Fixed Income M14-M16**: 信用分析中的 D/E ratio、ICR 与资本结构选择直接关联
- **Financial Statement Analysis M09**: 税盾概念源于 DTA/DTL 的所得税分析
