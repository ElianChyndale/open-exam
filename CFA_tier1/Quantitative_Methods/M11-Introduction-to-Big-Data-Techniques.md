---
title: "M11 — Introduction to Big Data Techniques"
description: "CFA Level I 2026 official module: Introduction to Big Data Techniques"
module: M11
subject: "Quantitative Methods"
topic_area: Quantitative_Methods
curriculum_year: 2026
official_module: "Module 11: Introduction to Big Data Techniques"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Quantitative_Methods
  - official_2026
---

# M11: Introduction to Big Data Techniques

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Introduction to Big Data Techniques
- 11.01 | Introduction
- 11.02 | How Is Fintech used in Quantitative Investment Analysis?
- 11.03 | Advanced Analytical Tools: Artificial Intelligence and Machine Learning
- 11.04 | Tackling Big Data with Data Science

## Learning Outcome Statements

The candidate should be able to:

- describe aspects of “fintech” that are directly relevant for the gathering and analyzing of financial data
- describe Big Data, artificial intelligence, and machine learning
- describe applications of Big Data and Data Science to investment management

## Local Study Notes

### Migrated from `CFA_tier1/Quantitative_Methods/M10-Big-Data-and-ML.md`

_Alignment score: 1.00. Original official module field: Module 11: Introduction to Big Data Techniques._

#### M11: Big Data and ML（大数据与机器学习）

##### 1. 核心知识点

###### 1.1 金融科技数据背景（Fintech Data Context）

**数据收集（Data Gathering）**：
- **结构化数据（Structured Data）**：以表格形式组织的定量数据（股价、财务比率、交易量），易于存储和分析
- **非结构化数据（Unstructured Data）**：无预定义格式的文本、图像、音频等（新闻文章、社交媒体帖子、电话会议记录）
- **替代数据（Alternative Data）**：传统数据源之外的信息（卫星图像、信用卡交易、物流数据、网络搜索趋势）

**数据分析在投资过程中的相关性**：
- **研究（Research）**：从海量数据中提取信号以改进投资决策
- **风险管理（Risk Management）**：更准确地识别和量化风险
- **运营（Operations）**：自动化流程、算法交易、降低成本
- **客户分析（Client Analytics）**：个性化推荐、投资者行为分析、客户细分

**数据的四个 V（Four Vs of Big Data）**：
- **Volume（体量）**：数据量极大（TB/PB 级别）
- **Velocity（速度）**：数据产生和处理的速度极快（实时/近实时）
- **Variety（多样性）**：数据类型多样（结构化、非结构化、半结构化）
- **Veracity（真实性）**：数据质量和可信度问题

###### 1.2 大数据 / AI / ML 定义

**人工智能（Artificial Intelligence, AI）**：让机器模拟人类智能的广义领域。包括推理、学习、感知、自然语言处理等。

**机器学习（Machine Learning, ML）**：AI 的子集，关注让机器从数据中学习模式和规律，而不需要显式编程。

**三种主要学习类型（Three Main Types of ML）**：

1. **监督学习（Supervised Learning）**：
   - 使用带标签的数据（Labeled Data）训练模型，输入 X → 输出 Y
   - 目标：学习从 X 到 Y 的映射关系
   - 常见任务：回归（预测连续值）、分类（预测类别标签）
   - 算法举例：线性回归（Linear Regression）、逻辑回归（Logistic Regression）、决策树（Decision Tree）、随机森林（Random Forest）、支持向量机（SVM）

2. **非监督学习（Unsupervised Learning）**：
   - 使用无标签的数据（Unlabeled Data），让算法自行发现数据中的结构或模式
   - 常见任务：聚类（Clustering）、降维（Dimensionality Reduction）
   - 算法举例：K-Means 聚类、主成分分析（PCA）、层次聚类（Hierarchical Clustering）

3. **强化学习（Reinforcement Learning）**：
   - 智能体（Agent）通过与环境的交互，通过奖励信号（Reward Signal）学习最优策略
   - 应用：算法交易、投资组合优化、游戏 AI
   - 核心概念：状态（State）、动作（Action）、奖励（Reward）

**深度学习（Deep Learning）**：
- ML 的子集，使用多层神经网络（Deep Neural Networks）
- 擅长处理非结构化数据（图像、文本、语音）
- 代表架构：CNN（卷积神经网络）、RNN（循环神经网络）、Transformer

###### 1.3 投资应用（Investment Applications）

