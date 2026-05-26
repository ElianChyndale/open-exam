---
title: "00-Derivatives-MOC"
description: "CFA Level I 2026 Derivatives 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Derivatives"
topic_area: "Derivatives"
level: CFA Level I
exam_year: 2026
exam_weight: "5-8%"
module_count: 10
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Derivatives
---

# Derivatives MOC

> **一句话核心**：用无套利、复制和工具结构理解远期、期货、互换、期权的风险转移。

---

## 1. 科目定位

- **考试权重**：5-8%
- **官方模块数**：10
- **主线框架**：识别标的与到期现金流 -> 建立无套利关系 -> 定价/估值 -> 判断风险暴露
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |
|---|---|---|---|---|
| M01 | Derivative Instrument and Derivative Market Features | 概念+应用 | Introduction / Derivative Features | [[M01-Derivative-Instrument-and-Derivative-Market-Features]] |
| M02 | Forward Commitment and Contingent Claim Features and Instruments | 概念+应用 | Introduction / Forwards, Futures, and Swaps | [[M02-Forward-Commitment-and-Contingent-Claim-Features-and-Instruments]] |
| M03 | Derivative Benefits, Risks, and Issuer and Investor Uses | 概念+应用 | Introduction / Derivative Benefits | [[M03-Derivative-Benefits-Risks-and-Issuer-and-Investor-Uses]] |
| M04 | Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives | 概念+应用 | Introduction / Arbitrage | [[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]] |
| M05 | Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities | 计算+解释 | Introduction / Pricing and Valuation of Forward Contracts | [[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]] |
| M06 | Pricing and Valuation of Futures Contracts | 计算+解释 | Introduction / Pricing of Futures Contracts at Inception | [[M06-Pricing-and-Valuation-of-Futures-Contracts]] |
| M07 | Pricing and Valuation of Interest Rates and Other Swaps | 计算+解释 | Introduction / Swaps vs. Forwards | [[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]] |
| M08 | Pricing and Valuation of Options | 计算+解释 | Introduction / Option Value relative to the Underlying Spot Price | [[M08-Pricing-and-Valuation-of-Options]] |
| M09 | Option Replication Using Put-Call Parity | 概念+应用 | Introduction / Put–Call Parity | [[M09-Option-Replication-Using-Put-Call-Parity]] |
| M10 | Valuing a Derivative Using a One-Period Binomial Model | 概念+应用 | Introduction / Binomial Valuation | [[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]] |

## 3. 核心知识树

```text
Derivatives (5-8%)
├─ 1. Derivative Instrument and Derivative Market Features
│  ├─ 1.1 合约要素：underlying、notional、long/short、settlement；价值来自标的未来状态
│  ├─ 1.2 市场结构：exchange-traded 标准化/清算/保证金，OTC 定制化/双边信用风险
│  └─ 1.3 考试判断：notional 放大敞口但不是最大损失；market value 可小于 economic exposure
├─ 2. Forward Commitment and Contingent Claim Features and Instruments
│  ├─ 2.1 Forward commitments：forwards、futures、swaps 都是义务；payoff 线性、上下行对称
│  ├─ 2.2 Contingent claims：options 是权利；holder 选择行权，writer 承担或有义务
│  └─ 2.3 第一分叉：right vs obligation 决定 payoff 图形、风险上限和是否有 premium
├─ 3. Derivative Benefits, Risks, and Issuer and Investor Uses
│  ├─ 3.1 用途：hedging、speculation、arbitrage、exposure transformation、price discovery
│  ├─ 3.2 风险：leverage、liquidity、counterparty、basis、model、operational risk
│  └─ 3.3 考试判断：hedge 降低目标风险，但可能引入 basis/counterparty risk
├─ 4. Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives
│  ├─ 4.1 无套利：相同未来现金流必须同价；错价时买便宜现金流、卖贵现金流
│  ├─ 4.2 复制：derivative price = replicating portfolio cost；后续 parity/binomial 都从这里来
│  └─ 4.3 持有成本：forward price = spot compounded by net carry；income/yield/convenience benefit 降低 fair price
├─ 5. Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities
│  ├─ 5.1 Pricing at inception：no income `F0=S0(1+r)^T`；known income `[S0-PV(I)](1+r)^T`；yield `S0[(1+r)/(1+q)]^T`
│  ├─ 5.2 Valuation during life：long value 约等于 current asset PV minus PV(delivery price)，price 与 value 不同
│  └─ 5.3 Varying maturities：远期曲线来自不同期限 carry、利率和收入假设
├─ 6. Pricing and Valuation of Futures Contracts
│  ├─ 6.1 Futures price：若利率确定且无 default，理论上接近 forward price
│  ├─ 6.2 Daily settlement：marking to market 每日实现盈亏，margin call 改变现金流时点
│  └─ 6.3 Forward vs futures：利率与标的正相关时 futures price 可高于 forward price
├─ 7. Pricing and Valuation of Interest Rates and Other Swaps
│  ├─ 7.1 Swap as forward strip：互换是一串远期/FRAs，初始 fixed rate 使价值约为零
│  ├─ 7.2 Net payment：`Notional x (Floating - Fixed) x accrual`，方向取决于 payer/receiver
│  └─ 7.3 Valuation intuition：fixed-rate payer 价值随市场固定利率上升而上升
├─ 8. Pricing and Valuation of Options
│  ├─ 8.1 Payoff：call `max(0,ST-X)`，put `max(0,X-ST)`；profit 还要扣 premium
│  ├─ 8.2 Value components：option value = intrinsic value + time value；moneyness 由 S 与 X 决定
│  └─ 8.3 Drivers：underlying price、strike、volatility、time、risk-free rate、income/yield
├─ 9. Option Replication Using Put-Call Parity
│  ├─ 9.1 European parity：`c + PV(X) = p + S0`，两边到期现金流相同
│  ├─ 9.2 Synthetics：移项得到 synthetic call/put/stock/bond；套利题买便宜组合、卖贵组合
│  └─ 9.3 Forward parity：用 forward 代替现货时要匹配到期和交割价
├─ 10. Valuing a Derivative Using a One-Period Binomial Model
│  ├─ 10.1 Terminal payoff：先算 up/down 状态的 option payoff
│  ├─ 10.2 Replication：`h=(Vu-Vd)/(Su-Sd)`，再用 borrowing/lending 完成复制
│  └─ 10.3 Risk-neutral pricing：`p*=[(1+r)-d]/(u-d)`，`V0=[p*Vu+(1-p*)Vd]/(1+r)`；p* 不是真实概率
```

