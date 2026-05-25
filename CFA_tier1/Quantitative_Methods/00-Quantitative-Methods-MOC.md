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

## 科目概览（与 CFA 2026 L1 官方课程对齐）

| 模块  | 官方 Module | 内容                        | 难度    | 必考点                                         | 章节文件 |
| --- | --- | ------------------------- | ----- | ------------------------------------------- | --- |
| M01 | M1: Rates and Returns | Rates and Returns         | 概念+计算 | HPR, MWRR, TWRR, annualized return          | [[M01-Rates-and-Returns]] |
| M02 | M2: Time Value of Money in Finance | Time Value of Money in Finance      | 计算    | PV/FV, annuity, perpetuity, implied return, cash flow additivity | [[M02-Time-Value-of-Money]] |
| M03 | M3: Statistical Measures of Asset Returns | Statistical Measures of Asset Returns      | 概念+计算 | mean, variance, skewness, kurtosis, correlation | [[M03-Statistical-Measures]] |
| M04 | M4: Probability Trees and Conditional Expectations | Probability Trees & Conditional Expectations | 概念    | expected value, probability trees, Bayes    | [[M04-Probability-Concepts]] |
| M05 | M5: Portfolio Mathematics | Portfolio Mathematics     | 计算    | covariance, correlation, portfolio variance, shortfall risk | [[M05-Portfolio-Mathematics]] |
| M06 | M6: Simulation Methods | Simulation Methods                | 概念    | Monte Carlo, bootstrap, lognormal distribution | [[M06-Simulation-Methods]] |
| M07 | M7: Estimation and Inference | Sampling, Estimation & Inference     | 计算    | CLT, standard error, confidence interval, bootstrap | [[M07-Sampling-and-Estimation]] |
| M08 | M8: Hypothesis Testing | Hypothesis Testing        | 计算+策略 | H0/H1, Type I/II, p-value, parametric vs nonparametric | [[M08-Hypothesis-Testing]] |
| M09 | M9: Parametric & Non-Parametric Tests of Independence | Tests of Independence     | 计算+策略 | correlation test, contingency table, parametric vs nonparametric | [[M09-Tests-of-Independence]] |
| M10 | M10: Simple Linear Regression | Correlation & Regression  | 计算+策略 | t-test, F-test, R^2, SEE, prediction | [[M09-Correlation-and-Regression]] |
| M11 | M11: Introduction to Big Data Techniques | Big Data / ML Techniques       | 概念    | fintech, AI/ML, data science applications | [[M10-Big-Data-and-ML]] |

---

## Quantitative Methods 核心知识树 (Core Knowledge Tree)

