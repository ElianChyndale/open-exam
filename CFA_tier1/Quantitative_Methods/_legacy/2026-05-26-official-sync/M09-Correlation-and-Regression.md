---
title: "M10 — Simple Linear Regression"
description: 简单线性回归 — 模型设定, 回归诊断, 拟合, 推断, 预测
module: M10
official_module: "Module 10: Simple Linear Regression"
subject: Quantitative_Methods
los:
  - describe a simple linear regression model, how the least squares criterion is used to estimate regression coefficients, and the interpretation of these coefficients
  - explain the assumptions underlying the simple linear regression model, and describe how residuals and residual plots indicate if these assumptions may have been violated
  - calculate and interpret measures of fit and formulate and evaluate tests of fit and of regression coefficients in a simple linear regression
  - describe the use of analysis of variance (ANOVA) in regression analysis, interpret ANOVA results, and calculate and interpret the standard error of estimate
  - calculate and interpret the predicted value for the dependent variable, and a prediction interval for it, given an estimated linear regression model
  - describe different functional forms of simple linear regressions
---

# M10: Simple Linear Regression（简单线性回归）

## 1. 核心知识点

### 1.1 简单线性回归模型（Simple Linear Regression Model）

**回归方程（Regression Equation）**：
`Y_i = b₀ + b₁X_i + e_i`
- Y = 因变量（Dependent Variable）= 被解释变量
- X = 自变量（Independent Variable）= 解释变量
- b₀ = 截距（Intercept）：当 X=0 时 Y 的期望值
- b₁ = 斜率（Slope）：X 每增加 1 单位，Y 的平均变化量
- e_i = 残差（Residual）：实际值 Y_i 与预测值 Ŷ_i 之差

**最小二乘法（Ordinary Least Squares, OLS）**：
- OLS 的目标：最小化残差平方和 SSE = Σ(Y_i - Ŷ_i)²
- 斜率公式：`b₁ = Cov(X, Y) / Var(X)`
- 截距公式：`b₀ = ȳ - b₁x̄`

**OLS 估计量的性质（Gauss-Markov Theorem）**：
- 在线性、无偏估计量中，OLS 估计量具有最小方差（BLUE: Best Linear Unbiased Estimator）

### 1.2 回归诊断（Regression Diagnostics）

**四个关键假设（Four Key Assumptions of OLS）**：
1. **线性（Linearity）**：Y 与 X 的关系是线性的
2. **同方差性（Homoskedasticity）**：残差的方差在所有 X 值上恒定
3. **独立性（Independence）**：各观测值的残差相互独立（时间序列数据中尤其重要）
4. **正态误差（Normality of Errors）**：残差服从正态分布（对系数的无偏性不是必须的，但对小样本推断很重要）

**诊断方法**：
- **残差图（Residual Plot）**：残差 vs 拟合值（或 vs 自变量）。如果残差图呈随机散布 → 假设满足；如果有明显模式（喇叭形、曲线形）→ 假设违反。
- **异方差（Heteroskedasticity）**：残差方差随 X 变化（常见于横截面数据）。后果：标准误有偏 → t 检验失效。
- **序列相关（Serial Correlation / Autocorrelation）**：时间序列回归中常见。后果：标准误被低估。

### 1.3 拟合与推断（Fit and Inference）

**拟合优度（R² / Coefficient of Determination）**：
`R² = SSR / SST = 1 - SSE / SST`
- R² 衡量模型解释的 Y 变异占总变异的比例
- R² 范围 [0, 1]，越高说明模型拟合越好
- 但 R² 高不意味着因果关系或模型正确（spurious regression 问题）

**估计标准误（Standard Error of Estimate, SEE）**：
`SEE = √[SSE / (n-2)]`
- 衡量回归模型中观测值围绕回归线的分散程度
- 单位与 Y 相同，越小说明预测越精确
- 对应的 MSE（Mean Squared Error）= SEE²

**斜率系数的 t 检验**：
`t = (b₁ - β₁,₀) / SE(b₁)`
- H₀: β₁ = 0（X 对 Y 无线性影响）
- 自由度 df = n-2
- 如果不拒绝 H₀，说明 X 对 Y 没有显著的线性关系

