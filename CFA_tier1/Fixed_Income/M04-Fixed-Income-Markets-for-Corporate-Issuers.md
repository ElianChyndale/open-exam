---
title: "M04 — Fixed-Income Markets for Corporate Issuers"
description: "CFA Level I 2026 official module: Fixed-Income Markets for Corporate Issuers"
module: M04
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 4: Fixed-Income Markets for Corporate Issuers"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M04: Fixed-Income Markets for Corporate Issuers

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Fixed-Income Markets for Corporate Issuers
- 4.01 | Introduction
- 4.02 | Short-Term Funding Alternatives
- 4.03 | Repurchase Agreements
- 4.04 | Long-Term Corporate Debt

## Learning Outcome Statements

The candidate should be able to:

- compare short-term funding alternatives available to corporations and financial institutions
- describe repurchase agreements (repos), their uses, and their benefits and risks
- contrast the long-term funding of investment-grade versus high-yield corporate issuers

## 🌳 核心知识树

```text
🏆 M04: Fixed-Income Markets for Corporate Issuers（公司发行人固定收益市场）
├─ ⭐ 4.1 公司债券市场
│  ├─ 📐 投资级 (IG)：BBB-/Baa3 及以上，低信用风险，低收益率
│  ├─ 📐 高收益 (HY)：BB+/Ba1 及以下，高信用风险，高收益率
│  ├─ 🎯 公开发行 (public offering)：注册制，面向广大投资者
│  ├─ 🎯 私募 (private placement)：免注册，面向合格机构投资者
│  └─ ⚠️ 高收益债券的"高收益"不等于高回报【考试陷阱】
│
├─ ⭐ 4.2 短期融资工具
│  ├─ 📐 商业票据 (CP)：短期无担保本票，期限 < 270 天
│  │  └─ ⚠️ CP 必须有备用信贷额度 (backup line) 支持
│  ├─ 📐 回购协议 (repo)：抵押短期融资
│  ├─ 📐 银行贷款：双边贷款 vs 银团贷款
│  └─ 💡 各工具的成本与风险比较
│
├─ ⭐ 4.3 中期票据 (MTN)
│  ├─ 📐 MTN = 持续发行的债务工具，期限 2-10 年
│  ├─ 🎯 比传统债券更灵活：可调整期限、金额、结构
│  └─ 💡 MTN vs 公司债券：持续发行 vs 一次性发行
│
└─ ⭐ 4.4 存款票据 (Deposit Notes)
   ├─ 💡 银行发行的债务工具，期限 18 个月 - 10 年
   ├─ 💡 可在二级市场交易
   └─ ⚠️ FDIC 保险有上限
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `BBB-/Baa3 = 投资级/高收益分界线` | 信用评级分界 | 判断债券类型 | 标普/穆迪体系不同 |
| `评级越低 → 利差越高 → 融资成本越高` | 信用风险溢价 | 融资成本分析 | 非线性关系 |
| `Price = FV × (1 - BDY × t/360)` | CP 贴现定价 | 商业票据定价 | 注意 day-count 惯例 |
| `Repo Rate ≈ 抵押品质量↑ → 利率↓` | 回购利率决定 | 融资成本分析 | 国债抵押 < 公司债抵押 |
| `Credit Spread = YTM_bond - YTM_benchmark` | 信用利差 | 风险定价 | 基准通常用同期限国债 |

### 关键数值记忆
- IG/HY 分界：S&P BBB- / Moody's Baa3
- CP 最大期限（免注册）：270 天
- MTN 典型期限：2-10 年
- Deposit notes 期限：18 个月 - 10 年

## 🛠️ 常见考点与解题思路

### 考点 1：区分 Investment-Grade vs High-Yield
- **思路**：IG = 低违约率、低收益率、利差稳定、融资渠道广泛
- **思路**：HY = 高违约率、高收益率、利差敏感、融资渠道受限
- **评级分界**：S&P BBB-/Moody's Baa3

### 考点 2：理解 CP 的备用信贷额度
- **思路**：备用信贷额度是 CP 评级的重要考量因素
- **考试常考**：无备用额度的 CP 风险显著更高，在市场压力下可能无法展期

### 考点 3：区分 MTN 与传统公司债券
- **思路**：MTN = 持续发行、条款灵活；传统债券 = 一次发行、条款固定
- **MTN 优势**：发行人可根据市场条件调整发行条款

### 考点 4：理解破产清偿顺序
- **思路**：有担保贷款 → 无担保债券 → 次级债券
- **回收率**：清偿顺序越靠前，预期回收率越高

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| 高收益债券 = 高回报 | 高票息对应高风险，违约后本金损失可能远超收益 | 风险补偿不等于确定回报 |
| CP 期限短所以无风险 | 展期风险在市场冻结时显著 | 金融危机证明 CP 市场可冻结 |
| 银团贷款 = 债券 | 本质是贷款协议，发行和交易机制不同 | 法律结构差异显著 |
| 同一公司所有债券评级相同 | 发行人评级 vs 债项评级可能不同 | 取决于抵押品和清偿顺序 |

## 🔄 跨模块关联

- **融资工具** → [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] 不同工具的价格计算
- **信用评级** → [[M14-Credit-Risk]] PD/LGD 与评级关系
- **利差行为** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 固定利率利差度量
- **公司信用分析** → [[M16-Credit-Analysis-for-Corporate-Issuers]] 公司发行人的财务分析

## 📋 复习与刷题提示

- **核心重点**：IG vs HY 的区分、CP 的特点和备用信贷额度
- **MTN 特点**：理解持续发行机制和灵活性优势（与传统公司债券的一次性发行对比）
- **清偿顺序**：掌握有担保贷款 → 无担保债券 → 次级债券的破产优先顺序和回收率关系
- **关键数据**：
  - IG/HY 分界线：S&P BBB- / Moody's Baa3
  - CP 期限：通常 < 270 天（美国免注册门槛）
- **融资工具对比**：
  - CP：短期（< 270 天）、无担保、需要备用信贷支持
  - MTN：中期（2-10 年）、持续发行、条款灵活
  - 公司债券：中长期、一次性发行、标准化
  - 银行贷款：双边或银团、可担保
- **刷题建议**：
  - 重点做融资工具识别题（描述 → 工具类型）
  - 评级分界题（给定评级判断 IG or HY）
  - 清偿顺序分析（破产时谁先受偿）
- **易混淆点**：
  - MTN 不是"中期"票据而是"持续发行"票据
  - 银团贷款本质是贷款，不是债券
  - 同一公司可能有不同债项评级

- **融资成本排序**（从低到高）：
  - 有担保贷款 < 优先无担保债券 < 次级债券 < 高收益债券
  - 同一公司内，清偿顺序越靠前融资成本越低
- **关键数据点**：
  - CP 期限：< 270 天（免注册）
  - MTN 期限：2-10 年
  - Deposit Notes 期限：18 个月 - 10 年
  - IG 回收率：50-80%（有担保），30-60%（优先无担保）
- **市场结构提示**：
  - 公开发行 vs 私募：注册要求、信息披露、投资者范围不同
  - 银团贷款市场大于高收益债券市场
  - MTN 是持续发行平台，不是单一期限工具
