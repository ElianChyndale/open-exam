---
title: "M14 — MBS and CMO"
description: 抵押贷款支持证券与 CMO——提前还款风险、收缩风险、展期风险与分层结构（中英双语 CFA 备考）
module: M18
subject: Fixed_Income
official_module: "Module 19: Mortgage-Backed Security (MBS) Instrument and Market Features"
---

# M18: 住宅 MBS 与 CMO 结构 (RMBS and CMO Structures)

## 1. 核心知识点

### 1.1 抵押贷款现金流风险 (Mortgage Cash-Flow Risk)

- **借款人提前还款导致利率下降时的收缩风险 (borrower prepayment creates contraction risk when rates fall)**：当利率下降时，借款人倾向于再融资来提前还款 (prepayment)。这导致 MBS 投资者提前收回本金，面临收缩风险 (contraction risk)——资金回笼后只能以较低利率再投资。
- **利率上升且再融资放缓时展期风险增加 (extension risk grows when rates rise and refinancing slows)**：当利率上升时，借款人不会提前还款，MBS 投资者面临展期风险 (extension risk)——预期回收本金的时间延长，锁定在较低利率的资金期限被拉长。
- **过手投资者收到计划本金加上提前还款 (passthrough investors receive scheduled principal plus prepayments)**：过手 MBS (pass-through) 将抵押贷款池的本息按比例传递给投资者，包含计划内本金摊销和任何提前还款。

### 1.2 结构化 (Structuring)

- **机构/非机构区分；抵押品与担保分析 (agency/non-agency distinction; collateral and guarantee analysis)**：机构 MBS (agency MBS) 由 Ginnie Mae、Fannie Mae、Freddie Mac 发行或担保，有政府或政府机构的信用支持；非机构 MBS (non-agency MBS) 没有政府担保，依赖信用增级。
- **CMO 分层重新分配提前还款时间 (CMO tranches redistribute prepayment timing)**：CMO (collateralized mortgage obligation) 将 MBS 现金流切分为不同层级的证券 (tranches)，各层级有不同的本金偿还顺序，从而重新分配提前还款风险。
- **顺序偿付 vs 计划分配 (sequential-pay vs planned allocation intuition)**：顺序偿付结构 (sequential-pay) 中，优先级 tranche 先收回本金，然后下一级再开始回收；计划分配结构（如 PAC tranche）有预先设定的本金偿还计划，提供更可预测的现金流。

## 2. 关键公式

本模块以概念为主。核心关系为：

- `Prepayment risk = 收缩风险 (利率↓) + 展期风险 (利率↑)`
- `CPR (Conditional Prepayment Rate) = 1 - (1 - SMM)^12`，其中 SMM 是单月提前还款率
- `PSA 基准模型：100% PSA = 第 1 个月 0.2%，直至第 30 个月 6%，之后保持 6%`
- `负凸性 (negative convexity) = 利率下降时 MBS 价格上涨受限`

## 3. 常见考点与解题思路

- **区分收缩风险与展期风险**：利率下降 → 提前还款增加 → 收缩风险（资金需低利率再投资）；利率上升 → 提前还款减少 → 展期风险（资金锁定时间延长）。
- **理解 CMO 分层的作用**：CMO 不消除提前还款风险，而是将其在不同层级间重新分配。优先级 tranche 先偿还，吸收部分收缩风险；次级 tranche 后偿还，承担更多展期风险。
- **分析 agency vs non-agency MBS 的区别**：agency MBS 有政府/机构担保，信用风险低；non-agency MBS 信用风险取决于抵押品质量和信用增级。
- **判断负凸性**：MBS 在利率下降时价格上升幅度小于普通债券，因为提前还款限制了价格上升空间。

## 4. 易错点提醒

- **MBS 可能呈现负凸性，因为现金流对投资者不利变化 (MBS can show negative convexity because cash flows change against the investor)**：MBS 投资者面临一种不对称：利率下降（好事）时，借款人提前还款（坏事），价格上涨受限；利率上升（坏事）时，提前还款停止（也是坏事），价格下跌无缓冲。
- **CMO 不消除提前还款风险**：它只重新分配。所有层的总风险和 MBS 池的总风险相同。
- **PAC (Planned Amortization Class) tranche 不是无风险的**：虽然 PAC 有本金偿还计划保护，但在极端提前还款情境下保护可能失效（打破 PAC 的还款计划）。
- **Prepayment modeling 是 MBS 分析的核心难点**：提前还款行为受利率路径、房价变动、失业率、季节性因素等多种因素影响，难以精确预测。

## 5. 跨模块关联

- 提前还款 → [[M01-Instrument-Features]] 的嵌入期权概念（隐含看涨期权）
- 负凸性 → [[M08-Duration-and-Convexity]] 的凸性概念
- CMO 分层 → [[M13-ABS-and-Credit-Enhancement]] 的分层信贷增级
- 现金流分配 → [[M12-Securitization-Foundations]] 的 SPV 结构
