---
title: "M01 — Portfolio Risk and Return"
description: 投资组合风险与收益的核心概念，包括期望收益计算、方差/协方差、相关系数、分散化收益与有效前沿
module: M01
subject: Portfolio_Management
---

# M01: 组合风险与收益 (Portfolio Risk and Return)

## 1. 核心知识点 (Core Knowledge Points)

### 1.1 从单资产到投资组合的转换 (Single Asset to Portfolio Translation)

- **期望收益**是各资产期望收益的加权平均，权重为投资比例。
  - 组合期望收益 (expected portfolio return) = `E(Rp) = Σ wi × E(Ri)`
  - 注意：收益用百分比连续复利或算术平均，考试通常用算术平均

- **组合方差**不单纯是各资产方差的加权和，还需加入协方差项 (covariance terms)。
  - 两资产组合方差：`σp² = w1²σ1² + w2²σ2² + 2w1w2Cov(R1,R2)`
  - 核心直觉：资产间联动关系决定了组合整体的波动

- **相关系数 (correlation coefficient)** 是标准化后的协方差，取值范围 [-1, +1]：
  - `Corr(R1,R2) = Cov(R1,R2) / (σ1 × σ2)`
  - `ρ = +1`：无分散化效果（完全正相关）
  - `ρ = -1`：完全对冲可能（完全负相关）
  - `ρ = 0`：有一定分散化效果（不相关）
  - `-1 < ρ < +1`：分散化收益随 ρ 降低而增加

### 1.2 分散化效果 (Diversification Effect)

- **分散化收益 (diversification benefit)** 来自资产间不完全正相关
- 随着组合中资产数量增加，**非系统性风险 (unsystematic risk / diversifiable risk / firm-specific risk)** 趋于下降
- **系统性风险 (systematic risk / market risk / non-diversifiable risk)** 无法通过分散化消除
- 有效前沿 (efficient frontier) 上每个点代表给定风险水平下的最高期望收益

### 1.3 有效机会集 (Efficient Opportunity Set)

- 最小方差组合 (minimum-variance portfolio) 是风险最低的点
- 有效前沿 (efficient frontier) 是从最小方差组合向上的部分
- 理性投资者会持有有效前沿上的某个组合，取决于其风险偏好

## 2. 关键公式 (Key Formulas)

| 指标 | 公式 | 说明 |
|------|------|------|
| 组合期望收益 | `E(Rp) = Σ wi × E(Ri)` | 加权平均，权重和为 1 |
| 两资产方差 | `σp² = w1²σ1² + w2²σ2² + 2w1w2Cov12` | 协方差项不可忽略 |
| 协方差 | `Cov(R1,R2) = E[(R1-E(R1))(R2-E(R2))]` | 衡量同向变动程度 |
| 相关系数 | `ρ12 = Cov(R1,R2) / (σ1σ2)` | 标准化到 [-1, +1] |
| 两资产最小方差权重 | `w1_min = (σ2² - Cov12) / (σ1² + σ2² - 2Cov12)` | N=2 时可用 |

## 3. 常见考点与解题思路 (Exam Tips & Approaches)

### 考点1：计算组合期望收益与方差
- **步骤**：先算加权收益 → 再带入方差公式 → 注意符号
- 常见陷阱：资产权重之和必须为 1（或 100%）

### 考点2：判断分散化程度
- **步骤**：给定相关系数 → 判断分散化收益 → 比较不同相关系数下的组合风险
- 常见题型：多选判断分散化效果

### 考点3：最小方差组合权重
- **步骤**：用两资产公式解权重 → 代入求最小方差 → 判断有效前沿位置

### 考点4：协方差/相关系数的计算
- **步骤**：给定历史数据 → 按定义计算均值 → 计算离差乘积 → 求协方差 → 除以标准差得相关系数

## 4. 易错点提醒 (Common Mistakes)

| 错误理解 | 正确理解 |
|----------|----------|
| 多买几个资产就完成分散化 | 分散化关键是低相关性，不是数量本身 |
| 组合方差是各资产方差的加权和 | 方差必须加入协方差项 |
| ρ=0 就能完全分散化 | ρ=0 只是部分分散化，ρ=-1 才能完全对冲 |
| 有效前沿上的所有组合都适合所有人 | 不同风险偏好的投资者选择不同位置 |
| 分散化可以消除所有风险 | 系统性风险无法通过分散化消除 |

## 5. 跨模块关联 (Cross-Module Links)

- [[M02-Utility-and-CAL]]：组合风险收益数据输入到效用函数和资本配置线
- [[M03-CAPM-and-Beta]]：系统性风险概念延伸至 CAPM 和 Beta
- [[M04-Market-Efficiency-and-Portfolio-Construction]]：有效前沿与组合构建流程相关联
- [[00-Portfolio-Management-MOC]]
