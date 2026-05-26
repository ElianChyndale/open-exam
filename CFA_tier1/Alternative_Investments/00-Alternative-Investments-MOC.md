---
title: "00-Alternative Investments-MOC"
description: "CFA Level I 2026 Alternative Investments 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Alternative Investments"
topic_area: "Alternative_Investments"
level: CFA Level I
exam_year: 2026
exam_weight: "7-10%"
module_count: 7
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Alternative_Investments
---

# Alternative Investments MOC

> **一句话核心**：识别另类投资结构、绩效、私募、实物资产、对冲基金与数字资产特征。

---

## 1. 科目定位

- **考试权重**：7-10%
- **官方模块数**：7
- **主线框架**：识别资产结构 -> 判断流动性/估值/费用 -> 解释收益来源 -> 比较风险约束
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |
|---|---|---|---|---|
| M01 | Alternative Investment Features, Methods, and Structures | 概念+应用 | Introduction / Alternative Investment Features | [[M01-Alternative-Investment-Features-Methods-and-Structures]] |
| M02 | Alternative Investment Performance and Returns | 计算+解释 | Introduction / Alternative Investment Performance | [[M02-Alternative-Investment-Performance-and-Returns]] |
| M03 | Investments in Private Capital: Equity and Debt | 概念+应用 | Introduction / Private Equity Investment Characteristics | [[M03-Investments-in-Private-Capital-Equity-and-Debt]] |
| M04 | Real Estate and Infrastructure | 概念+应用 | Introduction / Real Estate Features | [[M04-Real-Estate-and-Infrastructure]] |
| M05 | Natural Resources | 计算+解释 | Introduction / Natural Resources Investment Features | [[M05-Natural-Resources]] |
| M06 | Hedge Funds | 计算+解释 | Introduction / Hedge Fund Investment Features | [[M06-Hedge-Funds]] |
| M07 | Introduction to Digital Assets | 计算+解释 | Introduction / Distributed Ledger Technology | [[M07-Introduction-to-Digital-Assets]] |

## 3. 核心知识树

