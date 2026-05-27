---
title: "00-Economics-MOC"
description: "CFA Level I 2026 Economics 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Economics"
topic_area: "Economics"
level: CFA Level I
exam_year: 2026
exam_weight: "6-9%"
module_count: 8
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Economics
---

# Economics MOC

> **One-line spine 一句话主线**：Economics turns firm behavior, macro cycles, policy, geopolitics, trade, capital flows, and FX quotes into exam decisions about output, inflation, rates, currency value, and asset risk.

## 1. Subject Brief 科目定位

- **Exam weight 考试权重**：6-9%.
- **Official modules 官方模块数**：8.
- **Decision sequence 决策顺序**：micro structure -> business cycle -> fiscal/monetary policy -> geopolitics/trade -> FX market/regime -> FX calculation.
- **Study contract 学习契约**：先用公式与框架地图做主动回忆，再进入 module page；错题必须落到 `topic + LOS + error_type`，不能只写“宏观理解不熟”。
- **Core output 考试输出**：identify the shock, classify the policy/tool/regime, calculate when needed, then interpret direction and limitation.

## 2. Formula & Framework Map 公式与框架地图

### M01 Firm, Cost, Shutdown, Market Structure

| Trigger | Formula / framework | Exam action |
|---|---|---|
| Profit and cost | `TR = P x Q`; accounting profit = `TR - explicit costs`; economic profit = `TR - explicit - implicit costs` | Economic profit = 0 仍可能代表正常会计利润，不等于亏损。 |
| Breakeven | Breakeven where `TR = TC` or `P = ATC` | `P > ATC` positive economic profit; `P = ATC` normal profit; `P < ATC` economic loss. |
| Shutdown | Short run continue if `P >= AVC`; shut down if `P < AVC` | 先判断短期还是长期；短期固定成本 sunk，不用来决定 shutdown。 |
| Profit maximization | `MR = MC` | 所有市场结构先定 quantity，再从 demand/price rule 找 price。 |
| Economies of scale | LRAC falling = economies; flat = constant returns; rising = diseconomies | 区分 short-run diminishing marginal returns 和 long-run scale effects。 |
| Market structures | Perfect competition: many, homogeneous, no pricing power; monopolistic competition: many differentiated, low barriers; oligopoly: few, strategic interdependence, high barriers; monopoly: one, very high barriers | 题干通常用 barriers、product differentiation、number of sellers、pricing power 组合识别。 |
| Concentration | `CR_n = sum largest n market shares`; `HHI = sum market share_i^2` | HHI 百分数口径 monopoly = `10,000`；指标不能单独证明竞争强度。 |

### M02 Business Cycles and Indicators

| Trigger | Framework | Exam action |
|---|---|---|
| Cycle phases | Recovery -> expansion -> slowdown/peak -> contraction/recession -> trough | 看题目问 current state 还是 expected future。 |
| Indicators | Leading predict; coincident describe now; lagging confirm past | 预测题优先 leading；不要用 unemployment duration 这类 lagging 指标预测未来。 |
| Credit cycle | Credit availability, lending standards, default risk, asset values | 信贷收缩会放大 real economy weakness。 |
| Business behavior | New orders/capex/inventory/housing/labor productivity | Recession bottom 附近可能因 lean production 出现高 productivity。 |

### M03 Fiscal Policy

| Trigger | Formula / framework | Exam action |
|---|---|---|
| Policy actor | Government spending, taxation, transfers, automatic stabilizers | Money supply / policy rate 属于 monetary policy。 |
| Spending multiplier | `1 / (1 - MPC)` | MPC 越高，multiplier 越大；leakages 越多，multiplier 越小。 |
| Tax multiplier | `-MPC / (1 - MPC)` | 税收乘数绝对值小于支出乘数。 |
| Balanced budget multiplier | `1` | G 和 T 同额增加时 AD 通常增加。 |
| Fiscal stance | Expansionary: higher G/transfers or lower T; contractionary opposite | 先看 output gap/unemployment/inflation，再判断方向。 |
| Debt sustainability | Debt/GDP risk depends on growth, interest cost, primary balance, credibility | Level I 多为概念判断，不强行套复杂债务动态。 |

### M04 Monetary Policy

