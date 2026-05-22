---
title: "M03 — Working Capital and Liquidity"
description: 营运资本与流动性 — 经营周期、现金转换周期、融资政策
module: M03
subject: Corporate_Issuers
---

# M03: Working Capital and Liquidity（营运资本与流动性）

## 1. 核心知识点

### 1.1 经营周期 (Operating Cycle) 与现金转换周期 (Cash Conversion Cycle)

**营运资本管理 (Working Capital Management)** 的核心是管理短期资产与短期负债之间的匹配，确保公司有足够流动性维持日常运营。

- **经营周期 (Operating Cycle)** = 存货周转天数 (Days of Inventory Outstanding, DIO) + 应收账款周转天数 (Days of Sales Outstanding, DSO)
  - 代表从采购存货到收回现金的完整周期
- **现金转换周期 (Cash Conversion Cycle, CCC)** = DIO + DSO - 应付账款周转天数 (Days of Payables Outstanding, DPO)
  - 代表公司实际需要融资的天数。CCC 越短，说明公司对营运资本的需求越低。

**影响各周转天数的因素**：

- **DIO**：取决于行业特性（零售商周转快，制造商周转慢）和库存管理效率（如 JIT 模式）
- **DSO**：取决于信用政策和收款效率。宽松的信用政策可能增加销售，但也延长了现金回收期
- **DPO**：取决于与供应商的谈判地位。延迟付款可以保留现金，但可能损害供应商关系

**流动性缓冲 (Liquidity Buffers)**：持有现金或易于变现的资产可以保护运营不受现金流波动的影响，但同时也占用了资本，存在机会成本。

### 1.2 融资政策 (Financing Policy)

公司如何为营运资本融资可分为两种策略：

- **激进政策 (Aggressive Policy)**：使用更多短期债务融资，流动性缓冲较小。优势是融资成本较低（短期利率通常低于长期），劣势是**展期风险 (rollover risk)** 较高 — 如果市场环境恶化，公司可能无法续借。
- **保守政策 (Conservative Policy)**：使用更多长期资金和权益融资，持有较多流动性缓冲。更稳健但更资本密集，降低资产回报率 (ROA)。

**选择因素**：现金流可预测性越强，越适合采用激进政策；反之则宜保守。

### 1.3 流动性比率 (Liquidity Ratios)

- **流动比率 (Current Ratio)** = `Current Assets / Current Liabilities`，衡量短期偿债能力的粗略指标
- **速动比率 (Quick Ratio)** = `(Cash + Marketable Securities + Receivables) / Current Liabilities`，剔除了存货，更严格地衡量流动性
- **现金比率 (Cash Ratio)** = `(Cash + Marketable Securities) / Current Liabilities`，最保守的流动性指标

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| 存货周转天数 (DIO) | `(Average Inventory / COGS) x 365` | 存货售出平均天数 |
| 应收账款周转天数 (DSO) | `(Average Receivables / Revenue) x 365` | 收款平均天数 |
| 应付账款周转天数 (DPO) | `(Average Payables / Purchases or COGS) x 365` | 付款平均天数，注意分母是 purchases |
| 经营周期 | `DIO + DSO` | 从付出现金到收回现金的时间 |
| 现金转换周期 | `DIO + DSO - DPO` | 实际需要融资的天数 |

使用场景：CCC 分析帮助判断公司营运资本管理的效率。CCC 下降可能是好事（管理改善），也可能是坏事（过度挤压供应商或收紧信用导致销售下降）。

## 3. 常见考点与解题思路

**考点 1：计算现金转换周期**
- 给定 DIO、DSO、DPO 或相关周转率数据，求 CCC。
- 解题步骤：先分别计算 DIO、DSO、DPO，再代入 CCC = DIO + DSO - DPO。

**考点 2：激进 vs 保守融资政策判断**
- 题目描述公司的融资行为（如"公司用短期借款支持长期营运资本需求"），问其政策类型。
- 判断依据：短期融资占比高 → 激进；长期融资占比高 + 高流动性缓冲 → 保守。

**考点 3：流动性比率的解读陷阱**
- 题目问：流动比率高是否意味着流动性好？
- 不一定：如果大量流动资产是滞销存货，则流动比率虽高但无法快速变现。

## 4. 易错点提醒

- **DPO 的分母是 purchases 而不是 COGS**：如果题目只给了 COGS，可能需要假设 purchases = COGS 或通过存货变动调整。
- **缩短 CCC 并非总是好事**：过度压缩 DSO 可能流失客户，过度延长 DPO 可能激怒供应商。**服务质量、销售增长和信用质量必须同步考量。**
- **流动比率高 ≠ 效率高**：流动比率的分子中积压的存货和应收款可能是低效信号。
- **现金比率过于保守**：考试中不常作为首选指标，但需要知道其含义。

## 5. 跨模块关联

- 营运资本效率 → [[M04-Capital-Investments]] 项目现金流中需包含营运资本变动
- 融资政策 → [[M05-Cost-of-Capital]] 短期 vs 长期融资成本对应资本结构决策
- 流动性与杠杆 → [[M06-Capital-Structure-and-Leverage]] 激进融资政策增加财务杠杆风险
- 现金转换周期 → [[M07-Business-Models]] 不同商业模式的 CCC 特征不同（如零售业 CCC 通常为负）
