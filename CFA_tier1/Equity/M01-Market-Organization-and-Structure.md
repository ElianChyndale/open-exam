---
title: "M01 — Market Organization and Structure"
description: "CFA Level I 2026 official module: Market Organization and Structure"
module: M01
subject: "Equity Investments"
topic_area: Equity
curriculum_year: 2026
official_module: "Module 1: Market Organization and Structure"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Equity
  - official_2026
---

# M01: Market Organization and Structure

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Market Organization and Structure
- 1.01 | Introduction
- 1.02 | The Functions of the Financial System
- 1.03 | Assets and Contracts
- 1.04 | Securities
- 1.05 | Currencies, Commodities, and Real Assets
- 1.06 | Contracts
- 1.07 | Financial Intermediaries
- 1.08 | Securitizers, Depository Institutions and Insurance Companies
- 1.09 | Settlement and Custodial Services and Summary
- 1.10 | Positions and Short Positions
- 1.11 | Leveraged Positions
- 1.12 | Orders and Execution Instructions
- 1.13 | Validity Instructions and Clearing Instructions
- 1.14 | Primary Security Markets
- 1.15 | Secondary Security Market and Contract Market Structures
- 1.16 | Well-functioning Financial Systems
- 1.17 | Market Regulation
- 1.18 | Summary

## Learning Outcome Statements

The candidate should be able to:

- explain the main functions of the financial system
- describe classifications of assets and markets
- describe the major types of securities, currencies, contracts, commodities, and real assets that trade in organized markets, including their distinguishing characteristics and major subtypes
- describe types of financial intermediaries and services that they provide
- compare positions an investor can take in an asset
- calculate and interpret the leverage ratio, the rate of return on a margin transaction, and the security price at which the investor would receive a margin call
- compare execution, validity, and clearing instructions
- compare market orders with limit orders
- define primary and secondary markets and explain how secondary markets support primary markets
- describe how securities, contracts, and currencies are traded in quote-driven, order-driven, and brokered markets
- describe characteristics of a well-functioning financial system
- describe objectives of market regulation

## Local Study Notes

### Migrated from `CFA_tier1/Equity/M01-Market-Organization-and-Structure.md`

_Alignment score: 1.00. Original official module field: Module 1: Market Organization and Structure._

#### M01: 市场组织与结构 (Market Organization and Structure)

##### 1. 核心知识点

###### 市场管道 (Market plumbing)
- **初级市场 (primary market)** 筹集资本，公司通过 IPO/SEO 发行新证券；**二级市场 (secondary market)** 转让所有权，投资者之间交易已发行证券
- **做市商 (broker/dealer)**、**拍卖市场 (auction)**、**报价驱动市场 (quote-driven)**、**订单驱动市场 (order-driven)** 四种结构决定价格发现机制
- **流动性维度 (liquidity dimensions)**：**紧度 (tightness)** — 买卖价差大小；**深度 (depth)** — 大额订单对价格的影响；**弹性 (resiliency)** — 价格偏离后恢复速度

###### 订单与交易 (Orders and trading)
- **指令类型 (instruction types)**：**市价单 (market order)** 追求立即执行，**限价单 (limit order)** 控制价格，**止损单 (stop order)** 触发后转为市价单；**执行指令 (execution instructions)** 与**有效期限指令 (validity instructions)** 约束订单行为
- **交易成本 (transaction costs)**：**显性成本 (explicit cost)** 如佣金税费；**隐性成本 (implicit cost)** 如**买卖价差 (bid-ask spread)** 与**价格影响 (price impact)**
- **杠杆与风险 (leverage and risk)**：**保证金买入 (margin purchase)** 与**卖空 (short sale)** 放大收益的同时增加**清算风险 (liquidation risk)**

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| 杠杆比率 (Leverage Ratio) | `Value of Position / Investor Equity` |
| 初始保证金率 (Initial Margin) | `Investor Equity / Purchase Value` |
| 保证金追缴价格 (Margin Call Price, Long) | `Loan / [Shares x (1 - Maintenance Margin)]` |
| 卖空收益率 (Short Sale Return) | `(Initial Proceeds - Repurchase Cost - Costs) / Initial Equity` |