| Trigger | Formula / framework | Exam action |
|---|---|---|
| Central bank roles | Price stability, financial stability, payments system, lender of last resort | Price stability 通常是核心目标。 |
| Tools | Policy rate, open market operations, reserve requirements, asset purchases/QE | 工具改变 reserves, market rates, credit, asset prices, FX。 |
| Transmission | Policy tool -> short rates/reserves -> credit/asset prices/FX -> AD/output -> inflation | `ultimately affects` 常指 inflation，不停在 total demand。 |
| Inflation targeting | Effective target needs independence, credibility, transparency | 题干出现 credibility/commitment 时要连接 expectations。 |
| Current stance | Compare current policy rate with neutral rate | `policy rate < neutral` = expansionary now; `>` = contractionary now。 |
| Limitations | Zero lower bound, liquidity trap, impaired banking channel, uncertain lags | QE 不等于所有低利率情境都有效。 |

### M05 Geopolitics

| Trigger | Framework | Exam action |
|---|---|---|
| Actors | State actors, non-state actors, supranational institutions, firms, NGOs | 先识别 actor 与 objective，再判断 cooperation/competition。 |
| Cooperation | Security, economic interest, resource endowment, standardization, soft power, institutions | Cooperation requires aligned interests and acceptable costs. |
| Risk types | Event risk = date-driven; thematic risk = persistent theme; exogenous risk = unexpected external shock | Ongoing civil war 更像 thematic；earthquake 更像 exogenous。 |
| Investment channels | Supply chain, commodity prices, sanctions, risk premium, capital flows, FX pressure | 输出到 PM scenario analysis, country risk, currency exposure。 |

### M06 International Trade

| Trigger | Formula / framework | Exam action |
|---|---|---|
| Comparative advantage | Lowest opportunity cost; `OC(A) = units B forgone / units A gained` | Absolute advantage 看产出效率，comparative advantage 看机会成本。 |
| Terms of trade | `TOT = export price index / import price index` | TOT 上升通常利好贸易条件。 |
| Tariff | Raises domestic price, lowers import quantity, creates government revenue, deadweight loss | Tariff revenue 是与 quota 的常见区别。 |
| Quota | Quantity limit; creates quota rents | 租金归谁取决于 license allocation。 |
| Export subsidy | Encourages exports, may reduce national welfare | 不要自动当作本国福利增加。 |
| Trading blocs | FTA -> customs union -> common market -> economic union/monetary union | 分清 trade creation vs trade diversion。 |

### M07 FX Market, Quotes, Regimes

| Trigger | Formula / framework | Exam action |
|---|---|---|
| FX market | Spot, forward, swap; participants include banks, corporations, investors, governments/central banks | 题干问 market function 时连接 settlement, hedging, speculation, arbitrage。 |
| Quote convention | `A/B` means 1 unit of A costs B | `A/B` up = A appreciates versus B. |
| Nominal vs real FX | Real exchange rate adjusts nominal rate for relative price levels | 贸易竞争力题不要只看 nominal move。 |
| Regimes | Floating, managed float, peg, currency board, monetary union | Fixed regimes trade policy independence for exchange-rate stability。 |
| Capital restrictions | Limit inflows/outflows, reduce volatility, protect reserves or policy autonomy | 也可能 lower market efficiency and investor confidence。 |

### M08 Cross Rates, Forward Premiums, Arbitrage

| Trigger | Formula / framework | Exam action |
|---|---|---|
| Cross rate | `A/C = (A/B) x (B/C)` | 中间货币必须消掉；bid/ask 用可交易链。 |
| Inverted quote | `bid(B/A)=1/ask(A/B)`; `ask(B/A)=1/bid(A/B)` | 倒数报价 bid/ask 要换边。 |
| Forward premium/discount | `(F - S) / S`; annualized by period count | 先确认 quote direction；premium 是报价货币关系，不是预测保证。 |
| Covered interest parity | `F = S x (1 + i_domestic)/(1 + i_foreign)` | 高利率货币通常 forward discount。 |
| Arbitrage check | Compare quoted forward with no-arbitrage forward | 借低利率、换币、投资高利率、锁 forward，按 cash flow 判断 profit。 |

## 3. Module Atlas 模块地图

| Module | Official module | Active page | Core C+ role |
|---|---|---|---|
| M01 | The Firm and Market Structures | [[M01-The-Firm-and-Market-Structures]] | Cost/profit logic and market-structure identification. |
| M02 | Understanding Business Cycles | [[M02-Understanding-Business-Cycles]] | Phase diagnosis and indicator timing. |
| M03 | Fiscal Policy | [[M03-Fiscal-Policy]] | Government tools, multipliers, debt and implementation lags. |
| M04 | Monetary Policy | [[M04-Monetary-Policy]] | Central bank tools, transmission, inflation and credibility. |
| M05 | Introduction to Geopolitics | [[M05-Introduction-to-Geopolitics]] | Actor/risk classification and investment transmission. |
| M06 | International Trade | [[M06-International-Trade]] | Trade gains, restrictions, subsidies and regional integration. |
| M07 | Capital Flows and the FX Market | [[M07-Capital-Flows-and-the-FX-Market]] | FX participants, quotes, regimes and capital restrictions. |
| M08 | Exchange Rate Calculations | [[M08-Exchange-Rate-Calculations]] | Cross rates, forward points, premiums and no-arbitrage. |

