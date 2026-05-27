---
title: "00-Equity Investments-MOC"
description: "CFA Level I 2026 Equity Investments 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Equity Investments"
topic_area: "Equity"
level: CFA Level I
exam_year: 2026
exam_weight: "11-14%"
module_count: 8
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Equity
---

# Equity Investments MOC

> **一句话核心**：Equity 把市场如何交易、公司如何竞争、现金流如何预测、股票如何估值连成一条 investment decision chain。

## 1. Subject Brief 科目定位

- **Exam role**: 11-14% 权重，重点不是背股票名词，而是判断 market quality、index mechanics、company economics 与 valuation input 是否一致。
- **Core question**: `What is the equity worth, and why might market price differ from intrinsic value?`
- **Learning path**: M01-M03 建立市场与价格形成环境；M04-M07 建立公司、行业、预测输入；M08 把输入转成 value estimate。
- **Output standard**: 每个结论必须能落到 `classification -> driver -> formula/framework -> investment implication`。

## 2. Formula & Framework Map 公式与框架地图

### A. Market Organization / Orders / Market Quality

| Tool | Formula / Framework | Exam use |
|---|---|---|
| Leverage ratio | `leverage = asset value / equity` | 判断 margin position 放大收益与亏损。 |
| Margin return | `return = (ending equity - beginning equity) / beginning equity` | 先重建 equity account，再算 investor return。 |
| Margin call price | Long: `P = P0(1 - initial margin)/(1 - maintenance margin)`; Short: `P = P0(1 + initial margin)/(1 + maintenance margin)` | 方向先判 long/short，避免把 price trigger 反向。 |
| Order taxonomy | execution: market/limit/stop/stop-limit; validity: day/GTC; clearing: instruction for settlement | 题干问 certainty of execution 用 market；问 price protection 用 limit。 |
| Market structure | quote-driven / order-driven / brokered | quote-driven 看 dealer inventory；order-driven 看 matching rules；brokered 适合 unique/illiquid trades。 |
| Market quality | liquidity, transparency, assurity of completion, low transaction costs, price discovery | 判断制度或市场结构是否改善 price discovery 与 capital allocation efficiency。 |

### B. Indexes / Weighting / Rebalancing

| Tool | Formula / Framework | Exam use |
|---|---|---|
| Index value | `index = sum adjusted market values / divisor` | divisor handles splits, additions, deletions, non-market-value changes。 |
| Price return | `(ending price index - beginning price index) / beginning price index` | 不含 dividend/interest。 |
| Total return | `(ending value + income - beginning value) / beginning value` | 收入再投资假设常被隐藏。 |
| Price-weighted | `sum prices / divisor` | 高价股影响大；split requires divisor adjustment。 |
| Equal-weighted | average constituent returns or equal initial weights | small-cap tilt；requires frequent rebalancing。 |
| Market-cap weighted | `price x shares outstanding` weights | large-cap dominated；low turnover；float-adjusted excludes non-free-float shares。 |
| Fundamental weighted | weights by sales/cash flow/book/dividends | avoids price-driven weights but may create value tilt。 |
| Rebalancing vs reconstitution | rebalance resets weights; reconstitute changes constituents | 看到 weights drift 选 rebalancing；看到 add/delete securities 选 reconstitution。 |

### C. Market Efficiency

| Tool | Framework | Exam use |
|---|---|---|
| Value distinction | market value = traded price; intrinsic value = analyst estimate from fundamentals | Mispricing requires model-based intrinsic value, not just price movement。 |
| Efficiency drivers | many rational participants + low costs + information availability + limits-to-arbitrage low | 题干出现 high transaction costs / short-sale constraints -> lower efficiency。 |
| Forms | weak: past prices; semi-strong: public information; strong: all public and private information | Technical analysis conflicts with weak-form; fundamental abnormal returns conflict with semi-strong。 |
| Anomalies | time-series, momentum/overreaction, size, value, closed-end fund discount, earnings surprise, IPO patterns | 先 classify anomaly，再解释 active/passive implication。 |
| Behavioral link | loss aversion, herding, overconfidence, information cascades | 用来解释 why anomalies may persist, not as proof markets are always inefficient。 |

### D. Equity Securities / Ownership / Public-Private / Non-Domestic

