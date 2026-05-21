---
title: 00-Alternative-Investments-MOC
description: CFA Level I Alternative Investments master MOC with module map, detailed knowledge tree, comparisons, formulas, and exam traps.
subject: Alternative Investments
topic_area: Alternative_Investments
level: CFA Level I
exam_weight: 6-9%
exam_format: 单选题
difficulty: 概念密集，结构、费用与业绩衡量交织
note_type: master_moc
status: 学习中
aliases:
  - Alternative Investments 知识框架
  - 另类投资 MOC
cssclasses:
  - cfa-moc
tags:
  - CFA_L1
  - MOC
  - Alternative_Investments
  - formulas
---

# 00-Alternative-Investments-MOC

## 笔记属性

| 属性 | 内容 |
|------|------|
| title | Alternative Investments - Map of Content |
| description | CFA L1 另类投资科目学习导航：私募股权、房地产、基础设施、商品、对冲基金、数字资产知识树与核心对比专题 |
| subject | Alternative Investments |
| 权重 | 6-9% |
| 状态 | 学习中 |
| 创建日期 | 2026/05/11 |
| 最后更新 | 2026/05/12 |
| tags | CFA L1, Alternative Investments, MOC |

---

## 最关键：非流动换低相关，复杂结构要高费

Alternative Investments 的核心是理解**非流动性溢价**与**低相关性**带来的分散化价值。掌握各类另类资产的特征、结构与费用，精通业绩衡量指标与估值方法，熟悉J曲线、杠杆与风险特征。

- **学习顺序**：先建立另类投资基础概念（M1-M2）→ 掌握私募股权与私人债权（M3）→ 攻克房地产与基础设施（M4）→ 最后掌握商品、对冲基金与数字资产（M5-M7）

| 模块 | 内容 | 核心问题 |
|------|------|----------|
| M01-M02 | 基础框架 | "另类投资是什么？怎么衡量业绩？" |
| M03 | 私人资本 | "PE、LBO、VC、Private Debt 怎么运作？" |
| M04 | 实物资产 | "房地产 Cap Rate、基础设施棕绿地" |
| M05-M07 | 其他另类 | "商品期限结构、对冲基金策略、数字资产" |

---

## Alternative Investments - 学习导航

CFA一级Alternative Investments科目涵盖另类投资基础特征与结构、业绩衡量与收益、私人资本（股权与债权）、房地产与基础设施、自然资源、对冲基金以及数字资产，是概念密集且与实务结合紧密的科目。

### 科目概览

| 属性 | 内容 |
|------|------|
| 科目权重 | 6-9% |
| 考试形式 | 单选题（上午+下午各约6-9题） |
| 难度特点 | M1-M2 概念+计算（业绩指标），M3-M4 结构+估值，M5-M7 市场特征+策略 |
| 学习建议 | M1 费用结构（2/20）必须理解；M2 TVPI/DPI/RVPI 必须会算；M3 LBO结构、VC vs PE区分常考；M4 Cap Rate必须掌握；M5 Contango/Backwardation常考；M6对冲基金策略与杠杆；M7数字资产基础概念 |

---

## Alternative Investments 核心知识树

