---
title: "M10 — Simple Linear Regression"
description: "CFA Level I 2026 official module: Simple Linear Regression"
module: M10
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 10: Simple Linear Regression"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M10: Simple Linear Regression

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Simple Linear Regression
- 10.01 | Introduction
- 10.02 | Estimation of the Simple Linear Regression Model
- 10.03 | Assumptions of the Simple Linear Regression Model
- 10.04 | Hypothesis Tests in the Simple Linear Regression Model
- 10.05 | Prediction in the Simple Linear Regression Model
- 10.06 | Functional Forms for Simple Linear Regression

## Learning Outcome Statements

The candidate should be able to:

- describe a simple linear regression model, how the least squares criterion is used to estimate regression coefficients, and the interpretation of these coefficients
- explain the assumptions underlying the simple linear regression model, and describe how residuals and residual plots indicate if these assumptions may have been violated
- calculate and interpret measures of fit and formulate and evaluate tests of fit and of regression coefficients in a simple linear regression
- describe the use of analysis of variance (ANOVA) in regression analysis, interpret ANOVA results, and calculate and interpret the standard error of estimate in a simple linear regression
- calculate and interpret the predicted value for the dependent variable, and a prediction interval for it, given an estimated linear regression model and a value for the independent variable
- describe different functional forms of simple linear regressions

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M10: Simple Linear Regression（简单线性回归）
│
├── ⭐ 回归模型 (Regression Model)
│   ├── 📐 Yᵢ = b₀ + b₁Xᵢ + eᵢ
│   ├── b₀ (截距): X=0 时 Y 的期望值
│   ├── b₁ (斜率): X 每增 1 单位，Y 的平均变化量
│   ├── eᵢ (残差): Yᵢ - Ŷᵢ
│   └── 💡 OLS 目标: 最小化 SSE = Σ(Yᵢ-Ŷᵢ)²
│
├── ⭐ OLS 估计
│   ├── 📐 b₁ = Cov(X,Y)/Var(X)
│   ├── 📐 b₀ = ȳ - b₁x̄
│   └── 💡 Gauss-Markov: OLS 是 BLUE (Best Linear Unbiased Estimator)
│
├── ⭐ 四个关键假设 (Four OLS Assumptions)
│   ├── 线性 (Linearity): Y 与 X 关系是线性的
│   ├── 同方差性 (Homoskedasticity): 残差方差恒定
│   ├── 独立性 (Independence): 残差相互独立
│   └── 正态误差 (Normality of Errors): 残差服从正态（小样本推断需要）
│
├── ⭐ 回归诊断 — 残差图 (Residual Plot)
│   ├── 随机散布 → 假设满足
│   ├── 喇叭形 → 异方差 (Heteroskedasticity)
│   ├── 曲线形 → 非线性 (Nonlinearity)
│   └── 序列模式 → 序列相关 (Serial Correlation)
│
├── ⭐ 拟合优度与推断 (Fit & Inference)
│   ├── 📐 R² = SSR/SST = 1 - SSE/SST — 模型解释力
│   ├── 📐 SEE = √[SSE/(n-2)] — 回归预测精度
│   ├── 📐 t = (b₁-β₁,₀)/SE(b₁) — 斜率显著性检验, df=n-2
│   ├── 📐 F = MSR/MSE — 整体模型显著性检验
│   ├── 💡 简单回归中: F = t², R² = r²
│   └── ⚠️ R² 高 ≠ 因果关系
│
├── ⭐ 预测区间 (Prediction Interval)
│   ├── 点估计: Ŷ = b₀ + b₁X
│   ├── 预测区间比置信区间更宽
│   └── ⚠️ X 距 x̄ 越远，预测区间越宽
│
├── 💡 关键洞察
│   ├── b₁ = Cov(X,Y)/Var(X) = r × (sY/sX)
│   ├── 回归 t 检验与 M09 相关系数 t 检验等价
│   ├── 异方差不影响无偏性，但使标准误有偏 → t 检验失效
│   ├── 预测区间 = 置信区间 + 残差不确定性
│   └── R² 高可能是虚假回归，需要用经济理论验证
│
└── ⚠️ 考试陷阱总结
    ├── R² 高 ≠ 因果关系（虚假回归）
    ├── 相关系数 t 检验 df = n-2
    ├── 预测区间比置信区间宽（包含残差不确定性）
    ├── F = t² 在简单回归中成立，F 是单边，t 可是双边
    ├── 异方差不破坏无偏性，但破坏标准误和 t 检验
    └── 预测区间在 x̄ 处最窄
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Yᵢ = b₀ + b₁Xᵢ + eᵢ` | 回归方程 | 简单线性回归模型 | eᵢ = 残差 |
| `b₁ = Cov(X,Y)/Var(X)` | 斜率估计 | OLS 斜率系数 | Cov 和 Var 都用样本计算 |
| `b₀ = ȳ - b₁x̄` | 截距估计 | OLS 截距系数 | 回归线经过 (x̄, ȳ) |
| `R² = SSR/SST = 1-SSE/SST` | 拟合优度 | 模型解释力比例 | 范围 [0,1]，高 ≠ 因果 |
| `SEE = √[SSE/(n-2)]` | 估计标准误 | 回归预测精度 | df = n-2 |
| `t = (b₁-β₁,₀)/SE(b₁)` | 斜率 t 检验 | X 对 Y 的线性影响 | df = n-2 |
| `F = MSR/MSE` | ANOVA F 统计量 | 整体模型显著性 | 简单回归中 F = t² |
| `Ŷ = b₀ + b₁X` | 点预测 | 给定 X 预测 Y | 预测区间更宽 |

### 🛠️ 常见考点与解题思路

**考点1：ANOVA 表解读（高频必考）**
- 给定 ANOVA 表，需要计算的三个关键指标：
  - R² = SSR/SST = 1 - SSE/SST (模型解释力比例)
  - SEE (Standard Error of Estimate) = √[SSE/(n-2)]
  - F = MSR/MSE = [SSR/1] / [SSE/(n-2)]
- ANOVA 表的关键行：
  - SSR (回归平方和): 模型解释的变异
  - SSE (残差平方和): 模型未解释的变异
  - SST (总平方和): Y 的总变异 = SSR + SSE
- ⚠️ R²、F、t 三者在简单回归中相互关联 (F=t², R²=r²)
- 💡 高 R² 但低 F? 不可能 — 因为 F=MSR/MSE 与 R² 正相关

**考点2：相关 vs 回归关系**
- 斜率: b₁ = Cov(X,Y)/Var(X)
- 相关系数: r = Cov(X,Y)/(σ_Xσ_Y)
- 两者转换: b₁ = r × (s_Y/s_X)
- R² = r² (仅在简单线性回归中成立！)
- ⚠️ R² 和 r² 的数值相等关系只在简单回归中成立，多元回归中 R² ≠ r²
- 💡 相关系数 t 检验 = 回归斜率 t 检验 (两者等价)

**考点3：残差图判断假设违反（图形分析题）**
- 残差图 (Residual Plot): 横轴 = 拟合值(X)，纵轴 = 残差(e)
- 四种常见模式：
  - 散点随机散布在 0 附近 → 假设满足 ✓
  - 扇形/喇叭形 (方差随 X 增大) → 异方差 (Heteroskedasticity)
  - 有明显曲线趋势 → 非线性 (Nonlinearity)
  - 残差正负交替有规律 → 序列相关 (Serial Correlation)
- ⚠️ 考试常给残差图让你判断违反了哪个假设

**考点4：置信区间 vs 预测区间**
- 置信区间 (Confidence Interval):
  - 对回归系数的区间估计 (如 β₁ 的 95% CI)
  - 只包含参数估计的不确定性
- 预测区间 (Prediction Interval):
  - 对给定 X 值下 Y 的区间预测
  - 包含两种不确定性: 参数估计 + 随机误差项 eᵢ
  - 因此预测区间比置信区间更宽
- 两个区间的共同点:
  - 在 X = x̄ 处最窄
  - X 距 x̄ 越远，区间越宽
- ⚠️ 考试高频题: "为什么预测区间比置信区间宽？"

**考点5：回归假设违反的后果**
- 异方差 (Heteroskedasticity):
  - 系数仍然无偏 (Unbiased) ✓
  - 但标准误有偏 → t 检验不可靠 ✗
  - 常见于横截面数据
- 序列相关 (Serial Correlation / Autocorrelation):
  - 标准误被低估 → t 统计量被高估 → 更容易错误拒绝 H₀
  - 常见于时间序列数据
- 非线性 (Nonlinearity):
  - 模型设定错误 → 预测有偏
  - 需要使用非线性函数形式 (log, 二次项等)

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| R² 高 = X 导致 Y | R² 高 ≠ 因果关系 | 可能存在虚假回归或遗漏变量 |
| 相关系数 t 检验 df = n-1 | df = n-2 | 回归估计了两个参数（截距+斜率） |
| 预测区间 = 置信区间 | 预测区间比置信区间宽 | 预测区间含残差不确定性 |
| 异方差使系数有偏 | 异方差下系数仍无偏，但标准误有偏 | OLS 无偏性不依赖同方差 |
| 预测区间在各 X 值宽度相同 | 距 x̄ 越远越宽 | 斜率估计的不确定性在远端放大 |
| F 检验可用单边或双边 | F 检验永远是单边（右尾） | F 值非负，大值才拒绝 H₀ |

### 🔄 跨模块关联

- **[[M09-Parametric-and-Non-Parametric-Tests-of-Independence]]** — 相关系数的 t 检验与回归斜率系数的 t 检验完全等价，R² = r²。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 相关系数的概念在 M03 中引入，在回归中扩展为正式斜率检验和 R² 解释。
- **[[M05-Portfolio-Mathematics]]** — 协方差和相关系数是组合方差公式和回归分析的共同组件。
- **[[M08-Hypothesis-Testing]]** — 回归中的 t 检验和 F 检验是 M08 假设检验框架的直接应用。
- **[[M07-Estimation-and-Inference]]** — 回归系数标准误 SE(b₁) 是 M07 标准误概念在回归中的推广。
- **[[M11-Introduction-to-Big-Data-Techniques]]** — 简单线性回归是 ML 中监督学习的最基础模型。

### 📋 复习与刷题提示

- **核心能力**：掌握 OLS 估计、ANOVA 表解读、残差图诊断、置信区间 vs 预测区间
- **必考题型**：ANOVA 表计算、R² 和 SEE 计算、残差图判断、回归系数 t 检验
- **最常犯错误**：相关系数 df 记错、预测区间与置信区间混淆、R² 误认为因果关系
- 记忆口诀：
  - OLS：b₁ = Cov/Var，b₀ = ȳ - b₁x̄
  - R² = SSR/SST = 1 - SSE/SST
  - 简单回归：F = t²，R² = r²
  - 残差图诊断：喇叭 = 异方差，曲线 = 非线性，序列 = 自相关
- 刷题建议：ANOVA 表计算题是 CFA 高频题，务必熟练掌握
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
