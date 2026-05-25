---
title: "M13 — ABS and Credit Enhancement"
description: 资产支持证券与信用增级——ABS 类型、抵押品分析、内部与外部信用增级（中英双语 CFA 备考）
module: M13
subject: Fixed_Income
official_module: "Supplementary — Securitization"
---

# M13: ABS 与信用增级 (ABS and Credit Enhancement)

## 1. 核心知识点

### 1.1 ABS 类型 (ABS Families)

- **汽车贷款、信用卡、应收账款、其他非抵押担保品 (auto loans, credit cards, receivables, other non-mortgage collateral)**：ABS (asset-backed securities) 的抵押品范围广泛。汽车贷款 ABS 有明确的摊销计划；信用卡 ABS 通常为循环结构（本金可重新投资于新应收账款）；应收账款 ABS 依赖商业交易的付款周期。
- **担保品现金流模式决定摊还与触发风险 (collateral cash flow pattern determines amortization and trigger risk)**：不同类型 ABS 的现金流模式不同。摊还型 (amortizing) 如汽车贷款有固定还款计划；循环型 (revolving) 如信用卡允许借款人在额度内循环使用。
- **有担保债券保持双重追索权，不同于典型 ABS 隔离 (covered bond keeps dual recourse unlike typical ABS isolation)**：Covered bond（有担保债券）与 ABS 的关键区别：covered bond 投资者同时拥有对担保池和发行人的双重追索权 (dual recourse)；而 ABS 投资者仅对 SPV 中的资产池有追索权。

### 1.2 信用增级 (Credit Enhancement)

- **分层、超额抵押、超额利差、准备金账户 (subordination, overcollateralization, excess spread, reserve accounts)**：内部增级方式。分层 (subordination/tranching) 让优先级吸收次级层的保护；超额抵押 (overcollateralization) 指资产池价值超过发行的债券金额；超额利差 (excess spread) 是资产池收益超过证券支付和费用的部分；准备金账户 (reserve account) 作为现金缓冲。
- **担保/保险作为外部支持 (guarantees/insurance as external support)**：外部增级来自第三方机构，如保险公司提供的债券保险 (bond insurance)、银行开立的信用证 (letter of credit) 或公司担保 (corporate guarantee)。

## 2. 关键公式

| 指标 | 公式/概念 |
|------|-----------|
| 超额抵押 | `Overcollateralization = (资产池面值 - 证券面值) / 证券面值` |
| 超额利差 | `Excess Spread = 资产池加权平均利率 - 证券加权平均利率 - 费用` |
| 信用增级水平 | `Credit Enhancement Level = 次级层 + 准备金 + 超额利差现值` |
| 双重追索权 | `Covered Bond: 资产池 + 发行人信用` |

## 3. 常见考点与解题思路

- **区分内部与外部信用增级**：内部（分层、超额抵押、超额利差、准备金账户）vs 外部（保险、信用证、第三方担保）。
- **理解 covered bond 的双重追索权**：covered bond 投资者在发行人违约时，既可以追索担保资产池，也可以追索发行人的其他资产。这与 ABS 的单一追索权不同。
- **ABS 的摊销类型判断**：给定抵押品特征（如汽车贷款、信用卡应收款），判断是摊还型还是循环型结构。
- **分析超额利差的缓冲作用**：当资产池中部分贷款违约时，超额利差可以吸收损失，保护优先级证券投资者。

## 4. 易错点提醒

- **信用增级重新分配损失吸收，而非免费收益 (credit enhancement reallocates loss absorption; it is not free yield)**：信用增级提高优先级证券的信用质量，但代价是次级层承担更大的风险。优先级收益率的"降低"不是免费获得的，而是通过牺牲次级的利益实现的。
- **Covered bond 不是 ABS**：两者最大区别在于法律结构——covered bond 不出售资产给 SPV，资产仍留在发行人资产负债表上，投资者有双重追索权。
- **Excess spread 不是永久性保护**：如果资产池中的贷款大规模违约，超额利差可能迅速耗尽。
- **Trigger events（触发事件）** ：许多 ABS 设有信用触发机制（如超额利差降至阈值以下），一旦触发会改变现金流分配方式，如强制提前摊还。

## 5. 跨模块关联

- 信用增级 → [[M12-Securitization-Foundations]] 的 SPV 结构
- 分层设计 → [[M14-MBS-and-CMO]] 的 CMO 分层
- Covered bond → [[M11-Government-and-Corporate-Credit]] 的发行人信用分析
