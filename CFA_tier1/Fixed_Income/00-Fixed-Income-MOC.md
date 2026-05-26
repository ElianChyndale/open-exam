---
title: "00-Fixed-Income-MOC"
description: "CFA L1 Fixed Income 中枢 — 19模块·知识树·公式·陷阱·跨模关联"
subject: "Fixed Income"
topic_area: Fixed_Income
level: CFA Level I
exam_weight: "11-14%"
exam_format: 概念+计算混合
difficulty: 前半概念多（工具/市场），后半公式密集（估值/风险/信用）
note_type: master_moc
status: active
tags:
  - CFA_L1
  - MOC
  - Fixed_Income
  - official_2026
---

# 📈 00-Fixed-Income-MOC

> **一句话核心**：工具特征→市场结构→估值定价→风险度量→信用分析→证券化。M06-M13 是计算核心。

---

## 📋 官方模块概览

| # | 内容 | ⚖️ 难度 | 🎯 必考点 | 🔗 |
|---|------|----------|-----------|-----|
| M01 | Instrument Features | 概念 | indenture, covenants | [[M01-Fixed-Income-Instrument-Features]] |
| M02 | Cash Flows and Types | 概念 | 现金流结构、或有条款 | [[M02-Fixed-Income-Cash-Flows-and-Types]] |
| M03 | Issuance and Trading | 概念 | 一级/二级、FI指数 | [[M03-Fixed-Income-Issuance-and-Trading]] |
| M04 | Markets for Corp Issuers | 概念 | 回购、CP、IG vs HY | [[M04-Fixed-Income-Markets-for-Corporate-Issuers]] |
| M05 | Markets for Govt Issuers | 概念 | 主权债、TIPS | [[M05-Fixed-Income-Markets-for-Government-Issuers]] |
| M06 | Bond Valuation: Prices & Yields | 计算 | 定价公式、AI、matrix pricing | [[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]] |
| M07 | Yield & Spread (Fixed-Rate) | 计算 | YTM、G/I/Z-spread | [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] |
| M08 | Yield & Spread (Floating-Rate) | 计算 | FRN、QM/DM、货币市场收益率 | [[M08-Yield-and-Yield-Spread-Measures-for-Floating-Rate-Instruments]] |
| M09 | Term Structure | 计算 | spot/par/forward curve | [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] |
| M10 | Interest Rate Risk & Return | 计算 | Macaulay duration, horizon yield | [[M10-Interest-Rate-Risk-and-Return]] |
| M11 | Duration Measures | 计算 | ModDur, money duration, PVBP | [[M11-Yield-Based-Bond-Duration-Measures-and-Properties]] |
| M12 | Convexity | 计算 | convexity adjustment | [[M12-Yield-Based-Bond-Convexity-and-Portfolio-Properties]] |
| M13 | Curve-Based Risk | 计算 | EffDur, key rate dur, empirical dur | [[M13-Curve-Based-and-Empirical-Fixed-Income-Risk-Measures]] |
| M14 | Credit Risk | 概念 | PD/LGD、信用评级、利差 | [[M14-Credit-Risk]] |
| M15 | Govt Credit Analysis | 概念 | 主权信评维度 | [[M15-Credit-Analysis-for-Government-Issuers]] |
| M16 | Corp Credit Analysis | 计算 | ICR、杠杆率、优先级 | [[M16-Credit-Analysis-for-Corporate-Issuers]] |
| M17 | Securitization | 概念 | SPV、信用增级 | [[M17-Fixed-Income-Securitization]] |
| M18 | ABS | 概念 | covered bonds, CDO | [[M18-Asset-Backed-Security-Instrument-and-Market-Features]] |
| M19 | MBS | 概念 | RMBS, CMBS, prepayment | [[M19-Mortgage-Backed-Security-Instrument-and-Market-Features]] |

---

## 🌳 核心知识树

