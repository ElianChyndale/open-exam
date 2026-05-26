---
title: "M08 — Yield and Yield Spread Measures for Floating-Rate Instruments"
description: "CFA Level I 2026 official module: Yield and Yield Spread Measures for Floating-Rate Instruments"
module: M08
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 8: Yield and Yield Spread Measures for Floating-Rate Instruments"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M08: Yield and Yield Spread Measures for Floating-Rate Instruments

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Yield and Yield Spread Measures for Floating-Rate Instruments
- 8.01 | Introduction
- 8.02 | Yield and Yield Spread Measures for Floating-Rate Notes
- 8.03 | Yield Measures for Money Market Instruments

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret yield spread measures for floating-rate instruments
- calculate and interpret yield measures for money market instruments

## 🌳 核心知识树

```text
🏆 M08: Floating-Rate and Money Market Measures（浮动利率与货币市场指标）
├─ ⭐ 8.1 浮动利率工具 (FRN)
│  ├─ 📐 FRN 票息 = Reference Rate + Quoted Margin
│  ├─ 📐 贴现利差 (Discount Margin)：使定价等式成立的利差
│  ├─ 🎯 重置缓释但未消除利率风险
│  ├─ 💡 报价利差 > 市场要求的利差 → Premium
│  ├─ 💡 报价利差 < 市场要求的利差 → Discount
│  └─ ⚠️ 信用恶化可在重置后仍使 FRN 低于面值
│
├─ ⭐ 8.2 货币市场收益率
│  ├─ 📐 BDY (银行贴现收益率) = (FV-P)/FV × 360/t
│  ├─ 📐 MMY (货币市场收益率) = (FV-P)/P × 360/t
│  ├─ 📐 BEY (债券等价收益率) = (FV-P)/P × 365/t
│  ├─ 📐 HPY (持有期收益率) = (FV-P)/P
│  ├─ 🎯 HPY 是不同收益率转换的桥梁
│  └─ ⚠️ 分母陷阱：BDY 用 FV，MMY/BEY 用 P【考试陷阱】
│
└─ ⭐ 8.3 贴现基础 vs 加息基础
   ├─ 📐 贴现基础 (Discount Basis)：T-bill 等，折价发行
   ├─ 📐 加息基础 (Add-on Basis)：FRN 等，支付利息
   └─ 💡 年天数：BDY/MMY 用 360 天，BEY 用 365 天
```

## 📖 知识点详解

### 知识点1：浮动利率工具（Floating-Rate Instruments）
**核心概念**：浮动利率债券（FRN）的票息定期参照市场参考利率重置，使得其利率风险低于同期限的固定利率债券。但 FRN 并非无风险，信用风险仍然存在。
- **FRN 票息**：`Coupon = Reference Rate + Quoted Margin`，其中报价利差（quoted margin）在发行时固定，反映发行人的信用风险
- **重置机制**：定期重置减少但未完全消除利率风险——重置间隔期间价格仍会因市场利率变化而波动
- **贴现利差（Discount Margin）**：当 FRN 交易价格不等于面值时，贴现利差是使定价等式成立的利差，反映了信用风险变化。类似于 YTM 在固定利率债券中的作用
- **交易状态判断**：报价利差 > 市场要求的利差 → Premium（价格 > 面值）；报价利差 < 市场要求的利差 → Discount（价格 < 面值）
- ⚠️ **考试陷阱**：信用恶化可在重置后仍使 FRN 低于面值——即使票息重置，若报价利差低于市场要求的利差，FRN 仍会折价交易

**考试应用**：计算 FRN 的 discount margin（类似于 YTM 的逆运算）；判断 FRN 的交易状态（premium vs discount）。

### 知识点2：货币市场收益率（Money Market Yield Measures）
**核心概念**：货币市场工具使用多种不同的收益率报价方式，每种方式的计算公式不同。考试核心在于区分各种收益率的分母和天数基础。
- **银行贴现收益率（BDY）**：`(FV-P)/FV × 360/t`，分母为面值（FV），使用 360 天
- **货币市场收益率（MMY）**：`(FV-P)/P × 360/t`，分母为购买价格（P），使用 360 天
- **债券等价收益率（BEY）**：`(FV-P)/P × 365/t`，分母为购买价格（P），使用 365 天
- **持有期收益率（HPY）**：`(FV-P)/P`，不年化，是不同收益率转换的桥梁
- **BDY 转 MMY 捷径公式**：`MMY = (365 × BDY) / (360 - t × BDY)`
- ⚠️ **分母陷阱**：BDY 用 FV 做分母，MMY/BEY 用 P 做分母——这是考试最常考的易错点

**考试应用**：收益率类型转换——题目给出 BDY，要求计算 MMY 或 BEY。核心步骤：先通过 BDY 反推 HPY，再用 HPY 计算目标收益率。

### 知识点3：贴现基础 vs 加息基础（Discount Basis vs Add-on Basis）
**核心概念**：货币市场工具根据收益实现方式分为贴现基础和加息基础两类。理解两者的区别对于正确解读收益率报价至关重要。
- **贴现基础（Discount Basis）**：工具以面值折价发行（如 T-bill），收益体现在买入价与面值之差，无票息支付
- **加息基础（Add-on Basis）**：工具直接支付利息（如 FRN），收益来自利息收入
- **年天数差异**：BDY 和 MMY 使用 360 天，BEY 使用 365 天
- 不同市场的报价惯例不同，比较收益率时必须统一转换到同一基准

