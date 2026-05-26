---
title: "M02: Alternative Investment Performance and Returns"
description: "CFA Level I 2026 Alternative Investments 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Alternative Investments"
topic_area: "Alternative_Investments"
level: "CFA Level I"
exam_year: 2026
exam_weight: "7-10%"
module: "M02"
official_module: "Module 2: Alternative Investment Performance and Returns"
los_count: 2
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Alternative_Investments
---

# M02: Alternative Investment Performance and Returns

> **模块定位**：识别另类投资结构、绩效、私募、实物资产、对冲基金与数字资产特征。 本模块聚焦 **Alternative Investment Performance and Returns**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Alternative Investment Performance and Returns
- 2.01 | Introduction
- 2.02 | Alternative Investment Performance
- 2.03 | Alternative Investment Returns

## Learning Outcome Statements

1. describe the performance appraisal of alternative investments
2. calculate and interpret alternative investment returns both before and after fees

---

## 1. 模块定位

### 2.1 学习任务
- **核心问题**：考试希望你用 `Alternative Investment Performance and Returns` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 2.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 2.3 关键英文术语
- **Alternative Investment Performance and Returns（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Alternative Investment Performance（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Alternative Investment Returns（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 2.1 | describe the performance appraisal of alternative investments | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 2.2 | calculate and interpret alternative investment returns both before and after fees | 计算并解释数值结果；解释结果的投资含义 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
2. Alternative Investment Performance and Returns
├─ 2.1 业绩衡量指标 (Performance Measurement Metrics)【考试核心】
│  ├─ 2.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 2.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 2.2 J曲线 (J-Curve Dynamics)【考试核心】
│  ├─ 2.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 2.2.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 2.3 收益平滑 (Smoothed Returns)【考试陷阱】
│  ├─ 2.3.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 2.3.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 2.1 业绩衡量指标 (Performance Measurement Metrics)【考试核心】

**核心指标一览**:

| 指标 | 英文全称 | 公式 | 含义 |
|------|----------|------|------|
| TVPI | Total Value to Paid-In | (累计分配 + 剩余价值) / 实缴资本 = DPI + RVPI | 总价值倍数 |
| DPI | Distributed to Paid-In | 累计分配 / 实缴资本 | 现金回报倍数（已实现的） |
| RVPI | Residual Value to Paid-In | 剩余价值 / 实缴资本 | 未实现回报倍数 |
| IRR | Internal Rate of Return | NPV = 0 的折现率 | 内部收益率，考虑时间价值 |
| Sortino | Sortino Ratio | (R_p - R_f) / σ_d | 下行风险调整收益 |
| Sharpe | Sharpe Ratio | (R_p - R_f) / σ_p | 总风险调整收益 |

**关键关系**:
- TVPI = DPI + RVPI（**加法关系**，不是乘法）
- **DPI > 0** 表示已有现金分配回LP；**RVPI > 0** 表示还有未退出的投资价值
- **Sortino vs Sharpe**: Sortino只考虑下行波动 (σ_d)，Sharpe考虑总波动 (σ_p)。当资产收益分布不对称时，Sortino更准确

### 2.2 J曲线 (J-Curve Dynamics)【考试核心】

J曲线描述PE基金生命周期中**先负后正**的收益变化曲线。

**早期负收益原因**: 管理费持续收取（按承诺资本AUM）、初期交易成本与设立费用、投资尚未成熟退出

**后期转正原因**: 投资标的成熟、价值增长、项目退出（IPO/并购/二级出售）、DPI上升而RVPI下降

**不同策略的J曲线**:
- **VC**: J曲线最深（早期投资，失败率高，回报周期长）
- **LBO**: 相对较浅（成熟公司，有现金流，杠杆放大回报）
- **Growth Equity**: 介于两者之间

### 2.3 收益平滑 (Smoothed Returns)【考试陷阱】

**原因**: 非流动性资产按评估价值 (Appraisal Value) 而非市价 (Market Value) 估值

**后果**:
- 低估波动率 (Volatility)
- 低估与市场的相关性 (Correlation)
- 导致风险调整后收益被高估（Sharpe/Sortino偏高）

**Unsmoothing调整**: 对评估收益进行去平滑处理，还原真实波动率，使数据更接近公开市场价格波动

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 |
|------|------|
| TVPI | (累计分配 + 剩余价值) / 实缴资本 = DPI + RVPI |
| DPI | 累计分配 / 实缴资本 |
| RVPI | 剩余价值 / 实缴资本 |
| Sortino | (R_p - R_f) / σ_d |
| Sharpe | (R_p - R_f) / σ_p |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 2.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 2.2 Alternative Investment Performance | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 2.3 Alternative Investment Returns | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

1. **TVPI/DPI/RVPI计算**: 给定累计分配、剩余价值和实缴资本，计算三个指标。**思路**: 先分别算DPI和RVPI，再加总得TVPI。
2. **J曲线阶段判断**: 给出基金成立年限和收益状态，判断处于J曲线的哪个阶段。**思路**: 早期（1-3年）= 负收益；中期 = 逐步转正；后期 = 正收益稳定。
3. **Sortino vs Sharpe辨析**: 题干描述指标特征，要求选出正确的指标。**思路**: Sortino看下行，Sharpe看总波动。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：TVPI = DPI + RVPI（加法）: 常被误认为乘法关系 | ✅ TVPI = DPI + RVPI（加法）: 常被误认为乘法关系 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：J曲线先负后正: 不是全程亏损，最终转正 | ✅ J曲线先负后正: 不是全程亏损，最终转正 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：收益平滑高估表现: 评估估值导致波动率和相关性被低估，风险调整收益被高估 | ✅ 收益平滑高估表现: 评估估值导致波动率和相关性被低估，风险调整收益被高估 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：DPI vs RVPI的含义: DPI是已实现的现金回报，RVPI是未实现的账面价值，两者性质不同 | ✅ DPI vs RVPI的含义: DPI是已实现的现金回报，RVPI是未实现的账面价值，两者性质不同 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Sortino vs Sharpe: 在另类投资中，Sortino通常更适用（收益分布不对称） | ✅ Sortino vs Sharpe: 在另类投资中，Sortino通常更适用（收益分布不对称） | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M01-Alternative-Investment-Features-Methods-and-Structures]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M03-Investments-in-Private-Capital-Equity-and-Debt]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- TVPI/DPI/RVPI → [[M03-Private-Capital.md]] (PE基金业绩报告)
- J曲线 → [[M03-Private-Capital.md]] (PE基金生命周期)
- 收益平滑 → [[M04-Real-Estate-and-Infrastructure.md]] (房地产估值)
- 费用计算 → [[M01-Features-and-Structure.md]] (管理费和业绩提成)


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M02-Performance-Measurement.md` (high, 0.456)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
