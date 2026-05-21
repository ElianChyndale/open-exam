---
title: 00-Economics-MOC
description: CFA Level I Economics master MOC for microeconomics, macro policy, trade, FX formulas, and exam traps.
subject: Economics
topic_area: Economics
level: CFA Level I
exam_weight: 6-9%
exam_format: 单选题
difficulty: 微观概念与宏观传导机制易混
note_type: master_moc
status: 学习中
aliases:
  - Economics 知识框架
  - 经济学 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Economics
  - formulas
---

# 00-Economics-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Economics - Map of Content |
| description | CFA L1 经济学科目学习导航：市场结构、宏观周期、财政货币政策、国际贸易与汇率 |
| subject | Economics |
| 权重 | 6-9% |
| 考试形式 | 单选题，概念判断+少量计算 |
| 难度特点 | 微观容易混概念，宏观和汇率容易混机制与公式 |
| 学习建议 | 先抓市场结构和政策传导，再把 FX 计算单独练熟 |
| 状态 | 学习中 |
| tags | CFA L1, Economics, MOC |

---

## 最关键：先看激励与结构，再看政策，再看传导到利率和汇率

经济学最难的不是记定义，而是看懂机制怎样传到资产价格。

---

## 科目概览

| 模块 | 内容 | 难度 | 必考点 |
|------|------|------|--------|
| M01 | Demand, Supply, and Elasticity | 概念+轻计算 | curve shifts, elasticity, consumer/producer surplus |
| M02 | The Firm and Market Structures | 概念 | pricing power, barriers, output/profit logic |
| M03 | Aggregate Output, Prices, and Growth | 概念+计算 | GDP, inflation, real/nominal rates |
| M04 | Business Cycles and Indicators | 策略 | phases, indicators, credit/inventory effects |
| M05 | Fiscal Policy | 概念+策略 | multipliers, deficits, crowding out |
| M06 | Monetary Policy | 概念+策略 | objectives, tools, transmission, credibility |
| M07 | Geopolitics and Trade | 概念 | comparative advantage, restrictions, blocs |
| M08 | Capital Flows and FX Markets | 概念 | balance of payments, FX regimes, participants |
| M09 | Exchange Rate Calculations | 计算 | quotes, cross rates, forward points, parity |

---

## Economics 核心知识树