```text
Alternative Investments (7-10%)
├─ 1. Alternative Investment Features, Methods, and Structures
│  ├─ 1.1 另类投资特征：illiquidity、低透明度、高费用、复杂估值、监管限制、独特风险；考试先判断它们如何影响 required return 与 suitability。
│  ├─ 1.2 投资方法：direct investment 控制强但集中/运营负担高；co-investment 降低 fee drag 但依赖 GP sourcing；fund investment 分散但有双层费用和流动性约束。
│  └─ 1.3 结构与费用：LP/GP、closed-end/open-end、management fee、incentive fee/carried interest、hurdle、high-water mark；先识别 fee base 再算 net return。
├─ 2. Alternative Investment Performance and Returns
│  ├─ 2.1 业绩倍数：TVPI = DPI + RVPI；PIC = paid-in / committed；IRR 受现金流时点影响，倍数不反映时间价值。
│  ├─ 2.2 Fee impact：gross return 先扣 management fee，再按 hurdle/HWM 判断 incentive fee；FOF 可能有底层和母基金双重费用。
│  ├─ 2.3 J-curve：早期 fee/成本使回报为负，退出后 DPI 上升；VC 通常更深更长，LBO 相对较浅。
│  └─ 2.4 Smoothed returns：appraisal-based NAV 低估 volatility/correlation，可能高估 Sharpe/Sortino。
├─ 3. Investments in Private Capital: Equity and Debt
│  ├─ 3.1 Private equity：VC/growth/LBO/distressed；价值来源是 growth、operational improvement、multiple expansion、leverage。
│  ├─ 3.2 Private debt：direct lending、mezzanine、distressed debt；收益来自 contractual yield + credit spread + covenants/structure。
│  └─ 3.3 Diversification：低公开市场相关性常被 appraisal smoothing 夸大，考试要同时提 liquidity lockup 与 valuation lag。
├─ 4. Real Estate and Infrastructure
│  ├─ 4.1 Real estate：NOI、cap rate、income/cost/sales comparison；Value = NOI / cap rate，cap rate 上升则价值下降。
│  ├─ 4.2 REITs：equity REIT 收租金，mortgage REIT 收利息；公开 REIT 流动性高但市场相关性更高。
│  └─ 4.3 Infrastructure：brownfield 现金流稳定/风险低，greenfield 建设风险高/预期回报高；常与 inflation-linked cash flow、PPP、regulatory risk 绑定。
├─ 5. Natural Resources
│  ├─ 5.1 Raw land/timberland/farmland：收益来自价格增值、产出现金流和通胀保护；风险含天气、政策、经营和流动性。
│  ├─ 5.2 Commodities：spot、futures、commodity-linked equities；不能把实物商品收益和期货总收益混同。
│  └─ 5.3 Futures return：total return = spot return + roll yield + collateral yield；contango 对多头 roll yield 通常为负。
├─ 6. Hedge Funds
│  ├─ 6.1 Features：flexible mandate、leverage、shorting、derivatives、lockup/notice/redemption gates；名称含 hedge 不代表市场中性。
│  ├─ 6.2 Strategies：equity long/short、global macro、event driven、relative value；按题干收益来源和风险因子分类。
│  └─ 6.3 Exposure：gross exposure = long + |short|；net exposure = long - |short|；gross 看规模，net 看方向。
├─ 7. Introduction to Digital Assets
│  ├─ 7.1 DLT/blockchain：shared ledger、consensus、immutability、smart contracts；区块链是技术，比特币是应用。
│  ├─ 7.2 Digital asset forms：cryptocurrency、utility token、security token、stablecoin、tokenized assets；按 claim/right/function 判断。
│  └─ 7.3 Risk/return：high volatility、custody/private key、cybersecurity、regulation、liquidity fragmentation；tokenization 提高可分割性但不消除底层资产风险。
```

## 4. 跨模块依赖关系

```text
M01 结构/费用/流动性
├─ feeds M02：费用结构决定 gross-to-net return；流动性和估值频率解释 smoothed returns。
├─ feeds M03-M07：direct/co-invest/fund 是所有另类资产的进入方式。
└─ interfaces PM：另类投资加入组合时先判断 liquidity、correlation、risk budget、rebalancing constraint。

M02 绩效与回报
├─ feeds M03：TVPI/DPI/RVPI、PIC、IRR、J-curve 是 private capital 的主要报告语言。
├─ feeds M04：appraisal smoothing 常出现在 direct real estate 与 infrastructure NAV。
├─ feeds M06：Sharpe/Sortino、net return、fee drag 用于 hedge fund 评价。
└─ interfaces FSA/PM：NAV、valuation lag、fee accrual 影响业绩展示和风险统计。

M03 Private Capital
├─ depends on M01：LP/GP、closed-end fund、capital commitment、carried interest。
├─ depends on M02：J-curve 与 PE multiples。
├─ interfaces FSA/FI：LBO leverage、covenants、credit spread、cash flow coverage。
└─ interfaces Ethics：valuation marks、performance presentation、conflict disclosure。

M04 Real Estate and Infrastructure
├─ depends on M01：illiquidity、direct vs fund ownership、unique operational/regulatory risk。
├─ depends on M02：appraisal-based returns 与 smoothing。
├─ interfaces FSA/Equity：NOI、cap rate、REIT income model、depreciation vs operating cash flow。
└─ interfaces FI/PM：long-duration cash flows、inflation linkage、interest-rate sensitivity。

M05 Natural Resources
├─ depends on M01：direct ownership vs commodity funds/futures exposure。
├─ interfaces Derivatives：futures pricing、cost of carry、roll yield、collateral yield。
├─ interfaces Economics：inflation、supply shocks、business cycle、currency exposure。
└─ interfaces PM：diversification may come from inflation beta, but futures roll can dominate spot intuition。

M06 Hedge Funds
├─ depends on M01：fee terms、lockups、redemption gates、manager discretion。
├─ depends on M02：net return after management/incentive fees and risk-adjusted measures。
├─ interfaces Derivatives/FI/Equity：shorting、leverage、event risk、relative value spreads。
└─ interfaces PM：gross/net exposure, beta control, tail risk and liquidity risk。

M07 Digital Assets
├─ depends on M01：new asset form with custody, regulatory and market-structure risks。
├─ interfaces Derivatives：futures/ETP exposure, leverage and collateral mechanics。
├─ interfaces Ethics：client suitability, disclosure of custody/cyber/regulatory risks。
└─ interfaces PM：high volatility, unstable correlations and liquidity fragmentation affect allocation sizing。
```

