---
title: "00-Quantitative Methods-MOC"
description: "CFA Level I 2026 Quantitative Methods 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: CFA Level I
exam_year: 2026
exam_weight: "6-9%"
module_count: 11
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Quantitative_Methods
---

# Quantitative Methods MOC

> **一句话核心**：把投资问题翻译成收益率、现金流、统计推断和模型检验。

---

## 1. 科目定位

- **考试权重**：6-9%
- **官方模块数**：11
- **主线框架**：定义变量 -> 选择统计/现金流工具 -> 计算结果 -> 解释经济含义 -> 检查假设
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |
|---|---|---|---|---|
| M01 | Rates and Returns | 计算+解释 | Introduction / Interest Rates and Time Value of Money | [[M01-Rates-and-Returns]] |
| M02 | Time Value of Money in Finance | 计算+解释 | Introduction / Time Value of Money in Fixed Income and Equity | [[M02-Time-Value-of-Money-in-Finance]] |
| M03 | Statistical Measures of Asset Returns | 计算+解释 | Introduction / Measures of Central Tendency and Location | [[M03-Statistical-Measures-of-Asset-Returns]] |
| M04 | Probability Trees and Conditional Expectations | 计算+解释 | Introduction / Expected Value and Variance | [[M04-Probability-Trees-and-Conditional-Expectations]] |
| M05 | Portfolio Mathematics | 计算+解释 | Introduction / Portfolio Expected Return and Variance of Return | [[M05-Portfolio-Mathematics]] |
| M06 | Simulation Methods | 计算+解释 | Introduction / Lognormal Distribution and Continuous Compounding | [[M06-Simulation-Methods]] |
| M07 | Estimation and Inference | 概念+案例判断 | Introduction / Sampling Methods | [[M07-Estimation-and-Inference]] |
| M08 | Hypothesis Testing | 计算+解释 | Introduction / Hypothesis Tests for Finance | [[M08-Hypothesis-Testing]] |
| M09 | Parametric and Non-Parametric Tests of Independence | 计算+解释 | Introduction / Tests Concerning Correlation | [[M09-Parametric-and-Non-Parametric-Tests-of-Independence]] |
| M10 | Simple Linear Regression | 计算+解释 | Introduction / Estimation of the Simple Linear Regression Model | [[M10-Simple-Linear-Regression]] |
| M11 | Introduction to Big Data Techniques | 概念+应用 | Introduction / How Is Fintech used in Quantitative Investment Analysis? | [[M11-Introduction-to-Big-Data-Techniques]] |

## 3. 核心知识树