```
Alternative Investments (M01-M07)
│
├── M01: Alternative Investment Features, Methods, and Structures
│   ├── 1.1 另类投资的六大特征【考试核心】
│   │   ├── ILL (Illiquidity): 非流动性——买卖困难，周期长
│   │   │   ├── 各子类别流动性排序（从高到低）↔ PP_P20
│   │   │   ├── REITs: 高流动性 (publicly traded) ↔ PP_P20 正确答案
│   │   │   ├── Hedge Funds: 低流动性 (lockup + notice period)
│   │   │   ├── PE / VC: 极低流动性 (7-10年锁定)
│   │   │   └── Direct Real Estate: 最 illiquid (买卖困难)
│   │   ├── LOW (Low Correlation): 与传统资产低相关性——分散化价值
│   │   ├── HIGH (High Return Potential): 高收益潜力——风险补偿
│   │   ├── COMPLEX (Complex Structures): 复杂结构——多层实体、嵌套
│   │   ├── LIMIT (Limited Transparency): 透明度有限——信息披露少
│   │   └── UNIQUE (Unique Risks): 独特风险——非系统性、难以量化
│   │
│   ├── 1.2 投资方法【考试核心】
│   │   ├── Direct Investment (直接投资): 直接购买资产所有权
│   │   ├── Indirect Investment (间接投资): 通过基金、ETF投资
│   │   ├── Fund-of-Funds (FOF): 投资基金的基金 ↔ PP_P63
│   │   │   ├── 费用: **双重费用**（底层基金费 + FOF管理费，通常额外+1% + 10%激励）
│   │   │   ├── 赎回条款: **较好**（可协商 better terms）↔ PP_P63
│   │   │   ├── 分散化: **多样化**（投资多个对冲基金）↔ PP_P63
│   │   │   └── 门槛: **较低**（小投资者可通过 FOF 参与）↔ PP_P63
│   │   └── Single Hedge Fund vs FOF 对比 ↔ PP_P63
│   │       ├── 费用: Single **较低**（一层费用），FOF **较高**（双重费用）
│   │       ├── 流动性: Single **较差**，FOF **较好**（可协商条款）
│   │       ├── 分散化: Single **集中**，FOF **分散**
│   │       └── 尽调: Single **需自行尽调**，FOF **专业团队尽调**
│   │
│   ├── 1.3 费用结构【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `Management Fee = AUM × 管理费率`
│   │   │   ├── `Incentive Fee = 超额收益 × 提成比例`
│   │   │   └── `总费用 = 管理费 + 业绩提成`
│   │   ├── 管理费: X% × AUM（通常 1-2%）
│   │   ├── 业绩提成: Y% × 超额收益（通常 20%）
│   │   ├── 是否有 Hurdle Rate / High Water Mark?
│   │   │   ├── Hurdle Rate (门槛收益率): 通常为 6-8%，达到后才收取业绩提成
│   │   │   └── High Water Mark (高水位线): 只对新创造的收益收取提成，防止重复收费
│   │   ├── 计算步骤:
│   │   │   ├── 步骤1: 计算当期收益 = 期末NAV - 期初NAV
│   │   │   ├── 步骤2: 判断是否超过 Hurdle Rate（如有）
│   │   │   ├── 步骤3: 判断是否超过 High Water Mark（如有）
│   │   │   └── 步骤4: Incentive Fee = 超额收益 × 提成比例
│   │   └── 总费用 = 管理费 + 业绩提成
│   │       └── 注意: FOF有双重费用（底层基金费用 + FOF费用）
│   │
│   ├── 1.4 基金组织形式与治理结构【考试核心】↔ PP_P11
│   │   ├── 有限合伙制 (Limited Partnership)——另类投资最常用结构
│   │   │   ├── General Partner (GP)
│   │   │   │   ├── 角色: 基金日常管理和运营决策的唯一责任方
│   │   │   │   ├── 出资: 通常仅占 1-2%
│   │   │   │   ├── 责任: 承担无限责任（现实中通过 LLC 实体隔离）
│   │   │   │   └── 收益: 管理费 + Carried Interest（业绩分成，通常20%）
│   │   │   └── Limited Partner (LP)
│   │   │       ├── 角色: 被动投资者 (passive investors) ↔ 核心考点
│   │   │       ├── 出资: 绝大部分出资（98-99%）
│   │   │       ├── 责任: 以出资额为限 (limited liability)
│   │   │       ├── 不参与管理: not involved in management ↔ PP_P11
│   │   │       ├── 不参与运营: not involved in operations and decisions controlled solely by GP
│   │   │       ├── 不承担责任: not liable for debts and liabilities
│   │   │       └── 注意: "Limited"指责任有限，不是权力有限 ↔ PP_P11 陷阱
│   │   ├── LP的有限参与方式（不丧失有限责任保护）
│   │   │   ├── Advisory Committee (顾问委员会)
│   │   │   │   ├── 职能: 审议利益冲突、审批估值政策、审查关联交易
│   │   │   │   ├── 性质: 建议性 (advisory)，不具有投资决策权
│   │   │   │   └── 关键区分: 参与讨论 ≠ 拥有决策权 ↔ PP_P11
│   │   │   └── "No-fault Divorce" 条款
│   │   │       └── LP 可在特定条件下（如 GP 失职）罢免 GP
│   │   ├── LP过度参与的后果【考试陷阱】
│   │   │   ├── 若 LP 积极参与管理或运营决策
│   │   │   ├── 可能失去 limited liability（有限责任保护）
│   │   │   ├── 面临 unlimited liability（无限责任）
│   │   │   └── 这是法律上"刺破公司面纱" (Piercing the Corporate Veil) 的风险
│   │   └── GP 的 Fiduciary Duty（信托责任）
│   │       ├── Capital Calls 必须按比例公平分配投资机会
│   │       ├── Follow-on Investments 不得歧视某些 LP
│   │       └── Side Letters（特殊条款）需透明披露
│   │
│   ├── 1.5 收益瀑布分配结构 (Waterfall Distribution)【考试核心】↔ PP_P13
│   │   ├── American Waterfall (美式瀑布) = Deal-by-Deal
│   │   │   ├── 分配单位: 单个项目 (per-deal / deal-by-deal)
│   │   │   ├── GP 业绩报酬收取: 每个项目退出时即可收取
│   │   │   ├── 优势方: GP ↔ PP_P13
│   │   │   └── 风险: 可能前期多拿，后期需依赖Clawback
│   │   ├── European Waterfall (欧式瀑布) = Whole-of-Fund
│   │   │   ├── 分配单位: 整个基金 (whole fund / aggregate)
│   │   │   ├── LP 先收回全部出资 + 优先回报后，GP 才能收取业绩报酬
│   │   │   ├── 优势方: LP ↔ PP_P13
│   │   │   └── 特点: 更保守，保护LP利益
│   │   └── 回拨条款 (Clawback Provision)
│   │       ├── 若前期GP多拿了业绩报酬，后期需退还
│   │       └── 保护 LP 利益，确保整体收益分配公平
│   │
│   └── 1.6 数字资产基础结构【考试核心】
│       ├── 层级关系: Tokenization 的底层技术
│       ├── ICO (首次代币发行) ↔ PP_P70
│       │   ├── 本质: **融资方式** (Fundraising) **
│       │   ├── 定义: 公司出售加密代币筹集资金
│       │   └── 记忆口诀: "区块链是技术账本了，代币化是过程印本子，ICO是融资卖本子"
│       ├── 区块链 (Blockchain): 分布式账本技术 (DLT)
│       │   ├── 去中心化、不可篡改、透明可追溯
│       │   └── 注意: 区块链 ≠ 比特币，比特币只是区块链的应用之一
│       └── Tokenization (代币化)
│           ├── 定义: 将资产权利转化为区块链上的数字代币
│           ├── 优势: 提高流动性、降低交易成本、实现 fractional ownership
│           └── 与ICO区别: Tokenization是过程/技术，ICO是融资事件
│
├── M02: Alternative Investment Performance and Returns
│   ├── 2.1 业绩衡量指标【考试核心】
│   │   ├── 核心公式
│   │   │   ├── `TVPI = DPI + RVPI`
│   │   │   ├── `DPI = 累计分配 / 实缴资本`
│   │   │   ├── `RVPI = 剩余价值 / 实缴资本`
│   │   │   ├── `Sortino = (Rp - Rf) / σd`
│   │   │   └── `Sharpe = (Rp - Rf) / σp`
│   │   ├── TVPI (Total Value to Paid-In) = DPI + RVPI
│   │   │   └── 总价值倍数 = 已分配价值 + 剩余价值 / 实缴资本
│   │   ├── DPI (Distributed to Paid-In)
│   │   │   └── 现金回报倍数 = 累计分配 / 实缴资本
│   │   ├── RVPI (Residual Value to Paid-In)
│   │   │   └── 未实现回报倍数 = 剩余价值 / 实缴资本
│   │   ├── IRR (Internal Rate of Return)
│   │   │   └── NPV = 0 的折现率，考虑时间价值
│   │   ├── Sortino Ratio = (Rp - Rf) / σ_d
│   │   │   └── 下行风险调整收益（仅考虑下行波动）
│   │   └── Sharpe Ratio = (Rp - Rf) / σ_p
│   │       └── 总风险调整收益（考虑总波动）
│   ├── 2.2 J曲线【考试核心】
│   │   ├── 定义: PE基金生命周期中收益随时间变化的曲线形态
│   │   ├── 早期负收益原因:
│   │   │   ├── 管理费持续收取（按承诺资本AUM）
│   │   │   ├── 初期费用、交易成本、设立费用
│   │   │   └── 投资尚未成熟，未产生回报，未实现退出
│   │   ├── 后期转正原因:
│   │   │   ├── 投资标的成熟，价值增长
│   │   │   ├── 项目退出（IPO、并购、二级出售）
│   │   │   └── DPI上升，RVPI下降，TVPI趋于稳定
│   │   └── 不同策略的J曲线:
│   │       ├── VC: J曲线最深（早期投资，失败率高，回报周期长）
│   │       ├── LBO: 相对较浅（成熟公司，有现金流，杠杆放大回报）
│   │       └── Growth Equity: 介于两者之间
│   └── 2.3 收益平滑 (Smoothed Returns)【考试陷阱】
│       ├── 原因: 非流动性资产按评估估值 (Appraisal Value) 而非市价 (Market Value)
│       ├── 后果:
│       │   ├── 低估波动率 (Volatility)
│       │   ├── 低估与市场的相关性 (Correlation)
│       │   └── 导致风险调整后收益被高估（Sharpe/Sortino偏高）
│       └── Unsmoothing调整:
│           ├── 目的: 还原真实波动率
│           └── 方法: 对评估收益进行去平滑处理，更接近公开市场价格波动
│
├── M03: Private Capital (私人资本)
│   ├── 3.1 Private Equity (私募股权)【考试核心】
│   │   ├── LBO (Leveraged Buyout) 杠杆收购
│   │   │   ├── 资本结构: 60-80%债务 + 20-40%股权
│   │   │   ├── 回报来源:
│   │   │   │   ├── 价值创造: 运营改善、收入增长、成本削减
│   │   │   │   └── 杠杆放大: 用债务放大股权回报（放大效应）
│   │   │   ├── 退出方式:
│   │   │   │   ├── IPO (首次公开发行)
│   │   │   │   ├── Secondary Sale (二次出售给另一PE)
│   │   │   │   ├── Recapitalization (资本重组)
│   │   │   │   └── Write-off / Liquidation (核销/清算)
│   │   │   └── 注意: LBO 债务比例并非固定50%，而是根据目标公司现金流决定
│   │   ├── VC (Venture Capital) 风险投资
│   │   │   ├── 投资阶段:
│   │   │   │   ├── 种子期 (Seed): 最早阶段，概念验证
│   │   │   │   ├── 早期 (Early): 产品开发、市场初步验证
│   │   │   │   └── 成长期 (Expansion/Growth): 规模化扩张
│   │   │   ├── 与PE核心区别:
│   │   │   │   ├── 投资对象: 早期/成长期公司 vs 成熟公司
│   │   │   │   ├── 资本结构: 极少使用债务 vs 高杠杆
│   │   │   │   ├── 风险水平: 极高（失败率高）vs 中等
│   │   │   │   ├── 回报特征: 幂律分布（少数项目贡献大部分回报）vs 较稳定
│   │   │   │   └── 投资期限: 更长（7-10年+）vs 3-7年
│   │   │   └── 注意: VC投资早期公司，PE（LBO）投资成熟公司 ↔ 考试陷阱
│   │   └── Growth Equity (成长股权)
│   │       ├── 少数股权投资（不寻求控制权）
│   │       ├── 投资对象: 已盈利、需扩张资金的成熟公司
│   │       └── 风险/回报: 介于VC和LBO之间
│   │
│   ├── 3.2 Private Debt (私人债权)【考试核心】
│   │   ├── Direct Lending (直接借贷)
│   │   │   ├── 非银行金融机构向中小企业直接放贷
│   │   │   └── 特征: 有抵押、有契约保护、收益率高于公开市场债券
│   │   ├── Mezzanine Debt (夹层债务)
│   │   │   ├── 介于优先债务和股权之间的混合资本
│   │   │   ├── 特征: 可转换为股权的期权（Warrants/Equity Kicker）
│   │   │   └── 回报: 利息 + 股权上行收益，通常12-15%
│   │   ├── Venture Debt (创业债务)
│   │   │   ├── 向VC支持的公司提供债务融资
│   │   │   └── 特征: 通常无抵押，依赖VC背书，利率较高
│   │   └── 与PE费用结构差异:
│   │       ├── PE: 2%管理费 + 20%业绩提成（Carried Interest）
│   │       └── Private Debt: 通常只收管理费（1-1.5%），极少有业绩提成
│   │
│   └── 3.3 PE与Private Debt对比（见核心对比专题）
│
├── M04: Real Estate and Infrastructure (房地产与基础设施)
│   ├── 4.1 房地产【考试核心】
│   │   ├── 投资形式
│   │   │   ├── Direct Investment: 直接购买物业所有权
│   │   │   └── Indirect Investment:
│   │   │       ├── REITs (Real Estate Investment Trusts)
│   │   │       │   ├── Equity REITs: 拥有并经营物业，主要收入来自租金
│   │   │       │   ├── Mortgage REITs: 投资房地产抵押贷款/抵押支持证券
│   │   │       │   └── Hybrid REITs: 两者结合
│   │   │       └── 流动性: REITs > Direct Real Estate（公开交易 vs 非流动）
│   │   ├── 估值方法
│   │   │   ├── 核心公式
│   │   │   │   ├── `NOI = 租金收入 - 运营费用`
│   │   │   │   ├── `Cap Rate = NOI / Property Value`
│   │   │   │   └── `Property Value = NOI / Cap Rate`
│   │   │   ├── Income Approach (收益法)——最常用
│   │   │   │   ├── NOI (Net Operating Income) = 租金收入 - 运营费用（不含折旧和利息）
│   │   │   │   ├── Cap Rate (资本化率) = NOI / Property Value
│   │   │   │   └── Property Value = NOI / Cap Rate
│   │   │   ├── Cost Approach (成本法)
│   │   │   │   └── 土地价值 + 重置成本 - 折旧
│   │   │   └── Sales Comparison Approach (市场比较法)
│   │   │       └── 参照类似物业近期交易价格调整
│   │   ├── Cap Rate 驱动因素
│   │   │   ├── 利率环境: 利率↑ → Cap Rate↑ → Value↓
│   │   │   ├── 风险溢价: 风险↑ → Cap Rate↑ → Value↓
│   │   │   └── 增长预期: 增长↑ → Cap Rate↓ → Value↑
│   │   └── 房地产周期
│   │       ├── 复苏期、扩张期、过热期、衰退期
│   │       └── 与宏观经济、利率、就业密切相关
│   │
│   └── 4.2 基础设施【考试核心】
│       ├── 定义: 提供公共服务的长期实物资产（公路、港口、电网、通信塔等）
│       ├── 投资形式:
│       │   ├── Direct Ownership
│       │   ├── Listed Infrastructure Funds (上市基础设施基金)
│       │   └── Unlisted Funds / PPP (公私合营)
│       ├── 棕地 (Brownfield) vs 绿地 (Greenfield)
│       │   ├── Brownfield: 现有运营资产，有稳定现金流
│       │   │   ├── 风险: 低（运营成熟）
│       │   │   ├── 回报: 8-10%（稳定、防御性）
│   │   │   └── 特征: 购买既有资产，改造/运营优化
│   │   ├── Greenfield: 新建项目，从无到有
│   │   │   ├── 风险: 高（建设风险、监管风险、需求风险）
│   │   │   ├── 回报: 12-15%（高风险高回报）
│   │   │   └── 特征: 开发新建，周期长，资本投入大
│   │   └── 注意: 棕地风险低回报低，绿地风险高回报高 ↔ 考试陷阱
│       └── 与LBO关系: 基础设施收购常用杠杆（稳定现金流适合举债）
│
├── M05: Natural Resources (自然资源)
│   └── 5.1 商品期货【考试核心】
│       ├── 期货定价理论
│       │   ├── 核心公式
│       │   │   ├── `Futures Price = Spot × e^((r + s - y) × T)`
│       │   │   ├── `Roll Yield = (Near Future - Far Future) / Near Future`
│       │   │   └── `持有成本 ≈ r + s - y`
│       │   ├── Futures Price = Spot × e^((r + s - y) × T)
│       │   │   ├── r = 无风险利率
│       │   │   ├── s = 存储成本 (Storage Cost)
│       │   │   └── y = 便利收益 (Convenience Yield)
│       │   └── 持有成本理论 (Cost of Carry)
│       ├── Contango (正向市场) vs Backwardation (反向市场)
│       │   ├── Contango: Futures Price > Spot Price
│       │   │   ├── Roll Yield: 负 (不利)
│       │   │   ├── 驱动: 存储成本高 / 便利收益低
│       │   │   └── 投资者影响: 长期持期货有损耗（需不断展期亏损）
│       │   └── Backwardation: Futures Price < Spot Price
│       │       ├── Roll Yield: 正 (有利)
│       │       ├── 驱动: 便利收益高（现货稀缺）
│       │       └── 投资者影响: 长期持期货有收益（展期获利）
│       ├── Roll Yield 计算
│       │   ├── 公式: (Near Future - Far Future) / Near Future
│       │   └── 本质: 展期收益/成本，由期限结构决定
│       └── 商品期货投资策略
│           ├── 被动投资: 指数跟踪（考虑期限结构影响）
│           └── 主动投资: 期限结构套利、现货-期货套利
│
├── M06: Hedge Funds (对冲基金)
│   ├── 6.1 对冲基金特征
│   │   ├── 流动性: 相对PE/VC较高，但有 Lockup Period (锁定期，通常1-3年) + Notice Period (通知期，30-90天)
│   │   ├── 透明度: 相对其他另类投资较高（需定期披露持仓），但仍低于传统共同基金
│   │   ├── 费用结构: 通常 2/20（2%管理费 + 20%业绩提成），部分新基金降低至 1/10
│   │   └── 高水位线: 普遍采用，保护投资者
│   ├── 6.2 对冲基金策略【考试核心】
│   │   ├── Equity Long/Short (股票多空)
│   │   │   ├── 同时持有多头和空头头寸，降低市场风险敞口
│   │   │   ├── 风险: 中等，与股市相关性 0.5-0.7
│   │   │   └── 回报: 8-12%
│   │   ├── Global Macro (全球宏观)
│   │   │   ├── 基于宏观经济趋势，跨资产类别（外汇、利率、股指）
│   │   │   ├── 风险: 高，与股市相关性 0.2-0.4
│   │   │   └── 回报: 10-15%
│   │   ├── Event Driven (事件驱动)
│   │   │   ├── 利用公司特定事件（并购、重组、破产）
│   │   │   ├── 风险: 中高，与股市相关性 0.4-0.6
│   │   │   └── 回报: 10-14%
│   │   └── Relative Value (相对价值)
│   │       ├── 利用相关资产定价偏差，市场中性策略
│   │       ├── 风险: 低，与股市相关性 0.1-0.3
│   │       └── 回报: 6-10%
│   └── 6.3 杠杆与风险【考试核心】
│       ├── 核心公式
│       │   ├── `Gross Leverage = (Long + |Short|) / Capital`
│       │   └── `Net Leverage = (Long - |Short|) / Capital`
│       ├── Gross Leverage (总杠杆) = (Long + |Short|) / Capital
│       │   └── 反映基金总敞口，包括多空双边
│       ├── Net Leverage (净杠杆) = (Long - |Short|) / Capital
│       │   └── 反映市场风险敞口，市场中性策略Net Leverage接近0
│       └── 注意: Gross ≠ Net，完全不同 ↔ 考试陷阱
│           └── 很多对冲基金是净多头 (Net Long)，并非完全对冲市场风险
│
└── M07: Digital Assets (数字资产)
    ├── 7.1 区块链与共识机制【考试核心】
    │   ├── 区块链 (Blockchain)
    │   │   ├── 本质: 分布式账本技术 (DLT)
    │   │   ├── 特征: 去中心化、不可篡改、透明可追溯
    │   │   └── 注意: 区块链是底层技术，比特币是应用之一 ↔ 考试陷阱
    │   ├── PoW (Proof of Work) 工作量证明
    │   │   ├── 方式: 挖矿（算力竞争）
    │   │   ├── 能耗: 高
    │   │   ├── 安全性: 高（51%攻击成本高）
    │   │   └── 代表: Bitcoin
    │   └── PoS (Proof of Stake) 权益证明
    │       ├── 方式: 质押（持有量决定记账权）
    │       ├── 能耗: 低
    │       ├── 安全性: 中高
    │       └── 代表: Ethereum 2.0
    ├── 7.2 数字资产类型
    │   ├── Cryptocurrencies (加密货币): 支付型代币，如 Bitcoin, Litecoin
    │   ├── Utility Tokens (效用代币): 使用特定平台服务的权利
    │   └── Security Tokens (证券型代币): 代表传统资产所有权，受证券法规监管
    └── 7.3 Tokenization (代币化)【考试核心】
        ├── 定义: 将资产权利转化为区块链上的数字代币
        ├── 与ICO区别:
        │   ├── Tokenization: 资产数字化过程/技术
        │   └── ICO: 融资事件，公司出售代币筹集资金
        ├── 优势:
        │   ├── 提高流动性（ fractional ownership，降低投资门槛）
        │   ├── 降低交易成本（去中介化）
        │   ├── 24/7交易，跨境无障碍
        │   └── 提高透明度（链上可追溯）
        └── 风险:
            ├── 监管不确定性
            ├── 技术风险（智能合约漏洞）
            ├── 流动性风险（市场深度不足）
            └── 托管与安全风险（私钥管理）
```

