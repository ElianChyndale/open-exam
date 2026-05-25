---
title: "M03 — Issuance and Trading"
description: 债券发行与交易——一级市场、二级市场、回购融资与市场结构（中英双语 CFA 备考）
module: M03
subject: Fixed_Income
official_module: "Module 3: Fixed-Income Issuance and Trading"
---

# M03: 发行、交易与回购融资 (Issuance, Trading, and Repo Financing)

## 1. 核心知识点

### 1.1 市场地图 (Market Map)

- **货币市场 vs 资本市场；主权债 vs 准政府债 vs 公司债 (money market vs capital market; sovereign vs quasi-government vs corporate)**：货币市场 (money market) 交易期限不超过一年的短期工具；资本市场 (capital market) 交易长期债券。主权债由中央政府发行，准政府债由政府机构发行，公司债由企业发行，三者信用风险逐级升高。
- **一级发行 vs 二级交易；做市商市场流动性 (primary issuance vs secondary trading; dealer market liquidity)**：一级市场 (primary market) 是新发行债券的初始销售；二级市场 (secondary market) 是已发行债券的交易。债券二级市场以做市商 (dealer) 为核心，采用场外交易 (OTC) 模式。
- **固定收益指数：期限、发行人、信用、货币细分 (fixed-income indexes: maturity, issuer, credit, currency segmentation)**：债券指数按期限（短期/中期/长期）、发行人类型（政府/公司）、信用评级（投资级/高收益）、货币（本币/外币）等维度细分。

### 1.2 回购融资 (Repo Financing)

- **回购协议 (repurchase agreement / repo)**：一方出售证券并承诺在未来特定日期以约定价格购回。本质是抵押短期融资——卖出方融入资金，买入方获得抵押品和利息收入。
- **Haircut（折扣率）**：抵押品价值超过融资金额的部分，保护资金出借方在抵押品价值下降时的风险。Haircut 越高，借方可融得的资金越少。
- **回购利率 (repo rate)**：反映抵押融资成本，通常低于无担保融资利率（如银行间拆借利率）。回购利率受抵押品质量、期限和市场流动性影响。
- **交易对手风险 (counterparty risk)**：如果抵押品价值大幅下降，融资方可能违约；如果融资方违约，资金出借方持有抵押品但面临流动性风险。

## 2. 关键公式

本模块以概念为主。需要理解的核心关系：

- `Repo rate ≈ 抵押融资成本` —— 通常低于无担保融资利率
- `Haircut = (抵押品价值 - 融资金额) / 抵押品价值`
- `Bid-ask spread 衡量债券市场流动性` —— 做市商报价差越小，流动性越好

## 3. 常见考点与解题思路

- **区分 primary market 与 secondary market**：新发行 → primary；已发行债券交易 → secondary。
- **区分 money market 与 capital market 工具**：期限短于一年（如 T-bill、CP、repo）→ money market；期限长于一年 → capital market。
- **理解 repo 的经济实质**：虽然是买卖形式，但会计和风险上按抵押融资处理。
- **区分 investment-grade 与 high-yield 债券**：评级 BBB-/Baa3 及以上为投资级；以下为高收益。

## 4. 易错点提醒

- **Repo 看起来像 sale-and-repurchase，但经济本质常按融资理解【考试陷阱】**：不要因为存在两笔交易就认为它是买卖，应关注其抵押融资的经济实质。
- **一级市场发行量不直接反映二级市场流动性**：发行量大不一定流动性好，还要看交易活跃度和做市商参与度。
- **Commercial paper 通常有备用信贷额度支持**，这是其信用支持的重要来源，考试常考。

## 5. 跨模块关联

- 回购融资 → [[M01-Instrument-Features]] 的抵押品概念
- 市场结构 → [[M04-FI-Markets-Corp-Issuers]] 公司发行人融资市场
- 市场结构 → [[M05-FI-Markets-Government-Issuers]] 政府发行人融资市场
- 利差行为 → [[M07-Yield-and-Spread-Measures]] 的利差度量
