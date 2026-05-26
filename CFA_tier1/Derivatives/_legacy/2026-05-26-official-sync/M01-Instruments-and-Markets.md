---
title: "M01 -- Instruments and Markets"
description: "衍生品工具与市场：合约要素、市场结构、交易所与场外交易、结算方式 (Derivative Instruments and Markets: contract elements, market structure, exchange vs OTC, settlement)"
module: M01
subject: Derivatives
official_module: "Derivative Instrument and Derivative Market Features"
---

# M01: 衍生品工具与市场 (Instruments and Markets)

## 1. 核心知识点

**合约要素 (Contract Elements)**
- **标的资产 (Underlying)**：股票、利率、外汇、信用、大宗商品及其他参照物 (equity, rate, FX, credit, commodity, other reference)
- **多头与空头 (Long vs Short)**：多头在未来买入资产，空头在未来卖出资产；收益取决于标的资产未来状态 (long buys, short sells; payoff depends on future state of underlying)
- **结算方式 (Settlement)**：实物交割 (physical delivery) 或现金结算 (cash settlement)

**市场结构 (Market Structure)**
- **交易所交易 (Exchange-Traded)**：标准化合约、中央清算所、保证金制度、每日盯市 (standardized, clearinghouse, margin, daily marking-to-market)
- **场外交易 (OTC)**：定制化条款、双边交易对手风险、无中央清算 (customization, counterparty exposure, bilateral terms)
- **名义金额 (Notional Amount)**：放大风险敞口但不等于实际在险现金 (scales exposure but not automatically cash at risk)

## 2. 关键公式

该模块以概念为主，无核心计算公式。需理解以下关系：
- 衍生品价值可远小于其名义敞口 (derivative value < notional exposure)
- 合约价值取决于标的资产价格变化 (contract value depends on underlying price changes)

## 3. 常见考点与解题思路

- **区分交易所 vs OTC**：标准化 vs 定制化；清算所 vs 双边风险；保证金 vs 信用风险
- **判断结算方式**：实物交割多用于商品/外汇；现金结算多用于指数/利率
- **名义金额的理解**：名义金额不是实际投入资金，而是计算回报的参照基数

## 4. 易错点提醒

- 【考试陷阱】衍生品当前价值很小，但经济敞口可能非常大 (derivative value can be small today while exposure is economically large)
- 不要将名义金额 (notional) 误认为最大损失 —— 名义金额是规模参照，不是风险上限
- OTC 衍生品不意味着"更危险"，而是风险类型不同（交易对手风险 vs 流动性风险）

## 5. 跨模块关联

- [[M02-Forward-Commitments-and-Contingent-Claims]]：合约分类是 M02 的基础
- [[M05-Forward-and-Futures-Pricing]]：交易所合约的保证金制度影响期货定价
- [[M00-Derivatives-MOC]]：返回科目总览
