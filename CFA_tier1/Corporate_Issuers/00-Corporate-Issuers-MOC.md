---
title: 00-Corporate-Issuers-MOC
description: CFA Level I Corporate Issuers master MOC for governance, capital budgeting, WACC, leverage, and exam workflows.
subject: Corporate Issuers
topic_area: Corporate_Issuers
level: CFA Level I
exam_weight: 6-9%
exam_format: 单选题
difficulty: 治理概念与价值创造计算并重
note_type: master_moc
status: 学习中
aliases:
  - Corporate Issuers 知识框架
  - 公司金融 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Corporate_Issuers
  - formulas
---

# 00-Corporate-Issuers-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Corporate Issuers - Map of Content |
| description | CFA L1 公司金融科目学习导航：治理、营运资本、资本预算、资本结构、WACC、杠杆与商业模型 |
| subject | Corporate Issuers |
| 权重 | 6-9% |
| 考试形式 | 单选题，概念+计算混合 |
| 难度特点 | 治理偏概念，资本预算和WACC偏计算，资本结构偏策略判断 |
| 学习建议 | 先抓 NPV/WACC，再用治理和营运资本把“价值创造”主线补完整 |
| 状态 | 学习中 |
| tags | CFA L1, Corporate Issuers, MOC |

---

## 最关键：先看现金流创造价值，再看融资如何放大或拖累

Corporate Issuers 的主线是“公司决策是否真的增加股东价值”。

---

## 科目概览

| 模块 | 内容 | 难度 | 必考点 |
|------|------|------|--------|
| M01 | Corporate Structures and Ownership | 概念 | legal forms, stakeholders, claims |
| M02 | Corporate Governance and ESG | 概念+策略 | principal-agent, board, stakeholder conflicts |
| M03 | Working Capital and Liquidity | 计算+策略 | operating cycle, CCC, liquidity policy |
| M04 | Capital Investments | 计算 | incremental cash flow, NPV, IRR, real options |
| M05 | Cost of Capital | 计算 | component costs, WACC, marginal capital |
| M06 | Capital Structure and Leverage | 概念+计算 | DOL, DFL, debt capacity, trade-offs |
| M07 | Business Models | 概念 | revenue model, cost structure, scalability |
| M08 | Capital Allocation Integration | 策略 | governance -> projects -> financing -> value |

---

## Corporate Issuers 核心知识树

