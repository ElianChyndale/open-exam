---
title: "M14: Credit Risk"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M14"
official_module: "Module 14: Credit Risk"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M14: Credit Risk

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Credit Risk**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Credit Risk
- 14.01 | Introduction
- 14.02 | Sources of Credit Risk
- 14.03 | Credit Rating Agencies and Credit Ratings
- 14.04 | Factors Impacting Yield Spreads

## Learning Outcome Statements

1. describe credit risk and its components, probability of default and loss given default
2. describe the uses of ratings from credit rating agencies and their limitations
3. describe macroeconomic, market, and issuer-specific factors that influence the level and volatility of yield spreads

---

## 1. 模块定位

### 14.1 学习任务
- **核心问题**：考试希望你用 `Credit Risk` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 14.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 14.3 关键英文术语
- **Credit Risk（信用风险）**：发行人无法按时足额履约的风险。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Sources of Credit Risk（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Credit Rating Agencies and Credit Ratings（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Factors Impacting Yield Spreads（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。
- **Yield（收益率）**：把债券价格与未来现金流连接起来的回报度量。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 14.1 | describe credit risk and its components, probability of default and loss given default | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 14.2 | describe the uses of ratings from credit rating agencies and their limitations | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 14.3 | describe macroeconomic, market, and issuer-specific factors that influence the level and volatility of yield spreads | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
14. Credit Risk
├─ 14.1 损失逻辑 (Loss Logic)
│  ├─ 14.1.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 14.1.2 应用/判断：再处理计算、比较、解释或情境选择
├─ 14.2 评级与利差驱动因素 (Ratings and Spread Drivers)
│  ├─ 14.2.1 定义/识别：先说清概念、公式变量和适用条件
│  └─ 14.2.2 应用/判断：再处理计算、比较、解释或情境选择
```

## 4. 知识点详解

### 14.1 损失逻辑 (Loss Logic)

- **预期信用损失 = PD x LGD x 敞口 (expected credit loss intuition = PD x LGD x exposure)**：信用风险的核心度量。PD (probability of default) 是违约概率；LGD (loss given default) = 1 - 回收率；exposure 是违约时的风险敞口。
- **违约风险、降级风险、利差风险 (default risk, downgrade risk, spread risk)**：信用风险不限于违约本身。降级风险 (downgrade risk) 指评级下调导致价格下跌；利差风险 (spread risk) 指信用利差走阔导致价格下跌，即使尚未违约。
- **回收率与优先级决定损失严重程度 (recovery and seniority shape loss severity)**：担保债务的回收率通常高于无担保债务；优先级债务的回收率高于次级债务。LGD = 1 - Recovery Rate。

### 14.2 评级与利差驱动因素 (Ratings and Spread Drivers)

- **评级总结相对信用风险但非保证 (ratings summarize relative credit risk but are not guarantees)**：评级机构（Moody's、S&P、Fitch）的评级是对相对违约风险的综合评估，不保证特定违约概率或损失率。
- **宏观、市场、发行人因素影响利差水平与波动性 (macro, market, issuer factors move spread level and volatility)**：宏观因素（GDP 增长、利率）、市场因素（流动性、风险偏好）、发行人因素（财务健康、行业前景）共同决定信用利差。
- **流动性和期权特征可与纯信用利差共存 (liquidity and optionality can coexist with pure credit spread)**：观察到的利差是信用风险补偿、流动性补偿和期权补偿的混合体，不能简单等同于纯信用风险溢价。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式 |
|------|------|
| 预期信用损失 | `ECL ≈ PD x LGD x Exposure` |
| 违约损失率 | `LGD = 1 - Recovery Rate` |
| 信用利差 | `Credit Spread = YTM_bond - YTM_benchmark` |
| 利差分解 (概念) | `Spread ≈ 信用风险溢价 + 流动性溢价 + 期权成本` |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 14.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 14.2 Sources of Credit Risk | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 14.3 Credit Rating Agencies and Credit Ratings | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 14.4 Factors Impacting Yield Spreads | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **计算预期损失**：给出 PD、回收率、敞口，计算 ECL。注意回收率转 LGD：LGD = 1 - 回收率。
- **区分违约风险与利差风险**：违约风险涉及发行人无法支付本息；利差风险是二级市场价格因信用担忧而下跌，即使尚未发生违约。
- **理解评级对融资成本的影响**：降级通常导致利差走阔、债券价格下跌；列入负面观察名单也会产生影响。
- **分析利差变化的驱动因素**：判断利差走阔是源于信用恶化（发行人基本面变差）、流动性恶化（交易困难）还是市场风险偏好下降。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：利差常在违约前走阔，因为所需补偿发生了变化 (a spread widens before default often because required compensation… | ✅ 利差常在违约前走阔，因为所需补偿发生了变化 (a spread widens before default often because required compensation… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Issuer rating ≠ issue rating：发行人的评级针对其整体偿债能力，具体债项的评级可能因担保品、优先级等因素而不同。 | ✅ Issuer rating ≠ issue rating：发行人的评级针对其整体偿债能力，具体债项的评级可能因担保品、优先级等因素而不同。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Credit spread 不是静态的：即使发行人基本面不变，市场风险偏好的变化也会导致利差波动（如危机时期利差系统性走阔）。 | ✅ Credit spread 不是静态的：即使发行人基本面不变，市场风险偏好的变化也会导致利差波动（如危机时期利差系统性走阔）。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Recovery rate 存在很大不确定性：违约后的实际回收率取决于复杂的法律程序和市场环境，难以准确预测。 | ✅ Recovery rate 存在很大不确定性：违约后的实际回收率取决于复杂的法律程序和市场环境，难以准确预测。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **上游模块**：[[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M15-Credit-Analysis-for-Government-Issuers]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 信用利差 → [[M04-Yield-and-Spread-Measures]] 的利差度量
- 回收率/优先级 → [[M11-Government-and-Corporate-Credit]] 的债项优先级
- 信用风险建模 → [[M12-Securitization-Foundations]] 的资产隔离逻辑


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M10-Credit-Risk.md` (high, 0.567)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
