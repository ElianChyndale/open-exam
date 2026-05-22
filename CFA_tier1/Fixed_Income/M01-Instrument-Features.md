---
title: "M01 — Instrument Features"
description: 债券工具特征——合同解剖、现金流结构与或有条款（中英双语 CFA 备考）
module: M01
subject: Fixed_Income
---

# M01: 工具特征与现金流 (Instrument Features and Cash Flows)

## 1. 核心知识点

### 1.1 合同解剖 (Contract Anatomy)

- **发行人/面值/票息/期限/货币/优先级 (issuer/par/coupon/maturity/currency/seniority)**：债券合同的基本要素。面值 (par value) 是到期偿还的本金金额；票息率 (coupon rate) 决定每期利息支付；优先级 (seniority) 影响破产时的受偿顺序。
- **债券契约：法律承诺、支付条款、契约条款 (bond indenture: legal promises, payment terms, covenants)**：契约是发行人与持有人之间的法律合同，包含支付时间表、提前赎回条款、财务约束等。
- **肯定性契约 vs 否定性契约 (affirmative covenants vs negative covenants)【考试陷阱】**：肯定性契约要求发行人做某事（如按时披露财报），否定性契约禁止发行人做某事（如限制新增债务）。考试常混淆两者的分类。

### 1.2 现金流结构 (Cash-Flow Structures)

- **固定利率/浮动利率/零息/摊还债券 (fixed-rate/floating-rate/zero-coupon/amortizing)**：固定利率债券每期支付固定票息；浮动利率债券票息随参考利率调整；零息债券以折价发行，到期一次性支付面值；摊还债券每期偿还部分本金。
- **通胀挂钩/递增票息/递延票息 (inflation-linked/step-up/deferred coupon)**：通胀挂钩债券本金随 CPI 调整；递增票息债券的票息率随时间上升；递延票息债券初期不支付票息，后期一次性支付累积票息。
- **或有条款：可赎回利于发行人，可回售利于投资者 (contingency provisions: callable benefits issuer; putable benefits investor)**：可赎回债券 (callable bond) 允许发行人按约定价格提前赎回；可回售债券 (putable bond) 允许投资者按约定价格提前回售给发行人。

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

- 现金流结构 → [[M03-Bond-Valuation]] 的定价方法
- 或有条款 → [[M09-Curve-Based-and-Empirical-Risk]] 的有效久期与凸性
- 优先级与抵押品 → [[M11-Government-and-Corporate-Credit]] 的信用分析
