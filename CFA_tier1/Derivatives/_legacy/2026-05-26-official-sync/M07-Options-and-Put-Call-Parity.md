---
title: "M07 -- Options and Put-Call Parity"
description: "期权与买卖权平价：期权收益、利润、实值状态、买卖权平价、合成头寸 (Options and Put-Call Parity: payoff, profit, moneyness, put-call parity, synthetic positions)"
module: M07
subject: Derivatives
official_module: "Pricing and Valuation of Options, Option Replication Using Put-Call Parity"
---

# M07: 期权与买卖权平价 (Options and Put-Call Parity)

## 1. 核心知识点

**收益语言 (Payoff Language)**

| 指标 | 公式 | 说明 |
|------|------|------|
| 看涨期权到期收益 (Call Payoff) | `max(0, ST - X)` | ST > X 时行权盈利 |
| 看跌期权到期收益 (Put Payoff) | `max(0, X - ST)` | ST < X 时行权盈利 |
| 多头看涨期权利润 (Long Call Profit) | `max(0, ST - X) - c0` | 扣除权利金 |
| 多头看跌期权利润 (Long Put Profit) | `max(0, X - ST) - p0` | 扣除权利金 |

**关键概念**
- **内在价值 (Intrinsic Value)**：立即行权的经济价值，`= max(0, payoff driver)`
- **时间价值 (Time Value)**：期权价格超出内在价值的部分
- **实值状态 (Moneyness)**：实值 (in-the-money)、平值 (at-the-money)、虚值 (out-of-the-money)
- **收益 vs 利润**：收益不包括权利金；利润包括权利金和融资成本 (payoff excludes premium; profit includes premium and financing context)

**平价关系与合成头寸 (Parity and Synthetics)**

**买卖权平价公式 (Put-Call Parity)**：
```
c + PV(X) = p + S0
```

| 合成头寸 | 移项结果 |
|---------|---------|
| 合成看涨 (Synthetic Call) | `c = p + S0 - PV(X)` |
| 合成看跌 (Synthetic Put) | `p = c - S0 + PV(X)` |
| 合成股票 (Synthetic Stock) | `S0 = c + PV(X) - p` |
| 保护性看跌 (Protective Put) | `p + S0 = c + PV(X)` |

**有收入资产的平价调整**：
- 已知现金收入：`c + PV(X) + PV(I) = p + S0`
- 连续收益率：`c + PV(X) = p + S0e^{-qT}`

**期权价值边界（European options）**：
- 看涨下限：`c >= max(0, S0 - PV(X))`
- 看跌下限：`p >= max(0, PV(X) - S0)`
- 美式期权价值通常不低于对应欧式期权，因为提前行权权利不会降低价值。

## 2. 关键公式

```
Call payoff = max(0, ST - X)          Long call profit = max(0, ST - X) - c0
Put payoff  = max(0, X - ST)          Long put profit  = max(0, X - ST) - p0
c + PV(X) = p + S0                   买卖权平价 (仅适用于欧式期权)
c + PV(X) + PV(I) = p + S0           有已知收入资产的平价
c + PV(X) = p + S0e^(-qT)            有连续收益率资产的平价
```

**考纲标记**：
- 【考纲重点】payoff/profit、put-call parity、synthetics、option value bounds。
- 【考纲内但无核心公式】moneyness、American vs European、option uses。
- 【超纲/扩展】Black-Scholes 与 Greeks 不属于 Level I 必背公式。

## 3. 常见考点与解题思路

1. **payoff 题**：先分清 call/put → 代入 max(0, 公式)
2. **profit 题**：在 payoff 基础上减权利金（如有融资成本也要考虑）
3. **parity 题**：写标准 parity → 移项得到目标合成头寸 → 检查是否欧式期权条件
4. **套利题**：若 parity 两边不等，买入便宜方、卖出贵方

## 4. 易错点提醒

- payoff 不是 profit —— profit 还要减权利金和融资成本
- 【高频】payoff 和 profit 混淆后整题方向全错
- 基础版 put-call parity **仅适用于欧式期权** (European options)，美式期权因其可提前行权需要更复杂的处理
- 不要将欧式平价关系直接套用到所有美式期权场景
- 期权价格受波动率影响，不是越贵越差

## 5. 跨模块关联

- [[M04-Arbitrage-and-Replication]]：parity 本质是无套利关系的体现
- [[M08-Binomial-Valuation]]：二项式模型为期权提供估值框架
- [[M00-Derivatives-MOC]]：返回科目总览