---

## 核心对比专题

### 1. 另类投资六大特征速查

| 特征 | 英文 | 含义 | 考试重点 |
|------|------|------|----------|
| ILL | Illiquidity | 非流动性 | ⭐⭐⭐⭐⭐ |
| LOW | Low Correlation | 与传统资产低相关 | ⭐⭐⭐⭐⭐ |
| HIGH | High Return Potential | 高收益潜力 | ⭐⭐⭐⭐⭐ |
| COMPLEX | Complex Structures | 复杂结构 | ⭐⭐⭐⭐ |
| LIMIT | Limited Transparency | 透明度有限 | ⭐⭐⭐⭐ |
| UNIQUE | Unique Risks | 独特风险 | ⭐⭐⭐ |

### 2. Private Equity vs Private Debt

| 维度 | Private Equity | Private Debt |
|------|----------------|--------------|
| 本质 | 所有权(股权) | 债权 |
| 收益来源 | 价值创造 + 杠杆 | 利息 + 溢价 |
| 风险水平 | 高 | 中等 |
| 典型回报 | 15-25% IRR | 8-15% |
| 代表性策略 | VC, LBO, Growth | Direct Lending, Mezzanine |
| 费用结构 | 管理费+业绩提成(2/20) | 通常仅管理费(1-1.5%) |

