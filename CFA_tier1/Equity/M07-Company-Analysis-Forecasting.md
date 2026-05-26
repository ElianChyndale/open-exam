---
title: "M07 — Company Analysis: Forecasting"
description: "CFA Level I 2026 official module: Company Analysis: Forecasting"
module: M07
subject: "Equity Investments"
topic_area: Equity
curriculum_year: 2026
official_module: "Module 7: Company Analysis: Forecasting"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Equity
  - official_2026
---

# M07: Company Analysis: Forecasting

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Company Analysis: Forecasting
- 7.01 | Introduction
- 7.02 | Forecast Objects, Principles, and Approaches
- 7.03 | Forecasting Revenues
- 7.04 | Forecasting Operating Expenses and Working Capital
- 7.05 | Forecasting Capital Investments and Capital Structure
- 7.06 | Scenario Analysis

## Learning Outcome Statements

The candidate should be able to:

- explain principles and approaches to forecasting a company’s financial results and position
- explain approaches to forecasting a company’s revenues
- explain approaches to forecasting a company’s operating expenses and working capital
- explain approaches to forecasting a company’s capital investments and capital structure
- describe the use of scenario analysis in forecasting

## Local Study Notes

### Migrated from `CFA_tier1/Equity/M07-Company-Analysis-Forecasting.md`

_Alignment score: 1.00. Original official module field: Module 7: Company Analysis: Forecasting._

#### M07: 公司分析：预测 (Company Analysis: Forecasting)

##### 1. 核心知识点

###### 预测主干 (Forecast spine)
- **自上而下 (top-down)**：从宏观经济 → 行业增长 → 公司市场份额，推导收入
- **自下而上 (bottom-up)**：从产品线销量×价格 → 汇总收入，叠加运营驱动因素
- **逻辑链条**：**收入 (revenue)** → **利润率 (margin)** → **盈利/现金流 (earnings/cash flow)** → **资产负债表需求 (balance-sheet needs)**
- **情景分析 (scenario analysis)**：**基准 (base)**、**乐观 (upside)**、**悲观 (downside)** 三种情景，搭配**催化剂 (catalyst)** 与**风险 (risk)** 地图

###### 预测纪律 (Forecast discipline)
- **增长的资金来源**：**留存收益 (retention)**、**资本回报率 (returns on capital)** 或**外部资本 (external capital)** — 增长必须有融资逻辑
- **预测期选择 (forecast horizon)**：应与**竞争优势持续时间 (competitive advantage durability)** 匹配 — 护城河越宽预测期越长
- **可持续增长率 (sustainable growth rate)**：`g = Retention Ratio × ROE`，反映不改变资本结构下的最大增长率

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 可持续增长率 (Sustainable Growth) | `g = Retention Ratio × ROE` |
| 留存比率 (Retention Ratio) | `1 - Dividend Payout Ratio` |
| 预期增长率 (Expected Growth) | `ROE × (1 - Payout Ratio)` |

##### 3. 常见考点与解题思路

- **增长融资逻辑题**：公司增长是否可持续 → 检查 g vs ROE × Retention Ratio
- **情景敏感性分析**：关键假设变化（市占率、毛利率）对估值的影响
- **预测起点**：通常从最近一年的正常化盈利开始，而非将某异常年份外推

##### 4. 易错点提醒

- **没有假设质量的预测精度只是装饰**：模型越复杂不代表预测越准确
- **增长必须被融资**：高增长但无融资来源就不可持续
- **不要混淆历史增长率与可持续增长率**：历史增长可能来自杠杆扩张而非内生增长

##### 5. 跨模块关联

- **预测驱动估值输入** → [[M08-Equity-Valuation-Concepts]]
- **历史分析为预测提供基准** → [[M05-Company-Analysis-Past-and-Present]]
- **行业结构决定增长假设** → [[M06-Industry-and-Competitive-Analysis]]
### 🌳 核心知识树