## 5. 核心对比专题

| 重要性 | 对比项 | 英文 | 中文解释 | 考试判断 |
|---|---|---|---|---|
| ⭐⭐⭐ | 概念 vs 应用 | definition vs application | 先确认官方定义，再放入题干情境判断。 | 概念题也要能说出适用条件和例外。 |
| ⭐⭐⭐ | 计算 vs 解释 | calculation vs interpretation | 数值只是中间结果，答案要解释方向、含义和限制。 | 凡是 calculate and interpret 都不能只算。 |
| ⭐⭐ | 静态知识 vs 决策流程 | static knowledge vs decision process | 把每个模块压缩成输入 -> 工具 -> 输出 -> 陷阱。 | 流程化比孤立背诵更抗干扰。 |
| ⭐⭐⭐ | 英文识题 vs 中文理解 | English trigger vs Chinese explanation | 英文用于识别题干，中文用于确认真正含义。 | 避免看到熟词就按直觉作答。 |
| ⭐⭐ | 本模块 vs 跨模块 | single module vs cross-module use | 同一公式/概念可能在估值、风险、伦理或报表中换场景出现。 | 错题要回填到 MOC 节点。 |

## 6. 公式与框架速查

### 业绩衡量

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| TVPI | `(累计分配 + 剩余价值) / 实缴资本 = DPI + RVPI` | `2.1` | 总价值倍数 = 已分配 + 剩余价值 |
| DPI | `累计分配 / 实缴资本` | `2.1` | 现金回报倍数 |
| RVPI | `剩余价值 / 实缴资本` | `2.1` | 未实现回报倍数 |
| PIC Multiple | `Paid-in Capital / Committed Capital` | `2.1` | 【考纲重点】资本调用进度 |
| IRR | `0 = Σ_{t=0}^{N} CF_t/(1+IRR)^t` | `2.1` | 内部收益率 |
| Management Fee | `Fee base x management fee rate` | `1.3` | AUM/committed capital/paid-in capital 读题 |
| Incentive Fee / Carried Interest | `Eligible profit x incentive fee rate` | `1.3` | hurdle rate / high-water mark 先判断 |
| Net Return | `Gross return - fees and expenses` | `1.3/2.1` | 费用结构会改变投资者回报 |
| Sortino | `(R_p - R_f)/σ_d` | `2.1` | 下行风险调整收益 |
| Sharpe | `(R_p - R_f)/σ_p` | `2.1` | 总风险调整收益 |
| Fee drag | `Gross return - net return` | `1.3/2.2` | 分解管理费、激励费和双层费用影响 |

### 房地产

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Cap Rate | `NOI / Property Value` | `4.1` | 资本化率 |
| Property Value | `NOI / Cap Rate` | `4.1` | 房地产估值 |
| NOI | `租金收入 - 运营费用` | `4.1` | 净营运收入（不含折旧利息） |
| Cap Rate, Growth Form | `Cap rate = r - g` | `4.1` | 【考纲重点】稳定增长房地产估值直觉 |
| Property Value, Growth Form | `NOI_1 / (r - g)` | `4.1` | 与 Gordon growth 结构相同 |
| REIT income logic | `Rental income -> NOI -> funds available for distribution` | `4.2` | Level I 以逻辑为主，别把 depreciation/interest 塞进 NOI |

