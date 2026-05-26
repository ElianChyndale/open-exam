---
title: "M06 — Hedge Funds"
description: "CFA Level I 2026 official module: Hedge Funds"
module: M06
subject: "Alternative Investments"
topic_area: Alternative_Investments
curriculum_year: 2026
official_module: "Module 6: Hedge Funds"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Alternative_Investments
  - official_2026
---

# M06: Hedge Funds

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Hedge Funds
- 6.01 | Introduction
- 6.02 | Hedge Fund Investment Features
- 6.03 | Hedge Fund Investment Forms
- 6.04 | Hedge Fund Investment Risk, Return, and Diversification

## Learning Outcome Statements

The candidate should be able to:

- explain investment features of hedge funds and contrast them with other asset classes
- describe investment forms and vehicles used in hedge fund investments
- analyze sources of risk, return, and diversification among hedge fund investments

## Local Study Notes

### Migrated from `CFA_tier1/Alternative_Investments/M06-Hedge-Funds.md`

_Alignment score: 0.39. Original official module field: Hedge Funds._

#### M06: 对冲基金 (Hedge Funds)

##### 1. 核心知识点

###### 6.1 对冲基金特征 (Hedge Fund Characteristics)

| 特征 | 说明 |
|------|------|
| 流动性 | 相对PE/VC较高，但有锁定期 (Lockup Period, 通常1-3年) + 通知期 (Notice Period, 30-90天) |
| 透明度 | 相对其他另类投资较高（需定期披露持仓），但仍低于传统共同基金 |
| 费用结构 | 通常2/20（2%管理费 + 20%业绩提成），部分新基金降低至1/10 |
| 高水位线 | 普遍采用，保护投资者，只对新创造的收益收取提成 |

###### 6.2 对冲基金策略 (Hedge Fund Strategies)【考试核心】

| 策略 | 英文 | 运作方式 | 风险 | 回报 | 与股票相关性 |
|------|------|----------|------|------|-------------|
| 股票多空 | Equity Long/Short | 同时持有多头和空头头寸，降低市场风险敞口 | 中等 | 8-12% | 0.5-0.7 |
| 全球宏观 | Global Macro | 基于宏观经济趋势，跨资产类别交易（外汇、利率、股指） | 高 | 10-15% | 0.2-0.4 |
| 事件驱动 | Event Driven | 利用公司特定事件（并购、重组、破产） | 中高 | 10-14% | 0.4-0.6 |
| 相对价值 | Relative Value | 利用相关资产定价偏差，市场中性策略 | 低 | 6-10% | 0.1-0.3 |

###### 6.3 杠杆与风险 (Leverage and Risk)【考试核心】

| 指标 | 公式 | 含义 |
|------|------|------|
| 总杠杆 (Gross Leverage) | (多头 + \|空头\|) / 资本 | 反映基金总敞口，包括多空双边 |
| 净杠杆 (Net Leverage) | (多头 - \|空头\|) / 资本 | 反映市场风险敞口 |

**关键区别**: Gross ≠ Net，两者完全不同。很多对冲基金是净多头 (Net Long)，并非完全对冲市场风险。市场中性策略的Net Leverage接近0。

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 总杠杆 (Gross Leverage) | (Long + \|Short\|) / Capital |
| 净杠杆 (Net Leverage) | (Long - \|Short\|) / Capital |

##### 3. 常见考点与解题思路

1. **策略类型判断**: 题干描述基金的投资方式和持仓特征，要求判断属于哪种策略。**思路**: 多空持仓=Equity L/S；宏观经济判断=Global Macro；公司事件套利=Event Driven；价差套利=Relative Value。
2. **杠杆计算**: 给定多头和空头头寸及资本，计算总杠杆和净杠杆。**思路**: Gross = (多+|空|)/资本；Net = (多-|空|)/资本。
3. **策略风险排序**: 要求按风险水平排序。**思路**: Relative Value (低) < Equity L/S (中) < Event Driven (中高) < Global Macro (高)。

##### 4. 易错点提醒

