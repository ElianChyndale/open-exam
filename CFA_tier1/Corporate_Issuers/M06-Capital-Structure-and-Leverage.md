---
title: "M06 — Capital Structure and Leverage"
description: 资本结构与杠杆 — DOL、DFL、债务容量、MM理论、结构权衡
module: M06
official_module: 6
subject: Corporate_Issuers
---

# M06: Capital Structure and Leverage（资本结构与杠杆）

## 1. 核心知识点

### 1.1 杠杆机制 (Leverage Mechanics)

杠杆是指**使用固定成本放大收益和亏损**的机制。分为两类：

- **经营杠杆 (Operating Leverage)**：来自固定经营成本。固定成本占比越高，销售额的微小变化就会引起 EBIT 的大幅变化。
  - **经营杠杆度 (Degree of Operating Leverage, DOL)** = `%ΔEBIT / %ΔSales`
  - 高 DOL 意味着公司盈亏平衡点高，销售波动会显著影响利润。

- **财务杠杆 (Financial Leverage)**：来自固定融资成本（如债务利息）。EBIT 的变化会被固定利息费用放大为更大的 EPS 变化。
  - **财务杠杆度 (Degree of Financial Leverage, DFL)** = `%ΔEPS / %ΔEBIT`

- **总杠杆 (Total Leverage)** = **DOL × DFL**
  - **总杠杆度 (Degree of Total Leverage, DTL)** = `%ΔEPS / %ΔSales`
  - 体现了**销售端的波动如何被两级杠杆传导至每股收益 (EPS)**。

**经营风险 (Business Risk)** vs **财务风险 (Financial Risk)**：
- 经营风险取决于行业特性和成本结构（与融资方式无关）
- 财务风险取决于资本结构中的债务比例
- 两者叠加决定公司的**整体风险 (total risk)**

### 1.2 结构权衡 (Structure Trade-Offs)

理论上最优资本结构不存在统一公式，但需要理解以下权衡：

- **债务税盾 (Debt Tax Shield)**：利息可税前扣除，减少税负，增加公司价值。
- **财务困境成本 (Financial Distress Cost)**：债务过高导致违约风险上升，产生直接（法律费用）和间接（客户流失、供应商收紧）成本。
- **灵活性损失 (Loss of Flexibility)**：高债务水平限制公司响应市场机会的能力。

**影响债务容量 (Debt Capacity) 的因素**：
- **经营风险 (Business Risk)**：经营风险越高，债务容量越低
- **资产类型**：有形资产多的公司更容易获得债务融资（可抵押）
- **盈利稳定性**：现金流稳定可支撑更多债务

**MM 理论 (Modigliani-Miller Propositions)** 提供了基准框架：
- **MM 无税 (No Tax)**：资本结构不影响公司价值（理想世界）
- **MM 有税 (With Tax)**：债务税盾增加公司价值
- 真实世界中，权衡理论 (Trade-Off Theory) 和**优序融资理论 (Pecking Order Theory)** 提供了更现实的视角

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| 经营杠杆度 (DOL) | `%ΔEBIT / %ΔSales` | 衡量经营杠杆 |
| 财务杠杆度 (DFL) | `%ΔEPS / %ΔEBIT` | 衡量财务杠杆 |
| 总杠杆度 (DTL) | `DOL × DFL` 或 `%ΔEPS / %ΔSales` | 两级杠杆总效应 |
| 盈亏平衡点 | `Fixed Costs / (Price - Variable Cost per unit)` | 利润为零的销售量 |

## 3. 常见考点与解题思路

**考点 1：计算 DOL、DFL、DTL**
- 给定财务数据（如销售额、变动成本、固定成本、利息费用），求各杠杆度。
- 解题步骤：
  1. 计算 EBIT = 销售额 - 变动成本 - 固定成本
  2. 计算 EPS 或净利润
  3. 用百分比变化公式计算 DOL、DFL、DTL
  4. 或用公式：`DOL = (Sales - Variable Costs) / EBIT`，`DFL = EBIT / (EBIT - Interest)`

**考点 2：判断杠杆类型**
- 题目描述一种风险（如"销售下降 10% 导致 EBIT 下降 20%"），问这是何种杠杆。
- 答案：DOL = 2，属于经营杠杆效应。

**考点 3：理解 MM 理论**
- 题目问：在无税无摩擦的世界中，增加债务比例有何影响？
- 答案：不影响公司价值（MM Proposition I 无税）。但会提高股权成本和股权 β。

**考点 4：债务 vs 权益选择**
- 题目描述公司特征（如高盈利、高税率、低经营风险），问应多用债务还是权益。
- 思路：高税率 → 税盾价值大 → 适合债务。低经营风险 → 债务容量大 → 适合债务。

## 4. 易错点提醒

- **高 ROE 可能只是高风险的伪装**：**杠杆推高的 ROE 可能伴随着更高的风险，并不一定代表更好的经营表现。**
- **DOL 和 DFL 是两个不同的概念**：一个来自成本结构（卖什么、怎么卖），一个来自融资结构（钱哪来的）。两者不可混淆。
- **MM 无税世界中资本结构不重要**：这只是理想世界的基准，真实世界中税收、破产成本、代理成本使资本结构至关重要。
- **债务税盾不是只有好处**：同时带来财务困境风险和灵活性损失。
- **DTL = DOL × DFL**：总杠杆的乘数效应意味着两级杠杆叠加是乘法而非加法。

## 5. 跨模块关联

- 资本结构影响 WACC → [[M05-Cost-of-Capital]] 债务权重和股权成本随杠杆变化
- DOL 与商业模式 → [[M07-Business-Models]] 固定/变动成本结构决定经营杠杆水平
- 杠杆与资本预算 → [[M04-Capital-Investments]] 项目选择应考虑其对整体杠杆水平的影响
- 治理影响杠杆选择 → [[M02-Corporate-Governance-and-ESG]] 管理层可能选择次优杠杆以降低个人风险
- 资本结构整合 → [[M08-Capital-Allocation-Integration]] 融资决策是资本配置的一部分