## 4. 跨模块依赖关系

```text
Instrument layer (M01-M03)
├─ contract terms -> payoff / settlement / counterparty exposure
├─ forward commitments -> forwards, futures, swaps (linear obligations)
└─ contingent claims -> options, credit triggers (asymmetric rights)

Pricing spine (M04-M07)
├─ no-arbitrage + replication (M04)
├─ cost of carry -> forwards and futures (M05-M06)
└─ swap = strip of forwards / bond-pair intuition (M07)

Option spine (M08-M10)
├─ payoff/profit/moneyness (M08)
├─ put-call parity and synthetics (M09)
└─ binomial replication and risk-neutral value (M10)
```

| 依赖关系 | 输入 | 输出到考试判断 | 外部接口 |
|---|---|---|---|
| `M01 -> M02` | underlying、long/short、settlement、market venue | 区分 obligation 与 right，确定 payoff 图形 | PM hedge mandate、FI/FX underlying |
| `M03 -> M04` | hedge/speculate/arbitrage motive | 只有 identical cash flows 才能做 no-arbitrage；hedge 不等于套利 | Risk management、PM exposure control |
| `M04 -> M05/M06` | spot、risk-free rate、income/yield/storage/convenience | 选择 correct cost-of-carry formula；识别 mispricing | Economics rates/FX、FI money markets |
| `M05/M06 -> M07` | forward/futures cash-flow timing | swap 是多期 forward-like cash flows，notional 多数不交换 | FI floating/fixed rates |
| `M08 -> M09` | option payoff、strike、premium、exercise style | 仅 European vanilla 直接套基础 parity | Equity options、corporate liabilities |
| `M09 -> M10` | replication and same-payoff logic | binomial 的 hedge ratio 与 risk-neutral pricing 是 parity 思想延伸 | Quant probability trees |
| `Economics/Quant -> Derivatives` | interest rates、FX quotes、volatility、discounting | 定价输入来自宏观利率、汇率和概率模型 | Economics M08、Quant TVM/probability |

## 5. 核心对比专题

| 重要性 | 对比项 | 英文 | 中文解释 | 考试判断 |
|---|---|---|---|---|
| ⭐⭐⭐ | 概念 vs 应用 | definition vs application | 先确认官方定义，再放入题干情境判断。 | 概念题也要能说出适用条件和例外。 |
| ⭐⭐⭐ | 计算 vs 解释 | calculation vs interpretation | 数值只是中间结果，答案要解释方向、含义和限制。 | 凡是 calculate and interpret 都不能只算。 |
| ⭐⭐ | 静态知识 vs 决策流程 | static knowledge vs decision process | 把每个模块压缩成输入 -> 工具 -> 输出 -> 陷阱。 | 流程化比孤立背诵更抗干扰。 |
| ⭐⭐⭐ | 英文识题 vs 中文理解 | English trigger vs Chinese explanation | 英文用于识别题干，中文用于确认真正含义。 | 避免看到熟词就按直觉作答。 |
| ⭐⭐ | 本模块 vs 跨模块 | single module vs cross-module use | 同一公式/概念可能在估值、风险、伦理或报表中换场景出现。 | 错题要回填到 MOC 节点。 |