```text
Quantitative Methods (6-9%)
├─ 1. Rates and Returns
│  ├─ 1.1 利率三重身份：required return / discount rate / opportunity cost，先定折现口径
│  ├─ 1.2 名义利率分解：real risk-free + inflation + default + liquidity + maturity premium
│  ├─ 1.3 收益率口径：HPR、gross/net、arithmetic/geometric/harmonic，按单期/多期/倍数选择
│  ├─ 1.4 MWRR vs TWRR：现金流由投资者控制用 MWRR，评价经理表现用 TWRR
│  ├─ 1.5 年化与连续复利：普通复利用 `(1+r)^c-1`，连续复利用 `ln(1+HPR)`
│  └─ 1.6 杠杆与税后：先 gross/net，再 leverage，再 tax
├─ 2. Time Value of Money in Finance
│  ├─ 2.1 现金流时间轴：single sum / annuity / perpetuity / growing stream，先判时点再套公式
│  ├─ 2.2 固收与权益估值：债券=票息年金+本金现值，权益=股利现值
│  ├─ 2.3 隐含变量：给 PV 和现金流反推 r、g、PMT、n，Equity 常见 `r = D1/P0 + g`
│  └─ 2.4 现金流可加性：同一现金流组合必须有同一现值，是无套利定价接口
├─ 3. Statistical Measures of Asset Returns
│  ├─ 3.1 中心与位置：mean / median / mode / quantile；偏态或 outlier 时 median 更稳
│  ├─ 3.2 离散度：sample variance 用 `n-1`，CV 比较单位均值风险，downside deviation 看下行
│  ├─ 3.3 分布形态：skew 看长尾方向，kurtosis 看厚尾风险，fat tails 不是 high skewness
│  └─ 3.4 Correlation：方向和线性强度，不等于因果
├─ 4. Probability Trees and Conditional Expectations
│  ├─ 4.1 概率加权矩：`E(X)=Σp_ix_i`，`Var(X)=E(X^2)-[E(X)]^2`
│  ├─ 4.2 概率树：路径概率相乘、同层概率相加，从叶节点回推 conditional expectation
│  └─ 4.3 Bayes 更新：prior × likelihood / total probability，分母必须完整
├─ 5. Portfolio Mathematics
│  ├─ 5.1 组合收益与风险：`E(Rp)=Σw_iE(R_i)`；方差必须包含 covariance 项
│  ├─ 5.2 联合概率函数：由边际收益和联合概率算 covariance / correlation
│  ├─ 5.3 分散化机制：`ρ<1` 即有风险降低，`ρ=-1` 可出现完全对冲
│  └─ 5.4 Roy safety-first：最大化 `[E(Rp)-R_L]/σp`
├─ 6. Simulation Methods
│  ├─ 6.1 分布设定：先选输入分布、参数和相关结构，输出是结果分布而非单点答案
│  ├─ 6.2 Monte Carlo：适合复杂、多路径、非线性 payoff；风险是模型假设错
│  └─ 6.3 Historical / bootstrap：保留历史经验分布，但受样本代表性限制
├─ 7. Estimation and Inference
│  ├─ 7.1 抽样方法：simple random / stratified / cluster / systematic，先识别偏差来源
│  ├─ 7.2 CLT 与 SE：样本均值近似正态，`SE=s/√n` 决定区间宽度
│  ├─ 7.3 置信区间：σ 已知或大样本可用 z，σ 未知且小样本用 t
│  └─ 7.4 Bootstrap / jackknife：用重抽样估计估计量分布和标准误
├─ 8. Hypothesis Testing
│  ├─ 8.1 检验构件：H0/H1、test statistic、critical value、p-value、significance level
│  ├─ 8.2 错误结构：Type I=错拒真 H0，Type II=未拒假 H0；power=1-Type II
│  ├─ 8.3 均值/方差/比例检验：按样本数、独立/配对、方差是否已知选 z/t/F/χ²
│  └─ 8.4 参数 vs 非参数：分布假设不可靠或数据为 ranks 时转非参数
├─ 9. Parametric and Non-Parametric Tests of Independence
│  ├─ 9.1 Correlation test：检验 `ρ=0` 用 `t=r√[(n-2)/(1-r²)]`，df=`n-2`
│  └─ 9.2 Contingency table：expected cell=`row total × column total / n`，df=`(r-1)(c-1)`
├─ 10. Simple Linear Regression
│  ├─ 10.1 模型设定：`Y_i=b0+b1X_i+ε_i`，slope 是 X 每变 1 单位的 Y 期望变化
│  ├─ 10.2 ANOVA 与拟合：SST=SSR+SSE，`R²=SSR/SST` 只说明样本解释度
│  ├─ 10.3 斜率与整体检验：slope 用 t，整体模型用 F，简单回归中 `F=t²`
│  └─ 10.4 预测：点预测 `Ŷ=b0+b1X`，prediction interval 宽于 confidence interval
├─ 11. Introduction to Big Data Techniques
│  ├─ 11.1 Fintech 数据：volume / velocity / variety，非结构化数据需要清洗和特征提取
│  ├─ 11.2 AI/ML 类型：supervised / unsupervised / reinforcement，先看有无标签
│  ├─ 11.3 投资应用：文本情绪、风险监控、组合构建、交易执行
│  └─ 11.4 模型风险：overfitting、data snooping、sample bias、解释性不足
```

## 4. 跨模块依赖关系

```text
Return / discount rate layer
├─ M01 Rates and Returns
│  ├─ feeds M02: discount rate, compounding, IRR/MWRR
│  ├─ feeds M03: arithmetic/geometric/harmonic mean vocabulary
│  └─ feeds Portfolio Management: performance return, leverage, after-tax return
├─ M02 Time Value of Money
│  ├─ feeds Fixed Income: bond price = coupon PV + principal PV, YTM as implied rate
│  ├─ feeds Equity: DDM / Gordon growth and required return
│  └─ feeds Corporate Issuers: NPV, IRR, capital budgeting
Statistical measurement layer
├─ M03 Statistical Measures
│  ├─ feeds M04: mean/variance as probability-weighted moments
│  ├─ feeds M05: variance, covariance, correlation as portfolio risk inputs
│  └─ feeds M10: correlation intuition before regression inference
├─ M04 Probability and Bayes
│  ├─ feeds M05: joint probability table -> covariance/correlation
│  ├─ feeds M06: simulation inputs and scenario probabilities
│  └─ feeds Fixed Income / Risk: default probability updating
Portfolio and inference layer
├─ M05 Portfolio Mathematics
│  ├─ feeds Portfolio Management: diversification, efficient frontier, safety-first choice
│  └─ feeds M06: simulated portfolio return distribution
├─ M06 Simulation Methods
│  └─ feeds Risk Management: stress testing, scenario analysis, distribution of outcomes
├─ M07 Estimation -> M08 Hypothesis Testing -> M09 Independence -> M10 Regression
│  ├─ estimation supplies SE and confidence interval logic
│  ├─ hypothesis testing supplies reject/fail-to-reject discipline
│  └─ regression supplies prediction and model-risk language
└─ M11 Big Data
   ├─ consumes M03-M10: validation, overfitting checks, statistical evidence
   └─ feeds all investment topics: alternative data and model governance
```

