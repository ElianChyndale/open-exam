---
title: "M10 — Valuing a Derivative Using a One-Period Binomial Model"
description: "CFA Level I 2026 official module: Valuing a Derivative Using a One-Period Binomial Model"
module: M10
subject: "Derivatives"
topic_area: Derivatives
curriculum_year: 2026
official_module: "Module 10: Valuing a Derivative Using a One-Period Binomial Model"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Derivatives
  - official_2026
---

# M10: Valuing a Derivative Using a One-Period Binomial Model

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Valuing a Derivative Using a One-Period Binomial Model
- 10.01 | Introduction
- 10.02 | Binomial Valuation
- 10.03 | The Binomial Model
- 10.04 | Pricing a European Call Option
- 10.05 | Risk Neutrality

## Learning Outcome Statements

The candidate should be able to:

- explain how to value a derivative using a one-period binomial model
- describe the concept of risk neutrality in derivatives pricing

## Local Study Notes

### Migrated from `CFA_tier1/Derivatives/M08-Binomial-Valuation.md`

_Alignment score: 0.50. Original official module field: Valuing a Derivative Using a One-Period Binomial Model._

#### M08: 单期二叉树期权估值 (Binomial Valuation of Options)

##### 1. 核心知识点

**复制分支 (Replication Branch)**

复制方法的核心是构建一个由标的资产和无风险借贷组成的组合，使其收益与期权完全一致。

- **对冲比率 (Hedge Ratio)**：上涨与下跌状态下期权收益差除以股票价格差

```
h = (Cu - Cd)/(Su - Sd)
```

- **复制组合价值 (Replicating Portfolio Value)**

```
V0 = hS0 + B
```

其中 `B` 为借贷金额（可为负值，表示借入资金）

- **借贷头寸 (Borrowing/Lending Position)**：

```
B = (Cd - hSd)/(1+r)
```

也可用上涨状态验证：`B = (Cu - hSu)/(1+r)`。

**风险中性分支 (Risk-Neutral Branch)**

风险中性方法不依赖投资者的真实风险偏好，而是从无套利条件推导定价权重。

- **风险中性概率 (Risk-Neutral Probability)**

```
p* = [(1+r)-d]/(u-d)
```

其中 `u` = 上涨因子，`d` = 下跌因子

- **单期期权价值 (One-Period Option Value)**

```
V0 = [p*Vu + (1-p*)Vd]/(1+r)
```

| 概念 | 说明 |
|------|------|
| 风险中性概率 | 不是真实世界概率，是无套利定价权重 (pricing machinery, not real forecast) |
| 波动率影响 | 更高波动率扩大状态价差，可能提高期权价值 |
| 方法等价性 | 复制法和风险中性法得出相同结果 |

##### 2. 关键公式

```
h = (Cu - Cd)/(Su - Sd)          (对冲比率)
V0 = hS0 + B                     (复制组合价值)
B = (Cd - hSd)/(1+r)             (无风险借贷头寸)
p* = [(1+r)-d]/(u-d)             (风险中性概率)
V0 = [p*Vu + (1-p*)Vd]/(1+r)    (单期期权价值)
```

**考纲标记**：
- 【考纲重点】terminal payoff、hedge ratio、borrowing/lending position、risk-neutral probability、one-period option value。
- 【考纲内但无核心公式】risk-neutral probability 的含义、波动率对期权价值的方向影响。
- 【超纲/扩展】多期二叉树、Black-Scholes、Greeks 不作为 Level I 必背公式。

##### 3. 常见考点与解题思路

1. **计算题**：先确定 u/d 和 Su/Sd → 计算期权在上涨/下跌状态的 payoff → 代入公式求期权价值
2. **对冲比率题**：用 `(Cu-Cd)/(Su-Sd)` 计算，再确定借贷金额
3. **风险中性题**：先算 `p*` → 再用期望贴现求 `V0`
4. 题目若给利率和波动率，自己推导 u/d（通常 u=1/d 或给定数值）

##### 4. 易错点提醒

- 风险中性概率 `p*` **不是投资者的真实预测概率**，它只是无套利定价的数学工具 (risk-neutral probability is pricing machinery, not the investor's real forecast)
- 不要忘记贴现步骤 —— 风险中性期望值需除以 `(1+r)` 得到现值
- 对冲比率必须与状态依赖收益匹配，不能随意选取
- 复制法中 `B` 可为正（贷出资金）或负（借入资金）

##### 5. 跨模块关联

- [[M04-Arbitrage-and-Replication]]：二项式模型是无套利复制的直接应用
- [[M07-Options-and-Put-Call-Parity]]：二项式模型为欧式期权提供估值基础
- [[M00-Derivatives-MOC]]：返回科目总览
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
