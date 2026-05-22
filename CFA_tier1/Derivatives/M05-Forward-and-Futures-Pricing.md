---
title: "M05 -- Forward and Futures Pricing and Valuation"
description: "远期与期货定价估值：远期价格公式、合约存续期价值、逐日盯市 (Pricing and Valuation of Forwards and Futures: forward price formulas, contract value during life, marking-to-market)"
module: M05
subject: Derivatives
---

# M05: 远期与期货定价估值 (Forward and Futures Pricing and Valuation)

## 1. 核心知识点

**远期价格情形 (Forward Price Cases)**

| 资产类型 | 定价公式 | 核心思路 |
|---------|---------|---------|
| 无收益资产 (No-Income) | `F0(T) = S0(1+r)^T` | 现货以无风险利率增长 |
| 已知收入 (Known Income) | `F0(T) = [S0 - PV(I)](1+r)^T` | 先扣收入现值再前滚 |
| 已知收益率 (Known Yield) | `F0(T) = S0[(1+r)/(1+q)]^T` | 收益率降低持有成本 |

**合约价值 (Contract Value)**

| 指标 | 公式 | 说明 |
|------|------|------|
| 多头到期收益 (Long Expiry Payoff) | `ST - K` | `K` 为合约交割价 |
| 空头到期收益 (Short Expiry Payoff) | `K - ST` | 对称反向 |
| 存续期多头价值 (Long Forward Value) | `Vt = St - PVt(K)` | 无收益资产简化版本 |

- **期货与远期的关键区别**：期货每日盯市结算 (marking-to-market)，每日实现盈亏；远期到期一次结算
- 利率与标的资产价格的相关性可能导致期货与远期价格偏离

## 2. 关键公式

```
F0(T) = S0(1+r)^T                                         (无收益资产)
F0(T) = [S0 - PV(I)](1+r)^T                                (已知收入资产)
F0(T) = S0[(1+r)/(1+q)]^T 或 S0e^((r-q)T)                  (已知收益率资产)

Vt(long) = St - PVt(K)                                     (无收益资产存续期价值)
Long payoff at expiry = ST - K                              (多头到期收益)
Short payoff at expiry = K - ST                             (空头到期收益)
```

## 3. 常见考点与解题思路

1. **定价题**：识别资产类型 → 选对应公式 → 代入计算 fair forward price
2. **估值题**：区分期初 vs 存续期 → 用当前 spot 减合约价现值
3. **期货 vs 远期差异题**：关注 daily settlement 和 margin 的影响
4. **套利题**：比较市场价与公平价 → 设计 cash-and-carry / reverse cash-and-carry

## 4. 易错点提醒

- **Forward Price vs Forward Value 不是同一概念** —— Price 是新合约的公平交割价；Value 是现有合约当前值多少钱
- 多头远期到期收益 = spot - 交割价 (ST - K)，不是当前价值公式
- 有 income 的资产必须先折现 income 再扣减，不能直接用 future income
- 连续复利与离散复利公式不可混用

## 5. 跨模块关联

- [[M04-Arbitrage-and-Replication]]：carry 关系是定价基础
- [[M06-Swap-Pricing]]：互换可视为一系列远期合约的组合
- [[M00-Derivatives-MOC]]：返回科目总览
