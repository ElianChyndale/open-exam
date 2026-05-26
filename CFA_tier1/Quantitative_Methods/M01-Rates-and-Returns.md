---
title: "M01 — Rates and Returns"
description: "CFA Level I 2026 official module: Rates and Returns"
module: M01
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 1: Rates and Returns"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M01: Rates and Returns

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Rates and Returns
- 1.01 | Introduction
- 1.02 | Interest Rates and Time Value of Money
- 1.03 | Rates of Return
- 1.04 | Money-Weighted and Time-Weighted Return
- 1.05 | Annualized Return
- 1.06 | Other Major Return Measures and Their Applications

## Learning Outcome Statements

The candidate should be able to:

- interpret interest rates as required rates of return, discount rates, or opportunity costs and explain an interest rate as the sum of a real risk-free rate and premiums that compensate investors for bearing distinct types of risk
- calculate and interpret different approaches to return measurement over time and describe their appropriate uses
- compare the money-weighted and time-weighted rates of return and evaluate the performance of portfolios based on these measures
- calculate and interpret annualized return measures and continuously compounded returns, and describe their appropriate uses
- calculate and interpret major return measures and describe their appropriate uses

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M01: Rates and Returns（收益率与回报）
│
├── ⭐ 利率的三种解释 (Three Interpretations)
│   ├── 要求回报率 (Required Rate of Return)：投资者要求的最低回报
│   ├── 折现率 (Discount Rate)：将未来现金流折算为现值
│   └── 机会成本 (Opportunity Cost)：放弃次优选择的成本
│
├── ⭐ 利率分解 (Interest Rate Decomposition)
│   ├── 名义利率 ≈ 实际无风险利率 + 预期通胀溢价 + 违约风险溢价 + 流动性风险溢价 + 期限风险溢价
│   ├── 📐 实际无风险利率 = 短期国债实际收益率
│   └── 🎯 高名义利率可能来自高通胀、高违约风险或低流动性，不能简单归因于单一因素
│
├── ⭐ 收益率度量阶梯 (Return Measurement Ladder)
│   ├── 📐 HPR = (P₁ - P₀ + D₁) / P₀
│   ├── 📐 算术平均 = ΣRᵢ / n — 估计单期预期收益
│   ├── 📐 几何平均 = [Π(1+Rᵢ)]^(1/n) - 1 — 衡量多期复合增长
│   ├── 📐 调和平均 = n / Σ(1/xᵢ) — 平均价格倍数专用
│   └── ⚠️ 几何平均 ≤ 算术平均，差距越大说明波动越大
│
├── ⭐ MWRR vs TWRR
│   ├── MWRR = IRR，对现金流时点敏感 → 衡量投资者实际体验
│   ├── TWRR 分段计算子期间 HPR 再几何链接 → 衡量基金经理管理能力
│   └── ⚠️ 客户在低点赎回收高点追入 → MWRR 显著低于 TWRR
│
├── ⭐ 年化与连续复利 (Annualization & Continuous Compounding)
│   ├── 📐 年化收益率 = (1 + R_period)^c - 1
│   ├── 📐 连续复利 r_cc = ln(1 + HPR) — 可加性是最大优势
│   ├── 📐 FV = PV × e^(rt), PV = FV × e^(-rt)
│   └── ⚠️ 连续复利必须用 e^(rt)，不是 (1+r)^n
│
├── ⭐ Gross Return vs Net Return
│   ├── Gross Return = 1+HPR，已含 trading expenses
│   └── Net Return = Gross Return - Management/Admin Fees
│
├── ⭐ 杠杆与税后回报
│   ├── 📐 杠杆回报 = R_p + (B/E)(R_p - r_D)
│   ├── 📐 税后回报 = 税前回报 × (1 - t)
│   └── ⚠️ 顺序：Gross → Net → Leverage → Tax，不可逆
│
├── 💡 关键洞察
│   ├── 利率的三种解释相通 — 折现率 = 要求回报率 = 机会成本
│   ├── Geometric Mean 是衡量历史复合增长的唯一正确指标
│   ├── TWRR 消除了现金流决策的影响，是基金业绩评价的标准方法
│   └── 连续复利的多期可加性在大数据分析中优势明显
│
└── ⚠️ 考试陷阱总结
    ├── Gross Return 已含 trading expenses，不重复扣除
    ├── 计算顺序 Gross → Net → Leverage → Tax — 不可逆
    ├── MWRR 衡量投资者体验，TWRR 衡量经理能力 — 不要混淆评价对象
    ├── 连续复利必须用 ln() 和 e^()
    └── Harmonic Mean 用于平均价格倍数（如 P/E）
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `HPR = (P_1 - P_0 + D_1) / P_0` | 持有期收益率 | 衡量单一持有期总回报 | 不含 management fees；包含期间收入 |
| `算术平均 = ΣR_i / n` | 算术平均收益率 | 估计单期预期收益 | 高估多期复合增长 |
| `几何平均 = [Π(1+R_i)]^(1/n) - 1` | 几何平均收益率 | 多期复合增长衡量 | 几何平均 ≤ 算术平均 |
| `年化收益率 = (1 + R_period)^c - 1` | 年化收益率 | 期间→年化转化 | c 是一年内期数 |
| `r_cc = ln(1 + HPR)` | 连续复利收益率 | 需要可加性时 | 必须用 ln()，不是简单除法 |
| `MWRR: ΣCF_t/(1+r)^t = 0` | 资金加权收益率 | 投资者实际体验 | 本质是 IRR，对现金流时点敏感 |
| `TWRR = Π(1+HP_i) - 1` | 时间加权收益率 | 基金经理表现 | 分段 HPR 几何链接 |
| `FV = PV × e^(rt)` | 连续复利终值 | 连续复利金融建模 | 配合 r_cc 使用，不用 (1+r)^n |
| `杠杆回报 = R_p + (B/E)(R_p - r_D)` | 杠杆回报 | 借款投资决策 | B=借款额，E=自有本金 |
| `税后回报 = 税前 × (1 - t)` | 税后回报 | 考虑税收后的净回报 | 在杠杆回报基础上计算 |

