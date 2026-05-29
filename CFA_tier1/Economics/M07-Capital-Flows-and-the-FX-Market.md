---
title: "M07: Capital Flows and the FX Market"
description: "CFA Level I 2026 Economics 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Economics"
topic_area: "Economics"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M07"
official_module: "Module 7: Capital Flows and the FX Market"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Economics
---

# M07: Capital Flows and the FX Market

## 0. Reading Contract 阅读契约

- **Official spine**：FX market functions/participants, exchange-rate quotations, nominal vs real rates, regimes, international trade/capital-flow effects, capital restrictions.
- **LOS contract**：describe FX market and participants; distinguish nominal/real rates; calculate and interpret currency percentage changes; describe regimes and exchange-rate effects; describe capital restrictions.
- **Evidence rule**：错题标 `quote_direction`, `nominal_real_fx`, `regime`, `capital_restriction`, or `central_bank_intervention`。

## 1. Module Brief 模块定位

This module is the bridge from macro flows to FX mechanics. 本模块不只是解释外汇市场，还要为 M08 的汇率计算打底：quote direction, market participants, regimes and capital restrictions。

## 2. Curriculum Spine 教材主线

| Spine | English trigger | 中文任务 |
|---|---|---|
| FX market | spot, forward, swap, settlement, hedging | 识别市场功能与工具。 |
| Participants | banks, corporations, investors, governments, central banks | 判断交易动机。 |
| Quotes | base/price currency, direct/indirect | 先定义报价方向。 |
| Nominal vs real | relative price level adjustment | 判断贸易竞争力。 |
| Real exchange rate formula | `RER = S_{d/f} × P_f / P_d` | 关键公式：名义汇率 × 国内外价格比。 |
| Real ER approximate Δ | `%ΔRER ≈ %ΔS + π_f - π_d` | 快速估算，注意 domestic inflation 压低 RER。 |
| Real ER exact Δ | `%ΔRER = (1+%ΔS) × (1+π_f)/(1+π_d) - 1` | 精确计算，通胀率差异大时必须用。 |
| Base currency appreciation | `new / old = 1 + r` | new 已知时求 old → 除法。 |
| Regimes | floating, managed, fixed peg, currency board, monetary union | 判断政策独立性与稳定性。区分 fixed peg（有 discretion）vs currency board（hard peg + full reserve backing + no lender of last resort）。 |
| Capital restrictions | controls on inflows/outflows | 判断政策目标和成本。 |

## 3. Exam Translation 考试翻译

1. 写下 `A/B = 1 A costs B`，再判断升贬值。
2. 问 real exchange rate：加入 relative price level，不只看 nominal quote。
3. Regime 题：fixed peg（有 discretion，lender of last resort）vs currency board（hard peg + full reserve backing + no traditional lender of last resort）。
4. Capital restriction 题：说明保护 reserves/降低波动，也可能降低效率和信心。

## 4. Formula & Decision Bench 公式与决策台

| Item | Formula / rule | Use |
|---|---|---|
| Quote meaning | `A/B` means 1 unit of A costs B | If A/B rises, A appreciates versus B. |
| Percentage change | `(new - old) / old` for quoted rate | Interpret relative to base/price currency. |
| Real exchange rate | `RER = S_{d/f} × P_f / P_d` | 名义汇率调整国内外价格水平。S_{d/f} = domestic/foreign。 |
| Real ER approximate Δ | `%ΔRER ≈ %ΔS_{d/f} + π_f - π_d` | 快速算：名义涨幅 + foreign通胀 - domestic通胀。 |
| Real ER exact Δ | `%ΔRER = (1+%ΔS) × (1+π_f)/(1+π_d) - 1` | 通胀差大时必须用精确公式，不能用近似。 |
| Base currency appreciation | `new / old = 1 + r` → `old = new / (1+r)` | base 在分母（price/base），升值 → 除法。 |
| Central bank buys foreign currency | sells domestic currency; domestic money supply rises | Can lower domestic interest rates. |
| Fixed peg vs currency board | fixed peg: discretion, lender of last resort. currency board: hard peg + full reserve backing + no traditional lender of last resort. | Stability vs independence trade-off. Currency board is stricter。 |

### Real exchange rate 公式详解

**定义**：`RER = S_{d/f} × P_f / P_d`
- `S_{d/f}` = domestic currency per foreign currency（名义汇率）
- `P_f` = foreign price level，`P_d` = domestic price level

**近似变化率**：`%ΔRER ≈ %ΔS_{d/f} + π_f - π_d`
- 名义汇率上涨 → RER 上涨（本币实际购买力下降）
- foreign inflation 更高 → RER 上涨
- domestic inflation 更高 → RER 被压低

**精确变化率**：`%ΔRER = (1+%ΔS_{d/f}) × (1+π_f)/(1+π_d) - 1`
- 例：%ΔS = +7.5%, π_f = -4%, π_d = +2.5%
- 近似：7.5% + (-4%) - 2.5% = **1.0%**
- 精确：(1.075 × 0.96 / 1.025) - 1 = **0.7%**
- 通胀率差异大时，近似值有偏差，用精确公式。

### Base currency appreciation 公式详解

`A/B = 1.4500` → 1 unit of A (base) = 1.4500 of B (price)

Base currency A 升值 8%：`new_rate = old_rate × (1 + 0.08)`

已知 new=1.45 求 old：`old = 1.45 / 1.08 = 1.3426`

> **关键直觉**：base currency 在分母，升值 → 分数值增大 → new = old × (1+r) → 求 old 用除法。不要把 base 当成分子直接乘。

## 5. Practice & Mock Evidence 题库证据

- Track `base_price_currency` when appreciation direction flips.
- Track `real_nominal_miss` when price-level adjustment is ignored.
- Track `regime_tradeoff` when fixed regime is treated as fully independent policy.
- Track `intervention_balance_sheet` when central bank buy/sell currency effect is reversed.

## 6. Trap Ledger 陷阱账本

| Trap | Fix rule |
|---|---|
| Quote up always means domestic currency up | It depends which currency is base. |
| Nominal appreciation always improves purchasing power | Real rate depends on relative inflation. |
| Peg removes currency risk at no cost | Peg requires reserves and sacrifices policy flexibility. |
| Capital controls only help | They may reduce liquidity, confidence and market efficiency. |
| Currency board = regular fixed peg | Currency board = hard peg + full reserve backing + no traditional lender of last resort. CBS is not discretionary. |

## 7. Final Recall Sheet 最终回忆单

- `A/B` up = A appreciates, B depreciates.
- FX functions: exchange, hedging, speculation, arbitrage, settlement.
- Fixed peg = stability plus reserve/policy-independence cost (has discretion). Currency board = hard peg + full reserve backing + no traditional lender of last resort.
- Capital controls protect policy/reserves but reduce efficiency and confidence.