```text
Corporate Issuers (M01-M08)
│
├── M01: Corporate Structures and Ownership【考试核心】↔ 2026 Outline: Corporate Structures
│   ├── Legal form and claims
│   │   ├── sole proprietorship, partnership, corporation, limited liability form
│   │   ├── debt contract claims vs equity residual claims
│   │   └── public ownership separates capital provision from day-to-day control
│   ├── Stakeholders
│   │   ├── shareholders, creditors, managers, employees, customers, regulators
│   │   └── stakeholder objective conflicts become governance problems
│   └── 注意：limited liability protects owners from some losses; it does not guarantee firm survival
│
├── M02: Corporate Governance and ESG【考试核心】↔ 2026 Outline: Corporate Governance
│   ├── Agency architecture
│   │   ├── principal-agent conflict: control, information, incentive mismatch
│   │   ├── board oversight, committees, compensation, audit, shareholder rights
│   │   └── weak governance raises capital misallocation and financing risk
│   ├── ESG and stewardship
│   │   ├── material ESG factors alter risk, cash flows, cost of capital
│   │   └── disclosure quality and engagement shape investor assessment
│   └── 注意：governance is not decorative prose; it changes decisions and discount rates
│
├── M03: Working Capital and Liquidity【考试核心】↔ 2026 Outline: Working Capital
│   ├── Operating cycle
│   │   ├── 核心公式
│   │   │   ├── `Operating cycle = DIO + DSO`
│   │   │   └── `Cash conversion cycle = DIO + DSO - DPO`
│   │   ├── inventory days + receivable days - payable days = cash conversion cycle
│   │   ├── receivable quality, inventory policy, supplier terms, seasonality
│   │   └── liquidity buffers protect operations but tie up capital
│   ├── Financing policy
│   │   ├── aggressive policy: lower liquidity cushion, higher rollover pressure
│   │   ├── conservative policy: more stable, more capital intensive
│   │   └── short-term financing choice depends on cash-flow predictability
│   └── 注意：shrinking DIO or DSO helps only if service, sales, and credit quality survive
│
├── M04: Capital Investments【考试核心】↔ 2026 Outline: Capital Investments
│   ├── Cash-flow discipline
│   │   ├── 核心公式
│   │   │   ├── `NPV = Σ CFt/(1+r)^t - Initial Outlay`
│   │   │   ├── `0 = Σ CFt/(1+IRR)^t - Initial Outlay`
│   │   │   └── `PI = PV of future cash inflows / Initial investment`
│   │   ├── use incremental after-tax cash flows; ignore sunk costs
│   │   ├── include opportunity costs, cannibalization, working capital, salvage/tax effects
│   │   └── independent vs mutually exclusive vs capital-rationed decisions
│   ├── Decision criteria
│   │   ├── NPV maximizes value under compatible assumptions
│   │   ├── IRR, PI, payback, discounted payback answer different questions
│   │   └── real options: timing, expansion, abandonment, flexibility
│   └── 注意：financing cash flows usually do not enter project cash flows when discount rate handles financing
│
├── M05: Cost of Capital【考试核心】↔ 2026 Outline: Cost of Capital
│   ├── Component costs
│   │   ├── 核心公式
│   │   │   ├── `After-tax cost of debt = rd(1-T)`
│   │   │   ├── `Cost of preferred = Dp/Pp`
│   │   │   ├── `Cost of equity = rf + β(E(Rm)-rf)` 或 `D1/P0 + g`
│   │   │   └── `WACC = wd rd(1-T) + wp rp + we re`
│   │   ├── debt: after-tax required return on borrowing
│   │   ├── preferred: dividend relative to current price
│   │   └── common equity: CAPM, dividend growth, or risk-premium logic
│   ├── WACC construction
│   │   ├── market-value target weights; marginal cost for new capital
│   │   ├── project risk must match discount rate
│   │   └── flotation and issuance frictions affect financing choices
│   └── 注意：a company WACC is not a universal hurdle rate for every project【考试陷阱】
│
├── M06: Capital Structure and Leverage【考试核心】↔ 2026 Outline: Capital Structure
│   ├── Leverage mechanics
│   │   ├── 核心公式
│   │   │   ├── `DOL = %ΔEBIT / %ΔSales`
│   │   │   ├── `DFL = %ΔEPS / %ΔEBIT`
│   │   │   └── `DTL = DOL x DFL`
│   │   ├── operating leverage from fixed operating costs
│   │   ├── financial leverage from fixed financing costs
│   │   └── total leverage transmits sales shock to EPS shock
│   ├── Structure trade-offs
│   │   ├── debt tax benefit vs financial distress and loss of flexibility
│   │   ├── business risk shapes debt capacity
│   │   └── MM benchmark clarifies which frictions make structure matter
│   └── 注意：higher ROE from leverage may simply be higher risk wearing a nicer jacket
│
├── M07: Business Models【考试核心】↔ 2026 Outline: Business Models
│   ├── Model anatomy
│   │   ├── value proposition, revenue mechanism, customer economics
│   │   ├── asset-light vs asset-heavy; recurring vs transactional revenue
│   │   └── fixed/variable cost mix drives scalability and operating leverage
│   ├── Risk map
│   │   ├── network, platform, subscription, manufacturing, financial-intermediation patterns
│   │   └── model quality shows up in margins, cash conversion, reinvestment needs
│   └── 注意：fast revenue growth without economic unit value can still destroy value
│
└── M08: Capital Allocation Integration【考试核心】↔ Cross-module synthesis
    ├── Governance -> identify accountable decision makers
    ├── Working capital -> preserve operating liquidity
    ├── Capital budgeting -> choose value-adding projects
    ├── Cost of capital -> charge risk-consistent hurdle rates
    └── Capital structure -> fund without overloading resilience
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报 | 相关性 | 费用/代价 |
|--------|------|------|------|--------|-----------|
| NPV vs IRR | 绝对价值创造 vs 相对收益率 | IRR 在 scale/timing conflict 下误导 | NPV 更直接反映 wealth gain | 两者都贴现现金流 | IRR 代价是可能得出错误排序 |
| Aggressive vs Conservative WC Policy | 更高收益/更低流动性 vs 更稳健/更低收益 | aggressive 流动性风险更高 | aggressive 可能提升 ROE | 与融资成本、现金波动强相关 | 保守政策占用更多资本 |
| Business Risk vs Financial Risk | 经营波动 vs 融资结构带来的波动 | 两者叠加放大 EPS/ROE 波动 | 承担更多风险可能要求更高回报 | 与行业/资本结构相关 | 债务成本、财务困境成本 |
| Debt Financing vs Equity Financing | 固定义务资本 vs 剩余索取资本 | debt 有违约风险，equity 稀释控制权 | debt 税盾，equity 灵活 | 与 cash flow stability 相关 | 利息、发行成本、稀释 |
| Market Weights vs Book Weights | 当前市场价值 vs 历史账面价值 | 用错权重会错估 WACC | market weights 更贴近 opportunity cost | 与 valuation 直接相关 | 代价是估算更依赖市场数据 |
| Sunk Cost vs Opportunity Cost | 已发生不可逆成本 vs 放弃的最佳替代价值 | 混入 sunk cost 会污染 NPV | opportunity cost 真正影响选择 | 都常出现在项目叙述中 | 认错成本会错投项目 |
| Company WACC vs Project Hurdle Rate | 公司平均融资成本 vs 风险匹配项目折现率 | 风险错配会错估 NPV | hurdle rate 应服务项目风险 | 都连到资本预算 | 过高/过低折现率都会毁排序 |

---

## 跨模块关联

```text
Governance
├── affects Capital Allocation Quality
│   └── Capital Investments
│       └── WACC
│           └── Capital Structure
└── affects Working Capital Discipline
    └── Liquidity Risk
        └── Business Model Sustainability
