---
title: "M11: Introduction to Big Data Techniques"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M11"
official_module: "Module 11: Introduction to Big Data Techniques"
los_count: 3
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M11: Introduction to Big Data Techniques

## 0. Reading Contract 学习契约

- **Official module**: Module 11: Introduction to Big Data Techniques.
- **Official pages**: Learning Outcomes; 11.01 Introduction; 11.02 How Is Fintech used in Quantitative Investment Analysis?; 11.03 Advanced Analytical Tools: Artificial Intelligence and Machine Learning; 11.04 Tackling Big Data with Data Science.
- **LOS contract**: describe fintech aspects relevant to gathering/analyzing financial data; describe Big Data, AI, ML; describe Big Data/Data Science applications in investment management.
- **Evidence rule**: classify misses by data type, ML category, investment application, or model-risk/governance issue.

## 1. Module Brief 模块定位

M11 is concept-heavy but not optional: it tests whether you can classify data, identify ML method families, and audit model risk. 中文上它的核心是“先看有没有标签，再看数据治理，再看投资用途是否被验证”。

## 2. Curriculum Spine 教材正文主线

1. **How Is Fintech used in Quantitative Investment Analysis?**: fintech expands data gathering, processing, research, risk management, operations, and client analytics.
2. **Big Data**: data may be structured, semi-structured, or unstructured; alternative data includes satellite, transaction, web, logistics, search, and text sources.
3. **Big Data Challenges**: volume, velocity, variety, veracity, privacy, permission, bias, and infrastructure constraints must be managed.
4. **Advanced Analytical Tools: AI and ML**: supervised, unsupervised, reinforcement, and deep learning differ by labels, objective, and feedback structure.
5. **Tackling Big Data with Data Science**: data processing, visualization, text analytics, and NLP transform raw data into investment signals.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| table of prices, accounting variables | structured data | "Clean table data, easy to model directly." |
| news, transcript, image, audio | unstructured data | "Needs feature extraction such as NLP or image processing." |
| labels exist | supervised learning | "Regression for continuous target; classification for category target." |
| no labels, find groups | unsupervised learning | "Clustering or dimensionality reduction." |
| agent acts and receives reward | reinforcement learning | "Learns a policy from reward feedback." |
| training high, test poor | overfitting | "Model learned noise, not stable signal." |
| many backtests tried | data snooping | "Significance may be mined from noise." |

## 4. Formula & Decision Bench 公式与决策台

| Framework | Use | Trap check |
|---|---|---|
| Four Vs: volume, velocity, variety, veracity | Big Data characterization | Veracity is data quality/trustworthiness, not speed. |
| Structured / semi-structured / unstructured | data classification | JSON/XML are semi-structured; text/images are unstructured. |
| Supervised learning | labeled X -> Y | Regression vs classification depends on target type. |
| Unsupervised learning | unlabeled pattern discovery | Clusters need business interpretation. |
| Reinforcement learning | action -> reward -> policy | Backtest environment must reflect costs and constraints. |
| Cross-validation / out-of-sample testing | model validation | In-sample fit is insufficient. |
| Model-risk checklist | data permission, bias, overfitting, explainability, monitoring | Sophisticated model does not equal reliable model. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `data_type`, `alternative_data`, `supervised_unsupervised`, `reinforcement_learning`, `overfitting`, `data_snooping`, `model_governance`.
- Future records should preserve the task description because labels/no labels and output type drive most answers.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Alternative data assumed superior | It may be noisy, biased, costly, or legally constrained. |
| Supervised learning chosen without labels | Supervised learning requires labeled targets. |
| Clustering treated as causal classification | Clusters are model-discovered groups needing interpretation. |
| High training performance accepted as proof | Check validation/test performance and out-of-sample stability. |
| Complex model treated as automatically better | Complexity increases governance and explainability burden. |

## 7. Final Recall Sheet 最后回忆页

- Big Data: volume, velocity, variety, veracity.
- Data types: structured, semi-structured, unstructured.
- Labels? Yes -> supervised; no -> unsupervised; reward feedback -> reinforcement.
- Continuous target -> regression; category target -> classification.
- Key risks: overfitting, data snooping, look-ahead bias, sample bias, privacy/permission, poor explainability.
