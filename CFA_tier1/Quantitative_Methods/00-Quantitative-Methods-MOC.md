---
title: "00-Quantitative-Methods-MOC"
description: "CFA Level I Quantitative Methods 导航中枢 — 知识树·公式·陷阱·跨模关联·复习框架"
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
level: CFA Level I
exam_weight: "6-9%"
exam_format: 单选题
difficulty: 公式基础与统计推断并重
note_type: master_moc
status: active
aliases:
  - Quantitative Methods 知识框架
  - 数量方法 MOC
tags:
  - CFA_L1
  - MOC
  - Quantitative_Methods
  - formulas
  - official_2026
---

# 📊 00-Quantitative-Methods-MOC

> **一句话核心**：先统一口径 → 再折现 → 再统计 → 再检验。投资问题翻译成统一的计算语言。

---

## 📋 科目概览（与 CFA 2026 L1 官方课程对齐）

| # | 官方 Module | ⚖️ 难度 | 🎯 必考点 | 🔗 模块 |
|---|-------------|----------|-----------|---------|
| M01 | Rates and Returns | 概念+计算 | HPR, MWRR, TWRR, 年化/杠杆/税后收益率 | [[M01-Rates-and-Returns]] |
| M02 | Time Value of Money in Finance | 计算 | PV/FV, 年金, 永续, 隐含回报, 现金流可加性 | [[M02-Time-Value-of-Money-in-Finance]] |
| M03 | Statistical Measures | 概念+计算 | 均值/中位数, 方差/标准差, 偏度/峰度, 相关系数 | [[M03-Statistical-Measures-of-Asset-Returns]] |
| M04 | Probability Trees & Conditional Expectations | 概念 | 期望值, 概率树, 贝叶斯公式 | [[M04-Probability-Trees-and-Conditional-Expectations]] |
| M05 | Portfolio Mathematics | 计算 | 协方差/相关系数, 组合方差, 安全优先比率 | [[M05-Portfolio-Mathematics]] |
| M06 | Simulation Methods | 概念 | 蒙特卡洛, 自助法, 对数正态分布, 连续复利 | [[M06-Simulation-Methods]] |
| M07 | Estimation and Inference | 计算 | CLT, 标准误, 置信区间, 重抽样 | [[M07-Estimation-and-Inference]] |
| M08 | Hypothesis Testing | 计算+策略 | H₀/H₁, Type I/II, p-value, pooled/unpooled t, F检验, χ²检验, 配对检验 | [[M08-Hypothesis-Testing]] |
| M09 | Tests of Independence | 计算+策略 | 相关系数检验, 列联表, Spearman | [[M09-Parametric-and-Non-Parametric-Tests-of-Independence]] |
| M10 | Simple Linear Regression | 计算+策略 | t检验, F检验, R², SEE, 预测区间, 函数形式 | [[M10-Simple-Linear-Regression]] |
| M11 | Big Data Techniques | 概念 | Fintech, AI/ML, 大数据应用 | [[M11-Introduction-to-Big-Data-Techniques]] |

---

## 🌳 核心知识树

