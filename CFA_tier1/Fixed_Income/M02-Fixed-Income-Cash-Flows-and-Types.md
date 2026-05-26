---
title: "M02 — Fixed-Income Cash Flows and Types"
description: "CFA Level I 2026 official module: Fixed-Income Cash Flows and Types"
module: M02
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 2: Fixed-Income Cash Flows and Types"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M02: Fixed-Income Cash Flows and Types

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Fixed-Income Cash Flows and Types
- 2.01 | Introduction
- 2.02 | Fixed-Income Cash Flow Structures
- 2.03 | Fixed-Income Contingency Provisions
- 2.04 | Legal, Regulatory, and Tax Considerations

## Learning Outcome Statements

The candidate should be able to:

- describe common cash flow structures of fixed-income instruments and contrast cash flow contingency provisions that benefit issuers and investors
- describe how legal, regulatory, and tax considerations affect the issuance and trading of fixed-income securities

## 🌳 核心知识树

```text
🏆 M02: Fixed-Income Cash Flows and Types（固定收益现金流与类型）
├─ ⭐ 2.1 票息结构 (Coupon Structures)
│  ├─ 📐 固定利率债券 (fixed-rate)：票息率存续期内不变
│  ├─ 📐 浮动利率债券 (FRN)：Coupon = Reference Rate + Quoted Margin
│  ├─ 📐 零息债券 (zero-coupon)：折价发行，到期按面值偿还
│  ├─ 📐 递延票息债券 (deferred coupon)：初期不付息，累积后支付
│  └─ ⚠️ FRN 浮动票息缓释利率风险但未消除
│
├─ ⭐ 2.2 特殊票息与本金结构
│  ├─ 📐 递增票息债券 (step-up coupon)：票息率按预设时间表递增
│  ├─ 📐 摊还债券 (amortizing bonds)：每期同付利息和本金
│  ├─ 📐 通胀挂钩债券 (inflation-linked)：本金随 CPI 调整
│  ├─ 📐 信用联结票据 (CLN)：嵌入信用衍生品
│  └─ 📐 实物支付债券 (PIK)：可以额外债券付息
│
├─ ⭐ 2.3 或有条款 (Contingency Provisions)
│  ├─ 🎯 可赎回 (callable)：发行人有权提前赎回【考试核心】
│  ├─ 🎯 可回售 (putable)：投资者有权提前回售【考试核心】
│  ├─ 🎯 偿债基金 (sinking fund)：定期回购部分债券
│  └─ ⚠️ Callable bond 利率下降时出现价格上限 (negative convexity)
│
└─ ⭐ 2.4 法律、监管与税务考量
   ├─ 💡 法律因素：不同法域对债权人保护力度不同
   ├─ 💡 监管因素：发行注册要求、投资者限制
   └─ 💡 税务因素：利息收入所得税、资本利得税处理

   └─ ⭐ 2.5 全球债券分类
      ├─ 💡 国内债券：本国发行人 + 本国市场 + 本币
      ├─ 💡 外国债券：外国发行人 + 本国市场 + 本币（扬基/武士/熊猫）
      ├─ 💡 欧洲债券：任何市场 + 非该国货币发行
      └─ 💡 全球债券：同时在多国市场发行
```

## 📖 知识点详解

### 知识点1：票息结构（Coupon Structures）
**核心概念**：债券的票息结构决定了投资者在持有期间获得的利息支付方式和金额。不同类型的票息结构适合不同的市场环境和投资者需求。理解各种票息结构的特点有助于选择适合特定利率预期的债券投资。
- **固定利率债券（fixed-rate bonds）**：票息率在债券存续期内保持不变，每期支付固定金额的利息，是最常见的债券类型，适合预期利率稳定的环境
- **浮动利率债券（floating-rate notes, FRNs）**：票息定期重置，等于参考利率（如 SOFR、EURIBOR）+ 报价利差（quoted margin）。重置机制缓释利率风险，但报价利差固定使信用风险暴露持续存在
- **零息债券（zero-coupon bonds）**：不支付票息，以面值折价发行，到期按面值偿还。全部回报来自买入价与面值之间的价差。零息债券对利率变动最敏感（久期最大）
- **递延票息债券（deferred coupon bonds）**：初期不支付票息，票息累积后一次性或在约定时间开始支付，常见于高收益债券或项目融资

**考试应用**：比较固定利率与浮动利率债券在不同利率环境下的表现。利率上升时 FRN 更具吸引力，利率下降时固定利率债券更优。

### 知识点2：特殊票息与本金结构（Special Coupon and Principal Structures）
**核心概念**：除了基本的固定和浮动票息外，还存在多种特殊结构以满足特定的融资需求和投资目标。这些结构改变了债券的现金流模式，影响其风险和回报特征。
- **递增票息债券（step-up coupon bonds）**：票息率按预设时间表递增，补偿投资者应对未来利率上升的预期，但通常含有可赎回条款
- **摊还债券（amortizing bonds）**：每期同时支付利息和本金，现金流稳定递减，典型代表包括汽车贷款 ABS 和住房抵押贷款
- **通胀挂钩债券（inflation-linked bonds）**：本金随 CPI 调整，票息按调整后的本金支付，保护投资者购买力免受通胀侵蚀，典型产品为 TIPS
- **信用联结票据（credit-linked notes, CLNs）**：嵌入信用衍生品的债务工具，本金和票息与参考实体的信用事件挂钩
- **实物支付债券（PIK bonds）**：允许发行人选择以额外债券而非现金支付票息，常见于杠杆收购，会加剧发行人债务负担

