---
title: "M01 — Rates and Returns"
description: 收益率与回报 — HPR, MWRR, TWRR, 年化收益率, 连续复利
module: M01
subject: Quantitative_Methods
---

# M01: Rates and Returns（收益率与回报）

## 1. 核心知识点

### 1.1 利率的三种解释（Three Interpretations of Interest Rate）

利率（Interest Rate）在 CFA 考试中有三种等价解释：

- **要求回报率（Required Rate of Return）**：投资者投资所要求的最低回报率，包含机会成本和风险补偿。
- **折现率（Discount Rate）**：将未来现金流折算为现值的比率，反映货币的时间价值。
- **机会成本（Opportunity Cost）**：选择某一投资而放弃次优选择所损失的潜在收益。

这三种解释相通 — 折现率就是投资者对该投资的要求回报率，也就是放弃其他机会的成本。

### 1.2 利率分解（Interest Rate Decomposition）

名义利率可分解为多个组成部分：

`名义利率 ≈ 实际无风险利率 + 预期通胀溢价 + 违约风险溢价 + 流动性风险溢价 + 期限风险溢价 + 其他风险溢价`

- **实际无风险利率（Real Risk-Free Rate）**：无通胀、无风险环境下的纯粹时间价值，通常用短期国债实际收益率近似。
- **预期通胀溢价（Expected Inflation Premium）**：补偿投资者预期购买力下降的溢价。
- **违约风险溢价（Default Risk Premium）**：补偿发行人可能违约的风险。
- **流动性风险溢价（Liquidity Risk Premium）**：补偿资产难以快速变现的流动性风险。
- **期限风险溢价（Maturity Risk Premium）**：补偿长期债券的利率风险。

> **【考试核心】** 高名义利率可能来自高通胀，也可能来自高违约风险或低流动性，不能简单归因于单一因素。

### 1.3 收益率度量阶梯（Return Measurement Ladder）

**持有期收益率（Holding Period Return, HPR）**：
`HPR = (P_1 - P_0 + D_1) / P_0`

HPR 是基础收益率度量，不考虑投资期限长短，直接计算整个持有期的总回报比率。

**算术平均收益率（Arithmetic Mean Return）**：
`Arithmetic Mean = (R_1 + R_2 + ... + R_n) / n`

适用于估计单期预期收益（Expected Return），但会高估多期复合财富增长。

**几何平均收益率（Geometric Mean Return）**：
`Geometric Mean = [(1 + R_1)(1 + R_2)...(1 + R_n)]^(1/n) - 1`

适用于衡量多期复合增长。几何平均始终小于或等于算术平均，差异越大说明收益率波动越大。

**调和平均（Harmonic Mean）**：适用于价格倍数（Price Multiple）的平均，如平均市盈率（P/E）计算，因为调和平均对极端值更不敏感。

### 1.4 MWRR vs TWRR

**资金加权收益率（Money-Weighted Rate of Return, MWRR）**本质上是投资组合的内部收益率（IRR），对现金流进出时点敏感。MWRR 衡量的是**投资者实际体验** — 相同投资组合业绩下，在不同时点追加或赎回资金的投资者会得到不同的 MWRR。

**时间加权收益率（Time-Weighted Rate of Return, TWRR）**通过在每个现金流进出时点将投资组合拆分为子期间，将各子期间收益率几何链接起来。TWRR 衡量的是**基金经理的投资管理能力**，不受投资者现金流决策的影响。

> **【考试陷阱】** 当客户在业绩差的时候追加资金、业绩好的时候赎回资金时，MWRR 会显著低于 TWRR，这不代表基金经理表现差。

### 1.5 年化与连续复利（Annualization and Continuous Compounding）

**年化收益率（Annualized Return）**：
`Annualized Return = (1 + R_period)^c - 1`
其中 c 是一年内的期数。例如月度收益率年化时 c = 12。

**连续复利收益率（Continuously Compounded Return）**：
`r_cc = ln(1 + HPR)`

连续复利收益率的最大优势是**可加性（Additivity）**：多期连续复利收益率可以直接相加，而普通收益率必须用乘法链接。

**连续复利的终值与现值**：
- `FV = PV * e^(rt)`
- `PV = FV * e^(-rt)`

> **【考试核心】** 当题目所给利率是连续复利口径时，必须使用 e^(rt) 而不是 (1+r)^n。

### 1.6 总回报 vs 净回报（Gross Return vs Net Return）

- **总回报（Gross Return）**：`(P_1 + D_1) / P_0 = 1 + HPR`，已在价格中扣除交易费用（Trading Expenses），但不扣除管理费和行政费。
- **净回报（Net Return）**：`Gross Return - Management/Admin Fees`，投资者实际到手的回报。

