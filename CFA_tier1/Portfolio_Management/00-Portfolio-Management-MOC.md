---
title: "00-Portfolio-Management-MOC"
description: "CFA L1 PM 中枢 — 组合理论·CAPM·IPS·偏差·风险·公式·陷阱"
subject: "Portfolio Management"
topic_area: Portfolio_Management
level: CFA Level I
exam_weight: "8-12%"
exam_format: 概念+计算混合
difficulty: 组合理论和CAPM是核心框架
note_type: master_moc
status: active
tags:
  - CFA_L1
  - MOC
  - Portfolio_Management
  - official_2026
---

# 📊 00-Portfolio-Management-MOC

> **一句话核心**：从分散化(σp²公式)到定价(CAPM)到执行(IPS)→风险预算。

---

## 📋 官方模块概览

| # | 内容 | ⚖️ | 🎯 必考点 | 🔗 |
|---|------|-----|-----------|-----|
| M01 | Risk & Return Part I | 计算 | 📐 组合方差、有效前沿、CAL、效用函数 | [[M01-Portfolio-Risk-and-Return-Part-I]] |
| M02 | Risk & Return Part II | 计算 | 📐 CAPM、Beta、SML、Sharpe/Treynor/α | [[M02-Portfolio-Risk-and-Return-Part-II]] |
| M03 | PM Overview | 概念 | 三阶段流程、集合投资工具 | [[M03-Portfolio-Management-An-Overview]] |
| M04 | Portfolio Planning & Construction | 概念 | IPS、资产配置、ESG | [[M04-Basics-of-Portfolio-Planning-and-Construction]] |
| M05 | Behavioral Biases | 概念 | 认知错误 vs 情感偏差 | [[M05-The-Behavioral-Biases-of-Individuals]] |
| M06 | Risk Management | 概念 | 五步骤、金融/非金融风险 | [[M06-Introduction-to-Risk-Management]] |

---

## 🌳 核心知识树

```text
📊 Portfolio Management (8-12%) (M01-M06) 知识体系

├─ 🏆 M01: Portfolio Risk and Return Part I（组合风险与收益）【高频计算】
│  ├─ ⭐ 1.1 组合期望收益与方差
│  │  ├─ 📐 E(Rp) = Σwi·E(Ri)（收益=加权平均）
│  │  └─ 📐 σp² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂Cov₁₂（两资产组合方差）
│  │     ⚠️ 不是加权平均方差！必须加协方差项
│  ├─ ⭐ 1.2 协方差与相关系数
│  │  ├─ 📐 Cov₁₂ = Σp(R₁-ER₁)(R₂-ER₂)
│  │  └─ 📐 ρ₁₂ = Cov₁₂/(σ₁σ₂)，范围[-1,+1]
│  │     🎯 ρ=-1→可构建无风险组合；ρ=+1→无分散化
│  ├─ ⭐ 1.3 效用函数与风险厌恶
│  │  ├─ 📐 U = E(Rp) - 0.5·A·σp²
│  │  └─ ⭐ A>0=风险厌恶；A=0=风险中性；A<0=风险偏好
│  ├─ ⭐ 1.4 资本配置线(CAL)
│  │  └─ 📐 E(Rc) = Rf + [(E(Rp)-Rf)/σp]·σc
│  ├─ ⭐ 1.5 有效前沿
│  │  └─ 🎯 最小方差组合 → 上半部分曲线
│  └─ ⚠️ 增加资产→非系统风险↓；系统风险不可消除
│
├─ 🏆 M02: Portfolio Risk and Return Part II（CAPM与绩效评估）【高频计算】
│  ├─ ⭐ 2.1 CAPM
│  │  └─ 📐 E(Ri) = Rf + βi[E(Rm)-Rf]
│  ├─ ⭐ 2.2 Beta系数
│  │  ├─ 📐 βi = Cov(Ri,Rm)/σm²
│  │  └─ β=1同步；β>1进攻；β<1防御；β<0反向（极少见）
│  ├─ ⭐ 2.3 证券市场线(SML)
│  │  ├─ 🎯 SML上方=低估=正α；SML下方=高估=负α
│  │  └─ ⚠️ CML横轴=σ（只含有效组合）；SML横轴=β（所有资产）
│  └─ ⭐ 2.4 绩效评估指标
│     ├─ 📐 Sharpe = (Rp-Rf)/σp（总风险→评价完整组合）
│     ├─ 📐 Treynor = (Rp-Rf)/βp（系统风险→分散化部分）
│     ├─ 📐 Jensen's α = Rp - [Rf+βp(E(Rm)-Rf)]
│     └─ ⚠️ 正α≠经理能力强：可能只是承担了额外风险
│
├─ 🏆 M03: Portfolio Management Overview（组合管理概述）
│  ├─ ⭐ 三阶段：规划(Planning)→执行(Execution)→反馈(Feedback)
│  ├─ ⭐ 集合投资工具
│  │  ├─ 开放式基金（按NAV交易）
│  │  ├─ 封闭式基金（按市价，可能折溢价）
│  │  └─ ETF（场内交易·税收高效·费用低）
│  └─ ⚠️ DB（雇主担风险）vs DC（员工担风险）
│
├─ 🏆 M04: Portfolio Planning and Construction（IPS与构建）
│  ├─ ⭐ IPS = 投资策略说明书（投资目标+约束条件）
│  ├─ ⭐ 风险态度：意愿(willingness) × 能力(ability)
│  └─ ⭐ 约束：流动性·时间·税务·法律·独特情况
│
├─ 🏆 M05: Behavioral Biases（行为偏差）
│  ├─ ⭐ 认知错误（可因教育改善）
│  │  └─ 锚定·过度自信·确认偏误·框架依赖
│  └─ ⭐ 情感偏差（难改正）
│     └─ 损失厌恶·后悔厌恶·禀赋效应
│
└─ 🏆 M06: Risk Management（风险管理）
   ├─ ⭐ 五步骤：治理→识别→计量→改变化→监控
   ├─ ⭐ 金融风险：市场·信用·流动性·操作
   ├─ ⭐ 非金融风险：法律·监管·税务·声誉
   └─ 🎯 改变化：回避·接受·转移·分散
```

