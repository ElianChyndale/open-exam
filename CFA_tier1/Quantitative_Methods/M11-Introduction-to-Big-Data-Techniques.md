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

### 🌳 核心知识树

```text
🏆 M11: Introduction to Big Data Techniques（大数据与机器学习）
│
├── ⭐ 金融科技数据背景 (Fintech Data Context)
│   ├── 结构化数据: 表格形式（股价、财务比率）— 易分析
│   ├── 非结构化数据: 文本、图像、音频 — NLP/图像处理
│   ├── 替代数据 (Alternative Data): 卫星图、信用卡、物流数据
│   └── 四个 V: Volume(体量), Velocity(速度), Variety(多样性), Veracity(真实性)
│
├── ⭐ 三种机器学习类型 (Three ML Types)
│   ├── 📌 监督学习 (Supervised): 有标签数据, X→Y
│   │   ├── 回归: 预测连续值（线性回归）
│   │   └── 分类: 预测类别（逻辑回归、SVM、决策树）
│   ├── 📌 非监督学习 (Unsupervised): 无标签数据, 发现模式
│   │   ├── 聚类: K-Means、层次聚类
│   │   └── 降维: PCA
│   └── 📌 强化学习 (Reinforcement): Agent+环境+奖励 → 最优策略
│       └── 应用: 算法交易、游戏 AI
│
├── ⭐ 深度学习 (Deep Learning)
│   ├── ML 子集，多层神经网络
│   ├── 擅长非结构化数据（图像、文本、语音）
│   └── 代表: CNN, RNN, Transformer
│
├── ⭐ 过拟合 (Overfitting)
│   ├── 训练集好 + 验证集差 = 过拟合
│   ├── 📌 本质: 学到噪声而非信号
│   ├── 📌 原因: 模型复杂、样本少、特征多
│   └── 📌 解决: 交叉验证、正则化、简化模型
│
├── ⭐ 投资应用 (Investment Applications)
│   ├── 研究: NLP 分析财报情绪、因子挖掘
│   ├── 风险管理: 欺诈检测、异常交易识别
│   ├── 运营: 算法交易、自动化报告
│   └── 客户分析: 细分、流失预测、个性化建议
│
├── 💡 关键洞察
│   ├── 监督 vs 非监督: 决定因素是"是否有标签"
│   ├── ML 预测能力强，但不揭示因果关系
│   ├── 复杂模型 ≠ 好模型 — 过拟合是普遍问题
│   ├── 数据量大 ≠ 决策好 — GIGO 原则始终适用
│   └── 黑箱风险（不可解释）与过拟合（泛化差）是两个不同概念
│
└── ⚠️ 考试陷阱总结
    ├── Big Data 不自动 = Better Decisions (GIGO)
    ├── ML 不是因果分析（预测 ≠ 因果）
    ├── 样本外验证不可或缺
    ├── 黑箱风险 ≠ 过拟合 — 两个不同概念
    ├── 数据隐私与伦理合规（GDPR 等）
    └── 监督/非监督/强化学习的三分类
```

## 📖 知识点详解

### 知识点1：金融科技数据背景（Fintech Data Context）
**核心概念**：金融科技的发展产生了大量新型数据源，深刻改变了投资分析的方式。理解数据类型和大数据特征是运用现代数据分析技术的前提。
- **结构化数据**：以表格形式组织的定量数据（股价、财务比率），易于存储和分析
- **非结构化数据**：无预定义格式的文本、图像、音频（新闻文章、社交媒体帖子、电话会议记录）
- **替代数据（Alternative Data）**：传统数据源之外的信息（卫星图像、信用卡交易、物流数据、网络搜索趋势）
- **四个 V**：Volume（体量）、Velocity（速度）、Variety（多样性）、Veracity（真实性）
- **应用领域**：研究（信号提取）、风险管理、运营（算法交易）、客户分析（个性化建议）

**考试应用**：区分数据类型（结构化/非结构化/替代数据），理解四个 V 的概念。

### 知识点2：大数据/AI/ML 定义（Big Data, AI, and ML Definitions）
**核心概念**：人工智能（AI）是让机器模拟人类智能的广义领域，机器学习（ML）是 AI 的子集，关注让机器从数据中学习模式和规律。
- **监督学习（Supervised Learning）**：使用带标签的数据训练，任务包括回归（预测连续值）和分类（预测类别标签）
- **非监督学习（Unsupervised Learning）**：使用无标签数据，让算法自行发现数据中的结构，任务包括聚类和降维
- **强化学习（Reinforcement Learning）**：智能体通过与环境交互、奖励信号学习最优策略
- **深度学习（Deep Learning）**：ML 的子集，使用多层神经网络，擅长处理非结构化数据

**考试应用**：给定具体任务判断使用哪种学习方法（有标签 → 监督，无标签 → 非监督）。

