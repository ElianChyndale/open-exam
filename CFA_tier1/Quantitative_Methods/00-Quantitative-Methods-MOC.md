---
title: 00-Quantitative-Methods-MOC
description: CFA Level I Quantitative Methods master MOC with module map, detailed knowledge tree, formulas, workflows, and exam traps.
subject: Quantitative Methods
topic_area: Quantitative_Methods
level: CFA Level I
exam_weight: 6-9%
exam_format: 单选题
difficulty: 公式基础与统计推断并重
note_type: master_moc
status: 学习中
aliases:
  - Quantitative Methods 知识框架
  - 数量方法 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Quantitative_Methods
  - formulas
---

# 00-Quantitative-Methods-MOC

## 笔记属性

| 属性          | 内容                                                |
| ----------- | ------------------------------------------------- |
| title       | Quantitative Methods - Map of Content             |
| description | CFA L1 数量方法科目学习导航：收益率、TVM、统计、概率、抽样、假设检验、回归、机器学习基础 |
| subject     | Quantitative Methods                              |
| 权重          | 6-9%                                              |
| 考试形式        | 单选题，概念+计算混合                                       |
| 难度特点        | 前半段公式基础，后半段统计推断与回归更容易混                            |
| 学习建议        | 先搭“现金流-统计-检验-回归”总骨架，再用公式和题型标签反复刷                  |
| 状态          | 学习中                                               |
| tags        | CFA L1, Quantitative Methods, MOC                 |

---

## 最关键：先统一口径，再折现，再统计，再检验

数量的本质不是难算，而是把投资问题翻译成统一的计算和判断语言。

---

## 科目概览

| 模块  | 内容                        | 难度    | 必考点                                         |
| --- | ------------------------- | ----- | ------------------------------------------- |
| M01 | Rates and Returns         | 概念+计算 | HPR, MWRR, TWRR, annualized return          |
| M02 | Time Value of Money       | 计算    | PV/FV, annuity, perpetuity, implied return  |
| M03 | Statistical Measures      | 概念+计算 | mean, variance, skewness, kurtosis          |
| M04 | Probability Trees & Bayes | 概念    | conditional probability, Bayes              |
| M05 | Portfolio Mathematics     | 计算    | covariance, correlation, portfolio variance |
| M06 | Simulation                | 概念    | Monte Carlo, bootstrap                      |
| M07 | Sampling & Estimation     | 计算    | CLT, standard error, confidence interval    |
| M08 | Hypothesis Testing        | 计算+策略 | H0/H1, Type I/II, p-value                   |
| M09 | Correlation & Regression  | 计算+策略 | t-test, F-test, R^2, SEE                    |
| M10 | Big Data / ML Intro       | 概念    | supervised vs unsupervised, overfitting     |

---

## Quantitative Methods 核心知识树

