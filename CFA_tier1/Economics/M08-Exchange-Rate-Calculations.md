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

##### 1. 核心知识点（中英双语讲解）

###### 汇率报价基础（Exchange Rate Quote Basics）

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

###### 交叉汇率（Cross Rate Calculation）

**交叉汇率概念**：通过第三种货币计算两种货币之间的汇率。

`A/C = (A/B) × (B/C)`

**计算步骤**：
1. 确定目标配对（如 EUR/GBP）
2. 找到两种货币与共同第三种货币的汇率
3. 相乘约掉中间币种

**买卖价差下的交叉汇率**：计算时要小心"哪个乘哪个"。计算买入价时取保守方向（乘 BID 或除 ASK 取决于方向）。

###### 远期汇率（Forward Exchange Rate）

**远期升水/贴水（Forward Premium/Discount）**：
- `Forward Premium = (Forward Rate − Spot Rate) / Spot Rate`（年化时需乘以 12/N）
- 远期汇率 > 即期汇率 → 基础货币远期升水（forward premium）
- 远期汇率 < 即期汇率 → 基础货币远期贴水（forward discount）

**远期点数（Forward Points）** = Forward Rate − Spot Rate，通常以点数形式报价（1 point = 0.0001 或 0.01，视货币对而定）

###### 抛补利率平价（Covered Interest Parity, CIP）

**CIP公式**：`F = S × (1 + i_d) / (1 + i_f)`

其中：
- F = 远期汇率（直接报价）
- S = 即期汇率（直接报价）
- i_d = 本币利率（domestic interest rate）
- i_f = 外币利率（foreign interest rate）

**CIP的含义**：通过远期合约锁定汇率后，国内外无风险投资收益应相等。如果偏离CIP，存在**套利（arbitrage）** 机会。

###### 无抛补利率平价（Uncovered Interest Parity, UIP）

**UIP公式**：`E(S) = S × (1 + i_d) / (1 + i_f)`

UIP假设投资者不通过远期对冲，而是根据预期的未来即期汇率做决策。预期汇率的变化由利差驱动。

**套利交易（Carry Trade）**：借入低利率货币，投资高利率货币，赚取利差。但这面临汇率风险——高利率货币可能贬值。

##### 2. 关键公式（公式+解释+场景）

**倒数报价**：`B/A = 1 / (A/B)`
- 场景：若 EUR/USD = 1.10，则 USD/EUR = 1/1.10 = 0.9091
- 注意：买卖价差倒置时要交换 bid 和 ask：`(B/A)_bid = 1 / (A/B)_ask`

**交叉汇率**：`A/C = (A/B) × (B/C)`
- 场景：已知 EUR/USD = 1.10，USD/JPY = 110，则 EUR/JPY = 1.10 × 110 = 121

**远期升水**：`Forward Premium = (F − S) / S × (360 / N) × 100%`
- 场景：S = 1.10，F（90天）= 1.1088，则年化升水 = (1.1088 − 1.10) / 1.10 × 4 = 3.2%

**远期点数**：`Forward Points = Forward Rate - Spot Rate`
- 场景：F > S 时 forward points 为正；F < S 时为负。

**抛补利率平价**：`F = S × (1 + i_d) / (1 + i_f)`
- 场景：S = 7.25（USD/CNY），i_d = 2%，i_f = 5%，则 F = 7.25 × 1.02 / 1.05 = 7.0429（人民币远期升水）

**交叉买卖价差**：
- 若目标是 `A/C = (A/B) x (B/C)`：
  - `bid(A/C) = bid(A/B) x bid(B/C)`
  - `ask(A/C) = ask(A/B) x ask(B/C)`
- 若需要倒数报价：`bid(B/A) = 1/ask(A/B)`，`ask(B/A) = 1/bid(A/B)`

**考纲标记**：
- 【考纲重点】倒数报价、交叉汇率、forward premium/discount、forward points、CIP。
- 【考纲内但无核心公式】FX market participants、exchange-rate regime、capital flow intuition。
- 【超纲/扩展】UIP 和 carry trade 是理解辅助；CFA L1 重点不是证明 UIP，而是区分它与 covered arbitrage。

##### 3. 常见考点与解题思路

**考点1：判断升贬值方向**
- 先确定报价方向：A/B上升时，A升值B贬值
- 题干给的是直接报价还是间接报价？确定后再判断

**考点2：交叉汇率计算**
- 步骤：找出中间货币，将汇率配对方向调整一致，相乘
- 如给 EUR/USD 和 USD/GBP，求 EUR/GBP → EUR/USD × USD/GBP

**考点3：套利机会判断**
- 计算CIP理论远期汇率，与市场远期汇率比较
- 如果理论 ≠ 市场 → 可套利
- 套利方向：从利率低的国家借钱，换汇后投资于利率高的国家，再换回

##### 4. 易错点提醒

- **最常见错误：报价方向搞反**。大部分计算错误本质上是 quote-direction error，不是数学问题。
- **倒数报价的买卖价差**：倒置时要交换 bid 和 ask 两个数字，不能简单地取倒数。
- **远期升水≠未来即期汇率一定升值**：远期汇率是今天的定价关系，不等于未来一定会实现。
- **CIP在现实中可能不完美**：存在交易成本、资本管制和对手方风险，但在CFA L1中假设完美市场。
- **套利交易（carry trade）不是套利（arbitrage）**：carry trade承担汇率风险，不是无风险。Arbitrage才是无风险的。

##### 5. 跨模块关联

- 汇率制度对计算背景的影响见 **[[M07-Capital-Flows-and-FX-Markets]]**
- 利率差异对远期汇率的影响与 **[[M04-Monetary-Policy]]** 中的利率政策相连
- 贸易和资本流动影响即期和远期汇率，见 **[[M06-International-Trade]]** 和 **[[M05-Introduction-to-Geopolitics]]**
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
