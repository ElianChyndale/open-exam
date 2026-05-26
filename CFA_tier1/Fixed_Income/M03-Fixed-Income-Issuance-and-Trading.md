---
title: "M03: Fixed-Income Issuance and Trading"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M03"
official_module: "Module 3: Fixed-Income Issuance and Trading"
los_count: 3
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M03: Fixed-Income Issuance and Trading

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Fixed-Income Issuance and Trading**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Fixed-Income Issuance and Trading
- 3.01 | Introduction
- 3.02 | Fixed-Income Segments, Issuers, and Investors
- 3.03 | Fixed-Income Indexes
- 3.04 | Primary and Secondary Fixed-Income Markets

## Learning Outcome Statements

1. describe fixed-income market segments and their issuer and investor participants
2. describe types of fixed-income indexes
3. compare primary and secondary fixed-income markets to equity markets

---

## 1. 模块定位

### 3.1 学习任务
- **核心问题**：考试希望你用 `Fixed-Income Issuance and Trading` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 3.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 3.3 关键英文术语
- **Fixed-Income Issuance and Trading（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed-Income Segments, Issuers, and Investors（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed-Income Indexes（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Primary and Secondary Fixed-Income Markets（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 3.1 | describe fixed-income market segments and their issuer and investor participants | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 3.2 | describe types of fixed-income indexes | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 3.3 | compare primary and secondary fixed-income markets to equity markets | 比较相似概念的适用条件与差异 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
3. Fixed-Income Issuance and Trading
├─ 3.1 市场地图 (Market Map)
│  ├─ 3.1.1 Money market vs capital market：期限、流动性和报价口径不同；T-bill/CP/repo 属短端接口
│  ├─ 3.1.2 Issuers：sovereign、agency、supranational、corporate、structured finance；决定 benchmark 与 credit lens
│  ├─ 3.1.3 Investors：banks、insurers、pension funds、mutual funds；负债期限和监管约束决定需求
│  └─ 3.1.4 Indexes：按 maturity、issuer、currency、credit quality 分层；用于 benchmark 和 portfolio risk
├─ 3.2 回购融资 (Repo Financing)
│  ├─ 3.2.1 Repo = collateralized borrowing；经济实质是融资，不是普通证券买卖
│  ├─ 3.2.2 Haircut = (collateral value - loan amount)/collateral value；抵押品风险越高，haircut 越高
│  └─ 3.2.3 Dealer/OTC 市场：流动性由做市商、bid-ask spread、issue size 和交易活跃度驱动
```

## 4. 知识点详解

### 3.1 市场地图 (Market Map)

- **货币市场 vs 资本市场；主权债 vs 准政府债 vs 公司债 (money market vs capital market; sovereign vs quasi-government vs corporate)**：货币市场 (money market) 交易期限不超过一年的短期工具；资本市场 (capital market) 交易长期债券。主权债由中央政府发行，准政府债由政府机构发行，公司债由企业发行，三者信用风险逐级升高。
- **一级发行 vs 二级交易；做市商市场流动性 (primary issuance vs secondary trading; dealer market liquidity)**：一级市场 (primary market) 是新发行债券的初始销售；二级市场 (secondary market) 是已发行债券的交易。债券二级市场以做市商 (dealer) 为核心，采用场外交易 (OTC) 模式。
- **固定收益指数：期限、发行人、信用、货币细分 (fixed-income indexes: maturity, issuer, credit, currency segmentation)**：债券指数按期限（短期/中期/长期）、发行人类型（政府/公司）、信用评级（投资级/高收益）、货币（本币/外币）等维度细分。

### 3.2 回购融资 (Repo Financing)

- **回购协议 (repurchase agreement / repo)**：一方出售证券并承诺在未来特定日期以约定价格购回。本质是抵押短期融资——卖出方融入资金，买入方获得抵押品和利息收入。
- **Haircut（折扣率）**：抵押品价值超过融资金额的部分，保护资金出借方在抵押品价值下降时的风险。Haircut 越高，借方可融得的资金越少。
- **回购利率 (repo rate)**：反映抵押融资成本，通常低于无担保融资利率（如银行间拆借利率）。回购利率受抵押品质量、期限和市场流动性影响。
- **交易对手风险 (counterparty risk)**：如果抵押品价值大幅下降，融资方可能违约；如果融资方违约，资金出借方持有抵押品但面临流动性风险。

## 5. 关键公式与计算框架

### 5.1 核心内容

本模块以概念为主。需要理解的核心关系：

- `Repo rate ≈ 抵押融资成本` —— 通常低于无担保融资利率
- `Haircut = (抵押品价值 - 融资金额) / 抵押品价值`
- `Bid-ask spread 衡量债券市场流动性` —— 做市商报价差越小，流动性越好

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 3.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 3.2 Fixed-Income Segments, Issuers, and Investors | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 3.3 Fixed-Income Indexes | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 3.4 Primary and Secondary Fixed-Income Markets | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **区分 primary market 与 secondary market**：新发行 → primary；已发行债券交易 → secondary。
- **区分 money market 与 capital market 工具**：期限短于一年（如 T-bill、CP、repo）→ money market；期限长于一年 → capital market。
- **理解 repo 的经济实质**：虽然是买卖形式，但会计和风险上按抵押融资处理。
- **区分 investment-grade 与 high-yield 债券**：评级 BBB-/Baa3 及以上为投资级；以下为高收益。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：Repo 看起来像 sale-and-repurchase，但经济本质常按融资理解【考试陷阱】：不要因为存在两笔交易就认为它是买卖，应关注其抵押融资的经济实质。 | ✅ Repo 看起来像 sale-and-repurchase，但经济本质常按融资理解【考试陷阱】：不要因为存在两笔交易就认为它是买卖，应关注其抵押融资的经济实质。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：一级市场发行量不直接反映二级市场流动性：发行量大不一定流动性好，还要看交易活跃度和做市商参与度。 | ✅ 一级市场发行量不直接反映二级市场流动性：发行量大不一定流动性好，还要看交易活跃度和做市商参与度。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Commercial paper 通常有备用信贷额度支持，这是其信用支持的重要来源，考试常考。 | ✅ Commercial paper 通常有备用信贷额度支持，这是其信用支持的重要来源，考试常考。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 接口 | 连接模块 | 本模块输出 | 做题用途 |
|---|---|---|---|
| 市场分层 | [[M04-Fixed-Income-Markets-for-Corporate-Issuers]] / [[M05-Fixed-Income-Markets-for-Government-Issuers]] | issuer、maturity、primary/secondary | 判断工具属于公司、政府还是短端融资 |
| 流动性 | [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] | OTC/dealer market、bid-ask spread | 解释 spread 中的 liquidity premium |
| Repo | [[M08-Yield-and-Yield-Spread-Measures-for-Floating-Rate-Instruments]] | short-term collateralized funding | 连接 money market rates 与融资成本 |
| Benchmark | [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] | 政府债/短端利率市场输入 | 构造曲线和基准收益率 |

- **上游模块**：[[M02-Fixed-Income-Cash-Flows-and-Types]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M04-Fixed-Income-Markets-for-Corporate-Issuers]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 回购融资 → [[M01-Instrument-Features]] 的抵押品概念
- 市场结构 → [[M04-FI-Markets-Corp-Issuers]] 公司发行人融资市场
- 市场结构 → [[M05-FI-Markets-Government-Issuers]] 政府发行人融资市场
- 利差行为 → [[M07-Yield-and-Spread-Measures]] 的利差度量


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M02-Issuance-and-Trading.md` (high, 0.579)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
