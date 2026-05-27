---
title: "M02: Security Market Indexes"
description: "CFA Level I 2026 Equity Investments 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Equity Investments"
topic_area: "Equity"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M02"
official_module: "Module 2: Security Market Indexes"
los_count: 11
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Equity
---

# M02: Security Market Indexes

## 0. Reading Contract 阅读契约

- **Official scope**: index definition, value and return calculations, construction choices, weighting, rebalancing/reconstitution, uses, equity/fixed-income/alternative indexes.
- **C+ output**: 能根据 weighting method 判断 index return, bias, turnover and benchmark use。
- **Evidence anchor**: V5 Module 2, practice and solutions available in the 2026 ePub index.

## 1. Module Brief 模块定位

Index 是把 target market 压缩成可计算 proxy 的工具。考试常问三件事：value/return 怎么算、weighting method 让谁影响大、rebalance/reconstitution 改了什么。

## 2. Curriculum Spine 教材主线

1. Define target market and eligible securities.
2. Calculate price return and total return.
3. Choose weighting: price, equal, market-cap, float-adjusted, fundamental.
4. Manage index: rebalance weights and reconstitute constituents.
5. Use index: sentiment gauge, benchmark, asset-class proxy, model portfolio, risk/performance proxy.
6. Compare equity, fixed-income and alternative investment indexes.

## 3. Exam Translation 考试转译

- 题干给 constituent prices -> suspect price-weighted or price return.
- 题干给 market caps/shares -> market-cap or float-adjusted market-cap.
- 题干说 each constituent reset to same weight -> equal-weighted rebalancing.
- 题干说 add/delete securities -> reconstitution, not rebalancing.
- 题干说 benchmark for active manager -> index use, not index calculation.

## 4. Formula & Decision Bench 公式与决策台

| Trigger | Formula / Decision rule | Check |
|---|---|---|
| Price return | `(P1 - P0) / P0` | Excludes dividends/interest. |
| Total return | `(ending value + income - beginning value) / beginning value` | Include distributions. |
| Price-weighted index | `sum constituent prices / divisor` | High-priced stocks dominate; splits need divisor change. |
| Equal-weighted index | average returns or equal capital allocation | Small-cap tilt; high rebalancing turnover. |
| Market-cap weighted | `price x shares outstanding` weights | Large-cap dominated; price rise increases weight. |
| Float-adjusted | use free-float shares only | Excludes strategic/locked holdings. |
| Fundamental weighted | weights by sales/cash flow/book/dividends | Reduces price-driven concentration, may create value exposure. |

## 5. Practice & Mock Evidence 题库证据

- Expected item types: compute index value/return, identify weighting bias, distinguish rebalance vs reconstitution, choose index use.
- Review tag: `Equity-M02-indexes`.
- Miss log fields: weighting method, income treatment, divisor event, constituent change, benchmark use.

## 6. Trap Ledger 易错账本

- Total return includes income; price return does not。
- Stock split changes price but not investor wealth; divisor adjustment prevents artificial index move。
- Equal weighting is not neutral; it gives smaller companies more influence than market-cap weighting。
- Rebalancing changes weights; reconstitution changes members。

## 7. Final Recall Sheet 终局速记

- Price weighted: price matters.
- Equal weighted: every constituent starts equal.
- Market-cap weighted: size matters.
- Float-adjusted: tradable size matters.
- Fundamental weighted: economic scale matters.
