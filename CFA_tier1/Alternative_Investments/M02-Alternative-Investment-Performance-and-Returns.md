---
title: "M02 — Alternative Investment Performance and Returns"
description: "CFA Level I 2026 official module: Alternative Investment Performance and Returns"
module: M02
subject: "Alternative Investments"
topic_area: Alternative_Investments
curriculum_year: 2026
official_module: "Module 2: Alternative Investment Performance and Returns"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Alternative_Investments
  - official_2026
---

# M02: Alternative Investment Performance and Returns

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Alternative Investment Performance and Returns
- 2.01 | Introduction
- 2.02 | Alternative Investment Performance
- 2.03 | Alternative Investment Returns

## Learning Outcome Statements

The candidate should be able to:

- describe the performance appraisal of alternative investments
- calculate and interpret alternative investment returns both before and after fees

## Local Study Notes

### Migrated from `CFA_tier1/Alternative_Investments/M02-Performance-Measurement.md`

_Alignment score: 0.46. Original official module field: Alternative Investment Performance and Returns._

#### M02: 另类投资业绩与回报 (Performance and Returns)

##### 1. 核心知识点

###### 2.1 业绩衡量指标 (Performance Measurement Metrics)【考试核心】

**核心指标一览**:

| 指标 | 英文全称 | 公式 | 含义 |
|------|----------|------|------|
| TVPI | Total Value to Paid-In | (累计分配 + 剩余价值) / 实缴资本 = DPI + RVPI | 总价值倍数 |
| DPI | Distributed to Paid-In | 累计分配 / 实缴资本 | 现金回报倍数（已实现的） |
| RVPI | Residual Value to Paid-In | 剩余价值 / 实缴资本 | 未实现回报倍数 |
| IRR | Internal Rate of Return | NPV = 0 的折现率 | 内部收益率，考虑时间价值 |
| Sortino | Sortino Ratio | (R_p - R_f) / σ_d | 下行风险调整收益 |
| Sharpe | Sharpe Ratio | (R_p - R_f) / σ_p | 总风险调整收益 |

**关键关系**:
- TVPI = DPI + RVPI（**加法关系**，不是乘法）
- **DPI > 0** 表示已有现金分配回LP；**RVPI > 0** 表示还有未退出的投资价值
- **Sortino vs Sharpe**: Sortino只考虑下行波动 (σ_d)，Sharpe考虑总波动 (σ_p)。当资产收益分布不对称时，Sortino更准确

###### 2.2 J曲线 (J-Curve Dynamics)【考试核心】

J曲线描述PE基金生命周期中**先负后正**的收益变化曲线。

**早期负收益原因**: 管理费持续收取（按承诺资本AUM）、初期交易成本与设立费用、投资尚未成熟退出

**后期转正原因**: 投资标的成熟、价值增长、项目退出（IPO/并购/二级出售）、DPI上升而RVPI下降

**不同策略的J曲线**:
- **VC**: J曲线最深（早期投资，失败率高，回报周期长）
- **LBO**: 相对较浅（成熟公司，有现金流，杠杆放大回报）
- **Growth Equity**: 介于两者之间

###### 2.3 收益平滑 (Smoothed Returns)【考试陷阱】

**原因**: 非流动性资产按评估价值 (Appraisal Value) 而非市价 (Market Value) 估值

**后果**:
- 低估波动率 (Volatility)
- 低估与市场的相关性 (Correlation)
- 导致风险调整后收益被高估（Sharpe/Sortino偏高）

**Unsmoothing调整**: 对评估收益进行去平滑处理，还原真实波动率，使数据更接近公开市场价格波动

##### 2. 关键公式

| 指标 | 公式 |
|------|------|
| TVPI | (累计分配 + 剩余价值) / 实缴资本 = DPI + RVPI |
| DPI | 累计分配 / 实缴资本 |
| RVPI | 剩余价值 / 实缴资本 |
| Sortino | (R_p - R_f) / σ_d |
| Sharpe | (R_p - R_f) / σ_p |

##### 3. 常见考点与解题思路

1. **TVPI/DPI/RVPI计算**: 给定累计分配、剩余价值和实缴资本，计算三个指标。**思路**: 先分别算DPI和RVPI，再加总得TVPI。
2. **J曲线阶段判断**: 给出基金成立年限和收益状态，判断处于J曲线的哪个阶段。**思路**: 早期（1-3年）= 负收益；中期 = 逐步转正；后期 = 正收益稳定。
3. **Sortino vs Sharpe辨析**: 题干描述指标特征，要求选出正确的指标。**思路**: Sortino看下行，Sharpe看总波动。

##### 4. 易错点提醒

- **TVPI = DPI + RVPI（加法）**: 常被误认为乘法关系
- **J曲线先负后正**: 不是全程亏损，最终转正
- **收益平滑高估表现**: 评估估值导致波动率和相关性被低估，风险调整收益被高估
- **DPI vs RVPI的含义**: DPI是已实现的现金回报，RVPI是未实现的账面价值，两者性质不同
- **Sortino vs Sharpe**: 在另类投资中，Sortino通常更适用（收益分布不对称）

##### 5. 跨模块关联

- TVPI/DPI/RVPI → [[M03-Private-Capital.md]] (PE基金业绩报告)
- J曲线 → [[M03-Private-Capital.md]] (PE基金生命周期)
- 收益平滑 → [[M04-Real-Estate-and-Infrastructure.md]] (房地产估值)
- 费用计算 → [[M01-Features-and-Structure.md]] (管理费和业绩提成)
### 🌳 核心知识树