**方差分析 F 检验（ANOVA F-Test）**：
`F = MSR / MSE`
- 检验整体模型的显著性（在简单回归中，F = t²，与斜率 t 检验等价）
- 在多元回归中，F 检验检验所有斜率是否同时为零

**预测区间（Prediction Interval）**：
- 点估计（Point Estimate）给出 Y 的"最佳猜测"
- 预测区间比置信区间更宽，因为它包含了两种不确定性：参数估计的不确定性 + 随机误差项的不确定性
- 距离 x̄ 越远的 X 值，预测区间越宽

> **【考试陷阱】** Prediction Interval 比 Point Estimate 更诚实地表达了预测的不确定性。考试可能问：为什么预测区间比置信区间宽？因为预测区间包含了个体观测值的误差。

## 2. 关键公式

| 公式 | 解释 | 使用场景 |
|------|------|----------|
| `Y_i = b₀ + b₁X_i + e_i` | 回归方程 | 简单线性回归模型 |
| `b₁ = Cov(X,Y)/Var(X)` | 斜率 | 回归系数估计 |
| `b₀ = ȳ - b₁x̄` | 截距 | 回归截距估计 |
| `R² = SSR/SST` | 拟合优度 | 模型解释力 |
| `SEE = √[SSE/(n-2)]` | 估计标准误 | 回归预测精度 |
| `t = (b₁-β₁,₀)/SE(b₁)` | 斜率 t 检验 | 检验 X 对 Y 的线性影响 |
| `F = MSR/MSE` | ANOVA F 统计量 | 检验整体模型显著性 |

## 3. 常见考点与解题思路

**考点一：掌握 ANOVA 表解读**
- 给 ANOVA 表（SSR, SSE, SST; df; MSR, MSE），计算 R²、SEE、F 统计量
- R² = SSR/SST
- F = MSR/MSE = [SSR/1] / [SSE/(n-2)]

**考点二：相关 vs 回归关系**
- 回归斜率 b₁ = Cov(X,Y)/Var(X)
- 相关系数 r = Cov(X,Y)/(σ_Xσ_Y)
- 两者关系：b₁ = r × (s_Y/s_X)
- R² = r²（仅限简单线性回归）

**考点三：残差图判断假设违反**
- 散点随机分布 → OK
- 扇形/喇叭形 → 异方差（Heteroskedasticity）
- 曲线模式 → 非线性（Nonlinearity）
- 正/负序列模式 → 序列相关（Serial Correlation）

## 4. 易错点提醒

1. **R² ≠ 因果关系**：高 R² 不意味着 X 导致了 Y（辛普森悖论 / 虚假回归）。
2. **相关系数 t 检验自由度 = n-2**：不是 n-1。
3. **预测区间比置信区间宽**：预测区间包含了剩余误差 e_i 的不确定性，不只是回归参数的不确定性。
4. **F 与 t 在简单回归中等价**：F = t²，但注意 F 是单边检验，t 可以是双边检验。
5. **异方差不影响系数无偏性**：OLS 系数仍然无偏，但标准误有偏 → t 检验失效。
6. **预测区间在均值处最窄**：X 距离 x̄ 越远，预测区间越宽。

## 5. 跨模块关联

- **[[M09-Tests-of-Independence]]**：相关系数的 t 检验与回归斜率系数的 t 检验等价（t 统计量完全相等），R² = r²。列联表分析中发现的关联可以使用回归进一步建模。
- **[[M03-Statistical-Measures]]**：相关系数的概念在 M03 中引入，在回归分析中扩展为正式的斜率检验和 R² 解释。
- **[[M05-Portfolio-Mathematics]]**：协方差和相关系数是组合方差公式和回归分析框架的共同组件。
- **[[M08-Hypothesis-Testing]]**：回归中的 t 检验和 F 检验是 M08 假设检验框架的直接应用。
- **[[M07-Sampling-and-Estimation]]**：回归系数标准误 SE(b₁) 是 M07 中标准误概念在回归中的推广。
- **[[M10-Big-Data-and-ML]]**：简单线性回归是机器学习中监督学习的最基础模型 — 理解回归假设有助于理解更复杂的模型何时适用。
