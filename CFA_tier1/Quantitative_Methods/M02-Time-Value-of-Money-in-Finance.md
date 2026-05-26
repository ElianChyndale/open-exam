---
title: "M02 — Time Value of Money in Finance"
description: "CFA Level I 2026 official module: Time Value of Money in Finance"
module: M02
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 2: Time Value of Money in Finance"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M02: Time Value of Money in Finance

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Time Value of Money in Finance
- 2.01 | Introduction
- 2.02 | Time Value of Money in Fixed Income and Equity
- 2.03 | Implied Return and Growth
- 2.04 | Cash Flow Additivity

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret the present value (PV) of fixed-income and equity instruments based on expected future cash flows
- calculate and interpret the implied return of fixed-income instruments and required return and implied growth of equity instruments given the present value (PV) and cash flows
- explain the cash flow additivity principle, its importance for the no-arbitrage condition, and its use in calculating implied forward interest rates, forward exchange rates, and option values

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M02: Time Value of Money in Finance（货币时间价值）
│
├── ⭐ 现金流时间轴 (Cash-Flow Map)
│   ├── 📐 FV = PV × (1 + r)^n — TVM 核心关系
│   ├── 四种基本模式：单笔、等额年金、永续年金、增长现金流
│   ├── 先付年金 (Annuity Due)：期初支付 = 普通年金 × (1+r)
│   └── ⚠️ 先画时间轴，再选公式，不要一上来就套公式
│
├── ⭐ 四种基本现金流模式 (Four Cash Flow Patterns)
│   ├── Single Sum — 最简单，直接代入 FV/PV 公式
│   ├── 📐 Ordinary Annuity: PV = A[1 - 1/(1+r)^n] / r
│   ├── 📐 Perpetuity: PV = A / r — 分子必须是第一期现金流
│   ├── 📐 Growing Perpetuity: PV = A₁/(r-g) — 要求 r > g
│   └── 📐 Growing Annuity: PV = A₁/(r-g)[1 - ((1+g)/(1+r))^n]
│
├── ⭐ 工具现值应用 (Instrument PV Applications)
│   ├── Fixed Income：债券价格 = 票息年金现值 + 本金现值
│   ├── Equity：股票价值 = 未来股利现值 (DDM)
│   └── 🎯 先识别现金流时点和模式，再选公式
│
├── ⭐ 隐含变量求解 (Implied Quantities)
│   ├── 📐 戈登增长模型: r = D₁/P₀ + g
│   ├── 已知 PV, FV, PMT, n 中任意三个 → 反求第四个
│   ├── 债券 → 反求 YTM；股权 → 反求要求回报率
│   └── 🎯 高频考点：用金融计算器反向求解
│
├── ⭐ 现金流可加性 (Cash-Flow Additivity)
│   ├── 组合现值 = 各组成部分现值之和
│   ├── 是套利定价和无套利条件的基础
│   └── ⚠️ 多个现金流序列 → 分别折现再加总，不是单一公式
│
├── 💡 关键洞察
│   ├── TVM 是所有资产定价的共同基础 — 债券、股票、衍生品
│   ├── 先付年金 = 普通年金 × (1+r) — 记住这个简单倍数关系
│   ├── Perpetuity 公式是从年金公式取 n→∞ 的极限
│   └── Cash-flow additivity 是无套利定价的数学基础
│
└── ⚠️ 考试陷阱总结
    ├── Perpetuity 分子必须是第一期现金流 A₁，不是 A₀
    ├── Growing perpetuity 必须满足 r > g
    ├── 计息频率与支付频率不一致 → 先统一利率口径
    └── 画时间轴是最好的纠错方法
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `FV = PV(1+r)^n` | 终值公式 | 单笔投资未来价值 | r 和 n 必须同频率 |
| `PV = FV/(1+r)^n` | 现值公式 | 未来单笔现金流折现 | 折现率与期数匹配 |
| `PV_annuity = A[1-1/(1+r)^n]/r` | 普通年金现值 | 等额分期现金流 | 确认是期末支付 |
| `PV_annuity_due = PV_ordinary × (1+r)` | 先付年金现值 | 期初支付场景(房租/保费) | 比普通年金多乘 (1+r) |
| `PV_perpetuity = A/r` | 永续年金现值 | 永续债券、优先股 | 分子用 A₁ |
| `PV_growing_perpetuity = A₁/(r-g)` | 永续增长年金 | DDM 股利折现模型 | 必须 r > g |
| `PV_growing_annuity = A₁/(r-g)[1-((1+g)/(1+r))^n]` | 增长年金现值 | 有限期增长现金流 | g 可为 0 → 退化为普通年金 |
| `r = D₁/P₀ + g` | 戈登增长模型 | 从股价反推要求回报率 | 股利增长率恒定的假设 |
| `EAR = (1 + r_nom/m)^m - 1` | 有效年利率 | 比较不同计息频率 | m = 年复利次数 |

### 🛠️ 常见考点与解题思路