```text
📊 Quantitative Methods (6-9%) (M01-M11)
│
├─ 🏆 M01: Rates and Returns（收益率与回报）── 先统一口径
│  ├─ ⭐ 1.1 Interest Rate 三解释：required return / discount rate / opportunity cost
│  ├─ ⭐ 1.2 利率分解：实际无风险 + 通胀溢价 + 各类风险溢价
│  ├─ ⭐ 1.3 收益率阶梯
│  │  ├─ 📐 HPR = (P₁-P₀+D₁)/P₀
│  │  ├─ 📐 Arithmetic mean = ΣRi/n（单期期望）
│  │  └─ 📐 Geometric mean = [(1+R₁)...(1+Rₙ)]^(1/n)-1（多期复合）
│  ├─ ⭐ 1.4 MWRR vs TWRR【高频】
│  │  ├─ MWRR = IRR（投资者体验）
│  │  ├─ TWRR = 子期间几何链接（经理能力）
│  │  └─ ⚠️ 客户资金进出扭曲 MWRR，不影响 TWRR
│  ├─ ⭐ 1.5 年化与连续复利
│  │  ├─ 📐 Annualized = (1+R_period)^c - 1
│  │  ├─ 📐 r_cc = ln(1+HPR)，FV = PV·e^(rt)
│  │  └─ ⚠️ r_cc 不是 (P₁-P₀)/P₀，是对数比价
│  ├─ ⭐ 1.6 Gross vs Net Return【高频】
│  │  └─ ⚠️ Gross 已含 trading expenses，Net = Gross - mgmt/admin fees
│  └─ ⭐ 1.7 Leveraged & After-Tax Return【高频】
│     ├─ 📐 Leveraged = Rp + (B/E)(Rp-rD)
│     ├─ 📐 After-tax = Pre-tax×(1-t)
│     └─ ⚠️ 计算顺序不可逆：Gross → Net → Leverage → Tax
│
├─ 🏆 M02: Time Value of Money（货币时间价值）── 再折现
│  ├─ ⭐ 2.1 现金流地图
│  │  ├─ 📐 FV = PV(1+r)^n，PV = FV/(1+r)^n
│  │  ├─ 📐 普通年金 PV = A[1-1/(1+r)^n]/r
│  │  ├─ 📐 永续年金 PV = A/r
│  │  └─ ⚠️ Annuity due = ordinary × (1+r)
│  ├─ ⭐ 2.2 工具现值应用：FI价格 = 票息PV + 本金PV，Equity = 股利PV
│  ├─ ⭐ 2.3 隐含变量：📐 r = D₁/P₀ + g（Gordon，Quant↔Equity 交叉口）
│  └─ ⭐ 2.4 现金流可加性：Portfolio PV = ΣComponent PV（无套利基础）
│
├─ 🏆 M03: Statistical Measures（统计量与分布特征）── 描述数据
│  ├─ ⭐ 3.1 集中趋势：算术/几何/调和平均、中位数、分位数
│  │  └─ ⚠️ outlier 对 mean 影响 > median
│  ├─ ⭐ 3.2 离散度
│  │  ├─ 📐 总体方差 = Σ(x-μ)²/n，样本方差 = Σ(x-x̄)²/(n-1)
│  │  ├─ 📐 CV = s/x̄（相对离散度）
│  │  └─ ⚠️ 样本方差分母是 n-1，不是 n
│  ├─ ⭐ 3.3 分布形态：偏度（长尾方向=偏态），峰度（肥尾=kurtosis↑）
│  └─ ⭐ 3.4 相关性直觉：符号=方向，大小=强度，⚠️ 相关≠因果
│
├─ 🏆 M04: Probability Concepts（概率基础）
│  ├─ ⭐ 4.1 期望值/方差：📐 E(X)=Σpᵢxᵢ，Var(X)=E(X²)-[E(X)]²
│  ├─ ⭐ 4.2 概率树：分支概率→终端收益→条件期望
│  └─ ⭐ 4.3 贝叶斯更新
│     ├─ 📐 P(A|B)=P(A∩B)/P(B)
│     ├─ 📐 P(Bj|A)=P(A|Bj)P(Bj)/ΣP(A|Bi)P(Bi)
│     └─ ⚠️ 后验 = 回完整分母，不只是 numerator
│
├─ 🏆 M05: Portfolio Mathematics（投资组合数学）── Portfolio / Quant 交叉口
│  ├─ ⭐ 5.1 组合收益与方差
│  │  ├─ 📐 E(Rp)=ΣwᵢE(Rᵢ)
│  │  └─ 📐 σp² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂Cov₁₂
│  ├─ ⭐ 5.2 联合概率
│  │  ├─ 📐 Cov₁₂ = Σp(R₁-ER₁)(R₂-ER₂)
│  │  └─ 📐 ρ₁₂ = Cov₁₂/(σ₁σ₂)
│  ├─ ⭐ 5.3 分散化：ρ↓→diversification benefit↑；⚠️ 低ρ≠负收益
│  └─ ⭐ 5.4 短缺风险：📐 Roy SFRatio = (E(Rp)-RL)/σp
│
├─ 🏆 M06: Simulation Methods（模拟方法）── 概念为主
│  ├─ ⭐ 6.1 对数正态分布：连续复利~正态 → 价格~对数正态
│  ├─ ⭐ 6.2 蒙特卡洛：Specify→Draw→Summarize；⚠️ 结果依赖输入假设
│  └─ ⭐ 6.3 自助法：有放回重抽；⚠️ inherit sample limitations
│
├─ 🏆 M07: Sampling and Estimation（抽样与估计）
│  ├─ ⭐ 7.1 抽样方法：概率抽样 vs 非概率抽样
│  ├─ ⭐ 7.2 CLT 与标准误
│  │  ├─ 📐 SE = σ/√n 或 s/√n
│  │  ├─ x̄ ~ N as n↑（不管总体分布）
│  │  └─ ⚠️ 大样本降 SE，不消灭 bad sampling design
│  └─ ⭐ 7.3 重抽样：Bootstrap（估标准误），Jackknife（估偏误，⚠️ 非去异常值）
│
├─ 🏆 M08: Hypothesis Testing（假设检验）── 检验框架核心
│  ├─ ⭐ 8.1 检验构件
│  │  ├─ H₀ vs H₁, α (Type I), β (Type II), Power = 1-β
│  │  ├─ 📐 z = (x̄-μ₀)/(σ/√n)；t = (x̄-μ₀)/(s/√n)
│  │  └─ ⚠️ p-value ≠ P(H₀|data)；fail to reject ≠ accept
│  ├─ ⭐ 8.2 参数 vs 非参数：非参数→序数数据/严重非正态/小样本
│  ├─ 🎯 8.3 双样本检验【重点】
│  │  ├─ Pooled t（等方差）：📐 sₚ²=[(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)，df=n₁+n₂-2
│  │  ├─ Unpooled t（不等方差）：📐 t=[(x̄₁-x̄₂)-d₀]/√(s₁²/n₁+s₂²/n₂)，df Satterthwaite
│  │  ├─ 配对比较 t：📐 t = d̄/(sd/√n)，⚠️ df = n-1（n=对数，不是 n₁+n₂-2）
│  │  ├─ F检验（方差齐性）：📐 F = s₁²/s₂²，df₁=n₁-1, df₂=n₂-1
│  │  └─ 双样本比例 z：📐 z=(p̂₁-p̂₂)/√[p̂(1-p̂)(1/n₁+1/n₂)]
│  └─ ⭐ 8.4 卡方方差检验：📐 χ²=(n-1)s²/σ₀²，df=n-1；⚠️ 对正态极其敏感
│
├─ 🏆 M09: Tests of Independence（独立性检验）
│  ├─ ⭐ 9.1 相关系数检验：📐 t=r√[(n-2)/(1-r²)]，df=n-2；Spearman（非参数）
│  └─ ⭐ 9.2 列联表独立性：📐 χ²=Σ[(O-E)²/E]，df=(r-1)(c-1)
│
├─ 🏆 M10: Simple Linear Regression（简单线性回归）
│  ├─ ⭐ 10.1 回归模型：📐 Yᵢ=b₀+b₁Xᵢ+eᵢ，📐 b₁=Cov(X,Y)/Var(X)
│  ├─ ⭐ 10.2 假设检验：线性/同方差/独立/正态，残差图检测
│  ├─ 🎯 10.3 拟合与推断
│  │  ├─ 📐 R²=SSR/SST，📐 SEE=√[SSE/(n-2)]
│  │  ├─ 📐 t=(b₁-β₁,₀)/SE(b₁)；📐 F=MSR/MSE
│  │  └─ ⚠️ prediction interval > point estimate uncertainty
│  └─ ⭐ 10.4 函数形式：Log-lin / lin-log / log-log → 弹性解释
│
└─ 🏆 M11: Big Data & ML（大数据与机器学习）── 概念
   ├─ ⭐ 11.1 Fintech 数据采集与处理
   ├─ ⭐ 11.2 Big Data / AI / ML 辨析
   └─ ⚠️ 11.3 Model sophistication ≠ validation & governance
```

