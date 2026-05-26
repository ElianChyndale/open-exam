---
title: "M03 — Market Efficiency"
description: "CFA Level I 2026 official module: Market Efficiency"
module: M03
subject: "Equity Investments"
topic_area: Equity
curriculum_year: 2026
official_module: "Module 3: Market Efficiency"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Equity
  - official_2026
---

# M03: Market Efficiency

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Market Efficiency
- 3.01 | Introduction
- 3.02 | The Concept of Market Efficiency
- 3.03 | Factors Affecting Market Efficiency Including Trading Costs
- 3.04 | Forms of Market Efficiency
- 3.05 | Implications of the Efficient Market Hypothesis
- 3.06 | Market Pricing Anomalies - Time Series and Cross-Sectional
- 3.07 | Other Anomalies, Implications of Market Pricing Anomalies
- 3.08 | Behavioral Finance
- 3.09 | Summary

## Learning Outcome Statements

The candidate should be able to:

- describe market efficiency and related concepts, including their importance to investment practitioners
- contrast market value and intrinsic value
- explain factors that affect a market’s efficiency
- contrast weak-form, semi-strong-form, and strong-form market efficiency
- explain the implications of each form of market efficiency for fundamental analysis, technical analysis, and the choice between active and passive portfolio management
- describe market anomalies
- describe behavioral finance and its potential relevance to understanding market anomalies

## Local Study Notes

### Migrated from `CFA_tier1/Equity/M03-Market-Efficiency.md`

_Alignment score: 1.00. Original official module field: Module 3: Market Efficiency._

#### M03: 市场有效性 (Market Efficiency)

##### 1. 核心知识点

###### 信息集与有效形式 (Information set and forms)
- **弱式有效 (weak form)**：当前价格已反映所有历史价格与成交量信息 — 技术分析无法获得超额收益
- **半强式有效 (semi-strong form)**：当前价格已反映所有公开信息 — 基本面分析无法获得超额收益
- **强式有效 (strong form)**：当前价格已反映所有公开加私有信息 — 内幕交易也无法获得超额收益

###### 启示 (Implications)
- **交易成本 (transaction costs)** 与**套利限制 (limits to arbitrage)** 使实际市场无法完全有效
- **异常现象 (anomalies)** 可能源于**行为偏差 (behavior)**、**风险溢价 (risk)**、**数据挖掘 (data mining)** 或**市场摩擦 (market friction)**
- **市场效率程度指导主动与被动投资选择 (active vs passive choice)**

##### 2. 关键公式

本模块无复杂数学公式，核心是概念判断。

| 概念 | 核心逻辑 |
|------|----------|
| 有效市场假设 (EMH) | 价格反映信息，超额收益不可持续 |
| 异常回报 (Abnormal Return) | `实际收益 - 预期收益（如 CAPM）` |

##### 3. 常见考点与解题思路

- **三步判断法**：① 识别信息类型（历史/公开/私有）→ ② 匹配有效形式（weak/semi-strong/strong）→ ③ 判断主动策略是否仍有 edge
- **异常现象归类**：calendar effect、momentum effect、value effect — 判断它们违反哪一形式

##### 4. 易错点提醒

- **有效 ≠ 价格永远正确**：有效是指扣除成本后难以持续获得超额收益，而非价格不波动
- **半强式有效不意味着基本面分析完全无用**：只是公开信息难以产生持续超额收益
- **异常现象不等于市场无效**：可能是风险补偿、数据挖掘或幸存者偏差

##### 5. 跨模块关联

- **市场效率影响估值方法选择** → [[M08-Equity-Valuation-Concepts]]
- **市场质量依赖微观结构** → [[M01-Market-Organization-and-Structure]]
- **指数构建受市场效率理念影响** → [[M02-Security-Market-Indexes]]
### 🌳 核心知识树

```text
🏆 M03: Market Efficiency（市场有效性）
│
├── ⭐ EMH三形式 (Three Forms) 🎯超高頻
│   ├── 弱式有效 (Weak-Form)
│   │   ├── 价格反映历史价格和成交量
│   │   └── 技术分析无效，基本面分析可能有效
│   ├── 半强式有效 (Semi-Strong Form)
│   │   ├── 价格反映所有公开信息
│   │   └── 基本面分析无效，内幕信息可能有效
│   └── 强式有效 (Strong Form)
│       ├── 价格反映所有公开+私有信息
│       └── 没有任何分析方法能获得超额收益
│
├── ⭐ 异常现象 (Anomalies) 🎯高频
│   ├── 时间序列: 一月效应、周内效应、月末效应
│   ├── 横截面: 规模效应 (Size)、价值效应 (Value)
│   └── 其他: 盈利公告后漂移 (PEAD)、IPO异常
│       ⚠️ 异常可能来自: 风险补偿/数据挖掘/行为偏差
│
├── ⭐ 行为金融学 (Behavioral Finance) 🎯高频
│   ├── 认知偏差 (Cognitive Errors)
│   │   ├── 过度自信 (Overconfidence)
│   │   ├── 确认偏差 (Confirmation Bias)
│   │   ├── 代表性偏差 (Representativeness)
│   │   └── 锚定效应 (Anchoring)
│   └── 情感偏差 (Emotional Biases)
│       ├── 损失厌恶 (Loss Aversion)
│       └── 从众效应 (Herding)
│
├── ⭐ 市场效率的影响因素
│   ├── 投资者数量与多样性
│   ├── 交易成本（越低越有效）
│   ├── 信息传播速度（越快越有效）
│   └── 套利限制 (Limits to Arbitrage) ⚠️
│
└── ⭐ 投资策略含义
    ├── 弱式有效 → 技术分析失效 → 主动管理可能有效
    ├── 半强式有效 → 技术+基本面均失效 → 被动指数投资
    └── 强式有效 → 所有主动策略失效 → 只能被动投资
```

