---
title: "M14 — Credit Risk"
description: "CFA Level I 2026 official module: Credit Risk"
module: M14
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 14: Credit Risk"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M14: Credit Risk

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Credit Risk
- 14.01 | Introduction
- 14.02 | Sources of Credit Risk
- 14.03 | Credit Rating Agencies and Credit Ratings
- 14.04 | Factors Impacting Yield Spreads

## Learning Outcome Statements

The candidate should be able to:

- describe credit risk and its components, probability of default and loss given default
- describe the uses of ratings from credit rating agencies and their limitations
- describe macroeconomic, market, and issuer-specific factors that influence the level and volatility of yield spreads

## Local Study Notes

### Migrated from `CFA_tier1/Fixed_Income/M10-Credit-Risk.md`

_Alignment score: 1.00. Original official module field: Module 14: Credit Risk._

#### M13: 信用风险 (Credit Risk)

##### 1. 核心知识点

###### 1.1 损失逻辑 (Loss Logic)

- **预期信用损失 = PD x LGD x 敞口 (expected credit loss intuition = PD x LGD x exposure)**：信用风险的核心度量。PD (probability of default) 是违约概率；LGD (loss given default) = 1 - 回收率；exposure 是违约时的风险敞口。
- **违约风险、降级风险、利差风险 (default risk, downgrade risk, spread risk)**：信用风险不限于违约本身。降级风险 (downgrade risk) 指评级下调导致价格下跌；利差风险 (spread risk) 指信用利差走阔导致价格下跌，即使尚未违约。
- **回收率与优先级决定损失严重程度 (recovery and seniority shape loss severity)**：担保债务的回收率通常高于无担保债务；优先级债务的回收率高于次级债务。LGD = 1 - Recovery Rate。

###### 1.2 评级与利差驱动因素 (Ratings and Spread Drivers)

- **评级总结相对信用风险但非保证 (ratings summarize relative credit risk but are not guarantees)**：评级机构（Moody's、S&P、Fitch）的评级是对相对违约风险的综合评估，不保证特定违约概率或损失率。
- **宏观、市场、发行人因素影响利差水平与波动性 (macro, market, issuer factors move spread level and volatility)**：宏观因素（GDP 增长、利率）、市场因素（流动性、风险偏好）、发行人因素（财务健康、行业前景）共同决定信用利差。
- **流动性和期权特征可与纯信用利差共存 (liquidity and optionality can coexist with pure credit spread)**：观察到的利差是信用风险补偿、流动性补偿和期权补偿的混合体，不能简单等同于纯信用风险溢价。

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 预期信用损失 | `ECL ≈ PD x LGD x Exposure` |
| 违约损失率 | `LGD = 1 - Recovery Rate` |
| 信用利差 | `Credit Spread = YTM_bond - YTM_benchmark` |
| 利差分解 (概念) | `Spread ≈ 信用风险溢价 + 流动性溢价 + 期权成本` |

##### 3. 常见考点与解题思路

- **计算预期损失**：给出 PD、回收率、敞口，计算 ECL。注意回收率转 LGD：LGD = 1 - 回收率。
- **区分违约风险与利差风险**：违约风险涉及发行人无法支付本息；利差风险是二级市场价格因信用担忧而下跌，即使尚未发生违约。
- **理解评级对融资成本的影响**：降级通常导致利差走阔、债券价格下跌；列入负面观察名单也会产生影响。
- **分析利差变化的驱动因素**：判断利差走阔是源于信用恶化（发行人基本面变差）、流动性恶化（交易困难）还是市场风险偏好下降。

##### 4. 易错点提醒

- **利差常在违约前走阔，因为所需补偿发生了变化 (a spread widens before default often because required compensation changed)**：信用利差是市场对信用风险的前瞻性定价，利差走阔本身不意味着违约，而是市场要求的风险补偿增加。
- **Issuer rating ≠ issue rating**：发行人的评级针对其整体偿债能力，具体债项的评级可能因担保品、优先级等因素而不同。
- **Credit spread 不是静态的**：即使发行人基本面不变，市场风险偏好的变化也会导致利差波动（如危机时期利差系统性走阔）。
- **Recovery rate 存在很大不确定性**：违约后的实际回收率取决于复杂的法律程序和市场环境，难以准确预测。

##### 5. 跨模块关联

- 信用利差 → [[M04-Yield-and-Spread-Measures]] 的利差度量
- 回收率/优先级 → [[M11-Government-and-Corporate-Credit]] 的债项优先级
- 信用风险建模 → [[M12-Securitization-Foundations]] 的资产隔离逻辑
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
