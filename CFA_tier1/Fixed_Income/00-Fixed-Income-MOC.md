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

| 模块 | 官方 Module | 内容 | 难度 | 必考点 | 章节文件 |
|------|-------------|------|------|--------|----------|
| M01 | Module 1: Fixed-Income Instrument Features | Instrument Features | 概念 | indenture, covenants, contingency provisions | [[M01-Instrument-Features]] |
| M02 | Module 2: Fixed-Income Cash Flows and Types | Cash Flows and Types | 概念 | fixed vs floating, step-up, amortizing, PIK, CLN | [[M02-Fixed-Income-Cash-Flows]] |
| M03 | Module 3: Fixed-Income Issuance and Trading | Issuance, Trading, and Repo | 概念 | primary/secondary, repos, dealer market | [[M02-Issuance-and-Trading]] |
| M04 | Module 4: Fixed-Income Markets for Corporate Issuers | Corporate Issuer Markets | 概念 | IG vs HY, bank loans, CP, MTNs, deposit notes | [[M04-FI-Markets-Corp-Issuers]] |
| M05 | Module 5: Fixed-Income Markets for Government Issuers | Government Issuer Markets | 概念 | sovereign, agency, supranational, municipal | [[M05-FI-Markets-Government-Issuers]] |
| M06 | Module 6: Fixed-Income Bond Valuation: Prices and Yields | Bond Valuation: Prices and Yields | 计算 | clean/full price, accrued interest, matrix pricing | [[M03-Bond-Valuation]] |
| M07 | Module 7: Yield and Yield Spread Measures for Fixed-Rate Bonds | Fixed-Rate Yield and Spread Measures | 计算 | YTM, annual yield conversion, spread measures | [[M04-Yield-and-Spread-Measures]] |
| M08 | Module 8: Yield and Yield Spread Measures for Floating-Rate Instruments | Floating-Rate and Money Market Measures | 计算 | FRN spreads, discount yield, MMY | [[M05-Floating-Rate-and-Money-Market]] |
| M09 | Module 9: The Term Structure of Interest Rates: Spot, Par, and Forward Curves | Spot, Par, and Forward Curves | 计算 | curve comparison, spot discounting, forwards | [[M06-Spot-Par-and-Forward-Curves]] |
| M10 | Module 10: Interest Rate Risk and Return | Interest Rate Risk and Return | 计算+策略 | return sources, horizon, Macaulay duration | [[M07-Interest-Rate-Risk]] |
| M11 | Module 11: Yield-Based Bond Duration Measures and Properties, Module 12: Yield-Based Bond Convexity and Portfolio Properties | Yield-Based Duration and Convexity | 计算 | modified duration, money duration, PVBP, convexity | [[M08-Duration-and-Convexity]] |
| M12 | Module 13: Curve-Based and Empirical Fixed-Income Risk Measures | Curve-Based and Empirical Risk | 概念+计算 | effective duration, key rate duration | [[M09-Curve-Based-and-Empirical-Risk]] |
| M13 | Module 14: Credit Risk | Credit Risk | 概念 | PD, LGD, ratings, spread volatility | [[M10-Credit-Risk]] |
| M14 | Module 15: Credit Analysis for Government Issuers, Module 16: Credit Analysis for Corporate Issuers | Government and Corporate Credit Analysis | 概念+计算 | sovereign factors, coverage, leverage, priority | [[M11-Government-and-Corporate-Credit]] |
| M16 | Module 17: Fixed-Income Securitization | Securitization Foundations | 概念 | parties, benefits, structure | [[M12-Securitization-Foundations]] |
| M17 | Module 18: Asset-Backed Security (ABS) Instrument and Market Features | ABS and Credit Enhancement | 概念 | covered bonds, internal/external enhancement | [[M13-ABS-and-Credit-Enhancement]] |
| M18 | Module 19: Mortgage-Backed Security (MBS) Instrument and Market Features | Residential MBS and CMO Structures | 概念 | prepayment, contraction/extension, tranche cash flows | [[M14-MBS-and-CMO]] |
| M19 | Module 19: Mortgage-Backed Security (MBS) Instrument and Market Features | Commercial MBS (CMBS) | 概念 | balloon risk, lockout, defeasance, property types | [[M19-CMBS]] |

---

## Fixed Income 核心知识树 (Core Knowledge Tree)