##### 3. 常见考点与解题思路

- **区分市场类型**：先判断是一级还是二级市场交易 — IPO 属于一级，二级市场买卖已发行股票
- **保证金计算**：分清 equity 与 loan，用公式 `Margin Call Price = Loan / [Shares × (1 - MM%)]`，注意 maintenance margin 是下限
- **卖空题**：三步走 — 初始保证金存入、卖空所得款项、回购结算

##### 4. 易错点提醒

- **限价单并非更"安全"**：它只控制价格，不保证成交（未成交风险）
- **best price instruction ≠ best execution outcome**：最佳价格指令追求最优报价，但最佳执行结果还考虑速度、隐蔽性等
- **卖空亏损无上限**：股价理论上可以无限上涨，因此卖空风险远大于多头头寸

##### 5. 跨模块关联

- **市场结构影响指数构建** → [[M02-Security-Market-Indexes]]
- **交易成本与流动性影响市场效率** → [[M03-Market-Efficiency]]
- **margin 交易影响资本结构** → [[M05-Company-Analysis-Past-and-Present]]
### 🌳 核心知识树

```text
🏆 M01: Market Organization and Structure（市场组织与结构）
│
├── ⭐ 金融体系功能 (Financial System Functions)
│   ├── 储蓄-投资匹配 (Saving-Investment Matching)
│   ├── 资本形成 (Capital Formation)
│   ├── 风险配置 (Risk Allocation)
│   └── 信号功能 (Information Signaling)
│
├── ⭐ 资产与合约类型 (Assets & Contracts) 🎯高频
│   ├── 证券 (Securities): 股票、债券、优先股
│   ├── 货币与商品 (Currencies & Commodities)
│   ├── 合约 (Contracts): 远期、期货、互换、期权
│   └── 实物资产 (Real Assets): 房地产、基础设施
│
├── ⭐ 金融中介 (Financial Intermediaries)
│   ├── 经纪商 (Broker)
│   ├── 做市商 (Dealer)
│   ├── 交易所 (Exchange)
│   ├── 投资银行 (Investment Bank)
│   ├── 托管银行 (Custodian)
│   └── 清算所 (Clearinghouse)
│
├── ⭐ 市场结构 (Market Structures) 🎯高频
│   ├── 报价驱动 (Quote-Driven): 做市商报价
│   ├── 订单驱动 (Order-Driven): 订单簿撮合
│   └── 经纪人市场 (Brokered): 大额交易
│
├── ⭐ 头寸与杠杆 (Positions & Leverage) 🎯高频
│   ├── 多头 (Long): 预期上涨
│   ├── 空头 (Short): 预期下跌 ⚠️ 亏损无上限
│   ├── 📐 保证金交易 (Margin): Leverage = Position/Equity
│   └── 📐 追缴价格: P* = Loan / [Shares × (1-MM%)]
│
├── ⭐ 订单类型 (Order Types) 🎯高频
│   ├── 市价单 (Market Order): 立即执行 ⚠️ 价格不确定
│   ├── 限价单 (Limit Order): 价格确定 ⚠️ 可能不成交
│   ├── 止损单 (Stop Order): 触发后变市价单
│   └── 有效期指令 (Validity): DAY/GTD/GTC/IOC/FOK
│
├── ⭐ 一级与二级市场 (Primary & Secondary) 🎯高频
│   ├── IPO/SEO: 公司筹集新资本
│   └── 二级交易: 投资者之间交易
│
└── ⭐ 监管与系统稳定 (Regulation)
    ├── 投资者保护
    ├── 市场公平
    └── 系统风险防范
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| 杠杆比率 = Position Value / Equity | 总头寸 / 自有资金 | 衡量保证金交易的杠杆程度 | 比率越高风险越大 |
| 初始保证金率 = Equity / Purchase Value | 自有资金占比 | 确定最低首付要求 | 通常50% |
| Margin Call Price (Long) = Loan / [Shares × (1-MM%)] | 追缴保证金价格 | 计算股价跌到多少会触发追缴 | MM%是维持保证金率 |
| 卖空收益率 = (初始收入 - 回购成本 - 费用) / 初始权益 | 卖空回报率 | 计算卖空交易的净收益 | 股息和借贷费需计入成本 |
| Return on Margin Trade = (Ending Value - Loan - Initial Equity) / Initial Equity | 保证金交易收益率 | 考虑杠杆后的实际回报 | 亏损也会被放大 |

### 🛠️ 常见考点与解题思路

**Topic 1: 保证金交易计算**
- 步骤1：确定 Purchase Price、Shares、Initial Margin%
- 步骤2：计算 Equity = Purchase Value × Initial Margin%
- 步骤3：计算 Loan = Purchase Value - Equity
- 步骤4：Margin Call Price = Loan / [Shares × (1-MM%)]
- 注意：股价低于此价格时，broker会要求追加资金

**Topic 2: 卖空交易计算**
- 步骤1：卖空收入 = Shares × Short Price
- 步骤2：初始保证金存入 = 卖空收入 × Initial Margin%
- 步骤3：总抵押 = 卖空收入 + 初始保证金
- 步骤4：若股价上涨，抵押品需维持 MM% 比例
- 追缴价格 = 总抵押 / [Shares × (1+MM%)]

**Topic 3: 订单类型辨析**
- Market Order: 重执行速度 > 轻价格
- Limit Order: 轻执行 > 重价格控制
- Stop Order: 用作止损或突破入场
- GTC vs DAY: 有效期限的区别

**Topic 4: 市场类型判断**
- 报价驱动：做市商提供双边报价，适合流动性较低的证券
- 订单驱动：自动撮合，适合高流动性市场
- 经纪人市场：定制化大额交易

**Topic 5: 一级 vs 二级市场**
- 一级市场 = 新资本形成（公司收到资金）
- 二级市场 = 所有权转移（资金在投资者间流动）

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| 限价单比市价单更安全 | 限价单控制价格但不保证成交 | 有未成交风险（non-execution risk） |
| 卖空最大亏损 = 100% | 卖空亏损理论上无上限 | 股价可无限上涨 |
| Best price instruction=最佳执行 | 最佳价格≠最佳执行结果 | 执行质量还考虑速度和隐蔽性 |
| 一级市场和二级市场都是公司融资 | 只有一级市场是公司融资 | 二级市场是投资者之间交易 |
| 做市商=经纪商 | 做市商用自有资金交易，经纪商代理客户 | 角色和风险完全不同 |
| 高流动性=永远低交易成本 | 市场恐慌时流动性会枯竭 | 流动性是动态变化的 |
| FOK和IOC相同 | FOK = Fill-or-Kill（全部或取消），IOC = Immediate-or-Cancel（立即成交剩余取消） | FOK要求全部成交，IOC可部分成交 |

### 🔄 跨模块关联

- **市场结构影响指数构建方法** → [[M02-Security-Market-Indexes]]（加权方法选择依赖市场结构）
- **交易成本与流动性影响市场效率** → [[M03-Market-Efficiency]]（摩擦越少，市场越有效）
- **保证金交易影响资本结构分析** → [[M05-Company-Analysis-Past-and-Present]]（杠杆的微观基础）
- **一级市场与权益发行** → [[M04-Overview-of-Equity-Securities]]（IPO/SEO的具体安排）
- **市场微观结构与订单流** → [[M06-Industry-and-Competitive-Analysis]]（行业集中度与定价）
- **清算与结算风险** → [[M07-Company-Analysis-Forecasting]]（信用风险预测）

### 📋 复习与刷题提示

- **Margin Call计算是必考题**：掌握Price*=Loan/[Shares×(1-MM%)]的推导，注意做多和做空的不同公式
- **卖空题必做**：三步走 — 初始保证金存入 → 卖空所得款项 → 回购结算
- **订单类型概念题**：市价单vs限价单vs止损单的区别几乎每年都考
- **市场结构对比**：报价驱动vs订单驱动vs经纪人市场的特征和适用场景
- **一级vs二级市场**：理解新资本形成与所有权转移的本质区别
- **刷题重点**：margin计算、订单类型辨析、市场中介角色区分
- **FRM考点延伸**：清算风险、对手方风险、流动性风险的概念交叉

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
