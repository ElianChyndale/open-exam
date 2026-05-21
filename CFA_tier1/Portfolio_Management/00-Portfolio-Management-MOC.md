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
| 学习建议 | 先抓组合风险收益和 CAPM，再把 IPS 与 behavioral bias 串成“投资决策框架” |
| 状态 | 学习中 |
| tags | CFA L1, Portfolio Management, MOC |

---

## 最关键：不是找最好的资产，而是找最适合目标与约束的组合

Portfolio Management 的关键词是“组合、约束、匹配”，不是单资产英雄主义。

---

## 科目概览

| 模块 | 内容 | 难度 | 必考点 |
|------|------|------|--------|
| M01 | Portfolio Risk and Return | 计算 | E(Rp), variance, diversification |
| M02 | Utility and CAL | 计算+策略 | risk aversion, capital allocation line |
| M03 | CAPM and Beta | 计算 | SML, beta, required return |
| M04 | Market Efficiency / Active vs Passive | 概念 | active/passive implications |
| M05 | IPS | 策略 | return objective, risk objective, constraints |
| M06 | Behavioral Biases | 概念 | cognitive vs emotional biases |
| M07 | Risk Management | 概念 | governance, budgeting, exposure control |

---

## Portfolio Management 核心知识树

```text
Portfolio Management (M01-M07)
│
├── M01: Portfolio Risk and Return【考试核心】↔ 2026 Outline: Portfolio Risk and Return
│   ├── Single asset -> portfolio translation
│   │   ├── expected return is weight average
│   │   ├── variance adds covariance terms, not just asset variances
│   │   └── correlation controls diversification benefit
│   ├── Efficient opportunity set
│   │   ├── risk-return trade-off; minimum-variance intuition
│   │   └── unsystematic risk can be diversified away
│   └── 注意：portfolio risk can fall while every component remains risky
│
├── M02: Utility and Capital Allocation【考试核心】↔ 2026 Outline: Risk Aversion
│   ├── Investor preference
│   │   ├── utility penalizes variance according to risk aversion
│   │   ├── indifference curve slope reflects risk-return trade-off
│   │   └── higher `A` requires more return for the same variance
│   ├── CAL logic
│   │   ├── combine risk-free asset with risky portfolio
│   │   ├── Sharpe ratio is CAL slope
│   │   └── borrowing/lending choice changes risky-asset weight
│   └── 注意：risk tolerance is preference; risk capacity belongs in IPS reality check
│
├── M03: CAPM, Beta, and Performance Lens【考试核心】↔ 2026 Outline: CAPM
│   ├── Market equilibrium
│   │   ├── systematic risk earns expected compensation
│   │   ├── beta measures market sensitivity
│   │   └── SML prices required return for beta exposure
│   ├── Evaluation link
│   │   ├── alpha compares realized/expected return to CAPM benchmark
│   │   ├── Sharpe uses total risk; Treynor uses beta risk
│   │   └── security above SML looks underpriced in CAPM language
│   └── 注意：high standard deviation and high beta are different diagnoses
│
├── M04: Market Efficiency and Portfolio Construction【考试核心】↔ 2026 Outline: Portfolio Planning
│   ├── Construction spine
│   │   ├── objectives -> constraints -> asset allocation -> implementation -> review
│   │   ├── strategic allocation dominates policy risk budget
│   │   └── active/passive choice follows edge, cost, tax, market efficiency
│   ├── Practical constraints
│   │   ├── benchmark appropriateness, transaction costs, taxes, liquidity
│   │   └── risk budgeting allocates scarce active risk intentionally
│   └── 注意：portfolio design is a process, not a one-shot optimizer screenshot
│
├── M05: Investment Policy Statement【考试核心】↔ 2026 Outline: IPS
│   ├── Objectives
│   │   ├── return need and return desire are not always the same
│   │   ├── risk willingness and risk ability must be reconciled
│   │   └── objective language should be decision usable
│   ├── Constraints
│   │   ├── liquidity, time horizon, taxes, legal/regulatory, unique circumstances
│   │   └── constraints can force portfolio choice away from theoretical optimum
│   └── 注意：IPS is where investor reality vetoes elegant but unsuitable portfolios
│
├── M06: Behavioral Biases【考试核心】↔ 2026 Outline: Behavioral Biases
│   ├── Cognitive errors
│   │   ├── belief perseverance, information-processing, framing, availability
│   │   └── often mitigated by education, process, checklists
│   ├── Emotional biases
│   │   ├── loss aversion, overconfidence, self-control, endowment/status quo
│   │   └── often managed rather than fully corrected
│   └── 注意：bias classification matters because mitigation differs
│
└── M07: Risk Management【考试核心】↔ CFA Institute 2026 Introduction to Risk Management
    ├── Risk system
    │   ├── governance, identification, measurement, modification, monitoring
    │   ├── financial vs non-financial risks; risk interactions
    │   └── risk budget aligns exposure with mission and capital
    ├── Risk action
    │   ├── avoid, accept, transfer, mitigate, monitor
    │   └── reporting should make exposures decision-visible
    └── 注意：good risk management enables chosen risk taking; it is not fear with spreadsheets
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
Portfolio Risk/Return
├── Utility and CAL
│   └── CAPM and Beta
│       └── Active vs Passive Choice
└── IPS
    ├── Behavioral Biases
    └── Risk Management
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

| 指标 | 公式 | 考试说明 |
|------|------|----------|
| Portfolio Return | `Σ wiE(Ri)` | 组合期望收益 |
| Two-asset Variance | `w1²σ1²+w2²σ2²+2w1w2Cov12` | 分散化核心 |
| Correlation | `Cov/(σ1σ2)` | 判断分散化来源 |
| Utility | `E(Rp)-0.5Aσp²` | 风险厌恶框架 |
| CAL | `Rf + [(E(Rr)-Rf)/σr] x σp` | 风险资产与无风险资产组合 |
| CAPM | `Rf + β(E(Rm)-Rf)` | required return |
| Beta | `Cov(Ri,Rm)/Var(Rm)` | systematic risk |
| Sharpe | `(Rp-Rf)/σp` | total risk-adjusted performance |
| Treynor | `(Rp-Rf)/βp` | beta-adjusted performance |
| Jensen Alpha | `Rp-[Rf+βp(Rm-Rf)]` | CAPM 偏离度 |
| M-squared Intuition | `Sharpe difference scaled to market risk` | 看清 total-risk-adjusted comparison |
| Required Excess Return | `β_i x (E(R_m)-R_f)` | CAPM risk premium |

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