**考试应用**：识别不同特殊结构的特征，理解它们在不同利率环境下的表现以及对投资者和发行人的影响。

### 知识点3：或有条款（Contingency Provisions）
**核心概念**：或有条款赋予发行人或投资者在特定条件下改变债券现金流的权利。这些嵌入期权会影响债券的价格、收益率和风险特征，是 CFA 考试的重点内容。
- **可赎回债券（callable bonds）**【考试核心】：发行人有权提前赎回，利率下降时发行人可通过再融资获益。可赎回债券的收益率通常较高，以补偿投资者的赎回风险
- **可回售债券（putable bonds）**【考试核心】：投资者有权提前回售，利率上升时投资者可收回资金投入更高收益工具。可回售债券的收益率通常较低
- **偿债基金条款（sinking fund provisions）**：要求发行人定期回购部分债券，降低信用风险但影响投资者的再投资计划
- ⚠️ Callable bond 在利率下降时出现价格上限（negative convexity）

**考试应用**：判断嵌入式期权的受益方，理解含期权债券与普通债券的价格和收益率差异。

### 知识点4：法律、监管与税务考量（Legal, Regulatory, and Tax Considerations）
**核心概念**：法律、监管和税务因素显著影响固定收益证券的发行和交易方式。不同司法管辖区的法律框架对债权人保护力度不同，监管要求影响发行注册和投资者限制，税务处理则影响投资者的税后回报。
- 法律因素：不同法域对债权人保护力度不同，影响债券契约条款的设计
- 监管因素：发行注册要求（如 SEC 注册 vs 私募豁免）、投资者类型限制
- 税务因素：利息收入所得税、资本利得税处理、市政债券的税收优惠

**考试应用**：理解法律、监管和税务因素如何影响债券的定价、流动性和投资者选择。

### 知识点5：全球债券分类（Global Bond Classification）
**核心概念**：根据发行人和市场所在地的不同，债券可以进行全球分类。这是理解国际固定收益市场和跨境投资的基础。
- **国内债券（domestic bonds）**：本国发行人在本国市场以本币发行
- **外国债券（foreign bonds）**：外国发行人在本国市场以本币发行（如扬基债券、武士债券、熊猫债券）
- **欧洲债券（Eurobonds）**：在任何市场以非发行国货币发行
- **全球债券（global bonds）**：同时在多个国家市场发行

**考试应用**：区分各类全球债券的定义和特征，考试常考外国债券的俗称（扬基=美国、武士=日本、熊猫=中国）。

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `Coupon = Reference Rate + Quoted Margin` | FRN票息率 | FRN 定价 | 报价利差固定，信用风险暴露持续存在 |
| `P = FV / (1 + y)^n` | 零息债券价格 | 零息债券定价 | 到期前不产生现金流 |
| `Adjusted Principal = Par × (CPI_current / CPI_base)` | 通胀调整本金 | TIPS 定价 | 可能有通缩保护或上限 |
| `PMT = P × [r(1+r)^n] / [(1+r)^n - 1]` | 摊还债券每期现金流 | 摊还债券 | 每期相同，含本金和利息 |
| `Cap Rate = Reference Rate + Cap Spread` | 浮动利率上限率 | Capped FRN 分析 | 投资者最高收益受限 |
| `Floor Rate = Reference Rate + Floor Spread` | 浮动利率下限率 | Floored FRN 分析 | 投资者最低收益受保 |
| `YTC = IRR(赎回现金流)` | 赎回收益率 | Callable 债券分析 | 价格 > 赎回价时更相关 |
| `Credit-Linked Note Payoff = Par × (1 - LGD) if credit event` | CLN 偿付 | 信用联结票据 | 条件性偿付结构 |

## 🛠️ 常见考点与解题思路

### 考点 1：比较 Fixed-Rate vs Floating-Rate 债券
- **题型**：不同利率环境下哪种债券表现更好
- **思路**：利率上升 → FRN 更具吸引力（票息随之上升）；利率下降 → 固定利率债券更优（锁定高票息）
- **示例**：投资者预期未来 3 年利率将持续上升，应选择 FRN；若预期利率下降，应选择固定利率债券
- **延伸**：FRN 的价格波动远小于同期限固定利率债券，但信用利差变化仍会导致 FRN 价格波动

### 考点 2：区分现金流结构
- **题型**：根据描述识别债券类型
- **诊断流程**：
  1. 票息是否固定？→ 固定利率 vs 浮动利率
  2. 有无期间现金流？→ 零息 vs 附息
  3. 本金是否分期偿还？→ 摊还 vs 子弹型
  4. 票息率是否随时间变化？→ step-up（递增）vs 固定
  5. 票息支付能否延迟或以实物支付？→ PIK
  6. 本金是否随通胀调整？→ inflation-linked
