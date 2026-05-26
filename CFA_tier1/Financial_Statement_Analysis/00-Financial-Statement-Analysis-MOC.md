---
title: "00-Financial-Statement-Analysis-MOC"
description: "CFA L1 FSA 中枢 — 三表·比率·杜邦·递延税·报告质量·建模"
subject: "Financial Statement Analysis"
topic_area: Financial_Statement_Analysis
level: CFA Level I
exam_weight: "11-14%"
exam_format: 概念+计算混合
difficulty: 会计准则差异+比率计算，需大量练习
note_type: master_moc
status: active
tags:
  - CFA_L1
  - MOC
  - Financial_Statement_Analysis
  - official_2026
---

# 📚 00-Financial-Statement-Analysis-MOC

> **一句话核心**：三张报表+四种比率+杜邦分解+递延税+报告质量。M02-M05是计算核心。

---

## 📋 官方模块概览

| # | 内容 | ⚖️ | 🎯 必考点 | 🔗 |
|---|------|-----|-----------|-----|
| M01 | Introduction to FSA | 概念 | IFRS vs US GAAP、监管文件 | [[M01-Introduction-to-Financial-Statement-Analysis]] |
| M02 | Analyzing Income Statements | **计算** | 📐 收入确认、EPS、non-recurring | [[M02-Analyzing-Income-Statements]] |
| M03 | Analyzing Balance Sheets | **计算** | 无形资产、商誉、金融工具 | [[M03-Analyzing-Balance-Sheets]] |
| M04 | Cash Flows I | **计算** | 📐 直接/间接法、CFO/CFI/CFF | [[M04-Analyzing-Statements-of-Cash-Flows-I]] |
| M05 | Cash Flows II | **计算** | 📐 FCFF/FCFE、现金流比率 | [[M05-Analyzing-Statements-of-Cash-Flows-II]] |
| M06 | Analysis of Inventories | **计算** | FIFO/LIFO、通胀影响 | [[M06-Analysis-of-Inventories]] |
| M07 | Long-Term Assets | 计算 | 减值、处置 | [[M07-Analysis-of-Long-Term-Assets]] |
| M08 | Long-Term Liabilities & Equity | 计算 | 租赁、养老金、股权激励 | [[M08-Topics-in-Long-Term-Liabilities-and-Equity]] |
| M09 | Analysis of Income Taxes | **计算** | 📐 DTA/DTL、有效税率 | [[M09-Analysis-of-Income-Taxes]] |
| M10 | Financial Reporting Quality | 概念 | 激进vs保守、红旗信号 | [[M10-Financial-Reporting-Quality]] |
| M11 | Financial Analysis Techniques | **计算** | 📐 四大比率、DuPont分解 | [[M11-Financial-Analysis-Techniques]] |
| M12 | Financial Statement Modeling | 计算 | 预测模型、情景分析 | [[M12-Introduction-to-Financial-Statement-Modeling]] |

---

## 🌳 核心知识树