```text
📈 Fixed Income (11-14%) (M01-M19) 学习路径

├─ 🏆 M01-M05: FI基础工具与市场（概念为主）
│  │
│  ├─ 🏆 M01: Fixed-Income Instrument Features（债券要素）
│  │  ├─ ⭐ 1.1 债券基本要素：面值·票息·到期日·收益率
│  │  └─ ⭐ 1.2 契约条款
│  │     ├─ Affirmative covenants：必须做的事（按时付息）
│  │     └─ Negative covenants：禁止做的事（限制再融资）
│  │
│  ├─ 🏆 M02: Cash Flows and Types（现金流与类型）
│  │  ├─ ⭐ 2.1 现金流结构
│  │  │  ├─ 固定利率：已知每期票息金额
│  │  │  ├─ 浮动利率：票息 = 参考利率 + 利差
│  │  │  └─ 通胀挂钩：本金随CPI调整
│  │  └─ ⭐ 2.2 或有条款
│  │     ├─ Callable（可赎回）：issuer有权提前赎回→对发行人有利
│  │     ├─ Putable（可回售）：investor有权提前卖回→对投资者有利
│  │     └─ Convertible（可转换）：可换成一定数量的普通股
│  │
│  ├─ 🏆 M03: Fixed-Income Issuance and Trading（发行与交易）
│  │  └─ ⭐ 一级市场（新发）vs 二级市场（交易）、FI指数
│  │
│  ├─ 🏆 M04: Markets for Corporate Issuers（公司发行人市场）
│  │  ├─ ⭐ 短期融资：CP（商业票据）、Repo（回购）
│  │  └─ ⭐ IG（投资级）vs HY（高收益/垃圾债）区分
│  │
│  └─ 🏆 M05: Markets for Government Issuers（政府发行人市场）
│     ├─ ⭐ 主权债（国债）、TIPS（通胀保护债券）
│     └─ ⭐ 非主权债：市政债、超国家机构债
│
├─ 🏆 M06-M13: 估值、收益与风险（计算核心，占70%考题）
│  │
│  ├─ 🏆 M06: Bond Valuation（债券定价）【高频计算】
│  │  ├─ 📐 P = ΣC/(1+y/m)^t + FV/(1+y/m)^N（债券定价公式）
│  │  ├─ 📐 Full Price = Clean Price + Accrued Interest
│  │  ├─ 🎯 溢价/平价/折价判断：C > YTM → 溢价(premium)；C < YTM → 折价(discount)
│  │  ├─ ⚠️ Clean price是报价，Full price是实际结算价！两者差一个AI
│  │  └─ ⭐ Matrix pricing：用可比债券YTM估算非活跃债券价格
│  │
│  ├─ 🏆 M07: Yield Measures for Fixed-Rate Bonds（固定利率收益率）【高频计算】
│  │  ├─ 📐 YTM = 债券定价公式的反算（IRR of cash flows）
│  │  ├─ 📐 Current Yield = Annual Coupon / Bond Price
│  │  ├─ 📐 G-spread = YTM_bond - YTM_govt（国债基准）
│  │  ├─ 📐 I-spread = YTM_bond - Swap Rate（互换基准）
│  │  ├─ 🎯 Periodicity转换：(1+y/m)^m = (1+y/n)^n
│  │  └─ ⚠️ YTM隐含再投资假设——实际回报可能≠YTM
│  │
│  ├─ 🏆 M08: Yield Measures for Floating-Rate Instruments（浮动利率）【计算】
│  │  ├─ 📐 FRN定价：Coupon = Reference + QM（报价利差）
│  │  └─ 📐 DM（贴现利差）= 用当前信用风险折现后的FRN利差
│  │
│  ├─ 🏆 M09: Term Structure（期限结构）【计算】
│  │  ├─ 📐 Spot curve：零息债券即期收益率曲线
│  │  ├─ 📐 Par curve：平价债券的票息率曲线
│  │  ├─ 📐 Forward rate：隐含远期利率
│  │  ├─ 📐 spot→forward: f(j,k) = [(1+zj+k)^(j+k)/(1+zj)^j]^(1/k)-1
│  │  └─ 🎯 Spot / Par / Forward 三者互推（核心技能）
│  │
│  ├─ 🏆 M10: Interest Rate Risk and Return（利率风险）【高频计算】
│  │  ├─ 📐 Macaulay Duration = Σt·PVCFt / ΣPVCFt（加权平均回收期）
│  │  ├─ 🎯 持有期回报 = coupon reinvestment + price change
│  │  └─ ⚠️ 免疫策略：Macaulay duration ≈ 投资期
│  │
│  ├─ 🏆 M11: Yield-Based Duration（久期度量）【高频计算】
│  │  ├─ 📐 Modified Duration = MacDur / (1+y/m)
│  │  ├─ 📐 Money Duration = ModDur × Full Price
│  │  ├─ 📐 PVBP ≈ Money Duration × 0.0001（1bp的价格变化）
│  │  ├─ 🎯 久期性质：期限↑票息↓YTM↓ → 久期↑
│  │  └─ ⚠️ 久期只对微小Δy有效
│  │
│  ├─ 🏆 M12: Convexity（凸性）【高频计算】
│  │  ├─ 📐 Convexity = (P₋ + P₊ - 2P₀) / (P₀ × (Δy)²)
│  │  ├─ 📐 %ΔP ≈ -ModDur·Δy + 0.5·Convexity·(Δy)²（含凸性更精确）
│  │  ├─ ⭐ 正凸性：利率↓时涨幅>利率↑时跌幅（对投资者有利）
│  │  └─ ⚠️ 负凸性：可赎回债和MBS——利率↓时价格涨不动
│  │
│  └─ 🏆 M13: Curve-Based Risk（曲线风险）【计算】
│     ├─ 📐 Effective Duration（含期权债券用）
│     ├─ 📐 Key Rate Duration（非平行移动用）
│     └─ ⭐ Empirical vs Analytical Duration
│
├─ 🏆 M14-M16: 信用分析
│  │
│  ├─ 🏆 M14: Credit Risk（信用风险基础）
│  │  ├─ ⭐ PD（违约概率）+ LGD（违约损失率）= 预期损失
│  │  ├─ ⭐ 信用利差驱动因素：宏观/市场/发行人
│  │  └─ ⭐ 信用评级：投资级 vs 投机级
│  │
│  ├─ 🏆 M15: Government Credit Analysis（政府信用）
│  │  └─ ⭐ 四个维度：货币主权·财政灵活性·外部头寸·政治风险
│  │
│  └─ 🏆 M16: Corporate Credit Analysis（公司信用）【计算】
│     ├─ ⭐ 三支柱：商业风险 + 财务风险 + 治理结构
│     ├─ 📐 ICR = EBIT / Interest Expense（利息覆盖率）
│     │  ⚠️ ICR用EBIT vs EBITDA差别大！EBITDA更大→ICR更高
│     ├─ 📐 Leverage = Debt / EBITDA（杠杆率）
│     ├─ 🎯 债务优先顺序：Secured > Senior Unsecured > Subordinated
│     └─ ⚠️ 发行人评级≠债项评级（不同债项因担保/优先级可不同）
│
└─ 🏆 M17-M19: 证券化（概念为主）
   │
   ├─ 🏆 M17: Securitization（证券化流程）
   │  ├─ ⭐ SPV隔离风险（bankruptcy remote）
   │  ├─ ⭐ 信用增级（内/外部）
   │  └─ 🎯 对发行人：融资成本↓；对投资者：更高收益
   │
   ├─ 🏆 M18: Asset-Backed Securities（资产支持证券）
   │  ├─ ⭐ Covered bonds vs ABS
   │  ├─ ⭐ CDO结构：高级/夹层/次级
   │  └─ 🎯 信用增级方式：超额担保·储备金·劣后级
   │
   └─ 🏆 M19: Mortgage-Backed Securities（住房抵押贷款证券）
      ├─ ⭐ RMBS：按揭池→过手证券→CMO分层
      ├─ ⭐ Prepayment risk（提前还款风险）→ 负凸性
      └─ ⭐ CMBS：call protection更强
```