### 商品期货

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| 期货定价 | `F_0(T) = S_0e^((r + s - y)T)` | `5.1` | r=利率, s=存储, y=便利收益 |
| Roll Yield | `(Near Future - Far Future) / Near Future` | `5.1` | 展期收益 |
| 持有成本 | `ln[F_0(T)/S_0]/T = r + s - y` | `5.1` | 连续复利口径下的 cost of carry |
| Collateral Yield | `Return on collateral posted for futures exposure` | `5.1` | 商品期货总回报来源之一 |
| Commodity Futures Total Return | `Spot return + roll yield + collateral yield` | `5.1` | 【考纲重点】方向判断常考 |
| Contango / Backwardation gate | `Far > near -> contango -> long roll usually negative; near > far -> backwardation -> long roll usually positive` | `5.3` | 先看期限结构再判断 roll |

### 对冲基金

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Gross Leverage | `(Long + \|Short\|) / Capital` | `6.3` | 总杠杆 |
| Net Leverage | `(Long - \|Short\|) / Capital` | `6.3` | 净杠杆 |
| Long/Short Net Exposure | `Long exposure - Short exposure` | `6.3` | 市场方向性敞口 |
| Long/Short Gross Exposure | `Long exposure + Short exposure` | `6.3` | 总风险规模 |
| Market neutral check | `Net exposure ≈ 0, gross exposure can still be high` | `6.3` | 市场中性不等于低杠杆 |

### 数字资产与通用判断框架

| 框架 | 判断链 | 知识树节点 | 考试说明 |
|------|--------|------------|----------|
| Token classification | `claim/right/function -> cryptocurrency / utility token / security token / tokenized asset` | `7.2` | 按权利和用途分类，不按名称分类 |
| DLT application | `shared ledger + consensus + smart contract -> settlement/custody/tokenization use case` | `7.1/7.3` | 区块链是基础设施，不等于所有数字资产 |
| Suitability risk screen | `volatility + liquidity + custody + regulation + client constraints` | `7.3` | 与 Ethics/PM 联动，先看客户是否承受得住 |

### 考纲范围标记

| 标记 | 内容 |
|------|------|
| 【考纲重点】 | Fee structures, private capital return multiples, real estate cap-rate valuation, commodity futures carry/roll yield, hedge fund leverage |
| 【考纲内但无核心公式】 | Fund structures, private capital strategy types, infrastructure brownfield/greenfield, digital assets and tokenization 多为概念辨析 |
| 【超纲/扩展】 | PME 复杂版本、完整 LBO 建模、Black-Scholes/Greeks、DeFi 协议收益模型不作为 Level I 必背公式 |

---

## 7. 高频考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 高频场景 |
|---|---|---|
| ❌ 陷阱 | ✅ 错误理解 | 正确理解 |
| ❌ ❌ 另类投资都是高流动性 | ✅ 认为可以轻松买卖 | ✅ 大多数另类投资是非流动性的（ILL特征） |
| ❌ ❌ TVPI = DPI × RVPI | ✅ 乘法关系 | ✅ TVPI = DPI + RVPI（加法关系） |
| ❌ ❌ J曲线意味着总是负收益 | ✅ 全程亏损 | ✅ J曲线是先负后正，最终转正 |
| ❌ ❌ LBO 总是用50%债务 | ✅ 固定比例 | ✅ LBO 通常是 60-80% 债务 + 20-40% 股权 |
| ❌ ❌ Cap Rate上升价值上升 | ✅ 正向关系 | ✅ Cap Rate与价值是反向关系（Cap Rate↑→Value↓） |
| ❌ ❌ 棕地回报总是更高 | ✅ 现有资产回报高 | ✅ 棕地风险低、回报低（8-10%），绿地风险高、回报高（12-15%） |
| ❌ ❌ Contango = 正Roll Yield | ✅ 正向市场收益为正 | ✅ Contango（期货>现货）= 负 Roll Yield |
| ❌ ❌ Backwardation = 负Roll Yield | ✅ 反向市场收益为负 | ✅ Backwardation（期货<现货）= 正 Roll Yield |
| ❌ ❌ 对冲基金总是对冲市场风险 | ✅ 名称误导 | ✅ 很多对冲基金是净多头，并非完全对冲 |