## 6. 公式与框架速查

### M04-M06 Forward Commitments

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Forward Price, No Income | `F_0(T) = S_0(1+r)^T` | `M05` | carry 主干 |
| Forward Price, Continuous No Income | `F_0(T) = S_0e^{rT}` | `M05` | 连续复利口径 |
| Forward Price, Known Income | `F_0(T) = [S_0 - PV(I)](1+r)^T` | `M05` | 先扣收入现值 |
| Forward Price, Known Yield | `F_0(T) = S_0[(1+r)/(1+q)]^T` 或连续口径 `S_0e^{(r-q)T}` | `M05` | 看题目给的是离散收益率还是连续收益率 |
| Forward Price, Storage/Convenience | `F_0(T) = S_0e^{(r + storage - convenience)T}` | `M04/M05` | 商品 forward/cost-of-carry 直觉 |
| Long Forward Expiry Payoff | `S_T - K` | `M05` | `K` 是约定 delivery price |
| Short Forward Expiry Payoff | `K - S_T` | `M05` | long/short 对称 |
| Long Forward Value During Life | `V_t = S_t - PV_t(K)` | `M05` | 无 income 的简化直觉 |
| Long Forward Value, Known Income | `V_t = S_t - PV_t(I) - PV_t(K)` | `M05` | 标的在剩余期有已知收入 |
| Long Forward Value, Known Yield | `V_t = S_te^{-q(T-t)} - K e^{-r(T-t)}` | `M05` | 连续收益率口径 |
| Net Swap Payment | `Notional x (Floating rate - Fixed rate) x accrual factor` | `M06` | payer/receiver 方向先读题 |
| Fixed-rate Swap Value Intuition | `Value to fixed-rate payer = Floating-leg value - Fixed-leg value` | `M06` | 【考纲重点】方向判断多于完整手算 |

### M07 Options and Parity

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Call Payoff | `max(0, S_T - X)` | `M07` | payoff 不是 profit |
| Put Payoff | `max(0, X - S_T)` | `M07` | 高频 |
| Long Call Profit | `max(0, S_T - X) - c_0` | `M07` | premium 不能漏 |
| Long Put Profit | `max(0, X - S_T) - p_0` | `M07` | premium 不能漏 |
| Put-Call Parity | `c + PV(X) = p + S_0` | `M07` | European options |
| Put-Call Parity with Known Income | `c + PV(X) + PV(I) = p + S_0` | `M07` | 有已知股利/收入时调整 |
| Put-Call Parity with Yield | `c + PV(X) = p + S_0e^{-qT}` | `M07` | 连续收益率口径 |
| Synthetic Long Call | `c = p + S_0 - PV(X)` | `M07` | 会移项比背图强 |
| Synthetic Long Put | `p = c + PV(X) - S_0` | `M07` | parity 移项 |
| Synthetic Long Stock | `S_0 = c - p + PV(X)` | `M07` | fiduciary call/protective put 等价 |
| Synthetic Protective Put | `p + S_0 = c + PV(X)` | `M07` | 两边经济等价 |
| Intrinsic Value | `max(0, payoff driver)` | `M07` | call/put 分别代入 |
| European Call Lower Bound | `c >= max(0, S_0 - PV(X))` | `M07` | 【考纲重点】套利边界 |
| European Put Lower Bound | `p >= max(0, PV(X) - S_0)` | `M07` | 套利边界 |
| American Option Value Bound | `American option value >= European option value` | `M07` | 提前行权权利不降低价值 |

### M08 Binomial Valuation

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Hedge Ratio | `h = (C_u - C_d)/(S_u - S_d)` | `M08` | replication 核心 |
| Risk-neutral Probability | `p* = [(1+r)-d]/(u-d)` | `M08` | 不是真实概率 |
| One-Period Option Value | `V_0 = [p*V_u + (1-p*)V_d]/(1+r)` | `M08` | 先算 terminal payoff |
| Replicating Portfolio Value | `V_0 = hS_0 + B` | `M08` | `B` 可为 borrowing |
| Borrowing/Lending in Replication | `B = (C_d - hS_d)/(1+r)` | `M08` | 用下行状态求无风险借贷头寸 |