**研究信号提取（Research Signal Extraction）**：
- 用自然语言处理（NLP）分析财报电话会议记录、新闻情绪
- 从替代数据中提取预测信号
- 因子挖掘（Factor Mining） — 从大量候选因子中发现有效的定价因子

**风险管理（Risk Management）**：
- 欺诈检测（Fraud Detection）
- 异常交易行为识别
- 压力测试情景生成

**运营（Operations）**：
- 算法执行（Algorithmic Execution）
- 自动化报告生成
- 客户服务（聊天机器人）

**客户分析（Client Analytics）**：
- 客户细分（Segmentation）
- 流失预测（Churn Prediction）
- 个性化投资建议

**过拟合（Overfitting）**：
- 模型在训练数据上表现极好，但在新数据（样本外）上表现很差
- 本质：模型学到了数据中的噪声（Noise）而非信号（Signal）
- 原因：模型过于复杂、训练样本太少、特征过多
- 解决：交叉验证（Cross-Validation）、正则化（Regularization）、简化模型

> **【考试陷阱】** 模型 sophistication（复杂程度）不能替代模型验证（Validation）和治理（Governance）。更复杂的模型需要有更严格的验证。

##### 2. 关键公式

本模块以概念理解为主，不涉及复杂公式。关键概念对比如下：

| 概念 | 解释 | 应用场景 |
|------|------|----------|
| Supervised Learning | 用标签数据训练 | 预测股价走势（回归）、信用评级分类 |
| Unsupervised Learning | 发现无标签数据模式 | 客户细分、异常检测 |
| Reinforcement Learning | 通过奖励学习策略 | 算法交易机器人 |
| Overfitting | 学习噪声而非信号 | 所有 ML 模型的通用陷阱 |
| Cross-Validation | 训练/验证数据分离 | 模型选择与超参数调优 |

##### 3. 常见考点与解题思路

**考点一：监督 vs 非监督学习分类**
- 给定一个具体任务，判断使用哪种学习方法
- 规则：是否有标签（Label）？→ 有则监督，无则非监督

**考点二：过拟合识别**
- 训练集表现好，验证集/测试集表现差 → 过拟合
- 可以用学习曲线（Learning Curve）来诊断

**考点三：结构化 vs 非结构化数据**
- 给定数据源，判断其结构类型
- 数据库表格 → 结构化；新闻文章 → 非结构化；JSON/XML → 半结构化

**考点四：替代数据的应用**
- 列举如何将替代数据（Alternative Data）用于投资决策
- 例子：用卫星图像统计停车场车流量来预测零售企业收入

##### 4. 易错点提醒

1. **Big Data 不自动 = Better Decisions**：数据量大但质量差可能导致错误结论（GIGO）。
2. **过拟合的普遍性**：ML 模型越复杂，越容易过拟合。简单模型往往是更好的起点。
3. **ML 不是因果关系分析**：ML 预测能力强但不一定揭示因果关系（预测 ≠ 因果）。
4. **验证不可或缺**：永远需要用样本外数据（Out-of-Sample Data）验证模型。
5. **黑箱风险 vs 过拟合**：复杂的 ML 模型被称为"黑箱"是因为其内部决策过程难以解释（模型复杂度），不是由于 data biases。过拟合是训练数据学得过于精确导致样本外预测不准，与黑箱问题是两个不同的概念——简单模型也可能过拟合，黑箱模型也可能泛化良好。
6. **数据隐私与伦理**：使用客户数据时需要遵守隐私法规（如 GDPR），避免歧视性算法。

##### 5. 跨模块关联

- **[[M09-Correlation-and-Regression]]**：线性回归是监督学习中最基础的模型。R²、F检验、残差诊断等概念在 ML 中同样重要。
- **[[M07-Sampling-and-Estimation]]**：样本外验证、交叉验证的概念基于抽样理论。训练/验证/测试集的拆分是估计方法论的延伸。
- **[[M04-Probability-Concepts]]**：贝叶斯方法在 ML 中有广泛应用（如朴素贝叶斯分类器）。
- **[[M03-Statistical-Measures]]**：过度拟合的诊断依赖于对偏差（Bias）和方差（Variance）的理解 — Bias-Variance Tradeoff。
- **[[M06-Simulation-Methods]]**：Bootstrap 方法在 ML 的集成学习（Ensemble Learning）中被重要使用（如 Random Forest 的 Bagging）。
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
