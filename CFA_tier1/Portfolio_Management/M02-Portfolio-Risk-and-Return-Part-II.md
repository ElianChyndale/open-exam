---
title: "M02 — Portfolio Risk and Return: Part II"
description: "CFA Level I 2026 official module: Portfolio Risk and Return: Part II"
module: M02
subject: "Portfolio Management"
topic_area: Portfolio_Management
curriculum_year: 2026
official_module: "Module 2: Portfolio Risk and Return: Part II"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Portfolio_Management
  - official_2026
---

# M02: Portfolio Risk and Return: Part II

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Portfolio Risk and Return: Part II
- 2.01 | Introduction
- 2.02 | Capital Market Theory: Risk-Free and Risky Assets
- 2.03 | Capital Market Theory: The Capital Market Line
- 2.04 | Capital Market Theory: CML - Leveraged Portfolios
- 2.05 | Systematic and Nonsystematic Risk
- 2.06 | Return Generating Models
- 2.07 | Calculation and Interpretation of Beta
- 2.08 | Capital Asset Pricing Model: Assumptions and the Security Market Line
- 2.09 | Capital Asset Pricing Model: Applications
- 2.10 | Beyond CAPM: Limitations and Extensions of CAPM
- 2.11 | Portfolio Performance Appraisal Measures
- 2.12 | Applications of the CAPM in Portfolio Construction
- 2.13 | Summary

## Learning Outcome Statements

The candidate should be able to:

- describe the implications of combining a risk-free asset with a portfolio of risky assets
- explain the capital allocation line (CAL) and the capital market line (CML)
- explain systematic and nonsystematic risk, including why an investor should not expect to receive additional return for bearing nonsystematic risk
- explain return generating models (including the market model) and their uses
- calculate and interpret beta
- explain the capital asset pricing model (CAPM), including its assumptions, and the security market line (SML)
- calculate and interpret the expected return of an asset using the CAPM
- describe and demonstrate applications of the CAPM and the SML
- calculate and interpret the Sharpe ratio, Treynor ratio, M2, and Jensen's alpha

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M02: 组合风险与收益 Part II (Portfolio Risk and Return: Part II)
│
├── 🟢 核心主题：从组合理论到 CAPM
│   └── 市场均衡下的资产定价模型
│
├── ⭐ CAPM (资本资产定价模型)
│   ├── E(Ri) = Rf + βi × [E(Rm) - Rf]
│   ├── 必要回报率 = 无风险利率 + 风险溢价
│   └── 假设
│       ├── 投资者风险厌恶、均值-方差优化
│       ├── 可以无风险利率自由借贷
│       ├── 同质预期 (homogeneous expectations)
│       ├── 无交易成本、无税收
│       └── 🎯 高频考点：CAPM 假设
│
├── ⭐ Beta 系数
│   ├── βi = Cov(Ri, Rm) / Var(Rm)
│   ├── βi = ρim × σi / σm (相关式)
│   ├── β = 1 → 同步市场
│   ├── β > 1 → 进攻型 (aggressive)
│   ├── β < 1 → 防御型 (defensive)
│   ├── β = 0 → 无市场相关性
│   └── β < 0 → 反向资产（极少见）
│
├── ⭐ CML vs SML
│   ├── CML (资本市场线)
│   │   ├── 横轴: 总风险 σ
│   │   ├── 适用: 有效组合
│   │   └── 斜率: Sharpe Ratio
│   └── SML (证券市场线)
│       ├── 横轴: 系统性风险 β
│       ├── 适用: 所有资产
│       └── 斜率: 市场风险溢价 E(Rm)-Rf
│
├── ⭐ 系统性风险与非系统性风险
│   ├── 系统性风险 → 获得预期收益补偿
│   ├── 非系统性风险 → 可通过分散化消除 → 无补偿
│   └── 💡 只有系统风险定价
│
├── ⭐ 绩效评估指标
│   ├── Sharpe: (Rp-Rf)/σp (总风险)
│   ├── Treynor: (Rp-Rf)/βp (系统风险)
│   ├── Jensen's α: Rp - [Rf+βp(E(Rm)-Rf)]
│   └── M²: (Rp-Rf)×(σm/σp)+Rf
│
├── 💡 关键洞察
│   ├── SML 上方 = 低估 = 正 alpha = 买入信号
│   ├── SML 下方 = 高估 = 负 alpha = 卖出信号
│   ├── CAPM 是单因子模型: 只有市场风险因子
│
└── ⚠️ 考试陷阱
    ├── CML 只有有效组合在线上；SML 所有资产在线上
    ├── Beta 衡量系统风险，不是总风险
    ├── Alpha 正 ≠ 一定好（可能额外风险）
    └── CAPM 假设苛刻，实际应用需谨慎
