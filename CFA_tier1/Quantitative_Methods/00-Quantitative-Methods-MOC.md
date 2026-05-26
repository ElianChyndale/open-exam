---
title: "00-Quantitative Methods-MOC"
description: "CFA Level I 2026 Quantitative Methods 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module_count: 11
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Quantitative_Methods
---

# Quantitative Methods MOC

> **一句话核心**：把投资问题翻译成收益率、现金流、统计推断和模型检验。

---

## 1. 科目定位

- **考试权重**：6-9%
- **官方模块数**：11
- **主线框架**：定义变量 -> 选择统计/现金流工具 -> 计算结果 -> 解释经济含义 -> 检查假设
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |
|---|---|---|---|---|
| M01 | Rates and Returns | 计算+解释 | Introduction / Interest Rates and Time Value of Money | [[M01-Rates-and-Returns]] |
| M02 | Time Value of Money in Finance | 计算+解释 | Introduction / Time Value of Money in Fixed Income and Equity | [[M02-Time-Value-of-Money-in-Finance]] |
| M03 | Statistical Measures of Asset Returns | 计算+解释 | Introduction / Measures of Central Tendency and Location | [[M03-Statistical-Measures-of-Asset-Returns]] |
| M04 | Probability Trees and Conditional Expectations | 计算+解释 | Introduction / Expected Value and Variance | [[M04-Probability-Trees-and-Conditional-Expectations]] |
| M05 | Portfolio Mathematics | 计算+解释 | Introduction / Portfolio Expected Return and Variance of Return | [[M05-Portfolio-Mathematics]] |
| M06 | Simulation Methods | 计算+解释 | Introduction / Lognormal Distribution and Continuous Compounding | [[M06-Simulation-Methods]] |
| M07 | Estimation and Inference | 概念+案例判断 | Introduction / Sampling Methods | [[M07-Estimation-and-Inference]] |
| M08 | Hypothesis Testing | 计算+解释 | Introduction / Hypothesis Tests for Finance | [[M08-Hypothesis-Testing]] |
| M09 | Parametric and Non-Parametric Tests of Independence | 计算+解释 | Introduction / Tests Concerning Correlation | [[M09-Parametric-and-Non-Parametric-Tests-of-Independence]] |
| M10 | Simple Linear Regression | 计算+解释 | Introduction / Estimation of the Simple Linear Regression Model | [[M10-Simple-Linear-Regression]] |
| M11 | Introduction to Big Data Techniques | 概念+应用 | Introduction / How Is Fintech used in Quantitative Investment Analysis? | [[M11-Introduction-to-Big-Data-Techniques]] |

## 3. 核心知识树

```text
Quantitative Methods (6-9%)
├─ 1. Rates and Returns
│  ├─ 1.1 Introduction
│  ├─ 1.2 Interest Rates and Time Value of Money
│  ├─ 1.3 Rates of Return
├─ 2. Time Value of Money in Finance
│  ├─ 2.1 Introduction
│  ├─ 2.2 Time Value of Money in Fixed Income and Equity
│  ├─ 2.3 Implied Return and Growth
├─ 3. Statistical Measures of Asset Returns
│  ├─ 3.1 Introduction
│  ├─ 3.2 Measures of Central Tendency and Location
│  ├─ 3.3 Measures of Dispersion
├─ 4. Probability Trees and Conditional Expectations
│  ├─ 4.1 Introduction
│  ├─ 4.2 Expected Value and Variance
│  ├─ 4.3 Probability Trees and Conditional Expectations
├─ 5. Portfolio Mathematics
│  ├─ 5.1 Introduction
│  ├─ 5.2 Portfolio Expected Return and Variance of Return
│  ├─ 5.3 Forecasting Correlation of Returns: Covariance Given a Joint Probability Function
├─ 6. Simulation Methods
│  ├─ 6.1 Introduction
│  ├─ 6.2 Lognormal Distribution and Continuous Compounding
│  ├─ 6.3 Monte Carlo Simulation
├─ 7. Estimation and Inference
│  ├─ 7.1 Introduction
│  ├─ 7.2 Sampling Methods
│  ├─ 7.3 Central Limit Theorem and Inference
├─ 8. Hypothesis Testing
│  ├─ 8.1 Introduction
│  ├─ 8.2 Hypothesis Tests for Finance
│  ├─ 8.3 Tests of Return and Risk in Finance
├─ 9. Parametric and Non-Parametric Tests of Independence
│  ├─ 9.1 Introduction
│  ├─ 9.2 Tests Concerning Correlation
│  ├─ 9.3 Tests of Independence Using Contingency Table Data
├─ 10. Simple Linear Regression
│  ├─ 10.1 Introduction
│  ├─ 10.2 Estimation of the Simple Linear Regression Model
│  ├─ 10.3 Assumptions of the Simple Linear Regression Model
├─ 11. Introduction to Big Data Techniques
│  ├─ 11.1 Introduction
│  ├─ 11.2 How Is Fintech used in Quantitative Investment Analysis?
│  ├─ 11.3 Advanced Analytical Tools: Artificial Intelligence and Machine Learning
```

