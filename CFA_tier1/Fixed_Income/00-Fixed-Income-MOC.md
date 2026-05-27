---
title: "00-Fixed Income-MOC"
description: "CFA Level I 2026 Fixed Income 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: CFA Level I
exam_year: 2026
exam_weight: "11-14%"
module_count: 19
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Fixed_Income
---

# Fixed Income MOC

> **一句话核心**：Fixed Income 把 promised cash flows 转成 price, yield, spread, duration, convexity, credit risk, and securitization risk。考试不是只问定义，而是让你判断 cash flow 谁拿、discount rate 用哪个、price 对 yield/curve/spread 怎么动。

---

## 1. Subject Brief 科目定位

- **Exam weight**：11-14%，属于 Level I 中等偏高权重科目。
- **Subject job**：固定收益先读合约与现金流，再定价，再把收益率、利差、期限结构、利率风险、信用风险、证券化结构翻译成可计算的 exam actions。
- **Main spine 主线**：instrument features -> cash-flow structures -> markets/issuance -> valuation/yields/curves -> duration/convexity/curve risk -> credit analysis -> securitization/ABS/MBS。
- **Learning posture**：先背框架，再练公式口径。固定收益错题高发点通常不是公式本身，而是 price quote, compounding, spread benchmark, embedded option, or tranche cash-flow priority 的口径选错。
- **Source anchors**：官方 registry module count = 19；教材 index volume = V6；每个 module 的 EOC practice/solutions href 已在教材索引中记录。

## 2. Formula & Framework Map 公式与框架地图

### 2.1 Bond Cash Flows 债券现金流

- **Plain fixed-rate bond**：periodic coupon + principal at maturity；先确认 coupon rate, frequency, par, maturity, and payment timing。
- **Zero-coupon bond**：single future principal; price = discounted par；duration 接近 maturity。
- **Amortizing bond**：coupon + scheduled principal repayment；average life 短于 final maturity。
- **Floating-rate note (FRN)**：coupon = reference rate + quoted margin；reset 后 price 通常接近 par，但 credit/liquidity change 会让 price 偏离。
- **Embedded option**：call benefits issuer, put/convert benefits investor；option changes cash-flow uncertainty and required yield/spread。

### 2.2 Pricing, YTM, Full/Flat/Accrued 估值与报价

- **Full price**：`Full price = PV(cash flows at market discount rate)`。
- **Flat price**：`Flat price = Full price - Accrued interest`。
- **Accrued interest**：`AI = coupon payment x (days since last coupon / days in coupon period)`；题目常用 day-count convention 触发口径陷阱。
- **YTM**：the single discount rate that equates promised cash flows to price；assumes held to maturity, no default, and reinvestment at YTM for interpretation。
- **Price/yield relation**：yield up -> price down；lower coupon, longer maturity, lower yield level -> higher sensitivity。
- **Matrix pricing**：用 comparable bonds 的 yields/spreads 推断 thinly traded bond 的 required yield or price。

### 2.3 Yield and Spread Measures 收益率与利差

- **Annualized yield periodicity**：`effective annual yield = (1 + periodic rate)^m - 1`；不同 compounding periods 不可直接比较。
- **Current yield**：`annual coupon / flat price`，忽略 capital gain/loss。
- **Yield to call / put / worst**：按 call/put date and price 重新解 IRR；callable bond 常看 yield to worst。
- **Benchmark spread**：bond yield - benchmark yield of similar maturity。
- **G-spread / I-spread / Z-spread**：从单点 benchmark 到 swap/spot curve spread；Z-spread 是加到整条 spot curve 上的 constant spread。
- **Option-adjusted spread (OAS)**：`OAS = Z-spread - option cost` for callable/putable style reasoning。

### 2.4 Money Market Yields 货币市场收益率

- **Bank discount yield (BDY)**：discount/par x 360/days；base 是 face value，不是 price。
- **Holding period yield (HPY)**：return over holding period based on beginning price。
- **Money market yield / add-on yield**：annualizes using price as denominator and 360-day year。
- **Effective annual yield**：compounds holding-period return to 365-day year；考试先识别 denominator, day count, and compounding。

### 2.5 Spot, Par, and Forward Curves 期限结构

- **Spot rate**：zero-coupon rate for a maturity；price coupon bond by discounting each cash flow at its matching spot rate。
- **Par rate**：coupon rate that prices a bond at par for a given maturity。
- **Forward rate**：implied future rate linking spot rates；from spot rates: `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^(n-m)`。
- **Bootstrap logic**：short maturity spot first -> use known earlier spots -> solve longer spot from coupon bond price。
- **Curve comparison**：spot curve prices cash flows; par curve quotes par coupon yields; forward curve shows implied future rates and can be above/below spot curve depending on slope。

### 2.6 Return, Duration, Convexity 利率风险与回报