```text
Quantitative Methods (数量方法) (M01-M11)
│
├── M01: Rates and Returns (收益率与回报)
│   ├── 1.1 Interest Rate 的三种解释 (Three Interpretations of Interest Rate)【考试核心】↔ Topic Outline P0
│   │   ├── required rate of return: 投资者要求回报
│   │   ├── discount rate: 将未来现金流折现回今天
│   │   └── opportunity cost: 放弃下一优选择的代价
│   ├── 1.2 Interest Rate Decomposition (利率分解)【考试核心】
│   │   ├── 实际无风险利率 (Real Risk-Free Rate)
│   │   ├── 预期通胀溢价 (Expected Inflation Premium)
│   │   ├── 违约/流动性/期限/其他风险溢价 (Default/Liquidity/Maturity/Other Risk Premiums)
│   │   └── 注意：rate 高不只因 inflation，高风险补偿也会抬升 rate【考试陷阱】
│   ├── 1.3 Return Measurement Ladder (收益率度量阶梯)【考试核心】
│   │   ├── 持有期收益率 = (期末价-期初价+收入)/期初价值 (HPR = Price Change + Income over Beginning Value)
│   │   ├── 核心公式 (English)
│   │   │   ├── `HPR = (P_1 - P_0 + D_1)/P_0`（持有期收益率公式）
│   │   │   ├── `Arithmetic mean = Σ_{i=1}^{n} R_i / n`（算术平均收益率公式）
│   │   │   └── `Geometric mean = [(1 + R_1)...(1 + R_n)]^(1/n) - 1`（几何平均收益率公式）
│   │   ├── arithmetic mean: 单期 expected return 口径
│   │   ├── geometric mean: 多期复合增长口径
│   │   └── harmonic mean: price multiple / averaging rate 场景易见
│   ├── 1.4 MWRR vs TWRR (资金加权 vs 时间加权收益率)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   ├── `MWRR: Σ CFt/(1+r)^t = 0`（资金加权收益率公式）
│   │   │   ├── `Compounded TWRR = [(1 + HP_1)(1 + HP_2)...(1 + HP_n)] - 1`（复合时间加权收益率公式）
│   │   │   └── `Annualized TWRR = (1 + Compounded TWRR)^(1/n) - 1`（年化时间加权收益率公式）
│   │   ├── 资金加权收益率 = 组合现金流内部收益率 (MWRR = Portfolio Cash Flow IRR) (IRR反映投资者体验)
│   │   ├── 时间加权收益率 = 外部现金流中断后连接子期间收益 (TWRR = Subperiod Returns Linked After External Cash-Flow Breaks) (几何链接反映经理能力)
│   │   └── 注意：客户增减资金造成的 return distortion 归 MWRR，不归经理【考试陷阱】
│   └── 1.5 Annualization and Continuous Compounding (年化与连续复利)【考试核心】
│       ├── 核心公式 (English)
│       │   ├── `Annualized return = (1+R_period)^c - 1`（年化收益率公式）
│       │   ├── `r_cc = ln(1 + HPR)`（连续复利收益率公式）
│       │   ├── `FV = PVe^(rt)`（连续复利终值公式）
│       │   └── `PV = FVe^(-rt)`（连续复利现值公式）
│       ├── 实际年化收益率 vs 名义期间收益率 (Effective Annual Return vs Stated Period Return)
│       ├── 连续复利收益率 = ln(1 + HPR) (r_cc = ln(1 + HPR)) (对数比价非简单差)
│       └── continuously compounded returns 可加，普通 returns 不可直接相加
│   ├── 1.6 Gross Return vs Net Return (总回报 vs 净回报)【考试核心】← 高频错因
│   │   ├── 总回报 = (期末价+股利)/期初价 = 1 + HPR (Gross Return = (P_1 + D_1)/P_0 = 1 + HPR)
│   │   ├── Trading expenses 已反映在 gross return 中，不重复扣除 (已含交易费)
│   │   ├── 净回报 = 总回报 - 管理费/行政费 (Net Return = Gross Return - Management/Admin Fees) (管理费额外扣)
│   │   └── 注意：gross return 是税前、非风险调整口径【考试陷阱】
│   ├── 1.7 Leveraged and After-Tax Return (杠杆与税后回报)【考试核心】← 高频错因
│   │   ├── 杠杆回报 = 自有资金回报 + (借款/自有资本)(组合回报 - 借款利率) (Leveraged Return = R_p + (B/E)(R_p - r_D))
│   │   │   └── B = 借款额, E = 自有本金, r_D = 借款利率
│   │   ├── 税后回报 = 税前回报 × (1 - 税率) (After-Tax Return = Pre-tax Return × (1 - t))
│   │   │   └── t = 税率
│   │   └── 注意：计算顺序不可逆：Gross → Net → Leverage → Tax【考试陷阱】
│
├── M02: Time Value of Money (货币时间价值)
│   ├── 2.1 Cash-Flow Map (现金流时间轴)【考试核心】↔ Topic Outline P0
│   │   ├── 核心公式 (English)
│   │   │   ├── `FV = PV(1+r)^n`（终值公式）
│   │   │   ├── `PV = FV/(1+r)^n`（现值公式）
│   │   │   ├── `Ordinary annuity PV = A[1-1/(1+r)^n]/r`（普通年金现值公式）
│   │   │   └── `Perpetuity PV = A/r`（永续年金现值公式）
│   │   ├── 单笔现金流: 一个现值对应一个终值 (Single Sum: One PV / One FV)
│   │   ├── 等额年金: 有限期等额现金流 (Level Annuity: Equal Finite Cash Flows)
│   │   ├── 永续年金: 等额现金流永续支付 (Perpetuity: Equal Cash Flows Forever)
│   │   └── 增长现金流: 增长率和折现率都重要 (Growing Stream: Growth and Discount Rate Both Matter)
│   ├── 2.2 Instrument PV Applications (工具现值应用)【考试核心】
│   │   ├── 固定收益价格 = 票息现值 + 本金现值 (Fixed-Income Price = Coupons PV + Principal PV)
│   │   ├── 股权内在价值 = 股利/现金流预期现值 (Equity Intrinsic Value = Dividends/Cash-Flow Expectations PV)
│   │   └── 注意：先识别 cash-flow timing，再选 formula【考试陷阱】
│   ├── 2.3 Implied Quantities (隐含变量求解)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   └── `r = D_1/P_0 + g`（戈登增长模型隐含回报率）
│   │   ├── 债券隐含回报率 = 现值和约定现金流的反算 (Bond Implied Return from PV and Promised CF)
│   │   ├── 股权要求回报率 = 从价格、股利和增长反算 (Equity Required Return from Price, Dividend, Growth)
│   │   └── 股权隐含增长率 = 从价格和要求回报率反算 (Equity Implied Growth from Price and Required Return)
│   └── 2.4 Cash-Flow Additivity (现金流可加性)【考试核心】
│       ├── 组合现值 = 各组成部分现值之和 (Portfolio PV = Sum of Component PVs)
│       ├── 无套利逻辑 (No-Arbitrage Logic)
│       ├── 远期利率/远期外汇/期权价值直觉 (Forward Interest / Forward FX / Option Value Intuition)
│       └── 注意：同一 cash flow 不应因拆分方式不同而变价
│
├── M03: Statistical Measures (统计量与分布特征)
│   ├── 3.1 Central Tendency and Location (集中趋势与位置指标)【考试核心】↔ Topic Outline P1
│   │   ├── 算术/几何/调和平均 (Arithmetic / Geometric / Harmonic Mean)
│   │   ├── 加权平均 (Weighted Mean)
│   │   ├── 中位数、众数、分位数、百分位数位置 (Median, Mode, Quantiles, Percentile Location)
│   │   └── 注意：outlier 对 mean 影响通常大于 median【考试陷阱】
│   ├── 3.2 Dispersion (离散程度)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   ├── `Population variance = Σ(x-μ)^2/n`（总体方差公式）
│   │   │   ├── `Sample variance = Σ(x-x̄)^2/(n-1)`（样本方差公式）
│   │   │   └── `Standard deviation = sqrt(Variance)`（标准差公式）
│   │   ├── 极差/平均绝对偏差 (Range / Mean Absolute Deviation)
│   │   ├── 方差/标准差 (Variance / Standard Deviation)
│   │   ├── 下行偏差 (Downside Deviation)
│   │   └── 变异系数用于相对离散度 (Coefficient of Variation for Relative Dispersion)
│   ├── 3.3 Distribution Shape (分布形态)【考试核心】
│   │   ├── 偏度: 不对称性 (Skewness: Asymmetry) (y轴=frequency x轴=return)
│   │   ├── 峰度: 尾部厚度 (Kurtosis: Tail Thickness)
│   │   └── 注意：left-skew / right-skew 判断要看长尾方向【考试陷阱】
│   └── 3.4 Correlation Intuition (相关性直觉)【考试核心】
│       ├── 符号 = 方向 (Sign = Direction)
│       ├── 大小 = 线性关联强度 (Magnitude = Linear Association Strength)
│       └── 相关 ≠ 因果 (Correlation ≠ Causation)
│
├── M04: Probability Concepts (概率基础)
│   ├── 4.1 Expected Value / Variance / Standard Deviation (期望值/方差/标准差)【考试核心】↔ Topic Outline P1
│   │   ├── 核心公式 (English)
│   │   │   ├── `E(X) = Σ p(xi)xi`（期望值公式）
│   │   │   └── `Var(X) = E(X^2)-[E(X)]^2`（方差公式）
│   │   ├── 离散概率结果 (Discrete Outcome Probabilities)
│   │   ├── 概率加权离散度衡量的总风险 (Total Risk from Probability-Weighted Dispersion)
│   │   └── expected value 是概率加权中心，不是必然结果
│   ├── 4.2 Probability Tree (概率树)【考试核心】
│   │   ├── 分支概率 (Branch Probability)
│   │   ├── 终端收益 (Terminal Payoff)
│   │   └── 决策节点的条件期望 (Conditional Expectation at Decision Node)
│   └── 4.3 Bayes Update (贝叶斯更新)【考试核心】
│       ├── 核心公式 (English)
│       │   ├── `P(A|B) = P(A∩B)/P(B)`（条件概率公式）
│       │   └── `P(Bj|A)=[P(A|Bj)P(Bj)]/Σ[P(A|Bi)P(Bi)]`（贝叶斯公式）
│       ├── 先验概率 (Prior Probability)
│       ├── 条件似然 (Conditional Likelihood)
│       ├── 后验概率 (Posterior Probability)
│       └── 注意：更新后概率要回到完整分母，不只看 numerator【考试陷阱】
│
├── M05: Portfolio Mathematics (投资组合数学)
│   ├── 5.1 Return Moments (收益率矩)【考试核心】↔ Topic Outline P1
│   │   ├── 核心公式 (English)
│   │   │   ├── `E(Rp) = Σ wiE(Ri)`（组合期望收益率公式）
│   │   │   └── `σp² = w1²σ1²+w2²σ2²+2w1w2Cov12`（组合方差公式）
│   │   ├── 组合期望收益率 (Portfolio Expected Return)
│   │   ├── 方差和标准差 (Variance and Standard Deviation)
│   │   └── 全额投资组合权重和为1 (Weights Sum to One for Fully Invested Portfolio)
│   ├── 5.2 Joint Probability Function (联合概率函数)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   ├── `Cov12 = Σ p(R1-E(R1))(R2-E(R2))`（协方差公式）
│   │   │   └── `Corr12 = Cov12/(σ1σ2)`（相关系数公式）
│   │   ├── 情景对收益 (Scenario Pair Returns)
│   │   ├── 联合状态协方差 (Covariance from Joint States)
│   │   └── 相关系数标准化协方差 (Correlation Standardizes Covariance)
│   ├── 5.3 Diversification Mechanics (分散化机制)【考试核心】
│   │   ├── 协方差项驱动两资产风险 (Covariance Term Drives Two-Asset Risk)
│   │   ├── 较低相关性降低组合方差 (Lower Correlation Lowers Portfolio Variance)
│   │   └── 注意：低 correlation 不等于负 expected return
│   └── 5.4 Shortfall Risk (短缺风险)【考试核心】
│       ├── 核心公式 (English)
│       │   └── `Roy safety-first = (E(Rp)-RL)/σp`（罗伊安全优先比率公式）
│       ├── 阈值回报率 (Threshold Return RL)
│       ├── 罗伊安全优先比率 (Roy Safety-First Ratio)
│       └── 收益服从正态时选择最高安全优先比率的组合 (Choose Highest Safety-First Ratio When Returns Assumed Normal)
│
├── M06: Simulation Methods (模拟方法)
│   ├── 6.1 Distribution Link (分布联动)【考试核心】↔ Topic Outline P1
│   │   ├── 连续复利收益率可被建模为正态分布 (正态→对数正态映射)
│   │   └── 由这些收益导出的价格呈对数正态且非负 (价格非负有下限)
│   ├── 6.2 Monte Carlo (蒙特卡洛模拟)【考试核心】
│   │   ├── 指定输入分布 (Specify Input Distribution) (设定参数/分布形态)
│   │   ├── 抽取随机情景 (Draw Random Scenarios) (大量路径模拟)
│   │   └── 汇总输出分布 (Summarize Output Distribution) (统计量/分位数)
│   └── 6.3 Bootstrap Resampling (自助重抽样)【考试核心】
│       ├── 有放回地重抽观测数据 (Resample Observed Data with Replacement) (经验分布重抽样)
│       └── 注意：bootstrap inherits observed-sample limitations【考试陷阱】
│
├── M07: Sampling and Estimation (抽样与估计)
│   ├── 7.1 Sampling Methods (抽样方法)【考试核心】↔ Topic Outline P1
│   │   ├── 简单随机/分层/整群抽样 (Simple Random / Stratified / Cluster)
│   │   ├── 便利/判断抽样 (Convenience / Judgmental)
│   │   └── 抽样方法改变抽样误差和偏误暴露程度 (Sampling Method Changes Sampling Error and Bias Exposure)
│   ├── 7.2 CLT and Standard Error (中心极限定理与标准误)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   └── `SE = σ/√n` 或 `s/√n`（标准误公式）
│   │   ├── 样本均值分布随 n 增大而收紧 (Sample Mean Distribution Tightens as n Grows)
│   │   ├── 标准误按 1/sqrt(n) 缩放 (SE Scales by 1/sqrt(n))
│   │   └── 注意：大样本降低 standard error，不消灭 bad sampling design【考试陷阱】
│   └── 7.3 Resampling Estimators (重抽样估计量)【考试核心】
│       ├── 自助法 (Bootstrap)有放回重抽原始样本估统计量分布 (有放回重抽估标准误)
│       └── 刀切法 (Jackknife)逐次删除一个观测值估偏误，非去异常值 (逐次剔一估偏误)
│
├── M08: Hypothesis Testing (假设检验)
│   ├── 8.1 Test Components (检验构件)【考试核心】↔ Topic Outline P2
│   │   ├── 核心公式 (English)
│   │   │   ├── `CI: x̄ ± z_(α/2)σ/√n`（已知总体方差的置信区间）
│   │   │   ├── `CI: x̄ ± t_(α/2,n-1)s/√n`（未知总体方差的置信区间）
│   │   │   └── `z/t = (x̄-μ0)/(σ/√n)` or `(x̄-μ0)/(s/√n)`（检验统计量公式）
│   │   ├── 原假设/备择假设 (Null / Alternative)
│   │   ├── 显著性水平 α (Significance Level Alpha)
│   │   ├── 检验统计量和拒绝域 (Test Statistic and Rejection Region)
│   │   └── p值作为反对原假设的证据 (p-Value as Evidence Against Null)
│   ├── 8.2 Error Architecture (错误结构)【考试核心】
│   │   ├── 第一类错误 = 拒绝真实 H0 (Type I Error = Reject True H0)
│   │   ├── 第二类错误 = 未拒绝错误 H0 (Type II Error = Fail to Reject False H0)
│   │   └── 检验力 = 1 - P(第二类错误) (Power = 1 - Probability(Type II Error))
│   └── 8.3 Parametric vs Nonparametric (参数与非参数检验)【考试核心】
│       ├── 参数检验依赖分布假设 (Parametric Relies on Distributional Assumptions)
│       └── 非参数检验在假设/尺度条件不满足时有用 (Nonparametric Helps When Assumptions / Scale Conditions Fail)
│
├── M09: Tests of Independence (独立性检验)
│   ├── 9.1 Correlation Tests (相关检验)【考试核心】↔ Topic Outline P2
│   │   ├── 总体相关系数等于零检验 (Population Correlation Equals Zero Test)
│   │   ├── 参数 vs 非参数相关检验 (Parametric vs Nonparametric Correlation Test)
│   │   └── 列联表独立性检验 (Contingency Table Independence Test)
│
├── M10: Simple Linear Regression (简单线性回归)
│   ├── 10.1 Simple Linear Regression Model (简单线性回归模型)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   ├── `Yi = b0 + b1Xi + ei`（回归方程公式）
│   │   │   ├── `b1 = Cov(X,Y)/Var(X)`（斜率公式）
│   │   │   └── `b0 = ȳ - b1x̄`（截距公式）
│   │   ├── 因变量 Y (Dependent Variable Y)
│   │   ├── 自变量 X (Independent Variable X)
│   │   ├── 截距、斜率、残差 (Intercept, Slope, Residual)
│   │   └── 最小二乘法最小化 SSE (Least Squares Minimizes SSE)
│   ├── 10.2 Regression Diagnostics (回归诊断)【考试核心】
│   │   ├── 线性/同方差/独立性/正态误差 (Linearity / Homoskedasticity / Independence / Normal Errors)
│   │   └── 残差图提示假设违反 (Residual Plot Hints Assumption Violations)
│   ├── 10.3 Fit and Inference (拟合与推断)【考试核心】
│   │   ├── 核心公式 (English)
│   │   │   ├── `R² = SSR/SST`（R平方公式）
│   │   │   ├── `SEE = sqrt(SSE/(n-2))`（估计标准误公式）
│   │   │   ├── `t = (b1-β1,0)/SE(b1)`（斜率t检验公式）
│   │   │   └── `F = MSR/MSE`（F检验公式）
│   │   ├── R²、SEE、系数t检验、ANOVA F检验 (R2, SEE, Coefficient t-test, ANOVA F-test)
│   │   ├── 预测值和预测区间 (Predicted Value and Prediction Interval)
│   │   └── 不同函数形式 (Different Functional Forms)
│   └── 注意：prediction interval 比 point estimate 更诚实地表达 uncertainty【考试陷阱】
│
└── M11: Big Data and ML (大数据与机器学习)
    ├── 11.1 Fintech data context【考试核心】↔ Topic Outline P2
    │   ├── 数据收集 (Data Gathering)
    │   └── 数据分析在投资过程中的相关性 (Data Analysis Relevance for Investment Process)
    ├── 11.2 Big Data / AI / ML definitions【考试核心】(三大概念辨析)
    └── 11.3 Investment applications【考试核心】
        ├── 研究信号提取 (Research Signal Extraction) (Alpha/因子挖掘)
        ├── 风险/运营/客户分析 (Risk / Operations / Client Analytics) (风控/效率/画像)
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
└── TVM (中文)
    ├── Statistical Measures (中文)
    │   └── Probability (中文)
    │       └── Portfolio Mathematics (中文)
    └── Sampling and Estimation (中文)
        └── Hypothesis Testing (中文)
            └── Regression (中文)
                └── Big Data / ML (中文)
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
| HPR                            | `(P_1 - P_0 + D_1)/P_0`              | `1.3` | 最基础收益率公式                         |
| Gross Return                   | `(P_1 + D_1)/P_0 = 1 + HPR`          | `1.6` | 连乘收益时常改用 gross return            |
| Arithmetic Mean                | `Σ_{i=1}^{n} R_i / n`                | `1.3` | 单期 expected return 常用            |
| Geometric Mean                 | `[(1 + R_1)(1 + R_2)...(1 + R_n)]^(1/n) - 1` | `1.3` | 多期复合财富增长口径                       |
| Annualized Return              | `(1 + R_period)^c - 1`               | `1.5` | `c` 是一年内期数                       |
| Continuously Compounded Return | `ln(1 + HPR)`                        | `1.5` | 与普通 HPR 可互转                      |
| Convert CC Return              | `e^(r_cc) - 1`                       | `1.5` | 连续复利回到 holding period return     |
| MWRR                           | `0 = Σ_{t=0}^{N} CF_t/(1 + r)^t`     | `1.4` | 投资者现金流敏感，实质是 IRR                 |
| Compounded TWRR                | `[(1 + HP_1)(1 + HP_2)...(1 + HP_n)] - 1` | `1.4` | 多期子期间收益几何链接后的总回报                 |
| Annualized TWRR                | `(1 + Compounded TWRR)^(1/n) - 1`    | `1.4` | 跨 `n` 年比较时再做年化                     |
| Net Return                     | `Gross Return - Mgmt/Admin Fees`     | `1.6` | trading expenses 已在 gross 中，不重复减 |
| Leveraged Return               | `R_p + (B/E)(R_p - r_D)`             | `1.7` | B=借款, E=自有本金, r_D=借款利率           |
| After-Tax Return               | `R_pre × (1 - t)`                    | `1.7` | t=税率，先算杠杆后税前回报再扣税                |

### M02 Time Value of Money

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| FV | `FV = PV(1 + r)^n` | `2.1` | TVM 核心 |
| PV | `PV = FV/(1 + r)^n` | `2.1` | TVM 核心 |
| FV with Continuous Compounding | `FV = PV e^(rt)` | `2.1` | 当题目给的是连续复利利率时，用 `e^(rt)` 而不是 `(1+r)^n` |
| PV with Continuous Discounting | `PV = FV e^(-rt)` | `2.1` | 连续贴现是连续复利的逆运算 |
| Ordinary Annuity PV | `PV = A[1 - 1/(1 + r)^n]/r` | `2.1` | 固定期末现金流 |
| Ordinary Annuity FV | `FV = A[(1 + r)^n - 1]/r` | `2.1` | 累积型现金流 |
| Annuity Due PV | `PV_due = PV_ordinary(1 + r)` | `2.1` | 期初支付多滚一期 |
| Annuity Due FV | `FV_due = FV_ordinary(1 + r)` | `2.1` | 易与 ordinary annuity 混 |
| Perpetuity PV | `PV = A/r` | `2.1` | 高频快算 |
| Growing Perpetuity PV | `PV = A_1/(r - g)` | `2.1` | 必须满足 `r > g` |
| Growing Annuity PV | `PV = [A_1/(r - g)][1 - (1 + g)^n/(1 + r)^n]` | `2.1` | 增长有限期现金流 |
| Gordon Link | `r = D_1/P_0 + g` | `2.3` | Quant 与 Equity 交叉 |

### M03-M05 Statistics, Probability, Portfolio Math

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Population Variance | `Σ_{i=1}^{n}(x_i - μ)^2/n` | `3.2` | 总体已知口径 |
| Sample Variance | `Σ_{i=1}^{n}(x_i - x̄)^2/(n - 1)` | `3.2` | 注意 n-1 |
| Standard Deviation | `σ = sqrt(Variance)` | `3.2` | 风险与离散度基本量 |
| Coefficient of Variation | `CV = s/x̄` | `3.2` | 相对离散度 |
| Expected Value | `E(X) = Σ p_i x_i` | `4.1` | 概率题入口 |
| Variance Identity | `Var(X) = E(X^2) - [E(X)]^2` | `4.1` | 两种方差算法要会互认 |
| Conditional Probability | `P(A|B) = P(A∩B)/P(B)` | `4.3` | Bayes 前置 |
| Total Probability | `P(A) = Σ P(A|B_i)P(B_i)` | `4.3` | Bayes 分母 |
| Bayes Formula | `P(B_j|A) = [P(A|B_j)P(B_j)] / Σ[P(A|B_i)P(B_i)]` | `4.3` | 用新信息更新先验 |
| Portfolio Return | `E(R_p) = Σ w_i E(R_i)` | `5.1` | 权重求和 |
| Covariance | `Cov(R_1,R_2) = Σ p_i[R_{1,i} - E(R_1)][R_{2,i} - E(R_2)]` | `5.2` | 组合方差前置 |
| Correlation | `Corr(R_1,R_2) = Cov(R_1,R_2)/(σ_1σ_2)` | `5.2` | 规范到 `-1` 至 `1` |
| Portfolio Variance | `σ_p^2 = w_1^2σ_1^2 + w_2^2σ_2^2 + 2w_1w_2Cov(R_1,R_2)` | `5.1` | 常考两资产组合 |
| Roy Safety-First | `SFRatio = [E(R_p) - R_L]/σ_p` | `5.4` | threshold return 框架 |

### M07-M08 Sampling and Testing

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Standard Error | `SE = σ/√n` or `s/√n` | `7.2` | 抽样与估计核心 |
| CI, Sigma Known | `x̄ ± z_(α/2)σ/√n` | `8.1` | 总体方差已知 |
| CI, Sigma Unknown | `x̄ ± t_(α/2,n-1)s/√n` | `8.1` | 常见考试场景 |
| Required Sample Size | `n = (zσ/E)^2` | `7.2` | `E` 是 margin of error |
| z-stat / t-stat | `(x̄ - μ_0)/(σ/√n)` or `(x̄ - μ_0)/(s/√n)` | `8.1` | 先分清方差是否已知 |

### M09 Tests of Independence

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Correlation test t | `t = r√[(n - 2)/(1 - r^2)]` | `9.1` | 独立性检验 |

### M10 Simple Linear Regression

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Regression Equation | `Y_i = b_0 + b_1X_i + e_i` | `10.1` | 简单线性回归骨架 |
| Regression slope | `b_1 = Cov(X,Y)/Var(X)` | `10.1` | 回归核心 |
| Regression Intercept | `b_0 = ȳ - b_1x̄` | `10.1` | 斜率确定后回代 |
| R-squared | `R^2 = SSR/SST` | `10.3` | 拟合度，不是因果性 |
| SEE | `SEE = sqrt[SSE/(n - 2)]` | `10.3` | 回归残差尺度 |
| Slope t-stat | `t = (b_1 - β_{1,0})/SE(b_1)` | `10.3` | 检验 slope |
| F-stat | `F = MSR/MSE` | `10.3` | 检验整体模型 |

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
| 连续复利 r_cc 用 `(P_1 - P_0)/P_0` 计算 | `r_cc = ln(P_1/P_0) = ln(1 + HPR)`，不是简单收益率 |
| 连续复利下 FV 还用 `PV(1+r)^n` | 若题目利率口径是连续复利，应用 `FV = PVe^(rt)`，PV 则用 `FVe^(-rt)` |
| leveraged return = 自有资金回报率 | leveraged return = R_p + (B/E)(R_p - r_D)，杠杆放大正负收益 |
| after-tax return 先扣税再算杠杆 | 顺序不可逆：Gross → Net → Leverage → Tax |
