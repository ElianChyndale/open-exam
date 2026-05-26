---
title: "M02 — Performance Measurement"
description: "另类投资业绩衡量指标（TVPI/DPI/RVPI/IRR）、风险调整收益指标（Sortino Ratio / Sharpe Ratio）、J曲线动态以及收益平滑现象"
module: M02
subject: Alternative_Investments
official_module: "Alternative Investment Performance and Returns"
---

# M02: 另类投资业绩与回报 (Performance and Returns)

## 1. 核心知识点

### 2.1 业绩衡量指标 (Performance Measurement Metrics)【考试核心】

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

### 2.2 J曲线 (J-Curve Dynamics)【考试核心】

J曲线描述PE基金生命周期中**先负后正**的收益变化曲线。

**早期负收益原因**: 管理费持续收取（按承诺资本AUM）、初期交易成本与设立费用、投资尚未成熟退出

**后期转正原因**: 投资标的成熟、价值增长、项目退出（IPO/并购/二级出售）、DPI上升而RVPI下降

**不同策略的J曲线**:
- **VC**: J曲线最深（早期投资，失败率高，回报周期长）
- **LBO**: 相对较浅（成熟公司，有现金流，杠杆放大回报）
- **Growth Equity**: 介于两者之间

### 2.3 收益平滑 (Smoothed Returns)【考试陷阱】

**原因**: 非流动性资产按评估价值 (Appraisal Value) 而非市价 (Market Value) 估值

**后果**:
- 低估波动率 (Volatility)
- 低估与市场的相关性 (Correlation)
- 导致风险调整后收益被高估（Sharpe/Sortino偏高）

**Unsmoothing调整**: 对评估收益进行去平滑处理，还原真实波动率，使数据更接近公开市场价格波动

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| TVPI | (累计分配 + 剩余价值) / 实缴资本 = DPI + RVPI |
| DPI | 累计分配 / 实缴资本 |
| RVPI | 剩余价值 / 实缴资本 |
| Sortino | (R_p - R_f) / σ_d |
| Sharpe | (R_p - R_f) / σ_p |

## 3. 常见考点与解题思路

1. **TVPI/DPI/RVPI计算**: 给定累计分配、剩余价值和实缴资本，计算三个指标。**思路**: 先分别算DPI和RVPI，再加总得TVPI。
2. **J曲线阶段判断**: 给出基金成立年限和收益状态，判断处于J曲线的哪个阶段。**思路**: 早期（1-3年）= 负收益；中期 = 逐步转正；后期 = 正收益稳定。
3. **Sortino vs Sharpe辨析**: 题干描述指标特征，要求选出正确的指标。**思路**: Sortino看下行，Sharpe看总波动。

## 4. 易错点提醒

- **TVPI = DPI + RVPI（加法）**: 常被误认为乘法关系
- **J曲线先负后正**: 不是全程亏损，最终转正
- **收益平滑高估表现**: 评估估值导致波动率和相关性被低估，风险调整收益被高估
- **DPI vs RVPI的含义**: DPI是已实现的现金回报，RVPI是未实现的账面价值，两者性质不同
- **Sortino vs Sharpe**: 在另类投资中，Sortino通常更适用（收益分布不对称）

## 5. 跨模块关联

- TVPI/DPI/RVPI → [[M03-Private-Capital.md]] (PE基金业绩报告)
- J曲线 → [[M03-Private-Capital.md]] (PE基金生命周期)
- 收益平滑 → [[M04-Real-Estate-and-Infrastructure.md]] (房地产估值)
- 费用计算 → [[M01-Features-and-Structure.md]] (管理费和业绩提成)
