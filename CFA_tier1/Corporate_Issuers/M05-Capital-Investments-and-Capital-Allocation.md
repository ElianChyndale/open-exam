---
title: "M05: Capital Investments and Capital Allocation"
description: "CFA Level I 2026 Corporate Issuers 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Corporate Issuers"
topic_area: "Corporate_Issuers"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M05"
official_module: "Module 5: Capital Investments and Capital Allocation"
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

# M05: Capital Investments and Capital Allocation

> **模块定位**：理解公司组织、治理、营运资本、资本配置与商业模式如何影响价值创造。 本模块聚焦 **Capital Investments and Capital Allocation**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Capital Investments and Capital Allocation
- 5.01 | Introduction
- 5.02 | Capital Investments
- 5.03 | Capital Allocation
- 5.04 | Capital Allocation Principles and Pitfalls
- 5.05 | Real Options

## Learning Outcome Statements

1. describe types of capital investments
2. describe the capital allocation process, calculate net present value (NPV), internal rate of return (IRR), and return on invested capital (ROIC), and contrast their use in capital allocation
3. describe principles of capital allocation and common capital allocation pitfalls
4. describe types of real options relevant to capital investments

---

## 1. 模块定位

### 5.1 学习任务
- **核心问题**：考试希望你用 `Capital Investments and Capital Allocation` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 5.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 5.3 关键英文术语
- **Capital Investments and Capital Allocation（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Capital Investments（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Capital Allocation（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Capital Allocation Principles and Pitfalls（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Real Options（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Option（期权）**：买方拥有权利但无义务，卖方承担相应义务的衍生品。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 5.1 | describe types of capital investments | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 5.2 | describe the capital allocation process, calculate net present value (NPV), internal rate of return (IRR), and return on invested capital (ROIC), and contrast their use in capital allocation | 计算并解释数值结果；描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 5.3 | describe principles of capital allocation and common capital allocation pitfalls | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 5.4 | describe types of real options relevant to capital investments | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
5. Capital Investments and Capital Allocation
├─ 5.1 现金流纪律 (Cash-Flow Discipline)
│  ├─ 5.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 5.2 决策标准 (Decision Criteria)
│  ├─ 5.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 5.3 实物期权 (Real Options)
│  ├─ 5.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 5.3.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 5.1 现金流纪律 (Cash-Flow Discipline)

资本预算 (Capital Budgeting) 的核心是**识别和评估能增加股东价值的投资机会**。最关键的原则是：

- **使用增量税后现金流 (Use Incremental After-Tax Cash Flows)**：只考虑项目本身带来的额外现金流，而非公司整体的现金流。
- **忽略沉没成本 (Ignore Sunk Costs)**：已发生的、不可收回的成本与未来的增量决策无关。例如，市场调研费用不应计入项目现金流。
- **包含机会成本 (Include Opportunity Costs)**：公司已有资产如果用于新项目，其放弃的最佳替代用途的价值应作为成本计入。
- **考虑蚕食效应 (Cannibalization)**：新项目可能侵蚀现有产品的销售，这部分损失应计入。
- **包含营运资本变动 (Include Working Capital Changes)**：项目通常需要额外存货和应收账款投资，结束时可能收回。
- **考虑残值与税务影响 (Salvage Value & Tax Effects)**：项目结束时出售资产的净现金流，包括税务影响。

**决策类型**：
- **独立项目 (Independent Projects)**：接受或拒绝互不影响
- **互斥项目 (Mutually Exclusive Projects)**：只能选择其中一个
- **资本约束 (Capital Rationing)**：资金有限，需在竞争项目中择优分配

### 5.2 决策标准 (Decision Criteria)

- **净现值 (Net Present Value, NPV)**：`NPV = Σ CFt/(1+r)^t - Initial Outlay`
  - 最可靠的决策标准。NPV > 0 创造价值。
  - **NPV 在兼容假设下最大化价值**，是互斥项目中的首选标准。

- **内部收益率 (Internal Rate of Return, IRR)**：`0 = Σ CFt/(1+IRR)^t - Initial Outlay`
  - 即使 NPV 为 0 的折现率。IRR > 资本成本则接受。
  - **非常规现金流 (Unconventional Cash Flows)** 下可能出现多个 IRR 或无 IRR。

