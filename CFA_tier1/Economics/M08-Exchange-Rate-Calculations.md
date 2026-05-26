---
title: "M08 — Exchange Rate Calculations"
description: "CFA Level I 2026 official module: Exchange Rate Calculations"
module: M08
subject: "Economics"
topic_area: Economics
curriculum_year: 2026
official_module: "Module 8: Exchange Rate Calculations"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Economics
  - official_2026
---

# M08: Exchange Rate Calculations

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Exchange Rate Calculations
- 8.01 | Introduction
- 8.02 | Cross-Rate Calculations
- 8.03 | Forward Rate Calculations

## Learning Outcome Statements

The candidate should be able to:

- calculate and interpret currency cross-rates
- explain the arbitrage relationship between spot and forward exchange rates and interest rates, calculate a forward rate using points or in percentage terms, and interpret a forward discount or premium

## Local Study Notes

### Migrated from `CFA_tier1/Economics/M08-Exchange-Rate-Calculations.md`

_Alignment score: 1.00. Original official module field: Module 8: Exchange Rate Calculations._

#### M08: Exchange Rate Calculations（汇率计算）

### 🌳 核心知识树

```text
🏆 M08: Exchange Rate Calculations（汇率计算）
│
├── ⭐ 汇率报价基础 🎯超高頻
│   ├── 直接报价: 1单位外币=多少本币 (DC/FC)
│   ├── 间接报价: 1单位本币=多少外币 (FC/DC)
│   ├── 基础货币 vs 报价货币: A/B中A是基础, B是报价
│   ├── 升值/贬值: A/B↑ → A升值, B贬值
│   └── 买卖价差: Bid<Ask, 做市商低买高卖
│
├── ⭐ 交叉汇率 🎯超高頻
│   ├── A/C = (A/B) × (B/C)
│   ├── 通过中间货币间接计算
│   └── ⚠️ 买卖价差下方向要小心！
│
├── ⭐ 远期汇率 🎯高频
│   ├── Forward Premium = (F−S)/S × 360/N × 100%
│   ├── Forward Points = F − S
│   ├── F>S → 基础货币远期升水
│   └── F<S → 基础货币远期贴水
│
├── ⭐ 抛补利率平价 (CIP) 🎯高频
│   ├── F = S × (1 + i_d) / (1 + i_f)
│   ├── 远期锁定后国内外收益相等
│   └── 偏离CIP → 套利机会
│
├── ⭐ 无抛补利率平价 (UIP)
│   ├── E(S) = S × (1 + i_d) / (1 + i_f)
│   ├── 无远期对冲，基于预期
│   └── ⚠️ CFA L1非核心考点
│
└── ⭐ 套利交易 (Carry Trade)
    ├── 借低利率货币 → 投高利率货币
    └── ⚠️ 不是无风险套利！存在汇率风险
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| 倒数报价: B/A = 1 / (A/B) | 报价方向反转 | 已知A/B求B/A | 买卖价差倒置时交换bid和ask |
| 交叉汇率: A/C = (A/B) × (B/C) | 通过中间币种计算 | 无直接报价时的汇率 | 方向对齐，约掉中间币种 |
| Forward Premium = (F−S)/S × (360/N) × 100% | 远期升/贴水率 | 判断远期方向 | 年化处理，区分premium/discount |
| Forward Points = F − S | 远期点数 | 市场报价形式 | 正=升水，负=贴水 |
| CIP: F = S × (1 + i_d) / (1 + i_f) | 抛补利率平价 | 理论远期汇率计算 | 假设完美市场无交易成本 |
| 交叉买卖价差: bid(A/C)=bid(A/B)×bid(B/C) | 含价差的交叉汇率 | 实际交易中的交叉汇率 | 调方向时用倒数规则 |

### 🛠️ 常见考点与解题思路

**Topic 1: 升贬值方向判断**
- 确定报价方向：A/B格式，A是基础货币
- A/B上升 → A升值，B贬值
- 解题：先明确是直接报价还是间接报价

**Topic 2: 交叉汇率计算**
- 找出共同中间货币
- 将汇率做乘法或除法对齐方向
- 含买卖价差时小心方向
- 解题：如需倒数先用倒数公式，再相乘

**Topic 3: 套利机会判断 (CIP)**
- 计算CIP理论远期汇率
- 与市场远期汇率比较
- 若理论 ≠ 市场 → 有套利机会
- 套利方向：低利率国借钱 → 换汇 → 高利率国投资 → 远期换回
- 解题：F理论 > F市场 → 借入外币，反之借入本币

**Topic 4: 远期升水/贴水与利差关系**
- 高利率货币 → 远期贴水
- 低利率货币 → 远期升水
- 解题：利率高的国家，远期汇率低于即期（贴水）

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 直接报价和间接报价搞反 | 直接报价: DC/FC; 间接报价: FC/DC | 报价方向是计算基础 |
| A/B上升认为B升值 | A/B上升表示A升值B贬值 | 基础货币升值方向 |
| 倒数报价直接取倒数 | 含价差时需交换bid和ask | 做市商总是低买高卖 |
| 远期升水=未来即期一定升值 | 远期是今天定价关系，不等于未来实现 | 远期≠预期，升贴水是利率关系决定 |
| CIP在现实中完美成立 | 有交易成本/资本管制/对手方风险 | CFA L1假设完美市场 |
| Carry trade = Arbitrage | Carry trade承担汇率风险，不是无风险 | 混淆两者的根本区别 |
| Cross rate只用乘法 | 取决于报价方向，可能需用除法 | 关键是约掉中间货币 |
| 买卖价差不影响交叉汇率计算 | 含价差时计算方向必须正确 | 选错方向导致错误结果 |

### 🔄 跨模块关联

- **汇率制度与报价背景** → [[M07-Capital-Flows-and-FX-Markets]]（不同制度下的汇率定价机制）
- **利率差异对远期汇率的影响** → [[M04-Monetary-Policy]]（央行利率政策驱动远期升贴水）
- **资本流动对即期汇率的影响** → [[M07-Capital-Flows-and-FX-Markets]]（资本流入/流出对即期汇率的影响）
- **贸易对汇率的影响** → [[M06-International-Trade]]（贸易收支通过经常账户影响汇率）
- **地缘风险对汇率的影响** → [[M05-Introduction-to-Geopolitics]]（政治风险溢价影响汇率）

### 📋 复习与刷题提示

- **倒数报价必考题**：含买卖价差时的倒置规则（交换bid和ask）
- **交叉汇率计算**：确定中间货币，对齐方向，乘法约掉
- **CIP套利**：理解套利方向，记住低利率货币远期升水
- **Forward premium/discount**：年化计算方法
- **报价方向是一切计算的基础**：所有错误的80%来自报价方向搞反
- **刷题建议**：交叉汇率和forward点数计算最高频，CIP套利次之
- **先判断报价方向再计算**：养成这个习惯能避免大多数错误
- **注意考纲边界**：UIP不是CFA L1核心考点，但有助于理解
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