```text
Economics (M01-M09)
│
├── M01: Demand, Supply, and Elasticity【考试核心】↔ 2026 Outline: Demand and Supply
│   ├── Equilibrium map
│   │   ├── 核心公式
│   │   │   ├── `Own-price elasticity = %ΔQd / %ΔP`
│   │   │   ├── `Income elasticity = %ΔQd / %ΔIncome`
│   │   │   ├── `Cross-price elasticity = %ΔQx / %ΔPy`
│   │   │   └── `TR = Price x Quantity`
│   │   ├── price change -> movement along curve
│   │   ├── income, tastes, input cost, technology, taxes -> curve shifts
│   │   └── price control and taxes alter surplus and deadweight loss
│   ├── Elasticity toolkit
│   │   ├── own-price elasticity and total revenue relation
│   │   ├── income elasticity identifies normal/inferior and necessity/luxury intuition
│   │   └── cross-price elasticity distinguishes substitutes vs complements
│   └── 注意：elasticity is local and unit-free; slope alone is not the same object【考试陷阱】
│
├── M02: The Firm and Market Structures【考试核心】↔ CFA Institute 2026 Firm and Market Structures
│   ├── Cost and profit logic
│   │   ├── accounting profit vs economic profit
│   │   ├── short run fixed costs vs long run adjustment
│   │   └── marginal revenue / marginal cost decision intuition
│   ├── Structure comparison
│   │   ├── perfect competition, monopolistic competition, oligopoly, monopoly
│   │   ├── entry barriers, product differentiation, pricing power, strategic interaction
│   │   └── concentration measures help but do not replace competitive analysis
│   └── 注意：zero economic profit can coexist with positive accounting profit
│
├── M03: Aggregate Output, Prices, and Growth【考试核心】↔ 2026 Outline: Aggregate Output
│   ├── Output measures
│   │   ├── 核心公式
│   │   │   ├── `GDP = C + I + G + (X-M)`
│   │   │   ├── `GDP deflator = (Nominal GDP / Real GDP) x 100`
│   │   │   ├── `Inflation rate = (Index_t / Index_{t-1}) - 1`
│   │   │   └── `(1 + r_nominal) = (1 + r_real)(1 + inflation)`
│   │   ├── GDP expenditure identity and value-added intuition
│   │   ├── nominal vs real GDP; GDP deflator; per-capita lens
│   │   └── potential output and growth sources: labor, capital, productivity
│   ├── Price and labor lens
│   │   ├── inflation vs deflation vs disinflation
│   │   ├── unemployment types and output gap intuition
│   │   └── nominal vs real interest rate
│   └── 注意：inflation-adjusted comparisons must use real variables consistently
│
├── M04: Business Cycles and Indicators【考试核心】↔ 2026 Outline: Business Cycles
│   ├── Cycle anatomy
│   │   ├── expansion -> peak -> contraction -> trough
│   │   ├── inventory, labor, housing, credit, and profits move with different timing
│   │   └── recession narrative often appears before data revisions settle
│   ├── Indicator classes
│   │   ├── leading, coincident, lagging
│   │   └── diffusion and composites reduce single-indicator overreaction
│   └── 注意：indicator timing is the point; names alone are not enough
│
├── M05: Fiscal Policy【考试核心】↔ 2026 Outline: Fiscal Policy
│   ├── Tools
│   │   ├── spending, taxation, transfers, automatic stabilizers
│   │   ├── expansionary vs contractionary stance
│   │   └── multiplier depends on leakages, slack, policy timing
│   ├── Constraints
│   │   ├── deficits, debt sustainability, crowding out, implementation lag
│   │   └── redistributive and supply-side consequences
│   └── 注意：stimulus impact can fade if financing pressure lifts rates or confidence falls
│
├── M06: Monetary Policy【考试核心】↔ 2026 Outline: Monetary Policy
│   ├── Central bank design
│   │   ├── price stability, growth/employment context, credibility, independence
│   │   ├── policy rate, reserves, open-market/balance-sheet tools
│   │   └── money and credit conditions transmit to spending and asset prices
│   ├── Transmission
│   │   ├── rate channel, credit channel, asset-price channel, exchange-rate channel
│   │   └── neutral/tight/easy stance depends on real economy context
│   └── 注意：rate cut is an action; easing effectiveness is an outcome
│
├── M07: Geopolitics and Trade【考试核心】↔ 2026 Outline: International Trade
│   ├── Trade logic
│   │   ├── absolute vs comparative advantage
│   │   ├── gains from specialization and trade
│   │   └── tariffs, quotas, export subsidies, non-tariff barriers
│   ├── Integration
│   │   ├── free trade area -> customs union -> common market -> economic/monetary union
│   │   └── geopolitical shocks can alter supply chains, risk premia, policy paths
│   └── 注意：a policy can help a visible group and still reduce total welfare
│
├── M08: Capital Flows and FX Markets【考试核心】↔ 2026 Outline: FX Markets
│   ├── External accounts
│   │   ├── current account vs capital/financial account intuition
│   │   ├── capital flows connect saving, investment, and exchange-rate pressure
│   │   └── FX regimes range from floating to more managed systems
│   ├── FX market roles
│   │   ├── spot, forward, swap, participant motives
│   │   └── hedging and speculation share instruments but not purpose
│   └── 注意：trade balance alone does not explain every currency move
│
└── M09: Exchange Rate Calculations【考试核心】↔ 2026 Outline: Exchange Rate Calculations
    ├── Quote mechanics
    │   ├── 核心公式
    │   │   ├── `A/C = (A/B) x (B/C)`
    │   │   └── `B/A = 1/(A/B)`
    │   ├── direct vs indirect quote; base vs price currency
    │   ├── appreciation/depreciation follows quote convention
    │   └── bid/ask inversion and cross-rate logic
    ├── Forward mechanics
    │   ├── 核心公式
    │   │   ├── `Forward premium = (F-S)/S`
    │   │   └── `F = S(1+id)/(1+if)`
    │   ├── forward premium/discount and forward points
    │   ├── covered interest parity ties FX forward to interest differential
    │   └── arbitrage reasoning checks directional sanity
    └── 注意：most FX arithmetic errors are quote-direction errors wearing a calculator costume
```

---

## 核心对比专题