## 4. 跨模块依赖关系

- **M01 Rates and Returns**：承接 `本科目入口`，输出到 `Time Value of Money in Finance`。
- **M02 Time Value of Money in Finance**：承接 `Rates and Returns`，输出到 `Statistical Measures of Asset Returns`。
- **M03 Statistical Measures of Asset Returns**：承接 `Time Value of Money in Finance`，输出到 `Probability Trees and Conditional Expectations`。
- **M04 Probability Trees and Conditional Expectations**：承接 `Statistical Measures of Asset Returns`，输出到 `Portfolio Mathematics`。
- **M05 Portfolio Mathematics**：承接 `Probability Trees and Conditional Expectations`，输出到 `Simulation Methods`。
- **M06 Simulation Methods**：承接 `Portfolio Mathematics`，输出到 `Estimation and Inference`。
- **M07 Estimation and Inference**：承接 `Simulation Methods`，输出到 `Hypothesis Testing`。
- **M08 Hypothesis Testing**：承接 `Estimation and Inference`，输出到 `Parametric and Non-Parametric Tests of Independence`。
- **M09 Parametric and Non-Parametric Tests of Independence**：承接 `Hypothesis Testing`，输出到 `Simple Linear Regression`。
- **M10 Simple Linear Regression**：承接 `Parametric and Non-Parametric Tests of Independence`，输出到 `Introduction to Big Data Techniques`。
- **M11 Introduction to Big Data Techniques**：承接 `Simple Linear Regression`，输出到 `本科目总结`。

## 5. 核心对比专题

- **概念 vs 应用**：先确认官方定义，再把定义放入题干情境判断。
- **计算 vs 解释**：计算结果只是中间步骤，CFA Level I 经常要求解释方向、限制和投资含义。
- **静态知识 vs 决策流程**：把每个模块压缩成“输入 -> 工具 -> 输出 -> 陷阱”的流程。
- **英文术语 vs 中文理解**：英文保留用于识题，中文解释用于防止机械背诵。

## 6. 公式与框架速查

| 编号 | 工具 / Formula | 中文用途 |
|---|---|---|
| F1 | `HPR: HPR = (P1 - P0 + D1) / P0` | 持有期收益率，注意价格变动和期间现金流都要纳入。 |
| F2 | `Effective annual rate: EAR = (1 + periodic rate)^m - 1` | 不同复利频率比较时必须转成同一口径。 |
| F3 | `Present value: PV = FV / (1 + r)^N` | 折现率越高，现值越低。 |
| F4 | `Variance: σ² = Σ(xi - xbar)² / (n - 1)` | 样本方差分母通常用 n-1。 |
| F5 | `Test statistic: test statistic = (sample statistic - hypothesized value) / standard error` | 先判断单尾/双尾，再与临界值或 p-value 比较。 |
| F6 | `Simple regression: Yi = b0 + b1Xi + ei` | b1 表示 X 增加 1 单位时 Y 的预期变化。 |

## 7. 高频考试陷阱

- **模块名和旧笔记不一致**：以 2026 官方 module 名称、编号和顺序为准。
- **只背公式不解释**：凡是 `calculate and interpret`，必须同时会算和解释。
- **忽略 LOS 动词**：`describe`、`explain`、`compare`、`evaluate` 对答案深度要求不同。
- **跨模块断裂**：做错题时记录它关联到哪个 MOC 节点，必要时触发 MOC gap review。

## 8. 通用分析框架

1. **识别任务**：读 LOS 动词和题干问法。
2. **定位节点**：回到 `## 3. 核心知识树` 的编号节点。
3. **选择工具**：概念框架、公式、表格比较或合规流程。
4. **输出结论**：中文结论 + 英文关键词 + 必要限制条件。
5. **复盘缺口**：若错因重复出现，进入 `.system/events/` 和 `.system/memory/` 闭环。

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

- 本科目高置信 legacy 映射：11 条；中置信候选：33 条。
- 详细来源与处理建议见 [[cfa-legacy-to-official-enrichment-map]]。
- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。