```text
🏆 M02: Alternative Investment Performance and Returns（另类投资业绩与回报）
│
├── ⭐ 业绩衡量指标 (Performance Metrics) 🎯超高頻
│   ├── 📐 TVPI = (Distributions + Residual Value) / Paid-In = DPI + RVPI
│   ├── 📐 DPI = Cumulative Distributions / Paid-In （已实现）
│   ├── 📐 RVPI = Residual Value / Paid-In （未实现）
│   ├── 📐 IRR = NPV=0的折现率（时间加权）
│   ├── 📐 Sharpe = (R_p - R_f) / σ_p（总风险调整）
│   └── 📐 Sortino = (R_p - R_f) / σ_d（下行风险调整）
│
├── ⭐ J曲线 (J-Curve Dynamics) 🎯超高頻
│   ├── 早期负收益: 管理费+交易成本+投资未成熟
│   ├── 中期转正: 投资项目成熟退出
│   ├── 后期稳定: 持续产生正回报
│   ├── VC: J曲线最深（失败率高、回报周期长）
│   ├── LBO: 相对较浅（有现金流、杠杆放大）
│   └── Growth Equity: 介于两者之间
│
├── ⭐ 收益平滑 (Smoothed Returns) 🎯高频
│   ├── 原因: 非流动性资产按评估值而非市价估值
│   ├── 后果: ⚠️ 低估波动 → 低估相关性 → 高估Sharpe
│   └── 解决: Unsmoothing处理
│
└── ⭐ 费用对业绩的影响 (Impact of Fees)
    ├── 管理费: 逐年侵蚀回报
    ├── 业绩提成: 高水位线保护投资者
    └── 净回报 vs 总回报: 费用差异显著
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| TVPI = (Distributions + RV) / Paid-In | 总价值倍数 | 衡量基金整体业绩 | 未考虑时间价值 |
| DPI = Distributions / Paid-In | 已实现回报倍数 | 衡量LP已收回现金比例 | DPI > 1表示已收回全部本金 |
| RVPI = Residual Value / Paid-In | 未实现回报倍数 | 衡量剩余投资价值 | 基于评估值可能被平滑 |
| TVPI = DPI + RVPI | 三者加法关系 | 快速检查计算一致性 | ⚠️ 常被误认为乘法 |
| IRR (Internal Rate of Return) | 内部收益率 | 考虑时间价值的回报率 | 多期现金流输入，需用计算器 |
| Sortino Ratio = (R_p - R_f) / σ_d | 下行风险调整收益 | 非对称分布更适用 | σ_d只计算下行波动 |
| Sharpe Ratio = (R_p - R_f) / σ_p | 总风险调整收益 | 对称分布适用 | 高估另类投资风险调整收益 |

### 🛠️ 常见考点与解题思路

**Topic 1: TVPI/DPI/RVPI计算**
- 已知累计分配金额、剩余价值和实缴资本
- DPI = 分配/实缴；RVPI = 剩余/实缴；TVPI = DPI + RVPI
- 注意：这是加法关系不是乘法

**Topic 2: J曲线阶段判断**
- 早期（1-3年）= 负收益（管理费消耗）
- 中期（3-5年）= 逐步转正
- 后期（5-10年）= 项目退出，正收益稳定
- VC的J曲线最深，LBO较浅

**Topic 3: Sortino vs Sharpe辨析**
- 另类投资收益分布不对称 → Sortino更适合
- Sharpe高估另类投资的风险调整收益
- 解题：看题干描述的是"下行"还是"总"波动

**Topic 4: 收益平滑影响**
- 平滑导致：波动率↓、相关性↓、Sharpe↑（虚假）
- 考试常问：收益平滑对业绩指标的影响方向

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|------------|------------|------|
| TVPI = DPI × RVPI | TVPI = DPI + RVPI（加法） | 常见记忆错误 |
| J曲线是全程亏损的 | J曲线早期负收益后期转正 | 名称来自形状像J |
| 收益平滑是好的（数据更平稳） | 平滑导致波动和相关性被低估 | 高估了风险调整收益 |
| DPI = RVPI | DPI是已实现现金，RVPI是未实现账面价值 | 性质完全不同 |
| Sharpe和Sortino在另类投资中同等适用 | Sortino更适合非对称分布的另类投资 | 下行风险更相关 |
| IRR总是最高的回报指标 | IRR对现金流时点敏感 | 早期大额回报会推高IRR |
| TVPI > 1一定赚钱 | TVPI > 1但时间很长可能年化回报低 | 未考虑货币时间价值 |

### 🔄 跨模块关联

- **TVPI/DPI/RVPI的应用** → [[M03-Investments-in-Private-Capital-Equity-and-Debt]]（PE基金业绩报告标准）
- **J曲线** → [[M03-Investments-in-Private-Capital-Equity-and-Debt]]（PE基金的生命周期阶段）
- **收益平滑** → [[M04-Real-Estate-and-Infrastructure]]（房地产的评估估值）
- **费用计算** → [[M01-Alternative-Investment-Features-Methods-and-Structures]]（管理费和业绩提成对净回报的影响）
- **Sortino vs Sharpe** → [[M06-Hedge-Funds]]（对冲基金业绩评估）
- **IRR计算方法** → Corporate Finance科目（NPV与IRR的关系）

### 📋 复习与刷题提示

- **TVPI/DPI/RVPI计算是必考题**：记住加法关系，注意区分已实现vs未实现
- **J曲线是必考概念题**：三个阶段的特征、不同策略的J曲线差异
- **收益平滑的影响方向**：波动被低估、相关性被低估、Sharpe被高估
- **Sortino与Sharpe对比**：适用场景差异，另类投资中Sortino更优
- **费用对业绩的影响**：理解净回报与总回报的差异来源
- **IRR的局限性**：对现金流时点敏感，不直接可加
- **刷题建议**：mock中TVPI计算最高频，J曲线概念其次

## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