### 🛠️ 常见考点与解题思路

**考点1：HPR 计算与组成部分区分**
- 步骤 1：确认期初价格 P₀、期末价格 P₁、期间收入 D₁
- 步骤 2：代入 HPR = (P₁ - P₀ + D₁) / P₀
- 步骤 3：若问 Gross Return = 1 + HPR
- ⚠️ 不要混淆 Gross Return 与 HPR

**考点2：算术平均 vs 几何平均的选择**
- 给多个历史收益率要比较累计增长 → 几何平均
- 给概率分布求 expected return → 算术平均
- 给历史收益率但不指明 → 先判断题目问 expected return 还是 past growth
- ⚠️ 几何平均始终 ≤ 算术平均

**考点3：利率分解分析**
- 名义利率 = 实际无风险利率 + 预期通胀溢价 + 违约风险溢价 + 流动性风险溢价 + 期限风险溢价
- 给定两种不同债券的收益率 → 分析差异来源
  - 国债 vs 公司债 → 差异主要来自违约风险溢价
  - 短债 vs 长债 → 差异主要来自期限风险溢价
  - 上市股票 vs 非上市股权 → 差异包含流动性风险溢价
- ⚠️ 高名义利率可能是高通胀、高违约风险或低流动性的综合结果

**考点4：MWRR vs TWRR 计算与比较**
- MWRR：列出所有现金流（含追加/赎回）解 IRR
  - 本质 = TVM 反向求解：ΣCF_t/(1+r)^t = 0
  - 对现金流进出时点敏感 → 衡量投资者实际体验
- TWRR：在每次现金流进出时点分段 → 算各段 HPR → 几何链接
  - 消除现金流决策影响 → 衡量基金经理管理能力