- **Horizon return**：coupon income + reinvestment income + price change over holding period；investment horizon vs Macaulay duration decides whether price risk or reinvestment risk dominates。
- **Macaulay duration**：weighted average time to receipt of cash flows。
- **Modified duration**：`ModDur = MacDur / (1 + YTM/m)`；approx percentage price change for yield change。
- **Effective duration**：uses `PV-` and `PV+`; best for bonds with embedded options because cash flows may change。
- **Money duration / PVBP**：money duration converts percentage sensitivity into currency; `PVBP ≈ ModDur x full price x 0.0001`。
- **Convexity adjustment**：`%ΔP ≈ -Duration x Δy + 0.5 x Convexity x (Δy)^2`；convexity improves large-rate-change approximation。
- **Key rate duration**：price sensitivity to a non-parallel move at a specific maturity point on the benchmark curve。
- **Empirical duration**：estimated from observed price/yield behavior; useful when analytical assumptions do not capture market behavior。

### 2.7 Credit and Securitization 信用与结构化框架

- **Expected loss**：`EL = probability of default x loss given default`; `recovery rate = 1 - LGD`。
- **Credit spread**：compensates for expected loss, downgrade risk, liquidity, tax, and market risk appetite。
- **Rating lens**：issuer rating vs issue rating; secured/senior debt tends to have better recovery than subordinated/unsecured debt。
- **Government credit**：sovereign capacity/willingness, monetary flexibility, fiscal position, external position, political/institutional strength。
- **Corporate credit**：industry risk + competitive position + management + ratios + debt structure + liquidity。
- **Securitization**：pool assets -> SPE -> issue securities; risks are redistributed through credit enhancement and tranching。
- **ABS/MBS**：ABS focuses collateral cash flows and credit enhancement; MBS adds prepayment/contraction/extension risk; CMO tranching reallocates timing risk。

## 3. Module Atlas 模块地图

| Module | Official module | Primary exam job | Page |
|---|---|---|---|
| M01 | Fixed-Income Instrument Features | 读合约：issuer, maturity, par, coupon, seniority, covenants | [[M01-Fixed-Income-Instrument-Features]] |
| M02 | Fixed-Income Cash Flows and Types | 判断 cash-flow pattern and embedded option beneficiary | [[M02-Fixed-Income-Cash-Flows-and-Types]] |
| M03 | Fixed-Income Issuance and Trading | 市场分层、指数、一级/二级市场 | [[M03-Fixed-Income-Issuance-and-Trading]] |
| M04 | Fixed-Income Markets for Corporate Issuers | corporate funding, repo, IG vs HY issuance | [[M04-Fixed-Income-Markets-for-Corporate-Issuers]] |
| M05 | Fixed-Income Markets for Government Issuers | sovereign, agency, municipal, supranational debt | [[M05-Fixed-Income-Markets-for-Government-Issuers]] |
| M06 | Fixed-Income Bond Valuation: Prices and Yields | price/YTM/full-flat-accrued/matrix pricing | [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] |
| M07 | Yield and Yield Spread Measures for Fixed-Rate Bonds | compounding, YTC/YTP/YTW, spreads, OAS logic | [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] |
| M08 | Yield and Yield Spread Measures for Floating-Rate Instruments | FRN quoted/required margin and money-market yields | [[M08-Yield-and-Yield-Spread-Measures-for-Floating-Rate-Instruments]] |
| M09 | Term Structure: Spot, Par, Forward Curves | bootstrap and translate curves | [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] |
| M10 | Interest Rate Risk and Return | horizon return, price risk vs reinvestment risk, Macaulay duration | [[M10-Interest-Rate-Risk-and-Return]] |
| M11 | Yield-Based Bond Duration Measures and Properties | modified duration, money duration, PVBP, drivers | [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] |
| M12 | Yield-Based Bond Convexity and Portfolio Properties | convexity adjustment and portfolio duration/convexity | [[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]] |
| M13 | Curve-Based and Empirical Risk Measures | effective duration, key rate duration, empirical duration | [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] |
| M14 | Credit Risk | PD/LGD/recovery, ratings, spread drivers | [[M14-Credit-Risk]] |
| M15 | Credit Analysis for Government Issuers | sovereign/non-sovereign credit framework | [[M15-Credit-Analysis-for-Government-Issuers]] |
| M16 | Credit Analysis for Corporate Issuers | qualitative + ratio + seniority/recovery analysis | [[M16-Credit-Analysis-for-Corporate-Issuers]] |
| M17 | Fixed-Income Securitization | benefits, parties, SPE, cash-flow transfer | [[M17-Fixed-Income-Securitization]] |
| M18 | ABS Instrument and Market Features | covered bonds, enhancement, ABS types, CDO/CLO | [[M18-Asset-Backed-Security-Instrument-and-Market-Features]] |
| M19 | MBS Instrument and Market Features | prepayment, RMBS, CMO, CMBS, tranching | [[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]] |

