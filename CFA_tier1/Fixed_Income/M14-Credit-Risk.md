---
title: "M14 — Credit Risk"
description: "CFA Level I 2026 official module: Credit Risk"
module: M14
subject: "Fixed Income"
topic_area: Fixed_Income
curriculum_year: 2026
official_module: "Module 14: Credit Risk"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Fixed_Income
  - official_2026
---

# M14: Credit Risk

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Credit Risk
- 14.01 | Introduction
- 14.02 | Sources of Credit Risk
- 14.03 | Credit Rating Agencies and Credit Ratings
- 14.04 | Factors Impacting Yield Spreads

## Learning Outcome Statements

The candidate should be able to:

- describe credit risk and its components, probability of default and loss given default
- describe the uses of ratings from credit rating agencies and their limitations
- describe macroeconomic, market, and issuer-specific factors that influence the level and volatility of yield spreads

## 🌳 核心知识树

```text
🏆 M14: Credit Risk（信用风险）
├─ ⭐ 14.1 损失逻辑 (Loss Logic)
│  ├─ 📐 预期信用损失 = PD × LGD × Exposure
│  ├─ 📐 LGD = 1 - Recovery Rate
│  ├─ 🎯 PD (违约概率)：发行人无法支付本息的可能性
│  ├─ 🎯 LGD (违约损失率)：违约后的损失比例
│  ├─ 🎯 Recovery Rate：违约后回收的比例（担保高→回收高）
│  └─ ⚠️ 回收率存在很大不确定性
│
├─ ⭐ 14.2 信用风险类型
│  ├─ 📐 违约风险 (Default Risk)：实际不支付本息
│  ├─ 📐 降级风险 (Downgrade Risk)：评级下调导致价格下跌
│  ├─ 📐 利差风险 (Spread Risk)：信用利差走阔导致价格下跌
│  └─ 💡 利差常在违约前走阔（前瞻性定价）
│
├─ ⭐ 14.3 信用评级
│  ├─ 💡 Moody's / S&P / Fitch 三大评级机构
│  ├─ 💡 投资级：BBB-/Baa3 及以上；高收益：BB+/Ba1 及以下
│  ├─ 🎯 评级总结相对信用风险，非保证
│  └─ ⚠️ Issuer rating ≠ Issue rating（债项因担保、优先级不同）
│
└─ ⭐ 14.4 利差驱动因素
   ├─ 💡 宏观因素：GDP 增长、利率水平、通胀
   ├─ 💡 市场因素：流动性、风险偏好、技术面
   ├─ 💡 发行人因素：财务健康、行业前景、管理层质量
   └─ 💡 Spread ≈ 信用风险溢价 + 流动性溢价 + 期权成本
```

## 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `ECL ≈ PD × LGD × Exposure` | 预期信用损失 | 信用风险评估 | 三要素缺一不可 |
| `LGD = 1 - Recovery Rate` | 违约损失率 | 损失程度估算 | 回收率难以精确预测 |
| `Credit Spread = YTM_bond - YTM_benchmark` | 信用利差 | 风险度量 | 可能含流动性和期权溢价 |
| `Spread ≈ 信用 + 流动性 + 期权溢价` | 利差分解 | 利差因素分析 | 非纯信用补偿 |

## 🛠️ 常见考点与解题思路

### 考点 1：计算预期损失
- **题型**：给定 PD、回收率、敞口，计算 ECL
- **步骤**：
  1. 回收率 → LGD = 1 - 回收率
  2. ECL = PD × LGD × Exposure
- **注意**：LGD 和回收率的关系是互补的

### 考点 2：区分违约风险与利差风险
- **违约风险**：发行人无法按时支付本息，涉及实际违约
- **利差风险**：二级市场价格因信用担忧下跌，尚未发生违约
- **考试常考**：两者的概念区分和实际案例判断