```text
Quantitative Methods (M01-M10)
│
├── M01: Rates and Returns
│   ├── 1.1 Interest rate 的三种解释【考试核心】↔ Topic Outline P0
│   │   ├── required rate of return: 投资者要求回报
│   │   ├── discount rate: 将未来现金流折现回今天
│   │   └── opportunity cost: 放弃下一优选择的代价
│   ├── 1.2 Interest rate decomposition【考试核心】
│   │   ├── real risk-free rate
│   │   ├── expected inflation premium
│   │   ├── default / liquidity / maturity / other risk premiums
│   │   └── 注意：rate 高不只因 inflation，高风险补偿也会抬升 rate【考试陷阱】
│   ├── 1.3 Return measurement ladder【考试核心】
│   │   ├── HPR = price change + income over beginning value
│   │   ├── 核心公式
│   │   │   ├── `HPR = (P1 - P0 + D1)/P0`
│   │   │   ├── `Arithmetic mean = ΣRi / n`
│   │   │   └── `Geometric mean = [(1+R1)...(1+Rn)]^(1/n)-1`
│   │   ├── arithmetic mean: 单期 expected return 口径
│   │   ├── geometric mean: 多期复合增长口径
│   │   └── harmonic mean: price multiple / averaging rate 场景易见
│   ├── 1.4 MWRR vs TWRR【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `MWRR: Σ CFt/(1+r)^t = 0`
│   │   │   └── `TWRR: [(1+HP1)...(1+HPn)] - 1`
│   │   ├── MWRR = portfolio cash flow IRR
│   │   ├── TWRR = subperiod returns linked after external cash-flow breaks
│   │   └── 注意：客户增减资金造成的 return distortion 归 MWRR，不归经理【考试陷阱】
│   └── 1.5 Annualization and continuous compounding【考试核心】
│       ├── 核心公式
│       │   ├── `Annualized return = (1+R_period)^c - 1`
│       │   ├── `r_cc = ln(1 + HPR)`
│       │   ├── `FV = PVe^(rt)`
│       │   └── `PV = FVe^(-rt)`
│       ├── effective annual return vs stated period return
│       ├── r_cc = ln(1 + HPR)
│       └── continuously compounded returns 可加，普通 returns 不可直接相加
│   ├── 1.6 Gross Return vs Net Return【考试核心】← 高频错因
│   │   ├── Gross Return = (P1 + D1)/P0 = 1 + HPR
│   │   ├── Trading expenses 已反映在 gross return 中，不重复扣除
│   │   ├── Net Return = Gross Return - Management/Admin fees
│   │   └── 注意：gross return 是税前、非风险调整口径【考试陷阱】
│   ├── 1.7 Leveraged and After-Tax Return【考试核心】← 高频错因
│   │   ├── Leveraged Return = R_p + (B/E)(R_p - r_D)
│   │   │   └── B = 借款额, E = 自有本金, r_D = 借款利率
│   │   ├── After-Tax Return = Pre-tax Return × (1 - t)
│   │   │   └── t = 税率
│   │   └── 注意：计算顺序不可逆：Gross → Net → Leverage → Tax【考试陷阱】
│
├── M02: Time Value of Money
│   ├── 2.1 Cash-flow map【考试核心】↔ Topic Outline P0
│   │   ├── 核心公式
│   │   │   ├── `FV = PV(1+r)^n`
│   │   │   ├── `PV = FV/(1+r)^n`
│   │   │   ├── `Ordinary annuity PV = A[1-1/(1+r)^n]/r`
│   │   │   └── `Perpetuity PV = A/r`
│   │   ├── single sum: one PV / one FV
│   │   ├── level annuity: equal finite cash flows
│   │   ├── perpetuity: equal cash flows forever
│   │   └── growing stream: growth and discount rate both matter
│   ├── 2.2 Instrument PV applications【考试核心】
│   │   ├── fixed-income price = coupons + principal PV
│   │   ├── equity intrinsic value = dividends / cash-flow expectations PV
│   │   └── 注意：先识别 cash-flow timing，再选 formula【考试陷阱】
│   ├── 2.3 Implied quantities【考试核心】
│   │   ├── 核心公式
│   │   │   └── `r = D1/P0 + g`
│   │   ├── bond implied return from PV and promised CF
│   │   ├── equity required return from price, dividend, growth
│   │   └── equity implied growth from price and required return
│   └── 2.4 Cash-flow additivity【考试核心】
│       ├── portfolio PV = sum of component PVs
│       ├── no-arbitrage logic
│       ├── forward interest / forward FX / option value intuition
│       └── 注意：同一 cash flow 不应因拆分方式不同而变价
│
├── M03: Statistical Measures
│   ├── 3.1 Central tendency and location【考试核心】↔ Topic Outline P1
│   │   ├── arithmetic / geometric / harmonic mean
│   │   ├── weighted mean
│   │   ├── median, mode, quantiles, percentile location
│   │   └── 注意：outlier 对 mean 影响通常大于 median【考试陷阱】
│   ├── 3.2 Dispersion【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `Population variance = Σ(x-μ)^2/n`
│   │   │   ├── `Sample variance = Σ(x-x̄)^2/(n-1)`
│   │   │   └── `Standard deviation = sqrt(Variance)`
│   │   ├── range / mean absolute deviation
│   │   ├── variance / standard deviation
│   │   ├── downside deviation
│   │   └── coefficient of variation for relative dispersion
│   ├── 3.3 Distribution shape【考试核心】
│   │   ├── skewness: asymmetry
│   │   ├── kurtosis: tail thickness
│   │   └── 注意：left-skew / right-skew 判断要看长尾方向【考试陷阱】
│   └── 3.4 Correlation intuition【考试核心】
│       ├── sign = direction
│       ├── magnitude = linear association strength
│       └── correlation ≠ causation
│
├── M04: Probability Concepts
│   ├── 4.1 Expected value / variance / standard deviation【考试核心】↔ Topic Outline P1
│   │   ├── 核心公式
│   │   │   ├── `E(X) = Σ p(xi)xi`
│   │   │   └── `Var(X) = E(X^2)-[E(X)]^2`
│   │   ├── discrete outcome probabilities
│   │   ├── total risk from probability-weighted dispersion
│   │   └── expected value 是概率加权中心，不是必然结果
│   ├── 4.2 Probability tree【考试核心】
│   │   ├── branch probability
│   │   ├── terminal payoff
│   │   └── conditional expectation at decision node
│   └── 4.3 Bayes update【考试核心】
│       ├── 核心公式
│       │   ├── `P(A|B) = P(A∩B)/P(B)`
│       │   └── `P(Bj|A)=[P(A|Bj)P(Bj)]/Σ[P(A|Bi)P(Bi)]`
│       ├── prior probability
│       ├── conditional likelihood
│       ├── posterior probability
│       └── 注意：更新后概率要回到完整分母，不只看 numerator【考试陷阱】
│
├── M05: Portfolio Mathematics
│   ├── 5.1 Return moments【考试核心】↔ Topic Outline P1
│   │   ├── 核心公式
│   │   │   ├── `E(Rp) = Σ wiE(Ri)`
│   │   │   └── `σp² = w1²σ1²+w2²σ2²+2w1w2Cov12`
│   │   ├── portfolio expected return
│   │   ├── variance and standard deviation
│   │   └── weights sum to one for fully invested portfolio
│   ├── 5.2 Joint probability function【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `Cov12 = Σ p(R1-E(R1))(R2-E(R2))`
│   │   │   └── `Corr12 = Cov12/(σ1σ2)`
│   │   ├── scenario pair returns
│   │   ├── covariance from joint states
│   │   └── correlation standardizes covariance
│   ├── 5.3 Diversification mechanics【考试核心】
│   │   ├── covariance term drives two-asset risk
│   │   ├── lower correlation lowers portfolio variance
│   │   └── 注意：低 correlation 不等于负 expected return
│   └── 5.4 Shortfall risk【考试核心】
│       ├── 核心公式
│       │   └── `Roy safety-first = (E(Rp)-RL)/σp`
│       ├── threshold return RL
│       ├── Roy safety-first ratio
│       └── choose highest safety-first ratio when returns assumed normal
│
├── M06: Simulation Methods
│   ├── 6.1 Distribution link【考试核心】↔ Topic Outline P1
│   │   ├── continuously compounded returns may be modeled normal
│   │   └── prices derived from those returns are lognormal and nonnegative
│   ├── 6.2 Monte Carlo【考试核心】
│   │   ├── specify input distribution
│   │   ├── draw random scenarios
│   │   └── summarize output distribution
│   └── 6.3 Bootstrap resampling【考试核心】
│       ├── resample observed data with replacement
│       └── 注意：bootstrap inherits observed-sample limitations【考试陷阱】
│
├── M07: Sampling and Estimation
│   ├── 7.1 Sampling methods【考试核心】↔ Topic Outline P1
│   │   ├── simple random / stratified / cluster
│   │   ├── convenience / judgmental
│   │   └── sampling method changes sampling error and bias exposure
│   ├── 7.2 CLT and standard error【考试核心】
│   │   ├── 核心公式
│   │   │   └── `SE = σ/√n` 或 `s/√n`
│   │   ├── sample mean distribution tightens as n grows
│   │   ├── SE scales by 1/sqrt(n)
│   │   └── 注意：大样本降低 standard error，不消灭 bad sampling design【考试陷阱】
│   └── 7.3 Resampling estimators【考试核心】
│       ├── bootstrap
│       └── jackknife
│
├── M08: Hypothesis Testing
│   ├── 8.1 Test components【考试核心】↔ Topic Outline P2
│   │   ├── 核心公式
│   │   │   ├── `CI: x̄ ± z_(α/2)σ/√n`
│   │   │   ├── `CI: x̄ ± t_(α/2,n-1)s/√n`
│   │   │   └── `z/t = (x̄-μ0)/(σ/√n)` or `(x̄-μ0)/(s/√n)`
│   │   ├── null / alternative
│   │   ├── significance level alpha
│   │   ├── test statistic and rejection region
│   │   └── p-value as evidence against null
│   ├── 8.2 Error architecture【考试核心】
│   │   ├── Type I error = reject true H0
│   │   ├── Type II error = fail to reject false H0
│   │   └── power = 1 - probability(Type II error)
│   └── 8.3 Parametric vs nonparametric【考试核心】
│       ├── parametric relies on distributional assumptions
│       └── nonparametric helps when assumptions / scale conditions fail
│
├── M09: Correlation and Regression
│   ├── 9.1 Independence tests【考试核心】↔ Topic Outline P2
│   │   ├── population correlation equals zero test
│   │   ├── parametric vs nonparametric correlation test
│   │   └── contingency table independence test
│   ├── 9.2 Simple linear regression model【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `Yi = b0 + b1Xi + ei`
│   │   │   ├── `b1 = Cov(X,Y)/Var(X)`
│   │   │   └── `b0 = ȳ - b1x̄`
│   │   ├── dependent variable Y
│   │   ├── independent variable X
│   │   ├── intercept, slope, residual
│   │   └── least squares minimizes SSE
│   ├── 9.3 Regression diagnostics【考试核心】
│   │   ├── linearity / homoskedasticity / independence / normal errors
│   │   └── residual plot hints assumption violations
│   ├── 9.4 Fit and inference【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `R² = SSR/SST`
│   │   │   ├── `SEE = sqrt(SSE/(n-2))`
│   │   │   ├── `t = (b1-β1,0)/SE(b1)`
│   │   │   └── `F = MSR/MSE`
│   │   ├── R2, SEE, coefficient t-test, ANOVA F-test
│   │   ├── predicted value and prediction interval
│   │   └── different functional forms
│   └── 注意：prediction interval 比 point estimate 更诚实地表达 uncertainty【考试陷阱】
│
└── M10: Big Data and ML
    ├── 10.1 Fintech data context【考试核心】↔ Topic Outline P2
    │   ├── data gathering
    │   └── data analysis relevance for investment process
    ├── 10.2 Big Data / AI / ML definitions【考试核心】
    └── 10.3 Investment applications【考试核心】
        ├── research signal extraction
        ├── risk / operations / client analytics
        └── 注意：model sophistication 不替代 validation and governance【考试陷阱】
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报/用途 | 相关性/联系 | 费用/代价 |
|--------|------|------|-----------|-------------|-----------|
| MWRR vs TWRR | 投资者现金流敏感 vs 经理表现口径 | MWRR 受现金流时点扰动 | MWRR 评估 investor experience；TWRR 评估 manager skill | 都是收益衡量方法 | 代价是口径混淆导致误判 |
| Arithmetic Mean vs Geometric Mean | 单期平均 vs 多期复合 | arithmetic 高估长期回报 | geometric 更适合长期财富增长 | 都基于同一组 returns | 计算复杂度略高 |
| Sample Variance vs Population Variance | 用样本估总体 vs 已知总体 | 忘记 n-1 会低估波动 | sample 更常用 | 都衡量 dispersion | 无直接费用 |
| z-test vs t-test | 已知总体方差 vs 未知总体方差 | 用错分布会误判拒绝域 | 都用于 mean 检验 | t 在 n 小时更关键 | 代价是临界值不同 |
| Correlation vs Regression | 关系强度 vs 解释/预测模型 | 把相关当因果 | regression 可预测 / test slope | regression 常依赖 correlation 直觉 | 模型设定错误成本高 |

---

## 跨模块关联

```text
Returns
└── TVM
    ├── Statistical Measures
    │   └── Probability
    │       └── Portfolio Mathematics
    └── Sampling and Estimation
        └── Hypothesis Testing
            └── Regression
                └── Big Data / ML