- **总杠杆 ≠ 净杠杆**: Gross=总敞口（多+|空|），Net=市场敞口（多-|空|），概念完全不同
- **对冲基金并非完全对冲**: 名称中的"对冲"不代表完全对冲市场风险，很多基金是净多头
- **策略风险水平**: 不能凭名称判断风险，Equity L/S实际风险中等
- **锁定期+通知期**: 对冲基金的流动性限制包括锁定期和通知期两个概念
- **高水位线普遍采用**: 是对冲基金保护投资者的重要机制

##### 5. 跨模块关联

- 费用结构 → [[M01-Features-and-Structure.md]] (2/20结构与高水位线)
- 杠杆对比 → [[M03-Private-Capital.md]] (PE杠杆 vs 对冲基金杠杆)
- 业绩衡量 → [[M02-Performance-Measurement.md]] (Sharpe/Sortino应用于对冲基金评估)
### 🌳 核心知识树

```text
🏆 M06: Hedge Funds（对冲基金）
│
├── ⭐ 对冲基金特征 (HF Characteristics) 🎯高频
│   ├── 流动性: 锁定期(1-3年) + 通知期(30-90天)
│   ├── 透明度: 高于PE/VC，低于共同基金
│   ├── 费用: 通常2/20（2%管理费+20%业绩提成）
│   └── 高水位线: 普遍采用，保护投资者
│
├── ⭐ 四大策略 (HF Strategies) 🎯超高頻
│   ├── Equity Long/Short (股票多空)
│   │   ├── 同时持有多头和空头，降低市场风险
│   │   └── 风险中等，与股票相关性0.5-0.7
│   ├── Global Macro (全球宏观)
│   │   ├── 基于宏观经济趋势跨资产交易
│   │   └── 高风险，与股票相关性0.2-0.4
│   ├── Event Driven (事件驱动)
│   │   ├── 利用公司特定事件（并购、重组）
│   │   └── 风险中高，与股票相关性0.4-0.6
│   └── Relative Value (相对价值)
│       ├── 利用定价偏差，市场中性
│       └── 风险低，与股票相关性0.1-0.3
│
├── ⭐ 杠杆指标 (Leverage Metrics) 🎯超高頻
│   ├── 📐 总杠杆 (Gross) = (Long + |Short|) / Capital
│   └── 📐 净杠杆 (Net) = (Long - |Short|) / Capital
│       ⚠️ Gross≠Net，概念完全不同
│
├── ⭐ 对冲基金风险
│   ├── 策略风险: 不同策略风险水平差异大
│   ├── 杠杆风险: 放大收益也放大亏损
│   ├── 流动性风险: 锁定期和通知期限制赎回
│   ├── 对手方风险: 衍生品交易对手违约
│   └── 风格漂移: 偏离既定策略
│
└── ⭐ 对冲基金分散化
    ├── 与传统资产低到中等相关性
    ├── 不同策略之间互补性
    └── ⚠️ 危机时相关性可能上升
```

## 📖 知识点详解

### 知识点1：对冲基金特征（Hedge Fund Characteristics）
**核心概念**：对冲基金是面向合格投资者的私人投资基金，与传统共同基金相比有显著差异。流动性介于PE/VC和传统基金之间——通常设有锁定期（1-3年内不可赎回）和通知期（赎回需提前30-90天通知）。透明度高于PE/VC但低于共同基金——需要定期披露持仓但不完全公开。费用结构通常为2/20（2%管理费+20%业绩提成），部分新基金已降至1/10。高水位线（High Water Mark）被普遍采用——只有当基金净值超过历史最高水平时才能对超额收益收取业绩提成，防止重复收费。
- 流动性：锁定期（1-3年）+ 通知期（30-90天），高于PE/VC低于共同基金
- 透明度：定期披露持仓，高于PE/VC低于共同基金
- 费用：通常2/20结构（2%管理费+20%业绩提成）
- 高水位线：保护投资者，只对新收益收费
**考试应用**：锁定期和通知期的区别——锁定期是最短持有期，通知期是赎回提前告知。高水位线机制是保护LP而非GP的重要设计。

