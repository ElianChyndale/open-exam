---
title: "M02 — Utility and CAL"
description: 效用函数与资本配置线，包括风险厌恶系数、无差异曲线、最优风险组合选择与借贷决策
module: M02
subject: Portfolio_Management
official_module: "Portfolio Risk and Return Part II"
---

# M02: 效用与资本配置线 (Utility and Capital Allocation Line)

## 1. 核心知识点 (Core Knowledge Points)

### 1.1 投资者偏好与效用函数 (Investor Preference and Utility Function)

- **效用函数 (utility function)**：`U = E(Rp) - 0.5 × A × σp²`
  - `U` = 投资者效用 (utility)
  - `E(Rp)` = 组合期望收益
  - `A` = 风险厌恶系数 (risk aversion coefficient)
  - `σp²` = 组合方差

- **风险厌恶系数 (risk aversion coefficient, A)**：
  - `A > 0`：风险厌恶 (risk averse) —— 要求额外收益补偿波动
  - `A = 0`：风险中性 (risk neutral) —— 只关注收益
  - `A < 0`：风险偏好 (risk seeking) —— 偏好波动

- **无差异曲线 (indifference curve)**：相同效用水平下不同 (风险, 收益) 组合的轨迹
  - 斜率 = 风险-收益替代率
  - 风险厌恶程度越高，曲线越陡峭（需更高收益补偿单位风险）

### 1.2 资本配置线 (Capital Allocation Line, CAL)

- **CAL** 描述无风险资产与风险组合之间的所有可能配置
  - `E(Rc) = Rf + [(E(Rp) - Rf) / σp] × σc`
  - `Rf` = 无风险利率
  - `E(Rp) - Rf` = 风险溢价 (risk premium)
  - `(E(Rp)-Rf)/σp` = **夏普比率 (Sharpe ratio)**，即 CAL 的斜率

- **最优风险组合 (optimal risky portfolio)**：
  - 最大化夏普比率的组合
  - 在图形上，CAL 与有效前沿的切点组合

- **借贷决策 (borrowing/lending choice)**：
  - 贷出 (lending)：配置一部分资金到无风险资产
  - 借入 (borrowing)：以无风险利率借入资金，杠杆投资于风险组合
  - 借入时 CAL 的斜率可能不同（借入利率 > 贷出利率）

### 1.3 最优组合选择 (Optimal Portfolio Selection)

- 投资者选择使 **效用最大化** 的组合
- 无差异曲线与 CAL 的切点 = 最优完整组合 (optimal complete portfolio)
- 风险厌恶程度高的投资者配置更多到无风险资产

## 2. 关键公式 (Key Formulas)

| 指标 | 公式 | 说明 |
|------|------|------|
| 效用函数 | `U = E(Rp) - 0.5 × A × σp²` | A 越大，波动惩罚越重 |
| 资本配置线 | `E(Rc) = Rf + [(E(Rp)-Rf)/σp] × σc` | 无风险 + 风险组合线性配比 |
| 风险组合权重 | `w_p = (E(Rp)-Rf) / (A × σp²)` | 给定 A 下的最优分配 |
| 夏普比率 | `Sharpe = (E(Rp) - Rf) / σp` | CAL 斜率，衡量风险调整后收益 |

## 3. 常见考点与解题思路 (Exam Tips & Approaches)

### 考点1：效用计算
- **步骤**：已知 E(Rp), σp, A → 代入 `U = E(Rp) - 0.5Aσp²`
- 常见陷阱：注意 `A` 的数值 —— 不同教材可能数值有差异

### 考点2：CAL 上组合的收益与风险
- **步骤**：给定 wf（无风险资产权重）→ 计算 E(Rc) 和 σc
- 公式：`E(Rc) = wf×Rf + (1-wf)×E(Rp)`, `σc = (1-wf)×σp`
- 权重和为 1：`wf + wp = 1`；当 wf < 0 时表示借入

### 考点3：求最优风险组合权重
- **步骤**：已知风险组合的 E(Rp), σp, A → `wp* = (E(Rp)-Rf)/(A×σp²)`
- 若 wp* > 1：表示该投资者会借钱投资（A 较低）
- 若 wp* < 0：表示该投资者会做空风险组合（极少出现）

### 考点4：无差异曲线与最优组合
- **步骤**：给定多条无差异曲线 + CAL → 找切点 → 判断最优配置

## 4. 易错点提醒 (Common Mistakes)

| 错误理解 | 正确理解 |
|----------|----------|
| 效用只是一个抽象概念 | 效用函数直接决定风险资产与无风险资产的配置比例 |
| 风险厌恶系数 A 越高，配置越多到风险资产 | A 越高，配置越多到无风险资产 |
| CAL 只有一条 | 不同的风险组合有不同的 CAL，最优的是 Sharpe 最大的那条 |
| 借入利率和贷出利率一定相同 | 通常借入利率 > 贷出利率，导致 CAL 在借入段更平缓 |
| 无差异曲线可以相交 | 同一投资者的无差异曲线互不相交 |
| 夏普比率只在最优组合时有用 | 夏普比率可用于比较所有风险组合的性价比 |

## 5. 跨模块关联 (Cross-Module Links)

- [[M01-Portfolio-Risk-and-Return]]：效用函数和 CAL 基于 M01 的风险收益计算
- [[M03-CAPM-and-Beta]]：CAL 的资本市场线 (CML) 扩展对应于 CAPM 的 SML
- [[M05-IPS]]：风险厌恶程度影响 IPS 中 risk objective 的设定
- [[M06-Behavioral-Biases]]：行为偏差会使实际决策偏离效用最大化
- [[00-Portfolio-Management-MOC]]
