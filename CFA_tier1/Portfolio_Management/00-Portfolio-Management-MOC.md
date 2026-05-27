---
title: "00-Portfolio Management-MOC"
description: "CFA Level I 2026 Portfolio Management 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Portfolio Management"
topic_area: "Portfolio_Management"
level: CFA Level I
exam_year: 2026
exam_weight: "8-12%"
module_count: 6
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Portfolio_Management
---

# Portfolio Management MOC

> **One-line spine 一句话主线**：Portfolio Management converts investor facts into objectives, constraints, risk-return inputs, allocation, behavior-aware implementation, and risk governance.

## 1. Subject Brief 科目定位

- **Exam weight 考试权重**：8-12%.
- **Official modules 官方模块数**：6.
- **Decision sequence 决策顺序**：investor facts -> risk/return estimates -> diversification/CAPM -> IPS -> behavior diagnosis -> risk management.
- **Study contract 学习契约**：先掌握 formula/framework map，再把每道题归到 calculation、IPS classification、bias detection 或 governance process。
- **Core output 考试输出**：calculate risk-return metrics when given data; otherwise translate client facts into IPS, allocation, bias guidance, and risk controls.

## 2. Formula & Framework Map 公式与框架地图

### M01 Portfolio Risk and Return: Part I

| Trigger | Formula / framework | Exam action |
|---|---|---|
| Historical return | Arithmetic mean, geometric mean, real vs nominal comparison | Arithmetic 常用于 single-period expected return; geometric reflects compound growth. |
| Real vs nominal return | Approx: `real return ≈ nominal return - inflation`; exact: `(1+nominal)/(1+inflation)-1` | Inflation-adjusted purchasing power must use real return. |
| Expected portfolio return | `E(R_p)=sum w_i E(R_i)` | Return is weighted average; risk is not. |
| Variance/covariance | `Cov_12 = rho_12 sigma_1 sigma_2` | Correlation controls diversification benefit. |
| Two-asset risk | `sigma_p^2 = w_1^2 sigma_1^2 + w_2^2 sigma_2^2 + 2w_1w_2rho_12sigma_1sigma_2` | If `rho < +1`, diversification reduces risk relative to weighted average risk. |
| Risk-return tradeoff | Risk-averse investors require higher expected return for higher risk | Do not choose highest return without checking risk tolerance and utility. |
| Utility | `U = E(R) - 0.5 A sigma^2` | Higher `A` = more risk averse; choose highest utility for that investor. |

### M02 Portfolio Risk and Return: Part II

| Trigger | Formula / framework | Exam action |
|---|---|---|
| CAL/CML | `E(R_C)=R_f + [(E(R_P)-R_f)/sigma_P] sigma_C` | Slope is Sharpe ratio; borrowing means risky weight `y > 1`. |
| Risky asset weight | `y = [E(R_C)-R_f]/[E(R_P)-R_f]`; `sigma_C = y sigma_P` | Use when target return/risk combines risk-free asset and risky portfolio. |
| Systematic vs nonsystematic risk | Diversification removes nonsystematic risk; market pays only systematic risk | Extra expected return is not required for diversifiable risk. |
| Beta | `beta_i = Cov(R_i,R_M)/Var(R_M)`; `beta_p=sum w_i beta_i` | Beta measures systematic risk, not total risk. |
| CAPM/SML | `E(R_i)=R_f + beta_i[E(R_M)-R_f]` | Required return; compare expected return to required return for mispricing. |
| Performance | Sharpe `(R_p-R_f)/sigma_p`; Treynor `(R_p-R_f)/beta_p`; Jensen alpha `R_p-[R_f+beta_p(R_M-R_f)]`; `M^2` converts Sharpe to return units | Sharpe uses total risk; Treynor/Jensen use beta risk. |

### M03 Portfolio Management Process

