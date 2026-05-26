---
title: "M04 — Working Capital and Liquidity"
description: "CFA Level I 2026 official module: Working Capital and Liquidity"
module: M04
subject: "Corporate Issuers"
topic_area: Corporate_Issuers
curriculum_year: 2026
official_module: "Module 4: Working Capital and Liquidity"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Corporate_Issuers
  - official_2026
---

# M04: Working Capital and Liquidity

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Working Capital and Liquidity
- 4.01 | Introduction
- 4.02 | Cash Conversion Cycle
- 4.03 | Liquidity
- 4.04 | Managing Working Capital and Liquidity

## Learning Outcome Statements

The candidate should be able to:

- explain the cash conversion cycle and compare issuers' cash conversion cycles
- explain liquidity and compare issuers' liquidity levels
- describe issuers' objectives and compare methods for managing working capital and liquidity

## 🌳 核心知识树

```text
🏆 【营运资本与流动性】
│
├── 🔷 经营周期与现金转换周期（CCC）📐🎯
│   ├── 经营周期（Operating Cycle）= DOH + DSO
│   │   └── 从采购存货到收回现金的完整周期
│   ├── 现金转换周期（CCC）= DOH + DSO - DPO 🎯
│   │   └── 公司实际需要融资的天数
│   ├── DIO（存货周转天数）= (Avg Inv / COGS) × 365
│   │   └── 影响因素：行业特性、库存管理效率（JIT）
│   ├── DSO（应收账款天数）= (Avg AR / Revenue) × 365
│   │   └── 影响因素：信用政策、收款效率
│   └── DPO（应付账款天数）= (Avg AP / Purchases) × 365 ⚠️
│       └── 影响因素：供应商谈判地位
│
├── 🔷 融资政策 🎯
│   ├── 激进政策（Aggressive Policy）
│   │   ├── 更多短期债务，流动性缓冲小
│   │   ├── 优势：融资成本低（短期利率通常低于长期）
│   │   └── ⚠️ 劣势：展期风险（rollover risk）高
│   └── 保守政策（Conservative Policy）
│       ├── 更多长期资金 + 权益，高流动性缓冲
│       ├── 优势：更稳健，不易受市场波动影响
│       └── ⚠️ 劣势：降低 ROA，资本成本高
│
├── 🔷 流动性比率 📐🎯
│   ├── Current Ratio = CA / CL
│   │   └── ⚠️ 高不等于好（存货积压可能导致虚高）
│   ├── Quick Ratio = (Cash + ST Inv + AR) / CL
│   │   └── 排除存货，更严格的流动性衡量
│   └── Cash Ratio = (Cash + ST Inv) / CL
│       └── 最保守的流动性指标
│
├── 🔷 流动性缓冲
│   ├── 持有现金或易于变现的资产
│   ├── 保护运营不受现金流波动影响
│   └── ⚠️ 存在机会成本（占用资本）
│
│   💡 核心洞察：CCC 越短越好，负的 CCC 是优质信号
│   🎯 高频考点：CCC 计算、激进 vs 保守政策、流动性比率含义
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `DIO = (Avg Inventory / COGS) × 365` | 存货周转天数 | 衡量存货出售速度 | 越低越好，但过低可能缺货 |
| `DSO = (Avg Receivables / Revenue) × 365` | 应收账款天数 | 衡量收款速度 | 越高说明收款越慢 |
| `DPO = (Avg Payables / Purchases) × 365` | 应付账款天数 | 衡量付款速度 | 分母是 Purchases，非 COGS ⚠️ |
| `Operating Cycle = DIO + DSO` | 经营周期 | 从采购到收款的完整周期 | 越长说明营运资本需求越大 |
| `CCC = DIO + DSO - DPO` | 现金转换周期 | 实际需融资天数 | 越短越好；负值更优 |
| `Current Ratio = CA / CL` | 流动比率 | 短期偿债能力 | 包含存货，可能虚高 |
| `Quick Ratio = (Cash + ST Inv + AR) / CL` | 速动比率 | 严格流动性 | 排除存货 |
| `Cash Ratio = (Cash + ST Inv) / CL` | 现金比率 | 最保守流动性 | 很少单独使用 |
| `Net Working Capital = CA - CL` | 净营运资本 | 流动性缓冲 | 正值为传统模式 |

## 🛠️ 常见考点与解题思路

### 主题1：现金转换周期计算（🎯 必考）
- **题型**：给定财务数据，计算 CCC
- **解题步骤**：
  1. 计算 DIO = (Avg Inv / COGS) × 365
  2. 计算 DSO = (Avg AR / Revenue) × 365
  3. 计算 DPO = (Avg AP / Purchases) × 365（如果只给 COGS，假设 Purchases = COGS 或调整存货变动）
  4. CCC = DIO + DSO - DPO
  5. 解读：CCC 越短，对营运资本需求越低；负 CCC 意味着公司先收钱后付款

### 主题2：激进 vs 保守政策判断（🎯 高频）
- **题型**：描述公司融资行为，问政策类型
- **判断依据**：
  - 短期债务占比高 + 低流动性缓冲 → **激进政策**
  - 长期融资占比高 + 高流动性缓冲 → **保守政策**
- **选择因素**：现金流可预测性越强，越适合激进政策；反之保守

### 主题3：流动性比率解读陷阱
- **题型**：问流动比率高是否意味着流动性好
- **答案**：不一定。如果流动资产主要是滞销存货，流动比率虽高但无法快速变现
- **延展**：需结合存货质量、应收账款账龄和行业特征综合判断

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| DPO 的分母是 COGS | DPO 的分母是 **Purchases**，非 COGS | 只有 Purchases 才产生应付账款 |
| 缩短 CCC 总是好事 | 过度压缩 DSO 可能流失客户，过度延长 DPO 可能激怒供应商 | 利益平衡比数字本身更重要 |
| 流动比率高 = 流动性好 | 流动比率高可能因存货积压或应收款账期过长 | 需结合质量和行业特征分析 |
| 激进政策总是危险的 | 现金流可预测性强的公司适合激进政策 | 关键在匹配度 |
| CCC 为正才正常 | 优质商业模式 CCC 可以为负（如零售业先收钱后付款） | 负 CCC 是竞争优势 |
| 现金比率是最好的流动性指标 | 现金比率过于保守，忽略了应收款的变现能力 | 实际中很少单独使用 |
| 流动性缓冲越大越好 | 过多现金占用资本，降低 ROA | 需权衡安全与效率 |

## 🔄 跨模块关联

- **[[M05-Capital-Investments-and-Capital-Allocation]]** — 项目现金流分析中需包含营运资本变动（初始投入和回收）；营运资本效率影响项目 NPV
- **[[M06-Capital-Structure]]** — 融资政策（激进 vs 保守）与资本结构决策相关；短期 vs 长期融资选择影响资本成本
- **[[M07-Business-Models]]** — 不同商业模式的 CCC 特征不同（零售业 CCC 通常为负，制造业为正）；商业模式分析需考虑营运资本需求
- **[[M01-Organizational-Forms-Corporate-Issuer-Features-and-Ownership]]** — 不同企业形式的融资能力不同，影响营运资本融资政策选择
- **[[M03-Corporate-Governance-Conflicts-Mechanisms-Risks-and-Benefits]]** — 管理层可能因激励扭曲选择不适当的营运资本管理策略

## 📋 复习与刷题提示

- **计算题优先**：CCC = DIO + DSO - DPO 是必考公式。分别计算三个周转天数是关键
- **概念辨析**：区分 Operating Cycle（经营周期）和 CCC（现金转换周期），Operating Cycle 不包含 DPO
- **政策对比**：激进 vs 保守融资政策的优劣及其适用范围
- **比率解读**：流动比率、速动比率、现金比率的递进关系 — 越来越保守
- **DPO 陷阱**：牢记 DPO 的分母是 Purchases 而非 COGS。如果题目只给 COGS，需要根据存货变动推算 Purchases
- **综合分析**：理解 CCC 变化的多重含义 — 缩短 CCC 可能是好事（管理改善），也可能是坏事（过度挤压供应商）
- **行业背景**：同一 CCC 值在不同行业有完全不同的含义，永远在行业背景下解读

## 📋 复习与刷题提示

- **核心公式**：CCC = DOH + DSO - DPO（必须能默写）
- **高频考点**：CCC计算、流动性来源判断（CFO vs 外部融资）
- **跨科目链接**：CCC概念→FSA M11 比率分析；流动性→FI M04 回购市场