```

---

## 通用分析框架

### 框架1：资本预算题 SOP

1. 先分清项目是 independent 还是 mutually exclusive
2. 写现金流时间轴
3. 用适当折现率算 `NPV`
4. 再看 `IRR/PI/payback` 作辅助
5. 如排序冲突，回到 `NPV`

### 框架2：WACC 题 SOP

1. 识别资本来源：debt / preferred / equity
2. 分别算 component costs
3. debt 转 after-tax cost
4. 用 market weights 加权
5. 检查是否误用了 book weights

### 框架3：治理题 SOP

1. 找 principal-agent 冲突
2. 找治理机制是否对齐激励
3. 判断该机制是减少还是放大代理问题

---

## 核心公式速查

### M03 Working Capital

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Operating Cycle | `DIO + DSO` | `M03` | 销售与回款链 |
| Cash Conversion Cycle | `DIO + DSO - DPO` | `M03` | 营运资本核心 |
| DIO | `Average Inventory / COGS x 365` | `M03` | 题目有时给 turnover |
| DSO | `Average Receivables / Revenue x 365` | `M03` | collection speed |
| DPO | `Average Payables / Purchases or COGS x 365` | `M03` | denominator 读题 |
| Current Ratio | `Current Assets / Current Liabilities` | `M03` | liquidity 不等于 efficiency |
| Quick Ratio | `(Cash + Marketable Securities + Receivables)/Current Liabilities` | `M03` | 排除 inventory |

### M04 Capital Investments

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Net Present Value | `NPV = Σ CF_t/(1+r)^t - Initial Outlay` | `M04` | value rule 主指标 |
| Internal Rate of Return | `0 = Σ CF_t/(1+IRR)^t - Initial Outlay` | `M04` | 非常规现金流小心 |
| Profitability Index | `PI = PV of future cash inflows / Initial investment` | `M04` | capital rationing 辅助 |
| Payback Period | `Time until cumulative undiscounted CF recovers outlay` | `M04` | 不代表价值 |
| Discounted Payback | `Time until discounted CF recovers outlay` | `M04` | 仍忽略回收后现金流 |

### M05-M06 Cost of Capital and Leverage

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| After-tax Cost of Debt | `r_d(1-T)` | `M05` | interest tax shield |
| Cost of Preferred | `D_p/P_p` | `M05` | preferred no growth case |
| CAPM Cost of Equity | `r_f + β(E(R_m)-r_f)` | `M05` | 与 Portfolio 联动 |
| Dividend Growth Cost of Equity | `D_1/P_0 + g` | `M05` | stable growth 口径 |
| WACC | `w_d r_d(1-T) + w_p r_p + w_e r_e` | `M05` | market-value weights |
| Degree of Operating Leverage | `%ΔEBIT / %ΔSales` | `M06` | operating fixed costs |
| Degree of Financial Leverage | `%ΔEPS / %ΔEBIT` | `M06` | financing fixed costs |
| Degree of Total Leverage | `DOL x DFL` | `M06` | sales -> EPS |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| IRR 高就一定更好 | mutually exclusive 时通常优先 NPV |
| payback 可以代表价值创造 | payback 忽略 time value 和部分后期现金流 |
| WACC 权重用 book values 也差不多 | 考试优先 market weights |
| debt 永远比 equity 便宜就应多用 debt | 过高杠杆会提高 financial distress cost |
| ESG 只是“好形象” | ESG 会影响风险、现金流和估值 |
| aggressive WC policy 只是管理更高效 | 也意味着更高 liquidity risk |
| current ratio 高一定更好 | 过高可能意味着资本占用低效 |
| DOL 和 DFL 一样 | 一个来自成本结构，一个来自融资结构 |
| MM 理论说资本结构完全不重要 | 那是特定假设下的基准世界 |
| 债务税盾只带来好处 | 同时带来违约与灵活性损失 |
| sunk cost 是项目已经投入的钱所以必须算 | sunk cost 不影响增量决策 |
| 公司的 WACC 就是所有项目的 hurdle rate | 项目风险不同要调折现率 |
