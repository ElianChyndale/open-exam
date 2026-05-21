---
title: 00-Fixed-Income-MOC
description: CFA Level I Fixed Income master MOC for bond pricing, yield measures, duration, credit, structured products, and traps.
subject: Fixed Income
topic_area: Fixed_Income
level: CFA Level I
exam_weight: 11-14%
exam_format: 单选题
difficulty: 现金流贴现、利率风险与信用风险层层叠加
note_type: master_moc
status: 学习中
aliases:
  - Fixed Income 知识框架
  - 固定收益 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Fixed_Income
  - formulas
---

# 00-Fixed-Income-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Fixed Income - Map of Content |
| description | CFA L1 固定收益科目学习导航：债券基础、定价、收益率、现货利率、久期凸性、信用风险、结构化产品 |
| subject | Fixed Income |
| 权重 | 11-14% |
| 考试形式 | 单选题，计算+概念并重 |
| 难度特点 | 定价和久期是主干，结构化产品和嵌入期权是易混陷阱区 |
| 学习建议 | 先把现金流贴现彻底打透，再用 duration/convexity 和 spread 把风险分层 |
| 状态 | 学习中 |
| tags | CFA L1, Fixed Income, MOC |

---

## 最关键：先贴现现金流，再拆收益率，再量化利率和信用风险

固定收益几乎所有题都能回到“现金流值多少钱，为什么要这个折现率”。

---

## 科目概览

| 模块 | 内容 | 难度 | 必考点 |
|------|------|------|--------|
| M01 | Instrument Features and Cash Flows | 概念 | indenture, covenants, contingency provisions |
| M02 | Issuance, Trading, and Funding Markets | 概念 | primary/secondary, repos, government vs corporate |
| M03 | Bond Valuation: Prices and Yields | 计算 | clean/full price, accrued interest, matrix pricing |
| M04 | Fixed-Rate Yield and Spread Measures | 计算 | YTM, annual yield conversion, spread measures |
| M05 | Floating-Rate and Money Market Measures | 计算 | FRN spreads, discount yield, MMY |
| M06 | Spot, Par, and Forward Curves | 计算 | curve comparison, spot discounting, forwards |
| M07 | Interest Rate Risk and Return | 计算+策略 | return sources, horizon, Macaulay duration |
| M08 | Yield-Based Duration and Convexity | 计算 | modified duration, money duration, PVBP, convexity |
| M09 | Curve-Based and Empirical Risk | 概念+计算 | effective duration, key rate duration |
| M10 | Credit Risk | 概念 | PD, LGD, ratings, spread volatility |
| M11 | Government and Corporate Credit Analysis | 概念+计算 | sovereign factors, coverage, leverage, priority |
| M12 | Securitization Foundations | 概念 | parties, benefits, structure |
| M13 | ABS and Credit Enhancement | 概念 | covered bonds, internal/external enhancement |
| M14 | MBS and CMO Structures | 概念 | prepayment, contraction/extension, tranche cash flows |

---

## Fixed Income 核心知识树