| 接口 | Quant 输出 | 下游科目/模块 | 考试判断 |
|---|---|---|---|
| 折现率接口 | required return、PV/FV、IRR | Fixed Income、Equity、Corporate Issuers | 先确认现金流时点和复利频率，再折现或反求收益率。 |
| 风险度量接口 | variance、standard deviation、correlation、covariance | Portfolio Management、Risk Management | 风险不是简单加权平均，相关性决定分散化效果。 |
| 概率接口 | expected value、Bayes、probability tree | Fixed Income credit risk、Derivatives payoff、Risk scenarios | 新信息题用 Bayes，路径题用概率树从终点回推。 |
| 推断接口 | CI、p-value、test statistic、regression output | Equity research、Economics、Portfolio analytics | 统计显著不等于经济显著；fail to reject 不等于 accept。 |
| 数据科技接口 | ML 类型、alternative data、overfitting 风险 | Quant investing、Ethics、Risk governance | 先问数据是否有标签、是否有样本偏差、模型是否可解释。 |

## 5. 核心对比专题

| 重要性 | 对比项 | 英文 | 中文解释 | 考试判断 |
|---|---|---|---|---|
| ⭐⭐⭐ | 概念 vs 应用 | definition vs application | 先确认官方定义，再放入题干情境判断。 | 概念题也要能说出适用条件和例外。 |
| ⭐⭐⭐ | 计算 vs 解释 | calculation vs interpretation | 数值只是中间结果，答案要解释方向、含义和限制。 | 凡是 calculate and interpret 都不能只算。 |
| ⭐⭐ | 静态知识 vs 决策流程 | static knowledge vs decision process | 把每个模块压缩成输入 -> 工具 -> 输出 -> 陷阱。 | 流程化比孤立背诵更抗干扰。 |
| ⭐⭐⭐ | 英文识题 vs 中文理解 | English trigger vs Chinese explanation | 英文用于识别题干，中文用于确认真正含义。 | 避免看到熟词就按直觉作答。 |
| ⭐⭐ | 本模块 vs 跨模块 | single module vs cross-module use | 同一公式/概念可能在估值、风险、伦理或报表中换场景出现。 | 错题要回填到 MOC 节点。 |

## 6. 公式与框架速查

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
| Pooled Estimator | `s_p² = [(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)` | `8.4` | 双样本 t 检验，假设方差相等 |
| Two-Sample t-stat | `t = (x̄₁-x̄₂-d₀)/(s_p·√(1/n₁+1/n₂))` | `8.4` | df = n₁+n₂-2 |
| Unequal Variance t-stat | `t = [(x̄₁-x̄₂)-d₀]/√(s₁²/n₁+s₂²/n₂)` | `8.4.2` | 不合并方差，df 用 Satterthwaite 调整 |
| Paired Comparisons t | `t = d̄/(s_d/√n)` | `8.4` | 配对/相关样本，df = n-1 |
| F-test for Variances | `F = s₁²/s₂²` | `8.4` | 检验 σ₁² = σ₂²，df₁=n₁-1, df₂=n₂-1 |
| Two-Sample Proportion z | `z = (p̂₁-p̂₂)/√[p̂(1-p̂)(1/n₁+1/n₂)]` | `8.4` | 合并比例 p̂ = (x₁+x₂)/(n₁+n₂) |
| Chi-Square Test for Variance | `χ² = (n-1)s²/σ₀²` | `8.5` | 检验单总体方差，df = n-1，对正态性敏感 |

### M09 Tests of Independence

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Correlation test t | `t = r√[(n - 2)/(1 - r^2)]` | `9.1` | 【考纲重点】检验总体相关系数 `ρ = 0` |
| Correlation test df | `df = n - 2` | `9.1` | 【考纲重点】不要误用 `n - 1` |
| Chi-square Independence Test | `χ² = Σ[(O - E)^2/E]` | `9.1` | 【考纲重点】列联表独立性检验 |
| Expected Cell Frequency | `E = (row total x column total) / sample size` | `9.1` | 【考纲重点】先算期望频数再算 `χ²` |
| Chi-square df | `df = (r - 1)(c - 1)` | `9.1` | 【考纲重点】`r` 为行数，`c` 为列数 |

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
| Predicted Value | `Ŷ = b_0 + b_1X` | `10.3` | 【考纲重点】预测因变量点估计 |
| Prediction Interval | `Ŷ ± t_c x s_f` | `10.3` | 【考纲重点】CFA L1 常给 `s_f` 或软件输出，不要求手推完整 `s_f` |

