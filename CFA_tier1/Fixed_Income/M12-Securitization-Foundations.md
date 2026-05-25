---
title: "M12 — Securitization Foundations"
description: 资产证券化基础——SPV 结构、破产隔离、过手与结构化分配（中英双语 CFA 备考）
module: M16
subject: Fixed_Income
official_module: "Module 17: Fixed-Income Securitization"
---

# M16: 资产证券化基础 (Securitization Foundations)

## 1. 核心知识点

### 1.1 结构 (Structure)

- **发起人 -> SPV -> 投资者；服务机构收取现金流 (originator -> SPV -> investors; servicer collects cash flows)**：证券化的基本链条。发起人 (originator) 将资产出售给 SPV (special purpose vehicle)；SPV 以资产池为支持发行证券给投资者；服务机构 (servicer) 负责收取和管理现金流。
- **破产隔离与资产隔离 (bankruptcy remoteness and asset isolation)**：SPV 的核心功能是实现破产隔离 (bankruptcy remoteness)——即便发起人破产，SPV 中的资产也不受破产清算影响。这是证券化产品信用质量的核心基础。
- **过手 vs 结构化分配 (pass-through vs structured allocation intuition)**：过手结构 (pass-through) 将资产池的现金流按比例分配给所有投资者；结构化分配 (structured/tranched) 将现金流按优先级进行分层分配。

### 1.2 为何证券化 (Why Securitize)

- **融资多元化、流动性转换、风险再分配 (funding diversification, liquidity transformation, risk redistribution)**：对发起人而言，证券化提供了传统银行贷款之外的融资渠道，将非流动性资产转化为可交易的证券，并将信用风险转移给资本市场投资者。
- **投资者获得定制化敞口但面临结构复杂性 (investors gain tailored exposure but face structural complexity)**：不同风险偏好的投资者可以选择不同层级 (tranches) 的证券，获得与自身需求匹配的风险收益特征。但代价是需要理解复杂的交易结构和法律安排。

## 2. 关键公式

本模块以概念为主。核心关系为：

- `SPV 独立性 = 破产隔离 + 资产真实出售` —— SPV 必须独立于发起人
- `Pass-through: 投资者按比例分配现金流`；`Tranched: 优先级先收，次级再收`
- `信用质量 not only depend on collateral quality, but also on structure`

## 3. 常见考点与解题思路

- **理解 SPV 在证券化中的作用**：SPV 的法律独立性是破产隔离的前提。SPV 不是发起人的子公司，资产是"真实出售"给 SPV 的。
- **区分 pass-through 与 tranched 结构**：过手结构简单，所有投资者同比例分摊；分层结构复杂，不同层级有不同的现金流分配规则。
- **识别证券化的参与方**：发起人、SPV、服务机构、受托人、承销商、评级机构、信用增级提供方。理解每个角色的职能。
- **理解证券化的动机**：从发起人（降低融资成本、转移风险）和投资者（获得定制化敞口）两个角度分析。

## 4. 易错点提醒

- **结构改变对现金流的请求权，但不能神奇地消除抵押品风险 (structure changes claim on cash flows; it does not magic away collateral risk)**：证券化可以重新分配风险，但不会消除基础资产的内在风险。如果基础资产普遍违约，即使是优先级也会受到损失。
- **SPV 不是发起人的子公司**：这是破产隔离的关键。如果 SPV 被视为发起人的子公司，破产时资产可能被法院纳入破产财产。
- **Servicer 的角色很重要**：servicer 的尽职程度直接影响现金流回收。如果 servicer 能力不足或破产，可能导致违约率上升。
- **Not all securitizations are equal**：交易结构、触发机制、信用增级、服务人的差异会导致信用质量差异。

## 5. 跨模块关联

- SPV 结构 → [[M13-ABS-and-Credit-Enhancement]] 的信用增级
- 现金流分配 → [[M14-MBS-and-CMO]] 的 MBS 提前还款
- 破产隔离 → [[M11-Government-and-Corporate-Credit]] 的优先级概念