> **【考试陷阱】** Gross Return 已经包含了交易费用（Trading Expenses），不需要再额外扣除交易费用！净回报只额外扣除管理费和行政费。

### 1.7 杠杆与税后回报（Leveraged and After-Tax Return）

**杠杆回报（Leveraged Return）**：
`Leveraged Return = R_p + (B/E)(R_p - r_D)`
- B = 借款额
- E = 自有本金
- r_D = 借款利率

**税后回报（After-Tax Return）**：
`After-Tax Return = Pre-tax Return × (1 - t)`
- t = 税率

> **【考试陷阱】** 计算顺序至关重要：**Gross Return → Net Return → Leveraged Return → After-Tax Return**。不可以先扣税再算杠杆。

## 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `HPR = (P_1 - P_0 + D_1) / P_0` | 持有期收益率 | 衡量单一持有期的总回报 |
| `Arithmetic Mean = ΣR_i / n` | 算术平均收益率 | 估计单期预期收益 |
| `Geometric Mean = [(1+R_1)...(1+R_n)]^(1/n) - 1` | 几何平均收益率 | 衡量多期复合增长 |
| `Annualized Return = (1 + R_period)^c - 1` | 年化收益率 | 将期间收益率转化为年化口径 |
| `r_cc = ln(1 + HPR)` | 连续复利收益率 | 需要收益率可加性时使用 |
| `MWRR: Σ CF_t / (1+r)^t = 0` | 资金加权收益率 | 评估投资者实际体验 |
| `Compounded TWRR = ∏(1 + HP_i) - 1` | 复合时间加权收益率 | 评估基金经理表现 |
| `FY = PV * e^(rt)` | 连续复利终值 | 连续复利条件下的终值计算 |
| `Leveraged Return = R_p + (B/E)(R_p - r_D)` | 杠杆回报 | 借款投资时的回报计算 |
| `After-Tax Return = Pre-tax × (1 - t)` | 税后回报 | 考虑税收后的净回报 |

## 3. 常见考点与解题思路

**考点一：计算 HPR 并区分其组成部分**
- 给定期初价格、期末价格和期间收入（股息/利息），直接代入 HPR 公式
- 注意区分 Gross Return 和 HPR 的关系：Gross Return = 1 + HPR

**考点二：选择 arithmetic mean vs geometric mean**
- 给多个历史收益率，要比较累计增长 → 用 Geometric Mean
- 给概率分布，求 expected return → 用 Arithmetic Mean
- 给一系列历史收益率求平均 → 先判断题目问的是 expected return 还是 past growth

**考点三：MWRR vs TWRR 计算与比较**
- MWRR 用 IRR 计算，将所有现金流（初始投资、追加/赎回、最终价值）代入解 r
- TWRR 先分段计算子期间 HPR，再几何链接
- 考试中可能要求比较两者大小关系并解释原因

**考点四：年化收益率计算**
- 给定期间收益率，用 `(1 + R)^c - 1` 年化
- 注意区分"年化收益率"和"有效年利率（EAR）"的等价性

## 4. 易错点提醒

1. **Gross Return 含 trading expenses 不含 mgmt fees**：Gross Return 已经扣除了交易费用，计算 Net Return 时只额外扣除管理费和行政费。
2. **顺序不可逆**：Leverage 和 Tax 的计算顺序为 Gross → Net → Leverage → Tax。
3. **MWRR 受现金流影响**：MWRR 低不代表经理表现差，可能只是客户在低点赎回。
4. **连续复利用 e 不用 (1+r)^n**：题目给连续复利利率时，必须用指数函数。
5. **Harmonic Mean 的特殊用途**：计算平均价格倍数（如平均 P/E）时要用调和平均。
6. **几何平均 ≤ 算术平均**：两者差距反映波动率，差距越大说明波动越大。

## 5. 跨模块关联

- **[[M02-Time-Value-of-Money]]**：TVM 是 HPR 和 MWRR（本质就是 IRR）的基础。MWRR = 0 = ΣCF/(1+r)^t 正是 TVM 的反向应用。
- **[[M03-Statistical-Measures]]**：三种均值（算术/几何/调和）在此首次出现，在 M03 中会进一步展开为 general 统计量。
- **[[M05-Portfolio-Mathematics]]**：杠杆回报公式是 Portfolio return 的延伸，组合方差中的权重逻辑也在此预热。
- **M07**：年化收益率涉及的"periodicity 转换"与 EAR 概念在固收中也反复出现。