```

---

## 通用分析框架

### 框架1：收益率题决策树

1. 先问：有没有中途现金流？
2. 有现金流且要评估 investor experience：用 `MWRR`
3. 有现金流但要评估 manager performance：用 `TWRR`
4. 多期复合回报：优先 `geometric mean`

### 框架2：统计推断题决策树

1. 问题是在估计还是检验？
2. 如果是估计：先找 `point estimate` 还是 `confidence interval`
3. 如果是检验：先写 `H0 / H1`
4. 再判断 `z` 还是 `t`
5. 最后用 `p-value` 或 `critical value` 做结论

### 框架3：回归题决策树

1. 先看 `slope` 是否显著
2. 再看 `overall model` 是否显著
3. 再看 `R²` 是否够解释力
4. 最后检查 residual/经济含义，避免把统计显著误当投资显著

---

## 核心公式速查

### M01 Returns

| 指标                             | 公式                                   | 知识树节点 | 考试说明                             |
| ------------------------------ | ------------------------------------ | ----- | -------------------------------- |
| HPR                            | `(P1 - P0 + D1)/P0`                  | `1.3` | 最基础收益率公式                         |
| Gross Return                   | `(P1 + D1)/P0 = 1 + HPR`             | `1.6` | 连乘收益时常改用 gross return            |
| Arithmetic Mean                | `ΣRi / n`                            | `1.3` | 单期 expected return 常用            |
| Geometric Mean                 | `[(1+R1)(1+R2)...(1+Rn)]^(1/n)-1`    | `1.3` | 多期复合财富增长口径                       |
| Annualized Return              | `(1+R_period)^c - 1`                 | `1.5` | `c` 是一年内期数                       |
| Continuously Compounded Return | `ln(1+HPR)`                          | `1.5` | 与普通 HPR 可互转                      |
| Convert CC Return              | `e^(r_cc)-1`                         | `1.5` | 连续复利回到 holding period return     |
| MWRR                           | `Σ CFt/(1+r)^t = 0`                  | `1.4` | 投资者现金流敏感，实质是 IRR                 |
| TWRR                           | `[(1+HP1)(1+HP2)...(1+HPn)]^1/2 - 1` | `1.4` | 经理业绩口径                           |
| Net Return                     | `Gross Return - Mgmt/Admin Fees`     | `1.6` | trading expenses 已在 gross 中，不重复减 |
| Leveraged Return               | `R_p + (B/E)(R_p - r_D)`             | `1.7` | B=借款, E=自有本金, r_D=借款利率           |
| After-Tax Return               | `R_pre × (1 - t)`                    | `1.7` | t=税率，先算杠杆后税前回报再扣税                |

### M02 Time Value of Money

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| FV | `PV(1+r)^n` | `2.1` | TVM 核心 |
| PV | `FV/(1+r)^n` | `2.1` | TVM 核心 |
| FV with Continuous Compounding | `PVe^(rt)` | `2.1` | 当题目给的是连续复利利率时，用 `e^(rt)` 而不是 `(1+r)^n` |
| PV with Continuous Discounting | `FVe^(-rt)` | `2.1` | 连续贴现是连续复利的逆运算 |
| Ordinary Annuity PV | `A[1-1/(1+r)^n]/r` | `2.1` | 固定期末现金流 |
| Ordinary Annuity FV | `A[(1+r)^n-1]/r` | `2.1` | 累积型现金流 |
| Annuity Due PV | `PV_ordinary(1+r)` | `2.1` | 期初支付多滚一期 |
| Annuity Due FV | `FV_ordinary(1+r)` | `2.1` | 易与 ordinary annuity 混 |
| Perpetuity PV | `A/r` | `2.1` | 高频快算 |
| Growing Perpetuity PV | `A1/(r-g)` | `2.1` | 必须满足 `r>g` |
| Growing Annuity PV | `[A1/(r-g)][1-((1+g)^n/(1+r)^n)]` | `2.1` | 增长有限期现金流 |
| Gordon Link | `r=D1/P0+g` | `2.3` | Quant 与 Equity 交叉 |

### M03-M05 Statistics, Probability, Portfolio Math

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Population Variance | `Σ(x-μ)^2/n` | `3.2` | 总体已知口径 |
| Sample Variance | `Σ(x-x̄)²/(n-1)` | `3.2` | 注意 n-1 |
| Standard Deviation | `sqrt(Variance)` | `3.2` | 风险与离散度基本量 |
| Coefficient of Variation | `s/mean` | `3.2` | 相对离散度 |
| Expected Value | `Σ p(xi)xi` | `4.1` | 概率题入口 |
| Variance Identity | `E(X^2)-[E(X)]^2` | `4.1` | 两种方差算法要会互认 |
| Conditional Probability | `P(A∩B)/P(B)` | `4.3` | Bayes 前置 |
| Total Probability | `Σ P(A|Bi)P(Bi)` | `4.3` | Bayes 分母 |
| Bayes Formula | `P(Bj|A)=[P(A|Bj)P(Bj)]/Σ[P(A|Bi)P(Bi)]` | `4.3` | 用新信息更新先验 |
| Portfolio Return | `Σ wiE(Ri)` | `5.1` | 权重求和 |
| Covariance | `Σ p(R1-E(R1))(R2-E(R2))` | `5.2` | 组合方差前置 |
| Correlation | `Cov12/(σ1σ2)` | `5.2` | 规范到 `-1` 至 `1` |
| Portfolio Variance | `w1²σ1²+w2²σ2²+2w1w2Cov12` | `5.1` | 常考两资产组合 |
| Roy Safety-First | `(E(Rp)-RL)/σp` | `5.4` | threshold return 框架 |

### M07-M08 Sampling and Testing

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Standard Error | `σ/√n` or `s/√n` | `7.2` | 抽样与估计核心 |
| CI, Sigma Known | `x̄ ± z_(α/2)σ/√n` | `8.1` | 总体方差已知 |
| CI, Sigma Unknown | `x̄ ± t_(α/2,n-1)s/√n` | `8.1` | 常见考试场景 |
| Required Sample Size | `(zσ/E)^2` | `7.2` | `E` 是 margin of error |
| z-stat / t-stat | `(x̄-μ0)/(σ/√n)` or `(x̄-μ0)/(s/√n)` | `8.1` | 先分清方差是否已知 |

### M09 Correlation and Regression

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Correlation test t | `r√[(n-2)/(1-r²)]` | `9.1` | 独立性检验 |
| Regression Equation | `Yi=b0+b1Xi+ei` | `9.2` | 简单线性回归骨架 |
| Regression slope | `Cov(X,Y)/Var(X)` | `9.2` | 回归核心 |
| Regression Intercept | `ȳ-b1x̄` | `9.2` | 斜率确定后回代 |
| R-squared | `SSR/SST` | `9.4` | 拟合度，不是因果性 |
| SEE | `sqrt(SSE/(n-2))` | `9.4` | 回归残差尺度 |
| Slope t-stat | `(b1-β1,0)/SE(b1)` | `9.4` | 检验 slope |
| F-stat | `MSR/MSE` | `9.4` | 检验整体模型 |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| arithmetic mean 就是长期平均收益 | 长期复合更看 geometric mean |
| MWRR 和 TWRR 本质一样 | 一个看现金流敏感，一个看经理表现 |
| annuity due 和 ordinary annuity 一样 | annuity due 多乘 `(1+r)` |
| sample variance 分母也是 n | sample variance 用 `n-1` |
| fat tails 就是 skewness 高 | fat tails 对应 kurtosis 高 |
| Bayes 只是公式题 | 它本质是“用新信息更新旧概率” |
| p-value 小表示 H0 大概率为假 | p-value 是“在 H0 成立下出现样本的极端程度” |
| fail to reject H0 等于接受 H0 | 只是证据不足以拒绝 |
| correlation 高说明因果强 | 相关不等于因果 |
| R² 高说明模型一定好用 | 还要看显著性、设定和经济意义 |
| gross return 不含 trading expenses | gross return 已含 trading expenses，只额外扣 mgmt/admin fees |
| 连续复利 r_cc 用 (P1-P0)/P0 计算 | r_cc = ln(P1/P0) = ln(1+HPR)，不是简单收益率 |
| 连续复利下 FV 还用 `PV(1+r)^n` | 若题目利率口径是连续复利，应用 `FV = PVe^(rt)`，PV 则用 `FVe^(-rt)` |
| leveraged return = 自有资金回报率 | leveraged return = R_p + (B/E)(R_p - r_D)，杠杆放大正负收益 |
| after-tax return 先扣税再算杠杆 | 顺序不可逆：Gross → Net → Leverage → Tax |
