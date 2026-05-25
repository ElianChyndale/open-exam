---
title: 00-Portfolio-Management-MOC
description: CFA Level I Portfolio Management master MOC for risk-return, CAPM, IPS, behavioral biases, risk management, and formulas.
subject: Portfolio Management
topic_area: Portfolio_Management
level: CFA Level I
exam_weight: 8-12%
exam_format: 单选题
difficulty: 组合数学、IPS 策略与行为偏差共同考查
note_type: master_moc
status: 学习中
aliases:
  - Portfolio Management 知识框架
  - 投资组合 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Portfolio_Management
  - formulas
---

# 00-Portfolio-Management-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Portfolio Management - Map of Content |
| description | CFA L1 投资组合管理科目学习导航：风险收益、分散化、CAPM、IPS、行为偏差与风险管理 |
| subject | Portfolio Management |
| 权重 | 8-12% |
| 考试形式 | 单选题，概念+计算+策略判断 |
| 难度特点 | 数量逻辑不难，但 IPS 和 behavioral finance 常因边界不清而失分 |
| 学习建议 | 先抓组合风险收益和 CAPM，再把 IPS 与 behavioral bias 串成"投资决策框架" |
| 状态 | 学习中 |
| tags | CFA L1, Portfolio Management, MOC |

---

## 最关键：不是找最好的资产，而是找最适合目标与约束的组合

Portfolio Management 的关键词是"组合、约束、匹配"，不是单资产英雄主义。

---

## 科目概览

| 模块 | 官方 Module | 内容 | 难度 | 必考点 | 章节文件 |
|------|-------------|------|------|--------|----------|
| M01 | Portfolio Risk and Return Part I | Portfolio Risk and Return | 计算 | E(Rp), variance, diversification | [[M01-Portfolio-Risk-and-Return.md]] |
| M02 | Portfolio Risk and Return Part II | Utility and CAL | 计算+策略 | risk aversion, capital allocation line | [[M02-Utility-and-CAL.md]] |
| M03 | Portfolio Management: An Overview | Portfolio Management Overview | 概念 | pooled investments, PM process, IPS intro | [[M03-Portfolio-Management-Overview.md]] |
| M04 | Portfolio Risk and Return Part II | CAPM and Beta | 计算 | SML, beta, required return | [[M03-CAPM-and-Beta.md]] |
| M05 | Basics of Portfolio Planning and Construction | Market Efficiency / Active vs Passive | 概念 | active/passive implications | [[M04-Market-Efficiency-and-Portfolio-Construction.md]] |
| M06 | Basics of Portfolio Planning and Construction | IPS | 策略 | return objective, risk objective, constraints | [[M05-IPS.md]] |
| M07 | The Behavioral Biases of Individuals | Behavioral Biases | 概念 | cognitive vs emotional biases | [[M06-Behavioral-Biases.md]] |
| M08 | Introduction to Risk Management | Risk Management | 概念 | governance, budgeting, exposure control | [[M07-Risk-Management.md]] |

---

## Portfolio Management 核心知识树 (Core Knowledge Tree)