---

## 🔗 跨模块依赖关系

```text
📈 学习顺序

M01-M05（基础）→ 建理解
         │
         └──► M06-M09（估值+收益）←── Quant M02 TVM（折现）
                │
                ├──► M10-M13（风险度量）📐 公式核心
                │      └──► PM 风险预算概念
                │
                └──► M14-M16（信用分析）
                       └──► Corp Issuers M05-M06（资本结构）

🔗 跨科目关键接口：
  M06 债券定价 ──► Quant M02 TVM
  M08 FRN ──► Econ M07-M08 利率与汇率
  M10-M13 久期/凸性 ──► Portfolio Management M01 风险度量
  M14-M16 信用分析 ──► Corporate Issuers M05-M06 资本结构
  M17-M19 证券化 ──► Alternative Investments 结构化产品
```

---

## 🔑 核心对比专题

| 对比项 | 🔑 关键区别 | 🎯 考试判断 |
|--------|-------------|-------------|
| **固定 vs 浮动利率** | 已知现金流 vs 票息随参考利率变 | 看到reference rate→浮动 |
| **溢价 vs 折价** | C>YTM=溢价；C<YTM=折价 | 比较coupon vs YTM |
| **G-spread vs I-spread** | G=国债基准；I=互换基准 | 题目给什么基准 |
| **Mac vs Mod Duration** | Mac=加权回收期；Mod=%ΔP敏感度 | 价格变化→ModDur |
| **修正 vs 有效久期** | 修正假设固定现金流；有效允许含期权 | 可赎回债→有效 |
| **正凸性 vs 负凸性** | 利率↓时价格涨幅>跌幅；反之 | MBS/可赎回→负凸 |
| **平行 vs 非平行移动** | Duration=平行；Key rate=非平行 | 曲线斜率变化→KR |

