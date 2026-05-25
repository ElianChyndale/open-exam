---
title: 00-Equity-MOC
description: CFA Level I Equity master MOC for markets, indexes, efficiency, company analysis, valuation formulas, and traps.
subject: Equity Investments
topic_area: Equity
level: CFA Level I
exam_weight: 11-14%
exam_format: 单选题
difficulty: 市场概念与估值判断相连
note_type: master_moc
status: 学习中
aliases:
  - Equity 知识框架
  - 股权投资 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Equity
  - formulas
---

# 00-Equity-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Equity Investments - Map of Content |
| description | CFA L1 股权投资科目学习导航：市场结构、指数、市场效率、股票特征、公司分析与估值 |
| subject | Equity Investments |
| 权重 | 11-14% |
| 考试形式 | 单选题，概念+估值计算混合 |
| 难度特点 | 前半段市场结构偏概念，后半段估值偏计算和判断 |
| 学习建议 | 先抓“股票是什么、市场如何交易”，再把估值模型与 FRA/Corporate 连接起来 |
| 状态 | 学习中 |
| tags | CFA L1, Equity, MOC |

---

## 最关键：先看现金流和增长，再问市场价格是否偏离内在价值

Equity 的核心是“企业价值如何变成股票价格，以及价格为何会偏离价值”。

---

## 科目概览

| 模块 | 官方 Module | 内容 | 难度 | 必考点 | 章节文件 |
|------|-------------|------|------|--------|----------|
| M01 | Module 1: Market Organization and Structure | Market Organization and Structure | 概念 | orders, execution, margin, primary vs secondary | [[M01-Market-Organization-and-Structure]] |
| M02 | Module 2: Security Market Indexes | Security Market Indexes | 概念+轻计算 | index return, weighting, rebalancing | [[M02-Security-Market-Indexes]] |
| M03 | Module 3: Market Efficiency | Market Efficiency | 概念 | forms, anomalies, active/passive implications | [[M03-Market-Efficiency]] |
| M04 | Module 4: Overview of Equity Securities | Overview of Equity Securities | 概念 | common/preferred, public/private, foreign shares | [[M04-Overview-of-Equity-Securities]] |
| M05 | Module 5: Company Analysis: Past and Present | Company Analysis: Past and Present | 策略 | business model, profitability, quality of earnings | [[M05-Company-Analysis-Past-and-Present]] |
| M06 | Module 6: Industry and Competitive Analysis | Industry and Competitive Analysis | 策略 | life cycle, competitive forces, pricing power | [[M06-Industry-and-Competitive-Analysis]] |
| M07 | Module 7: Company Analysis: Forecasting | Company Analysis: Forecasting | 策略+计算 | revenue drivers, margins, scenario linkage | [[M07-Company-Analysis-Forecasting]] |
| M08 | Module 8: Equity Valuation: Concepts and Basic Tools | Equity Valuation Concepts and Tools | 计算 | DDM, multiples, justified valuation ratios | [[M08-Equity-Valuation-Concepts]] |

---

## Equity Investments 核心知识树 (Core Knowledge Tree)