```text
投资组合管理 (Portfolio Management) (M01-M08)
│
├── M01: 组合风险与收益 (Portfolio Risk and Return)【考试核心】↔ 2026 Outline: Portfolio Risk and Return
│   ├── 从单资产到投资组合的转换 (Single asset -> portfolio translation)
│   │   ├── 核心公式 (English)
│   │   │   ├── 组合期望收益: `E(Rp) = Σ wiE(Ri)`
│   │   │   ├── 两资产方差: `σp² = w1²σ1²+w2²σ2²+2w1w2Cov12`
│   │   │   └── 相关系数: `Corr(R1,R2) = Cov(R1,R2)/(σ1σ2)`
│   │   ├── 期望收益是单项收益的加权平均 (expected return is weight average)
│   │   ├── 方差包含协方差项而非仅资产方差 (variance adds covariance terms, not just asset variances)
│   │   └── 相关系数决定分散化收益 (correlation controls diversification benefit)
│   ├── 有效机会集 (Efficient opportunity set)
│   │   ├── 风险-收益权衡与最小方差直觉 (risk-return trade-off; minimum-variance intuition)
│   │   └── 非系统性风险可通过分散化消除 (unsystematic risk can be diversified away)
│   └── 注意：组合风险可以在每个成分资产仍有风险时下降 (portfolio risk can fall while every component remains risky)
│
├── M02: 效用与资本配置 (Utility and Capital Allocation)【考试核心】↔ 2026 Outline: Risk Aversion
│   ├── 投资者偏好 (Investor preference)
│   │   ├── 核心公式 (English)
│   │   │   ├── 效用函数: `U = E(Rp)-0.5Aσp²`
│   │   │   └── 资本配置线: `E(R_C) = R_f + [(E(R_P)-R_f)/σ_P] x σ_C`
│   │   ├── 效用按风险厌恶程度惩罚方差 (utility penalizes variance according to risk aversion)
│   │   ├── 无差异曲线斜率反映风险-收益权衡 (indifference curve slope reflects risk-return trade-off)
│   │   └── 更高的 `A` 需要更高收益补偿相同方差 (higher `A` requires more return for the same variance)
│   ├── 资本配置线逻辑 (CAL logic)
│   │   ├── 无风险资产与风险组合的配比 (combine risk-free asset with risky portfolio)
│   │   ├── 夏普比率是CAL的斜率 (Sharpe ratio is CAL slope)
│   │   └── 借入/贷出选择影响风险资产权重 (borrowing/lending choice changes risky-asset weight)
│   └── 注意：风险容忍度是偏好；风险承受能力属于IPS现实检验 (risk tolerance is preference; risk capacity belongs in IPS reality check)
│
├── M03: 投资组合管理概述 (Portfolio Management: An Overview)【新模块】↔ 2026 Outline: Portfolio Management: An Overview
│   ├── 组合管理流程 (Portfolio management process)
│   │   ├── 三阶段循环：规划 → 执行 → 反馈 (planning -> execution -> feedback)
│   │   ├── 规划阶段产出 IPS 和战略资产配置 (IPS + SAA from planning)
│   │   └── 反馈阶段包含监控、再平衡和 IPS 调整 (monitoring, rebalancing, IPS update)
│   ├── 集合投资工具 (Pooled investment vehicles)
│   │   ├── 共同基金 (Mutual funds)：按 NAV 定价，开放/封闭型
│   │   ├── ETF：交易所交易，AP套利维持价格贴近NAV
│   │   ├── SMA：直接持有证券，个性化管理
│   │   ├── 对冲基金 (Hedge funds)：多策略，锁定期，"2 and 20"费用
│   │   └── 私募股权 (Private equity)：长期锁定，J-curve效应
│   ├── 投资者类型 (Types of investors)
│   │   ├── 个人投资者：行为偏差影响大，生命周期驱动
│   │   └── 机构投资者：受托责任，监管严格，长期投资
│   └── IPS 简介：组合管理流程中的指导性决策框架
│
├── M04: CAPM、Beta与绩效视角 (CAPM, Beta, and Performance Lens)【考试核心】↔ 2026 Outline: CAPM
│   ├── 市场均衡 (Market equilibrium)
│   │   ├── 核心公式 (English)
│   │   │   ├── CAPM: `E(R_i) = R_f + β_i[E(R_M)-R_f]`
│   │   │   ├── Beta系数: `β_i = Cov(R_i,R_M)/Var(R_M)`
│   │   │   ├── 夏普比率: `Sharpe = (Rp-Rf)/σp`
│   │   │   ├── 特雷诺比率: `Treynor = (Rp-Rf)/βp`
│   │   │   └── 詹森阿尔法: `α_p = R_p-[R_f+β_p(E(R_M)-R_f)]`
│   │   ├── 系统性风险获得预期补偿 (systematic risk earns expected compensation) (Beta风险有补偿)
│   │   ├── Beta衡量市场敏感度 (beta measures market sensitivity)
│   │   └── SML对Beta暴露定价必要回报 (SML prices required return for beta exposure)
│   ├── 绩效评估关联 (Evaluation link)
│   │   ├── Alpha比较实际/预期收益与CAPM基准 (alpha compares realized/expected return to CAPM benchmark) (超额收益测经理)
│   │   ├── Sharpe使用总风险，Treynor使用Beta风险 (Sharpe uses total risk; Treynor uses beta risk) (风险口径不同)
│   │   └── SML上方的证券在CAPM框架中看似被低估 (security above SML looks underpriced in CAPM language)
│   └── 注意：高标准差和高Beta是不同的诊断 (high standard deviation and high beta are different diagnoses)
│
├── M05: 市场有效性与组合构建 (Market Efficiency and Portfolio Construction)【考试核心】↔ 2026 Outline: Portfolio Planning
│   ├── 组合构建主线 (Construction spine)
│   │   ├── 目标→约束→资产配置→执行→回顾 (objectives -> constraints -> asset allocation -> implementation -> review) (IPS五步法)
│   │   ├── 战略性配置主导政策风险预算 (strategic allocation dominates policy risk budget) (长期收益主驱动)
│   │   └── 主动/被动选择取决于优势、成本、税收、市场有效性 (active/passive choice follows edge, cost, tax, market efficiency)
│   ├── 实际约束 (Practical constraints)
│   │   ├── 基准适配性、交易成本、税收、流动性 (benchmark appropriateness, transaction costs, taxes, liquidity)
│   │   └── 风险预算有意分配稀缺的主动风险 (risk budgeting allocates scarce active risk intentionally)
│   └── 注意：组合设计是一个过程，而非一次优化器截图 (portfolio design is a process, not a one-shot optimizer screenshot)
│
├── M06: 投资政策声明 (Investment Policy Statement)【考试核心】↔ 2026 Outline: IPS
│   ├── 目标 (Objectives)
│   │   ├── 收益需求与收益期望并不总是一致 (return need and return desire are not always the same) (需求≠期望)
│   │   ├── 风险意愿与风险能力必须协调 (risk willingness and risk ability must be reconciled) (意愿≠能力)
│   │   └── 目标表述应具有决策指导性 (objective language should be decision usable)
│   ├── 约束 (Constraints)
│   │   ├── 流动性、时间跨度、税收、法律/监管、特殊情形 (liquidity, time horizon, taxes, legal/regulatory, unique circumstances) (L-T-T-L-U五约束)
│   │   └── 约束可能迫使组合偏离理论最优 (constraints can force portfolio choice away from theoretical optimum)
│   └── 注意：IPS是投资者现实否决优雅但不适配合约的地方 (IPS is where investor reality vetoes elegant but unsuitable portfolios)
│
├── M07: 行为偏差 (Behavioral Biases)【考试核心】↔ 2026 Outline: Behavioral Biases
│   ├── 认知错误 (Cognitive errors)
│   │   ├── 信念固着、信息处理、框架效应、可得性 (belief perseverance, information-processing, framing, availability) (认知错误四类)
│   │   └── 常可通过教育、流程、检查表缓解 (often mitigated by education, process, checklists)
│   ├── 情绪偏差 (Emotional biases)
│   │   ├── 损失厌恶、过度自信、自我控制、禀赋/现状偏差 (loss aversion, overconfidence, self-control, endowment/status quo) (情绪偏差四类)
│   │   └── 通常管理而非完全纠正 (often managed rather than fully corrected)
│   └── 注意：偏差分类之所以重要是因为纠正方式不同 (bias classification matters because mitigation differs)
│
└── M08: 风险管理 (Risk Management)【考试核心】↔ CFA Institute 2026 Introduction to Risk Management
    ├── 风险体系 (Risk system)
    │   ├── 治理、识别、衡量、改变化、监控 (governance, identification, measurement, modification, monitoring)
    │   ├── 金融风险与非金融风险；风险互动 (financial vs non-financial risks; risk interactions)
    │   └── 风险预算使风险暴露与使命和资本对齐 (risk budget aligns exposure with mission and capital)
    ├── 风险行动 (Risk action)
    │   ├── 规避、接受、转移、缓释、监控 (avoid, accept, transfer, mitigate, monitor)
    │   └── 报告应使风险暴露决策可视化 (reporting should make exposures decision-visible)
    └── 注意：好的风险管理使选定的风险承担成为可能，而非用电子表格恐惧 (good risk management enables chosen risk taking; it is not fear with spreadsheets)
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报 | 相关性 | 费用/代价 |
|--------|------|------|------|--------|-----------|
| Systematic vs Unsystematic Risk | 市场共同风险 vs 个体特有风险 | systematic 不能靠分散化消掉 | 承担 systematic 才通常有风险补偿 | 都影响 total risk | unsystematic 可用分散化降低 |
| Active vs Passive | 主动偏离基准 vs 跟踪市场 | active 有 tracking risk 与 underperformance risk | active 追求 alpha；passive 获取 beta | 与 market efficiency 直接相关 | active fees 通常更高 |
| Risk Objective vs Return Objective | 能承受多少波动/损失 vs 想达到多少收益 | 混写会导致 IPS 错 | 两者必须相互一致 | 与 constraints 强相关 | 目标过高可能导致风险失配 |
| Cognitive Bias vs Emotional Bias | 信息处理错误 vs 情绪驱动错误 | 后者更难纠正 | 都可能破坏纪律 | 与 client behavior 相关 | 代价是偏离长期最优配置 |
| Total Risk vs Beta Risk | 总波动 vs 市场敏感度 | 混淆会错用 Sharpe/Treynor/CAPM | 不同绩效指标针对不同风险 | beta 是 total risk 的一部分 | 风险衡量错会导致配置错误 |
| Risk Tolerance vs Risk Capacity | 心理愿意承受 vs 财务能够承受 | 只听偏好会做出不适配组合 | IPS 要调和两者 | 都影响 risk objective | capacity 较低时要收紧配置 |
| Strategic vs Tactical Allocation | 长期政策配置 vs 短期偏离 | tactical 可能超预算承担主动风险 | strategic 决定主暴露 | 都连到 benchmark | turnover、tax、tracking cost |

---

## 跨模块关联

```text
投资组合管理概述 (Portfolio Management Overview) [M03]
├── 投资组合风险与收益 (Portfolio Risk/Return) [M01]
│   └── 效用与资本配置线 (Utility and CAL) [M02]
│       └── CAPM与Beta (CAPM and Beta) [M04]
│           └── 主动与被动选择 (Active vs Passive Choice) [M05]
└── 投资政策说明书 (IPS) [M06]
    ├── 行为偏差 (Behavioral Biases) [M07]
    └── 风险管理 (Risk Management) [M08]