## 4. Curriculum Spine 教材主线

| Module | Official page items / textbook spine | What to extract |
|---|---|---|
| M01 | Breakeven, shutdown, economies of scale; market structures; monopolistic competition; oligopoly; concentration measures | Decision tree from cost condition to market identification. |
| M02 | Business-cycle phases; credit cycles; labor, capital spending, inventories, indicators, nowcasting | Time-order map of signals and economic state. |
| M03 | Monetary vs fiscal intro; objectives; tools; multipliers; fiscal stance; execution difficulty | Tool, multiplier, lag and debt logic. |
| M04 | Central bank roles; tools and transmission; inflation/exchange-rate targeting; limitations; policy mix | Transmission chain and credibility constraints. |
| M05 | State/non-state actors; cooperation; globalization; institutions; geopolitical risk; tools; investment process | Risk taxonomy and channel-to-asset translation. |
| M06 | Benefits/costs of trade; tariffs; quotas; export subsidies; trading blocs | Restriction type, welfare implication and integration level. |
| M07 | FX market, participants, quotations; regimes; capital restrictions | Quote direction, regime trade-offs and capital-flow pressure. |
| M08 | Cross-rate calculations; forward-rate calculations; arbitrage relationships; forward discounts/premiums | Mechanical calculation with bid/ask and no-arbitrage interpretation. |

## 5. Exam Routes 做题路线

1. **Classification route 分类题**：identify actor/tool/regime/market structure -> list defining features -> reject tempting adjacent category.
2. **Direction route 方向题**：state shock -> transmission channel -> output/inflation/rates/FX direction -> limitation.
3. **Formula route 计算题**：write quote/variable definition first -> plug formula -> interpret the sign in words.
4. **Policy route 政策题**：separate fiscal vs monetary -> expansionary/contractionary -> lags/crowding-out/credibility -> asset implication.
5. **FX route 汇率题**：quote convention -> invert/cross if needed -> spot vs forward -> annualize premium -> arbitrage/no-arbitrage conclusion.

## 6. Practice & Mock Evidence Map 题库证据地图

| Evidence target | Track in events | Why it matters |
|---|---|---|
| M01 market-structure/shutdown errors | `topic=M01`, `error_type=classification/calculation` | Most errors come from mixing short-run shutdown with long-run exit. |
| M02 indicator timing errors | `topic=M02`, `error_type=indicator_timing` | Leading vs lagging mistakes distort macro direction. |
| M03/M04 policy confusion | `topic=M03/M04`, `error_type=policy_actor/transmission` | Fiscal/monetary boundary is a repeated trap. |
| M05 risk taxonomy errors | `topic=M05`, `error_type=risk_classification` | Event/thematic/exogenous categories need evidence from date and predictability. |
| M06 tariff/quota/subsidy errors | `topic=M06`, `error_type=trade_restriction` | Welfare and revenue/rent differences are testable. |
| M07/M08 quote and forward errors | `topic=M07/M08`, `error_type=quote_direction/arbitrage` | One quote-direction miss can flip every calculation. |

## 7. Review Routes 复习路线

- **30-minute pre-drill**：M01 shutdown/market structure -> M03/M04 policy actor -> M08 quote/CIP formulas.
- **Post-error retro**：错题先标 `question/bias/agent`，再问“是公式不会、方向反了、分类错了，还是题干 trigger 漏看？”
- **Weekly pattern mining**：若同一 `topic + los + error_type` 出现 3 次，升级为 pattern；有 `moc_target` 时再做 MOC gap review。
- **Final recall**：遮住答案，口述每个 module 的 input -> tool -> output -> trap。

## 8. Cross-Subject Interfaces 跨科目接口

| Interface | Economics sends | Receiving subject |
|---|---|---|
| Rates and inflation | Policy stance, inflation expectations, real/nominal rate logic | Fixed Income, Portfolio Management |
| Required return / macro scenarios | Growth, inflation, FX, geopolitical risk channels | Equity, Corporate Issuers, Portfolio Management |
| FX forwards | Quote conventions, cross rates, CIP | Derivatives, Quantitative Methods |
| Trade and country risk | Tariffs, quotas, sanctions, trade blocs, capital restrictions | Equity, Alternative Investments, Portfolio Management |
| Indicator interpretation | Leading/coincident/lagging, nowcasting caution | Quantitative Methods, Portfolio Management |
