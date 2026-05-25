---
title: "M01 — Instrument Features"
description: 债券工具特征——合同解剖、债券契约、肯定性与否定性契约及或有条款（中英双语 CFA 备考）
module: M01
subject: Fixed_Income
official_module: "Module 1: Fixed-Income Instrument Features"
---

# M01: 工具特征 (Instrument Features)

## 1. 核心知识点

### 1.1 合同解剖 (Contract Anatomy)

- **发行人/面值/票息/期限/货币/优先级 (issuer/par/coupon/maturity/currency/seniority)**：债券合同的基本要素。面值 (par value) 是到期偿还的本金金额；票息率 (coupon rate) 决定每期利息支付；优先级 (seniority) 影响破产时的受偿顺序。
- **债券契约：法律承诺、支付条款、契约条款 (bond indenture: legal promises, payment terms, covenants)**：契约是发行人与持有人之间的法律合同，包含支付时间表、提前赎回条款、财务约束等。
- **肯定性契约 vs 否定性契约 (affirmative covenants vs negative covenants)【考试陷阱】**：肯定性契约要求发行人做某事（如按时披露财报），否定性契约禁止发行人做某事（如限制新增债务）。考试常混淆两者的分类。

### 1.2 债券契约 (Bond Indenture)

- **法律承诺 (legal promises)**：包括按时支付利息和本金、提供财务报表、维持抵押品等。这些承诺构成发行人的法律义务。
- **支付条款 (payment terms)**：明确票息支付时间和金额、本金偿还方式、计息基准 (day-count convention) 等。
- **契约条款 (covenants)**：保护投资者利益的约定。肯定性契约 (affirmative covenants) 要求发行人做某事（如按时披露财报、支付税负）；否定性契约 (negative covenants) 限制发行人做某事（如限制新增债务、限制资产出售、限制股息支付）。

### 1.3 或有条款 (Contingency Provisions)

- **可赎回债券 (callable bond)【考试核心】**：发行人在约定时间按约定价格赎回债券，有利于发行人（利率下行时可再融资）。
- **可回售债券 (putable bond)【考试核心】**：投资者在约定时间按约定价格将债券回售给发行人，有利于投资者（利率上升时可收回资金）。
- **偿债基金条款 (sinking fund provision)**：要求发行人定期偿还部分本金，降低信用风险但影响投资者再投资计划。

## 2. 关键公式

本模块以概念为主，不涉及复杂计算。核心关系为：

- `债券价值 = Σ 票息现值 + 本金现值` ——将在 M03 中详细展开
- `票息率 > YTM → 溢价债券 (premium bond)`；`票息率 < YTM → 折价债券 (discount bond)`

## 3. 常见考点与解题思路

- **区分 affirmative vs negative covenants**：肯定性（affirmative） = 必须做；否定性（negative） = 不能做。题目给出具体条款，让考生判断属于哪一类。
- **识别 embedded option 的受益人**：callable → 发行人受益（利率下降时可低成本再融资）；putable → 投资者受益（利率上升时可提前收回资金）。
- **区分债券类型**：根据描述判断是 fixed-rate、floating-rate、zero-coupon 还是 amortizing 债券。

## 4. 易错点提醒

- **票息的确定性不等于回报的确定性**：即使固定票息债券的现金流金额确定，价格变动和再投资利率的不确定性仍会导致实际回报波动。
- **可赎回债券在利率下降时价格上升有限**：因为发行人会选择赎回，价格被 cap 在赎回价附近。
- **sinking fund provision** 要求发行人定期偿还部分本金，这降低了信用风险但也可能影响投资者的再投资计划。

## 5. 跨模块关联

- 现金流结构 → [[M02-Fixed-Income-Cash-Flows]] 的完整现金流分类
- 或有条款 → [[M09-Curve-Based-and-Empirical-Risk]] 的有效久期与凸性
- 优先级与抵押品 → [[M11-Government-and-Corporate-Credit]] 的信用分析
