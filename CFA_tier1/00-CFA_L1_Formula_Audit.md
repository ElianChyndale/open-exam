---
title: "CFA Level I Formula Coverage Audit"
description: 2026 CFA Level I 考纲公式覆盖审计：缺失公式补全、考纲重点、考纲内无核心公式、超纲扩展标记
level: CFA Level I
curriculum_year: 2026
note_type: formula_audit
status: active
tags:
  - CFA_L1
  - formulas
  - audit
---

# CFA Level I Formula Coverage Audit

## Source and Scope

本审计按 2026 CFA Level I topic outlines / LOS 与本地 `CFA_2026_L1_Complete_Curriculum.md` 对齐。

- 官方范围：CFA Institute 2026 Level I Topic Outlines。
- 教材锚点：`.system/memory/strategy/cfa-2026-epub-textbook-index.md`。
- 本地范围：`CFA_tier1/` 下 10 个科目 MOC 与高频计算模块。
- 补写原则：只补 Level I LOS 可支持的核心公式；概念型 LOS 标记为“考纲内但无核心公式”；明显超出 Level I 的模型标记为“超纲/扩展”。

配套使用方式：

1. 先用教材索引确认某个公式属于哪一模块、哪组小节。
2. 再回到对应 `00-*-MOC.md` 和 `Mxx-*` 模块页检查公式是否已经落到正文。
3. 若刷题暴露缺口，再决定是补公式表、补模块正文，还是只补错题规则。

## Coverage Labels

| 标记 | 含义 | 操作规则 |
|------|------|----------|
| 【考纲重点】 | LOS 中出现 calculate / determine / interpret / evaluate 且考试可直接计算或判断 | 写入主 MOC 公式速查，并在高频模块文件同步 |
| 【考纲内但无核心公式】 | 2026 Level I 范围内，但主要考定义、流程、分类、机制或合规判断 | 不硬造公式，只保留判断链 |
| 【超纲/扩展】 | 有助理解但不是 Level I 必背、或需要完整模型/软件/高级课程 | 明确标记，不混入核心公式 |

## Subject-Level Formula Completion

### Quantitative Methods

已补强：

- `M08` 方差不等双样本 t 检验 / Welch 公式与 Satterthwaite df。
- `M09` 相关系数 t 检验、列联表卡方检验、期望频数、自由度。
- `M10` 预测值与预测区间的 Level I 表达。

考纲内但无核心公式：

- Simulation Methods。
- Big Data and ML。

超纲/扩展：

- 多元回归、完整预测区间标准误推导、机器学习模型数学细节。

### Economics

已补强：

- 市场结构的收益、成本、利润、集中度与 HHI。
- 财政乘数、税收乘数、平衡预算乘数。
- FX 交叉汇率、倒数报价、forward premium、forward points、CIP、买卖价差倒置。

考纲内但无核心公式：

- Business cycles、monetary policy、geopolitics、FX participants / regimes。

超纲/扩展：

- IS-LM、完整福利三角、宏观债务动态深入模型。

### Corporate Issuers

已补强：

- Working capital、operating cycle、CCC、turnover/day ratios。
- NPV、IRR、PI、EAA、OCF tax forms。
- Cost of capital: after-tax debt、preferred、CAPM、DDM、bond-yield-plus-risk-premium、WACC。
- Leverage: DOL/DFL/DTL percentage form and quantity form。

考纲内但无核心公式：

- Corporate structures、stakeholder conflicts、governance、business models。

超纲/扩展：

- APV、MM proof、复杂实物期权定价。

### Financial Statement Analysis

已补强：

- Income statement measures, EPS, direct/indirect CFO conversions。
- FCFF/FCFE。
- Inventory turnover, DIO/DSO/DPO/CCC, LIFO reserve adjustments。
- Liquidity/activity/solvency/profitability ratios。
- Three-step and five-step DuPont。
- Effective/cash tax rates, DTA/DTL direction, accrual quality ratio。

考纲内但无核心公式：

- Reporting framework、audit reports、financial reporting quality classification。

超纲/扩展：

- Pension actuarial detail、full lease amortization schedules、full credit loss models。

### Equity Investments

已补强：

- Margin purchase and short sale margin-call formulas。
- Price/equal/value-weighted indexes, float-adjusted market cap, total return。
- GGM, implied return/growth, sustainable growth。
- Justified P/E, P/B, P/S, P/CF, EV and EV/EBITDA。

考纲内但无核心公式：

- Market organization、market efficiency、equity security types、industry analysis。

超纲/扩展：

- Multi-stage DDM, FCFF/FCFE valuation, residual income model。

### Fixed Income

已补强：

- Bond price, full/clean price, accrued interest, matrix pricing interpolation。
- YTM, current yield, BEY, EAY, BDY, MMY, G-spread, I-spread, Z-spread concept。
- Spot pricing, discount factors, forward rates, par rate。
- HPR, Macaulay duration, modified duration, money duration, PVBP, convexity adjustment。
- Effective duration/convexity, key rate duration。
- ECL intuition, LGD, coverage/leverage metrics, taxable equivalent yield, TIPS adjustment, CPR/SMM, CMBS ratios。

考纲内但无核心公式：

- Instrument features, covenants, issuance/trading, securitization parties and structure。

超纲/扩展：

- OAS modeling、structured product waterfall model、prepayment model。

### Derivatives

已补强：

- Forward price/value under no income, known income, known yield, storage/convenience yield。
- Forward payoff and long forward value。
- Swap net payment and fixed-rate payer value direction。
- Option payoff/profit, put-call parity with known income/yield, synthetics, bounds。
- One-period binomial hedge ratio, borrowing/lending position, risk-neutral probability, option value。

考纲内但无核心公式：

- Market features, uses/risks, exchange vs OTC, hedging/speculation/arbitrage distinctions。

超纲/扩展：

- Black-Scholes, Greeks, multi-period trees, swap curve bootstrapping。

### Alternative Investments

已补强：

- Management / incentive fee logic。
- TVPI/DPI/RVPI/PIC/IRR。
- Real estate NOI/cap rate/property value and growth form。
- Commodity futures carry, roll yield, collateral yield, total return components。
- Hedge fund gross/net exposure and leverage。

考纲内但无核心公式：

- Fund structures, private capital strategies, infrastructure, digital assets。

超纲/扩展：

- PME variants、full LBO model、DeFi protocol yield models。

### Portfolio Management

已补强：

- Portfolio return/variance/correlation。
- Utility and CAL formulas, risky asset weight。
- NAV for pooled vehicles。
- CAPM, beta, portfolio beta, SML。
- Sharpe, Treynor, Jensen alpha, M-squared, tracking error, information ratio。

考纲内但无核心公式：

- Portfolio management process, IPS, behavioral biases, risk management governance。

超纲/扩展：

- Full Markowitz matrix optimization、Black-Litterman、VaR derivation、full attribution。

### Ethical and Professional Standards

已标记：

- Ethics 无核心数值公式。
- 保留 Priority Rule、Stricter Standard Rule、MNPI Gate、Suitability Gate、Conflict Gate、GIPS Logic 作为判断链。

超纲/扩展：

- 国家具体法律判例、GIPS 深层审计技术。

## Maintenance Rule

以后每次新增错题暴露公式缺口时：

1. 先补事件层。
2. 再判断是否是 MOC 公式缺口。
3. 若是考纲内核心公式，补到对应 `00-*-MOC.md` 和模块文件。
4. 若是扩展知识，只能标记【超纲/扩展】，不能混进核心公式表。
