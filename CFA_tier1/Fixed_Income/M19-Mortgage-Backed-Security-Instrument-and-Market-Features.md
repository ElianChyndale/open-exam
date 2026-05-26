---
title: "M19 — Mortgage-Backed Security (MBS) Instrument and Market Features"
description: "CFA Level I 2026 official module: Mortgage-Backed Security (MBS) Instrument and Market Features"
module: M19
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 19: Mortgage-Backed Security (MBS) Instrument and Market Features"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M19: Mortgage-Backed Security (MBS) Instrument and Market Features

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Mortgage-Backed Security (MBS) Instrument and Market Features
- 19.01 | Introduction
- 19.02 | Time Tranching
- 19.03 | Mortgage Loans and Their Characteristic Features
- 19.04 | Residential Mortgage-Backed Securities (RMBS)
- 19.05 | Commercial Mortgage-Backed Securities (CMBS)

## Learning Outcome Statements

The candidate should be able to:

- define prepayment risk and describe time tranching structures in securitizations and their purpose
- describe fundamental features of residential mortgage loans that are securitized
- describe types and characteristics of residential mortgage-backed securities, including mortgage pass-through securities and collateralized mortgage obligations, and explain the cash flows and risks for each type
- describe characteristics and risks of commercial mortgage-backed securities

## 🌳 核心知识树