---

## 🔄 跨模块依赖关系（学习顺序图）

```text
📊 学习起点 ─── 先建立"现金流"思维
│
M01 Returns ◄────────────────► M02 TVM
│  （统一收益口径）              （折现工具）
└──► M03 Statistical Measures ◄── 描述数据特征
     │
     ├──► M04 Probability ◄──── 概率基础
     │    │
     │    └──► M05 Portfolio Math ──► Portfolio Management M01-M02
     │           （Quant 与 PM 的交叉口）
     │
     └──► M07 Sampling & Estimation
          │
          └──► M08 Hypothesis Testing ──► 所有含"检验"的模块
               │
               ├──► M09 Tests of Independence
               │
               └──► M10 Regression ──► 跨科目：Economics / Equity 估值
                    │
                    └──► M11 Big Data & ML（扩展应用）

🔗 跨科目关键接口：
  M02 Gordon r = D₁/P₀+g ──► Equity M08 估值
  M05 组合方差 ──► Portfolio Management M01-M02
  M10 回归 ──► Economics 模型 / Equity 预测
  M08 假设检验 ──► 几乎所有含统计推断的模块
```

### 🔗 各模块详细跨模引用

| 本模块 | 依赖前置 | 提供基础给 |
|--------|----------|-----------|
| **M01** | 无 | M02（折现率概念）、M06（连续复利）、PM M01 |
| **M02** | M01（折现率） | Equity M08（GGM）、FI M06（定价）、Deriv M05 |
| **M03** | 无 | M04-M05-M07（统计基础） |
| **M04** | M03（概率分布） | M05（概率加权）、M08（p-value） |
| **M05** | M03-M04 | **PM M01-M02**（组合理论核心输入） |
| **M06** | M01（连续复利） | 模拟分析基础 |
| **M07** | M03 | **M08-M10**（统计推断基础） |
| **M08** | M07 | **所有含检验的模块** |
| **M09** | M08（检验框架） | — |
| **M10** | M07-M08 | Economics / Equity / FI 回归应用 |
| **M11** | — | 扩展了解 |