## 8. 通用分析框架

### 框架1: 另类投资题目总决策树

```text
1. 先识别资产类型
   ├─ Private capital -> 用 capital commitment、J-curve、TVPI/DPI/RVPI、IRR
   ├─ Real estate/infrastructure -> 用 NOI/cap rate、brownfield/greenfield、regulatory/inflation risk
   ├─ Natural resources/commodities -> 用 spot/roll/collateral、cost of carry、term structure
   ├─ Hedge funds -> 用 strategy type、gross/net exposure、fee/HWM/liquidity terms
   └─ Digital assets -> 用 DLT/token type/custody/regulatory/suitability screen
2. 再判断投资方式
   ├─ Direct -> control high, concentration and operational burden high, liquidity low
   ├─ Co-investment -> fee lower, selection/access depends on GP, concentration higher
   └─ Fund/FOF -> diversification and access higher, fee drag and transparency constraints higher
3. 再选公式或框架
   ├─ 题干给 paid-in/distribution/residual/commitment -> TVPI/DPI/RVPI/PIC
   ├─ 题干给 gross return、fee base、hurdle/HWM -> gross-to-net fee waterfall
   ├─ 题干给 NOI 与 cap rate -> Value = NOI / cap rate
   ├─ 题干给 spot/futures/storage/convenience yield -> cost of carry / roll yield
   └─ 题干给 long/short/capital -> gross and net exposure
4. 最后输出考试判断
   ├─ 说明方向：cap rate↑ value↓；contango long roll yield negative；gross≠net
   └─ 补限制：估值滞后、流动性、费用、监管、集中度会改变表面结论
```

### 框架2: 另类投资费用计算

```
另类投资费用计算
├── 1. 识别费用结构 (English)
│   ├── 管理费: X% × AUM（通常 1-2%）
│   ├── 业绩提成: Y% × 超额收益（通常 20%）
│   └── 是否有 Hurdle Rate / High Water Mark?
├── 2. 计算管理费 (English)
│   └── Management Fee = AUM × 管理费率
├── 3. 计算业绩提成（如有） (English)
│   ├── 步骤1: 计算当期收益 = 期末NAV - 期初NAV
│   ├── 步骤2: 判断是否超过 Hurdle Rate（如有）
│   ├── 步骤3: 判断是否超过 High Water Mark（如有）
│   └── 步骤4: Incentive Fee = 超额收益 × 提成比例
├── 4. 总费用 = 管理费 + 业绩提成 (English)
│   └── 注意: FOF有双重费用（底层基金费用 + FOF费用）
└── 5. 计算净回报 (English)
    └── Net Return = Gross Return - 总费用率
```

### 框架3: 房地产估值分析

```
房地产估值分析
├── 1. 获取 NOI (Net Operating Income)
│   └── NOI = 租金收入 - 运营费用（不含折旧和利息）
├── 2. 确定 Cap Rate
│   ├── 可比交易法: 参照类似物业的交易 Cap Rate
│   └── 市场数据法: 市场平均 Cap Rate
├── 3. 计算估值 (English)
│   └── 物业价值 (Property Value) = NOI / 资本化率 (Cap Rate)
└── 4. 敏感性分析 (English)
    ├── Cap Rate ↑ → Value ↓（反向关系）
    └── NOI ↑ → Value ↑（正向关系）
```

---

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

- 本 MOC 已优先吸收 `_legacy/2026-05-26-official-sync/` 中的中文解释、公式、陷阱和框架。
- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。