### 考点 3：理解评级对融资成本的影响
- **降级** → 利差走阔 → 债券价格下跌 → 发行人融资成本上升
- **负面观察**：即使未正式降级，列入负面观察名单也会产生影响
- **评级限制**：滞后性、发债人付费模式可能产生利益冲突

### 考点 4：分析利差变化的驱动因素
- **信用恶化**（基本面变差）：发行人的财务指标恶化
- **流动性恶化**（交易困难）：市场深度下降、bid-ask spread 扩大
- **风险偏好下降**（市场整体因素）：危机时期利差系统性走阔

## 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-------------|-------------|------|
| 利差走阔 = 即将违约 | 利差是前瞻性定价，走阔是为风险补偿增加 | 违约前利差常先走阔 |
| Issuer rating = Issue rating | 具体债项因担保、优先级可能不同 | 需区分主体评级和债项评级 |
| Credit spread 只反映信用风险 | 包含流动性溢价和期权成本 | 多因素混合 |
| 回收率可精确预测 | 取决于复杂的法律和市场环境 | 不确定性很大 |

## 🔄 跨模块关联

- **信用利差** → [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] 的利差度量
- **回收率/优先级** → [[M15-Credit-Analysis-for-Government-Issuers]] 和 [[M16-Credit-Analysis-for-Corporate-Issuers]] 的债项优先级
- **信用风险建模** → [[M17-Fixed-Income-Securitization]] 的资产隔离逻辑
- **信用增级** → [[M18-Asset-Backed-Security-Instrument-and-Market-Features]] 的内外部增级

## 📋 复习与刷题提示

- **核心重点**：ECL 计算、PD/LGD/回收率的关系
  - ECL = PD × LGD × Exposure
  - LGD = 1 - Recovery Rate
  - 回收率取决于担保品和优先级
- **风险类型区分**：
  - 违约风险：实际不支付本息（最严重）
  - 降级风险：评级下调导致价格下跌
  - 利差风险：信用利差走阔导致价格下跌
  - 利差常在违约前走阔（市场前瞻性定价）
- **评级体系**：
  - 投资级：BBB-/Baa3 及以上
  - 高收益（垃圾级）：BB+/Ba1 及以下
  - 局限性：滞后性、发债人付费模式
  - Issuer rating ≠ Issue rating
- **利差分解**：
  - Spread ≈ 信用溢价 + 流动性溢价 + 期权成本
  - 利差驱动三因素：宏观（GDP、利率）、市场（流动性、风险偏好）、发行人（财务、行业）
- **典型计算流程**：
  1. 已知 PD = 2%，Recovery Rate = 40%，Exposure = $10M
  2. LGD = 1 - 0.40 = 0.60
  3. ECL = 0.02 × 0.60 × $10M = $120,000
- **刷题建议**：
  - 重点做 ECL 计算题
  - 利差驱动因素分析题（判断给定因素 → spread ↑/↓）
  - 评级相关题（投资级 vs 高收益分界）
- **易混淆点**：
  - 利差走阔 ≠ 即将违约（可能是流动性恶化或风险偏好转变）
  - Issuer rating ≠ Issue rating
  - 回收率难以精确预测

- **关键数值记忆**：
  - ECL = PD × LGD × Exposure
  - LGD = 1 - Recovery Rate
  - IG 回收率：有担保 50-80%，优先无担保 30-60%
  - HY 回收率：优先有担保 30-60%，次级 10-30%
- **信用评级体系**：
  - 投资级：AAA → BBB-（S&P）/ Aaa → Baa3（Moody's）
  - 高收益：BB+ → D（S&P）/ Ba1 → C（Moody's）
  - 评级符号：S&P ±（如 BBB+），Moody's 数字（如 Baa1）
- **利差驱动因素总结**：
  - 宏观：GDP 增长、通胀、货币政策
  - 市场：流动性、风险偏好、技术面供需
  - 发行人：财务健康、行业地位、管理层质量
  - 利差 ≈ 信用溢价 + 流动性溢价 + 期权成本