**考点1：现金流模式识别与分类（第一步最关键）**
- 步骤 1：画现金流时间轴 — 将每个现金流标注在时间轴上
- 步骤 2：判断支付时点 — 期初 = Annuity Due，期末 = Ordinary Annuity
- 步骤 3：判断期限 — 有限期 = Annuity，无限期 = Perpetuity
- 步骤 4：是否有增长 — 有增长 = Growing Annuity/Perpetuity
- 步骤 5：代入对应公式，注意 r 与 n 的频率一致
- ⚠️ 最常见错误：不画时间轴直接套公式；把 Annuity Due 当 Ordinary Annuity
- 💡 时间轴是 TVM 问题最有效的纠错工具

**考点2：隐含利率反推（金融计算器必会）**
- 已知：贷款额 (PV)、月还款额 (PMT)、期数 (n)
- 金融计算器操作：输入 PV, PMT, n, FV=0 → 求解 I/Y
- 解出的是每期利率（如月利率），需年化
- 年化方法：名义年利率 = 月利率 × 12；EAR = (1+月利率)^12 - 1
- 戈登增长模型反推: r = D₁/P₀ + g (已知股价、股利、增长率求回报率)
- ⚠️ 注意还款频率 vs 计息频率的匹配 — 先统一再计算

**考点3：不同计息频率比较与 EAR 计算**
- 公式：EAR = (1 + r_nominal/m)^m - 1，m = 年复利次数
- 计息频率越高 → EAR 越高（但增速递减）
- 极端情况 — 连续复利: EAR = e^r - 1 (m → ∞)
- 💡 EAR 用于比较不同计息频率下的真实年化收益率
- ⚠️ 复利次数不同时不能直接比较名义利率，必须统一到 EAR

**考点4：债券定价 (TVM 在固收中的直接应用)**
- 债券价格 = 未来各期票息的年金现值 + 到期本金的单笔现值
- 票息 = 面值 × 票面利率 / 年付息次数
- 半年付息的处理: 周期利率 = r/2，期数 = 2n
- 到期收益率 (YTM) 是使债券价格等于现金流现值的折现率
- ⚠️ 最易错：半年付息但不用 r/2 和 2n；或混淆票面利率和 YTM

**考点5：现金流可加性 (Cash Flow Additivity) 的应用**
- 原则：一个投资组合的现值 = 各组成部分现值的和
- 应用场景：
  - 混合现金流 → 分别折现再加总
  - 远期利率计算 (利用不同期限债券价格)
  - 套利定价中的无套利条件
- ⚠️ 不要试图找"统一公式" — 逐一处理各子序列才是正确思路
- 💡 这是无套利定价的数学基础 — 同一现金流不应因拆分方式不同而得到不同现值

**考点6：先付年金 vs 普通年金转换**
- Annuity Due PV = Ordinary Annuity PV × (1+r)
- Annuity Due FV = Ordinary Annuity FV × (1+r)
- 核心逻辑：先付年金每笔付款早了一个计息期
- ⚠️ 考试中常见陷阱：模糊描述支付时点，默认是 Ordinary Annuity
- 💡 如果题目说"immediate"或"at the beginning" → Annuity Due

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| Perpetuity 用任意一期现金流做分子 | 必须用第一期现金流 A₁ 做分子 | 公式由等比级数求和推导，A₁ 对应第一期 |
| Growing perpetuity 可接受 r ≤ g | 必须 r > g，否则现值无穷大 | r ≤ g 时级数发散，经济上不合理 |
| Annuity Due 和 Ordinary Annuity 一样 | Annuity Due = Ordinary × (1+r) | 期初付款比期末付款早一期生息 |
| 半年付息直接用年利率 | 半年付息用 r/2 做周期利率，2n 做期数 | 利率和期数必须同频率 |
| 混合现金流可套单一公式 | 不同模式分别折现再加总 | 现金流可加性原则要求分别处理 |

### 🔄 跨模块关联

- **[[M01-Rates-and-Returns]]** — MWRR 本质就是 TVM 的 IRR 应用，"折现率"的概念从 M01 的利率解释延续而来。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 几何平均收益率与 TVM 中的复合增长概念相通。
- **[[M05-Portfolio-Mathematics]]** — Sharpe Ratio、SFRatio 均涉及折现概念。
- **Fixed Income** — 债券定价 = TVM 最直接的应用（票息年金 + 本金现值）。
- **Equity** — DDM 戈登增长模型 = TVM 永续增长年金在股权中的应用。
- **Corporate Issuers** — 资本预算中的 NPV、IRR、Payback Period 全部基于 TVM 框架。

### 📋 复习与刷题提示

- **核心能力**：快速识别四种现金流模式，熟练使用金融计算器求解隐含变量
- **必考题型**：年金现值/终值计算、隐含利率反推、EAR 换算、债券定价计算
- **最常犯错误**：年金模式误判、利率与期数频率不匹配、Perpetuity 分子用错
- 记忆口诀：
  - 时间轴画第一 — 现金流的时点决定一切
  - 频率必须匹配 — 折半率配加倍期数
  - Due 比 Ordinary 多乘 (1+r)
- 刷题建议：重点练习年金模式识别题和金融计算器反求解题，这些是 CFA 必考
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