```text
📚 Financial Statement Analysis (11-14%) (M01-M12) 知识体系

├─ 🏆 M01: Introduction to FSA（分析框架）
│  └─ ⭐ IFRS vs US GAAP 主要差异、监管文件
│
├─ 🏆 M02: Analyzing Income Statements（损益表分析）【高频计算】
│  ├─ ⭐ 收入确认五步法（IFRS 15）
│  ├─ 📐 Basic EPS = (NI - Preferred Dividends) / Weighted Avg Shares
│  ├─ 📐 Diluted EPS（含可转债·期权·认股权证的稀释效应）
│  ├─ ⭐ Non-recurring items：Discontinued/I/U、会计政策变更
│  └─ ⚠️ 资本化vs费用化：资本化→当期NI↑但折旧↓未来NI
│
├─ 🏆 M03: Analyzing Balance Sheets（资产负债表分析）【计算】
│  ├─ ⭐ 无形资产：购买(capitalize) vs 内部自创(expense) vs 并购(公允价值)
│  ├─ ⭐ 商誉：不摊销·每年减值测试（⚠️ 减值不可转回）
│  └─ ⭐ 金融工具：FVTPL / FVTOCI / Amortized Cost
│
├─ 🏆 M04-M05: Cash Flow Statements（现金流量表）【高频计算】
│  ├─ 📐 CFO间接法 = NI + Depreciation - ΔAR + ΔAP - ΔInventory
│  ├─ 📐 FCFF = CFO + Interest×(1-t) - CapEx（公司自由现金流）
│  ├─ 📐 FCFE = CFO - CapEx + Net Borrowing（权益自由现金流）
│  └─ ⚠️ NI≠CFO！NI含非现金项目（折旧·摊销·递延税），需调整营运资本变动
│
├─ 🏆 M06: Analysis of Inventories（存货分析）【高频计算】
│  ├─ ⭐ FIFO：COGS低·NI高·存货高（通胀时）
│  ├─ ⭐ LIFO：COGS高·NI低·存货低（⚠️ IFRS不允用LIFO）
│  └─ 📐 LIFO Reserve = FIFO Inventory - LIFO Inventory（FIFO↔LIFO转换）
│
├─ 🏆 M07: Analysis of Long-Term Assets（长期资产）
│  ├─ ⭐ 减值：判断→比较账面vs回收额→确认/转回
│  └─ ⚠️ IFRS允许减值转回；US GAAP不允许（商誉也不允许）
│
├─ 🏆 M08: Long-Term Liabilities and Equity（长期负债与权益）【计算】
│  ├─ ⭐ 租赁：lessee→使用权资产(ROU)+租赁负债
│  └─ ⭐ 养老金：DC(缴款确定) vs DB(待遇确定)
│
├─ 🏆 M09: Analysis of Income Taxes（所得税分析）【高频计算】
│  ├─ 📐 DTL = 应纳税暂时性差异 × 税率（未来需多交税）
│  ├─ 📐 DTA = 可抵扣暂时性差异 × 税率（未来可少交税）
│  ├─ 🎯 永久性差异→不影响DTA/DTL（如罚款·招待费）
│  └─ ⚠️ DTL≠欠税！是未来才需交的税
│
├─ 🏆 M10: Financial Reporting Quality（报告质量）
│  ├─ ⭐ 激进vs保守会计的识别
│  └─ ⭐ 红旗信号(red flags)：收入提前确认·费用递延·关联交易
│
├─ 🏆 M11: Financial Analysis Techniques（财务分析技术）【高频计算】
│  ├─ ⭐ 四大比率
│  │  ├─ 流动性：Current / Quick / Cash Ratio
│  │  ├─ 营运：Inventory / Receivables / Payables Turnover
│  │  ├─ 偿债：D/E / Debt-to-Assets / ICR
│  │  └─ 盈利：Gross/Operating/Net Margin / ROA / ROE
│  └─ 📐 DuPont ROE = (NI/Rev)×(Rev/Assets)×(Assets/Equity)
│     🎯 三因子分解：净利率×资产周转率×财务杠杆
│
└─ 🏆 M12: Financial Statement Modeling（财务建模）
   └─ ⭐ 历史比率→预测假设→pro forma模型
```

---

## 🔗 跨模块依赖关系

```text
M01（FSA概览）
├── M02（损益）→ M10（报告质量）
├── M03（资产负债）→ M06（存货）→ M07（长期资产）→ M08（负债/权益）
│                                    └── M09（所得税）
├── M04-M05（现金流）→ M11（比率分析）
│                          └── M12（建模）
└── 所有模块 → Equity估值/FI信用分析/PM

🔗 跨科目关键接口：
  M02 EPS ──► Equity M08 估值市盈率
  M04 CFO ──► Corporate Issuers M04 营运资本
  M06 FIFO/LIFO ──► FI 债券分析与比率
  M08 租赁 ──► FI M08 长期负债
  M11 杜邦 ──► Equity M05 公司分析
```

---

## 📐 核心公式速查

| 公式 | 用途 | ⚠️ |
|------|------|-----|
| Basic EPS=(NI-PS Div)/WA Shares | 基本EPS | 优先股股利扣除 |
| CFO(indirect)=NI+Dep-ΔAR+ΔAP-ΔInv | 间接法CFO | |
| FCFF=CFO+Int(1-t)-CapEx | 公司自由现金流 | |
| DTL/(DTA)=暂差×税率 | 递延税 | 永久差异不影响 |
| DuPont=(NI/Rev)×(Rev/Assets)×(Assets/Equity) | ROE三因子 | |

## 🚨 高频陷阱速查

| ❌ 错误 | ✅ 正确 | 🎯 |
|---------|---------|-----|
| NI=CFO | CFO需调整非现金+营运资本 | ⭐⭐⭐ |
| LIFO下COGS更低 | 通胀时LIFO-COSS↑ NI↓ | ⭐⭐⭐ |
| 资本化=当期NI更高 | 是，但未来折旧降低后续NI | ⭐⭐⭐ |
| DTL=欠税 | DTL是未来才需交的税 | ⭐⭐ |
| 商誉可摊销 | 不摊销，每年减值测试 | ⭐⭐ |
| 稀释EPS>Basic | 稀释因子加入分母→更小 | ⭐⭐ |

---

## 💡 学习路径

```
阶段1（三表基础）：M01→M02→M03→M04→M05（损益表+资产负债表+现金流）
阶段2（专题+计算）：M06→M07→M08→M09（存货+资产+负债+税）
阶段3（分析+应用）：M11→M12→M10（比率/杜邦→建模→报告质量）
```
