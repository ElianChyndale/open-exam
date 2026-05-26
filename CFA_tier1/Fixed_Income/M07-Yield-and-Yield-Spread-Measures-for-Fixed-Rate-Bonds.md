---
title: "M07 — Yield and Yield Spread Measures for Fixed-Rate Bonds"
description: "CFA Level I 2026 official module: Yield and Yield Spread Measures for Fixed-Rate Bonds"
module: M07
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 7: Yield and Yield Spread Measures for Fixed-Rate Bonds"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M07: Yield and Yield Spread Measures for Fixed-Rate Bonds

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Yield and Yield Spread Measures for Fixed-Rate Bonds
- 7.01 | Introduction
- 7.02 | Periodicity and Annualized Yields
- 7.03 | Other Yield Measures, Conventions, and Accounting for Embedded Options
- 7.04 | Yield Spread Measures for Fixed-Rate Bonds and Matrix Pricing

## Learning Outcome Statements

The candidate should be able to:

- calculate annual yield on a bond for varying compounding periods in a year
- compare, calculate, and interpret yield and yield spread measures for fixed-rate bonds

## 🌳 核心知识树

```text
🏆 M07: Fixed-Rate Yield and Spread Measures（固定利率债收益率与利差）
├─ ⭐ 7.1 收益率指标 (Yield Measures)
│  ├─ 📐 YTM (到期收益率)：使债券现值等于价格的贴现率
│  │  └─ ⚠️ 隐含假设：持有至到期且票息按 YTM 再投资
│  ├─ 📐 当期收益率 (Current Yield) = 年票息 / 债券价格
│  │  └─ ⚠️ 仅捕捉票息收入，忽略资本利得和再投资收入
│  ├─ 📐 债券等价收益率 (BEY) = Periodic Yield × periods/year
│  ├─ 📐 有效年化收益率 (EAY) = (1 + periodic rate)^m - 1
│  └─ 🎯 不同复利频率下的收益率需标准化比较
│
├─ ⭐ 7.2 利差指标 (Spread Measures)
│  ├─ 📐 G-spread = YTM_bond - YTM_government_benchmark（需插值匹配期限）
│  ├─ 📐 I-spread = YTM_bond - swap rate at same maturity
│  ├─ 📐 Z-spread = 各即期利率上统一加常数利差使 PV = 价格
│  ├─ 💡 利差包含：信用 + 流动性 + 期权 + 税收 + 技术面因素
│  └─ ⚠️ 利差不是纯信用补偿，需区分各成分
│
└─ ⭐ 7.3 价格-收益率关系
   ├─ 📐 无期权固定利率债券：价格与收益率呈反向关系
   ├─ 💡 利差走阔 → 价格下降；利差收窄 → 价格上升
   └─ ⚠️ Same YTM ≠ same value（现金流结构不同时）
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `P = Σ C/(1+YTM/m)^t + FV/(1+YTM/m)^N` | YTM 定义式 | 债券定价/收益率计算 | 需用金融计算器迭代 |
| `Current Yield = 年票息 / 债券价格` | 当期收益率 | 快速估算票息回报 | 忽略资本利得 |
| `BEY = Periodic Yield × periods/year` | 债券等价收益率 | 标准化比较 | 半年度最常用 |
| `EAY = (1 + periodic rate)^m - 1` | 有效年化收益率 | 跨复利频率比较 | m = 年复利次数 |
| `G-spread = YTM_bond - YTM_benchmark` | G-利差 | 信用风险衡量 | 需插值匹配期限 |
| `Z-spread = constant spread on spot curve` | Z-利差 | 精确利差度量 | Level I 偏概念 |

## 🛠️ 常见考点与解题思路

### 考点 1：YTM 计算
- **题型**：给出债券价格、票息率、期限、面值，反推 YTM
- **工具**：使用金融计算器 TVM 功能
- **注意**：YTM 假设持有至到期且再投资率等于 YTM

### 考点 2：不同复利频率收益率转换
- **题型**：比较不同复利频率的债券收益率
- **思路**：统一转换为 EAY 或 BEY 后再比较
- **步骤**：先算 periodic rate → 再用公式转换为目标收益率

### 考点 3：计算 G-spread
- **步骤**：确定目标债券的期限 → 在国债曲线上插值得到对应期限的基准收益率 → 计算差值
- **注意**：如果目标债券期限不等于任何国债期限，需要线性插值

### 考点 4：解读利差变化
- **利差走阔** → 债券价格下降（相对基准），可能由于信用恶化、流动性下降或风险偏好转变
- **利差收窄** → 债券价格上升（相对基准），可能由于信用改善或市场情绪好转

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| Same YTM = same value | 现金流时间分布不同时风险和再投资也不同 | YTM 是加权平均 |
| Current yield = 总回报 | 忽略 price change 和 reinvestment income | 仅捕捉票息部分 |
| YTM 是承诺回报 | 再投资假设现实中无法严格满足 | 市场利率变化影响实际回报 |
| Spread widening = 违约风险上升 | 也可能是流动性恶化或风险偏好转变 | 利差是多因素综合结果 |

## 🔄 跨模块关联

- **YTM** → [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] 的定价逆运算
- **利差分析** → [[M14-Credit-Risk]] 的信用风险度量
- **年化转换** → [[M08-Yield-and-Yield-Spread-Measures-for-Floating-Rate-Instruments]] 的货币市场指标
- **曲线分析** → [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] 的即期曲线

## 📋 复习与刷题提示

- **核心重点**：YTM/Current Yield/EAY/BEY 的计算和转换是最高频考点
- **利差指标**：
  - G-spread：国债曲线上插值的利差（需匹配期限）
  - I-spread：swap curve 上的利差
  - Z-spread：各即期利率上加常数利差（Level I 偏概念）
- **关键区分**：
  - YTM = 总回报率（含票息+资本利得+再投资），假设持有至到期
  - Current Yield = 仅票息回报率，忽略资本利得和再投资
  - EAY vs BEY：EAY 考虑复利效应（年化），BEY 是单利（periodic × periods）
- **复利频率转换**步骤：
  1. 从报价收益率计算 periodic rate
  2. 转换为 EAY：`EAY = (1 + periodic rate)^m - 1`
  3. 转换为 BEY：`BEY = periodic rate × m`
- **计算流程**：
  - 已知 EAY 求 BEY：`periodic = (1 + EAY)^(1/m) - 1` → `BEY = periodic × m`
  - 已知 BEY 求 EAY：`periodic = BEY/m` → `EAY = (1 + periodic)^m - 1`
- **刷题建议**：
  - 重点做收益率转换计算题（EAY ↔ BEY 转换）
  - 利差分析题（G-spread 的计算和理解）
  - YTM 相关题（金融计算器使用）
- **易混淆点**：
  - Current Yield 不是总回报
  - YTM 的再投资假设在现实中无法严格满足

- **关键数值记忆**：
  - G-spread：以国债曲线为基准（需插值匹配期限）
  - I-spread：以 swap curve 为基准
  - Z-spread：spot curve 上统一加的常数利差
  - OAS：含期权债券调整后的利差（Level I 了解概念即可）
- **考试技巧**：
  - YTM ≠ 已实现回报（再投资率变化会导致偏离）
  - 不同复利频率的收益率必须先统一才能比较
  - EAY 到 BEY 的转换：periodic rate = (1+EAY)^(1/m)-1，BEY = periodic × m
- **计算流程总结**：
  1. 已知 EAY → BEY：periodic = (1+EAY)^(1/2)-1，BEY = periodic × 2
  2. 已知 BEY → EAY：periodic = BEY/2，EAY = (1+periodic)^2-1
  3. 已知 YTM 半年付 → EAY：先算 periodic = YTM/2，再算 EAY = (1+periodic)^2-1
- **利差变化分析**：
  - Spread widening → 债券价格相对基准下降
  - Spread narrowing → 债券价格相对基准上升
  - 利差不是纯信用补偿，含流动性溢价和期权成本
