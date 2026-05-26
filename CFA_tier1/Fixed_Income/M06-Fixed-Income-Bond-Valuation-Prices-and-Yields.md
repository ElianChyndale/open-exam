---
title: "M06 — Fixed-Income Bond Valuation: Prices and Yields"
description: "CFA Level I 2026 official module: Fixed-Income Bond Valuation: Prices and Yields"
module: M06
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 6: Fixed-Income Bond Valuation: Prices and Yields"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M06: Fixed-Income Bond Valuation: Prices and Yields

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Fixed-Income Bond Valuation: Prices and Yields
- 6.01 | Introduction
- 6.02 | Bond Pricing and the Time Value of Money
- 6.03 | Relationships between Bond Prices and Bond Features
- 6.04 | Matrix Pricing

## Learning Outcome Statements

The candidate should be able to:

- calculate a bond's price given a yield-to-maturity on or between coupon dates
- identify the relationships among a bond's price, coupon rate, maturity, and yield-to-maturity
- describe matrix pricing

## 🌳 核心知识树

```text
🏆 M06: Bond Valuation: Prices and Yields（债券估值：价格与收益率）
├─ ⭐ 6.1 定价引擎 (Pricing Engine)
│  ├─ 📐 债券价值 = Σ 票息现值 + 本金现值
│  │  └─ P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N
│  ├─ 🎯 折价/溢价/平价：票息率 vs YTM 比较
│  │  ├─ Coupon > YTM  → Premium
│  │  ├─ Coupon = YTM  → Par
│  │  └─ Coupon < YTM  → Discount
│  ├─ 💡 期限越长、票息越低 → 价格对收益率变动越敏感
│  └─ ⚠️ 零息债券对利率变动最敏感（久期最大）
│
├─ ⭐ 6.2 交易价格惯例 (Trading Price Conventions)
│  ├─ 📐 全价 (Full Price) = 净价 (Clean Price) + 应计利息 (AI)
│  ├─ 📐 AI = 每期票息 × 上次付息至今天数 / 付息周期天数
│  ├─ 🎯 报价用净价，实际交易结算用全价【考试核心】
│  └─ ⚠️ Day-count convention 因市场而异（国债 actual/actual，公司债 30/360）
│
└─ ⭐ 6.3 矩阵定价 (Matrix Pricing)
   ├─ 📐 利用可比债券收益率估算非流动性债券价格
   ├─ 💡 适用于不活跃交易的债券
   └─ 💡 依赖相似信用评级和相近期限
```

## 📖 知识点详解

### 知识点1：定价引擎（Pricing Engine）
**核心概念**：债券定价的核心逻辑是未来现金流的现值之和。债券价值等于所有未来票息和本金按照到期收益率（YTM）贴现的现值。这是固定收益分析最基础也最重要的概念。
- **核心公式**：`P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N`，其中 C 为每期票息，y 为 YTM，m 为年复利次数，N 为总期数
- **溢价/折价/平价判断**：Coupon > YTM → Premium；Coupon = YTM → Par；Coupon < YTM → Discount
- **利率敏感度规律**：期限越长、票息越低 → 价格对收益率变动越敏感
- **零息债券**：对利率变动最敏感，因为久期等于其期限，且无期间现金流缓释影响
- ⚠️ 折价/溢价/平价关系是理解后续全部债券分析的基础

**考试应用**：给定债券参数计算价格，或给定价格反推 YTM（使用金融计算器）。判断 premium/discount/par 只需比较 coupon rate 与 YTM 的大小，无需精确计算。

### 知识点2：交易价格惯例（Trading Price Conventions）
**核心概念**：债券交易中存在全价和净价两种报价方式，理解两者的区别对正确计算实际交易结算金额至关重要。
- **全价（Full Price / Dirty Price）**：买方实际支付的金额，= 净价 + 应计利息
- **净价（Clean Price / Quoted Price）**：报价时通常使用的价格，不含应计利息
- **应计利息（Accrued Interest, AI）**：`AI = 每期票息 × 上次付息至今天数 / 付息周期天数`
- ⚠️ **考试核心**：报价用净价，但实际交易结算用全价
- ⚠️ Day-count convention 因市场而异：国债 actual/actual，公司债 30/360，计算 AI 时必须先确认

**考试应用**：计算应计利息和全价。注意 fractional period 处理——两个票息日之间交易时，需将贴现期调整为分数期。

### 知识点3：矩阵定价（Matrix Pricing）
**核心概念**：矩阵定价用于估算非流动性或新发行债券的合理价格或收益率。当债券不活跃交易时，利用信用评级和期限相近的可比债券价格来估算。
- **适用场景**：不活跃交易的债券、新发行但无活跃二级市场的债券
- **方法**：找信用评级和期限相近的可比债券 → 计算其 YTM → 用该 YTM 贴现目标债券的现金流
- **依赖假设**：相似信用评级和相近期限的债券应具有相似的收益率
- 矩阵定价的准确性取决于可比债券选择的合理性

