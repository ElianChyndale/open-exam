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

| 属性          | 内容                                        |
| ----------- | ----------------------------------------- |
| title       | Economics - Map of Content                |
| description | CFA L1 经济学科目学习导航：市场结构、宏观周期、财政货币政策、国际贸易与汇率 |
| subject     | Economics                                 |
| 权重          | 6-9%                                      |
| 考试形式        | 单选题，概念判断+少量计算                             |
| 难度特点        | 微观容易混概念，宏观和汇率容易混机制与公式                     |
| 学习建议        | 先抓市场结构和政策传导，再把 FX 计算单独练熟                  |
| 状态          | 学习中                                       |
| tags        | CFA L1, Economics, MOC                    |

---

## 最关键：先看激励与结构，再看政策，再看传导到利率和汇率

经济学最难的不是记定义，而是看懂机制怎样传到资产价格。

---

## 科目概览

| 模块  | 内容                                   | 难度     | 必考点                                                 | 章节文件                                      |
| --- | ------------------------------------ | ------ | --------------------------------------------------- | ----------------------------------------- |
| M01 | Demand, Supply, and Elasticity       | 概念+轻计算 | curve shifts, elasticity, consumer/producer surplus | [[M01-Demand-Supply-and-Elasticity]]      |
| M02 | The Firm and Market Structures       | 概念     | pricing power, barriers, output/profit logic        | [[M02-The-Firm-and-Market-Structures]]    |
| M03 | Aggregate Output, Prices, and Growth | 概念+计算  | GDP, inflation, real/nominal rates                  | [[M03-Aggregate-Output-Prices-and-Growth]] |
| M04 | Business Cycles and Indicators       | 策略     | phases, indicators, credit/inventory effects        | [[M04-Business-Cycles]]                   |
| M05 | Fiscal Policy                        | 概念+策略  | multipliers, deficits, crowding out                 | [[M05-Fiscal-Policy]]                     |
| M06 | Monetary Policy                      | 概念+策略  | objectives, tools, transmission, credibility        | [[M06-Monetary-Policy]]                   |
| M07 | Geopolitics and Trade                | 概念     | comparative advantage, restrictions, blocs          | [[M07-Geopolitics-and-Trade]]             |
| M08 | Capital Flows and FX Markets         | 概念     | balance of payments, FX regimes, participants       | [[M08-Capital-Flows-and-FX-Markets]]      |
| M09 | Exchange Rate Calculations           | 计算     | quotes, cross rates, forward points, parity         | [[M09-Exchange-Rate-Calculations]]        |

---

## Economics 核心知识树 (Core Knowledge Tree)

