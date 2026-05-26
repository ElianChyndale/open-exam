---
title: "M03 — Fixed-Income Issuance and Trading"
description: "CFA Level I 2026 official module: Fixed-Income Issuance and Trading"
module: M03
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 3: Fixed-Income Issuance and Trading"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M03: Fixed-Income Issuance and Trading

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Fixed-Income Issuance and Trading
- 3.01 | Introduction
- 3.02 | Fixed-Income Segments, Issuers, and Investors
- 3.03 | Fixed-Income Indexes
- 3.04 | Primary and Secondary Fixed-Income Markets

## Learning Outcome Statements

The candidate should be able to:

- describe fixed-income market segments and their issuer and investor participants
- describe types of fixed-income indexes
- compare primary and secondary fixed-income markets to equity markets

## 🌳 核心知识树

```text
🏆 M03: Fixed-Income Issuance and Trading（固定收益发行与交易）
├─ ⭐ 3.1 市场分类 (Market Map)
│  ├─ 📐 货币市场 vs 资本市场：期限是否超过一年
│  ├─ 📐 主权债 vs 准政府债 vs 公司债：信用风险逐级升高
│  ├─ 🎯 一级市场 (primary)：新发行债券的初始销售
│  ├─ 🎯 二级市场 (secondary)：已发行债券的交易 (OTC 模式)
│  ├─ 🎯 固定收益指数细分：期限/发行人/信用/货币
│  └─ ⚠️ 一级市场发行量不直接反映二级市场流动性
│
├─ ⭐ 3.2 市场参与者
│  ├─ 💡 发行人：政府、机构、公司、超国家组织
│  ├─ 💡 投资者：机构（养老保险基金、保险公司、基金）主导
│  └─ 💡 做市商 (dealer)：OTC 市场的核心流动性提供者
│
├─ ⭐ 3.3 回购融资 (Repo Financing)
│  ├─ 📐 Repo = 出售证券 + 承诺未来购回（抵押短期融资）
│  ├─ 📐 Haircut (折扣率) = (抵押品价值 - 融资金额) / 抵押品价值
│  ├─ 🎯 回购利率 (repo rate)：通常低于无担保融资利率
│  ├─ 🎯 交易对手风险 (counterparty risk)
│  └─ ⚠️ Repo 看起来像买卖，但经济本质常按融资理解【考试陷阱】
│
└─ ⭐ 3.4 指数与基准
   ├─ 💡 债券指数类型：综合、政府、公司、高收益
   ├─ 💡 指数构建：市值加权 vs 等权重
   └─ 💡 基准作用：业绩比较、ETF 追踪
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Repo rate ≈ 抵押融资成本` | 回购利率 | 比较融资成本 | 通常低于无担保融资利率 |
| `Haircut = (抵押品价值 - 融资金额) / 抵押品价值` | 折扣率 | 计算融资比例 | Haircut 越高，可融资金越少 |
| `Bid-ask spread 衡量流动性` | 做市商报价差 | 评估市场流动性 | 报价差越小，流动性越好 |
| `Bond Index: market-value-weighted` | 债券指数构建 | 指数追踪 | 市值加权最常用 |
| `Investment Grade: BBB-/Baa3+` | 投资级/高收益分界 | 信用分类 | 标普 vs 穆迪命名不同 |

### 关键数值记忆
- 货币市场期限分界：1 年（365 天）
- 投资级/高收益分界：S&P BBB- / Moody's Baa3
- CP 免注册期限：美国 270 天
- Repo haircut 范围：通常 2%-20%（取决于抵押品质量）

## 🛠️ 常见考点与解题思路

### 考点 1：区分 Primary vs Secondary Market
- **思路**：新发行 → primary；已发行债券交易 → secondary
- **关键**：一级市场决定发行价格和融资额，二级市场决定流动性和价格发现

### 考点 2：区分 Money Market vs Capital Market
- **思路**：期限 < 1 年（T-bill、CP、repo）→ money market；期限 > 1 年 → capital market
- **典型工具**：Money market = T-bills, commercial paper, bankers' acceptances, repos

### 考点 3：理解 Repo 的经济实质
- **思路**：虽然是买卖形式，但会计和风险上按抵押融资处理
- **记忆技巧**：Repo = secured short-term borrowing (出售方融入资金，买入方融出资金)

### 考点 4：区分 Investment-Grade vs High-Yield
- **思路**：评级 BBB-/Baa3 及以上为投资级；以下为高收益
- **考试常考**：两类债券的收益率特征、利差敏感性、违约率差异

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| Repo 是两笔独立的买卖 | 经济本质是抵押融资（一笔交易的两个环节） | 会计处理可能不同，但经济实质是贷款 |
| 发行量大 = 流动性好 | 流动性取决于交易活跃度和做市商参与度 | 发行量和流动性是不同概念 |
| 债券市场以交易所交易为主 | 债券市场以 OTC（场外）交易为主 | 与股票市场不同 |
| Commercial paper 无风险 | CP 依赖发行人信用和备用信贷额度 | 金融危机中 CP 市场曾冻结 |

## 🔄 跨模块关联

- **回购融资** → [[M01-Fixed-Income-Instrument-Features]] 的抵押品概念
- **市场结构** → [[M04-Fixed-Income-Markets-for-Corporate-Issuers]] 公司发行人融资市场
- **市场结构** → [[M05-Fixed-Income-Markets-for-Government-Issuers]] 政府发行人融资市场
- **利差行为** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的利差度量
- **指数与基准** → [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] 的基准收益率曲线

## 📋 复习与刷题提示

- **核心重点**：回购协议 (repo) 的经济实质和风险管理是最高频考点
- **市场分类**：
  - 货币市场（T-bill、CP、Repo、BA）：期限 ≤ 1 年
  - 资本市场（国债、公司债、MBS）：期限 > 1 年
- **概念对比**：一级市场（新发行、定价、融资额）vs 二级市场（交易、流动性、价格发现）
- **Commercial paper**：理解备用信贷额度的重要性，CP 市场在金融危机中的冻结风险
- **关键区分**：
  - 投资级（BBB-/Baa3 及以上）vs 高收益（BB+/Ba1 及以下）
  - 公开发行 vs 私募的区别
- **刷题建议**：
  - 重点做回购融资（repo rate、haircut 的计算和理解）
  - 市场分类（money market vs capital market 工具识别）
  - 指数相关题目（债券指数构建方法和细分维度）
- **易混淆点**：Repo 的"买卖"形式 vs "融资"实质；一级市场发行量不直接等于二级市场流动性
- **复习时间分配**：40% 回购协议，30% 市场分类，20% 指数，10% 参与者

- **市场数据**：
  - 固定收益市场规模约 3 倍于股票市场
  - OTC 交易占债券交易 > 90%
  - 美国国债日均交易量 > $500B
- **交易结算**：
  - 美国国债 T+1 结算
  - 公司债 T+2 结算
  - DVP（付款交割）消除本金风险
- **关键数值**：
  - 货币市场期限分界：1 年
  - IG/HY 分界：BBB-/Baa3
  - CP 免注册：270 天
  - Repo haircut：通常 2%-20%（取决于抵押品质量和波动性）
  - 债券市场规模：约 3 倍于全球股票市场
  - OTC 交易：占债券市场交易量的 90% 以上