| Trigger | Framework | Exam action |
|---|---|---|
| Portfolio perspective | Diversification and risk-return trade-off apply at total portfolio level | Single security suitability depends on portfolio context. |
| Process | Planning -> execution -> feedback | IPS is planning output; rebalancing and performance review are feedback. |
| Investor types | Individuals, banks, endowments, foundations, insurers, pension plans | Match objectives, constraints, liquidity, regulation, tax and time horizon. |
| Pooled vehicles | Mutual funds, ETFs, hedge funds, private equity, separately managed accounts | Compare by liquidity, fees, transparency, regulation and strategy. |
| NAV | `NAV = (assets - liabilities) / shares outstanding` | Pooled vehicle valuation and purchase/redemption questions. |

### M04 IPS and Portfolio Construction

| Trigger | Formula / framework | Exam action |
|---|---|---|
| IPS role | Written link between objectives, constraints, strategic allocation and review | Prevents ad hoc reactions to markets or emotions. |
| Return objective | Required return from spending, liabilities, inflation, fees, taxes | Avoid vague “maximize return.” |
| Risk objective | Ability/capacity + willingness; if conflict, capacity is hard constraint | Stated willingness may be distorted by bias. |
| Constraints | `L-T-T-L-U`: liquidity, time horizon, taxes, legal/regulatory, unique circumstances | Classify facts, do not force every fact into return objective. |
| Asset allocation | Strategic asset allocation drives most portfolio risk/return | Security selection comes after policy allocation. |
| ESG integration | Values, risk control, or return opportunity depending on mandate | Place in objectives/constraints only when client facts support it. |

### M05 Behavioral Biases

| Trigger | Framework | Exam action |
|---|---|---|
| Bias taxonomy | Cognitive errors vs emotional biases | Cognitive: educate/moderate; emotional: often accommodate unless goals are threatened. |
| Belief perseverance | Conservatism, confirmation, representativeness, illusion of control, hindsight | Client holds prior belief despite new evidence. |
| Information processing | Anchoring, mental accounting, framing, availability | Client processes data with flawed shortcut. |
| Emotional biases | Loss aversion, overconfidence, self-control, status quo, endowment, regret aversion | Usually tied to fear, pride, attachment or regret. |
| Detection/guidance | Identify behavior -> classify bias -> investment consequence -> guidance | Guidance must connect to IPS and concrete action. |

### M06 Risk Management

| Trigger | Framework | Exam action |
|---|---|---|
| Risk management definition | Identify, measure, monitor, modify risk to support objectives | Goal is not minimum risk; goal is appropriate risk. |
| Process | Set objectives/tolerance -> identify risks -> measure -> modify -> monitor/communicate | Order questions often test the process. |
| Governance | Board/senior management oversight, policies, limits, reporting, culture | Governance sets accountability and escalation. |
| Risk tolerance | Maximum risk an organization/client is willing and able to accept | Drives limits, allocation and escalation triggers. |
| Risk budgeting | Allocate total risk tolerance across activities/managers/exposures | Links strategy to risk limits. |
| Risk types | Market, credit, liquidity, operational, model, settlement, legal/regulatory, reputational | Classify source before choosing response. |
| Risk modification | Avoid, prevent/control, transfer/hedge, diversify, accept/retain | Tool must match source and objective. |

## 3. Module Atlas 模块地图

| Module | Official module | Active page | Core C+ role |
|---|---|---|---|
| M01 | Portfolio Risk and Return: Part I | [[M01-Portfolio-Risk-and-Return-Part-I]] | Historical return, real vs nominal return, utility and diversification math. |
| M02 | Portfolio Risk and Return: Part II | [[M02-Portfolio-Risk-and-Return-Part-II]] | CAL/CML, systematic risk, beta, CAPM and performance measures. |
| M03 | Portfolio Management: An Overview | [[M03-Portfolio-Management-An-Overview]] | Portfolio process, investor types and pooled vehicles. |
| M04 | Basics of Portfolio Planning and Construction | [[M04-Basics-of-Portfolio-Planning-and-Construction]] | IPS objectives, constraints, asset allocation and ESG integration. |
| M05 | The Behavioral Biases of Individuals | [[M05-The-Behavioral-Biases-of-Individuals]] | Bias taxonomy, detection, investment consequences and guidance. |
| M06 | Introduction to Risk Management | [[M06-Introduction-to-Risk-Management]] | Risk process, governance, tolerance, budgeting, risk types and modification. |

