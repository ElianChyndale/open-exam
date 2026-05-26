---
title: "00-Derivatives-MOC"
description: "CFA L1 Derivatives 中枢 — 远期/期货/互换/期权/二叉树·公式·框架·陷阱"
subject: "Derivatives"
topic_area: Derivatives
level: CFA Level I
exam_weight: "5-8%"
exam_format: 概念+计算混合
difficulty: 无套利定价逻辑是核心主线
note_type: master_moc
status: active
tags:
  - CFA_L1
  - MOC
  - Derivatives
  - official_2026
---

# 🔀 00-Derivatives-MOC

> **一句话核心**：衍生品的本质是用少量资金获取标的资产价格敞口，核心定价逻辑是无套利(replication + cost of carry)。

---

## 📋 官方模块概览

| # | 内容 | ⚖️ | 🎯 必考点 | 🔗 |
|---|------|-----|-----------|-----|
| M01 | Instrument & Market Features | 概念 | 衍生品定义、OTC vs 交易所 | [[M01-Derivative-Instrument-and-Derivative-Market-Features]] |
| M02 | Forward Commitment & Contingent Claim | 概念 | 远期/期货/互换/期权到期收益 | [[M02-Forward-Commitment-and-Contingent-Claim-Features-and-Instruments]] |
| M03 | Benefits, Risks, Uses | 概念 | 对冲、投机、套利 | [[M03-Derivative-Benefits-Risks-and-Issuer-and-Investor-Uses]] |
| M04 | Arbitrage, Replication, Cost of Carry | 概念 | 无套利、复制定价 | [[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]] |
| M05 | Forward Pricing & Valuation | **计算** | 📐 远期定价公式、存续期估值 | [[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]] |
| M06 | Futures Pricing & Valuation | **计算** | MTM、期货vs远期差异 | [[M06-Pricing-and-Valuation-of-Futures-Contracts]] |
| M07 | Swap Pricing & Valuation | **计算** | 互换=一系列远期 | [[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]] |
| M08 | Option Pricing & Valuation | **计算** | moneyness、内在/时间价值、影响因素 | [[M08-Pricing-and-Valuation-of-Options]] |
| M09 | Put-Call Parity | **计算** | 📐 c+PV(X)=p+S₀、合成头寸 | [[M09-Option-Replication-Using-Put-Call-Parity]] |
| M10 | Binomial Model | **计算** | 📐 一期二叉树、风险中性概率 | [[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]] |

---

## 🌳 核心知识树

```text
🔀 Derivatives (5-8%) (M01-M10) 知识体系

├─ 🏆 M01-M04: 衍生品基础（概念为主）
│  │
│  ├─ 🏆 M01: Instrument and Market Features（衍生品特征与市场）
│  │  ├─ ⭐ 衍生品定义：价值源于标的资产的金融工具
│  │  └─ ⭐ OTC（定制·对手风险）vs 交易所（标准化·CCP清算）
│  │
│  ├─ 🏆 M02: Forward Commitment & Contingent Claim（分类）
│  │  ├─ ⭐ Forward commitment：远期/期货/互换——双方有义务履约
│  │  ├─ ⭐ Contingent claim：期权——买方有选择权
│  │  └─ 🎯 到期收益计算
│  │     ├─ 📐 Long call payoff = max(0, ST-X)
│  │     ├─ 📐 Long put payoff = max(0, X-ST)
│  │     └─ ⚠️ payoff≠profit！profit要扣除期权费
│  │
│  ├─ 🏆 M03: Benefits, Risks, Uses（用途与风险）
│  │  └─ ⭐ 对冲·投机·套利·价格发现·杠杆
│  │
│  └─ 🏆 M04: Arbitrage, Replication, Cost of Carry（定价原则）
│     ├─ ⭐ 无套利原则：复制组合成本 = 衍生品公允价值
│     └─ ⭐ 持有成本模型：F = S×(1+持有成本) - 持有收益
│
├─ 🏆 M05-M07: 远期承诺定价（计算核心）
│  │
│  ├─ 🏆 M05: Forward Pricing and Valuation（远期定价）【高频计算】
│  │  ├─ 📐 无收益资产：F₀(T) = S₀(1+r)^T（基础公式）
│  │  ├─ 📐 已知收入资产：F₀(T) = [S₀-PV(I)](1+r)^T
│  │  ├─ 📐 已知收益率资产：F₀(T) = S₀[(1+r)/(1+q)]^T
│  │  ├─ 📐 存续期价值：Vt(long) = St - PVt(K)
│  │  ├─ 📐 多头到期收益：ST - K；空头：K - ST
│  │  └─ ⚠️ 期初价值=0（公平定价），存续期间价值≠0
│  │
│  ├─ 🏆 M06: Futures Pricing（期货定价）【计算】
│  │  ├─ ⭐ 期货公平价格 ≈ 远期公平价格（公式相同）
│  │  ├─ 🎯 期货 vs 远期核心区别
│  │  │  ├─ 期货每日盯市（Mark-to-Market）+ 保证金，远期到期结算
│  │  │  └─ 利率与标的正相关→期货价>远期；负相关→期货价<远期
│  │  └─ ⚠️ 中央对手方(CCP)降低对手风险
│  │
│  ├─ 🏆 M07: Swap Pricing（互换定价）【计算】
│  │  └─ ⭐ 互换 ≈ 一系列远期合约（FRA）
│  │
│  └─ 🏆 M08-M10: 期权定价（计算核心）
│     │
│     ├─ 🏆 M08: Option Pricing and Valuation（期权定价）【高频计算】
│     │  ├─ ⭐ Moneyness：ITM（实值）/ ATM（平值）/ OTM（虚值）
│     │  ├─ 📐 内在价值(Intrinsic)：立即行权的价值
│     │  ├─ 📐 时间价值(Time)：期权价 - 内在价值
│     │  ├─ 🎯 影响期权价格的因素
│     │  │  ├─ c↑：S₀↑, X↓, T↑, σ↑, r↑
│     │  │  └─ p↑：S₀↓, X↑, T↑, σ↑, r↓
│     │  └─ ⚠️ 美式期权价值≥欧式（提前行权权有价）
│     │
│     ├─ 🏆 M09: Put-Call Parity（买卖权平价）【高频计算】
│     │  ├─ 📐 c + PV(X) = p + S₀（标准欧式平价）
│     │  ├─ 📐 c + PV(X) + PV(I) = p + S₀（含股息）
│     │  ├─ 📐 c + PV(X) = p + S₀e^(-qT)（连续收益率）
│     │  ├─ 📐 c + PV(X) = p + PV(F)（远期平价）
│     │  ├─ 🎯 合成头寸：移项可得合成call/put/stock
│     │  └─ ⚠️ 平价只对欧式成立！美式因提前行权不严格成立
│     │
│     └─ 🏆 M10: Binomial Model（二叉树模型）【计算】
│        ├─ 📐 c = [πc⁺ + (1-π)c⁻] / (1+r)（期权价值）
│        ├─ 📐 π = (1+r-d) / (u-d)（风险中性概率）
│        ├─ 🎯 风险中性定价：用风险中性概率，不关心真实概率
│        └─ ⚠️ 多期二叉树 = 一期递归应用
```