### 知识点2：对冲基金四大策略（Hedge Fund Strategies）
**核心概念**：对冲基金策略按其投资方式和风险特征可分为四大类。股票多空（Equity Long/Short）同时持有多头和空头头寸以降低市场风险，风险中等，与股票相关性较高（0.5-0.7）。全球宏观（Global Macro）基于对宏观经济趋势的判断跨资产类别（外汇、利率、商品、股票）交易，风险较高，与股票相关性低（0.2-0.4）。事件驱动（Event Driven）利用公司特定事件（并购、重组、破产、分拆）套利，风险中高。相对价值（Relative Value）利用相关资产之间的定价偏差进行市场中性套利，风险最低，与股票相关性最低（0.1-0.3）。
- 股票多空（Equity Long/Short）：多+空仓位，降低市场Beta
- 全球宏观（Global Macro）：跨资产宏观交易，高风险
- 事件驱动（Event Driven）：利用公司事件套利，中高风险
- 相对价值（Relative Value）：定价偏差套利，市场中性，低风险
**考试应用**：四大策略的识别和风险排序是最高频考点。风险排序：Relative Value(低) < Equity L/S(中) < Event Driven(中高) < Global Macro(高)。

### 知识点3：杠杆指标——总杠杆与净杠杆（Gross and Net Leverage）
**核心概念**：对冲基金的杠杆通过两个指标衡量。总杠杆（Gross Leverage）= (多头 + |空头|) / 资本，反映基金的全部持仓头寸——包括多头和空头两边，衡量的是总交易规模。净杠杆（Net Leverage）= (多头 - |空头|) / 资本，反映基金的方向性市场敞口——净杠杆为正表示总体看涨（净多头），为负表示总体看跌（净空头），接近0表示市场中性。两者概念完全不同——一个基金可能总杠杆很高（大量多空配对交易）但净杠杆很低（市场中性策略）。
- 📐 总杠杆（Gross）= (Long + |Short|) / Capital
- 📐 净杠杆（Net）= (Long - |Short|) / Capital
- Gross衡量总交易规模，Net衡量方向性风险
- 市场中性策略：Gross高但Net≈0
**考试应用**：Gross vs Net区分是常考陷阱。给定多头和空头头寸分别计算两个杠杆指标。注意：名称中的"对冲"不意味着完全对冲——很多对冲基金是净多头。

### 知识点4：对冲基金风险类型（Hedge Fund Risks）
**核心概念**：对冲基金面临多重风险。策略风险是基金采用的投资策略本身固有的风险——不同策略风险水平差异大。杠杆风险指使用借贷放大头寸规模既放大收益也放大亏损。流动性风险来自锁定期和通知期——市场危机时基金可能暂停赎回（Gates），投资者资金被锁定。交易对手风险来自衍生品交易中对手方可能违约。风格漂移（Style Drift）风险指基金经理偏离既定策略——投资者根据某一策略选择基金，但基金经理可能逐渐改变投资方式。
- 策略风险：策略本身的风险，四大策略风险水平不同
- 杠杆风险：总杠杆和净杠杆代表的财务风险
- 流动性风险：锁定期和通知期限制，危机时可能暂停赎回
- 对手方风险：衍生品交易对手违约风险
- 风格漂移：基金经理偏离既定策略的变化风险
**考试应用**：区分不同类型风险及各自的含义。注意对冲基金的"对冲"不意味着低风险——某些策略（如Global Macro）风险很高。