### 考纲范围标记

| 标记 | 内容 |
|------|------|
| 【考纲重点】 | Forwards/futures pricing and value、swap net payment and value direction、option payoff/profit/moneyness、put-call parity/synthetics/bounds、one-period binomial valuation |
| 【考纲内但无核心公式】 | Market features, uses/risks, exchange vs OTC, hedge/speculation/arbitrage distinctions |
| 【超纲/扩展】 | Black-Scholes 公式、Greeks 全套计算、多期树完整回溯、复杂 swap curve bootstrapping 不作为 Level I 必背公式 |

---

## 7. 高频考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 高频场景 |
|---|---|---|
| ❌ option holder 一定会行权 | ✅ 只有在经济上有利时才行权 | 按官方定义和 LOS 口径核验。 |
| ❌ payoff 就是 profit | ✅ profit 还要减 premium/融资成本 | 按官方定义和 LOS 口径核验。 |
| ❌ futures 和 forwards 完全一样 | ✅ futures 有 daily settlement 和 margining | 按官方定义和 LOS 口径核验。 |
| ❌ forward pricing 可以不看 income | ✅ 分红/收益率会改变 fair forward price | 按官方定义和 LOS 口径核验。 |
| ❌ call 越贵越差 | ✅ 价格要结合波动率、到期日、内在值判断 | 按官方定义和 LOS 口径核验。 |
| ❌ put-call parity 适用于所有期权 | ✅ 基础版本用于 European options | 按官方定义和 LOS 口径核验。 |
| ❌ binomial 先求 risk-neutral p 就够了 | ✅ terminal payoff 和 hedge ratio 同样关键 | 按官方定义和 LOS 口径核验。 |
| ❌ swap 会凭空创造收益 | ✅ swap 本质是交换现金流暴露 | 按官方定义和 LOS 口径核验。 |
| ❌ long forward 和 long call 一样 | ✅ 一个是 obligation，一个是 right | 按官方定义和 LOS 口径核验。 |
| ❌ 衍生品题都先代公式 | ✅ 先画 payoff 往往能救整题 | 按官方定义和 LOS 口径核验。 |

## 8. 通用分析框架

### 框架1：衍生品定价题决策树

1. 识别工具：forward/futures/swap 是 obligation；option 是 right；credit derivative 看 trigger。
2. 画到期 payoff：linear payoff 用 `S_T-K` 或 `K-S_T`；option 用 `max(0, S_T-X)` 或 `max(0, X-S_T)`。
3. 选择定价骨架：有现货与 carry -> cost of carry；两组现金流相同 -> parity/replication；单期上下状态 -> binomial。
4. 选择公式条件：无收入 `F0=S0(1+r)^T`；已知现金收入 `[S0-PV(I)](1+r)^T`；收益率 `S0[(1+r)/(1+q)]^T`；连续口径用指数形式。
5. 区分 price 与 value：price 是新合约公平交割价，value 是既有合约当前价值；题干问 valuation 时不能只报 forward price。

### 框架2：风险管理与用途题决策树

1. 先找原始暴露：price、rate、FX、credit、commodity、equity beta。
2. 判断目标：hedge 降低既有风险；speculation 建立方向性风险；arbitrage 锁定无风险错价；exposure transformation 改变现金流形态。
3. 匹配工具：linear exposure 用 forward/futures/swap；需要下行保护并保留上行可用 option。
4. 检查残余风险：basis、counterparty、liquidity、model、operational、margin/cash-flow timing。
5. 输出结论时说明收益代价：hedge 可能放弃 upside，option protection 需要 premium，futures 需要 margin。

### 框架3：option / parity / binomial 决策树

1. Option 题先分 call/put、long/short、European/American，再分 payoff/profit。
2. 若问 moneyness 或 intrinsic value：call 用 `max(0,S-X)`，put 用 `max(0,X-S)`；profit 才扣 premium。
3. 若问 parity：先写 `c + PV(X) = p + S0`，有 known income 加 `PV(I)`，有 yield 用 `S0e^{-qT}`，再移项。
4. 若问套利：买入 parity 较便宜一边，卖出较贵一边；必须确认同一 underlying、strike、maturity、European 条件。
5. 若问 binomial：先算 `V_u/V_d`，再选 replication `h=(V_u-V_d)/(S_u-S_d)` 或 risk-neutral `p*=[(1+r)-d]/(u-d)`；最后折现。

---

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

- 本 MOC 已优先吸收 `_legacy/2026-05-26-official-sync/` 中的中文解释、公式、陷阱和框架。
- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。