## 4. Curriculum Spine 教材主线

| Module | Official page items / textbook spine | What to extract |
|---|---|---|
| M01 | Historical return and risk; asset characteristics; risk aversion; utility; two/many risky assets; diversification; efficient frontier | Risk-return and diversification mechanics before CAPM. |
| M02 | Risk-free + risky assets; CAL/CML; systematic/nonsystematic risk; return models; beta; CAPM/SML; performance appraisal | Market risk pricing and performance interpretation. |
| M03 | Portfolio perspective; risk-return trade-off; process; investor types; asset management industry; mutual funds and pooled products | Process and vehicle selection. |
| M04 | IPS; objectives; risk tolerance; constraints; client information; asset allocation; ESG | Client facts to portfolio policy. |
| M05 | Bias categories; cognitive errors; emotional biases; market behavior | Diagnosis and corrective guidance. |
| M06 | Risk process; framework; governance; tolerance; budgeting; financial/non-financial risks; risk measurement and modification | Enterprise and portfolio risk control. |

## 5. Exam Routes 做题路线

1. **Risk-return route 风险收益题**：identify return type -> calculate portfolio return/risk -> interpret diversification and risk aversion.
2. **CAPM route 定价题**：calculate beta or required return -> compare with expected return -> decide under/overvalued.
3. **IPS route 客户题**：separate objectives from constraints -> ability vs willingness -> strategic allocation implication.
4. **Behavior route 偏差题**：behavior clue -> cognitive/emotional taxonomy -> consequence -> educate/moderate/accommodate.
5. **Risk route 风险管理题**：risk source -> tolerance/budget -> measure -> modify -> monitor/governance.

## 6. Practice & Mock Evidence Map 题库证据地图

| Evidence target | Track in events | Why it matters |
|---|---|---|
| M01 variance/correlation misses | `topic=M01`, `error_type=portfolio_risk_math` | Return is weighted average; risk depends on covariance. |
| M02 beta/CAPM/performance confusion | `topic=M02`, `error_type=capm_metric_selection` | Sharpe/Treynor/Jensen mistakes are common metric-selection errors. |
| M03 process/vehicle classification | `topic=M03`, `error_type=process_vehicle` | Portfolio process and pooled products are concept-dense. |
| M04 IPS objective vs constraint errors | `topic=M04`, `error_type=ips_classification` | IPS questions punish vague or misclassified facts. |
| M05 bias diagnosis errors | `topic=M05`, `error_type=bias_taxonomy` | Similar client behaviors can map to different biases. |
| M06 risk type/modification errors | `topic=M06`, `error_type=risk_governance` | Risk management questions test sequence and matching response. |

## 7. Review Routes 复习路线

- **30-minute formula loop**：M01 two-asset variance -> M02 CAPM/beta/performance -> M04 required return and L-T-T-L-U.
- **Concept loop**：M03 process -> M05 bias diagnosis -> M06 governance/risk response.
- **Post-error retro**：错题先标 calculation、classification、client-fact extraction 或 metric-selection；再写 next drill。
- **Final recall**：每个 module 用一句话回答 input -> formula/framework -> output -> trap。

## 8. Cross-Subject Interfaces 跨科目接口

| Interface | Portfolio Management consumes/sends | Related subject |
|---|---|---|
| Return and risk math | Means, variance, covariance, correlation, regression beta | Quantitative Methods |
| Required return | CAPM required return and market risk premium | Equity, Corporate Issuers, Fixed Income |
| Client suitability | IPS, objectives, constraints, bias-aware recommendations | Ethics |
| Macro allocation | Business cycle, rates, inflation, FX and geopolitical scenarios | Economics |
| Hedging and risk transfer | Risk modification via futures/options/swaps and liquidity constraints | Derivatives, Fixed Income, Alternatives |