### 知识点5：对冲基金分散化价值（Diversification Benefits）
**核心概念**：对冲基金通过与传统资产的低到中等相关性提供组合分散化价值。不同策略与股票的相关性差异显著：相对价值策略（相关性0.1-0.3）分散化效果最好，股票多空（相关性0.5-0.7）分散化效果有限。但有两个重要警告：第一，危机时期相关性趋于上升——当系统性事件发生时，几乎所有策略都同时亏损（如2008年金融危机）；第二，对冲基金的收益平滑（微笑估值、流动性较差的持仓按评估值估值）可能人为降低报告的相关性。
- 与传统资产低到中等相关性：提供分散化
- 不同策略分散化效果不同：Relative Value最好，Equity L/S最差
- ⚠️ 危机时相关性上升：分散化收益可能消失
- ⚠️ 收益平滑：可能人为降低报告的相关性
**考试应用**：理解分散化价值的局限性。"危机时相关性上升"是重要考点——分散化在投资者最需要的时候可能失效。

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| 总杠杆 = (Long + |Short|) / Capital | 总敞口杠杆 | 衡量总头寸规模 | 包括多空双边 |
| 净杠杆 = (Long - |Short|) / Capital | 市场敞口杠杆 | 衡量方向性风险 | 市场中性≈0 |
| 管理费 = AUM × 2% | 管理费 | 年度固定费用 | 无论盈亏都收取 |
| 业绩提成 = 超额收益 × 20% | 激励费 | 收益分成 | 受High Water Mark约束 |
| 净回报 = Gross Return - Fees | 投资者所得 | 真实投资回报 | 费用侵蚀显著 |

### 🛠️ 常见考点与解题思路

**Topic 1: 四大策略辨析**
- 题干描述基金的投资方式和持仓特征 → 判断策略类型
- 多空持仓 → Equity L/S
- 宏观经济判断 → Global Macro
- 公司事件套利 → Event Driven
- 价差套利 → Relative Value

**Topic 2: 杠杆计算**
- Gross Leverage = (Long + |Short|) / Capital
- Net Leverage = (Long - |Short|) / Capital
- 市场中性：Net ≈ 0
- 解题：注意空头用绝对值

**Topic 3: 策略风险排序**
- 低风险：Relative Value
- 中等风险：Equity Long/Short
- 中高风险：Event Driven
- 高风险：Global Macro

**Topic 4: 费用计算**
- 管理费直接从AUM中扣除
- 业绩提成需考虑Hurdle Rate和High Water Mark
- 净回报 = 总回报 - 管理费 - 业绩提成

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 总杠杆 = 净杠杆 | 总杠杆=总敞口，净杠杆=市场敞口 | 概念完全不同 |
| 对冲基金名称中的"对冲"=完全对冲市场风险 | 很多基金是净多头的 | 名称不反映实际风险 |
| 策略风险水平仅由名称决定 | 同策略内也有差异 | 看具体持仓和管理人 |
| 锁定期=通知期 | 锁定期是最短持有期，通知期是赎回提前通知 | 两个不同约束 |
| Relative Value = 无风险 | 有模型风险和执行风险 | 价差可能扩大 |
| Global Macro = 股票策略 | 跨资产类别交易 | 外汇、利率、商品、股票 |
| 对冲基金总是提供分散化 | 危机时相关性上升 | 分散化是动态的 |
| 高水位线保护GP | 高水位线保护LP | 防止重复收费 |

### 🔄 跨模块关联

- **费用结构** → [[M01-Alternative-Investment-Features-Methods-and-Structures]]（2/20结构和高水位线）
- **杠杆对比** → [[M03-Investments-in-Private-Capital-Equity-and-Debt]]（PE杠杆vs对冲基金杠杆）
- **业绩衡量** → [[M02-Alternative-Investment-Performance-and-Returns]]（Sharpe/Sortino用于HF评估）
- **对冲基金策略与市场效率** → Equity M03（套利与市场效率）
- **基金结构** → [[M01-Alternative-Investment-Features-Methods-and-Structures]]（GP/LP角色）
- **Global Macro与宏观经济** → Economics M02-M04（宏观策略的决策依据）
- **EV/EBITDA与事件驱动** → Equity M08（并购套利的估值逻辑）

### 📋 复习与刷题提示

- **四大策略特征对比**：运作方式、风险水平、与股票相关性是最高频考点
- **Gross vs Net Leverage计算**：区分总杠杆和净杠杆的计算和含义
- **策略风险排序**：Relative Value < Equity L/S < Event Driven < Global Macro
- **费用结构**：理解2/20和高水位线的保护机制
- **对冲基金vs PE/VC对比**：流动性、透明度、费用结构差异
- **风险类型**：策略风险、杠杆风险、流动性风险、对手方风险
- **刷题建议**：mock中策略判断和杠杆计算最高频
- **注意"对冲"的误导**：名称易引起误解，基金可能保留大量方向性风险

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