```text
🏆 M19: MBS Instrument and Market Features（抵押贷款支持证券）
├─ ⭐ 19.1 抵押贷款基础
│  ├─ 📐 固定利率 vs 可调利率抵押贷款
│  ├─ 📐 摊还型 vs 气球还款型
│  ├─ 📐 提前还款权 (Prepayment Option)：借款人可提前还款
│  └─ 💡 抵押贷款是 MBS 的基础资产
│
├─ ⭐ 19.2 提前还款风险 (Prepayment Risk)
│  ├─ 📐 收缩风险 (Contraction Risk)：利率↓ → 提前还款↑ → 资金需低利率再投资
│  ├─ 📐 展期风险 (Extension Risk)：利率↑ → 提前还款↓ → 资金锁定时间延长
│  ├─ 📐 CPR = 1 - (1 - SMM)^12（条件提前还款率）
│  ├─ 📐 PSA 基准：100% PSA = 第1月 0.2% → 第30月 6% → 后保持 6%
│  └─ ⚠️ MBS 呈现负凸性：利率↓时价格上涨受限
│
├─ ⭐ 19.3 RMBS 结构
│  ├─ 📐 过手 MBS (Pass-Through)：按比例传递本息
│  ├─ 📐 CMO：分层重新分配提前还款风险
│  │  ├─ Sequential-Pay：按顺序偿还各层
│  │  └─ PAC Tranche：有预先设定的偿还计划
│  ├─ 💡 Agency MBS：Ginnie/Fannie/Freddie 担保
│  └─ 💡 Non-Agency MBS：依赖信用增级
│
├─ ⭐ 19.4 CMBS 特征
│  ├─ 📐 气球到期 (Balloon Maturity)：期末大额本金余额
│  ├─ 📐 气球风险：到期无法再融资的风险
│  ├─ 📐 提前还款保护：Lockout / Defeasance / Yield Maintenance
│  ├─ 📐 物业类型：办公、零售、工业、多户住宅、酒店
│  └─ ⚠️ 气球风险是 CMBS 独有的核心风险【考试核心】
│
└─ ⭐ 19.5 CMBS 信用分析
   ├─ 📐 DSCR = NOI / Debt Service
   ├─ 📐 LTV = Loan Amount / Property Value
   ├─ 📐 Debt Yield = NOI / Loan Amount
   └─ 💡 分层结构 + 信用增级
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `CPR = 1 - (1 - SMM)^12` | 条件提前还款率 | 提前还款速度 | SMM = 单月提前还款率 |
| `100% PSA = 第1月0.2% → 第30月6%` | PSA 基准模型 | 提前还款假设 | 行业标准基准 |
| `Prepayment Risk = 收缩风险 + 展期风险` | 提前还款风险拆分 | 风险分析 | 利率↑↓方向不同 |
| `DSCR = NOI / Debt Service` | 偿债覆盖比率 | CMBS 信用分析 | < 1.0 表示不足 |
| `LTV = Loan Amount / Property Value` | 贷款价值比 | CMBS 信用分析 | 越高风险越大 |
| `Debt Yield = NOI / Loan Amount` | 债务收益率 | CMBS 信用分析 | 不依赖资本化率 |

## 🛠️ 常见考点与解题思路

### 考点 1：区分收缩风险与展期风险
- **利率下降 → 提前还款增加 → 收缩风险**（好处变坏处：资金需低利率再投资）
- **利率上升 → 提前还款减少 → 展期风险**（坏处加坏处：低利率锁定时间延长）
- **记忆技巧**：Contraction = 资金"收缩"回来；Extension = 期限"延长"了

### 考点 2：理解 CMO 分层的作用
- **CMO 不消除提前还款风险**，只重新分配
- Sequential-Pay：A 层先收本金 → B 层 → C 层
- PAC Tranche：有保护的本金偿还计划，但极端情况下保护可能失效
- **考试常考**：判断给定分层结构对哪类投资者有利

### 考点 3：区分 CMBS 与 RMBS
- **CMBS 独有的**：气球风险、提前还款保护（lockout/defeasance）、贷款笔数少、集中度高
- **RMBS 特征**：无气球风险、提前还款灵活（可随时还款）、贷款笔数多
- **Core difference**：气球到期 + 提前还款保护是 CMBS 的关键标识

### 考点 4：CMBS 提前还款保护机制排序
- **严格程度**：Lockout > Defeasance > Yield Maintenance > Prepayment Penalty
- **Lockout**：完全禁止提前还款（最严格）
- **Defeasance**：以国债替代抵押（常见于 CMBS）
- **Yield Maintenance**：补偿投资者利息损失

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| MBS 无凸性问题 | MBS 有负凸性（利率↓价格↑受限） | 提前还款行为的不对称性 |
| CMO 消除提前还款风险 | 只重新分配，总量不变 | PAC 保护在极端下失效 |
| CMBS 与 RMBS 提前还款风险相同 | CMBS 有更强保护机制（lockout/defeasance） | 商业 vs 住宅贷款差异 |
| 气球风险在 RMBS 中也存在 | RMBS 通常 fully amortizing，无气球风险 | 住宅贷款 30 年摊还 |
| CMBS 提前还款保护 = 无风险 | 保护机制在特定条件下可能失效 | 物业出售等因素 |

## 🔄 跨模块关联

- **提前还款与嵌入期权** → [[M01-Fixed-Income-Instrument-Features]] 的或有条款（隐含看涨期权）
- **负凸性** → [[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]] 的凸性概念
- **CMO 分层** → [[M18-Asset-Backed-Security-Instrument-and-Market-Features]] 的分层信用增级
- **现金流分配** → [[M17-Fixed-Income-Securitization]] 的 SPV 结构
- **时间分层** → time tranching 的概念

## 📋 复习与刷题提示

- **核心重点**：收缩风险 vs 展期风险的区分（最高频考点）
  - 利率↓ → 提前还款↑ → 收缩风险（资金需低利率再投资）
  - 利率↑ → 提前还款↓ → 展期风险（低利率锁定时间延长）
  - 记忆：收缩 = 资金"缩"回来；展期 = 期限拉"长"
- **关键概念**：
  - 负凸性：MBS 在利率↓时价格↑受限（因为提前还款↑）
  - PSA 模型：100% PSA = 第1月 0.2% CPR → 第30月 6% CPR
  - CPR（年化提前还款率）：CPR = 1 - (1 - SMM)^12
- **RMBS vs CMBS 核心差异**：
  | 维度 | RMBS | CMBS |
  |------|------|------|
  | 气球风险 | 极少（fully amortizing） | 核心风险（balloon maturity）|
  | 提前还款 | 灵活（随时可还） | 有保护（lockout/defeasance）|
  | 贷款笔数 | 成百上千 | 20-100 笔 |
  | 集中度风险 | 低 | 高 |
  | 物业类型 | 住宅 | 商业（办公/零售/工业/酒店）|
- **CMBS 提前还款保护排序（严格→宽松）**：
  Lockout > Defeasance > Yield Maintenance > Prepayment Penalty
- **CMBS 信用分析指标**：
  - DSCR = NOI / Debt Service（< 1.0 = 不足）
  - LTV = Loan Amount / Property Value
  - Debt Yield = NOI / Loan Amount
- **刷题建议**：
  - 重点做收缩/展期风险判断题（给定利率变化方向 → 判断风险类型）
  - CMBS vs RMBS 对比题（列表对比关键差异）
  - 提前还款保护机制排序
  - 负凸性分析题
- **易混淆点**：
  - CMO 不消除提前还款风险（只重新分配）
  - CMBS 保护机制可能失效
  - 气球风险是 CMBS 独有的
  - MBS 的负凸性特征
