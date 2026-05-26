---
title: "M18 — Asset-Backed Security (ABS) Instrument and Market Features"
description: "CFA Level I 2026 official module: Asset-Backed Security (ABS) Instrument and Market Features"
module: M18
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 18: Asset-Backed Security (ABS) Instrument and Market Features"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M18: Asset-Backed Security (ABS) Instrument and Market Features

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Asset-Backed Security (ABS) Instrument and Market Features
- 18.01 | Introduction
- 18.02 | Covered Bonds
- 18.03 | ABS Structures to Address Credit Risk
- 18.04 | Non-Mortgage Asset-Backed Securities
- 18.05 | Collateralized Debt Obligations

## Learning Outcome Statements

The candidate should be able to:

- describe characteristics and risks of covered bonds and how they differ from other asset-backed securities
- describe typical credit enhancement structures used in securitizations
- describe types and characteristics of non-mortgage asset-backed securities, including the cash flows and risks of each type
- describe collateralized debt obligations, including their cash flows and risks

## 🌳 核心知识树

```text
🏆 M18: ABS and Credit Enhancement（ABS 与信用增级）
├─ ⭐ 18.1 ABS 类型
│  ├─ 📐 汽车贷款 ABS：有明确摊销计划
│  ├─ 📐 信用卡 ABS：循环结构，本金可重新投资
│  ├─ 📐 应收账款 ABS：依赖商业付款周期
│  ├─ 📐 CDO (债务抵押债券)：以债券/贷款为担保品
│  └─ 💡 摊还型 vs 循环型：还款模式不同
│
├─ ⭐ 18.2 Covered Bond（有担保债券）
│  ├─ 📐 双重追索权 (Dual Recourse)：担保池 + 发行人信用
│  ├─ 🎯 资产不出表（留在发行人资产负债表上）
│  ├─ 💡 Covered bond ≠ ABS（法律结构不同）
│  └─ ⚠️ Covered bond 不是 ABS【易错】
│
├─ ⭐ 18.3 内部信用增级
│  ├─ 📐 分层 (Subordination)：优先级先受偿
│  ├─ 📐 超额抵押 (Overcollateralization)：资产 > 证券
│  ├─ 📐 超额利差 (Excess Spread)：收益 > 支付 + 费用
│  ├─ 📐 准备金账户 (Reserve Account)：现金缓冲
│  └─ ⚠️ 增级重新分配损失吸收，非免费收益
│
└─ ⭐ 18.4 外部信用增级
   ├─ 💡 债券保险 (Bond Insurance)
   ├─ 💡 信用证 (Letter of Credit)
   ├─ 💡 公司担保 (Corporate Guarantee)
   └─ 💡 依赖第三方信用质量
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Overcollateralization = (资产池面值 - 证券面值) / 证券面值` | 超额抵押率 | 信用增级评估 | 比率越高保护越强 |
| `Excess Spread = 资产池利率 - 证券利率 - 费用` | 超额利差 | 损失吸收缓冲 | 可迅速耗尽 |
| `Credit Enhancement Level = 次级层 + 准备金 + 超额利差现值` | 信用增级水平 | 全面评估 | 加权计算 |
| `Covered Bond: 资产池 + 发行人信用` | 双重追索权 | 风险分析 | 与 ABS 的单一追索不同 |

## 🛠️ 常见考点与解题思路

### 考点 1：区分内部 vs 外部信用增级
- **内部**：分层、超额抵押、超额利差、准备金账户（不依赖第三方）
- **外部**：保险、信用证、第三方担保（依赖第三方信用质量）
- **考试常考**：给定增级方式判断类型

### 考点 2：理解 Covered Bond 的双重追索权
- **第一重追索**：对担保资产池
- **第二重追索**：对发行人的其他资产
- **与 ABS 区别**：ABS 投资者仅对 SPV 资产池有追索权
- **关键**：Covered bond 资产不出表，仍在发行人资产负债表上

### 考点 3：ABS 摊销类型判断
- **摊还型 (Amortizing)**：汽车贷款 → 有固定还款计划
- **循环型 (Revolving)**：信用卡 → 额度可循环使用
- **判断依据**：基础资产的现金流模式

### 考点 4：分析超额利差的缓冲作用
- **机制**：资产池利率 - 证券利率 - 费用 = 超额利差
- **缓冲**：当部分贷款违约时，超额利差先吸收损失
- **风险**：大规模违约会迅速耗尽

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| Credit enhancement = free yield | 重新分配损失吸收，优先级收益降低有代价 | 次级层承受更大风险 |
| Covered bond = ABS | 法律结构不同，covered bond 资产不出表 | 双重追索 vs 单一追索 |
| 超额利差永久有效 | 大规模违约后可能迅速耗尽 | 缓冲有限 |
| 所有 ABS 结构相同 | 有摊还型、循环型、触发机制等差异 | 需逐一分析 |

## 🔄 跨模块关联

- **信用增级** → [[M17-Fixed-Income-Securitization]] 的 SPV 结构
- **分层设计** → [[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]] 的 CMO 分层
- **Covered bond** → [[M15-Credit-Analysis-for-Government-Issuers]] 和 [[M16-Credit-Analysis-for-Corporate-Issuers]] 的发行人信用分析
- **信用风险** → [[M14-Credit-Risk]] 的 PD/LGD 框架

## 📋 复习与刷题提示

- **核心重点**：内部 vs 外部信用增级的区分
  - 内部：分层、超额抵押、超额利差、准备金账户
  - 外部：保险、信用证、第三方担保
  - 考试常考：给定增级方式 → 判断内/外部类型
- **Covered bond 要点**：
  - 双重追索权：担保池 + 发行人信用
  - 资产不出表：仍在发行人资产负债表
  - 与 ABS 本质区别：法律结构不同（covered bond 不是 ABS）
  - Covered bond 投资者在发行人违约时有双重追索
- **ABS 类型与现金流特征**：
  - 汽车贷款 ABS：摊销型，有固定还款计划，提前还款风险低
  - 信用卡 ABS：循环型，本金可重新投资，提前还款风险中等
  - 应收账款 ABS：循环或摊销，依赖商业付款周期
  - CDO：以债券/贷款为担保品，多层结构化
- **关键数据**：
  - 超额抵押率 = (资产池面值 - 证券面值) / 证券面值
  - 超额利差 = 资产池利率 - 证券利率 - 费用
  - 信用增级水平 = 次级层 + 准备金 + 超额利差现值
- **刷题建议**：
  - 重点做信用增级识别题（内部 vs 外部）
  - Covered bond 分析题（双重追索权和 ABS 对比）
  - ABS 类型特征题（汽车贷款/信用卡/应收账款区别）
  - Trigger events 相关题（超额利差触发机制）
- **易混淆点**：
  - Credit enhancement ≠ free yield
  - Covered bond ≠ ABS
  - 超额利差不是永久性保护
  - 不同 ABS 的结构差异大

- **考试技巧**：
  - 信用增级 ≠ 免费收益（次级层承受更多风险）
  - Covered bond 不是 ABS，核心区别为资产是否出表
  - 超额利差缓冲有限，大规模违约时迅速耗尽
  - 摊还型 vs 循环型：看基础资产现金流的还款模式
  - CDO 的担保资产池是债券/贷款而非消费贷款
- **补充概念**：
  - 触发机制（Triggers）：超额利差下降到阈值以下 → 现金流瀑布转向
  - 提前摊还（Early Amortization）：触发后加速偿还投资者本金
  - CDO 的经理人主动管理 vs ABS 的被动池管理
  - 金融危机后 CDO 市场大幅萎缩，合规 CLO 仍活跃
