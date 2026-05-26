---
title: "00-Equity-MOC"
description: "CFA Level I Equity 详细 MOC — 市场结构、指数、效率、估值模型、行业分析"
subject: "Equity Investments"
topic_area: Equity
level: CFA Level I
exam_weight: "11-14%"
exam_format: 概念+计算混合
difficulty: 前半概念（市场/指数/效率），后半计算（估值模型）
note_type: master_moc
status: active
tags:
  - CFA_L1
  - MOC
  - Equity
  - official_2026
---

# 00-Equity-MOC

## 官方模块概览

| 模块 | 内容 | 难度 | 必考点 | 文件 |
|------|------|------|--------|------|
| M01 | Market Organization & Structure | 概念 | 金融系统功能、交易指令类型、保证金 | [[M01-Market-Organization-and-Structure]] |
| M02 | Security Market Indexes | 概念+计算 | 指数构建方法、价格/总回报、加权方法 | [[M02-Security-Market-Indexes]] |
| M03 | Market Efficiency | 概念 | 三式有效、行为金融、市场异象 | [[M03-Market-Efficiency]] |
| M04 | Overview of Equity Securities | 概念 | 普通股/优先股特征、存托凭证 | [[M04-Overview-of-Equity-Securities]] |
| M05 | Company Analysis: Past & Present | 概念 | 商业模型分析、收入与盈利分析 | [[M05-Company-Analysis-Past-and-Present]] |
| M06 | Industry & Competitive Analysis | 概念 | Porter Five Forces、PESTLE | [[M06-Industry-and-Competitive-Analysis]] |
| M07 | Company Analysis: Forecasting | 概念 | 收入/费用预测、情景分析 | [[M07-Company-Analysis-Forecasting]] |
| M08 | Equity Valuation | 计算 | DDM、GGM、Multiples、EV、Asset-based | [[M08-Equity-Valuation-Concepts-and-Basic-Tools]] |

---

## 核心知识树

```text
📈 Equity (11-14%) (M01-M08) 知识体系

├─ 🏆 M01: Market Organization and Structure（市场组织）【高频考点】
│  ├─ ⭐ 金融系统四大功能：储蓄→投资·支付清算·风险管理·价发现
│  ├─ ⭐ 交易指令：市价单(立即成交) vs 限价单(指定价格)
│  ├─ 📐 保证金交易
│  │  ├─ 杠杆率 = 市值 / 自有资金
│  │  └─ 📐 Margin Call价 = P₀×(1-im)/(1-mm)
│  └─ ⭐ 做空：先借后卖·需支付股息·无限风险
│
├─ 🏆 M02: Security Market Indexes（指数）【计算】
│  ├─ ⭐ 加权方法
│  │  ├─ 价格加权：高价股影响大（DJIA）
│  │  ├─ 市值加权：大公司影响大（S&P 500）
│  │  ├─ 等权重：小公司影响放大
│  │  └─ 基本面加权：按财务指标加权
│  ├─ 📐 价格回报(Price Return) vs 总回报(Total Return含股息)
│  └─ 🎯 再平衡(Rebalancing) vs 重构(Reconstitution)不同
│
├─ 🏆 M03: Market Efficiency（市场效率）【高频概念】
│  ├─ ⭐ 三式有效假设
│  │  ├─ 弱式：技术分析无效（历史价已反映）
│  │  ├─ 半强式：基本面无效（公开信息已反映）
│  │  └─ 强式：内幕信息也无效（所有信息已反映）
│  ├─ ⭐ 市场异象：规模效应·价值效应·动量效应
│  └─ ⚠️ 行为偏差：过度反应·代表性偏误·锚定
│
├─ 🏆 M04: Overview of Equity Securities（权益证券）
│  ├─ ⭐ 普通股：投票权·剩余索偿权·无固定股息
│  ├─ ⭐ 优先股：固定股息·优先分配·无投票权
│  └─ ⭐ 存托凭证(DR)：ADR/GDR（非本土股投资方式）
│
├─ 🏆 M05-M07: 公司行业分析（概念为主）
│  ├─ M05: Company Analysis Past & Present（过去与现在）
│  ├─ M06: Industry & Competitive Analysis（行业竞争分析）
│  │  └─ Porter Five Forces + PESTLE
│  └─ M07: Company Analysis Forecasting（预测）
│
└─ 🏆 M08: Equity Valuation（权益估值）【高频计算】
   ├─ 📐 GGM: V₀ = D₁/(r-g)
   │  🎯 稳定增长公司；⚠️ g<r
   ├─ 📐 两阶段DDM: V₀ = ΣDt/(1+r)^t + Pn/(1+r)^n
   ├─ 📐 P/E multiple: V₀ = 可比P/E × 目标EPS
   ├─ 📐 EV/EBITDA：消除杠杆和折旧差异
   ├─ 📐 资产基础法：V = 资产公允价值 - 负债
   ├─ 📐 隐含回报率：r = D₁/P₀ + g（Gordon反转）
   └─ ⚠️ P/E低≠便宜——要考虑增长(PEG ratio)
```