```text
Fixed Income (M01-M14)
│
├── M01: Instrument Features and Cash Flows【考试核心】↔ 2026 Outline P18
│   ├── Contract anatomy
│   │   ├── issuer / par / coupon / maturity / currency / seniority
│   │   ├── bond indenture: legal promises, payment terms, covenants
│   │   └── affirmative covenants vs negative covenants【考试陷阱】
│   ├── Cash-flow structures
│   │   ├── fixed-rate / floating-rate / zero-coupon / amortizing
│   │   ├── inflation-linked / step-up / deferred coupon intuition
│   │   └── contingency provisions: callable benefits issuer; putable benefits investor
│   └── 注意：coupon 的确定性不等于回报确定，价格、再投资和信用仍会变
│
├── M02: Issuance, Trading, and Funding Markets【考试核心】↔ 2026 Outline P18-P19
│   ├── Market map
│   │   ├── money market vs capital market; sovereign vs quasi-government vs corporate
│   │   ├── primary issuance vs secondary trading; dealer market liquidity
│   │   └── fixed-income indexes: maturity, issuer, credit, currency segmentation
│   ├── Corporate funding
│   │   ├── bank loans / commercial paper / repos / bonds
│   │   ├── repo = collateralized financing with haircut and counterparty exposure
│   │   └── investment-grade vs high-yield access and spread behavior
│   └── 注意：repo 看起来像 sale-and-repurchase，经济本质常按融资理解
│
├── M03: Bond Valuation: Prices and Yields【考试核心】↔ 2026 Outline P19
│   ├── Price engine
│   │   ├── bond value = coupon PV + principal PV
│   │   ├── discount / premium / par relation to coupon rate and YTM
│   │   └── longer maturity + lower coupon -> price more sensitive to yield change
│   ├── Trading price conventions
│   │   ├── full price = clean price + accrued interest【考试核心】
│   │   ├── between-coupon-date pricing uses fractional period handling
│   │   └── matrix pricing estimates yield/price for illiquid bonds
│   └── 注意：quoted clean price 是报价习惯，不是买方最终 cash paid【考试陷阱】
│
├── M04: Fixed-Rate Yield and Spread Measures【考试核心】↔ 2026 Outline P19
│   ├── Yield lens
│   │   ├── YTM is IRR under promised cash flows and reinvestment assumptions
│   │   ├── current yield captures coupon income only
│   │   └── annual yield conversion depends on compounding frequency
│   ├── Spread lens
│   │   ├── government benchmark spread / interpolated spread / G-spread intuition
│   │   ├── spread embeds credit, liquidity, option, tax, technical factors
│   │   └── price and yield move inversely for option-free fixed-rate bonds
│   └── 注意：same YTM 不代表 same value if timing/risk structure differs
│
├── M05: Floating-Rate and Money Market Measures【考试核心】↔ 2026 Outline P19
│   ├── Floating-rate instruments
│   │   ├── reference rate + quoted margin; reset mitigates but does not erase rate risk
│   │   ├── discount margin connects price away from par with required spread
│   │   └── credit deterioration can push FRN below par despite resets
│   ├── Money market instruments
│   │   ├── discount basis vs add-on basis
│   │   ├── bank discount yield vs money market yield vs bond equivalent yield
│   │   └── denominator matters: par or purchase price; 360-day or 365-day year
│   └── 注意：money market quotes love denominator traps more than they love elegance
│
├── M06: Spot, Par, and Forward Curves【考试核心】↔ 2026 Outline P19
│   ├── Curve dictionary
│   │   ├── spot curve discounts a single cash flow at each maturity
│   │   ├── par curve gives coupon rate making a bond price equal par
│   │   └── forward curve implies future borrowing/lending rates from today's curve
│   ├── Curve calculations
│   │   ├── spot pricing: each CF gets its maturity-matched spot rate
│   │   ├── forward from spot; spot from chained forwards
│   │   └── par rate solved from discount factors
│   └── 注意：forward rate is an implied no-arbitrage rate, not a guaranteed forecast
│
├── M07: Interest Rate Risk and Return【考试核心】↔ 2026 Outline P19
│   ├── Return decomposition
│   │   ├── coupon income + reinvestment income + price change
│   │   ├── pull to par and horizon effect
│   │   └── realized return differs when sale yield or reinvestment rate changes
│   ├── Horizon and Macaulay duration
│   │   ├── investment horizon < Macaulay duration -> price risk dominates
│   │   ├── investment horizon > Macaulay duration -> reinvestment risk dominates
│   │   └── Macaulay duration = weighted average time to cash flows
│   └── 注意：duration matching is about balancing price and reinvestment effects, not freezing price
│
├── M08: Yield-Based Duration and Convexity【考试核心】↔ 2026 Outline P20
│   ├── Duration family
│   │   ├── modified duration estimates % price sensitivity to yield
│   │   ├── money duration estimates currency price change per yield unit
│   │   └── PVBP = price change for 1 bp yield shift
│   ├── Convexity
│   │   ├── convexity corrects curvature missed by duration
│   │   ├── positive convexity helps for symmetric yield moves
│   │   └── portfolio duration/convexity use value weights with limitations
│   └── 注意：duration is local and yield-based; do not treat it as a full curve stress test
│
├── M09: Curve-Based and Empirical Risk Measures【考试核心】↔ 2026 Outline P20
│   ├── Option-aware risk
│   │   ├── effective duration/effective convexity reprice when cash flows may change
│   │   ├── embedded option changes callability/prepayment behavior
│   │   └── analytical duration may differ from observed empirical duration
│   ├── Curve risk
│   │   ├── key rate duration isolates maturity-bucket sensitivity
│   │   ├── non-parallel curve shifts break single-duration intuition
│   │   └── benchmark shift and credit spread shift are separate questions
│   └── 注意：callable and MBS risk cannot be fully trusted to plain modified duration
│
├── M10: Credit Risk【考试核心】↔ 2026 Outline P20
│   ├── Loss logic
│   │   ├── expected credit loss intuition = PD x LGD x exposure
│   │   ├── default risk, downgrade risk, spread risk
│   │   └── recovery and seniority shape loss severity
│   ├── Ratings and spread drivers
│   │   ├── ratings summarize relative credit risk but are not guarantees
│   │   ├── macro, market, issuer factors move spread level and volatility
│   │   └── liquidity and optionality can coexist with pure credit spread
│   └── 注意：a spread widens before default often because required compensation changed
│
├── M11: Government and Corporate Credit Analysis【考试核心】↔ 2026 Outline P20
│   ├── Government issuers
│   │   ├── monetary sovereignty, fiscal flexibility, external position, political risk
│   │   └── sovereign and non-sovereign issuers do not share identical support assumptions
│   ├── Corporate issuers
│   │   ├── business risk + financial risk + governance/structure
│   │   ├── leverage, coverage, cash-flow stability, refinancing access
│   │   └── secured vs unsecured; senior vs subordinated; bankruptcy priority
│   └── 注意：issuer rating and issue rating can differ when collateral and ranking differ
│
├── M12: Securitization Foundations【考试核心】↔ 2026 Outline P20
│   ├── Structure
│   │   ├── originator -> SPV -> investors; servicer collects cash flows
│   │   ├── bankruptcy remoteness and asset isolation
│   │   └── pass-through vs structured allocation intuition
│   ├── Why securitize
│   │   ├── funding diversification, liquidity transformation, risk redistribution
│   │   └── investors gain tailored exposure but face structural complexity
│   └── 注意：structure changes claim on cash flows; it does not magic away collateral risk
│
├── M13: ABS and Credit Enhancement【考试核心】↔ 2026 Outline P21
│   ├── ABS families
│   │   ├── auto loans, credit cards, receivables, other non-mortgage collateral
│   │   ├── collateral cash flow pattern determines amortization and trigger risk
│   │   └── covered bond keeps dual recourse unlike typical ABS isolation
│   ├── Credit enhancement
│   │   ├── subordination, overcollateralization, excess spread, reserve accounts
│   │   └── guarantees/insurance as external support
│   └── 注意：credit enhancement reallocates loss absorption; it is not free yield
│
└── M14: MBS and CMO Structures【考试核心】↔ 2026 Outline P21
    ├── Mortgage cash-flow risk
    │   ├── borrower prepayment creates contraction risk when rates fall
    │   ├── extension risk grows when rates rise and refinancing slows
    │   └── passthrough investors receive scheduled principal plus prepayments
    ├── Structuring
    │   ├── agency/non-agency distinction; collateral and guarantee analysis
    │   ├── CMO tranches redistribute prepayment timing
    │   └── sequential-pay vs planned allocation intuition
    └── 注意：MBS can show negative convexity because cash flows change against the investor
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报 | 相关性 | 费用/代价 |
|--------|------|------|------|--------|-----------|
| Clean Price vs Full Price | 报价净价 vs 实际付款价 | 混淆会整题算错 | full price 是真实交易金额 | 与 accrued interest 直接相关 | AI 是持有期间应计代价 |
| YTM vs Spot Rate | 单一内含收益率 vs 分期限无套利贴现率 | 只用 YTM 会忽略 term structure | YTM 便于概括，spot 更精确 | 两者共同刻画收益率 | 代价是简化 vs 精确性取舍 |
| Macaulay vs Modified Duration | 时间加权平均 vs 价格敏感度 | 用错会解释错误 | modified 更适合 price approximation | modified 来自 Macaulay | 需考虑 compounding convention |
| Callable vs Putable Bond | 发行人有权赎回 vs 投资者有权回售 | callable 不利投资者，putable 保护投资者 | putable 通常收益率更低 | 都受利率路径影响 | embedded option 改变价格 |
| Credit Spread vs Liquidity Spread | default/credit quality补偿 vs 交易流动性补偿 | 混合解释会错判风险来源 | 都体现在 required yield 上 | 常共同存在 | 代价是融资成本更高 |
| Spot Curve vs Par Curve vs Forward Curve | 单现金流贴现率 vs 平价票息率 vs 隐含未来区间率 | 曲线混用会错价 | 都描述 term structure | 三者可互相推导但含义不同 | 代价是计算口径切换 |
| Modified vs Effective Duration | 固定现金流的 yield sensitivity vs 可变现金流的 repricing sensitivity | 嵌入期权时 modified 易失真 | effective 更接近 option-aware 风险 | 都服务利率风险衡量 | effective 依赖定价模型 |
| ABS vs Covered Bond | 资产隔离证券化 vs 发行人资产池支持且常有 dual recourse | 法律追索与资产隔离不同 | 都把资产池现金流带入融资 | 都受 collateral quality 影响 | 结构与监管代价不同 |

---

## 跨模块关联

```text
Instrument Features
├── Cash-flow structure -> Pricing on coupon dates and between dates
├── Contingency provisions -> Effective duration / convexity
└── Seniority and collateral -> Credit analysis
Pricing and Yield
├── YTM -> fixed-rate spread measures
├── Spot curve -> par curve -> forward curve
└── Holding-period return -> horizon vs Macaulay duration
Risk Layer
├── Yield-based duration -> convexity -> portfolio aggregation
├── Curve-based risk -> key rate duration -> non-parallel shifts
└── Credit spread -> sovereign/corporate analysis -> issue ranking
Securitization
└── SPV structure -> ABS enhancement -> MBS prepayment -> CMO tranching
```

---

## 通用分析框架

### 框架1：债券定价题 SOP

1. 写出每期现金流
2. 判断用单一 YTM 还是 spot rates
3. 贴现求和
4. 如有 quoted price，再区分 clean/full

### 框架2：利率风险题 SOP

1. 先用 modified duration 做一阶方向判断
2. yield move 较大时加 convexity
3. 若债券有 embedded option，警惕 duration 直觉失灵

### 框架3：信用题 SOP

1. 先看 spread 变化方向
2. 再找原因：default / downgrade / liquidity / option
3. 最后回到价格影响

---

## 核心公式速查

### M03-M06 定价、收益率与曲线

| 指标 | 公式 | 考试说明 |
|------|------|----------|
| Coupon Bond Price | `P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N` | `y` 与 coupon frequency 必须同口径 |
| Full Price | `Full Price = Clean Price + Accrued Interest` | invoice price 看 full |
| Accrued Interest | `AI = Coupon per period x Days since last coupon / Days in coupon period` | day-count convention 题先读清 |
| Current Yield | `Annual Coupon / Bond Price` | 只看 coupon income |
| Effective Annual Yield | `EAY = (1 + periodic rate)^m - 1` | 年化 conversion 高频 |
| Discount Yield | `BDY = (FV - P)/FV x 360/t` | 分母是 face value |
| Money Market Yield | `MMY = (FV - P)/P x 360/t` | 分母换成 purchase price |
| Bond Equivalent Yield | `BEY = (FV - P)/P x 365/t` | 与 MMY 的 day basis 区分 |
| Spot Pricing | `P = Σ CF_t/(1+s_t)^t` | 每笔 cash flow 用匹配 spot |
| Forward from Spot | `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^{n-m}` | 先对齐区间长度 |
| Par Rate | `Par coupon = (1 - DF_N)/Σ DF_t` | discount factor 版最稳 |

### M07-M09 回报与利率风险

| 指标 | 公式 | 考试说明 |
|------|------|----------|
| Holding Period Return | `HPR = (Coupon income + reinvestment income + sale price - purchase price)/purchase price` | return source 要拆开 |
| Macaulay Duration | `D_mac = Σ[t x PV(CF_t)] / Price` | cash-flow time weighted average |
| Modified Duration | `D_mod = D_mac/(1+y/m)` | fixed cash-flow % price sensitivity |
| Money Duration | `Money Duration = D_mod x Full Price` | 货币价格变化基础 |
| PVBP | `PVBP ≈ Money Duration x 0.0001` | 1 bp shock |
| Duration Price Approx | `%ΔP ≈ -D_mod x Δy` | 一阶近似 |
| Convexity | `Convexity = [P_- + P_+ - 2P_0] / (P_0 x (Δy)^2)` | 价格重估版常见 |
| Convexity Adjusted Change | `%ΔP ≈ -D x Δy + 0.5 x Convexity x (Δy)^2` | 注意 `Δy` 用小数 |
| Portfolio Duration | `D_p = Σ w_i D_i` | 价值权重，曲线非平行时有限 |

### M10-M14 信用与证券化

| 指标 | 公式 | 考试说明 |
|------|------|----------|
| Expected Credit Loss Intuition | `ECL ≈ PD x LGD x Exposure` | Level I 重点在三因子方向 |
| Loss Given Default | `LGD = 1 - Recovery Rate` | recovery 越高，LGD 越低 |
| Interest Coverage | `EBIT / Interest Expense` 或 `EBITDA / Interest Expense` | 看题目指定 numerator |
| Debt to EBITDA | `Total Debt / EBITDA` | leverage 越高通常信用越弱 |
| Senior Claim Recovery Logic | `Higher priority -> higher expected recovery` | 排名不是公式但常决定答案 |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| clean price 就是付款价 | 实际付款价是 full price |
| current yield 就是总回报 | 它忽略 price change 和 reinvestment |
| YTM 就是每期现金流真实折现率 | 更精确时应使用 spot curve |
| duration 越大收益越高 | duration 衡量的是利率敏感度，不是回报 |
| convexity 只是锦上添花 | yield move 大时很关键 |
| callable bond 对投资者更好 | callable 通常有利发行人 |
| spread 变宽只可能是 default 风险上升 | 也可能是 liquidity 或 option factors |
| MBS 提前还款一定利好投资者 | 再投资风险和负 convexity 可能伤害投资者 |
| high coupon bond 一定 duration 更高 | 通常反而 duration 更低 |
| 债券题都先算 YTM 就够了 | spot/forward/option-adjusted 场景不能偷懒 |
| forward curve 就是市场对未来 spot 的确定预测 | 它首先是当前曲线隐含的无套利关系 |
| floating-rate note 没有利率风险 | reset 会缓释，但 spread 与 reset timing 仍会影响价格 |
| secured debt 一定不会亏损 | collateral 改善 recovery，不消灭信用风险 |
| effective duration 和 modified duration 可随便互换 | 现金流会随利率变时优先 effective measures |
| ABS credit enhancement 提高收益且没有代价 | 它改变 loss allocation，也带来结构和定价取舍 |