```

## 📖 知识点详解

### 知识点1：资本资产定价模型 (CAPM)

**核心概念**：CAPM 描述了资产的期望收益与系统性风险之间的线性关系，是现代金融中最核心的定价模型之一。其核心思想是：只有系统性风险（Beta）获得风险溢价补偿，非系统性风险可通过分散化消除，因此不获得补偿。

- **CAPM 公式**：E(Ri) = Rf + βi × [E(Rm) - Rf]。资产必要回报率 = 无风险利率 + Beta × 市场风险溢价
- **Beta 系数**：βi = Cov(Ri, Rm) / Var(Rm)，衡量资产对市场变动的敏感度。β > 1 表示进攻型，β < 1 表示防御型，β = 1 表示与市场同步
- **证券市场的线 (SML)**：CAPM 的图形化表示，横轴为 Beta，纵轴为期望收益。资产点在 SML 上方表示被低估（正 Alpha），下方表示被高估（负 Alpha）
- 💡 **重要区分**：CML（资本市场线）衡量总风险（σ），SML（证券市场线）衡量系统性风险（β）

**考试应用**：CAPM 是 PM 科目最高频考点。计算必要回报率需注意区分 E(Rm) 和 [E(Rm)-Rf]（市场风险溢价）。Beta 计算有两种方式：协方差/市场方差，或 ρim×σi/σm。SML 定价判断：SML 上方 → 低估 → 正 Alpha。

### 知识点2：效用函数与资本配置线 (Utility Function and CAL)

**核心概念**：效用函数量化投资者对风险-收益的主观偏好，资本配置线（CAL）描述无风险资产与风险组合之间的所有可能配置。两者的结合决定了投资者的最优完整组合。

- **效用函数**：U = E(Rp) - 0.5 × A × σp²。A 是风险厌恶系数，决定了对风险的惩罚程度
- **资本配置线 (CAL)**：E(Rc) = Rf + [(E(Rp)-Rf)/σp] × σc。斜率 = 夏普比率 (Sharpe ratio)
- **最优风险组合权重**：wp* = (E(Rp)-Rf) / (A × σp²)
- **最优完整组合**：无差异曲线与 CAL 的切点
- 💡 借入利率通常高于贷出利率，导致 CAL 在借入段变得更平缓

**考试应用**：效用计算题需代入公式 U = E(Rp) - 0.5Aσp²。CAL 题需计算给定无风险资产权重下的组合收益和风险。最优权重题需用 wp* 公式。常见陷阱：借入/贷出利率不同时，CAL 在借入段和贷出段斜率不同。

### 知识点3：系统性风险与非系统性风险 (Systematic vs Unsystematic Risk)

**核心概念**：总风险分为系统性风险和非系统性风险。系统性风险影响整个市场，无法通过分散化消除，是 CAPM 中唯一被定价的风险。非系统性风险是公司或行业特有的，可通过分散化消除，因此理性投资者不应期望获得非系统性风险补偿。

- **系统性风险 (Systematic Risk)**：又称市场风险、不可分散风险。由宏观经济因素（利率、通胀、GDP 增长等）驱动。用 Beta 衡量
- **非系统性风险 (Unsystematic Risk)**：又称公司特有风险、可分散风险。由公司特定事件（管理层变更、产品召回等）驱动。可通过增加资产数量降低
- **总风险 = 系统性风险 + 非系统性风险**。充分分散化的组合只承担系统性风险
- 🎯 **高频考点**：为什么投资者不应期望非系统性风险的额外回报——因为可以通过分散化免费消除

**考试应用**：给定风险来源描述，判断是系统性还是非系统性。理解分散化只降低非系统性风险。常见陷阱：认为所有风险都得到补偿（实际只有系统性风险获得风险溢价）。

### 知识点4：绩效评估指标 (Performance Evaluation Measures)

**核心概念**：评估投资组合绩效需要同时考虑收益和风险。不同的指标使用不同的风险度量，适用于不同的评估场景。选择合适的指标取决于被评估组合的性质（完整组合还是子组合）和评估目标。

- **夏普比率 (Sharpe Ratio)**：(Rp - Rf) / σp。使用总风险，适用于评估完整组合
- **特雷诺比率 (Treynor Ratio)**：(Rp - Rf) / βp。使用系统性风险，适用于评估充分分散化的组合或子组合
- **詹森阿尔法 (Jensen's Alpha)**：αp = Rp - [Rf + βp(E(Rm)-Rf)]。CAPM 框架下的超额收益
- **M 平方 (M²)**：Rf + (Rp-Rf) × (σm/σp)。将组合风险调整到市场风险水平后的收益
- **信息比率 (Information Ratio)**：(Rp-Rb) / σ(Rp-Rb)。主动收益除以主动风险（追踪误差）
- 💡 对充分分散化的组合，Sharpe 和 Treynor 排序通常一致

**考试应用**：绩效指标选择题是高频题。关键：Sharpe 用总风险，Treynor 用系统性风险。给定一个组合（如完整组合 vs 子组合），选择最合适的评估指标。Alpha 正表示超额收益，但需考虑统计显著性。

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `E(Ri) = Rf + βi × [E(Rm)-Rf]` | CAPM 必要回报率 | 资产定价、资本成本计算 | 确认 E(Rm)-Rf 是市场风险溢价而非 E(Rm) |
| `βi = Cov(Ri,Rm) / σm²` | Beta 系数 = 协方差/市场方差 | 计算资产系统风险 | 也可用 β = ρim × σi/σm |
| `βp = Σ wi × βi` | 组合 Beta | 计算组合系统风险 | 组合 Beta = 加权平均 |
| `Sharpe = (Rp-Rf)/σp` | 夏普比率 | 评价完整组合（总风险） | 用于横向比较 |
| `Treynor = (Rp-Rf)/βp` | 特雷诺比率 | 评价分散化组合（系统风险） | 适用于组合的子部分 |
| `Jensen's α = Rp - [Rf+βp(E(Rm)-Rf)]` | 詹森阿尔法 | 衡量超额收益（经理选股能力） | α > 0 表示优于市场 |
| `M² = (Rp-Rf)×(σm/σp) + Rf` | M 平方 | 将组合风险调整到市场水平 | 可与市场直接比较 |
| `Tracking Error = σ(Rp-Rb)` | 跟踪误差 | 衡量主动风险 | 信息比率 = (Rp-Rb)/TE |