---

## 🔑 核心对比专题

| 对比项 | 🔑 关键区别 | 🎯 考试判断 |
|--------|-------------|-------------|
| **MWRR vs TWRR** | 投资者体验 vs 经理能力 | 有现金流→评估经理→TWRR；评估投资者→MWRR |
| **Arithmetic vs Geometric** | 单期平均 vs 多期复合 | 多期财富增长→Geometric |
| **Sample vs Pop Variance** | n-1 vs n | 用样本估总体→n-1 |
| **z-test vs t-test** | σ已知 vs σ未知 | 看到 σ→z，s→t |
| **Pooled vs Unpooled** | 假设等方差 vs 不等 | "equal variances"→Pooled |
| **配对 df ≠ 独立 df** | n-1 vs n₁+n₂-2 | 配对样本→df=n-1 |
| **F-test vs χ²-test** | 两方差比较 vs 单方差 | 比两个→F；比一个→χ² |
| **相关 ≠ 因果** | 关系强度 vs 因果 | 任何涉及因果的结论都要怀疑 |
| **R² 高 ≠ 模型好** | 拟合度 vs 显著性 | 还要看 F/t 检验、经济意义 |

---

## 📐 核心公式速查

### M01-M02 收益率与 TVM

| 指标 | 📐 公式 | ⚠️ 注意 |
|------|---------|---------|
| HPR | `(P₁-P₀+D₁)/P₀` | 最基础 |
| Geometric Mean | `[(1+R₁)...(1+Rₙ)]^(1/n)-1` | 多期复合 |
| r_cc | `ln(1+HPR)` | 对数比价，不是简单差 |
| MWRR | `0=ΣCFt/(1+r)^t` | 实质是 IRR |
| TWRR | `[(1+HP₁)...(1+HPₙ)]-1` | 子期间几何链接 |
| FV | `PV(1+r)^n` | TVM 基石 |
| Ordinary Annuity PV | `A[1-1/(1+r)^n]/r` | 固定期末现金流 |
| Perpetuity PV | `A/r` | 高频快算 |

### M03-M05 统计·概率·组合

