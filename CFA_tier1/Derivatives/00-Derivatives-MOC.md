---
title: 00-Derivatives-MOC
description: CFA Level I Derivatives master MOC for payoffs, forwards, options, parity, binomial pricing, swaps, and traps.
subject: Derivatives
topic_area: Derivatives
level: CFA Level I
exam_weight: 5-8%
exam_format: 单选题
difficulty: payoff 直觉、复制组合与定价公式高度绑定
note_type: master_moc
status: 学习中
aliases:
  - Derivatives 知识框架
  - 衍生品 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Derivatives
  - formulas
---

# 00-Derivatives-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Derivatives - Map of Content |
| description | CFA L1 衍生品科目学习导航：远期、期货、期权、互换、no-arbitrage、binomial、put-call parity |
| subject | Derivatives |
| 权重 | 5-8% |
| 考试形式 | 单选题，概念+定价计算 |
| 难度特点 | payoff 直觉是入口，定价关系和 parity 是丢分重灾区 |
| 学习建议 | 先分清 payoff / profit，再统一用 no-arbitrage 和 replication 理解价格 |
| 状态 | 学习中 |
| tags | CFA L1, Derivatives, MOC |

---

## 最关键：先画 payoff，再找复制组合，再看无套利价格

衍生品最容易学乱，但主线其实很单纯：`payoff -> replication -> no-arbitrage price`。

---

## 科目概览

| 模块 | 内容 | 难度 | 必考点 |
|------|------|------|--------|
| M01 | Derivative Instruments and Markets | 概念 | underlying, exchange vs OTC, settlement |
| M02 | Forward Commitments and Contingent Claims | 概念 | forwards, futures, swaps, options |
| M03 | Benefits, Risks, and Uses | 策略 | hedging, exposure transformation, leverage |
| M04 | Arbitrage, Replication, and Cost of Carry | 计算 | no-arbitrage, carry, replication |
| M05 | Pricing and Valuation of Forwards/Futures | 计算 | forward price vs forward value, marking to market |
| M06 | Pricing and Valuation of Swaps | 概念+计算 | fixed-for-floating, FRA strip intuition |
| M07 | Options and Put-Call Parity | 计算 | payoff, moneyness, parity, synthetics |
| M08 | One-Period Option Valuation | 计算 | binomial hedge ratio, risk-neutral pricing |

---

## Derivatives 核心知识树

