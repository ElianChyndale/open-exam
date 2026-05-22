---
title: "M02 -- Forward Commitments and Contingent Claims"
description: "远期承诺与或有索取权：远期、期货、互换、期权的定义、特征与区别 (Forward Commitments and Contingent Claims: forwards, futures, swaps, options definitions and features)"
module: M02
subject: Derivatives
---

# M02: 远期承诺与或有索取权 (Forward Commitments and Contingent Claims)

## 1. 核心知识点

**远期承诺 (Forward Commitments)** —— 双方均有义务在未来执行交易 (both parties obligated to transact in the future)

| 合约类型 | 特征 | 交易场所 |
|---------|------|---------|
| 远期合约 (Forward) | 定制化、到期一次结算 (customized, single settlement at maturity) | OTC |
| 期货 (Futures) | 标准化、每日盯市结算 (standardized, daily marking-to-market) | 交易所 |
| 互换 (Swap) | 一系列类似远期的现金流交换 (series of forward-like exchanges) | OTC |

**或有索取权 (Contingent Claims)** —— 持有人有权利但无义务 (holder has right but no obligation)

- **看涨期权 (Call)**：赋予买入权利 (right to buy)
- **看跌期权 (Put)**：赋予卖出权利 (right to sell)
- **期权卖方 (Writer)**：承担或有义务，收取权利金 (bears contingent obligation, receives premium)
- **信用衍生品及其他**：仅在触发条件下支付 (pay only if trigger/state occurs)

## 2. 关键公式

该模块以概念为主，核心区别在于：

```
远期承诺 payoff = 标的资产价格变化 x 合约规模  (双边义务)
或有索取权 payoff = max(0, 标的资产价格 - 行权价) 或 max(0, 行权价 - 标的资产价格)  (单边权利)
```

## 3. 常见考点与解题思路

- **权利 vs 义务 (Right vs Obligation)**：这是每道 payoff 题的第一步判断 (the first fork before every payoff question)
- **远期 vs 期货**：同样锁定未来价格，但期货有每日结算和保证金
- **互换本质**：一系列远期合约的组合 (strip of forwards)

## 4. 易错点提醒

- long forward 和 long call 不一样 —— 一个是义务 (obligation)，一个是权利 (right)
- 期权持有人不一定会行权，只有经济上有利时才行权
- 互换的名义本金通常不交换，只在利率互换中作为计算利息的基数

## 5. 跨模块关联

- [[M01-Instruments-and-Markets]]：市场结构是合约分类的基础
- [[M05-Forward-and-Futures-Pricing]]：远期和期货的定价估值
- [[M06-Swap-Pricing]]：互换定价与估值
- [[M07-Options-and-Put-Call-Parity]]：期权的深入定价
- [[M00-Derivatives-MOC]]：返回科目总览
