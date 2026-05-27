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

> **Module job**：把 credit risk 拆成 probability of default, loss given default, recovery, ratings, and spread drivers。考试常把 spread change 和 price change 结合起来问。

## 0. Reading Contract 阅读契约

- **Official LOS**：describe credit risk and PD/LGD；describe uses and limitations of credit ratings；describe macro, market, and issuer-specific factors affecting yield spreads。
- **Textbook anchors**：Sources of Credit Risk；Measuring Credit Risk；Credit Ratings；Credit Rating Considerations；Macroeconomic Factors；Market Factors；Issuer-Specific Factors；Price Impact of Spread Changes。
- **Output standard**：看到 credit spread 先分 expected loss, downgrade risk, liquidity, and market risk appetite。

## 1. Module Brief 模块定位

M14 是信用模块总入口。它不只问 default，还问 rating limitations and spread volatility。后面 M15-M16 是政府和公司信用分析的应用版。

## 2. Curriculum Spine 教材主线

1. **Default risk**：issuer fails to make promised payment。
2. **Loss severity**：LGD depends on recovery, collateral, and seniority。
3. **Credit ratings**：useful summary but lagging, imperfect, and not investment advice。
4. **Spread drivers**：macro cycle, liquidity, risk appetite, issuer fundamentals。
5. **Price impact**：spread widening generally lowers bond price。

## 3. Exam Translation 考试翻译

- If expected loss appears, use PD and LGD。
- If recovery improves, LGD falls and expected loss falls。
- If spread widens, price falls with spread duration intuition。
- If rating is mentioned, discuss both information value and limitations。

## 4. Formula & Decision Bench 公式与决策台

| Item | Formula / rule |
|---|---|
| Expected loss | `PD x LGD` |
| LGD | `1 - recovery rate` |
| Credit spread | Compensation over benchmark for credit/liquidity/risk |
| Spread widening | Price down |
| Spread narrowing | Price up |
| Rating limitation | Ratings can lag, differ by agency, and are not guarantees |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2444-eorq-q.xhtml` / `CFA2444-eorq-a.xhtml`。
- **Evidence to capture**：PD/LGD/recovery relation reversed；rating treated as guarantee；spread-price sign error。
- **Review tag**：`Fixed Income / credit risk / spreads ratings recovery`。

## 6. Trap Ledger 陷阱账本

- Recovery rate is not LGD; it is the complement。
- Credit rating is not a recommendation to buy。
- Spread widening hurts price even if benchmark rates are unchanged。
- Higher yield may reflect higher risk, not better value。

## 7. Final Recall Sheet 最终速记

- `EL = PD x LGD`；`LGD = 1 - recovery`。
- Spread wider -> price lower。
- Ratings summarize credit opinion but have limits。
- Credit risk includes default probability and loss severity。