- **关键区分**：零息债券不支付期间票息但折价发行；递延票息债券是前几年不支付但后期补付

### 考点 3：Callable Bond 收益率分析
- **题型**：当债券价格高于赎回价时用哪个收益率指标
- **思路**：YTC (yield-to-call) 通常比 YTM 更相关，因为发行人会选择赎回
- **解题步骤**：
  1. 确认赎回价格和最早赎回日期
  2. 以赎回价格代替面值、以赎回日期代替到期日计算 YTC
  3. 比较 YTC 与 YTM，取较低者作为实际收益率预期
- **考试规律**：当债券市价 > 赎回价时，YTC 必定低于 YTM；考试常让计算两者并比较

### 考点 4：理解或有条款的受益人
- **题型**：判断条款对谁有利
- **思路**：Callable → 发行人；Putable → 投资者；Sinking fund → 降低发行人信用风险，但影响投资者再投资
- **记忆技巧**：合约中谁拥有"选择权"谁就受益
  - Callable：发行人选择是否赎回 → 发行人受益
  - Putable：投资者选择是否回售 → 投资者受益
- **价格影响**：含对投资者有利的期权 → 债券价格更高（收益率更低）；含对发行人有利的期权 → 债券价格更低（收益率更高）

### 考点 5：区分国内债券、外国债券与欧洲债券
- **题型**：识别给定发行情境下的债券类型
- **思路**：看发行人国籍、发行市场、发行货币三个维度
  1. 本国发行人 + 本国市场 + 本币 → 国内债券
  2. 外国发行人 + 本国市场 + 本币 → 外国债券（如美国发行人发日元债 = 武士债）
  3. 任何发行人 + 外国市场 + 非该国货币 → 欧洲债券
- **记忆技巧**："国内"看发行人和市场是否一致；"外国"看发行人是否外国人但用当地货币；"欧洲"看货币是否与市场所在国不同
- **考试规律**：给具体名称判断类型，扬基=美国、武士=日本、熊猫=中国

### 考点 6：理解 Step-Up Coupon 与 PIK 债券的投资者含义
- **Step-up**：票息按预设时间表递增，适用于信用质量预期改善的发行人，投资者早期承担更多风险
- **PIK**：发行人可选择以额外债券而非现金付息，增加发行人的杠杆风险，投资者面临更高违约风险
- **关键区分**：Step-up 自动递增不依赖发行人选择；PIK 是发行人选择是否以实物支付
- **考试规律**：识别两者特征和对发行人的利弊

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| FRN 无利率风险 | 重置间利率变化仍会导致价格波动 | 重置频率有限，credit spread 变化始终影响 |
| 零息债券无票息所以无需纳税 | 美国对 accrued interest 征税 | 每年隐含应计利息仍需纳税 |
| PIK bonds 利息是"免费"的 | 以债券付息增加总债务和杠杆 | 未来违约风险更高 |
| 通胀挂钩债券总是保护投资者 | 可能有调整上限或通缩保护不完整 | 条款差异显著 |

## 🔄 跨模块关联

- **现金流类型** → [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] 不同现金流的定价方法
- **浮动利率** → [[M08-Yield-and-Yield-Spread-Measures-for-Floating-Rate-Instruments]] FRN 定价与贴现利差
- **FRN 风险度量** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 利差度量
- **或有条款** → [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] 有效久期与有效凸性
- **摊销结构** → [[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]] MBS 的提前还款与摊销风险
- **债券分类** → [[M03-Fixed-Income-Issuance-and-Trading]] 市场分类中的国内/外国/欧洲债
- **税务考量** → [[M05-Fixed-Income-Markets-for-Government-Issuers]] 市政债券的税收优惠对比
- **或有条款** → [[M01-Fixed-Income-Instrument-Features]] 嵌入看涨/看跌期权的特征

## 📋 复习与刷题提示

- **核心重点**：或有条款（callable/putable）的受益人和价格影响是最高频考点
- **FRN 关键点**：理解 quoted margin vs discount margin 的区别
  - Quoted Margin：合约中固定的报价利差
  - Discount Margin：市场要求的利差，反映信用风险
- **概念区分**：固定利率 vs 浮动利率在不同利率环境下的优劣势对比
- **零息债券**：理解折价发行原理和税收处理（美国需为 accrued interest 纳税）
- **特殊结构**：
  - Step-up coupon：票息递增，常见于信用质量预期改善的发行人
  - PIK bonds：以债付息，增加杠杆风险
  - Inflation-linked：TIPS 的本金调整机制
- **刷题建议**：
  - 重点做或有条款分析题（识别受益人和价格影响）
  - 现金流结构识别题（根据描述判断债券类型）
  - FRN 相关题目（理解重置机制和定价原理）
- **易混淆点**：
  - Callable bond 的 YTC vs YTM（何时用哪个）
  - 零息债券的税务处理（应计利息的年度纳税）
- **复习时间分配**：50% 或有条款，30% 现金流结构，20% 特殊债券类型