### 3. Contango（正向市场） vs Backwardation（反向市场）

| 维度 | Contango | Backwardation |
|------|----------|---------------|
| 价格关系 | Futures > Spot | Futures < Spot |
| Roll Yield | 负 (不利) | 正 (有利) |
| 驱动因素 | 存储成本高 / 便利收益低 | 便利收益高 |
| 投资者影响 | 长期持期货有损耗 | 长期持期货有收益 |
| 市场状态 | 期货溢价，远期贴水预期 | 期货贴水，现货稀缺 |

### 4. Brownfield（棕地） vs Greenfield（绿地）

| 维度 | Brownfield (棕地) | Greenfield (绿地) |
|------|-------------------|-------------------|
| 定义 | 收购现有运营资产 | 新建开发项目 |
| 现金流 | 现有稳定现金流 | 建设期无现金流 |
| 风险水平 | 低 | 高 |
| 典型回报 | 8-10% | 12-15% |
| 投资阶段 | 运营优化、提升效率 | 规划、建设、运营 |
| 资本需求 | 收购对价 | 建设资本支出 |
| 适用投资者 | 追求稳定收益、低风险偏好 | 追求高增长、高风险承受能力 |

### 5. 对冲基金策略对比

| 策略 | 风险 | 回报 | 与股票相关性 |
|------|------|------|--------------|
| Equity L/S | 中等 | 8-12% | 0.5-0.7 |
| Global Macro | 高 | 10-15% | 0.2-0.4 |
| Event Driven | 中高 | 10-14% | 0.4-0.6 |
| Relative Value | 低 | 6-10% | 0.1-0.3 |