## 📖 知识点详解

### 知识点1：有效市场假说的三种形式（Three Forms of EMH）
**核心概念**：有效市场假说（EMH）根据价格反映的信息集将市场效率分为三个层次。弱式有效认为当前价格已包含所有历史价格和成交量信息，因此技术分析无法持续获得超额收益。半强式有效认为价格已反映所有公开信息（财务报表、新闻公告等），因此基本面分析也无法持续获得超额收益。强式有效认为价格已反映所有公开和非公开（内幕）信息，即使内幕交易也无法获得超额收益。
- 弱式有效（Weak-Form）：价格反映历史交易数据，技术分析无效
- 半强式有效（Semi-Strong Form）：价格反映所有公开信息，基本面分析无效
- 强式有效（Strong Form）：价格反映所有公开+私有信息，任何分析均无效
- 📐 超额收益（Abnormal Return）= 实际收益 - 预期收益（如CAPM）
**考试应用**：三步判断法——先识别题干中的信息类型（历史/公开/内幕），再匹配对应的有效形式，最后判断哪种分析方法仍然有效。这是最高频考点。

### 知识点2：市场效率的影响因素（Factors Affecting Market Efficiency）
**核心概念**：市场的有效程度不是绝对的，受多种因素影响。投资者数量越多、多样性越强，市场越有效——因为更多的参与者意味着更多的信息和更激烈的竞争。交易成本越低、信息传播速度越快，市场越有效。套利限制（Limits to Arbitrage）是市场无法完全有效的重要原因——即使价格偏离内在价值，套利者也面临基本面风险、执行成本、噪音交易者风险等障碍，导致错误定价难以被立刻纠正。
- 投资者数量与多样性：参与者越多，信息越充分
- 交易成本：成本越低，套利越容易，市场越有效
- 信息传播速度：信息传播越快，价格调整越及时
- 套利限制：基本面风险、执行成本、噪音交易者风险、模型风险
**考试应用**：判断给定因素对市场效率的影响方向。特别注意套利限制的四种来源及其如何导致市场持续无效。

### 知识点3：市场异常现象（Market Anomalies）
**核心概念**：市场异常是指与有效市场假说预测不符的、可重复出现的价格模式。时间序列异常如一月效应（一月份小盘股表现优于大盘）、周内效应（周一收益率偏低）、年末效应等。横截面异常包括规模效应（小盘股长期跑赢大盘股）、价值效应（低P/B股票跑赢高P/B股票）。事件相关异常如盈利公告后漂移（PEAD——利好公告后股价持续上涨）。
- 时间序列异常：一月效应、周内效应、月末效应
- 横截面异常：规模效应（Size Effect）、价值效应（Value Effect）
- 事件异常：盈利公告后漂移（PEAD）、IPO异常
- 异常的可能解释：风险补偿、数据挖掘（Data Mining）、行为偏差
**考试应用**：判断给定异常现象的类型（时间序列/横截面/事件）。常考将异常归类到对应的EMH形式中。注意异常现象不等于市场无效——可能是风险溢价或数据挖掘所致。

### 知识点4：行为金融学（Behavioral Finance）
**核心概念**：行为金融学研究发现投资者在决策过程中存在系统性认知偏差和情感偏差。认知偏差包括过度自信（高估自身判断能力，导致过度交易）、确认偏差（只关注支持自身观点的信息）、代表性偏差（过度依赖小样本推断整体）和锚定效应（过度依赖初始信息）。情感偏差包括损失厌恶（同等金额的亏损比盈利带来的心理影响更大）和从众效应（跟随大众行为）。
- 认知偏差（Cognitive Errors）：过度自信、确认偏差、代表性偏差、锚定效应
- 情感偏差（Emotional Biases）：损失厌恶、从众效应、过度乐观
- 偏差对市场的影响：可能导致错误定价和异常现象
**考试应用**：给定投资者行为描述，判断属于哪种偏差。核心区分：认知偏差来自信息处理错误（可纠正），情感偏差来自直觉/情绪（更难纠正）。