```text
Derivatives (M01-M08)
│
├── M01: Derivative Instruments and Markets【考试核心】↔ 2026 Outline: Derivative Instrument and Market Features
│   ├── Contract map
│   │   ├── underlying: equity, rate, FX, credit, commodity, other reference
│   │   ├── long vs short; payoff depends on future state of underlying
│   │   └── settlement: physical delivery vs cash settlement
│   ├── Market map
│   │   ├── exchange-traded: standardized, clearinghouse, margin
│   │   ├── OTC: customization, counterparty exposure, bilateral terms
│   │   └── notional amount scales exposure but is not automatically cash at risk
│   └── 注意：derivative value can be small today while exposure is economically large【考试陷阱】
│
├── M02: Forward Commitments and Contingent Claims【考试核心】↔ 2026 Outline: Forward Commitment and Contingent Claim Features
│   ├── Forward commitments
│   │   ├── forward: customized future trade obligation
│   │   ├── futures: standardized obligation with daily settlement
│   │   └── swap: series of forward-like exchanges
│   ├── Contingent claims
│   │   ├── call gives right to buy; put gives right to sell
│   │   ├── option holder has right; writer bears contingent obligation
│   │   └── credit and other claims pay only if trigger/state occurs
│   └── 注意：right vs obligation is the first fork before every payoff question
│
├── M03: Benefits, Risks, and Uses【考试核心】↔ CFA Institute 2026 Derivative Benefits
│   ├── Benefits
│   │   ├── hedge an existing exposure; transform duration, beta, currency, commodity risk
│   │   ├── gain exposure with capital efficiency and lower implementation friction
│   │   └── price discovery and risk transfer
│   ├── Risks and users
│   │   ├── leverage, liquidity, counterparty, basis, model, operational risk
│   │   ├── issuers use hedges to stabilize financing/operating cash flows
│   │   └── investors use derivatives for risk control, tactical exposure, arbitrage
│   └── 注意：hedging reduces a chosen risk; it may introduce basis or counterparty risk
│
├── M04: Arbitrage, Replication, and Cost of Carry【考试核心】↔ 2026 Outline: Arbitrage and Replication
│   ├── No-arbitrage logic
│   │   ├── law of one price for identical future cash flows
│   │   ├── replication portfolio pins fair derivative price
│   │   └── arbitrage action pushes mispriced contract back to fair relation
│   ├── Carry relation
│   │   ├── financing cost raises forward price for an investment asset
│   │   ├── known income / yield / convenience benefits reduce net carry
│   │   └── value after initiation differs from original forward price
│   └── 注意：price at initiation and value during life are cousins, not twins【考试陷阱】
│
├── M05: Pricing and Valuation of Forwards and Futures【考试核心】↔ 2026 Outline: Pricing and Valuation of Forward Contracts
│   ├── Forward price cases
│   │   ├── 核心公式
│   │   │   ├── `F0(T) = S0(1+r)^T`
│   │   │   ├── `F0(T) = [S0 - PV(I)](1+r)^T`
│   │   │   └── `F0(T) = S0[(1+r)/(1+q)]^T` 或连续口径 `S0e^((r-q)T)`
│   │   ├── no-income asset: spot grown at risk-free rate
│   │   ├── known income: subtract PV of income before carrying forward
│   │   └── known yield: reduce carry by continuous/discrete yield assumption
│   ├── Contract value
│   │   ├── 核心公式
│   │   │   ├── `Long expiry payoff = ST - K`
│   │   │   ├── `Short expiry payoff = K - ST`
│   │   │   └── `Vt = St - PVt(K)`
│   │   ├── long forward gains when market forward price rises above contract price
│   │   ├── futures marking-to-market realizes gains/losses daily
│   │   └── interest-rate correlation can make futures and forwards diverge
│   └── 注意：long forward payoff at expiry = spot minus delivery price, not current value formula
│
├── M06: Pricing and Valuation of Swaps【考试核心】↔ 2026 Outline: Pricing and Valuation of Interest Rates and Other Swaps
│   ├── Swap anatomy
│   │   ├── 核心公式
│   │   │   └── `Net swap payment = Notional x (Floating rate - Fixed rate) x accrual factor`
│   │   ├── fixed-for-floating interest rate swap exchanges net interest cash flows
│   │   ├── currency swap may exchange principal and coupon currencies
│   │   └── initial fixed rate chosen so inception value is approximately zero
│   ├── Valuation intuition
│   │   ├── swap can be viewed as bond pair or strip of forward-rate agreements
│   │   ├── value changes as fixed rate vs market swap curve changes
│   │   └── payer/receiver label follows fixed leg exposure
│   └── 注意：notional is reference amount in vanilla interest rate swaps, not exchanged principal
│
├── M07: Options and Put-Call Parity【考试核心】↔ 2026 Outline: Options
│   ├── Payoff language
│   │   ├── 核心公式
│   │   │   ├── `Call payoff = max(0, ST - X)`
│   │   │   ├── `Put payoff = max(0, X - ST)`
│   │   │   ├── `Long call profit = max(0, ST - X) - c0`
│   │   │   └── `Long put profit = max(0, X - ST) - p0`
│   │   ├── call payoff `max(0, S_T - X)`; put payoff `max(0, X - S_T)`
│   │   ├── intrinsic value, time value, moneyness
│   │   └── payoff excludes premium; profit includes premium and financing context
│   ├── Parity and synthetics
│   │   ├── 核心公式
│   │   │   ├── `c + PV(X) = p + S0`
│   │   │   └── `c = p + S0 - PV(X)`
│   │   ├── European parity: call + PV(strike) = put + stock
│   │   ├── rearrange to synthesize call, put, stock, protective put, fiduciary call
│   │   └── lower/upper bounds expose arbitrage relationships
│   └── 注意：do not carry European parity unchanged into every American-option fact pattern
│
└── M08: One-Period Option Valuation【考试核心】↔ 2026 Outline: Binomial Valuation
    ├── Replication branch
    │   ├── 核心公式
    │   │   ├── `h = (Cu - Cd)/(Su - Sd)`
    │   │   └── `V0 = hS0 + B`
    │   ├── compute option payoff in up/down states
    │   ├── hedge ratio matches state-contingent payoff difference
    │   └── borrowing/lending completes replicating portfolio
    ├── Risk-neutral branch
    │   ├── 核心公式
    │   │   ├── `p* = [(1+r)-d]/(u-d)`
    │   │   └── `V0 = [p*Vu + (1-p*)Vd]/(1+r)`
    │   ├── derive risk-neutral probability from no-arbitrage growth
    │   ├── expected risk-neutral payoff discounted at risk-free rate
    │   └── higher volatility widens state spread and can raise option value
    └── 注意：risk-neutral probability is pricing machinery, not the investor's real forecast
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报 | 相关性 | 费用/代价 |
|--------|------|------|------|--------|-----------|
| Forward vs Futures | OTC customized vs exchange standardized | counterparty risk vs basis/marking risk | 都锁定未来价格 | 都对标的价格敏感 | futures 有 margining 成本 |
| Call vs Put | 买涨权利 vs 买跌权利 | premium loss limited to cost | upside/downside asymmetry | payoff 对标的价格方向相反 | premium 是 upfront cost |
| Payoff vs Profit | 到期现金流 vs 扣除期初成本后的净结果 | 混淆后整题方向错 | profit 才是投资者真实收益 | payoff 是 profit 的前置 | premium/financing 是 profit 代价 |
| American vs European Option | 可提前行权 vs 仅到期行权 | early exercise value 差异 | American flexibility 更高 | parity 处理需更谨慎 | American 通常更贵 |
| Fixed-for-Floating Swap vs Currency Swap | 利率暴露交换 vs 币种+利率现金流交换 | basis / FX risk 来源不同 | 都用于重塑风险暴露 | 都与债务管理相关 | 交易结构更复杂 |
| Forward Price vs Forward Value | 新合约公平 delivery price vs 现有合约当前价值 | 混淆会把定价题和估值题串台 | 一个常使初始价值为零，一个可正可负 | 都随 spot/carry 改变 | value 受原 contract price 约束 |
| Hedging vs Speculating | 降低既有风险 vs 主动建立风险 | hedge 仍有 residual risk | speculate 寻求方向性收益 | 都使用同一合约 | hedge 代价常是放弃部分 upside |

---

## 跨模块关联

```text
Instrument and Market Features
├── Forward commitments -> forward/futures/swaps cash-flow obligations
└── Contingent claims -> option payoff asymmetry
Uses and Risks
├── issuer hedge -> financing/operating exposure control
└── investor exposure -> capital efficiency + leverage discipline
Pricing Spine
├── no-arbitrage -> replication -> cost of carry
├── forwards/futures -> forward value and daily settlement
├── swaps -> bond pair / FRA strip intuition
└── options -> parity -> binomial valuation
```

---

## 通用分析框架

### 框架1：衍生品定价题 SOP

1. 先识别 instrument type
2. 画 payoff
3. 找复制组合或 carry relation
4. 再贴现 / 套 parity

### 框架2：option 题 SOP

1. 先分清 call/put
2. 再分清 payoff/profit
3. 再判断 moneyness
4. 最后代入 premium / strike

### 框架3：parity 题 SOP

1. 先写标准 parity
2. 再移项得到目标 synthetic position
3. 最后检查是不是 European option 条件

---

## 核心公式速查

### M04-M06 Forward Commitments

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Forward Price, No Income | `F_0(T) = S_0(1+r)^T` | `M05` | carry 主干 |
| Forward Price, Known Income | `F_0(T) = [S_0 - PV(I)](1+r)^T` | `M05` | 先扣收入现值 |
| Forward Price, Known Yield | `F_0(T) = S_0[(1+r)/(1+q)]^T` 或连续口径 `S_0e^{(r-q)T}` | `M05` | 看题目给的是离散收益率还是连续收益率 |
| Long Forward Expiry Payoff | `S_T - K` | `M05` | `K` 是约定 delivery price |
| Short Forward Expiry Payoff | `K - S_T` | `M05` | long/short 对称 |
| Long Forward Value During Life | `V_t = S_t - PV_t(K)` | `M05` | 无 income 的简化直觉 |
| Net Swap Payment | `Notional x (Floating rate - Fixed rate) x accrual factor` | `M06` | payer/receiver 方向先读题 |

### M07 Options and Parity

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Call Payoff | `max(0, S_T - X)` | `M07` | payoff 不是 profit |
| Put Payoff | `max(0, X - S_T)` | `M07` | 高频 |
| Long Call Profit | `max(0, S_T - X) - c_0` | `M07` | premium 不能漏 |
| Long Put Profit | `max(0, X - S_T) - p_0` | `M07` | premium 不能漏 |
| Put-Call Parity | `c + PV(X) = p + S_0` | `M07` | European options |
| Synthetic Long Call | `c = p + S_0 - PV(X)` | `M07` | 会移项比背图强 |
| Synthetic Protective Put | `p + S_0 = c + PV(X)` | `M07` | 两边经济等价 |
| Intrinsic Value | `max(0, payoff driver)` | `M07` | call/put 分别代入 |

### M08 Binomial Valuation

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Hedge Ratio | `h = (C_u - C_d)/(S_u - S_d)` | `M08` | replication 核心 |
| Risk-neutral Probability | `p* = [(1+r)-d]/(u-d)` | `M08` | 不是真实概率 |
| One-Period Option Value | `V_0 = [p*V_u + (1-p*)V_d]/(1+r)` | `M08` | 先算 terminal payoff |
| Replicating Portfolio Value | `V_0 = hS_0 + B` | `M08` | `B` 可为 borrowing |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| option holder 一定会行权 | 只有在经济上有利时才行权 |
| payoff 就是 profit | profit 还要减 premium/融资成本 |
| futures 和 forwards 完全一样 | futures 有 daily settlement 和 margining |
| forward pricing 可以不看 income | 分红/收益率会改变 fair forward price |
| call 越贵越差 | 价格要结合波动率、到期日、内在值判断 |
| put-call parity 适用于所有期权 | 基础版本用于 European options |
| binomial 先求 risk-neutral p 就够了 | terminal payoff 和 hedge ratio 同样关键 |
| swap 会凭空创造收益 | swap 本质是交换现金流暴露 |
| long forward 和 long call 一样 | 一个是 obligation，一个是 right |
| 衍生品题都先代公式 | 先画 payoff 往往能救整题 |
| notional amount 就是最大损失 | notional 是 exposure scale，不自动等于 cash at risk |
| hedge 一定消灭所有风险 | hedge 可能留下 basis、liquidity、counterparty risk |
| forward price 和 forward value 是一回事 | fair delivery price 与 existing contract value 要分开 |
| risk-neutral probability 是主观预测概率 | 它是无套利定价权重 |