---

## 📐 核心公式速查

| 指标 | 📐 公式 | ⚠️ 注意 |
|------|---------|---------|
| Bond Price | `P=ΣC/(1+y/m)^t+FV/(1+y/m)^N` | 基础定价 |
| Full Price | `Clean + Accrued Interest` | 结算价 |
| AI | `Coupon×(days since coupon/days in period)` | day-count |
| Mod Duration | `MacDur/(1+y/m)` | 价格%变化 |
| Money Duration | `ModDur×FullPrice` | 货币变化 |
| PVBP | `≈MoneyDur×0.0001` | 1bp |
| %ΔP含凸性 | `-ModDur·Δy+0.5·Conv·(Δy)²` | 组合公式 |
| Eff Duration | `(P₋-P₊)/(2·P₀·Δy)` | 含期权债券 |
| ICR | `EBIT/Interest` | 偿债能力 |
| Leverage | `Debt/EBITDA` | 杠杆水平 |

---

## 🚨 高频陷阱速查

| ❌ 错误 | ✅ 正确 | 🎯 考频 |
|---------|---------|---------|
| Clean price=实际支付 | 实际付full price=clean+AI | ⭐⭐⭐ |
| YTM=持有期回报 | YTM需满足再投资假设 | ⭐⭐⭐ |
| 凸性总是正 | 可赎回/MBS有负凸区 | ⭐⭐ |
| 久期可用于含期权债 | 含期权→effective duration | ⭐⭐⭐ |
| 发行人评级=债项评级 | 因担保/优先级可不同 | ⭐⭐ |
| 证券化消除风险 | 仅转移，不消除 | ⭐⭐ |

---

## 💡 通用分析框架

### 🎯 FI 估值三步法
```
Step 1 ─── 确定现金流（固定/浮动/通胀挂钩）
Step 2 ─── 选贴现率（YTM/spot/forward）
Step 3 ─── 计算 full price → 减 AI → clean price
```

### 🎯 利率风险度量选择
```
不含期权 ──→ ModDur + Convexity
含期权 ───→ EffDur + EffConvexity
非平行变动 ──→ Key rate duration
```

## 🗺️ 学习路径

```
阶段1（概念）：M01→M02→M03→M04→M05（重点理解工具特征）
阶段2（计算核心）：M06→M07→M08→M09→M10→M11→M12→M13（公式+计算）
阶段3（信用+证券化）：M14→M15→M16→M17→M18→M19
```