### 🛠️ 常见考点与解题思路

**考点1：CAPM 计算期望收益**
- **步骤**：
  1. 确定 Rf, β, E(Rm)
  2. 代入 E(Ri) = Rf + β × (Rm - Rf)
  3. **陷阱**：确认题目给的是 E(Rm) 还是市场风险溢价
  - 给 E(Rm) = 10%, Rf = 2% → 市场溢价 = 8%
  - 给市场溢价 = 8%, Rf = 2% → 直接代入 8%

**考点2：SML 定价判断**
- **步骤**：
  1. 用 CAPM 计算必要回报率
  2. 比较实际预期收益与必要回报率
  3. 实际 > 必要 → 被低估 → 正 alpha → SML 上方 → 买入
  4. 实际 < 必要 → 被高估 → 负 alpha → SML 下方 → 卖出

**考点3：Beta 计算**
- **步骤**：
  1. 给定协方差和市场方差 → β = Cov/σm²
  2. 给定相关系数和标准差 → β = ρim × σi/σm
  3. 给定历史数据 → 回归 Ri = α + βRm + ε

**考点4：绩效指标选择**
- **步骤**：先判断组合类型
  - 完整组合（含所有资产）→ Sharpe ratio（总风险）
  - 充分分散化的组合 → Treynor ratio（系统风险）
  - 主动管理 → Jensen's alpha
- **关键**：Sharpe 和 Treynor 对充分分散化组合排序通常一致

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| CML 和 SML 相同 | CML 横轴 σ 适用于有效组合；SML 横轴 β 适用于所有资产 | 风险度量不同 |
| Beta 高 = 总风险高 | Beta 只衡量系统性风险，总风险还包含非系统性风险 | 总风险 = 系统 + 非系统 |
| SML 上方资产被高估 | SML 上方资产被低估（正 alpha） | 实际收益 > 必要收益 |
| Sharpe 和 Treynor 可互换 | Sharpe 用总风险，Treynor 用系统风险 | 视角不同，适用场景不同 |
| CAPM 适用于所有市场 | CAPM 依赖严格假设，实际需谨慎 | 假设同质预期、无摩擦 |
| Alpha 正 ≠ 经理能力强 | Alpha 需考虑统计显著性（t 检验） | 可能只是运气 |
| 高风险 = 高回报 | 只有系统性风险获得补偿 | 非系统性风险可分散，无额外回报 |

### 🔄 跨模块关联

- **[[M01-Portfolio-Risk-and-Return-Part-I]]** — CAPM 建立在 M01 的风险收益概念之上，Beta 依赖协方差概念
- **[[M04-Basics-of-Portfolio-Planning-and-Construction]]** — CAPM 为战略资产配置提供理论框架
- **[[M05-The-Behavioral-Biases-of-Individuals]]** — 行为偏差可能导致市场价格偏离 CAPM 定价
- **[[M06-Introduction-to-Risk-Management]]** — 系统性风险是全面风险管理的重要维度
- **[[00-Portfolio-Management-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M02 是 Portfolio Management 中**最核心的计算模块**，公式密集
- **核心能力**：CAPM 计算、Beta 计算、绩效指标计算和选择
- **必考题型**：CAPM 必要回报率计算、SML 定价判断、Sharpe/Treynor/Alpha 计算
- **最常犯错误**：混淆 CML 与 SML、误判 SML 上方为高估、绩效指标选错
- 记忆技巧：
  - CAPM = Rf + β × (Rm - Rf)
  - SML 上方 = 低估 = 正 alpha
  - Sharpe 适用于完整组合，Treynor 适用于子组合
- 对考试影响：绩效评估指标的计算和解释是 CFA L1 高频考点
