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

## 科目概览（与 CFA 2026 L1 官方课程对齐）

| 模块 | 官方 Module | 内容 | 难度 | 必考点 | 章节文件 |
|------|-------------|------|------|--------|----------|
| M01 | M1: Organizational Forms, Corporate Issuer Features, and Ownership | Corporate Structures and Ownership | 概念 | legal forms, stakeholders, claims | [[M01-Corporate-Structures-and-Ownership]] |
| M02 | M2: Investors and Other Stakeholders | Investors and Other Stakeholders | 概念 | investor types, stakeholder objectives, information asymmetry, analyst role | [[M02-Investors-and-Other-Stakeholders]] |
| M03 | M3: Corporate Governance: Conflicts, Mechanisms, Risks, and Benefits | Corporate Governance and ESG | 概念+策略 | principal-agent, board, stakeholder conflicts | [[M02-Corporate-Governance-and-ESG]] |
| M04 | M4: Working Capital and Liquidity | Working Capital and Liquidity | 计算+策略 | operating cycle, CCC, liquidity policy | [[M03-Working-Capital-and-Liquidity]] |
| M05 | M5: Capital Investments and Capital Allocation | Capital Investments | 计算 | incremental cash flow, NPV, IRR, real options | [[M04-Capital-Investments]] |
| M06 | M5: Capital Investments and Capital Allocation | Cost of Capital | 计算 | component costs, WACC, marginal capital | [[M05-Cost-of-Capital]] |
| M07 | M6: Capital Structure | Capital Structure and Leverage | 概念+计算 | DOL, DFL, debt capacity, trade-offs | [[M06-Capital-Structure-and-Leverage]] |
| M08 | M7: Business Models | Business Models | 概念 | revenue model, cost structure, scalability | [[M07-Business-Models]] |
| M09 | M5: Capital Investments and Capital Allocation | Capital Allocation Integration | 策略 | governance -> projects -> financing -> value | [[M08-Capital-Allocation-Integration]] |

> **差距提示**：
> 1. ~~**官方 M2 "Investors and Other Stakeholders" 完全缺失** -- 已新建 [[M02-Investors-and-Other-Stakeholders]]，涵盖投资者类型、利益相关者关系、信息不对称与分析师角色。~~
> 2. **官方 M5 "Capital Investments and Capital Allocation"** 内容分散在 vault 的 M05 (Capital Investments)、M06 (Cost of Capital) 和 M09 (Capital Allocation Integration) 三个笔记中。官方课程将资本成本视为资本预算的一部分而非独立模块。
> 3. **vault 模块编号与官方不完全对齐**：官方 Corporate Issuers 仅 7 个模块 (M1-M7)，vault 拆分 M5 为三个笔记 (M05-M06, M09)，共 9 个 vault 模块。M08 (Business Models) 对应官方 M7。

---

## Corporate Issuers 核心知识树 (Core Knowledge Tree)