| 对比项 | 本质 | 风险 | 回报/用途 | 相关性 | 费用/代价 |
|--------|------|------|-----------|--------|-----------|
| Perfect Competition vs Monopoly | price taker vs price maker | monopoly 可能资源错配 | competition 提高效率，monopoly 有定价权 | 与 entry barriers 强相关 | monopoly 可能带来 deadweight loss |
| Expansionary Fiscal vs Expansionary Monetary | 政府预算工具 vs 中央银行货币工具 | 赤字/通胀 vs transmission failure | 刺激总需求 | 常在周期低迷时配合 | 代价是债务或通胀压力 |
| Nominal vs Real GDP | current prices vs inflation-adjusted output | 混淆会误判真实增长 | real GDP 更适合比较实际产出 | 与 inflation measure 强相关 | 无直接费用 |
| Spot Rate vs Forward Rate | 即期兑换 vs 未来锁定汇率 | forward 定价判断错误 | forward 用于锁定未来 FX 风险 | 与 interest differential 强相关 | carry cost / opportunity cost |
| Tariff vs Quota | 税收壁垒 vs 数量限制 | 两者都扭曲贸易 | tariff 产生政府收入；quota 常让进口配额受益 | 都削弱自由贸易 | 社会福利损失 |
| Direct Quote vs Indirect Quote | 本币每外币 vs 外币每本币的视角切换 | 升贬值判断翻车 | 都描述同一 FX price | 互为倒数 | bid/ask inversion 易错 |
| Current Account vs Financial Account | 商品服务收入流 vs 资本融资流 | 只盯贸易忽视资本流 | 共同解释外部平衡 | 与 FX 压力相关 | 政策含义不同 |

---

## 跨模块关联

```text
Demand/Supply
└── Market Structures
    └── Aggregate Output and Prices
        ├── Business Cycles
        │   ├── Fiscal Policy
        │   └── Monetary Policy
        └── International Trade
            └── Currency Exchange Rates
```

---

## 通用分析框架

### 框架1：政策题判断树

1. 先判断经济在衰退还是过热
2. 再看工具来自政府还是央行
3. 再判断是扩张还是收缩
4. 最后推导对增长、通胀、利率、汇率的方向影响

### 框架2：市场结构题判断树

1. 先看 entry barriers
2. 再看 firms 数量和产品差异化
3. 再看 pricing power
4. 据此锁定 market structure

### 框架3：汇率题决策树

1. 先看 quote convention
2. 再算 cross rate / forward relation
3. 最后解释 domestic currency 是 premium 还是 discount

---

## 核心公式速查

### M01-M03 Micro and Macro Measures

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Own-price Elasticity | `%ΔQ_d / %ΔP` | `M01` | magnitude 判 elastic/inelastic |
| Income Elasticity | `%ΔQ_d / %ΔIncome` | `M01` | sign 与 size 都有信息 |
| Cross-price Elasticity | `%ΔQ_x / %ΔP_y` | `M01` | substitutes positive |
| Total Revenue | `TR = Price x Quantity` | `M01` | 与 elasticity 方向联动 |
| GDP Expenditure Identity | `GDP = C + I + G + (X-M)` | `M03` | 宏观入口 |
| GDP Deflator | `(Nominal GDP / Real GDP) x 100` | `M03` | price level lens |
| Inflation Rate | `(Index_t / Index_{t-1}) - 1` | `M03` | CPI/deflator 都可 |
| Fisher Exact | `(1 + r_nominal) = (1 + r_real)(1 + inflation)` | `M03` | 口径最稳 |
| Fisher Approximation | `r_real ≈ r_nominal - inflation` | `M03` | 小率近似 |

### M09 FX Calculations

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Cross Rate | `A/C = (A/B) x (B/C)` | `M09` | 中间币种要约掉 |
| Inverted Quote | `B/A = 1 / (A/B)` | `M09` | bid/ask inversion 要换边 |
| Forward Premium | `(F - S) / S` | `M09` | 报价方向先定 |
| Forward Points | `Forward Rate - Spot Rate` | `M09` | points sign 看 quote |
| Covered Interest Parity | `F = S[(1 + i_d)/(1 + i_f)]` | `M09` | domestic/foreign 先定义 |

---

## 高频考试陷阱速查

| 错误理解 | 正确理解 |
|----------|----------|
| 价格变化导致需求曲线右移 | 价格变化通常只是沿曲线移动 |
| monopoly 一定高利润且无风险 | 也受监管、需求弹性和替代品影响 |
| nominal GDP 增长高说明经济更强 | 可能只是通胀高 |
| leading indicator 是确认当前周期 | leading 是预测未来方向 |
| expansionary fiscal 就一定降低利率 | 也可能挤出私人投资 |
| monetary easing 一定立即刺激信贷 | 传导可能失灵 |
| tariff 和 quota 只是形式不同 | tariff 有政府收入，quota 不一定 |
| forward premium 表示一定会升值 | 它先是定价关系，不等于必然实现 |
| 本币报价上升一定是本币升值 | 先看 quote convention |
| 汇率题可以不看 domestic/foreign 定义 | 不看报价方向最容易整题错掉 |
| economic profit 为零就是公司亏损 | 可能仍有正常会计利润和资本补偿 |
| 贸易逆差单独决定本币走势 | 资本流、政策、利差和预期都可能主导 |