### 6. PoW vs PoS

| 维度 | PoW (工作量证明) | PoS (权益证明) |
|------|------------------|----------------|
| 方式 | 挖矿（算力竞争） | 质押（持有量） |
| 能耗 | 高 | 低 |
| 安全性 | 高 | 中高 |
| 代表 | Bitcoin | Ethereum 2.0 |
| 去中心化程度 | 高（算力分散） | 较高（财富集中风险） |
| 扩展性 | 较低（吞吐量受限） | 较高（可支持智能合约） |

---

## 跨模块关联

```
M01 基础特征
├── 六大特征 → M02-M07 各类资产的具体体现
├── 费用结构 → M03 (PE/VC), M06 (Hedge Funds)
└── 投资方法 → M03-M07 各类资产的参与方式

M02 业绩衡量
├── TVPI/DPI/RVPI → M03 (PE Fund 业绩报告)
├── J曲线 → M03 (PE Fund 生命周期)
└── 收益平滑 → M04 (房地产估值)

M03 私人资本
├── PE 杠杆 → M06 (Hedge Fund 杠杆对比)
└── Private Debt → M01 (费用结构差异)

M04 实物资产
├── 房地产周期 → M05 (商品周期对比)
└── 基础设施 → M03 (LBO基础设施收购)

M05-M07 其他另类
├── 商品期货 → Derivatives 科目联动
├── 对冲基金 → M01-M02 (费用+业绩)
└── 数字资产 → M01 (独特风险案例)
```