```text
Economics (经济学) (M01-M09)
│
├── M01: Demand, Supply, and Elasticity (需求、供给与弹性)【考试核心】↔ 2026 Outline: Demand and Supply
│   ├── 均衡图（Equilibrium map）
│   │   ├── 核心公式 (English)
│   │   │   ├── 需求价格弹性：`Own-price elasticity = %ΔQd / %ΔP`
│   │   │   ├── 收入弹性：`Income elasticity = %ΔQd / %ΔIncome`
│   │   │   ├── 交叉价格弹性：`Cross-price elasticity = %ΔQx / %ΔPy`
│   │   │   └── 总收益：`TR = Price x Quantity`
│   │   ├── 价格变化 → 沿曲线移动（price change → movement along curve）
│   │   ├── 收入、偏好、投入成本、技术、税收 → 曲线移动（income, tastes, input cost, technology, taxes → curve shifts）
│   │   └── 价格管制与税收改变剩余和无谓损失（price control and taxes alter surplus and deadweight loss）
│   ├── 弹性工具包（Elasticity toolkit）
│   │   ├── 需求价格弹性与总收益的关系（own-price elasticity and total revenue relation）
│   │   ├── 收入弹性区分正常品/低档品和必需品/奢侈品（income elasticity identifies normal/inferior and necessity/luxury）
│   │   └── 交叉价格弹性区分替代品与互补品（cross-price elasticity distinguishes substitutes vs complements）
│   └── 注意：elasticity is local and unit-free; slope alone is not the same object【考试陷阱】
│
├── M02: The Firm and Market Structures (企业与市场结构)【考试核心】↔ CFA Institute 2026 Firm and Market Structures
│   ├── 成本与利润逻辑（Cost and profit logic）
│   │   ├── 会计利润与经济利润（accounting profit vs economic profit）
│   │   ├── 短期固定成本与长期调整（short run fixed costs vs long run adjustment）
│   │   └── 边际收益/边际成本决策逻辑（marginal revenue / marginal cost decision intuition）
│   ├── 市场结构比较（Structure comparison）
│   │   ├── 完全竞争、垄断竞争、寡头、垄断（perfect competition, monopolistic competition, oligopoly, monopoly）
│   │   ├── 进入壁垒、产品差异化、定价权、策略互动（entry barriers, product differentiation, pricing power, strategic interaction）
│   │   └── 集中度指标有助于但不替代竞争分析（concentration measures help but do not replace competitive analysis）
│   └── 注意：zero economic profit can coexist with positive accounting profit
│
├── M03: Aggregate Output, Prices, and Growth (总产出、价格与增长)【考试核心】↔ 2026 Outline: Aggregate Output
│   ├── 产出衡量（Output measures）
│   │   ├── 核心公式 (English)
│   │   │   ├── 支出法GDP：`GDP = C + I + G + (X-M)`
│   │   │   ├── GDP平减指数：`GDP deflator = (Nominal GDP / Real GDP) x 100`
│   │   │   ├── 通胀率：`Inflation rate = (Index_t / Index_{t-1}) - 1`
│   │   │   └── 费雪等式：`(1 + r_nominal) = (1 + r_real)(1 + inflation)`
│   │   ├── GDP支出恒等式与增加值逻辑（GDP expenditure identity and value-added intuition）
│   │   ├── 名义与实际GDP；GDP平减指数；人均视角（nominal vs real GDP; GDP deflator; per-capita lens）
│   │   └── 潜在产出与增长来源：劳动、资本、生产率（potential output and growth sources: labor, capital, productivity）
│   ├── 价格与劳动力视角（Price and labor lens）
│   │   ├── 通胀、通缩、反通胀（inflation vs deflation vs disinflation）
│   │   ├── 失业类型与产出缺口（unemployment types and output gap intuition）
│   │   └── 名义与实际利率（nominal vs real interest rate）
│   └── 注意：inflation-adjusted comparisons must use real variables consistently
│
├── M04: Business Cycles and Indicators (商业周期与指标)【考试核心】↔ 2026 Outline: Business Cycles
│   ├── 周期结构（Cycle anatomy）
│   │   ├── 扩张 → 顶峰 → 收缩 → 谷底（expansion → peak → contraction → trough）
│   │   ├── 库存、劳动力、住房、信贷、利润按不同节奏变化（inventory, labor, housing, credit, and profits move with different timing）
│   │   └── 衰退叙事常在数据修正前出现（recession narrative often appears before data revisions settle）
│   ├── 指标分类（Indicator classes）
│   │   ├── 先行、同步、滞后指标（leading, coincident, lagging）
│   │   └── 扩散指数与综合指数减少单一指标的过度反应（diffusion and composites reduce single-indicator overreaction）
│   └── 注意：indicator timing is the point; names alone are not enough
│
├── M05: Fiscal Policy (财政政策)【考试核心】↔ 2026 Outline: Fiscal Policy
│   ├── 政策工具（Tools）
│   │   ├── 支出、税收、转移支付、自动稳定器（spending, taxation, transfers, automatic stabilizers）
│   │   ├── 扩张性与紧缩性立场（expansionary vs contractionary stance）
│   │   └── 乘数取决于漏出、闲置产能、政策时机（multiplier depends on leakages, slack, policy timing）
│   ├── 约束条件（Constraints）
│   │   ├── 赤字、债务可持续性、挤出效应、实施时滞（deficits, debt sustainability, crowding out, implementation lag）
│   │   └── 再分配与供给侧后果（redistributive and supply-side consequences）
│   └── 注意：stimulus impact can fade if financing pressure lifts rates or confidence falls
│
├── M06: Monetary Policy (货币政策)【考试核心】↔ 2026 Outline: Monetary Policy
│   ├── 央行设计（Central bank design）
│   │   ├── 价格稳定、增长/就业背景、可信度、独立性（price stability, growth/employment context, credibility, independence）
│   │   ├── 政策利率、准备金、公开市场/资产负债表工具（policy rate, reserves, open-market/balance-sheet tools）
│   │   └── 货币与信贷条件传导至支出和资产价格（money and credit conditions transmit to spending and asset prices）
│   ├── 传导机制（Transmission）
│   │   ├── 利率渠道、信贷渠道、资产价格渠道、汇率渠道（rate channel, credit channel, asset-price channel, exchange-rate channel）
│   │   └── 中性/紧缩/宽松取决于实体经济背景（neutral/tight/easy stance depends on real economy context）
│   └── 注意：rate cut is an action; easing effectiveness is an outcome
│
├── M07: Geopolitics and Trade (地缘政治与贸易)【考试核心】↔ 2026 Outline: International Trade
│   ├── 贸易逻辑（Trade logic）
│   │   ├── 绝对优势与比较优势（absolute vs comparative advantage）
│   │   ├── 专业化与贸易收益（gains from specialization and trade）
│   │   └── 关税、配额、出口补贴、非关税壁垒（tariffs, quotas, export subsidies, non-tariff barriers）
│   ├── 区域一体化（Integration）
│   │   ├── 自贸区 → 关税同盟 → 共同市场 → 经济/货币联盟（free trade area → customs union → common market → economic/monetary union）
│   │   └── 地缘政治冲击可改变供应链、风险溢价、政策路径（geopolitical shocks can alter supply chains, risk premia, policy paths）
│   └── 注意：a policy can help a visible group and still reduce total welfare
│
├── M08: Capital Flows and FX Markets (资本流动与外汇市场)【考试核心】↔ 2026 Outline: FX Markets
│   ├── 外部账户（External accounts）
│   │   ├── 经常账户与资本/金融账户（current account vs capital/financial account）
│   │   ├── 资本流动连接储蓄、投资与汇率压力（capital flows connect saving, investment, and exchange-rate pressure）
│   │   └── 汇率制度从浮动到更受管理的体系（FX regimes range from floating to more managed systems）
│   ├── 外汇市场角色（FX market roles）
│   │   ├── 即期、远期、掉期、参与者动机（spot, forward, swap, participant motives）
│   │   └── 套期保值与投机共享工具但目的不同（hedging and speculation share instruments but not purpose）
│   └── 注意：trade balance alone does not explain every currency move
│
└── M09: Exchange Rate Calculations (汇率计算)【考试核心】↔ 2026 Outline: Exchange Rate Calculations
    ├── 报价机制（Quote mechanics）
    │   ├── 核心公式 (English)
    │   │   ├── 交叉汇率：`A/C = (A/B) x (B/C)`
    │   │   └── 倒数报价：`B/A = 1/(A/B)`
    │   ├── 直接报价与间接报价；基础货币与报价货币（direct vs indirect quote; base vs price currency）
    │   ├── 升值/贬值遵循报价惯例（appreciation/depreciation follows quote convention）
    │   └── 买卖价差倒置与交叉汇率逻辑（bid/ask inversion and cross-rate logic）
    ├── 远期机制（Forward mechanics）
    │   ├── 核心公式 (English)
    │   │   ├── 远期升水：`Forward premium = (F-S)/S`
    │   │   └── 抛补利率平价：`F = S(1+id)/(1+if)`
    │   ├── 远期升水/贴水与远期点数（forward premium/discount and forward points）
    │   ├── 抛补利率平价将外汇远期与利差挂钩（covered interest parity ties FX forward to interest differential）
    │   └── 套利推理检查方向合理性（arbitrage reasoning checks directional sanity）
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
Demand and Supply（需求与供给）
└── Market Structures（市场结构）
    └── Aggregate Output and Prices（总产出与价格）
        ├── Business Cycles（经济周期）
        │   ├── Fiscal Policy（财政政策）
        │   └── Monetary Policy（货币政策）
        └── International Trade（国际贸易）
            └── Currency Exchange Rates（汇率）
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
