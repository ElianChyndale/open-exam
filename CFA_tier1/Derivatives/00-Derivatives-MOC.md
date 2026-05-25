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

| 模块 | 官方 Module | 内容 | 难度 | 必考点 | 章节文件 |
|------|-------------|------|------|--------|----------|
| M01 | Derivative Instrument and Derivative Market Features | Derivative Instruments and Markets | 概念 | underlying, exchange vs OTC, settlement | [[M01-Instruments-and-Markets]] |
| M02 | Forward Commitment and Contingent Claim Features and Instruments | Forward Commitments and Contingent Claims | 概念 | forwards, futures, swaps, options | [[M02-Forward-Commitments-and-Contingent-Claims]] |
| M03 | Derivative Benefits/Risks/Uses | Benefits, Risks, and Uses | 策略 | hedging, exposure transformation, leverage | [[M03-Benefits-and-Risks]] |
| M04 | Arbitrage/Replication/Cost of Carry | Arbitrage, Replication, and Cost of Carry | 计算 | no-arbitrage, carry, replication | [[M04-Arbitrage-and-Replication]] |
| M05 | Pricing and Valuation of Forward Contracts, Pricing and Valuation of Futures Contracts | Pricing and Valuation of Forwards/Futures | 计算 | forward price vs forward value, marking to market | [[M05-Forward-and-Futures-Pricing]] |
| M06 | Pricing and Valuation of Interest Rates and Other Swaps | Pricing and Valuation of Swaps | 概念+计算 | fixed-for-floating, FRA strip intuition | [[M06-Swap-Pricing]] |
| M07 | Pricing and Valuation of Options, Option Replication Using Put-Call Parity | Options and Put-Call Parity | 计算 | payoff, moneyness, parity, synthetics | [[M07-Options-and-Put-Call-Parity]] |
| M08 | Valuing a Derivative Using a One-Period Binomial Model | One-Period Option Valuation | 计算 | binomial hedge ratio, risk-neutral pricing | [[M08-Binomial-Valuation]] |

---

## Derivatives 核心知识树 (Core Knowledge Tree)