---

## 🔗 跨模块依赖关系

```text
📊 学习顺序

M01（组合风险Part I）◄── Quant M05 Portfolio Math
└── M02（组合风险Part II）◄── Quant M07-M10 统计+回归
    ├── M03（PM概述）
    ├── M04（规划与构建）┐
    │                   ├── ◄── Ethics M03 III(C) Suitability
    │                   │   └── 跨科目FSA比率分析
    ├── M05（行为偏差）
    └── M06（风险管理）

🔗 跨科目关键接口：
  M01 CAL + M02 CML/SML ──► Quant M05 组合数学
  M02 CAPM ──► Quant M10 回归β估算
  M02 Jensen's α ──► Equity M08 估值-经理评估
  M04 IPS ──► Ethics M03 客户义务
  M05 行为偏差 ──► Equity M03 市场效率-行为金融
  M06 风险管理 ──► FI M14-M16 信用风险
```

---

## 🔑 核心对比专题

| 对比 | 🔑 区别 | 🎯 判断 |
|------|---------|---------|
| **CAL vs CML** | CAL=任意风险组合；CML=市场组合 | 市场组合→CML |
| **CML vs SML** | CML横轴σ；SML横轴β | β→SML，σ→CML |
| **Sharpe vs Treynor** | 总风险 vs 系统风险 | 全组合→Sharpe；子部分→Treynor |
| **DB vs DC** | 雇主担风险 vs 员工担风险 | |
| **认知 vs 情感偏差** | 可改善 vs 难改正 | |

---

## 📐 核心公式速查

| 公式 | 用途 | ⚠️ |
|------|------|-----|
| `E(Rp)=ΣwiE(Ri)` | 组合收益 | 加权平均 |
| `σp²=w₁²σ₁²+w₂²σ₂²+2w₁w₂Cov₁₂` | 组合方差 | 含协方差 |
| `βi=Cov(Ri,Rm)/σm²` | Beta | |
| `E(Ri)=Rf+βi[E(Rm)-Rf]` | CAPM | 系统风险定价 |
| `Sharpe=(Rp-Rf)/σp` | 总风险回报 | 评价全组合 |
| `α=Rp-[Rf+βp(E(Rm)-Rf)]` | Jensen's α | 超额收益 |

---

## 🚨 高频陷阱速查

| ❌ 错误 | ✅ 正确 | 🎯 |
|---------|---------|-----|
| 组合方差=加权平均方差 | 必须加协方差项 | ⭐⭐⭐ |
| CML上所有资产 | CML只含有效组合 | ⭐⭐⭐ |
| β不可能为负 | β可负（反向波动） | ⭐⭐ |
| α正=经理能力强 | 可能只是承担额外风险 | ⭐⭐ |
| 认知偏差=情感偏差 | 认知可改善，情感难改正 | ⭐⭐ |

---

## 💡 学习路径

```
阶段1 ─── M01→M02（组合数学+CAPM计算核心）
阶段2 ─── M04（IPS和构建）
阶段3 ─── M03→M05→M06（概念+偏差+风险管理）
```
