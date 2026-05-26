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