---

## 通用分析框架

### 框架1: 另类投资费用计算

```
另类投资费用计算
├── 1. 识别费用结构
│   ├── 管理费: X% × AUM（通常 1-2%）
│   ├── 业绩提成: Y% × 超额收益（通常 20%）
│   └── 是否有 Hurdle Rate / High Water Mark?
├── 2. 计算管理费
│   └── Management Fee = AUM × 管理费率
├── 3. 计算业绩提成（如有）
│   ├── 步骤1: 计算当期收益 = 期末NAV - 期初NAV
│   ├── 步骤2: 判断是否超过 Hurdle Rate（如有）
│   ├── 步骤3: 判断是否超过 High Water Mark（如有）
│   └── 步骤4: Incentive Fee = 超额收益 × 提成比例
├── 4. 总费用 = 管理费 + 业绩提成
│   └── 注意: FOF有双重费用（底层基金费用 + FOF费用）
└── 5. 计算净回报
    └── Net Return = Gross Return - 总费用率
```

### 框架2: 房地产估值分析

```
房地产估值分析
├── 1. 获取 NOI (Net Operating Income)
│   └── NOI = 租金收入 - 运营费用（不含折旧和利息）
├── 2. 确定 Cap Rate
│   ├── 可比交易法: 参照类似物业的交易 Cap Rate
│   └── 市场数据法: 市场平均 Cap Rate
├── 3. 计算估值
│   └── Property Value = NOI / Cap Rate
└── 4. 敏感性分析
    ├── Cap Rate ↑ → Value ↓（反向关系）
    └── NOI ↑ → Value ↑（正向关系）
```