### 知识点5：投资策略含义（Implications for Investment Strategies）
**核心概念**：市场效率程度直接指导投资者的策略选择。弱式有效市场下技术分析失效但基本面分析可能有效，主动管理仍有存在价值。半强式有效市场下技术和基本面分析均失效，被动指数投资为更优选择。强式有效市场下所有主动策略均无法获得超额收益，只能选择被动投资。实际上市场效率是一个连续谱，不同市场（发达 vs 新兴）、不同证券（大盘股 vs 小盘股）的信息效率各不相同。
- 弱式有效 → 技术分析失效 → 主动管理可能有效（基本面分析）
- 半强式有效 → 技术+基本面均失效 → 被动指数投资
- 强式有效 → 所有主动策略失效 → 只能被动投资
- 现实中：发达市场大盘股接近半强式，小盘股和新兴市场效率较低
**考试应用**：给定市场有效形式，判断推荐的投资策略。注意市场效率是连续谱而非二元分类。考虑费用后的净收益才是投资者真正获得的回报。

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| Abnormal Return = Actual Return - Expected Return | 超额收益 | 检验市场效率的基本指标 | 预期收益模型（如CAPM）的选择影响结果 |
| Risk-Adjusted Return = (R_p - R_f) / β | 风险调整后收益 | 比较不同风险水平下的表现 | 系数估计可能不准确 |
| Market Model: R_i = α_i + β_i R_m + ε_i | 市场模型 | 分离系统性风险和公司特定收益 | α>0表示超额收益 |
| EMH测试中的正反例 | 若α显著≠0，则市场可能无效 | 检验EMH的统计方法 | 需考虑交易成本后的净收益 |

### 🛠️ 常见考点与解题思路

**Topic 1: EMH三种形式判断**
- 三步法：① 识别信息类型（历史/公开/私有）→ ② 匹配有效形式 → ③ 判断策略是否有效
- 题眼："past prices" → Weak Form；"public information" → Semi-Strong；"inside information" → Strong

**Topic 2: 异常现象归类**
- Calendar: January Effect, Monday Effect
- Fundamental: Value Premium, Size Effect
- Event: PEAD (Post-Earnings Announcement Drift)
- 解题：判断异常属于时间序列、横截面还是事件驱动

**Topic 3: 行为偏差辨析**
- 题目描述投资者行为，判断属于哪种偏差
- Overconfidence: 过度交易、低估风险
- Confirmation Bias: 只关注支持自己观点的信息
- Herding: 跟随大众
- Anchoring: 过度依赖初始信息

**Topic 4: 被动vs主动投资选择**
- 市场越有效 → 越应选择被动投资
- 市场越无效 → 主动管理越有可能创造价值
- 但需考虑费用后的净收益

**Topic 5: 套利限制**
- 即使价格偏离价值，套利也可能受限
- 原因：基本面风险、执行成本、噪音交易者风险、资金约束

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 有效市场 = 价格永远正确 | 有效是指难以持续获得超额收益 | 价格可能偏离价值，但套利难以纠正 |
| 异常现象 = 市场无效 | 异常可能来自风险补偿或数据挖掘 | 需统计显著且经济显著才表明无效 |
| 半强式有效意味着基本面分析完全无用 | 基本面分析有助于理解风险，只是难以获得持续alpha | 信息已被定价但投资者仍需分析来理解风险 |
| Weak-Form下技术分析完全无用 | 短期内可能有模式，但扣除成本后无法持续获利 | 微小机会被交易成本吞噬 |
| 市场效率是二元分类 | 是连续谱，不同程度市场效率不同 | 新兴市场 vs 发达市场效率不同 |
| 行为偏差只导致错误定价 | 行为偏差也可能被套利者纠正 | 市场有自我修正机制 |

### 🔄 跨模块关联

- **市场效率影响估值方法可靠性** → [[M08-Equity-Valuation-Concepts-and-Basic-Tools]]（有效市场中折现率估计更可靠）
- **市场质量依赖微观结构** → [[M01-Market-Organization-and-Structure]]（流动性越强市场越有效）
- **指数选择影响市场效率检验** → [[M02-Security-Market-Indexes]]（基准选择影响alpha判断）
- **行业分析中的市场效率** → [[M06-Industry-and-Competitive-Analysis]]（竞争格局影响信息效率）
- **公司分析中的效率含义** → [[M05-Company-Analysis-Past-and-Present]]（历史业绩能否预测未来）
- **行为偏差与预测** → [[M07-Company-Analysis-Forecasting]]（分析师偏差影响预测质量）
- **地缘政治与市场效率** → Economics M05（突发事件的信息吸收速度）

### 📋 复习与刷题提示

- **EMH三形式对比**：这是最高频考点。记住每种形式的价格反映信息集和策略含义
- **异常现象归类练习**：calendar/event/cross-sectional三种类型的区别
- **行为偏差辨析**：cognitive vs emotional偏差的区别
- **套利限制**：记住四大限制因素（fundamental risk、implementation cost、noise trader risk、model risk）
- **常见题干陷阱**：注意题目问的是"violates which form of EMH?"——先确定信息类型
- **刷题建议**：mock中概念判断型题目为主，计算alpha的题目较少
- **主动vs被动**：理解市场效率程度与投资策略选择的关系

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