```text
🏆 M07: Company Analysis: Forecasting（公司分析：预测）
│
├── ⭐ 预测原则与方法 (Forecast Principles) 🎯高频
│   ├── 自上而下 (Top-Down): 宏观→行业→公司
│   ├── 自下而上 (Bottom-Up): 产品线→经营驱动→汇总
│   ├── 逻辑链: 收入→利润率→盈利→资产负债表
│   └── 预测期应与竞争优势期匹配
│
├── ⭐ 收入预测 (Revenue Forecasting) 🎯高频
│   ├── 量×价分解: Volume + Price/Mix
│   ├── 市场份额方法: 行业规模×公司份额
│   ├── 增长驱动: 有机增长 vs 并购增长
│   └── 情景输入: 价格弹性、客户增长、产品周期
│
├── ⭐ 运营费用预测 (Expense Forecasting)
│   ├── 固定成本: 不随收入变动（租金、折旧）
│   ├── 可变成本: 随收入比例变动（原材料、佣金）
│   ├── 半可变: 阶梯增长（人力）
│   └── 规模效应 (Economies of Scale)
│
├── ⭐ 营运资金预测 (Working Capital Forecast)
│   ├── DSO / DIO / DPO 周转天数
│   ├── 现金转换周期 (CCC) = DSO + DIO - DPO
│   └── ⚠️ 增长需要营运资金投入
│
├── ⭐ 资本投资与结构预测 (Capital & Structure)
│   ├── CapEx: 维护性vs增长性
│   ├── 融资来源: 留存收益、债务、权益
│   └── 资本结构目标: 目标D/E比率
│
├── ⭐ 情景分析 (Scenario Analysis) 🎯高频
│   ├── 基准(Base): 最可能情况
│   ├── 乐观(Upside): 正面意外
│   ├── 悲观(Downside): 负面意外
│   └── 概率加权: Σ(P_i × Scenario Value_i)
│
└── 📐 可持续增长率 (Sustainable Growth) 🎯高频
    └── g = Retention Ratio × ROE
        ⚠️ 保持资本结构不变的内生增长率上限
```

## 📖 知识点详解

### 知识点1：预测原则与方法（Forecast Principles and Approaches）
**核心概念**：公司财务预测是连接历史分析和估值判断的桥梁。自上而下法从宏观经济预测出发，逐步推导行业增长率和公司市场份额，最终得到收入预测。自下而上法从产品线层面的销量和价格出发，逐项汇总到公司整体。逻辑链条为：收入 → 利润率 → 盈利/现金流 → 资产负债表需求。预测期长度应与公司竞争优势持续时间匹配——护城河越宽预测可以越长，因为竞争压力侵蚀超额利润的速度更慢。
- 自上而下（Top-Down）：宏观 → 行业 → 公司，关注外部环境
- 自下而上（Bottom-Up）：产品线 → 公司整体，关注经营细节
- 逻辑链：收入 → 利润率 → 盈利 → 资产负债表
- 预测期选择：与竞争优势期匹配
**考试应用**：判断哪些场景适合自上而下（受宏观影响大的行业）和自下而上（产品线清晰的公司）。注意两种方法可以交叉验证。

### 知识点2：收入预测（Revenue Forecasting）
**核心概念**：收入预测的核心是量×价的分解——分析销量增长（市场份额提升、市场扩张）和价格变化（定价能力、产品组合升级）各自的贡献。常用的方法包括市场份额法（预测行业总规模×公司市场份额）、增长驱动法（识别具体驱动力并建立关联）和产品生命周期法。需要区分有机增长（内生扩张）和并购增长（外延扩张），有机增长通常更可持续。
- 量×价分解：Volume（销量） + Price/Mix（价格/组合）共同驱动收入
- 市场份额法：行业规模 × 公司市场份额变化
- 增长驱动：有机增长（更可持续）vs 并购增长
- 情景输入：价格弹性、客户增长、产品周期阶段
**考试应用**：给定收入增长来源，判断是否有可持续性。大量依赖并购的增长模式风险更高。

### 知识点3：运营费用预测（Expense Forecasting）
**核心概念**：费用预测需要区分成本的行为模式。固定成本（租金、折旧）不随收入变动；可变成本（原材料、佣金）与收入成比例变动；半可变成本（人力）呈阶梯式增长。规模效应（Economies of Scale）意味着随着收入增长，固定成本被摊薄，利润率逐步改善。但规模不经济也可能发生——公司规模过大后管理复杂度和协调成本上升。
- 固定成本：租金、折旧、固定薪酬，不随收入变动
- 可变成本：原材料、佣金、物流成本，随收入比例变动
- 半可变成本：人力成本，阶梯式增长
- 规模效应：收入增长 → 固定成本摊薄 → 利润率改善
**考试应用**：理解成本结构对盈利敏感性的影响。固定成本越高，经营杠杆越大，利润波动性更高。