**考试应用**：区分贴现基础与加息基础工具，理解不同 day-count 惯例对收益率计算的影响。

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `BDY = (FV-P)/FV × 360/t` | 银行贴现收益率 | T-bill 报价 | 分母 FV，360 天 |
| `MMY = (FV-P)/P × 360/t` | 货币市场收益率 | 货币市场比较 | 分母 P，360 天 |
| `BEY = (FV-P)/P × 365/t` | 债券等价收益率 | 与债券收益率比较 | 分母 P，365 天 |
| `HPY = (FV-P)/P` | 持有期收益率 | 收益转换桥梁 | 不年化 |
| `MMY = (365 × BDY) / (360 - t × BDY)` | BDY 转 MMY | 收益率转换 | BDY 转 MMY 的捷径公式 |
| `FRN: Coupon = Ref Rate + Quoted Margin` | FRN 票息 | FRN 定价 | Quoted Margin 固定 |

## 🛠️ 常见考点与解题思路

### 考点 1：收益率类型转换
- **题型**：给出 BDY，要求计算 MMY 或 BEY
- **步骤**：
  1. 先算 HPY = BDY × t/360（从 BDY 公式反推）
  2. 再用 HPY 算目标收益率：MMY = HPY × 360/t；BEY = HPY × 365/t
- **捷径**：MMY = (365 × BDY) / (360 - t × BDY)；BDY 和 BEY 在 t<365 时数值相近

### 考点 2：FRN 的 Discount Margin 计算
- **题型**：FRN 价格偏离面值时，求解贴现利差
- **思路**：类似于 YTM 的逆运算，使 FRN 定价等式成立的利差
- **判断**：Quoted Margin > Discount Margin → Premium；反之 → Discount

### 考点 3：判断 FRN 交易状态
- **思路**：报价利差 vs 市场要求的利差（贴现利差）
- **Premium**：报价利差 > 贴现利差（FRN 价格 > 面值）
- **Discount**：报价利差 < 贴现利差（FRN 价格 < 面值）

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| BDY 和 MMY 都用 P 做分母 | BDY 用 FV，MMY 用 P | 分母不同导致数值不同 |
| 所有收益率都用 365 天 | BDY/MMY 用 360，BEY 用 365 | 市场惯例不同 |
| FRN 重置频率高 = 无利率风险 | 重置间隔间价格仍会波动 | 参考利率变化 + 信用利差变化 |
| Quoted Margin = Discount Margin | Quoted Margin 固定，Discount Margin 随信用变化 | 两者是不同的概念 |

## 🔄 跨模块关联

- **FRN 定价** → [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] 的 DCF 框架
- **货币市场收益率** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的 yield conversion
- **贴现利差** → [[M14-Credit-Risk]] 的信用风险定价
- **FRN 现金流** → [[M02-Fixed-Income-Cash-Flows-and-Types]] 浮动利率现金流结构

## 📋 复习与刷题提示

- **核心重点**：BDY/MMY/BEY 的计算和转换是最高频计算考点
- **FRN 关键**：理解 Quoted Margin（合约固定）与 Discount Margin（市场要求，随信用变化）的区别
  - Quoted Margin > Discount Margin → Premium（FRN 价格 > 面值）
  - Quoted Margin < Discount Margin → Discount（FRN 价格 < 面值）
- **转换技巧**：HPY = (FV-P)/P 是不同收益率之间的转换桥梁
  - BDY → HPY：HPY = BDY × t/360
  - HPY → MMY：MMY = HPY × 360/t
  - HPY → BEY：BEY = HPY × 365/t
  - 捷径：MMY = (365 × BDY) / (360 - t × BDY)
- **分母陷阱**：
  - BDY 分母 = FV（面值），360 天
  - MMY 分母 = P（价格），360 天
  - BEY 分母 = P（价格），365 天
  - 三者对同一工具可能给出不同数值（考试常考数值比较）
- **典型计算流程**：
  1. 题目给出 BDY = 4.5%，t = 180 天
  2. HPY = BDY × t/360 = 4.5% × 180/360 = 2.25%
  3. BEY = HPY × 365/t = 2.25% × 365/180 = 4.5625%
- **刷题建议**：
  - 重点做 BDY/MMY/BEY 转换计算题
  - FRN discount margin 分析题（判断交易状态）
  - HPY 中间桥梁的应用题
- **易混淆点**：
  - BDY 不是债券的"收益率"，它是银行贴现报价
  - FRN 重置不消除利率风险
  - Discount Margin 随信用变化，不是固定的

- **关键数值记忆**：
  - BDY：分母 = FV，360 天
  - MMY：分母 = P，360 天
  - BEY（货币市场）：分母 = P，365 天
  - BDY < MMY < BEY（对同一工具，t < 365 时恒成立）
- **考试技巧**：
  - HPY 是不同收益率之间的转换桥梁
  - BDY → HPY：HPY = BDY × t/360
  - HPY → BEY：BEY = HPY × 365/t
  - 捷径公式：MMY = (365 × BDY) / (360 - t × BDY)
- **典型计算示例**：
  - T-bill t=180天，BDY=4.5%
  - HPY = 4.5% × 180/360 = 2.25%
  - BEY = 2.25% × 365/180 = 4.5625%
  - MMY = 2.25% × 360/180 = 4.50%
  - BDY(4.5%) < MMY(4.5%)... 实际 BDY(4.5%) < BEY(4.5625%)
- **FRN 关键概念**：
  - Quoted Margin（固定）≠ Discount Margin（市场要求，随信用变化）
  - QM > DM → Premium（FRN 价格 > 面值）
  - QM < DM → Discount（FRN 价格 < 面值）
  - DM 是类似 YTM 的逆运算概念