## 4. Curriculum Spine 教材主线

1. **Contract layer 合约层**：M01-M02 define who pays what, when, and under which covenants or contingency provisions。
2. **Market layer 市场层**：M03-M05 explain who issues/trades/funds, and why government/corporate markets use different instruments。
3. **Valuation layer 估值层**：M06-M09 convert cash flows into price, yield, spread, and spot/par/forward curve language。
4. **Risk layer 风险层**：M10-M13 translate yield/curve movement into horizon return, duration, convexity, PVBP, and key-rate exposure。
5. **Credit layer 信用层**：M14-M16 move from expected loss and ratings into sovereign and corporate credit decisions。
6. **Structured layer 证券化层**：M17-M19 explain asset pooling, SPE, credit enhancement, prepayment, and tranche priority。

## 5. Exam Routes 做题路线

- **Price route**：identify cash flows -> choose discount rate or spot curve -> calculate full price -> subtract accrued interest if flat price is asked。
- **Yield route**：identify quote convention -> solve periodic yield -> annualize with correct compounding -> compare YTM/YTC/YTP/YTW。
- **Spread route**：select benchmark -> compute spread -> adjust for curve or option when Z-spread/OAS appears。
- **Curve route**：spot prices each cash flow; par sets price = par; forward connects adjacent spots；遇到 curve wording 先写三者定义。
- **Duration route**：decide yield-based vs curve-based vs empirical；option-free fixed-rate usually modified; embedded-option bond usually effective。
- **Credit route**：start with PD/LGD/recovery -> rating limits -> spread impact -> issuer-specific/government/corporate framework。
- **Securitization route**：identify asset pool -> SPE isolation -> cash-flow waterfall -> credit enhancement/tranche/prepayment risk。

## 6. Practice & Mock Evidence Map 题库证据地图

| Module group | Official EOC anchors | Evidence to capture after practice |
|---|---|---|
| M01-M05 foundations | `CFA2431` to `CFA2435` EOC Q/A | contract term confused, issuer/funding market confused, repo/CP/government agency distinction |
| M06-M09 valuation/yields/curves | `CFA2436` to `CFA2439` EOC Q/A | full vs flat price, accrued interest, compounding, spread benchmark, spot/par/forward setup |
| M10-M13 risk | `CFA2440` to `CFA2443` EOC Q/A | duration type, sign of price change, convexity term, PVBP, key-rate vs parallel shift |
| M14-M16 credit | `CFA2444` to `CFA2446` EOC Q/A | PD/LGD/recovery, rating limitation, sovereign vs corporate factor, seniority/recovery ranking |
| M17-M19 securitization | `CFA2447`, `CFA2449`, `CFA2448` EOC Q/A | SPE role, enhancement, ABS collateral, CMO tranche, prepayment/contraction/extension risk |

After each practice block, record the evidence as `question` if the error is a calculation/definition miss, `bias` if the error is a repeated process issue such as ignoring quote convention, and `agent` if generated explanation invents a convention or unsupported conclusion。

## 7. Review Routes 复习路线

- **30-minute formula pass**：M06 full/flat/accrued -> M07 compounding/spreads -> M08 money-market yields -> M09 spot/par/forward -> M10-M13 duration/convexity/PVBP/key-rate。
- **60-minute conceptual pass**：M01-M05 instrument/market definitions -> M14-M16 credit frameworks -> M17-M19 securitization structure。
- **Mock-eve brief**：write one page with price route, yield route, duration route, credit route, securitization route；do not reread all prose。
- **Post-mock retro**：tag every miss as quote convention, cash-flow timing, curve selection, duration type, credit hierarchy, or tranche/prepayment logic。
- **Pattern trigger**：same `topic + los + error_type` 3 times -> promote to pattern; if a MOC formula/framework is missing, use `moc-gap-review` before patching。

## 8. Cross-Subject Interfaces 跨科目接口

- **Quantitative Methods**：TVM, IRR, compounding, probability/default interpretation, regression-style empirical duration language。
- **Corporate Issuers**：capital structure, leverage, liquidity ratios, seniority, secured/unsecured debt, bankruptcy priority。
- **Financial Statement Analysis**：coverage, leverage, cash-flow ratios, earnings quality used in corporate credit analysis。
- **Derivatives**：embedded options, callable/putable logic, OAS intuition, option-adjusted duration/convexity。
- **Portfolio Management**：duration matching, immunization intuition, key-rate exposure, fixed-income allocation risk。
- **Economics**：yield curve shape, monetary policy, inflation, sovereign risk, macro spread drivers。
- **Alternative Investments**：structured products and securitization cash-flow waterfalls overlap with asset-backed structures。