```text
衍生品 (Derivatives) (M01-M08)
│
├── M01: 衍生品工具与市场 (Derivative Instruments and Markets)【考试核心】↔ 2026 Outline: Derivative Instrument and Market Features
│   ├── 合约地图 (Contract Map)
│   │   ├── 标的资产：股票、利率、外汇、信用、大宗商品及其他参照物 (underlying: equity, rate, FX, credit, commodity, other reference)
│   │   ├── 多头 vs 空头；收益取决于标的资产未来状态 (long vs short; payoff depends on future state of underlying)
│   │   └── 结算：实物交割或现金结算 (settlement: physical delivery vs cash settlement)
│   ├── 市场地图 (Market Map)
│   │   ├── 交易所交易：标准化、清算所、保证金 (exchange-traded: standardized, clearinghouse, margin)
│   │   ├── 场外交易：定制化、交易对手风险、双边条款 (OTC: customization, counterparty exposure, bilateral terms)
│   │   └── 名义金额放大敞口但不等于在险现金 (notional amount scales exposure but is not automatically cash at risk)
│   └── 注意：derivative value can be small today while exposure is economically large【考试陷阱】
│
├── M02: 远期承诺与或有求偿 (Forward Commitments and Contingent Claims)【考试核心】↔ 2026 Outline: Forward Commitment and Contingent Claim Features
│   ├── 远期承诺 (Forward Commitments)
│   │   ├── 远期合约：定制化的未来交易义务 (forward: customized future trade obligation)
│   │   ├── 期货：标准化的每日结算义务 (futures: standardized obligation with daily settlement)
│   │   └── 互换：一系列类似远期的交换协议 (swap: series of forward-like exchanges)
│   ├── 或有索取权 (Contingent Claims)
│   │   ├── 看涨期权赋予买入权利；看跌期权赋予卖出权利 (call gives right to buy; put gives right to sell)
│   │   ├── 期权持有人拥有权利；卖方承担或有义务 (option holder has right; writer bears contingent obligation)
│   │   └── 信用衍生品及其他仅在触发时支付 (credit and other claims pay only if trigger/state occurs)
│   └── 注意：right vs obligation is the first fork before every payoff question
│
├── M03: 收益、风险与用途 (Benefits, Risks, and Uses)【考试核心】↔ CFA Institute 2026 Derivative Benefits
│   ├── 收益 (Benefits)
│   │   ├── 对冲现有敞口；转换久期、Beta、货币、商品风险 (hedge an existing exposure; transform duration, beta, currency, commodity risk)
│   │   ├── 以资本效率和较低摩擦获得风险敞口 (gain exposure with capital efficiency and lower implementation friction)
│   │   └── 价格发现与风险转移 (price discovery and risk transfer)
│   ├── 风险与使用者 (Risks and Users)
│   │   ├── 杠杆、流动性、交易对手、基差、模型、操作风险 (leverage, liquidity, counterparty, basis, model, operational risk)
│   │   ├── 发行方使用对冲稳定融资/经营现金流 (issuers use hedges to stabilize financing/operating cash flows)
│   │   └── 投资者使用衍生品进行风险控制、战术性敞口、套利 (investors use derivatives for risk control, tactical exposure, arbitrage)
│   └── 注意：hedging reduces a chosen risk; it may introduce basis or counterparty risk
│
├── M04: 套利、复制与持有成本 (Arbitrage, Replication, and Cost of Carry)【考试核心】↔ 2026 Outline: Arbitrage and Replication
│   ├── 无套利逻辑 (No-Arbitrage Logic)
│   │   ├── 一价定律适用于相同未来现金流 (law of one price for identical future cash flows)
│   │   ├── 复制组合确定衍生品公平价格 (replication portfolio pins fair derivative price)
│   │   └── 套利行为将错误定价推回公平关系 (arbitrage action pushes mispriced contract back to fair relation)
│   ├── 持有成本关系 (Carry Relation)
│   │   ├── 融资成本提高投资资产的远期价格 (financing cost raises forward price for an investment asset)
│   │   ├── 已知收入/收益率/便利收益减少净持有成本 (known income / yield / convenience benefits reduce net carry)
│   │   └── 存续期价值与初始远期价格不同 (value after initiation differs from original forward price)
│   └── 注意：price at initiation and value during life are cousins, not twins【考试陷阱】
│
├── M05: 远期与期货定价估值 (Pricing and Valuation of Forwards and Futures)【考试核心】↔ 2026 Outline: Pricing and Valuation of Forward Contracts
│   ├── 远期价格情形 (Forward Price Cases)
│   │   ├── 核心公式 (English)
│   │   │   ├── `F0(T) = S0(1+r)^T` 无收益资产远期价格 (no-income asset)
│   │   │   ├── `F0(T) = [S0 - PV(I)](1+r)^T` 已知收入资产远期价格 (known income asset)
│   │   │   └── `F0(T) = S0[(1+r)/(1+q)]^T` 或连续口径 `S0e^((r-q)T)`
│   │   ├── 无收益资产：现货以无风险利率增长 (no-income asset: spot grown at risk-free rate)
│   │   ├── 已知收入：扣除收入现值后向前滚动 (known income: subtract PV of income before carrying forward)
│   │   └── 已知收益率：按连续/离散收益率减少持有成本 (known yield: reduce carry by continuous/discrete yield assumption)
│   ├── 合约价值 (Contract Value)
│   │   ├── 核心公式 (English)
│   │   │   ├── `Long expiry payoff = ST - K` 多头到期收益 (long expiry payoff)
│   │   │   ├── `Short expiry payoff = K - ST` 空头到期收益 (short expiry payoff)
│   │   │   └── `Vt = St - PVt(K)` 存续期多头价值 (long forward value during life)
│   │   ├── 多头远期在市场远期价格高于合约价格时获利 (long forward gains when market forward price rises above contract price)
│   │   ├── 期货逐日盯市每日实现盈亏 (futures marking-to-market realizes gains/losses daily)
│   │   └── 利率相关性可导致期货与远期价格分化 (interest-rate correlation can make futures and forwards diverge)
│   └── 注意：long forward payoff at expiry = spot minus delivery price, not current value formula
│
├── M06: 互换定价与估值 (Pricing and Valuation of Swaps)【考试核心】↔ 2026 Outline: Pricing and Valuation of Interest Rates and Other Swaps
│   ├── 互换结构 (Swap Anatomy)
│   │   ├── 核心公式 (English)
│   │   │   └── `Net swap payment = Notional x (Floating rate - Fixed rate) x accrual factor` 互换净支付 (net swap payment)
│   │   ├── 固定换浮动利率互换交换净利息现金流 (fixed-for-floating interest rate swap exchanges net interest cash flows)
│   │   ├── 货币互换可能交换本金和票息币种 (currency swap may exchange principal and coupon currencies)
│   │   └── 初始固定利率使起始价值约等于零 (initial fixed rate chosen so inception value is approximately zero)
│   ├── 估值直觉 (Valuation Intuition)
│   │   ├── 互换可视为债券对或远期利率协议组合 (swap can be viewed as bond pair or strip of forward-rate agreements)
│   │   ├── 价值随固定利率与市场互换曲线变化 (value changes as fixed rate vs market swap curve changes)
│   │   └── 支付方/接收方标签取决于固定端敞口 (payer/receiver label follows fixed leg exposure)
│   └── 注意：notional is reference amount in vanilla interest rate swaps, not exchanged principal
│
├── M07: 期权与看涨看跌平价 (Options and Put-Call Parity)【考试核心】↔ 2026 Outline: Options
│   ├── 收益语言 (Payoff Language)
│   │   ├── 核心公式 (English)
│   │   │   ├── `Call payoff = max(0, ST - X)` 看涨期权到期收益 (call expiry payoff)
│   │   │   ├── `Put payoff = max(0, X - ST)` 看跌期权到期收益 (put expiry payoff)
│   │   │   ├── `Long call profit = max(0, ST - X) - c0` 多头看涨期权利润 (long call profit)
│   │   │   └── `Long put profit = max(0, X - ST) - p0` 多头看跌期权利润 (long put profit)
│   │   ├── 看涨期权收益 `max(0, S_T - X)`；看跌期权收益 `max(0, X - S_T)` (call payoff; put payoff)
│   │   ├── 内在价值、时间价值、实值状态 (intrinsic value, time value, moneyness)
│   │   └── 收益不包括权利金；利润包括权利金和融资成本 (payoff excludes premium; profit includes premium and financing context)
│   ├── 平价关系与合成头寸 (Parity and Synthetics)
│   │   ├── 核心公式 (English)
│   │   │   ├── `c + PV(X) = p + S0` 买卖权平价 (put-call parity)
│   │   │   └── `c = p + S0 - PV(X)` 合成看涨期权 (synthetic long call)
│   │   ├── 欧式平价：看涨期权 + 行权价现值 = 看跌期权 + 股票 (European parity: call + PV(strike) = put + stock)
│   │   ├── 移项可合成看涨、看跌、股票、保护性看跌、信托看涨 (rearrange to synthesize call, put, stock, protective put, fiduciary call)
│   │   └── 上下限揭示套利关系 (lower/upper bounds expose arbitrage relationships)
│   └── 注意：do not carry European parity unchanged into every American-option fact pattern
│
└── M08: 单期二叉树期权估值 (One-Period Option Valuation)【考试核心】↔ 2026 Outline: Binomial Valuation
    ├── 复制分支 (Replication Branch)
    │   ├── 核心公式 (English)
    │   │   ├── `h = (Cu - Cd)/(Su - Sd)` 对冲比率 (hedge ratio)
    │   │   └── `V0 = hS0 + B` 复制组合价值 (replicating portfolio value)
    │   ├── 计算上涨/下跌状态的期权收益 (compute option payoff in up/down states)
    │   ├── 对冲比率匹配状态依赖收益差异 (hedge ratio matches state-contingent payoff difference)
    │   └── 借入/贷出完成复制组合 (borrowing/lending completes replicating portfolio)
    ├── 风险中性分支 (Risk-Neutral Branch)
    │   ├── 核心公式 (English)
    │   │   ├── `p* = [(1+r)-d]/(u-d)` 风险中性概率 (risk-neutral probability)
    │   │   └── `V0 = [p*Vu + (1-p*)Vd]/(1+r)` 单期期权价值 (one-period option value)
    │   ├── 从无套利增长推导风险中性概率 (derive risk-neutral probability from no-arbitrage growth)
    │   ├── 风险中性期望收益以无风险利率贴现 (expected risk-neutral payoff discounted at risk-free rate)
    │   └── 更高波动率扩大状态价差并可能提高期权价值 (higher volatility widens state spread and can raise option value)
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
├── Forward commitments -> forward/futures/swaps cash-flow obligations (中文)
└── Contingent claims -> option payoff asymmetry (中文)
Uses and Risks
├── issuer hedge -> financing/operating exposure control (中文)
└── investor exposure -> capital efficiency + leverage discipline (中文)
Pricing Spine
├── no-arbitrage -> replication -> cost of carry (中文)
├── forwards/futures -> forward value and daily settlement (中文)
├── swaps -> bond pair / FRA strip intuition (中文)
└── options -> parity -> binomial valuation (中文)
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
