---
title: "M06: Capital Structure"
description: "CFA Level I 2026 Corporate Issuers 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Corporate Issuers"
topic_area: "Corporate_Issuers"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M06"
official_module: "Module 6: Capital Structure"
los_count: 4
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Corporate_Issuers
---

# M06: Capital Structure

> **模块定位**：理解公司组织、治理、营运资本、资本配置与商业模式如何影响价值创造。 本模块聚焦 **Capital Structure**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Capital Structure
- 6.01 | Introduction
- 6.02 | The Cost of Capital
- 6.03 | Factors Affecting Capital Structure
- 6.04 | Modigliani–Miller Capital Structure Propositions
- 6.05 | Optimal Capital Structure

## Learning Outcome Statements

1. calculate and interpret the weighted-average cost of capital for a company
2. explain factors affecting capital structure and the weighted-average cost of capital
3. explain the Modigliani-Miller propositions regarding capital structure
4. describe optimal and target capital structures

---

## 1. 模块定位

### 6.1 学习任务
- **核心问题**：考试希望你用 `Capital Structure` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 6.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 6.3 关键英文术语
- **Capital Structure（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **The Cost of Capital（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Factors Affecting Capital Structure（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Modigliani–Miller Capital Structure Propositions（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Optimal Capital Structure（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 6.1 | calculate and interpret the weighted-average cost of capital for a company | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |
| 6.2 | explain factors affecting capital structure and the weighted-average cost of capital | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 6.3 | explain the Modigliani-Miller propositions regarding capital structure | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 6.4 | describe optimal and target capital structures | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
6. Capital Structure
├─ 6.1 杠杆机制 (Leverage Mechanics)
│  ├─ 6.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 6.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 6.2 结构权衡 (Structure Trade-Offs)
│  ├─ 6.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 6.2.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 6.1 杠杆机制 (Leverage Mechanics)

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

### 6.2 结构权衡 (Structure Trade-Offs)

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

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 | 说明 |
|------|------|------|
| 经营杠杆度 (DOL) | `%ΔEBIT / %ΔSales` | 衡量经营杠杆 |
| 财务杠杆度 (DFL) | `%ΔEPS / %ΔEBIT` | 衡量财务杠杆 |
| 总杠杆度 (DTL) | `DOL × DFL` 或 `%ΔEPS / %ΔSales` | 两级杠杆总效应 |
| 盈亏平衡点 | `Fixed Costs / (Price - Variable Cost per unit)` | 利润为零的销售量 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 6.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 6.2 The Cost of Capital | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.3 Factors Affecting Capital Structure | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 6.4 Modigliani–Miller Capital Structure Propositions | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐ | 6.5 Optimal Capital Structure | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

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

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：高 ROE 可能只是高风险的伪装：杠杆推高的 ROE 可能伴随着更高的风险，并不一定代表更好的经营表现。 | ✅ 高 ROE 可能只是高风险的伪装：杠杆推高的 ROE 可能伴随着更高的风险，并不一定代表更好的经营表现。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：DOL 和 DFL 是两个不同的概念：一个来自成本结构（卖什么、怎么卖），一个来自融资结构（钱哪来的）。两者不可混淆。 | ✅ DOL 和 DFL 是两个不同的概念：一个来自成本结构（卖什么、怎么卖），一个来自融资结构（钱哪来的）。两者不可混淆。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：MM 无税世界中资本结构不重要：这只是理想世界的基准，真实世界中税收、破产成本、代理成本使资本结构至关重要。 | ✅ MM 无税世界中资本结构不重要：这只是理想世界的基准，真实世界中税收、破产成本、代理成本使资本结构至关重要。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：债务税盾不是只有好处：同时带来财务困境风险和灵活性损失。 | ✅ 债务税盾不是只有好处：同时带来财务困境风险和灵活性损失。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：DTL = DOL × DFL：总杠杆的乘数效应意味着两级杠杆叠加是乘法而非加法。 | ✅ DTL = DOL × DFL：总杠杆的乘数效应意味着两级杠杆叠加是乘法而非加法。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M05-Capital-Investments-and-Capital-Allocation]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M07-Business-Models]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 资本结构影响 WACC → [[M05-Cost-of-Capital]] 债务权重和股权成本随杠杆变化
- DOL 与商业模式 → [[M07-Business-Models]] 固定/变动成本结构决定经营杠杆水平
- 杠杆与资本预算 → [[M04-Capital-Investments]] 项目选择应考虑其对整体杠杆水平的影响
- 治理影响杠杆选择 → [[M02-Corporate-Governance-and-ESG]] 管理层可能选择次优杠杆以降低个人风险
- 资本结构整合 → [[M08-Capital-Allocation-Integration]] 融资决策是资本配置的一部分


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M06-Capital-Structure-and-Leverage.md` (medium, 0.394)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