---

## 核心公式速查

### 业绩衡量

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| TVPI | DPI + RVPI | `2.1` | 总价值倍数 = 已分配 + 剩余价值 |
| DPI | 累计分配 / 实缴资本 | `2.1` | 现金回报倍数 |
| RVPI | 剩余价值 / 实缴资本 | `2.1` | 未实现回报倍数 |
| IRR | NPV = 0 的折现率 | `2.1` | 内部收益率 |
| Sortino | (Rp - Rf) / σ_d | `2.1` | 下行风险调整收益 |
| Sharpe | (Rp - Rf) / σ_p | `2.1` | 总风险调整收益 |

### 房地产

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Cap Rate | NOI / Property Value | `4.1` | 资本化率 |
| Property Value | NOI / Cap Rate | `4.1` | 房地产估值 |
| NOI | 租金收入 - 运营费用 | `4.1` | 净营运收入（不含折旧利息） |

### 商品期货

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| 期货定价 | Spot × e^((r + s - y)×T) | `5.1` | r=利率, s=存储, y=便利收益 |
| Roll Yield | (Near Future - Far Future) / Near Future | `5.1` | 展期收益 |
| 持有成本 | Futures - Spot ≈ r + s - y | `5.1` | 成本 carry |

### 对冲基金

| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Gross Leverage | (Long + \|Short\|) / Capital | `6.3` | 总杠杆 |
| Net Leverage | (Long - \|Short\|) / Capital | `6.3` | 净杠杆 |