### 知识点4：营运资金预测（Working Capital Forecasting）
**核心概念**：增长需要营运资金投入——随着收入增加，应收账款和存货通常也增加，消耗现金流。营运资金效率通过周转天数衡量：DSO（应收账款周转天数）、DIO（存货周转天数）、DPO（应付账款周转天数）。现金转换周期（CCC）= DSO + DIO - DPO，表示从支付原材料到收回现金所需的时间，CCC越短对现金流的压力越小。
- 📐 DSO = 应收账款 / (年销售收入 / 365)
- 📐 DIO = 存货 / (年COGS / 365)
- 📐 DPO = 应付账款 / (年COGS / 365)
- 📐 CCC（现金转换周期）= DSO + DIO - DPO
**考试应用**：CCC的计算和分析。缩短CCC的方法：加快收款（降低DSO）、提高存货周转（降低DIO）、延长付款（提高DPO）。

### 知识点5：资本投资与结构预测（Capital Investments and Capital Structure Forecasting）
**核心概念**：资本支出分为维护性和增长性两类，只有增长性CapEx创造未来增长。维护性CapEx通常与折旧接近，可按折旧的一定比例估算；增长性CapEx需与增长假设一致。融资来源有三种：留存收益（内部融资成本最低）、债务融资（利息可抵税但增加财务风险）、权益融资（成本最高但不增加固定义务）。资本结构预测应维持目标D/E比率。
- 维护性CapEx ≈ 折旧金额，维持现有业务运营
- 增长性CapEx：与收入和产能扩张计划相关
- 融资来源：留存收益（内部）< 债务（利息可抵税）< 权益（成本最高）
- 目标资本结构：维持目标D/E比率
**考试应用**：理解增长必须被融资的逻辑。可持续增长率g = ROE × RR是保持资本结构不变下的最大增长率。

### 知识点6：情景分析（Scenario Analysis）
**核心概念**：单一情景预测往往不够全面，情景分析通过基准、乐观和悲观三种情景揭示不同条件下的投资结果。基准情景代表最可能的情况，乐观和悲观情景分别代表正面和负面意外。每个情景需要明确关键假设（市场增长率、市占率、毛利率）的变化并计算对应的财务结果和估值结果。概率加权后的期望值提供更全面的风险收益评估。
- 基准情景（Base Case）：最可能的预测假设
- 乐观情景（Upside Case）：假设正面因素超预期
- 悲观情景（Downside Case）：假设负面因素发生
- 📐 概率加权价值 = Σ(P_i × 情景价值_i)，概率总和必须为100%
**考试应用**：情景分析中识别关键假设变量和判断概率加权期望值。核心在于理解哪些假设变化对估值影响最大（敏感性分析）。

### 知识点7：可持续增长率（Sustainable Growth Rate）
**核心概念**：可持续增长率是在不改变资本结构和融资政策的前提下，公司能够实现的最大增长率。公式为g = 留存比率 × ROE。如果公司的实际增长率超过可持续增长率，则需要外部融资或改变资本结构（提高杠杆或发行新股）。反之，如果实际增长率低于可持续增长率，公司可能积累现金或增加分红。
- 📐 g = 留存比率（Retention Ratio）× ROE
- 留存比率 = 1 - 派息率（Payout Ratio）
- 若实际g > 可持续g → 需要外部融资
- 若实际g < 可持续g → 可能积累现金或增加分红
**考试应用**：可持续增长率计算是必考题。注意历史增长率不等于可持续增长率——历史增长可能来自杠杆扩张而非内生增长。

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| g = Retention Ratio × ROE | 可持续增长率 | 不改变资本结构下最大增长率 | 假设ROE和派息率不变 |
| Retention Ratio = 1 - Payout Ratio | 留存比率 | 公司保留多少利润用于再投资 | 亏损时Retention Ratio无意义 |
| Payout Ratio = Dividends / Net Income | 分红比率 | 公司利润分配比例 | 成熟公司通常更高 |
| 现金转换周期(CCC) = DSO + DIO - DPO | 现金循环周期 | 衡量现金回收效率 | CCC越短越好 |
| DSO = AR / (Annual Sales / 365) | 应收账款周转天数 | 收款效率 | 行业标准差异大 |
| DIO = Inventory / (COGS / 365) | 存货周转天数 | 存货管理效率 | 需考虑行业特性 |
| DPO = AP / (COGS / 365) | 应付账款周转天数 | 付款策略 | 过长可能影响供应商关系 |
| Probability-Weighted Value = Σ(P_i × V_i) | 概率加权期望值 | 情景分析的定量结果 | 概率总和必须=100% |

