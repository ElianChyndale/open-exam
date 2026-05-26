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

## 📖 知识点详解

### 知识点1：汇率报价基础（Exchange Rate Quote Basics）

**报价方式（Quote Convention）**：
- **直接报价（Direct Quote）**：一单位外币折合多少本币（DC/FC）。在中国，USD/CNY = 7.25 就是直接报价。
- **间接报价（Indirect Quote）**：一单位本币折合多少外币（FC/DC）。

**基础货币与报价货币（Base Currency vs Price Currency）**：
- 在 A/B 报价中：A 是**基础货币（base currency）**，B 是**报价货币（price currency）**
- 汇率表示 1 单位基础货币可以兑换多少报价货币

**升值与贬值（Appreciation and Depreciation）**：
- A/B 上升 → A 升值（appreciates），B 贬值（depreciates）
- 注意：必须先明确报价方向再判断升贬值！

**买卖价差（Bid-Ask Spread）**：
- **买入价（Bid）**：做市商愿意买入基础货币的价格
- **卖出价（Ask/Offer）**：做市商愿意卖出基础货币的价格
- 做市商低买高卖：Bid < Ask，差额 = 交易成本

### 知识点2：交叉汇率（Cross Rate Calculation）

**交叉汇率概念**：通过第三种货币计算两种货币之间的汇率。

`A/C = (A/B) × (B/C)`

**计算步骤**：
1. 确定目标配对（如 EUR/GBP）
2. 找到两种货币与共同第三种货币的汇率
3. 相乘约掉中间币种

**买卖价差下的交叉汇率**：计算时要小心"哪个乘哪个"。计算买入价时取保守方向（乘 BID 或除 ASK 取决于方向）。

### 知识点3：远期汇率（Forward Exchange Rate）

**远期升水/贴水（Forward Premium/Discount）**：
- `Forward Premium = (Forward Rate − Spot Rate) / Spot Rate`（年化时需乘以 12/N）
- 远期汇率 > 即期汇率 → 基础货币远期升水（forward premium）
- 远期汇率 < 即期汇率 → 基础货币远期贴水（forward discount）

**远期点数（Forward Points）** = Forward Rate − Spot Rate，通常以点数形式报价（1 point = 0.0001 或 0.01，视货币对而定）

### 知识点4：抛补利率平价（Covered Interest Parity, CIP）

**CIP公式**：`F = S × (1 + i_d) / (1 + i_f)`

其中：
- F = 远期汇率（直接报价）
- S = 即期汇率（直接报价）
- i_d = 本币利率（domestic interest rate）
- i_f = 外币利率（foreign interest rate）

**CIP的含义**：通过远期合约锁定汇率后，国内外无风险投资收益应相等。如果偏离CIP，存在**套利（arbitrage）** 机会。

### 知识点5：无抛补利率平价（Uncovered Interest Parity, UIP）

**UIP公式**：`E(S) = S × (1 + i_d) / (1 + i_f)`

UIP假设投资者不通过远期对冲，而是根据预期的未来即期汇率做决策。预期汇率的变化由利差驱动。

**套利交易（Carry Trade）**：借入低利率货币，投资高利率货币，赚取利差。但这面临汇率风险——高利率货币可能贬值。

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