```text
Corporate Issuers (公司金融) (M01-M09)
│
├── M01: Corporate Structures and Ownership (公司结构与所有权)【考试核心】↔ 2026 Outline: Corporate Structures
│   ├── 法律形式与权益类型 (Legal Form & Claims)
│   │   ├── 独资/合伙/公司/有限责任公司 (Sole Proprietorship / Partnership / Corporation / LLC)（企业类型）
│   │   ├── 债务合约索偿权 vs 股权剩余索偿权 (Debt Contract Claims vs Equity Residual Claims)（索偿权）
│   │   └── 公众所有权将资本提供与日常控制分离 (Public Ownership Separates Capital from Control)（两权分离）
│   ├── 利益相关者 (Stakeholders)
│   │   ├── 股东/债权人/管理层/员工/客户/监管机构 (Shareholders, Creditors, Managers, Regulators, etc.)（利益群体）
│   │   └── 利益相关者目标冲突 → 治理问题 (Stakeholder Objective Conflicts)（目标冲突）
│   └── 注意：limited liability protects owners from some losses; it does not guarantee firm survival
│
├── M02: Investors and Other Stakeholders (投资者与其他利益相关者)【考试核心】↔ 2026 Outline: Investors & Stakeholders
│   ├── 投资者类型 (Types of Investors)
│   │   ├── 机构投资者 vs 散户投资者 (Institutional vs Retail Investors)（投资主体）
│   │   ├── 股权投资者 vs 债务投资者 (Equity vs Debt Holders)（权益类型）
│   │   └── 积极所有权、代理投票与受托责任 (Active Ownership, Proxy Voting, Fiduciary Duty)（股东权利）
│   ├── 利益相关者目标与冲突 (Stakeholder Objectives & Conflicts)
│   │   ├── 各利益相关者核心目标差异 (Different Stakeholder Objectives)（目标差异）
│   │   ├── 股东-债权人冲突 / 股东-管理层冲突 / 股东-其他利益相关者冲突（三类冲突）
│   │   └── 资产置换与债务悬置问题 (Asset Substitution & Debt Overhang)（代理问题）
│   ├── 信息不对称 (Information Asymmetry)
│   │   ├── 逆向选择 (Adverse Selection) — 交易前信息不对称（事前不对称）
│   │   ├── 道德风险 (Moral Hazard) — 交易后信息不对称（事后不对称）
│   │   └── 信号传递 (Signaling) — 管理层通过行动传递私有信息（信号机制）
│   ├── 金融分析师角色 (Role of Financial Analysts)
│   │   ├── 信息中介缓解信息不对称 (Information Intermediary Reduces Asymmetry)（信息中介）
│   │   ├── 卖方 vs 买方 vs 独立分析师 (Sell-Side vs Buy-Side vs Independent)（分析师类型）
│   │   └── 中国墙防止信息不当流动 (Chinese Wall Prevents Improper Information Flow)（信息隔离）
│   └── ESG 与利益相关者视角 (ESG & Stakeholder View)
│       ├── E/S/G 各维度影响不同利益相关者群体 (Each ESG Dimension Affects Different Stakeholders)（ESG维度）
│       └── 利益相关者资本主义 vs 股东至上 (Stakeholder Capitalism vs Shareholder Primacy)（理念对比）
│
├── M03: Corporate Governance and ESG (公司治理与 ESG)【考试核心】↔ 2026 Outline: Corporate Governance
│   ├── 代理架构 (Agency Architecture)
│   │   ├── 委托-代理冲突：控制权、信息、激励不匹配 (Principal-Agent Conflict: Control, Information, Incentive)（代理矛盾）
│   │   ├── 董事会监督/委员会/薪酬/审计/股东权利 (Board Oversight, Committees, Compensation, Audit, Shareholder Rights)（治理机制）
│   │   └── 弱治理导致资本错配与融资风险上升 (Weak Governance Raises Capital Misallocation & Financing Risk)（治理风险）
│   ├── ESG 与受托责任 (ESG and Stewardship)
│   │   ├── 重大 ESG 因素改变风险、现金流与资本成本 (Material ESG Factors Alter Risk, Cash Flows, Cost of Capital)（ESG影响）
│   │   └── 披露质量与投资者沟通影响评估 (Disclosure Quality & Engagement Shape Investor Assessment)（披露评估）
│   └── 注意：governance is not decorative prose; it changes decisions and discount rates
│
├── M04: Working Capital and Liquidity (营运资本与流动性)【考试核心】↔ 2026 Outline: Working Capital
│   ├── 经营周期 (Operating Cycle)
│   │   ├── 核心公式 (English)
│   │   │   ├── `Operating cycle = DIO + DSO` 经营周期
│   │   │   └── `Cash conversion cycle = DIO + DSO - DPO` 现金转换周期
│   │   ├── 存货天数 + 应收天数 - 应付天数 = 现金转换周期 (Cash Conversion Cycle)（现金周期）
│   │   ├── 应收质量/库存政策/供应商条款/季节性因素 (Receivable Quality, Inventory Policy, Supplier Terms, Seasonality)（影响因素）
│   │   └── 流动性缓冲保护运营但占用资本 (Liquidity Buffers Protect Operations but Tie Up Capital)（缓冲权衡）
│   ├── 融资政策 (Financing Policy)
│   │   ├── 激进政策：低流动性缓冲，高展期压力 (Aggressive Policy: Lower Liquidity Cushion, Higher Rollover Pressure)（激进策略）
│   │   ├── 保守政策：更稳定，更资本密集 (Conservative Policy: More Stable, More Capital Intensive)（保守策略）
│   │   └── 短期融资选择取决于现金流可预测性 (Short-Term Financing Choice Depends on Cash-Flow Predictability)（融资选择）
│   └── 注意：shrinking DIO or DSO helps only if service, sales, and credit quality survive
│
├── M05: Capital Investments (资本投资决策)【考试核心】↔ 2026 Outline: Capital Investments
│   ├── 现金流纪律 (Cash-Flow Discipline)
│   │   ├── 核心公式 (English)
│   │   │   ├── `NPV = Σ CFt/(1+r)^t - Initial Outlay` 净现值
│   │   │   ├── `0 = Σ CFt/(1+IRR)^t - Initial Outlay` 内部收益率
│   │   │   └── `PI = PV of future cash inflows / Initial investment` 盈利指数
│   │   ├── 使用增量税后现金流；忽略沉没成本 (Use Incremental After-Tax Cash Flows; Ignore Sunk Costs)（现金流原则）
│   │   ├── 包含机会成本、蚕食效应、营运资本、残值与税务影响 (Include Opportunity Costs, Cannibalization, WC, Salvage/Tax)（调整项目）
│   │   └── 独立项目 vs 互斥项目 vs 资本约束决策 (Independent vs Mutually Exclusive vs Capital-Rationed)（项目类型）
│   ├── 决策标准 (Decision Criteria)
│   │   ├── NPV 在兼容假设下最大化价值 (NPV Maximizes Value Under Compatible Assumptions)（NPV优先）
│   │   ├── IRR、PI、回收期、折现回收期回答不同问题 (IRR, PI, Payback, Discounted Payback Answer Different Questions)（辅助指标）
│   │   └── 实物期权：时机、扩张、放弃、灵活性 (Real Options: Timing, Expansion, Abandonment, Flexibility)（期权价值）
│   └── 注意：financing cash flows usually do not enter project cash flows when discount rate handles financing
│
├── M06: Cost of Capital (资本成本)【考试核心】↔ 2026 Outline: Cost of Capital
│   ├── 各要素成本 (Component Costs)
│   │   ├── 核心公式 (English)
│   │   │   ├── `After-tax cost of debt = rd(1-T)` 税后债务成本
│   │   │   ├── `Cost of preferred = Dp/Pp` 优先股成本
│   │   │   ├── `Cost of equity = r_f + β[E(R_M) - r_f]` 或 `D_1/P_0 + g` 股权成本
│   │   │   └── `WACC = wd rd(1-T) + wp rp + we re` 加权平均资本成本
│   │   ├── 债务：税后借款必要回报率 (Debt: After-Tax Required Return on Borrowing)（债务成本）
│   │   ├── 优先股：相对于当前价格的股息率 (Preferred: Dividend Relative to Current Price)（优先股成本）
│   │   └── 普通股：CAPM、股息增长或风险溢价逻辑 (Common Equity: CAPM, Dividend Growth, or Risk-Premium)（股权成本）
│   ├── WACC 构建 (WACC Construction)
│   │   ├── 市场价值目标权重；新资本的边际成本 (Market-Value Target Weights; Marginal Cost for New Capital)（权重原则）
│   │   ├── 项目风险必须与折现率匹配 (Project Risk Must Match Discount Rate)（风险匹配）
│   │   └── 发行摩擦影响融资选择 (Flotation and Issuance Frictions Affect Financing Choices)（发行摩擦）
│   └── 注意：a company WACC is not a universal hurdle rate for every project【考试陷阱】
│
├── M07: Capital Structure and Leverage (资本结构与杠杆)【考试核心】↔ 2026 Outline: Capital Structure
│   ├── 杠杆机制 (Leverage Mechanics)
│   │   ├── 核心公式 (English)
│   │   │   ├── `DOL = %ΔEBIT / %ΔSales` 经营杠杆度
│   │   │   ├── `DFL = %ΔEPS / %ΔEBIT` 财务杠杆度
│   │   │   └── `DTL = DOL x DFL` 总杠杆度
│   │   ├── 经营杠杆来自固定经营成本 (Operating Leverage from Fixed Operating Costs)（经营杠杆）
│   │   ├── 财务杠杆来自固定融资成本 (Financial Leverage from Fixed Financing Costs)（财务杠杆）
│   │   └── 总杠杆将销售冲击传导为 EPS 冲击 (Total Leverage Transmits Sales Shock to EPS Shock)（总杠杆）
│   ├── 结构权衡 (Structure Trade-Offs)
│   │   ├── 债务税盾 vs 财务困境与灵活性损失 (Debt Tax Benefit vs Financial Distress & Loss of Flexibility)（税盾权衡）
│   │   ├── 经营风险决定债务容量 (Business Risk Shapes Debt Capacity)（债务容量）
│   │   └── MM 基准明确了哪些摩擦让结构变得重要 (MM Benchmark Clarifies Which Frictions Make Structure Matter)（MM理论）
│   └── 注意：higher ROE from leverage may simply be higher risk wearing a nicer jacket
│
├── M08: Business Models (商业模式)【考试核心】↔ 2026 Outline: Business Models
│   ├── 模型解剖 (Model Anatomy)
│   │   ├── 价值主张、收入机制、客户经济学 (Value Proposition, Revenue Mechanism, Customer Economics)（商业要素）
│   │   ├── 轻资产 vs 重资产；经常性 vs 交易性收入 (Asset-Light vs Asset-Heavy; Recurring vs Transactional Revenue)（模式分类）
│   │   └── 固定/可变成本结构决定可扩展性与经营杠杆 (Fixed/Variable Cost Mix Drives Scalability & Operating Leverage)（成本结构）
│   ├── 风险地图 (Risk Map)
│   │   ├── 网络/平台/订阅/制造/金融中介模式 (Network, Platform, Subscription, Manufacturing, Financial-Intermediation)（典型模式）
│   │   └── 模型质量体现在利润率、现金转换、再投资需求 (Model Quality Shows in Margins, Cash Conversion, Reinvestment)（质量指标）
│   └── 注意：fast revenue growth without economic unit value can still destroy value
│
└── M09: Capital Allocation Integration (资本配置整合)【考试核心】↔ Cross-module synthesis
    ├── 治理 → 明确决策责任人 (Governance -> Identify Accountable Decision Makers)
    ├── 营运资本 → 维持经营流动性 (Working Capital -> Preserve Operating Liquidity)
    ├── 资本预算 → 选择增值项目 (Capital Budgeting -> Choose Value-Adding Projects)
    ├── 资本成本 → 设定风险匹配的最低收益率 (Cost of Capital -> Charge Risk-Consistent Hurdle Rates)
    └── 资本结构 → 融资而不过度消耗缓冲 (Capital Structure -> Fund Without Overloading Resilience)
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
├── affects Capital Allocation Quality (中文)
│   └── Capital Investments (中文)
│       └── WACC (中文)
│           └── Capital Structure (中文)
└── affects Working Capital Discipline (中文)
    └── Liquidity Risk (中文)
        └── Business Model Sustainability (中文)
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

### M02 Investors and Other Stakeholders

| 概念 | 核心逻辑 | 知识树节点 | 考试说明 |
|------|----------|------------|----------|
| 信息不对称 | 内部人 vs 外部人的信息差距 | `M02` | 概念理解为主 |
| 逆向选择 | 事前信息不对称导致市场失灵 | `M02` | 区分事前/事后 |
| 道德风险 | 事后信息不对称导致代理行为偏移 | `M02` | 与 M03 治理联动 |
| 信号传递 | 通过资本结构/股息等可信行动传递信息 | `M02` | 区分信号 vs 噪音 |
| 利益相关者冲突 | 不同群体目标不一致导致财富转移 | `M02` | 分析谁受益谁受损 |

### M04 Working Capital

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Operating Cycle | `DIO + DSO` | `M04` | 销售与回款链 |
| Cash Conversion Cycle | `DIO + DSO - DPO` | `M04` | 营运资本核心 |
| DIO | `(Average Inventory / COGS) x 365` | `M04` | 题目有时给 turnover |
| DSO | `(Average Receivables / Revenue) x 365` | `M04` | collection speed |
| DPO | `(Average Payables / Purchases or COGS) x 365` | `M04` | denominator 读题 |
| Current Ratio | `Current Assets / Current Liabilities` | `M04` | liquidity 不等于 efficiency |
| Quick Ratio | `(Cash + Marketable Securities + Receivables)/Current Liabilities` | `M04` | 排除 inventory |

### M05 Capital Investments

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Net Present Value | `NPV = Σ_{t=0}^{N} CF_t/(1 + r)^t` | `M05` | value rule 主指标 |
| Internal Rate of Return | `0 = Σ_{t=0}^{N} CF_t/(1 + IRR)^t` | `M05` | 非常规现金流小心 |
| Profitability Index | `PI = PV of future cash inflows / Initial investment` | `M05` | capital rationing 辅助 |
| Payback Period | `Time until cumulative undiscounted CF recovers outlay` | `M05` | 不代表价值 |
| Discounted Payback | `Time until discounted CF recovers outlay` | `M05` | 仍忽略回收后现金流 |

### M06-M07 Cost of Capital and Leverage

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| After-tax Cost of Debt | `r_d(1 - T)` | `M06` | interest tax shield |
| Cost of Preferred | `r_p = D_p/P_p` | `M06` | preferred no growth case |
| CAPM Cost of Equity | `r_e = r_f + β[E(R_M) - r_f]` | `M06` | 与 Portfolio 联动 |
| Dividend Growth Cost of Equity | `r_e = D_1/P_0 + g` | `M06` | stable growth 口径 |
| WACC | `WACC = w_d r_d(1 - T) + w_p r_p + w_e r_e` | `M06` | market-value weights |
| Degree of Operating Leverage | `%ΔEBIT / %ΔSales` | `M07` | operating fixed costs |
| Degree of Financial Leverage | `%ΔEPS / %ΔEBIT` | `M07` | financing fixed costs |
| Degree of Total Leverage | `DOL x DFL` | `M07` | sales -> EPS |

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