### 考纲范围标记

| 标记 | 内容 |
|------|------|
| 【考纲重点】 | Returns/TVM/Statistics/Probability/Portfolio Math/Sampling/Hypothesis Testing/Independence Tests/Regression 中所有 `calculate / determine / interpret` 型 LOS |
| 【考纲内但无核心公式】 | Simulation Methods、Big Data and ML 主要考概念、流程、用途与风险 |
| 【超纲/扩展】 | 多元回归、机器学习模型数学细节、完整预测区间标准误推导属于 Level I 以外或软件输出层面 |

---

## 7. 高频考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 高频场景 |
|---|---|---|
| ❌ arithmetic mean 就是长期平均收益 | ✅ 长期复合更看 geometric mean | 按官方定义和 LOS 口径核验。 |
| ❌ MWRR 和 TWRR 本质一样 | ✅ 一个看现金流敏感，一个看经理表现 | 按官方定义和 LOS 口径核验。 |
| ❌ annuity due 和 ordinary annuity 一样 | ✅ annuity due 多乘 `(1+r)` | 按官方定义和 LOS 口径核验。 |
| ❌ sample variance 分母也是 n | ✅ sample variance 用 `n-1` | 按官方定义和 LOS 口径核验。 |
| ❌ fat tails 就是 skewness 高 | ✅ fat tails 对应 kurtosis 高 | 按官方定义和 LOS 口径核验。 |
| ❌ Bayes 只是公式题 | ✅ 它本质是“用新信息更新旧概率” | 按官方定义和 LOS 口径核验。 |
| ❌ p-value 小表示 H0 大概率为假 | ✅ p-value 是“在 H0 成立下出现样本的极端程度” | 按官方定义和 LOS 口径核验。 |
| ❌ fail to reject H0 等于接受 H0 | ✅ 只是证据不足以拒绝 | 按官方定义和 LOS 口径核验。 |
| ❌ correlation 高说明因果强 | ✅ 相关不等于因果 | 按官方定义和 LOS 口径核验。 |
| ❌ R² 高说明模型一定好用 | ✅ 还要看显著性、设定和经济意义 | 按官方定义和 LOS 口径核验。 |

## 8. 通用分析框架

### 框架1：收益率题决策树

1. 题目问单一持有期总回报：用 `HPR = (P1 - P0 + D1)/P0`。
2. 题目问多期历史平均财富增长：用 `geometric mean`；问下一期预期收益：用 `arithmetic mean`。
3. 有外部现金流且问投资者实际体验：用 `MWRR/IRR`。
4. 有外部现金流但问经理表现：拆分子期间，用 `TWRR = Π(1+HP_i)-1`。
5. 题目给连续复利口径：普通收益转 `r_cc=ln(1+HPR)`；连续转普通用 `e^r-1`。
6. 题目有费用、杠杆、税：按 `gross -> net -> leveraged -> after-tax` 排序，不提前扣税。

### 框架2：统计推断题决策树

1. 先问任务是 estimation 还是 hypothesis test。
2. Estimation：点估计直接用样本统计量；区间估计先选标准误 `SE=s/√n`，再选 z/t。
3. σ 已知或大样本且条件允许：用 z；σ 未知、小样本且近似正态：用 t。
4. Hypothesis test：先写 H0/H1，再判断 one-tailed / two-tailed。
5. 单总体均值：z/t；双均值独立样本：pooled 或 unequal t；配对样本：paired t。
6. 方差检验：单方差用 χ²，双方差用 F；类别独立性用 χ²。
7. 决策只写 reject / fail to reject；解释时补充经济意义和样本限制。

### 框架3：回归题决策树

1. 先确认模型：`Y_i=b0+b1X_i+ε_i`，Y 是被解释变量，X 是解释变量。
2. 问点预测：代入 `Ŷ=b0+b1X`。
3. 问 slope 解释：X 增加 1 单位，Y 的条件期望改变 `b1`。
4. 问 slope 是否显著：用 `t=(b1-β1,0)/SE(b1)`。
5. 问模型整体是否显著：用 `F=MSR/MSE`；简单回归中可用 `F=t²` 校验。
6. 问拟合度：看 `R²=SSR/SST`，但不能推出因果或预测稳定。
7. 问预测区间：prediction interval 用于单个 Y，宽于 mean response 的 confidence interval。

---

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

- 本 MOC 已优先吸收 `_legacy/2026-05-26-official-sync/` 中的中文解释、公式、陷阱和框架。
- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。
