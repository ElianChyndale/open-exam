---
title: "M02 — Understanding Business Cycles"
description: "CFA Level I 2026 official module: Understanding Business Cycles"
module: M02
subject: "Economics"
topic_area: Economics
curriculum_year: 2026
official_module: "Module 2: Understanding Business Cycles"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Economics
  - official_2026
---

# M02: Understanding Business Cycles

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Understanding Business Cycles
- 2.01 | Introduction
- 2.02 | Overview of the Business Cycle
- 2.03 | Credit Cycles
- 2.04 | Economic Indicators over the Business Cycle

## Learning Outcome Statements

The candidate should be able to:

- describe the business cycle and its phases
- describe credit cycles
- describe how resource use, consumer and business activity, housing sector activity, and external trade sector activity vary over the business cycle and describe their measurement using economic indicators

## Local Study Notes

### Migrated from `CFA_tier1/Economics/M02-Understanding-Business-Cycles.md`

_Alignment score: 1.00. Original official module field: Module 2: Understanding Business Cycles._

#### M02: Understanding Business Cycles（经济周期）

##### 1. 核心知识点（中英双语讲解）

###### 经济周期阶段（Phases of the Business Cycle）

经济周期由四个阶段组成：
1. **扩张（Expansion）**：经济活动上升，GDP增长，就业增加，企业利润改善
2. **顶峰（Peak）**：经济活动达到周期最高点
3. **收缩（Contraction）**：经济活动下降，GDP负增长通常构成衰退（recession）
4. **谷底（Trough）**：经济活动最低点，之后转入下一轮扩张

**衰退的常见定义**：连续两个季度GDP负增长，但NBER官方判定更综合（考虑深度、广度、持续时间）。

###### 各经济变量的周期行为（Cyclical Behavior of Key Variables）

| 变量 | 周期行为 | 时序 |
|------|---------|------|
| 库存（Inventory） | 销售下降时企业被动积累库存；预期改善时主动补库 | 领先 |
| 劳动力（Labor） | 扩张期就业上升，收缩期失业上升；但就业是滞后指标 | 滞后 |
| 住房（Housing） | 利率敏感，通常领先周期 | 领先 |
| 信贷（Credit） | 扩张期信贷扩张，紧缩期信贷收缩 | 领先或同步 |
| 企业利润（Profits） | 高度周期性，与GDP同向 | 同步 |

**库存周期（Inventory Cycle）** 是短期经济波动的重要驱动因素。企业预期转弱时减少库存→订单下降→生产下降→GDP下降。反之亦然。

###### 经济指标分类（Classes of Economic Indicators）

**先行指标（Leading Indicators）**：在整体经济变化之前变动，用于预测周期拐点。
- 包括：制造业平均每周工时、首次申请失业救济人数、新订单、消费者信心指数、房屋开工、股票价格、货币供应量、利差等

**同步指标（Coincident Indicators）**：与整体经济同时变动，确认当前周期位置。
- 包括：非农就业人数、个人收入、工业产值、制造业和贸易销售额

**滞后指标（Lagging Indicators）**：在整体经济变化之后变动，确认周期已发生转变。
- 包括：失业率（平均失业持续时间）、单位劳动成本、银行优惠利率、商业贷款余额

###### 扩散指数与综合指数（Diffusion and Composite Indexes）

- **扩散指数（Diffusion Index）**：衡量有多少成分指标在上升，反映经济变动的广度
- **综合指数（Composite Index）**：将多个指标加权合并为一个数值

使用多个指标而非单一指标可以避免单个数据噪声导致的误判。

###### 信贷渠道与经济周期（Credit Channel and Business Cycles）

信用市场在经济周期中扮演放大器角色：
- **金融加速器（Financial Accelerator）**：经济下行→企业资产负债表恶化→银行惜贷→企业融资困难→投资进一步下降
- 反之，经济上行时信贷扩张放大繁荣

##### 2. 关键公式（公式+解释+场景）

**产出缺口**：`Output Gap = (Actual GDP − Potential GDP) / Potential GDP`
- 场景：判断当前周期位置。正缺口 → 过热阶段（接近顶峰）；负缺口 → 衰退阶段（接近谷底）

**奥肯定律（Okun's Law）**（近似关系）：`ΔUnemployment ≈ −0.5 × (ΔReal GDP − Potential Growth)`
- 场景：GDP增速超出潜在增长率时，失业率下降；反之失业率上升。注意不同国家系数不同，CFA考试中理解方向性关系即可。

##### 3. 常见考点与解题思路

**考点1：区分领先、同步、滞后指标**
- 题干给出某指标的变化趋势，判断处于周期哪个阶段
- 例如：首次申请失业救济人数上升通常领先衰退 → 先行指标
- 失业率持续上升通常在衰退后期才达到峰值 → 滞后指标

**考点2：周期阶段的资产配置含义**
- 扩张早期：股票（cyclical sectors）表现较好
- 扩张晚期：商品和通胀敏感资产
- 衰退期：国债、防御型股票（defensive sectors）
- 注意：CFA L1经济学侧重指标识别，资产配置更多在Portfolio Management中

**考点3：库存周期逻辑**
- 销售下降→库存意外增加→企业减少订单→生产下降→GDP下降
- 销售回升→库存消化→企业增加订单→生产上升→GDP回升

##### 4. 易错点提醒

- **领先指标"领先"多少不确定**：领先时间从几个月到一两年不等，不是精确预测工具。
- **滞后的失业率**：失业率通常在衰退结束后仍继续上升一段时间（lagging indicator），因为企业需要时间恢复招聘。
- **不是所有先行指标都是领先的**：个别指标可能因特定原因给出错误信号（false signal），所以使用扩散指数和综合指数更可靠。
- **库存投资是GDP的一部分**：存货投资变化对GDP有直接且放大效应。

##### 5. 跨模块关联

- 经济周期的政策应对涉及 **[[M03-Fiscal-Policy]]** 和 **[[M04-Monetary-Policy]]**
- 周期不同阶段对汇率和资本流动的影响见 **[[M07-Capital-Flows-and-FX-Markets]]**
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