```

---

## 通用分析框架

### 框架1：组合题 SOP

1. 先算 expected return
2. 再看 correlation/covariance
3. 再判断 diversification effect
4. 最后回到 investor objective

### 框架2：IPS 题 SOP

1. 先写 return objective
2. 再写 risk objective
3. 再按 `L-T-T-L-U` 写 constraints
   - Liquidity
   - Time horizon
   - Taxes
   - Legal/regulatory
   - Unique circumstances

### 框架3：行为偏差题 SOP

1. 判断是认知偏差还是情绪偏差
2. 找偏差如何影响 asset allocation / trading / risk tolerance
3. 再给出纠偏方式

---

## 核心公式速查

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Portfolio Return | `Σ wiE(Ri)` | `M01` | 组合期望收益 |
| Two-asset Variance | `w1²σ1²+w2²σ2²+2w1w2Cov12` | `M01` | 分散化核心 |
| Correlation | `Corr(R_1,R_2) = Cov(R_1,R_2)/(σ_1σ_2)` | `M01` | 判断分散化来源 |
| Utility | `E(Rp)-0.5Aσp²` | `M02` | 风险厌恶框架 |
| CAL | `E(R_C) = R_f + [(E(R_P)-R_f)/σ_P] x σ_C` | `M02` | 风险资产与无风险资产组合 |
| Pooled Vehicle NAV | `(资产市值 - 负债) / 流通份额` | `M03` | 基金定价基础 |
| CAPM | `E(R_i) = R_f + β_i[E(R_M)-R_f]` | `M04` | required return |
| Beta | `β_i = Cov(R_i,R_M)/Var(R_M)` | `M04` | systematic risk |
| Sharpe | `(Rp-Rf)/σp` | `M04` | total risk-adjusted performance |
| Treynor | `(Rp-Rf)/βp` | `M04` | beta-adjusted performance |
| Jensen Alpha | `α_p = R_p-[R_f+β_p(E(R_M)-R_f)]` | `M04` | CAPM 偏离度 |
| M-squared Intuition | `Sharpe difference scaled to market risk` | `M04` | 看清 total-risk-adjusted comparison |
| Required Excess Return | `β_i x (E(R_m)-R_f)` | `M04` | CAPM risk premium |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| 多买几个资产就完成分散化 | 关键是低相关，而不是数量本身 |
| beta 高说明总风险一定高 | beta 只反映 systematic risk |
| utility 只是抽象概念 | 它决定风险资产与无风险资产配置 |
| active 管理 = 更专业 | active 只是更主动承担 tracking/selection risk |
| passive 管理 = 不用判断市场 | 仍要判断目标、基准与成本 |
| IPS 先写约束再写目标也无所谓 | 考试常严格区分 objective 与 constraints |
| 高 return objective 必然合理 | 还要看 risk capacity / risk tolerance 是否支持 |
| behavioral bias 是心理学边角料 | 它直接影响配置和交易错误 |
| risk management 的目标是把风险压到最低 | 目标是使风险与回报目标匹配 |
| Sharpe 和 Treynor 可以随便替换 | 一个基于 total risk，一个基于 beta risk |
| willingness 高就可设高风险组合 | 还要看 capacity 是否撑得住 |
| active risk 越大越有机会 | 没有 edge 和预算约束时只是更大偏离 |