| Tool | Framework | Exam use |
|---|---|---|
| Common vs preference shares | common: residual claim + voting; preference: dividend priority, often no/limited voting | 分清 control rights 与 cash-flow priority。 |
| Preference types | cumulative, non-cumulative, participating, convertible, callable, putable | 题干关键字决定 risk/return profile。 |
| Public vs private equity | public: liquidity/transparency/regulation; private: negotiated valuation, limited liquidity, concentrated ownership | 估值折价和 disclosure 差异高频。 |
| Non-domestic access | direct investing, depository receipts, global registered shares, baskets | ADR/GDR 解决 custody/trading/currency access，但仍有 FX 与 country risk。 |
| Equity value links | market value vs book value; cost of equity vs ROE vs required return | ROE 是 accounting return；required return 是 investor opportunity cost。 |

### E. Company / Industry / Forecasting Frameworks

| Tool | Framework | Exam use |
|---|---|---|
| Company report spine | business model -> revenue drivers -> profitability -> working capital -> capex/capital structure -> valuation | 研究报告题按链条补缺。 |
| Revenue drivers | price x volume, mix, market share, market growth, pricing power | pricing power 来自 differentiation, brand, switching costs, supply/demand tightness。 |
| Working capital | receivables + inventory - payables; turnover and days measures | 连接 FSA 与 Corporate Issuers liquidity。 |
| Industry classification | products/services, business-cycle sensitivity, statistical clustering, supply-chain position, GICS-like schemes | 第三方分类便于比较，但可能掩盖 diversified companies。 |
| Porter Five Forces | entrants, substitutes, buyers, suppliers, rivalry | force stronger -> expected profitability lower, unless company has offsetting competitive position。 |
| PESTLE | political, economic, social, technological, legal, environmental | 用于 external influences，不替代 Five Forces。 |
| Forecast approaches | historical trend, base rates/convergence, management guidance, analyst discretionary forecast | forecast horizon 与 disclosure granularity 必须匹配。 |
| Scenario analysis | base/upside/downside with explicit drivers | 改 drivers，不是随意改 valuation output。 |

### F. Equity Valuation Tools

| Tool | Formula / Framework | Exam use |
|---|---|---|
| Valuation decision | if `estimated value > market price` undervalued; if `<` overvalued | 先比较 value estimate 与 price，再给 recommendation language。 |
| DDM general | `V0 = sum Dt / (1 + r)^t` | dividends are cash flows to shareholders。 |
| FCFE model | `V0 = sum FCFEt / (1 + r)^t` | company does not pay stable dividends or dividends differ from capacity。 |
| Preferred stock | `V0 = Dp / rp` | non-callable, non-convertible preferred as perpetuity。 |
| Gordon growth | `V0 = D1 / (r - g)`; `D1 = D0(1+g)` | requires `r > g`, stable growth, mature firm。 |
| Implied required return | `r = D1/P0 + g` | dividend yield + growth。 |
| Implied growth | `g = r - D1/P0` | use only under constant-growth assumptions。 |
| Two-stage DDM | PV of high-growth dividends + PV of terminal value | terminal value at start of stable stage, then discount back。 |
| Multiples | `P/E`, `P/CF`, `P/S`, `P/B`; compare to fundamentals and peers | numerator must match denominator equity claim。 |
| Enterprise value | `EV = market value of debt + market value of equity - cash/investments` | EV multiples match pre-debt measures such as EBITDA。 |
| Asset-based value | assets minus liabilities, adjusted to market values | best for asset-heavy firms; weak for going-concern intangibles。 |

## 3. Module Atlas 模块地图