## 关键公式

| 公式 | 用途 |
|------|------|
| Leverage Ratio = 市值/自有资金 | 保证金交易杠杆 |
| Margin Call Price = P₀ × (1-im)/(1-mm) | 追缴价格 |
| V₀ = D₁/(r-g) | GGM |
| r = D₁/P₀ + g | Gordon 隐含回报 |
| P/E = (1-b)/(r-g) | 基本面 P/E |
| EV = MV Equity + MV Debt - Cash | 企业价值 |
| V₀ = ΣDt/(1+r)^t + Pn/(1+r)^n | 两阶段 DDM |

## 🔑 核心对比专题

| 对比项 | 🔑 关键区别 | 🎯 考试判断 |
|--------|-------------|-------------|
| 价格加权 vs 市值加权 | 高价股影响大 vs 大公司影响大 | 看指数构成 |
| 弱/半强/强式有效 | 依次否定技术/基本面/内幕信息 | 哪类分析能获利？ |
| 普通股 vs 优先股 | 有投票权 vs 优先分配 | 固定股息→优先股 |
| GGM vs 两阶段DDM | 稳定增长 vs 先高增后稳 | 增长模式判断 |
| P/E vs EV/EBITDA | PE受杠杆影响；EV消除杠杆差异 | 资本结构差异大→EV |

## 📐 核心公式速查

| 公式 | 用途 | ⚠️ 注意 |
|------|------|---------|
| `Leverage = MV/Equity` | 杠杆率 | |
| `Margin Call = P₀×(1-im)/(1-mm)` | 追缴价 | 理解推导逻辑 |
| `V₀ = D₁/(r-g)` | GGM | ⚠️ 要求g<r |
| `r = D₁/P₀ + g` | 隐含回报率 | |
| `P/E = (1-b)/(r-g)` | 基本面P/E | 与增长相关 |
| `EV = MV Equity + MV Debt - Cash` | 企业价值 | |

## 🚨 高频陷阱速查

| ❌ 错误理解 | ✅ 正确理解 | 🎯 考频 |
|-------------|-------------|---------|
| 弱式有效=市场完全无效 | 仅反映历史价格 | ⭐⭐⭐ |
| 价格回报=总回报 | 总回报含股息再投资 | ⭐⭐ |
| P/E越低越便宜 | 要考虑增长(PEG) | ⭐⭐⭐ |
| GGM适用所有公司 | 要求g<r且稳定增长 | ⭐⭐⭐ |
| 技术分析有效市场也能用 | 弱式以上无效 | ⭐⭐ |

## 🔗 跨模块关联

```text
M01（市场基础）
├── M02（指数）──► M03（效率）
├── M04（权益类型）──► M08（估值核心）
└── M05-M07（公司/行业分析）←── FSA比率

🔗 跨科目：
  M08 GGM r=D₁/P₀+g ──► Quant M02 TVM
  M01 保证金 ──► FI M04 回购市场
  M03 行为金融 ──► PM M05 行为偏差
  M08 估值倍数 ──► FSA M11 比率分析
```

## 🗺️ 学习路径

```
阶段1 ─── M01→M02→M03（市场基础+指数+效率概念）
阶段2 ─── M04→M05→M06→M07（权益+公司/行业分析）
阶段3 ─── M08（估值计算：DDM/GGM/倍数）
```