**考试应用**：利用可比债券的 YTM 估算目标债券的价格，理解其适用场景和局限性。

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `P = Σ_{t=1}^{N} C/(1+y/m)^t + FV/(1+y/m)^N` | 债券定价 | 计算价格 | 注意复利频率 m |
| `Full Price = Clean Price + Accrued Interest` | 全价 | 实际结算 | 报价 ≠ 支付金额 |
| `AI = Coupon × (Days_since_last / Days_in_period)` | 应计利息 | 票息日间交易 | 先确认 day-count 规则 |
| `Coupon > YTM → Premium` | 溢价判断 | 判断交易状态 | 无需精确计算 |

## 🛠️ 常见考点与解题思路

### 考点 1：计算应计利息 (AI)
- **步骤**：计算上次付息日至结算日的天数占比 → 乘以每期票息金额
- **关键**：先确认 day-count convention（actual/actual vs 30/360）
- **公式**：`AI = (C/m) × (Days_since_last_payment / Days_in_coupon_period)`

### 考点 2：计算 Full Price
- **方法一**：先按票息日定价公式计算现值 → 再复利至结算日
- **方法二**：先计算 Clean Price → 计算 AI → Full Price = Clean Price + AI
- **注意**：Fractional period 处理易错，可先将现金流贴现至上一个票息日，再复利至结算日

### 考点 3：判断 Premium/Discount/Par
- **思路**：直接比较 Coupon Rate 与 YTM
- **技巧**：不需要精确计算，大小比较即可

### 考点 4：矩阵定价计算
- **题型**：利用可比债券的 YTM 估算目标债券的价格
- **步骤**：找信用评级和期限相近的可比债券 → 计算其 YTM → 用该 YTM 贴现目标债券的现金流

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| Clean price 是买方最终支付 | 实际结算支付 Full Price | Clean Price 只是报价习惯 |
| 所有债券用相同 day-count | 国债 actual/actual，公司债 30/360 | 计算 AI 时必须确认 |
| 票息日间定价与票息日相同 | 需要分数期处理 | 时间价值需精确计算 |
| 所有市场报价惯例相同 | 美国国债、欧洲债券、公司债报价不同 | 需注意市场差异 |

## 🔄 跨模块关联

- **定价方法** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的 YTM 计算（定价的逆运算）
- **应计利息** → 与 day-count convention 紧密结合
- **矩阵定价** → [[M03-Fixed-Income-Issuance-and-Trading]] 的流动性概念
- **不同债券结构** → [[M02-Fixed-Income-Cash-Flows-and-Types]] 的现金流类型影响定价方法

## 📋 复习与刷题提示

- **核心重点**：Full Price / Clean Price / AI 的计算是最高频考点
- **计算题**：
  - 债券定价公式必须熟练使用金融计算器（TVM 功能）
  - 应计利息计算：注意 day-count convention（国债 actual/actual，公司债 30/360）
  - 分数期处理：贴现至上一个票息日 → 再复利至结算日
- **概念理解**：YTM 与票息率的关系决定溢价/折价（Coupon > YTM → Premium，反之 Discount）
- **Day-count conventions**：
  - 美国国债：Actual/Actual
  - 公司债/市政债：30/360
  - 货币市场工具：Actual/360
- **Matrix pricing**：理解应用场景（非流动性债券的定价估算）和方法（利用可比债券）
- **关键区分**：
  - Clean Price = 报价价格（不含应计利息）
  - Full Price = 实际结算价格（含应计利息）
  - 投资者支付 Full Price，卖方收到 Full Price
- **刷题建议**：
  - 重点做应计利息计算题（含不同 day-count 转换）
  - Full price 计算题（票息日和非票息日两种场景）
  - 溢价/折价/平价判断题
- **常见错误**：
  - 混淆 Clean Price 与 Full Price
  - 忽略 Day-count convention
  - 分数期处理时复利方向错误

- **关键数值记忆**：
  - Day-count conventions：国债 actual/actual，公司债 30/360，货币市场 actual/360
  - 应计利息计算必须精确到天数
  - Matrix pricing 适用于非活跃交易债券的估值
- **考试技巧**：
  - 全价 = 净价 + 应计利息（这一步占分很高）
  - 折价/溢价判断只需比较 Coupon vs YTM，不需要计算
  - 分数期定价时优先使用贴现至上一票息日再复利的方法
- **计算流程总结**：
  1. 确定结算日和 day-count convention
  2. 计算上次付息日到结算日的应计利息天数
  3. 计算 AI = 每期票息 × (天数占比)
  4. 若在票息日：直接使用标准定价公式
  5. 若在票息日之间：先贴现至上一票息日，再复利至结算日
  6. Full Price = Clean Price + AI（若已知其一）

- **矩阵定价公式**：YTM_target ≈ 线性插值（可比债券 A 和 B 的 YTM 按期限加权平均）
