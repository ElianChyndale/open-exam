---
title: "M12 — Introduction to Financial Statement Modeling"
description: "CFA Level I 2026 official module: Introduction to Financial Statement Modeling"
module: M12
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
curriculum_year: 2026
official_module: "Module 12: Introduction to Financial Statement Modeling"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Financial_Statement_Analysis
  - official_2026
---

# M12: Introduction to Financial Statement Modeling

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Introduction to Financial Statement Modeling
- 12.01 | Introduction
- 12.02 | Building a Financial Statement Model
- 12.03 | Behavioral Finance and Analyst Forecasts
- 12.04 | The Impact of Competitive Factors in Prices and Costs
- 12.05 | Modeling Inflation and Deflation
- 12.06 | The Forecast Horizon and Long-Term Forecasting

## Learning Outcome Statements

The candidate should be able to:

- demonstrate the development of a sales-based pro forma company model
- explain how behavioral factors affect analyst forecasts and recommend remedial actions for analyst biases
- explain how the competitive position of a company based on a Porter’s five forces analysis affects prices and costs
- explain how to forecast industry and company sales and costs when they are subject to price inflation or deflation
- explain considerations in the choice of an explicit forecast horizon and an analyst’s choices in developing projections beyond the short-term forecast horizon

## Local Study Notes

### Migrated from `CFA_tier1/Financial_Statement_Analysis/M11-Financial-Statement-Modeling.md`

_Alignment score: 0.37. Original official module field: M12: Introduction to Financial Statement Modeling._

#### M12: 财务报表建模 (Financial Statement Modeling)

### 🌳 核心知识树

```text
🏆 FSA M12: Introduction to Financial Statement Modeling（财务报表建模）
│
├── ⭐ 基于销售的 Pro Forma 模型
│   ├── 以销售预测为输入驱动变量
│   ├── 销售百分比法: 假设部分项目与销售额固定比例
│   ├── 固定项目: 长期债务、固定资产需单独预测
│   └── 📐 预测项 = 预测销售 × (历史项目/历史销售)
│
├── ⭐ 模型结构
│   ├── 利润表预测 → 资产负债表预测 → 现金流量表预测
│   └── 融资缺口分析: 📐 Plug = 预测资产 - 预测负债 - 预测权益
│
├── ⭐ 分析师预测偏差
│   ├── 过度乐观偏差: 高估收益增长
│   ├── 选择性偏差: 只跟踪表现好的公司
│   ├── 羊群效应: 维持接近共识的预测
│   └── 自我归因偏差: 归功于己，归咎于外
│
├── ⭐ 偏差修正方法
│   ├── 多情景分析: 基准/乐观/悲观
│   ├── 预测与历史表现一致性检查
│   ├── 交叉验证: 管理层指引 vs 卖方 vs 第三方
│   └── 使用预测精确度指标跟踪历史记录
│
├── ⭐ 波特五力在预测中的应用
│   ├── 供应商议价能力 → COGS 和利润率
│   ├── 客户议价能力 → 定价能力和毛利率
│   ├── 新进入者威胁 → 长期利润率假设
│   ├── 替代品威胁 → 销量增长假设
│   └── 行业竞争强度 → 投资回报率
│
├── ⭐ 通胀/通缩影响
│   ├── 通胀: 考虑价格传导和工资/原材料上涨
│   ├── 通缩: 定价能力下降，毛利率受压，存货减记
│   └── 区分名义增长率和实际增长率
│
├── ⭐ 预测期与终值
│   ├── 显式预测期: 通常 3-5 年
│   ├── 📐 永续增长终值: TV = FCFF_{n+1} / (WACC - g)
│   ├── 📐 退出倍数法: TV = EBITDA_n × 所选倍数
│   └── ⚠️ 终值通常占估值 > 70%
│
├── 💡 关键洞察
│   ├── 预测假设间必须逻辑一致
│   ├── 永续增长率 g 不应显著超过经济长期增长
│   ├── 终值假设对估值结果极其敏感
│   └── 历史关系可能因环境变化而失效
│
└── ⚠️ 考试陷阱总结
    ├── 终值占估值绝大部分 — 勿放松对终值假设的审视
    ├── 永续增长率必须合理
    ├── 循环引用需启用迭代计算
    └── 历史关系可能会变 — 基于百分比法的假设未必持续
```

### 📐 关键公式表

| 指标 | 公式 | 说明 |
|------|------|------|
| 销售百分比预测 | `Forecast Item = Forecast Sales x (Historical Item / Historical Sales)` | 简单比例法 |
| 永续增长终值 (FCFF) | `TV = FCFF_{n+1} / (WACC - g)` | FCFF 终值 |
| 永续增长终值 (FCFE) | `TV = FCFE_{n+1} / (r - g)` | FCFE 终值 |
| 退出倍数终值 | `TV = EBITDA_n x Selected Multiple` | 基于可比退出倍数 |
| 融资缺口 (Plug) | `Forecast Assets - Forecast Liabilities - Forecast Equity` | 需外部融资或产生盈余 |

### 🛠️ 常见考点与解题思路

**考点1：销售百分比法预测财务报表**
- 先预测销售，再将各项目分为随销售变动和固定项目。

**考点2：预测偏差识别与修正**
- 使用多情景分析和交叉验证方法修正。

**考点3：波特五力在预测中的运用**
- 将行业竞争分析转化为具体预测假设。

**考点4：终值计算与敏感性分析**
- 应用永续增长模型或退出倍数法，在不同假设下敏感性测试。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| 预测假设可独立设定 | 各假设必须逻辑一致 |
| 详细预测了 3-5 年可忽视终值 | 终值通常占估值 > 70% |
| 永续增长率可任意设定 | 不应显著超过经济长期增长率 |
| 历史关系永远有效 | 经济/竞争/业务模式变化会使历史关系失效 |
| 循环引用不可解决 | Excel 中需启用迭代计算 |

### 🔄 跨模块关联

- [[M10-Financial-Analysis-Techniques]]：比率分析和 DuPont 分解是模型假设设定基础
- [[M02-Income-Statement]]：收入预测和利润率假设是 pro forma 模型起点
- [[M03-Balance-Sheet]]：杠杆比率和营运资本效率影响融资需求预测
- [[M04-Cash-Flow-Statements]]：FCFF/FCFE 预测是估值模型核心输入
- [[M09-Financial-Reporting-Quality]]：报告质量影响预测假设可靠性

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.

## 📋 复习与刷题提示

- **核心技能**：销售百分比法构建pro forma模型、情景分析
- **高频考点**：预测假设合理性判断、行为偏差对预测的影响
- **跨科目**：建模→Equity M07 公司预测、Corp M05 资本预算