```text
Equity Investments (权益投资) (M01-M08)
│
├── M01: Market Organization and Structure (市场组织与结构)【考试核心】↔ 2026 Outline: Market Organization
│   ├── 市场管道 (Market plumbing)
│   │   ├── 初级市场筹集资本，二级市场转让所有权 (primary market raises capital; secondary market transfers ownership)
│   │   ├── 经纪商、自营商、拍卖、报价驱动、订单驱动结构 (broker, dealer, auction, quote-driven, order-driven structures)
│   │   └── 流动性维度：紧度、深度、弹性 (liquidity dimensions: tightness, depth, resiliency)
│   ├── 订单与交易 (Orders and trading)
│   │   ├── 市价单、限价单、止损单、执行与有效期限指令 (market, limit, stop, execution and validity instructions)
│   │   ├── 买卖价差、显性成本、隐性成本、价格影响 (bid-ask spread, explicit cost, implicit cost, price impact)
│   │   └── 保证金买入与卖空改变杠杆与清算风险 (margin purchase and short sale alter leverage and liquidation risk)
│   └── 注意：best price instruction and best execution outcome are related but not identical
│
├── M02: Security Market Indexes (证券市场指数)【考试核心】↔ CFA Institute 2026 Security Market Indexes
│   ├── 指数构建 (Index construction)
│   │   ├── 核心公式 (English)
│   │   │   ├── 价格加权指数：`Price-weighted index = Σ Prices / Divisor`
│   │   │   ├── 等权收益率：`Equal-weighted return = Σ Security Returns / N`
│   │   │   └── 市值加权收益率：`Value-weighted return = Σ weight_i x Return_i`
│   │   ├── 目标市场、成分选择、加权、再平衡、指数重构 (target market, constituent selection, weighting, rebalancing, reconstitution)
│   │   ├── 价格加权、等权、市值加权、基本面加权 (price-weighted, equal-weighted, market-cap-weighted, fundamental-weighted)
│   │   └── 除数调整在股票拆分或成分变更后保持连续性 (divisor adjustment preserves continuity after splits/constituent changes)
│   ├── 指数收益 (Index return)
│   │   ├── 价格收益不包括收入；总收益将收入再投资 (price return excludes income; total return reinvests income)
│   │   ├── 等权加重再平衡与换手率压力 (equal weighting raises rebalancing/turnover pressure)
│   │   └── 指数用途：基准、市场代理、产品标的 (index use: benchmark, market proxy, product underlying)
│   └── 注意：weighting method changes both representation and return pattern【考试陷阱】
│
├── M03: Market Efficiency (市场有效性)【考试核心】↔ 2026 Outline: Market Efficiency
│   ├── 信息集 (Information set)
│   │   ├── 弱式：历史价格与成交量信息 (weak form: past price/volume information)
│   │   ├── 半强式：公开信息 (semi-strong form: public information)
│   │   └── 强式：公开加私有信息 (strong form: public plus private information)
│   ├── 启示 (Implications)
│   │   ├── 交易成本与套利限制很重要 (transaction costs and limits to arbitrage matter)
│   │   ├── 异常现象可能反映行为、风险、数据挖掘或市场摩擦 (anomalies may reflect behavior, risk, data mining, or market friction)
│   │   └── 市场有效性指导主动与被动选择 (efficiency informs active vs passive choice)
│   └── 注意：efficiency is about consistent abnormal return after costs, not about prices never moving
│
├── M04: Overview of Equity Securities (权益证券概览)【考试核心】↔ 2026 Outline: Overview of Equity Securities
│   ├── 权益设计 (Claim design)
│   │   ├── 普通股：剩余索取权、投票权、股息自主决定权、清算剩余 (common shares: residual claim, voting, dividend discretion, liquidation residual)
│   │   ├── 优先股：股息优先、通常有限投票权、类似债券与类似权益特征 (preferred shares: dividend priority, often limited voting, bond-like/equity-like traits)
│   │   └── 可赎回、可回售、累积、参与条款改变投资者权利 (callable, putable, cumulative, participating terms change investor rights)
│   ├── 获取方式与地域 (Access and geography)
│   │   ├── 公开与私募权益证券 (public vs private equity securities)
│   │   ├── 存托凭证与外国所有权敞口 (depositary receipts and foreign ownership exposure)
│   │   └── 流动性、披露、治理、结算差异 (differences in liquidity, disclosure, governance, settlement)
│   └── 注意：equity claim priority is low, but upside participation is not capped like debt
│
├── M05: Company Analysis - Past and Present (公司分析：历史与现状)【考试核心】↔ 2026 Outline: Company Analysis
│   ├── 了解业务 (Understand the business)
│   │   ├── 收入模式、客户经济学、成本结构、资本密集度 (revenue model, customer economics, cost structure, capital intensity)
│   │   ├── 盈利能力、再投资、资产负债表韧性 (profitability, reinvestment, balance-sheet resilience)
│   │   └── 管理层质量与资本配置纪律 (management quality and capital allocation discipline)
│   ├── 理性看待历史 (Read history without worshiping it)
│   │   ├── 正常化与暂时性业绩 (normalized vs transitory performance)
│   │   ├── 会计质量与同行可比性 (accounting quality and peer comparability)
│   │   └── ROE、利润率、周转率、杠杆的驱动因素 (drivers of ROE, margins, turnover, leverage)
│   └── 注意：historical growth becomes useful only after you identify its driver and sustainability
│
├── M06: Industry and Competitive Analysis (行业与竞争分析)【考试核心】↔ 2026 Outline: Industry Analysis
│   ├── 行业视角 (Industry lens)
│   │   ├── 生命周期阶段、周期性、长期趋势、监管 (life-cycle stage, cyclicality, secular change, regulation)
│   │   ├── 需求增长、供给纪律、产能、替代品 (demand growth, supply discipline, capacity, substitution)
│   │   └── 竞争力量塑造定价能力与利润率 (competitive forces shape pricing power and margins)
│   ├── 行业中的公司 (Company within industry)
│   │   ├── 成本优势、差异化、网络效应、转换成本 (cost advantage, differentiation, network effects, switching costs)
│   │   └── 市场份额增长可能创造价值或破坏利润率 (market share gain can be value creating or margin destroying)
│   └── 注意：an attractive industry does not guarantee an attractive stock at its current price
│
├── M07: Company Analysis - Forecasting (公司分析：预测)【考试核心】↔ 2026 Outline: Company Analysis Forecasting
│   ├── 预测主干 (Forecast spine)
│   │   ├── 自上而下宏观/行业假设与自下而上运营驱动因素 (top-down macro/industry assumptions vs bottom-up operating drivers)
│   │   ├── 收入 -> 利润率 -> 盈利/现金流 -> 资产负债表需求 (revenue -> margin -> earnings/cash flow -> balance-sheet needs)
│   │   └── 基准、乐观、悲观情景与催化剂/风险地图 (base, upside, downside scenarios and catalyst/risk map)
│   ├── 预测纪律 (Forecast discipline)
│   │   ├── 增长必须由留存收益、资本回报率或外部资本提供资金 (growth must be funded by retention, returns on capital, or external capital)
│   │   └── 预测期应与竞争优势持续时间匹配 (forecast horizon should fit competitive advantage durability)
│   └── 注意：forecast precision without assumption quality is decoration, not analysis
│
└── M08: Equity Valuation Concepts and Tools (权益估值概念与工具)【考试核心】↔ 2026 Outline: Equity Valuation
    ├── 内在价值 (Intrinsic value)
    │   ├── 核心公式 (English)
    │   │   ├── 戈登增长模型：`P_0 = D_1/(r - g)`
    │   │   ├── 隐含必要收益率：`r = D_1/P_0 + g`
    │   │   ├── 可持续增长率：`g = Retention Ratio x ROE`
    │   │   └── 合理领先市盈率：`P_0/E_1 = Payout Ratio/(r - g)`
    │   ├── 现值逻辑；股息/现金流预期；必要收益率 (present value logic; dividends/cash-flow expectations; required return)
    │   ├── 适用于稳定永续股息增长的戈登增长模型 (Gordon growth for stable perpetual dividend growth)
    │   └── 合理倍数将基本面与价格比率联系起来 (justified multiples connect fundamentals to price ratios)
    ├── 相对估值 (Relative valuation)
    │   ├── 市盈率、市净率、市销率、市现率、EV/EBITDA 与同行选择 (P/E, P/B, P/S, P/CF, EV/EBITDA and peer selection)
    │   ├── 领先与 trailing 分母；周期性与会计可比性 (trailing vs forward denominator; cyclicality and accounting comparability)
    │   └── 估值信号必须经过增长、风险、质量检验 (valuation signal must be tested against growth, risk, quality)
    └── 注意：a low multiple can be cheap, deserved, or both【考试陷阱】
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报 | 相关性 | 费用/代价 |
|--------|------|------|------|--------|-----------|
| Market Order vs Limit Order | 立即执行 vs 价格约束执行 | market order 有价格风险；limit order 有未成交风险 | 取决于执行质量 | 与市场流动性强相关 | implicit cost = slippage/opportunity cost |
| Price-weighted vs Equal-weighted vs Value-weighted | 不同指数构建法 | 权重扭曲风险不同 | 表征市场方式不同 | 与 rebalancing frequency 相关 | equal-weighted turnover 更高 |
| Common vs Preferred | 剩余索取权 vs 较固定收益特征 | common 波动更高 | common 上行大，preferred 更稳定 | 都属于 equity-like claims | preferred 通常收益上限较受限 |
| Weak-form vs Semi-strong-form | 历史价量已反映 vs 公开信息已反映 | 错判形式会错推 active edge | semi-strong 对基本面分析更不友好 | 与 anomaly 讨论相关 | active research cost 可能难回收 |
| DDM vs Multiples | 内在价值贴现法 vs 相对估值法 | DDM 对 r/g 很敏感；multiples 依赖 comparables | DDM 更结构化；multiples 更实务 | 都依赖盈利/现金流质量 | 错选模型会大幅偏估 |
| Price Return vs Total Return Index | 价格变化 vs 价格变化加收入再投资 | 忽略 dividend 会低估 return | total return 更接近投资体验 | 同一 constituent universe | income reinvestment assumption |
| Public vs Private Equity | 公开交易证券 vs 非公开权益 | liquidity/disclosure/governance 风险不同 | private 可能给控制溢价和 illiquidity premium | 都连到企业价值 | diligence 与交易成本不同 |

---

## 跨模块关联

```text
市场组织 (Market Organization)
├── 交易摩擦 -> 指数构建 -> 基准选择 (trading frictions -> index construction -> benchmark choice)
└── 信息流 -> 市场效率 -> 主动/被动含义 (information flow -> market efficiency -> active/passive implications)
权益证券设计 (Equity Security Design)
└── 权利与流动性 -> 必要收益率 -> 估值视角 (rights and liquidity -> required return -> valuation lens)
公司分析 (Company Analysis)
├── 历史 -> 业务质量 -> 行业地位 (history -> business quality -> industry position)
├── 预测驱动因素 -> 盈利/现金流预期 (forecast drivers -> earnings/cash-flow expectations)
└── 预期与风险 -> DDM 与倍数 (expectations + risk -> DDM and multiples)
```

---

## 通用分析框架

### 框架1：股票估值题 SOP

1. 先判断公司适合哪种模型：stable growth 还是 relative valuation
2. 若 dividend stable：优先考虑 `Gordon model`
3. 若同业可比性强：再用 multiples
4. 最后检查假设：`r > g`、可比公司是否真可比

### 框架2：指数题 SOP

1. 先识别 index weighting method
2. 再判断受哪类股票影响最大
3. 最后看是否包含 dividends（price vs total return）

### 框架3：市场效率题 SOP

1. 先识别信息类型：historical / public / private
2. 再匹配 weak / semi-strong / strong
3. 最后推 active edge 是否理论上还能存在

---

## 核心公式速查

### M01-M03 市场、交易与指数

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Leverage Ratio | `Value of Position / Investor Equity` | `M01` | margin 基础 |
| Initial Margin | `Investor Equity / Purchase Value` | `M01` | 先分清 equity 与 loan |
| Margin Call Price, Long | `Loan / [Shares x (1 - Maintenance Margin)]` | `M01` | 高频轻计算 |
| Short Sale Return | `(Initial Proceeds - Repurchase Cost - Costs) / Initial Equity` | `M01` | 注意借券与保证金语境 |
| Price-weighted Index | `Σ Price_i / Divisor` | `M02` | split 后 divisor 调整 |
| Equal-weighted Index Return | `Σ_{i=1}^{N} R_i / N` | `M02` | 再平衡影响不能忘 |
| Value-weighted Index Return | `Σ_{i=1}^{N} w_i R_i` | `M02` | market-cap 权重 |
| Total Return | `(Ending Value + Income - Beginning Value) / Beginning Value` | `M02` | 与 price return 区分 |

### M07-M08 预测与估值

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Sustainable Growth | `g = Retention Ratio x ROE` | `M07` | growth 要有融资逻辑 |
| Gordon Growth Model | `P_0 = D_1/(r - g)` | `M08` | 必须 `r > g` |
| Required Return from GGM | `r = D_1/P_0 + g` | `M08` | implied return |
| Dividend Yield | `D_1/P_0` | `M08` | total expected return 的一部分 |
| Justified Leading P/E | `P_0/E_1 = Payout Ratio/(r - g)` | `M08` | fundamentals link |
| Justified Trailing P/E | `P_0/E_0 = Payout Ratio(1 + g)/(r - g)` | `M08` | denominator 差异 |
| P/B | `Price per share / BVPS` | `M08` | 资产型/金融公司常见 |
| P/S | `Price per share / Sales per share` | `M08` | loss firms 也可能可比 |
| EV | `Equity value + Debt + Preferred + Minority interest - Cash` | `M08` | enterprise multiples 底座 |
| EV/EBITDA | `Enterprise Value / EBITDA` | `M08` | capital structure comparability 较强 |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| limit order 比 market order 更“安全” | 它只是控制价格，不控制成交 |
| price-weighted index 更代表市场整体 | 它更偏向高价股 |
| total return index 和 price return index 基本一样 | 前者包含分红再投资 |
| semi-strong efficiency 表示基本面分析毫无价值 | 只是说公开信息难持续带来超额收益 |
| preferred stock 就是 bond | 它有 mixed characteristics，不等于债券 |
| 低 P/E 一定低估 | 也可能是增长差、风险高或会计质量差 |
| DDM 所有公司都适用 | dividend policy 不稳定时不合适 |
| higher growth 一定意味着更高价值 | 还要看 required return 和可持续性 |
| EV/EBITDA 一定优于 P/E | 只是适用场景不同 |
| 公司分析和估值是两件独立事 | 真正考试常把两者绑在一起考 |
| trailing multiple 和 forward multiple 可直接比 | denominator 口径不同，预期也不同 |
| private equity security 只是 public share 不上市 | liquidity、governance、disclosure 和 control 都会变 |
