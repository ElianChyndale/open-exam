---
title: "M03 — CAPM and Beta"
description: 资本资产定价模型、Beta系数、证券市场线、绩效评估指标（Sharpe/Treynor/Alpha）及系统性风险与非系统性风险的辨析
module: M03
subject: Portfolio_Management
---

# M03: CAPM 与 Beta (CAPM and Beta)

## 1. 核心知识点 (Core Knowledge Points)

### 1.1 资本资产定价模型 (Capital Asset Pricing Model, CAPM)

- **CAPM 公式**：
  - `E(Ri) = Rf + βi × [E(Rm) - Rf]`
  - 必要回报率 (required return) = 无风险利率 + 风险溢价
  - 风险溢价 = Beta × 市场风险溢价

- **CAPM 基本假设**：
  - 投资者是风险厌恶的均值-方差优化者
  - 可以以无风险利率自由借贷
  - 所有投资者有相同的预期（同质预期 homogeneous expectations）
  - 无交易成本、无税收、资产无限可分

- **系统性风险定价**：只有系统性风险 (systematic risk) 获得预期收益补偿
  - 非系统性风险 (unsystematic risk) 可通过分散化消除，因此不获得风险溢价

### 1.2 Beta 系数 (Beta Coefficient)

- **Beta 计算公式**：`βi = Cov(Ri, Rm) / Var(Rm)`
- **Beta 的含义**：
  - `β = 1`：资产与市场同步波动
  - `β > 1`：资产比市场波动更大（进攻型 aggressive）
  - `β < 1`：资产比市场波动更小（防御型 defensive）
  - `β = 0`：与市场无相关性
  - `β < 0`：与市场反向波动（极少数资产）

### 1.3 证券市场线 (Security Market Line, SML)

- **SML**：图形化 CAPM，横轴为 Beta，纵轴为期望收益
- SML 的截距 = Rf，斜率 = 市场风险溢价 `[E(Rm)-Rf]`
- **定价判断**：
  - 资产点在 SML 上方 → 被低估 (undervalued) → 正 alpha
  - 资产点在 SML 下方 → 被高估 (overvalued) → 负 alpha
  - 资产点在 SML 上 → 合理定价 (fairly priced)

### 1.4 绩效评估指标 (Performance Evaluation Measures)

| 指标 | 公式 | 风险类型 | 适用场景 |
|------|------|----------|----------|
| 夏普比率 (Sharpe ratio) | `(Rp-Rf)/σp` | 总风险 | 评价完整组合 |
| 特雷诺比率 (Treynor ratio) | `(Rp-Rf)/βp` | 系统性风险 | 评价组合中分散化部分 |
| 詹森阿尔法 (Jensen's alpha) | `αp = Rp - [Rf+βp(E(Rm)-Rf)]` | 系统性风险 | CAPM 超额收益 |
| M 平方 (M-squared) | `(Rp-Rf)×(σm/σp) + Rf` | 总风险 | 风险调整到市场风险水平 |

## 2. 关键公式 (Key Formulas)

| 指标 | 公式 | 说明 |
|------|------|------|
| CAPM | `E(Ri) = Rf + βi × [E(Rm)-Rf]` | 必要回报率 |
| Beta | `βi = Cov(Ri,Rm) / σm²` | 市场敏感度 |
| 市场风险溢价 | `E(Rm) - Rf` | 市场组合超额收益 |
| 夏普比率 | `Sharpe = (Rp-Rf)/σp` | 每单位总风险超额收益 |
| 特雷诺比率 | `Treynor = (Rp-Rf)/βp` | 每单位系统性风险超额收益 |
| 詹森阿尔法 | `α = Rp - [Rf+βp(E(Rm)-Rf)]` | 实际 vs CAPM 基准 |
| 必要超额收益 | `βi × (E(Rm)-Rf)` | CAPM 的风险溢价 |

## 3. 常见考点与解题思路 (Exam Tips & Approaches)

### 考点1：计算必要回报率
- **步骤**：给定 β、Rf、E(Rm) → CAPM 公式直接计算
- 常见陷阱：确认 E(Rm) 是市场期望收益还是市场风险溢价

### 考点2：计算 Beta
- **步骤**：给定协方差与市场方差 → `β = Cov / Var(Rm)`
- 或给定相关系数：`β = ρim × σi / σm`

### 考点3：SML 定价判断
- **步骤**：计算 CAPM 必要收益 → 比较实际预期收益 → 判断低估/高估
- 正 alpha = 实际收益 > CAPM 必要收益 → 被低估

### 考点4：绩效指标选择
- **步骤**：分析组合为完整组合还是子组合 → 选 Sharpe（总风险）或 Treynor（系统风险）
- 常见陷阱：对充分分散化的组合，Sharpe 和 Treynor 排序通常一致

## 4. 易错点提醒 (Common Mistakes)

| 错误理解 | 正确理解 |
|----------|----------|
| Beta 高说明总风险一定高 | Beta 只衡量系统性风险，总风险还要考虑非系统性风险 |
| Sharpe 和 Treynor 可以互换使用 | Sharpe 用总风险，Treynor 用系统性风险 |
| SML 上方的资产被高估 | SML 上方的资产被低估（正 alpha） |
| CAPM 适用于任何市场 | CAPM 依赖于苛刻的假设，实际应用需谨慎 |
| 高风险一定带来高回报 | CAPM 中只有系统性风险获得补偿 |
| alpha 为正就说明组合表现好 | alpha 需要考虑统计显著性（t 检验） |

## 5. 跨模块关联 (Cross-Module Links)

- [[M01-Portfolio-Risk-and-Return]]：CAPM 建立在前序风险收益概念基础上
- [[M02-Utility-and-CAL]]：CML 是 CAL 在 CAPM 市场均衡下的特例
- [[M04-Market-Efficiency-and-Portfolio-Construction]]：CAPM 与市场有效性共同决定主动/被动策略
- [[M06-Behavioral-Biases]]：行为偏差可能导致市场价格偏离 CAPM 定价
- [[00-Portfolio-Management-MOC]]