---

## 🔗 跨模块依赖关系

```text
M01-M04（基础概念）
└── M04（无套利定价原则）←── Quant M02 TVM
    ├── M05-M06（远期/期货）──► M07（互换 = 一系列FRA）
    └── M08（期权基础）──► M09（Put-Call Parity）──► M10（二叉树）

🔗 跨科目：
  M05 远期定价 ──► Quant M02 TVM（折现）
  M04 无套利 ──► FI M06 估值
  M08 期权 ──► Equity M08 认股权证
```

---

## 🔑 核心对比专题

| 对比 | 🔑 区别 | 🎯 判断 |
|------|---------|---------|
| **远期 vs 期货** | OTC vs 交易所；到期结算 vs 每日MTM | 交易所交易→期货 |
| **远期承诺 vs 期权** | 对称义务 vs 不对称权利 | 有权利无义务→期权 |
| **欧式 vs 美式** | 到期行权 vs 到期前任意时间 | 美式≥欧式价值 |
| **看涨 vs 看跌** | 买权(S↑获利) vs 卖权(S↓获利) | 看涨call，看跌put |
| **内在 vs 时间价值** | 现在行权值 vs 未来溢价 | 期权价=内在+时间 |
| **风险中性vs真实概率** | 二叉树用风险中性π，非真实 | 调整衍生品定价 |

---

## 📐 核心公式速查

| 公式 | 用途 | ⚠️ |
|------|------|-----|
| `F₀(T)=S₀(1+r)^T` | 无收益远期定价 | 基础公式 |
| `F₀(T)=[S₀-PV(I)](1+r)^T` | 已知收入资产 | 股息调整 |
| `Vt(long)=St-PVt(K)` | 存续期多头价值 | |
| `c+PV(X)=p+S₀` | Put-Call Parity | 只对欧式 |
| `c=max(0,S₀-X)` | 看涨到期收益 | 不含期权费 |
| `p=max(0,X-S₀)` | 看跌到期收益 | |
| `c=[πc⁺+(1-π)c⁻]/(1+r)` | 二叉树 | π是风险中性 |
| `π=(1+r-d)/(u-d)` | 风险中性概率 | |

---

## 🚨 高频陷阱速查

| ❌ 错误 | ✅ 正确 | 🎯 |
|---------|---------|-----|
| 期货=远期价格相同 | 利率相关时可能不同（MTM） | ⭐⭐⭐ |
| 期权价=内在价值 | 期权价=内在+时间价值 | ⭐⭐⭐ |
| 平价公式对所有期权成立 | 只对**欧式** | ⭐⭐⭐ |
| 二叉树用真实概率 | 用风险中性概率 | ⭐⭐ |
| 远期期初有价值 | 期初价值=0（公平定价） | ⭐⭐⭐ |

---

## 💡 学习路径

```
阶段1 ─── M01→M02→M03→M04（基础概念+定价原则）
阶段2 ─── M05→M06→M07（远期/期货/互换 定价计算）
阶段3 ─── M08→M09→M10（期权定价/平价/二叉树）
```