```text
固定收益 (Fixed Income) (M01-M19)
│
├── M01: 工具特征 (Instrument Features)【考试核心】↔ 2026 Outline P18
│   ├── 合同解剖 (Contract Anatomy)
│   │   ├── 发行人/面值/票息/期限/货币/优先级 (issuer/par/coupon/maturity/currency/seniority) (基本条款)
│   │   ├── 债券契约：法律承诺、支付条款、契约条款 (bond indenture: legal promises, payment terms, covenants) (契约内容)
│   │   └── 肯定性契约 vs 否定性契约 (affirmative covenants vs negative covenants)【考试陷阱】(契约类型)
│   └── 或有条款：可赎回利于发行人，可回售利于投资者 (contingency provisions: callable benefits issuer; putable benefits investor) (或有条款)
│
├── M02: 现金流类型 (Cash Flows and Types)【考试核心】↔ 2026 Outline P18
│   ├── 票息结构 (Coupon Structures)
│   │   ├── 固定利率/浮动利率/零息/递延票息 (fixed-rate/floating-rate/zero-coupon/deferred coupon) (票息类型)
│   │   └── 递增票息/摊还债券/通胀挂钩 (step-up/amortizing/inflation-linked) (特殊结构)
│   ├── 特殊工具 (Special Instruments)
│   │   ├── 信用联结票据/实物支付债券 (credit-linked notes/PIK bonds) (结构化工具)
│   │   └── 偿债基金条款 (sinking fund provisions) (本金保护)
│   └── 注意：coupon 的确定性不等于回报确定，价格、再投资和信用仍会变
│
├── M03: 发行、交易与回购 (Issuance, Trading, and Repo)【考试核心】↔ 2026 Outline P18-P19
│   ├── 市场地图 (Market Map)
│   │   ├── 货币市场 vs 资本市场；一级发行 vs 二级交易 (money market vs capital market; primary vs secondary) (市场分类)
│   │   └── 固定收益指数：期限、发行人、信用、货币细分 (fixed-income indexes: maturity, issuer, credit, currency segmentation) (指数细分)
│   └── 回购融资 (Repo Financing)
│       ├── 回购 = 附抵押融资，含 haircut 和交易对手风险 (repo = collateralized financing with haircut and counterparty exposure) (回购融资)
│       └── 回购利率 vs 无担保融资利率 (repo rate vs unsecured rate) (融资成本)
│
├── M04: 公司发行人市场 (Corporate Issuer Markets)【考试核心】↔ 2026 Outline P18-P19
│   ├── 公司债券 (Corporate Bonds)
│   │   ├── 投资级 vs 高收益债券的融资渠道与利差行为 (IG vs HY access and spread behavior) (信用分级)
│   │   └── 公开发行 vs 私募 (public offering vs private placement) (发行方式)
│   ├── 其他融资工具 (Other Funding Instruments)
│   │   ├── 银行贷款/商业票据/中期票据/存款票据 (bank loans/CP/MTNs/deposit notes) (融资工具)
│   │   └── 备用信贷额度支持 CP 评级 (backup credit lines support CP ratings) (信用支持)
│   └── 注意：高收益的"高收益"不等于高回报 (high-yield is not necessarily high-return)
│
├── M05: 政府发行人市场 (Government Issuer Markets)【考试核心】↔ 2026 Outline P18-P19
│   ├── 主权债券 (Sovereign Bonds)
│   │   ├── 发达经济体国债 vs 新兴市场主权债 (developed vs emerging market sovereign) (主权分类)
│   │   └── 通胀挂钩债券 (inflation-linked bonds / TIPS) (通胀保护)
│   ├── 机构与超国家债券 (Agency and Supranational Bonds)
│   │   ├── 准政府/机构债券 (quasi-government / agency bonds) (机构债券)
│   │   └── 超国家债券 (supranational bonds: World Bank, EIB, ADB) (超国家)
│   └── 市政债券 (Municipal Bonds)
│       ├── 一般义务债券 vs 收益债券 (GO bonds vs revenue bonds) (市政类型)
│       └── 税收等价收益率 (taxable equivalent yield) (税收优势)
│
├── M06: 债券估值：价格与收益率 (Bond Valuation: Prices and Yields)【考试核心】↔ 2026 Outline P19
│   ├── 定价引擎 (Pricing Engine)
│   │   ├── 核心公式 (English)
│   │   │   ├── 债券定价公式: `P = Σ C/(1+y/m)^t + FV/(1+y/m)^N`
│   │   │   └── 全价公式: `Full Price = Clean Price + Accrued Interest`
│   │   ├── 债券价值 = 票息现值 + 本金现值 (bond value = coupon PV + principal PV) (估值逻辑)
│   │   ├── 折价/溢价/平价与票息率及 YTM 的关系 (discount/premium/par relation to coupon rate and YTM) (价格状态)
│   │   └── 期限越长、票息越低 -> 价格对收益率变动越敏感 (longer maturity + lower coupon -> price more sensitive to yield change) (敏感度规律)
│   ├── 交易价格惯例 (Trading Price Conventions)
│   │   ├── 全价 = 净价 + 应计利息 (full price = clean price + accrued interest)【考试核心】(全价净价)
│   │   ├── 票息日间定价使用分数期处理 (between-coupon-date pricing uses fractional period handling) (分数期)
│   │   └── 矩阵定价估算非流动性债券的收益率/价格 (matrix pricing estimates yield/price for illiquid bonds) (矩阵定价)
│   └── 注意：quoted clean price 是报价习惯，不是买方最终 cash paid【考试陷阱】
│
├── M07: 固定利率债收益率与利差 (Fixed-Rate Yield and Spread Measures)【考试核心】↔ 2026 Outline P19
│   ├── 收益率视角 (Yield Lens)
│   │   ├── YTM 是承诺现金流和再投资假设下的 IRR (YTM is IRR under promised cash flows and reinvestment assumptions) (到期收益率)
│   │   ├── 当期收益率仅捕捉票息收入 (current yield captures coupon income only) (当期收益)
│   │   └── 年化收益率转换取决于复利频率 (annual yield conversion depends on compounding frequency) (年化转换)
│   ├── 利差视角 (Spread Lens)
│   │   ├── 国债基准利差/插值利差/G-利差 (government benchmark spread/interpolated spread/G-spread) (利差类型)
│   │   ├── 利差包含信用、流动性、期权、税收、技术面因素 (spread embeds credit, liquidity, option, tax, technical factors) (利差成分)
│   │   └── 无期权固定利率债券的价格与收益率呈反向关系 (price and yield move inversely for option-free fixed-rate bonds) (价率关系)
│   └── 注意：same YTM 不代表 same value if timing/risk structure differs
│
├── M08: 浮动利率与货币市场指标 (Floating-Rate and Money Market Measures)【考试核心】↔ 2026 Outline P19
│   ├── 浮动利率工具 (Floating-Rate Instruments)
│   │   ├── 核心公式 (English)
│   │   │   ├── 银行贴现收益率: `BDY = (FV - P)/FV x 360/t`
│   │   │   ├── 货币市场收益率: `MMY = (FV - P)/P x 360/t`
│   │   │   └── 债券等价收益率: `BEY = (FV - P)/P x 365/t`
│   │   ├── 参考利率 + 报价利差；重置缓释但未消除利率风险 (reference rate + quoted margin; reset mitigates but does not erase rate risk) (浮动利率)
│   │   ├── 贴现利差连接偏离面值的价格与所需利差 (discount margin connects price away from par with required spread) (贴现利差)
│   │   └── 信用恶化可在重置后仍使 FRN 低于面值 (credit deterioration can push FRN below par despite resets) (信用风险)
│   ├── 货币市场工具 (Money Market Instruments)
│   │   ├── 贴现基础 vs 加息基础 (discount basis vs add-on basis) (报价基础)
│   │   ├── 银行贴现收益率 vs 货币市场收益率 vs 债券等价收益率 (bank discount yield vs money market yield vs bond equivalent yield) (收益率类型)
│   │   └── 分母陷阱：面值或购买价格；360 天或 365 天 (denominator matters: par or purchase price; 360-day or 365-day year) (分母陷阱)
│   └── 注意：货币市场报价偏爱分母陷阱 (money market quotes love denominator traps)
│
├── M09: 即期、平价与远期曲线 (Spot, Par, and Forward Curves)【考试核心】↔ 2026 Outline P19
│   ├── 曲线词典 (Curve Dictionary)
│   │   ├── 核心公式 (English)
│   │   │   ├── 即期定价公式: `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t`
│   │   │   ├── 远期利率推导: `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^(n-m)`
│   │   │   └── 平价利率公式: `Par rate = (1 - DF_N)/Σ_{t=1}^{N} DF_t`
│   │   ├── 即期曲线以各期限匹配的即期利率贴现单笔现金流 (spot curve discounts a single cash flow at each maturity) (即期曲线)
│   │   ├── 平价曲线给出使债券价格等于面值的票息率 (par curve gives coupon rate making a bond price equal par) (平价曲线)
│   │   └── 远期曲线隐含从当前曲线推算的未来借贷利率 (forward curve implies future borrowing/lending rates from today's curve) (远期曲线)
│   ├── 曲线计算 (Curve Calculations)
│   │   ├── 即期定价：每笔现金流使用其期限匹配的即期利率 (spot pricing: each CF gets its maturity-matched spot rate) (即期定价)
│   │   ├── 从即期推导远期；从链式远期推导即期 (forward from spot; spot from chained forwards) (曲线推导)
│   │   └── 从贴现因子求解平价利率 (par rate solved from discount factors) (平价求解)
│   └── 注意：远期利率是隐含的无套利利率，非确定性预测 (forward rate is an implied no-arbitrage rate, not a guaranteed forecast)
│
├── M10: 利率风险与回报 (Interest Rate Risk and Return)【考试核心】↔ 2026 Outline P19
│   ├── 回报分解 (Return Decomposition)
│   │   ├── 核心公式 (English)
│   │   │   ├── 持有期回报率: `HPR = (coupon + reinvestment income + sale price - purchase price)/purchase price`
│   │   │   └── Macaulay 久期: `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price`
│   │   ├── 票息收入 + 再投资收入 + 价格变动 (coupon income + reinvestment income + price change) (回报来源)
│   │   ├── 回归面值与持有期效应 (pull to par and horizon effect) (面值回归)
│   │   └── 当卖出收益率或再投资率变化时，已实现回报不同 (realized return differs when sale yield or reinvestment rate changes) (已实现回报)
│   ├── 持有期与 Macaulay 久期 (Horizon and Macaulay Duration)
│   │   ├── 投资期限 < Macaulay 久期 -> 价格风险占主导 (investment horizon < Macaulay duration -> price risk dominates) (价格风险)
│   │   ├── 投资期限 > Macaulay 久期 -> 再投资风险占主导 (investment horizon > Macaulay duration -> reinvestment risk dominates) (再投资风险)
│   │   └── Macaulay 久期 = 现金流的时间加权平均 (Macaulay duration = weighted average time to cash flows) (久期定义)
│   └── 注意：久期匹配是关于平衡价格和再投资效应，而非锁定价格 (duration matching is about balancing price and reinvestment effects, not freezing price)
│
├── M11: 基于收益率的久期与凸性 (Yield-Based Duration and Convexity)【考试核心】↔ 2026 Outline P20
│   ├── 久期家族 (Duration Family)
│   │   ├── 核心公式 (English)
│   │   │   ├── 修正久期: `D_mod = D_mac/(1+y/m)`
│   │   │   ├── 货币久期: `Money Duration = D_mod x Full Price`
│   │   │   ├── PVBP: `PVBP ≈ Money Duration x 0.0001`
│   │   │   └── 价格变化近似: `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2`
│   │   ├── 修正久期估计价格对收益率变动的百分比敏感度 (modified duration estimates % price sensitivity to yield) (修正久期)
│   │   ├── 货币久期估计每单位收益率变动的货币价格变化 (money duration estimates currency price change per yield unit) (货币久期)
│   │   └── PVBP = 收益率变动 1bp 的价格变化 (PVBP = price change for 1 bp yield shift) (基点价值)
│   ├── 凸性 (Convexity)
│   │   ├── 凸性修正久期遗漏的曲率 (convexity corrects curvature missed by duration) (凸性作用)
│   │   ├── 正凸性有利于对称收益率变动 (positive convexity helps for symmetric yield moves) (正凸性)
│   │   └── 组合久期/凸性使用价值权重但有局限性 (portfolio duration/convexity use value weights with limitations) (组合局限)
│   └── 注意：久期是局部的、基于收益率的；勿将其视为完整曲线压力测试 (duration is local and yield-based; do not treat it as a full curve stress test)
│
├── M12: 曲线与实证风险度量 (Curve-Based and Empirical Risk Measures)【考试核心】↔ 2026 Outline P20
│   ├── 期权感知风险 (Option-Aware Risk)
│   │   ├── 有效久期/有效凸性在现金流可能变化时重新定价 (effective duration/effective convexity reprice when cash flows may change) (有效久期)
│   │   ├── 嵌入期权改变可赎回/提前还款行为 (embedded option changes callability/prepayment behavior) (嵌入期权)
│   │   └── 分析久期可能与观察到的经验久期不同 (analytical duration may differ from observed empirical duration) (经验久期)
│   ├── 曲线风险 (Curve Risk)
│   │   ├── 关键利率久期隔离期限区间的敏感度 (key rate duration isolates maturity-bucket sensitivity) (关键利率)
│   │   ├── 非平行曲线移动打破单一久期直觉 (non-parallel curve shifts break single-duration intuition) (非平行移动)
│   │   └── 基准利率变动与信用利差变动是独立问题 (benchmark shift and credit spread shift are separate questions) (利差独立)
│   └── 注意：可赎回债券和 MBS 的风险不能完全依赖普通修正久期 (callable and MBS risk cannot be fully trusted to plain modified duration)
│
├── M13: 信用风险 (Credit Risk)【考试核心】↔ 2026 Outline P20
│   ├── 损失逻辑 (Loss Logic)
│   │   ├── 预期信用损失 = PD x LGD x 敞口 (expected credit loss intuition = PD x LGD x exposure) (预期损失)
│   │   ├── 违约风险、降级风险、利差风险 (default risk, downgrade risk, spread risk) (信用风险类型)
│   │   └── 回收率与优先级决定损失严重程度 (recovery and seniority shape loss severity) (损失程度)
│   ├── 评级与利差驱动因素 (Ratings and Spread Drivers)
│   │   ├── 评级总结相对信用风险但非保证 (ratings summarize relative credit risk but are not guarantees) (评级作用)
│   │   ├── 宏观、市场、发行人因素影响利差水平与波动性 (macro, market, issuer factors move spread level and volatility) (利差因素)
│   │   └── 流动性和期权特征可与纯信用利差共存 (liquidity and optionality can coexist with pure credit spread) (利差混合)
│   └── 注意：利差常在违约前走阔，因为所需补偿发生了变化 (a spread widens before default often because required compensation changed)
│
├── M14: 政府与公司信用分析 (Government and Corporate Credit Analysis)【考试核心】↔ 2026 Outline P20
│   ├── 政府发行人 (Government Issuers)
│   │   ├── 货币主权、财政灵活性、外部头寸、政治风险 (monetary sovereignty, fiscal flexibility, external position, political risk) (主权因素)
│   │   └── 主权与非主权发行人的支持假设不同 (sovereign and non-sovereign issuers do not share identical support assumptions) (支持差异)
│   ├── 公司发行人 (Corporate Issuers)
│   │   ├── 商业风险 + 财务风险 + 治理结构 (business risk + financial risk + governance/structure) (风险框架)
│   │   ├── 杠杆率、覆盖率、现金流稳定性、再融资渠道 (leverage, coverage, cash-flow stability, refinancing access) (信用指标)
│   │   └── 担保 vs 无担保；优先 vs 次级；破产优先级 (secured vs unsecured; senior vs subordinated; bankruptcy priority) (清偿顺序)
│   └── 注意：发行人评级与债项评级在抵押品和清偿顺序不同时可能不同 (issuer rating and issue rating can differ when collateral and ranking differ)
│
├── M16: 资产证券化基础 (Securitization Foundations)【考试核心】↔ 2026 Outline P20
│   ├── 结构 (Structure)
│   │   ├── 发起人 -> SPV -> 投资者；服务机构收取现金流 (originator -> SPV -> investors; servicer collects cash flows) (SPV结构)
│   │   ├── 破产隔离与资产隔离 (bankruptcy remoteness and asset isolation) (破产隔离)
│   │   └── 过手 vs 结构化分配 (pass-through vs structured allocation intuition) (分配方式)
│   ├── 为何证券化 (Why Securitize)
│   │   ├── 融资多元化、流动性转换、风险再分配 (funding diversification, liquidity transformation, risk redistribution) (证券化优势)
│   │   └── 投资者获得定制化敞口但面临结构复杂性 (investors gain tailored exposure but face structural complexity) (定制风险)
│   └── 注意：结构改变对现金流的请求权，但不能消除抵押品风险 (structure changes claim on cash flows; it does not magic away collateral risk)
│
├── M17: ABS 与信用增级 (ABS and Credit Enhancement)【考试核心】↔ 2026 Outline P21
│   ├── ABS 类型 (ABS Families)
│   │   ├── 汽车贷款、信用卡、应收账款、其他非抵押担保品 (auto loans, credit cards, receivables, other non-mortgage collateral) (ABS类型)
│   │   ├── 担保品现金流模式决定摊还与触发风险 (collateral cash flow pattern determines amortization and trigger risk) (现金流模式)
│   │   └── 有担保债券保持双重追索权，不同于典型 ABS 隔离 (covered bond keeps dual recourse unlike typical ABS isolation) (双重追索)
│   ├── 信用增级 (Credit Enhancement)
│   │   ├── 分层、超额抵押、超额利差、准备金账户 (subordination, overcollateralization, excess spread, reserve accounts) (内部增级)
│   │   └── 担保/保险作为外部支持 (guarantees/insurance as external support) (外部增级)
│   └── 注意：信用增级重新分配损失吸收，而非免费收益 (credit enhancement reallocates loss absorption; it is not free yield)
│
├── M18: 住宅 MBS 与 CMO 结构 (RMBS and CMO Structures)【考试核心】↔ 2026 Outline P21
│   ├── 抵押贷款现金流风险 (Mortgage Cash-Flow Risk)
│   │   ├── 借款人提前还款导致利率下降时的收缩风险 (borrower prepayment creates contraction risk when rates fall) (收缩风险)
│   │   ├── 利率上升且再融资放缓时展期风险增加 (extension risk grows when rates rise and refinancing slows) (展期风险)
│   │   └── 过手投资者收到计划本金加上提前还款 (passthrough investors receive scheduled principal plus prepayments) (过手支付)
│   ├── 结构化 (Structuring)
│   │   ├── 机构/非机构区分；抵押品与担保分析 (agency/non-agency distinction; collateral and guarantee analysis) (机构区分)
│   │   ├── CMO 分层重新分配提前还款时间 (CMO tranches redistribute prepayment timing) (CMO分层)
│   │   └── 顺序偿付 vs 计划分配 (sequential-pay vs planned allocation intuition) (偿付方式)
│   └── 注意：MBS 可能呈现负凸性，因为现金流对投资者不利变化 (MBS can show negative convexity because cash flows change against the investor)
│
└── M19: 商业 MBS (Commercial MBS)【考试核心】↔ 2026 Outline P21
    ├── CMBS 特征 (CMBS Features)
    │   ├── 商业抵押贷款池，气球到期结构 (commercial mortgage pool with balloon maturity) (产品特征)
    │   ├── 气球风险：到期时无法偿还大额剩款 (balloon risk: inability to refinance at maturity) (气球风险)
    │   └── 贷款笔数少，集中度风险高 (fewer loans, higher concentration risk vs RMBS) (集中度)
    ├── 提前还款保护 (Prepayment Protection)
    │   ├── 锁定期/收益率维持/Defeasance (lockout/yield maintenance/defeasance) (保护机制)
    │   └── 提前还款罚金 (prepayment penalty) (罚金结构)
    └── 物业类型与风险 (Property Types and Risk)
        ├── 办公楼/零售/工业/多户/酒店 (office/retail/industrial/multifamily/hotel) (物业类型)
        └── DSCR/LTV/Debt Yield 信用指标 (key credit metrics) (信用度量)
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
工具特征 (Instrument Features)
├── 或有条款 -> 有效久期/凸性 (Contingency provisions -> Effective duration / convexity)
├── 优先级与抵押品 -> 信用分析 (Seniority and collateral -> Credit analysis)
└── 现金流类型 -> 不同票息结构的定价 (Cash-flow types -> Pricing of different coupon structures)
现金流与市场 (Cash Flows and Markets)
├── 浮动利率 -> FRN 定价与贴现利差 (Floating rate -> FRN pricing and discount margin)
├── 公司融资工具 -> 公司信用分析 (Corporate funding instruments -> Corporate credit analysis)
└── 政府发行人 -> 主权信用分析 (Government issuers -> Sovereign credit analysis)
定价与收益率 (Pricing and Yield)
├── YTM -> 固定利率利差度量 (YTM -> fixed-rate spread measures)
├── 即期曲线 -> 平价曲线 -> 远期曲线 (Spot curve -> par curve -> forward curve)
└── 持有期回报 -> 持有期 vs Macaulay 久期 (Holding-period return -> horizon vs Macaulay duration)
风险分层 (Risk Layer)
├── 基于收益率的久期 -> 凸性 -> 组合聚合 (Yield-based duration -> convexity -> portfolio aggregation)
├── 基于曲线的风险 -> 关键利率久期 -> 非平行移动 (Curve-based risk -> key rate duration -> non-parallel shifts)
└── 信用利差 -> 主权/公司分析 -> 债项排名 (Credit spread -> sovereign/corporate analysis -> issue ranking)
证券化 (Securitization)
├── SPV 结构 -> ABS 增级 -> RMBS 提前还款 -> CMO 分层 -> CMBS 气球风险 (SPV structure -> ABS enhancement -> RMBS prepayment -> CMO tranching -> CMBS balloon risk)
└── RMBS 提前还款概念 vs CMBS 提前还款保护 (RMBS prepayment risk vs CMBS prepayment protection)
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

### M06-M09 定价、收益率与曲线

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Coupon Bond Price | `P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N` | `M06` | `y` 与 coupon frequency 必须同口径 |
| Full Price | `Full Price = Clean Price + Accrued Interest` | `M06` | invoice price 看 full |
| Accrued Interest | `AI = Coupon per period x Days since last coupon / Days in coupon period` | `M06` | day-count convention 题先读清 |
| Current Yield | `Annual Coupon / Bond Price` | `M07` | 只看 coupon income |
| Effective Annual Yield | `EAY = (1 + periodic rate)^m - 1` | `M07` | 年化 conversion 高频 |
| Discount Yield | `BDY = (FV - P)/FV x 360/t` | `M08` | 分母是 face value |
| Money Market Yield | `MMY = (FV - P)/P x 360/t` | `M08` | 分母换成 purchase price |
| Bond Equivalent Yield | `BEY = (FV - P)/P x 365/t` | `M08` | 与 MMY 的 day basis 区分 |
| Spot Pricing | `P = Σ_{t=1}^{N} CF_t/(1+s_t)^t` | `M09` | 每笔 cash flow 用匹配 spot |
| Forward from Spot | `(1+s_n)^n = (1+s_m)^m(1+f_{m,n})^{n-m}` | `M09` | 先对齐区间长度 |
| Par Rate | `Par rate = (1 - DF_N)/Σ_{t=1}^{N} DF_t` | `M09` | discount factor 版最稳 |

### M10-M12 回报与利率风险

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Holding Period Return | `HPR = (Coupon income + reinvestment income + sale price - purchase price)/purchase price` | `M10` | return source 要拆开 |
| Macaulay Duration | `D_mac = Σ_{t=1}^{N}[t x PV(CF_t)] / Full Price` | `M10` | cash-flow time weighted average |
| Modified Duration | `D_mod = D_mac/(1+y/m)` | `M11` | fixed cash-flow % price sensitivity |
| Money Duration | `Money Duration = D_mod x Full Price` | `M11` | 货币价格变化基础 |
| PVBP | `PVBP ≈ Money Duration x 0.0001` | `M11` | 1 bp shock |
| Duration Price Approx | `%ΔP ≈ -D_mod x Δy` | `M11` | 一阶近似 |
| Convexity | `Convexity = [P_- + P_+ - 2P_0] / (P_0 x (Δy)^2)` | `M11` | 价格重估版常见 |
| Convexity Adjusted Change | `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2` | `M11` | 注意 `Δy` 用小数 |
| Portfolio Duration | `D_p = Σ w_i D_i` | `M11` | 价值权重，曲线非平行时有限 |

### M13-M19 信用与证券化

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Expected Credit Loss Intuition | `ECL ≈ PD x LGD x Exposure` | `M10` | Level I 重点在三因子方向 |
| Loss Given Default | `LGD = 1 - Recovery Rate` | `M10` | recovery 越高，LGD 越低 |
| Interest Coverage | `EBIT / Interest Expense` 或 `EBITDA / Interest Expense` | `M11` | 看题目指定 numerator |
| Debt to EBITDA | `Total Debt / EBITDA` | `M11` | leverage 越高通常信用越弱 |
| Senior Claim Recovery Logic | `Higher priority -> higher expected recovery` | `M11` | 排名不是公式但常决定答案 |

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