### 🛠️ 常见考点与解题思路

**Topic 1: 可持续增长率判断**
- 公司增长是否可持续 → 比较实际g vs ROE×RR
- 若g > ROE×RR → 需要外部融资或改变资本结构
- 若g < ROE×RR → 可能积累现金或增加派息

**Topic 2: 自上而下 vs 自下而上**
- Top-Down: 从宏观经济预测出发，逐步推导到公司
- Bottom-Up: 从产品线细节汇总
- 考试可能问哪种方法更适合特定场景

**Topic 3: 情景敏感性分析**
- 识别关键假设：市场增长率、市占率、毛利率
- 改变关键假设输入 → 观察输出变化
- 识别哪些变量对估值影响最大

**Topic 4: 预测起点选择**
- 从最近一年的正常化盈利开始
- 剔除一次性项目（重组费、资产出售）
- 除非有结构性变化，否则以历史趋势为基准

**Topic 5: 增长融资逻辑**
- 增长需要资金来源：内部留存 vs 外部融资
- 高增长但无融资来源 = 不可持续
- 避免混淆历史增长率与可持续增长率

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 没有假设质量的预测精度只是装饰 | 模型越复杂不意味着预测越准确 | GIGO (Garbage In, Garbage Out) |
| 增长不需要融资就能持续 | 增长需要资金来源支撑 | 留存、债务或权益三种来源 |
| 历史增长率=可持续增长率 | 历史增长可能来自杠杆扩张而非内生增长 | 需拆解增长来源 |
| 预测越长越准确 | 预测期越长越不确定 | 竞争优势期决定了可靠预测期 |
| 单一情景足够做投资决策 | 情景分析揭示不同情况下的投资风险 | 多情景提供更全面信息 |
| 收入增长的来源不重要 | 有机增长vs并购增长的可持续性不同 | 有机增长更可持续 |
| CapEx支出都创造增长 | 维护性CapEx仅维持现有业务 | 只有增长性CapEx推动扩张 |
| 会计预测=经济预测 | 会计利润未考虑权益资本成本 | 经济利润才是价值创造的真实衡量 |

### 🔄 跨模块关联

- **预测驱动估值输入** → [[M08-Equity-Valuation-Concepts-and-Basic-Tools]]（g和D₁是GGM输入）
- **历史分析为预测提供基准** → [[M05-Company-Analysis-Past-and-Present]]（正常化盈利是起点）
- **行业结构决定增长假设** → [[M06-Industry-and-Competitive-Analysis]]（行业增长率约束公司增长）
- **可持续增长率与DuPont ROE** → [[M05-Company-Analysis-Past-and-Present]]（g = RR × ROE）
- **情景分析与风险** → [[M03-Market-Efficiency]]（不确定性管理）
- **预测中的经济周期考虑** → Economics M02（经济指标对预测的影响）

### 📋 复习与刷题提示

- **可持续增长率是必考点**：掌握g = RR × ROE的计算和含义
- **Top-Down vs Bottom-Up**：理解两种方法的应用场景和特点
- **正常化盈利调整**：学会从报告盈利中剔除一次性项目
- **增长融资逻辑链**：增长来源 = 留存收益 + 债务融资 + 权益融资
- **营运资金预测**：DSO/DIO/DPO计算和现金转换周期
- **情景分析法**：三个情景的构建和概率加权
- **刷题建议**：mock中可持续增长率计算和概念题为高频
- **易混淆点专项**：历史增长率 vs 可持续增长率 vs 预期增长率

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
