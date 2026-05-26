---
title: "M01 — Fixed-Income Instrument Features"
description: "CFA Level I 2026 official module: Fixed-Income Instrument Features"
module: M01
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 1: Fixed-Income Instrument Features"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M01: Fixed-Income Instrument Features

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Fixed-Income Instrument Features
- 1.01 | Introduction
- 1.02 | Features of Fixed-Income Securities
- 1.03 | Bond Indentures and Covenants

## Learning Outcome Statements

The candidate should be able to:

- describe the features of a fixed-income security
- describe the contents of a bond indenture and contrast affirmative and negative covenants

## 🌳 核心知识树

```text
🏆 M01: Fixed-Income Instrument Features（固定收益工具特征）
├─ ⭐ 1.1 合同解剖 (Contract Anatomy)
│  ├─ 📐 债券基本要素：发行人/面值/票息/期限/货币/优先级
│  ├─ 🎯 面值 (par value) = 到期偿还的本金金额
│  ├─ 🎯 票息率 (coupon rate) = 决定每期利息支付
│  ├─ 💡 优先级 (seniority) = 影响破产时的受偿顺序
│  └─ ⚠️ 票息确定性 ≠ 回报确定性：价格变动和再投资利率不确定性
│
├─ ⭐ 1.2 债券契约 (Bond Indenture)
│  ├─ 📐 债券契约 = 发行人与持有人之间的法律合同
│  ├─ 🎯 法律承诺 (legal promises)：按时付息、提供财报、维持抵押品
│  ├─ 🎯 支付条款 (payment terms)：票息时间表、计息基准 (day-count)
│  ├─ 🎯 肯定性契约 (affirmative covenants)：必须做（披露财报、缴税）
│  ├─ 🎯 否定性契约 (negative covenants)：不能做（限制新增债务、资产出售、股息）
│  └─ ⚠️ 考试常混淆 affirmative vs negative covenants 分类
│
├─ ⭐ 1.3 或有条款 (Contingency Provisions)
│  ├─ 📐 可赎回债券 (callable bond)【考试核心】
│  │  ├─ 💡 发行人在约定时间按约定价格赎回债券
│  │  └─ 💡 有利于发行人：利率下行时可再融资
│  ├─ 📐 可回售债券 (putable bond)【考试核心】
│  │  ├─ 💡 投资者在约定时间按约定价格回售给发行人
│  │  └─ 💡 有利于投资者：利率上升时可收回资金
│  ├─ 📐 偿债基金条款 (sinking fund provision)
│  │  └─ 💡 要求定期偿还部分本金，降低信用风险
│  └─ ⚠️ 可赎回债券利率下降时价格上升有限（被 cap 在赎回价附近）
│
├─ ⭐ 1.4 债券类型分类 (Bond Types)
│  ├─ 💡 固定利率债券 (fixed-rate)：票息率固定
│  ├─ 💡 浮动利率债券 (floating-rate)：票息随参考利率调整
│  ├─ 💡 零息债券 (zero-coupon)：折价发行，无票息
│  ├─ 💡 摊还债券 (amortizing)：每期同付利息和本金
│  └─ 💡 通胀挂钩债券 (inflation-linked)：本金随 CPI 调整
│
└─ ⭐ 1.5 债券的清偿优先级
   ├─ 📐 优先级担保债务 (Senior Secured) → 最高回收率
   ├─ 📐 优先级无担保债务 (Senior Unsecured)
   ├─ 📐 次级债务 (Subordinated) → 较低回收率
   └─ ⚠️ 清偿顺序影响回收率的估值
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `债券价格 = Σ 票息现值 + 本金现值` | 债券定价基础 | 任何债券估值 | 将在 M06 中详细展开 |
| `票息率 > YTM → 溢价债券` | 溢价/折价判断 | 判断债券交易状态 | Premium bond 价格 > 面值 |
| `票息率 = YTM → 平价债券` | 平价状态 | 判断债券交易状态 | 价格 = 面值 |
| `票息率 < YTM → 折价债券` | 折价判断 | 判断债券交易状态 | Discount bond 价格 < 面值 |

## 🛠️ 常见考点与解题思路

### 考点 1：区分 Affirmative vs Negative Covenants
- **题型**：题目给出具体条款，让考生判断属于哪一类
- **思路**：肯定性（affirmative）= 必须做某事；否定性（negative）= 不能做某事
- **典型例子**：
  - "发行人必须按时披露财务报表" → affirmative
  - "发行人不得新增超过 X 金额的债务" → negative
  - "发行人必须维持最低流动比率 1.5x" → affirmative
  - "发行人不得将资产出售给关联方" → negative
- **解题步骤**：
  1. 读题找出动词或情态动词（must / shall / will → affirmative；shall not / may not / cannot → negative）
  2. 确认主语（发行人需主动做 → affirmative；发行人被限制 → negative）
  3. 使用排除法验证
- **记忆口诀**：Affirmative = 做该做的事 (Do); Negative = 不做事 (Don't)

### 考点 2：识别 Embedded Option 的受益人
- **题型**：判断某种或有条款对谁有利
- **思路**：
  - Callable bond → 发行人受益（利率下降时可低成本再融资）
  - Putable bond → 投资者受益（利率上升时可提前收回资金）
- **记忆技巧**：
  - Callable = Issuer calls it back（发行人占主动）
  - Putable = Investor puts it back（投资者占主动）
- **延伸思考**：含期权的债券价格特征
  - Callable bond 价格 ≤ 同等普通债券价格（期权对投资者不利）
  - Putable bond 价格 ≥ 同等普通债券价格（期权对投资者有利）
- **考试陷阱**：题目可能问"哪一种债券的收益率更高" → Callable 债券收益率更高（补偿投资者的赎回风险）

### 考点 3：区分债券类型
- **题型**：根据描述判断具体债券类型
- **诊断流程**：
  1. 票息是否固定？ → 固定利率 vs 浮动利率
  2. 是否有期间现金流？ → 零息 vs 附息
  3. 本金是否分期偿还？ → 摊还 (amortizing) vs 子弹型 (bullet)
  4. 是否有特殊条款？ → 可赎回/可回售/通胀挂钩/PIK

### 考点 4：理解债券契约内容
- **题型**：问债券契约包含哪些内容或功能
- **思路**：契约 = 法律承诺（付息还本）+ 支付条款（时间表+计息基准）+ 契约条款（covenants）
- **债券契约的关键保护机制**：
  - 限制新增债务（保护现有债权人不受稀释）
  - 限制资产出售（防止资产剥离损害还款能力）
  - 限制股息支付（防止资金流出影响偿债）
  - 交叉违约条款 (cross-default)：发行人在其他债务上违约也构成本债券违约

### 考点 5：识别偿债基金条款的影响
- **题型**：判断 sinking fund provision 对债券价格、收益率和信用风险的影响
- **思路**：
  - 对信用风险：降低（发行人定期回购）
  - 对再投资风险：增加（提前收回本金需再投资）
  - 对价格：可能提供价格支撑（需求增加）
  - 关键：sinking fund 可以按面值回购或市场价格回购

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| 固定票息债券的回报是确定的 | 现金流金额确定，但价格变动和再投资利率不确定性导致实际回报波动 | 回报 = 票息 + 价格变动 + 再投资收益 |
| Callable bond 在利率下降时价格上涨无限 | 价格被赎回价 (call price) 封顶 | 发行人会选择赎回，限制上行空间 |
| Sinking fund 只降低风险 | 降低信用风险，但可能影响投资者再投资计划 | 提前偿还本金导致再投资 |
| Affirmative covenant 没有约束力 | 肯定性契约有法律约束力，违反会导致违约 | 契约条款都有法律效力 |

## 🔄 跨模块关联

- **现金流结构** → [[M02-Fixed-Income-Cash-Flows-and-Types]] 的完整现金流分类（固定/浮动/零息/摊还）
- **或有条款与嵌入期权** → [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] 的有效久期与有效凸性（期权感知风险度量）
- **优先级与抵押品** → [[M15-Credit-Analysis-for-Government-Issuers]] 和 [[M16-Credit-Analysis-for-Corporate-Issuers]] 的信用分析
- **债券契约** → [[M03-Fixed-Income-Issuance-and-Trading]] 的发行文件与信息披露

## 📋 复习与刷题提示

- **最高频考点**：affirmative vs negative covenants 的区分，几乎每次考试必出 1-2 题
- **嵌入期权**：务必掌握 callable/putable 的受益方向及其对价格的影响
  - Callable → 发行人受益，收益率更高，价格有上限
  - Putable → 投资者受益，收益率更低，价格有下限
- **概念区分**：票息率与 YTM 的关系决定了债券是溢价/折价/平价交易，这是理解后续全部分析的基础
- **常见题型**：
  - 给出具体条款判断 covenant 类型（最多）
  - 或有条款分析（次多）
  - 债券基本要素识别
  - 偿债基金条款的影响判断
- **刷题建议**：
  - 重点做债券契约内容和或有条款相关的题目（占比最高）
  - 关注 sinking fund 的双面影响（降低信用风险 vs 增加再投资风险）
  - 练习识别不同债券类型的特征描述
- **易混淆点**：Coupon rate ≠ Yield rate；票息率是债券条款的一部分，收益率是市场决定的回报率
- **复习时间分配**：本章概念为主，建议 60% 时间用于契约条款 + 或有条款，40% 用于债券要素识别