---

## 高频考试陷阱速查

| 陷阱 | 错误理解 | 正确理解 |
|------|----------|----------|
| ❌ 另类投资都是高流动性 | 认为可以轻松买卖 | ✅ 大多数另类投资是**非流动性的**（ILL特征） |
| ❌ TVPI = DPI × RVPI | 乘法关系 | ✅ TVPI = DPI + RVPI（**加法关系**） |
| ❌ J曲线意味着总是负收益 | 全程亏损 | ✅ J曲线是**先负后正**，最终转正 |
| ❌ LBO 总是用50%债务 | 固定比例 | ✅ LBO 通常是 **60-80% 债务** + 20-40% 股权 |
| ❌ Cap Rate上升价值上升 | 正向关系 | ✅ Cap Rate与价值是**反向关系**（Cap Rate↑→Value↓） |
| ❌ 棕地回报总是更高 | 现有资产回报高 | ✅ 棕地风险低、回报低（8-10%），绿地风险高、回报高（12-15%） |
| ❌ Contango = 正Roll Yield | 正向市场收益为正 | ✅ Contango（期货>现货）= **负** Roll Yield |
| ❌ Backwardation = 负Roll Yield | 反向市场收益为负 | ✅ Backwardation（期货<现货）= **正** Roll Yield |
| ❌ 对冲基金总是对冲市场风险 | 名称误导 | ✅ 很多对冲基金是**净多头**，并非完全对冲 |
| ❌ 总杠杆 = 净杠杆 | 概念混淆 | ✅ 完全不同: Gross=(L+\|S\|)/C, Net=(L-\|S\|)/C |
| ❌ 数字资产完全匿名 | 完全不可追溯 | ✅ 数字资产是**伪匿名**（Pseudonymous），交易可追溯 |
| ❌ 区块链 = 比特币 | 概念等同 | ✅ 区块链是**技术**，比特币是区块链的**应用之一** |
| ❌ Blockchain = Tokenization | 技术混淆为过程 | ✅ Blockchain是底层技术，Tokenization是在该技术上的应用过程 |
| ❌ FOF 费用更低 | 分散化降低成本 | ✅ FOF有**双重费用**（底层基金费+FOF管理费） |
| ❌ 评估估值反映真实波动 | Appraisal准确 | ✅ 评估估值**低估波动率**，需Unsmoothing调整 |
| ❌ PE 和 VC 是同一件事 | 概念混淆 | ✅ VC投资**早期**公司，PE（LBO）投资**成熟**公司 |

---

*注：本MOC基于CFA Level I Alternative Investments考纲整理，知识树中标注【考试核心】和 ↔ PP_Pxx 的部分为高频考点与教材页码对应，建议结合原版书重点复习。*