- 比较规则：
  - 若客户在差业绩时追加、好业绩时赎回 → MWRR < TWRR
  - 若客户在好业绩时追加、差业绩时赎回 → MWRR > TWRR
- ⚠️ MWRR 低不代表基金经理差 — 可能是客户现金流时点导致的

**考点5：年化收益率与连续复利**
- 给定期间收益率 → 年化用 (1+R)^c - 1 (c = 一年内期数)
- 给定 HPR → 连续复利用 r_cc = ln(1+HPR)
- 连续复利终值用 FV = PV × e^(rt)
- 连续复利的可加性: 多期 r_cc 直接相加，普通收益率需乘法链接
- ⚠️ 连续复利与非连续复利的终值公式本质不同，不要混用
- 💡 EAR = (1 + r_nom/m)^m - 1 与年化收益率公式等价

**考点6：Gross → Net → Leverage → Tax 顺序**
- Step 1: Gross Return = (P₁ + D₁) / P₀（已含 trading expenses）
- Step 2: Net Return = Gross Return - Mgmt/Admin Fees
- Step 3: Leveraged Return = Net Return + (B/E)(Net Return - r_D)
- Step 4: After-Tax Return = Leveraged Return × (1 - t)
- ⚠️ 最大错误：在 Gross 阶段多减 trading expenses，或在 Leverage 前扣税
- ⚠️ Gross Return 已含交易费用，Net Return 只减管理费和行政费
- ⚠️ 顺序不可逆 — 先杠杆后税，不是先税后杠杆

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| Gross Return 不含任何费用 | Gross Return 已含 trading expenses，只另减 mgmt/admin fees | Trading expenses 直接贡献于价格回报 |
| 可以先在 Gross Return 中减 trading expenses 再算 Net Return | Trading expenses 已在 Gross Return 中反映，不可重复扣除 | 重复扣减会低估收益率 |
| Leverage 和 Tax 可以任意顺序计算 | 严格：Gross → Net → Leverage → Tax | 杠杆基于净回报，税收基于杠杆后回报 |
| MWRR 低 = 基金经理表现差 | MWRR 衡量投资者体验，TWRR 衡量经理能力 | MWRR 受现金流时点扰动 |
| 连续复利可用 (1+r)^n 计算终值 | 连续复利必须用 e^(rt) | 连续复利假设无间断复利 |
| Harmonic Mean 用于一般收益率平均 | Harmonic Mean 仅用于平均价格倍数 | 调和平均对极端值最不敏感 |

### 🔄 跨模块关联

- **[[M02-Time-Value-of-Money-in-Finance]]** — TVM 是 HPR 和 MWRR（本质就是 IRR）的基础。MWRR = ΣCF/(1+r)^t = 0 正是 TVM 的反向应用。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 三种均值（算术/几何/调和）在此首次出现，在 M03 中进一步展开为一般统计量。
- **[[M05-Portfolio-Mathematics]]** — 杠杆回报公式是 Portfolio return 的延伸，组合方差中的权重逻辑在此预热。
- **[[M07-Estimation-and-Inference]]** — 年化收益率的 periodicity 转换与标准误中样本量计算有相通概念。

### 📋 复习与刷题提示

- **核心能力**：熟练区分 MWRR 与 TWRR 的应用场景，掌握多步计算顺序（Gross→Net→Leverage→Tax）
- **必考题型**：HPR 计算、几何/算术平均选择、MWRR/TWRR 判别、连续复利终值计算
- **最常犯错误**：连续复利用错公式、Gross Return 重复减 trading expenses、顺序记错
- 记忆口诀：
  - 利率三维度：回报率、折现率、机会成本 — 互通
  - 平均三兄弟：算术最大，几何居中，调和最小
  - 连续复利：HPR 取 ln，终值用 e
- 刷题建议：重点做包含多步计算的题目（Gross→Net→Leverage→Tax），这是 CFA 高频综合题
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