### 知识点3：过拟合与投资应用（Overfitting and Investment Applications）
**核心概念**：过拟合是机器学习中最常见的问题，模型学到噪声而非信号。大数据技术在投资管理中有广泛的应用。
- **过拟合表现**：训练集表现好 + 验证集差 = 过拟合；原因：模型复杂、样本少、特征多
- **解决方法**：交叉验证、正则化、简化模型
- **投资应用**：NLP 分析财报情绪、因子挖掘、欺诈检测、算法交易、客户细分
- ⚠️ Big Data 不自动 = Better Decisions（GIGO 原则始终适用）
- ⚠️ ML 预测能力强但不揭示因果关系——预测 ≠ 因果
- ⚠️ 样本外验证不可或缺

**考试应用**：识别过拟合迹象，理解交叉验证的作用，区分监督/非监督/强化学习。

### 📐 关键公式表

| 概念 | 解释 | 应用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| Supervised Learning | 带标签数据训练 X→Y | 股价预测（回归）、信用分类 | 需要高质量标签数据 |
| Unsupervised Learning | 无标签数据发现模式 | 客户细分、异常检测 | 结果难以验证 |
| Reinforcement Learning | Agent+环境+奖励学习策略 | 算法交易、组合优化 | 需要大量交互环境 |
| Deep Learning | 多层神经网络 | 图像识别、NLP、语音 | 数据需求大，黑箱属性强 |
| Overfitting | 学到噪声而非信号 | 所有 ML 模型的陷阱 | 用交叉验证诊断 |
| Cross-Validation | 训练/验证数据分离 | 模型选择、超参数调优 | 防止数据泄露 |

### 🛠️ 常见考点与解题思路

**考点1：监督 vs 非监督 vs 强化学习分类**
- 规则：有标签 × 已知输出 → 监督学习
- 无标签 × 发现模式 → 非监督学习
- Agent × 环境 × 奖励 → 强化学习
- ⚠️ 给定具体任务判断学习类型是 CFA 必考

**考点2：过拟合识别与应对**
- 症状：训练集表现好 + 验证集/测试集表现差
- 诊断：学习曲线 (Learning Curve)、交叉验证
- 应对：正则化、简化模型、更多训练数据
- ⚠️ 过拟合是 ML 中最常见的问题

**考点3：结构化 vs 非结构化数据**
- 数据库表格、CSV → 结构化
- 新闻文章、社交媒体 → 非结构化
- JSON、XML → 半结构化
- ⚠️ 考试常给数据源让你判断结构类型

**考点4：替代数据的投资应用**
- 卫星图像 → 停车场车流量 → 零售收入预测
- 信用卡交易 → 消费趋势分析
- 物流数据 → 供应链效率判断
- 网络搜索趋势 → 投资者情绪指标

**考点5：数据相关风险与伦理**
- GIGO: 数据质量差 → 结论质量差
- 预测 ≠ 因果: ML 不揭示因果关系
- 黑箱风险: 复杂模型难以解释
- 隐私合规: GDPR、数据伦理

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| Big Data 自动 = 更好决策 | 数据量大但质量差 → GIGO（垃圾进垃圾出） | 数据质量比数据量更重要 |
| ML 模型揭示因果关系 | ML 预测能力强，但不一定揭示因果关系 | 相关性 ≠ 因果性 |
| 黑箱风险 = 过拟合 | 黑箱风险是模型不可解释，过拟合是泛化差 | 两个不同问题：简单模型也可能过拟合 |
| 模型越复杂越好 | 复杂模型更容易过拟合，简单模型往往是更好起点 | Occam's Razor: 简单优先 |
| 非监督学习需要标签 | 非监督学习恰恰不需要标签 | 监督学习才需要标签 |
| 替代数据 = 非结构化数据 | 替代数据可以是结构化或非结构化的 | 替代数据是按"来源"分类，不是按格式 |

### 🔄 跨模块关联

- **[[M10-Simple-Linear-Regression]]** — 线性回归是监督学习中最基础的模型。R²、F 检验、残差诊断等在 ML 中同样重要。
- **[[M07-Estimation-and-Inference]]** — 样本外验证、交叉验证基于抽样理论。训练/验证/测试集拆分是估计方法论的延伸。
- **[[M04-Probability-Trees-and-Conditional-Expectations]]** — 贝叶斯方法在 ML 中有广泛应用（朴素贝叶斯分类器）。
- **[[M03-Statistical-Measures-of-Asset-Returns]]** — 过拟合诊断依赖于对偏差 (Bias) 和方差 (Variance) 的理解 — Bias-Variance Tradeoff。
- **[[M06-Simulation-Methods]]** — Bootstrap 在 ML 集成学习中重要使用（如 Random Forest 的 Bagging）。

### 📋 复习与刷题提示

- **核心能力**：区分三种 ML 类型（监督/非监督/强化），理解过拟合的本质和应对方法
- **必考题型**：ML 类型分类、过拟合识别、替代数据应用、数据结构判断
- **最常犯错误**：监督/非监督/强化分类混淆、黑箱风险与过拟合混为一谈、认为 Big Data = 好决策
- 记忆口诀：
  - 有标签 = 监督，无标签 = 非监督，有环境+奖励 = 强化
  - 过拟合：训练好，验证差 = 学噪声
  - GIGO：垃圾进，垃圾出
  - 预测 ≠ 因果：ML 找相关，不找原因
- 刷题建议：本模块概念题为主，重点掌握 ML 三分类和过拟合的识别与应对
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