- **盈利指数 (Profitability Index, PI)**：`PI = PV of future cash inflows / Initial investment`
  - PI > 1 则接受。适用于 **资本约束 (capital rationing)** 下的项目排序。

- **回收期 (Payback Period)**：累计未折现现金流收回初始投资的时间。
  - **不反映价值创造**，忽略时间价值和回收期后的现金流。

- **折现回收期 (Discounted Payback Period)**：考虑时间价值，但仍忽略回收期后现金流。

### 5.3 实物期权 (Real Options)

传统 NPV 假设项目决策不可逆，而现实中管理层有灵活性：
- **时机期权 (Timing Option)**：延迟投资等待更有利条件
- **扩张期权 (Expansion Option)**：如果项目成功可追加投资
- **放弃期权 (Abandonment Option)**：项目失败时可退出减少损失
- **灵活性期权 (Flexibility Option)**：调整产出、投入或生产方式

实物期权**增大了项目的 NPV**，因为管理层可以在有利时行动、不利时止损。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 | 说明 |
|------|------|------|
| 净现值 (NPV) | `NPV = Σ_{t=0}^{N} CF_t/(1+r)^t` | 价值创造的绝对度量 |
| 内部收益率 (IRR) | `0 = Σ_{t=0}^{N} CF_t/(1+IRR)^t` | 项目本身的收益率 |
| 盈利指数 (PI) | `PI = PV of future cash inflows / Initial investment` | 每单位投资创造的现值 |
| 回收期 | 累计现金流 ≥ 0 的时间点 | 流动性指标而非价值指标 |
| 折现回收期 | 累计折现现金流 ≥ 0 的时间点 | 略好于回收期但仍不完整 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 5.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 5.2 Capital Investments | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.3 Capital Allocation | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.4 Capital Allocation Principles and Pitfalls | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐ | 5.5 Real Options | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

**考点 1：NPV 计算**
- 给定初始投资、系列现金流和折现率，求 NPV。
- 解题：逐期折现后加总，减去初始投资。注意时间轴从 t=0 开始。

**考点 2：NPV vs IRR 冲突**
- 当互斥项目的规模 (scale) 或时间 (timing) 不同时，IRR 可能给出错误排序。
- 解题原则：**NPV 优先于 IRR**。NPV 反映的是绝对的财富增加量。

**考点 3：识别应计入的现金流**
- 题目列出若干项目相关和无关的成本，要求选择应计入的。
- 关键：排除沉没成本，包含机会成本、营运资本变动、残值等。

**考点 4：资本约束下的项目选择**
- 用 PI 排序。在资本限额内依次选择 PI 最高的项目。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：融资成本不应重复计算：折现率已经反映了融资成本，项目现金流中一般不应再包含利息支出等融资现金流。 | ✅ 融资成本不应重复计算：折现率已经反映了融资成本，项目现金流中一般不应再包含利息支出等融资现金流。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：IRR 在非常规现金流下会误导：现金流正负交替多次时可能出现多个 IRR 或无 IRR。 | ✅ IRR 在非常规现金流下会误导：现金流正负交替多次时可能出现多个 IRR 或无 IRR。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：回收期短 ≠ 项目好：回收期忽略时间价值和后期现金流，可能拒绝 NPV 高但回收慢的项目。 | ✅ 回收期短 ≠ 项目好：回收期忽略时间价值和后期现金流，可能拒绝 NPV 高但回收慢的项目。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：NPV 与 IRR 对再投资率假设不同：NPV 假设以资本成本再投资，IRR 假设以 IRR 本身再投资，NPV 的假设更合理。 | ✅ NPV 与 IRR 对再投资率假设不同：NPV 假设以资本成本再投资，IRR 假设以 IRR 本身再投资，NPV 的假设更合理。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M04-Working-Capital-and-Liquidity]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M06-Capital-Structure]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 折现率 → [[M05-Cost-of-Capital]] WACC 是资本预算中最常用的折现率
- 项目风险调整 → [[M05-Cost-of-Capital]] 风险不同的项目应使用不同折现率
- 经营杠杆影响项目风险 → [[M06-Capital-Structure-and-Leverage]] 固定成本高的项目经营杠杆大
- 实物期权概念 → [[M07-Business-Models]] 不同商业模式的灵活性不同
- 资本配置整合 → [[M08-Capital-Allocation-Integration]] 资本预算应纳入公司整体价值创造策略


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M04-Capital-Investments.md` (high, 0.542)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