| 指标 | 📐 公式 | ⚠️ 注意 |
|------|---------|---------|
| Sample Variance | `Σ(x-x̄)²/(n-1)` |  n-1 |
| CV | `s/x̄` | 相对离散 |
| E(X) | `Σpᵢxᵢ` | 概率加权 |
| Bayes | `P(Bj|A)=P(A|Bj)P(Bj)/ΣP(A|Bi)P(Bi)` | 新信息更新 |
| Portfolio Variance | `σp²=w₁²σ₁²+w₂²σ₂²+2w₁w₂Cov₁₂` | 双资产常考 |
| Safety-First | `(E(Rp)-RL)/σp` | 选最高者 |

### M07-M08 抽样与检验

| 指标 | 📐 公式 | ⚠️ 注意 |
|------|---------|---------|
| SE | `σ/√n` 或 `s/√n` | 抽样核心 |
| CI (σ未知) | `x̄ ± t_(α/2,n-1)·s/√n` | 最常见 |
| Pooled sp² | `[(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2)` | 等方差双样本 |
| 配对 t | `d̄/(sd/√n)` | ⚠️ df=n-1 |
| F-test | `s₁²/s₂²` | df₁=n₁-1, df₂=n₂-1 |
| χ²-test | `(n-1)s²/σ₀²` | ⚠️ 极敏感正态 |

### M09-M10 回归与独立性

| 指标 | 📐 公式 | ⚠️ 注意 |
|------|---------|---------|
| Correlation t | `r√[(n-2)/(1-r²)]` | df=n-2 |
| Chi-square (indep.) | `Σ[(O-E)²/E]` | df=(r-1)(c-1) |
| R² | `SSR/SST` | 拟合度 |
| SEE | `√[SSE/(n-2)]` | 残差尺度 |
| Slope t | `(b₁-β₁,₀)/SE(b₁)` | 检验显著 |
| F-stat | `MSR/MSE` | 整体显著 |

---

## 🚨 高频考试陷阱速查

| ❌ 错误理解 | ✅ 正确理解 | 🎯 容易出现的题 |
|-------------|-------------|----------------|
| Arithmetic = 长期收益 | 长期→Geometric | 多期收益率 |
| MWRR = TWRR | MWRR看现金流，TWRR看经理 | 业绩评估选哪个 |
| Annuity due = ordinary | Due多乘(1+r) | 年金现值计算 |
| Sample var分母=n | n-1 | 方差计算 |
| p-value = P(H₀) | H₀下样本极端概率 | p-value 解读 |
| Fail to reject = 接受 | 只是证据不足 | 假设检验结论 |
| 配对检验 df=n₁+n₂-2 | df=n-1 | 自由度判断 |
| Pooled/unpooled 随便选 | 等方差→pooled | 双样本t检验 |
| χ²=独立性检验 | 单方差也用χ²（M08） | 卡方应用范围 |
| 相关=因果 | 相关≠因果 | 回归结论判断 |
| R²高=模型好 | 还要看显著性和经济意义 | 回归评价 |
| Gross不含交易费 | 已含 | 收益率计算 |

---

## 💡 通用分析框架

### 框架1：收益率决策树
```
有中途现金流？──→ No ──→ HPR 即可
        │
        └──→ Yes ──→ 评估 investor experience → MWRR
                    └── 评估 manager performance → TWRR
多期复合回报 → Geometric Mean
```

### 框架2：统计推断决策树
```
估计还是检验？──→ 估计 → point estimate 或 confidence interval
        │
        └──→ 检验 → 写 H₀/H₁ → σ已知？→ z / t → 查表得结论
```

### 框架3：检验方法选择决策树
```
单样本 → 均值→ z/t；方差→ χ²
双样本 ─→ 独立 → 均值→ 等方差→Pooled / 不等→Unpooled
       │        方差→ F-test
       └── 配对 → 均值→ 配对 t (df=n-1)
比例 → z 检验
```

---

## 🗺️ 学习路径建议

```
阶段1（理解主干）：M01 → M02 → M03 → M07 → M08 → M10
  先建立"收益率→TVM→统计→抽样→检验→回归"主线

阶段2（填空补细节）：M04 → M05 → M06 → M09 → M11
  概率→组合数学→模拟→独立性→ML概念

阶段3（刷题反查）：按做题错题定位到对应公式和陷阱
```