| Module | Official focus | C+ anchor |
|---|---|---|
| [[M01-Market-Organization-and-Structure]] | Financial system, securities, intermediaries, orders, markets, regulation | 市场功能 + order execution + margin mechanics。 |
| [[M02-Security-Market-Indexes]] | Index value/return, construction, weighting, rebalancing, uses | weighting method drives return, risk, turnover, bias。 |
| [[M03-Market-Efficiency]] | Efficiency forms, anomalies, behavioral finance | 信息集决定 active strategy 是否可持续。 |
| [[M04-Overview-of-Equity-Securities]] | Equity types, ownership rights, public/private, non-domestic investing | cash-flow claim, control right, liquidity, risk-return。 |
| [[M05-Company-Analysis-Past-and-Present]] | Research reports, business model, revenue, profitability, working capital, capital structure | 从历史事实提取 forecast drivers。 |
| [[M06-Industry-and-Competitive-Analysis]] | Industry classification, survey, Five Forces, PESTLE, competitive position | 行业结构决定 sustainable profitability。 |
| [[M07-Company-Analysis-Forecasting]] | Forecast objects, approaches, revenue/cost/WC/capex/capital structure, scenarios | forecast assumptions must trace to drivers。 |
| [[M08-Equity-Valuation-Concepts-and-Basic-Tools]] | Value vs price, DDM, FCFE, preferred, Gordon, multistage, multiples, EV, asset-based | 把 cash flow and required return 转成 intrinsic value。 |

## 4. Curriculum Spine 教材主线

1. **Market spine**: financial system functions -> assets/contracts -> intermediaries -> positions/orders -> primary/secondary markets -> regulation and market quality.
2. **Index spine**: define target market -> select constituents -> choose weighting -> calculate value/return -> rebalance/reconstitute -> use as benchmark/proxy/product.
3. **Efficiency spine**: information set -> cost/frictions -> efficiency form -> anomaly or strategy implication.
4. **Issuer spine**: equity security rights -> business model -> revenue/profitability/working capital -> industry structure -> forecast inputs.
5. **Valuation spine**: select cash flow model -> estimate `r` and `g` -> calculate value -> compare with price -> explain model limits.

## 5. Exam Routes 做题路线

- **Calculation route**: identify claim and time line -> write formula -> align numerator/denominator -> calculate -> interpret sign and economic meaning.
- **Classification route**: locate keyword -> classify market/order/security/index/model -> state consequence, not just definition.
- **Valuation route**: decide DDM/FCFE/preferred/multiple/EV/asset-based -> check assumptions -> compute or compare -> conclude under/over/fair value.
- **Framework route**: for company/industry questions, move from `driver` to `profitability effect` to `valuation implication`。

## 6. Practice & Mock Evidence Map 题库证据地图

- Source evidence: 2026 official registry and ePub index show end-of-reading practice available for M01-M08.
- **High calculation evidence**: M01 margin/order mechanics, M02 index value/return/weights, M08 preferred/Gordon/two-stage/multiples.
- **High judgment evidence**: M03 efficiency/anomalies, M04 equity security rights, M05 revenue/working capital drivers, M06 Porter/PESTLE, M07 forecasting approach selection.
- **Mock review tag rule**: tag every miss as `market mechanics`, `index weighting`, `efficiency form`, `equity claim`, `company driver`, `industry force`, `forecast assumption`, or `valuation model`。

## 7. Review Routes 复习路线

- **Fast route 45-60 min**: M02 weighting formulas -> M08 valuation formulas -> M01 margin/order triggers -> M03 efficiency forms.
- **Deep route half day**: M05 company drivers -> M06 industry forces -> M07 forecasts -> M08 valuation; finish with 10 mixed valuation questions.
- **Error route**: if calculation error, rewrite formula and units; if concept error, rebuild contrast table; if framework error, force a one-line decision rule.
- **Pre-mock route**: rehearse `r > g`, D1 vs D0, price vs total return, rebalance vs reconstitute, weak/semi-strong/strong, public vs private equity。

## 8. Cross-Subject Interfaces 跨科目接口

| Interface | Link | Why it matters |
|---|---|---|
| Quantitative Methods | returns, discounting, regression intuition | valuation and index returns rely on TVM and return measures。 |
| Economics | market structure, business cycles, industry demand | pricing power, growth and cyclicality feed forecasts。 |
| Financial Statement Analysis | revenue, margins, working capital, book value, cash flow | company analysis and valuation inputs come from statements。 |
| Corporate Issuers | capital structure, WACC, working capital, governance, business models | Equity forecasts and required returns depend on issuer decisions。 |
| Portfolio Management | active/passive choice, benchmarks, systematic risk | indexes and market efficiency shape portfolio implementation。 |
| Alternative Investments | REIT/commodity/hedge fund indexes | index construction extends outside listed equity。 |
