---
title: "M05 — Capital Investments and Capital Allocation"
description: "CFA Level I 2026 official module: Capital Investments and Capital Allocation"
module: M05
subject: "Corporate Issuers"
topic_area: Corporate_Issuers
curriculum_year: 2026
official_module: "Module 5: Capital Investments and Capital Allocation"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Corporate_Issuers
  - official_2026
---

# M05: Capital Investments and Capital Allocation

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Capital Investments and Capital Allocation
- 5.01 | Introduction
- 5.02 | Capital Investments
- 5.03 | Capital Allocation
- 5.04 | Capital Allocation Principles and Pitfalls
- 5.05 | Real Options

## Learning Outcome Statements

The candidate should be able to:

- describe types of capital investments
- describe the capital allocation process, calculate net present value (NPV), internal rate of return (IRR), and return on invested capital (ROIC), and contrast their use in capital allocation
- describe principles of capital allocation and common capital allocation pitfalls
- describe types of real options relevant to capital investments

## Local Study Notes

### Migrated from `CFA_tier1/Corporate_Issuers/M04-Capital-Investments.md`

_Alignment score: 1.00. Original official module field: Module 5: Capital Investments and Capital Allocation._

#### M05: Capital Investments（资本投资决策）

### 🌳 核心知识树

```text
🏆 Corp M05: Capital Investments（资本投资决策）
│
├── ⭐ 现金流纪律 (Cash-Flow Discipline)
│   ├── 使用增量税后现金流 — 只考虑项目带来的额外现金流
│   ├── 忽略沉没成本 — 已发生不可收回的成本与决策无关
│   ├── 包含机会成本 — 放弃的最佳替代用途的价值
│   ├── 考虑蚕食效应 — 新项目侵蚀现有产品的销售
│   ├── 包含营运资本变动 — 存货和应收投资的增减
│   └── 考虑残值与税务影响 — 项目结束时的净现金流
│
├── ⭐ 决策标准
│   ├── 📐 NPV = Σ CFt/(1+r)^t — Initial Outlay（最可靠标准）
│   ├── 📐 IRR: 0 = Σ CFt/(1+IRR)^t — Initial Outlay
│   ├── 📐 PI = PV inflows / Initial investment
│   ├── 回收期: 累计现金流 ≥ 0（忽略时间价值）
│   └── 折现回收期: 累计折现现金流 ≥ 0
│
├── ⭐ NPV vs IRR
│   ├── 互斥项目规模/时间不同时，IRR 可能错误排序
│   ├── ⚠️ NPV 优先于 IRR — 反映绝对财富增加量
│   └── 📐 NPV 假设资本成本再投资；IRR 假设 IRR 再投资
│
├── ⭐ 项目类型
│   ├── 独立项目: 接受或拒绝互不影响
│   ├── 互斥项目: 只能选其一
│   └── 资本约束: 资金有限，按 PI 排序择优
│
├── ⭐ 实物期权 (Real Options)
│   ├── 时机期权: 延迟投资等待更有利条件
│   ├── 扩张期权: 成功后追加投资
│   ├── 放弃期权: 失败时退出减少损失
│   └── 灵活性期权: 调整产出/投入/生产方式
│
├── 💡 关键洞察
│   ├── 实物期权增大了项目 NPV
│   ├── 融资成本不应重复计算（已反映在折现率中）
│   ├── 回收期短 ≠ 项目好
│   └── NPV 的再投资率假设比 IRR 更合理
│
└── ⚠️ 考试陷阱总结
    ├── 非常规现金流下 IRR 可能误导（多个或无 IRR）
    ├── 回收期忽略时间价值和后期现金流
    ├── NPV 优于 IRR（互斥项目时）
    └── 沉没成本与项目决策无关
```

## 📖 知识点详解

### 知识点1：现金流纪律 (Cash-Flow Discipline)

**核心概念**：资本预算的核心是识别和评估能增加股东价值的投资机会。最关键的原则是使用增量税后现金流，忽略沉没成本，包含机会成本和外部性（蚕食效应）。

- **使用增量现金流 (Incremental Cash Flows)**：只考虑项目本身带来的额外现金流
- **忽略沉没成本 (Sunk Costs)**：已发生的不可收回成本与未来决策无关
- **包含机会成本 (Opportunity Costs)**：资产用于新项目时放弃的最佳替代用途的价值
- **考虑蚕食效应 (Cannibalization)**：新项目侵蚀现有产品销售的部分应计入
- **包含营运资本变动 (Working Capital Changes)**：项目通常需要额外营运资本投资
- 💡 融资成本不应重复计算——折现率已反映融资成本，现金流中不再包含利息

**考试应用**：给定一系列成本项目，判断哪些应计入现金流。关键：排除沉没成本，包含机会成本和营运资本变动。

### 知识点2：决策标准 (Decision Criteria)

**核心概念**：NPV是最可靠的决策标准——NPV > 0 创造价值。IRR虽然直观但在非常规现金流和互斥项目时可能错误。PI适用于资本约束下的项目排序。回收期和折现回收期作为辅助指标。

- **NPV (净现值)**：NPV = Σ CFt/(1+r)^t - Initial Outlay。NPV > 0 接受。互斥项目中首选 NPV
- **IRR (内部收益率)**：0 = Σ CFt/(1+IRR)^t - Initial Outlay。IRR > 资本成本则接受。非常规现金流可能多解或无解
- **PI (盈利指数)**：PI = PV of future inflows / Initial investment。PI > 1 接受。适用于资本约束排序
- **回收期 (Payback)**：累计未折现现金流收回初始投资的时间。不反映价值创造，忽略时间价值和后期现金流
- 💡 NPV优先于IRR（互斥项目时IRR可能错误排序）。NPV假设以资本成本再投资，IRR假设以IRR再投资

**考试应用**：NPV/IRR/PI计算是必考题型。NPV vs IRR冲突时以NPV为准。互斥项目注意规模和时间差异。资本约束时用PI排序。

### 知识点3：实物期权 (Real Options)

**核心概念**：传统NPV假设项目决策不可逆，但现实中管理层有灵活性。实物期权增大了项目的NPV，因为管理层可以在有利时行动、不利时止损。

- **时机期权 (Timing Option)**：延迟投资等待更有利条件
- **扩张期权 (Expansion Option)**：项目成功后可追加投资
- **放弃期权 (Abandonment Option)**：项目失败时可退出减少损失
- **灵活性期权 (Flexibility Option)**：调整产出、投入或生产方式
- 💡 实物期权 = 管理灵活性价值。传统NPV低估了包含灵活性的项目价值

**考试应用**：给定项目情景，判断包含哪种实物期权。理解实物期权增加项目价值（NPV传统方法低估了有灵活性的项目）。

### 📐 关键公式表

| 指标 | 公式 | 说明 |
|------|------|------|
| 净现值 (NPV) | `NPV = Σ CFt/(1+r)^t - Initial Outlay` | 价值创造的绝对度量 |
| 内部收益率 (IRR) | `0 = Σ CFt/(1+IRR)^t - Initial Outlay` | 项目本身的收益率 |
| 盈利指数 (PI) | `PI = PV of future cash inflows / Initial investment` | 单位投资创造的现值 |
| 回收期 | 累计现金流 ≥ 0 的时间点 | 流动性指标 |
| 折现回收期 | 累计折现现金流 ≥ 0 的时间点 | 流动性指标 |

### 🛠️ 常见考点与解题思路

**考点1：NPV 计算**
- 逐期折现后加总，减去初始投资。注意时间轴从 t=0 开始。

**考点2：NPV vs IRR 冲突**
- 互斥项目规模或时间不同时，**NPV 优先于 IRR**。

**考点3：识别应计入的现金流**
- 排除沉没成本，包含机会成本、营运资本变动、残值等。

**考点4：资本约束下的项目选择**
- 用 PI 排序，在资本限额内依次选择 PI 最高的项目。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| 融资成本应计入项目现金流 | 折现率已反映融资成本，不应重复计算 |
| IRR 总是可靠的标准 | 非常规现金流下可能有多个或无 IRR |
| 回收期短 = 项目好 | 回收期忽略时间价值和后期现金流 |
| NPV 和 IRR 再投资率假设相同 | NPV 假设资本成本；IRR 假设 IRR 本身 |

### 🔄 跨模块关联

- 折现率 → [[M05-Cost-of-Capital]] WACC 是资本预算中最常用的折现率
- 项目风险调整 → [[M05-Cost-of-Capital]] 风险不同的项目应使用不同折现率
- 经营杠杆影响项目风险 → [[M06-Capital-Structure-and-Leverage]]
- 实物期权概念 → [[M07-Business-Models]]
- 资本配置整合 → [[M08-Capital-Allocation-Integration]]

### Migrated from `CFA_tier1/Corporate_Issuers/M05-Cost-of-Capital.md`

_Alignment score: 1.00. Original official module field: Module 5: Capital Investments and Capital Allocation._

#### M06: Cost of Capital（资本成本）

### 🌳 核心知识树

```text
🏆 Corp M06: Cost of Capital（资本成本）
│
├── ⭐ 债务成本 (Cost of Debt, rd)
│   ├── 📐 税后债务成本 = rd × (1 - T)
│   ├── 利息可税前扣除 → 税盾效应
│   └── 可用债券 YTM 作为税前债务成本
│
├── ⭐ 优先股成本 (Cost of Preferred Stock, rp)
│   ├── 📐 rp = Dp / Pp（永续年金公式）
│   ├── 股息固定且优先于普通股
│   └── 股息通常不可税前扣除
│
├── ⭐ 普通股成本 (Cost of Common Equity, re)
│   ├── 📐 CAPM: re = rf + β × [E(Rm) - rf]（最常用）
│   ├── 📐 DGM: re = D1/P0 + g（稳定派息公司）
│   └── 📐 Bond Yield + Risk Premium: re = rd + RP
│
├── ⭐ WACC 构建
│   ├── 📐 WACC = wd × rd(1-T) + wp × rp + we × re
│   ├── 使用市场价值权重，非账面价值
│   ├── 使用目标权重（如有明确目标资本结构）
│   └── ⚠️ WACC 不能作为所有项目的通用折现率
│
├── ⭐ 边际资本成本 (MCC)
│   ├── 每多筹集一元新资本的成本
│   ├── 融资额超阈值 → MCC 上升
│   └── WACC 不是固定不变的
│
├── ⭐ 发行费用 (Flotation Costs)
│   ├── 承销费、法律费用等
│   └── ⚠️ 应作为初始现金流出，而非调整 WACC
│
├── 💡 关键洞察
│   ├── 债务成本必须用税后 — 忘记 ×(1-T) 是最常见失误
│   ├── 市场权重 > 账面权重
│   ├── 项目风险应与折现率匹配
│   └── β 衡量系统性风险，非总风险
│
└── ⚠️ 考试陷阱总结
    ├── 债务成本必须用税后 (1-T)
    ├── 优先使用市场价值权重
    ├── 发行费用调现金流，不调 WACC
    └── CAPM 中用市场风险溢价 (rm - rf)，不是 rm 本身
```

## 📖 知识点详解

### 知识点1：资本成本要素 (Component Costs of Capital)

**核心概念**：资本成本是公司为融资支付的必要回报率，也是投资者提供资金所要求的回报。不同来源的资本成本不同，债务有税盾效应，股权成本通过CAPM、股息增长模型或债券收益率加风险溢价法估算。

- **债务成本 (Cost of Debt, rd)**：税后债务成本 = rd × (1-T)。利息可税前扣除（税盾效应），因此税后成本低于税前成本
- **优先股成本 (Cost of Preferred Stock, rp)**：rp = Dp / Pp。优先股股息固定且不可税前扣除（除非特定结构），不调整税
- **普通股成本 (Cost of Common Equity, re)**：三种估算方法——CAPM法（最常用）、股息增长模型(DGM)、债券收益率加风险溢价法
- 💡 债务成本必须用税后！乘以 (1-T) 是必做步骤，忘记调整是最常见的失误

**考试应用**：WACC计算是必考题型。注意：债务成本用税后（×(1-T)），优先股成本不调税，股权成本首选CAPM。权重使用市场价值而非账面价值。

### 知识点2：WACC构建 (WACC Construction)

**核心概念**：WACC是公司整体融资成本的加权平均 = wd×rd(1-T) + wp×rp + we×re。权重必须使用市场价值且尽量使用目标权重。公司的WACC不能作为所有项目的通用折现率。

- **权重选择**：必须使用市场价值权重（market-value weights），而非账面价值权重
- **目标权重 (Target Weights)**：如果公司有明确的长期目标资本结构，应使用目标权重
- **边际资本成本 (MCC)**：每多筹集一元新资本的成本。当融资额超过阈值时MCC上升
- ⚠️ **重要**：公司的WACC不能作为所有项目的通用折现率。项目风险与公司整体风险不同时，应使用项目特定折现率

**考试应用**：WACC计算步骤：① 计算各要素成本；② 确定市场价值权重；③ 加权平均。常见陷阱：用账面权重、忘记债务税后调整、发行费用调WACC（应调现金流）。

### 知识点3：发行费用 (Flotation Costs)

**核心概念**：发行新股或债券会产生承销费、法律费用等摩擦成本。在资本预算中，发行费用应作为项目初始现金流出处理，而非调整WACC。

- 发行费用减少公司实际收到的融资净额
- 正确的处理方式：作为项目初始现金流出，增加初始投资额
- 不正确的处理方式：调整WACC中的资本要素成本（会导致WACC整体偏高）
- 💡 **关键区分**：发行费用调现金流，不调WACC

**考试应用**：给定发行费用数据，要求正确处理。常见陷阱：错误地将发行费用并入WACC调整。

### 📐 关键公式表

| 指标 | 公式 | 应用场景 |
|------|------|----------|
| 税后债务成本 | `rd(1-T)` | 债务要素成本 |
| 优先股成本 | `Dp/Pp` | 优先股要素成本 |
| CAPM 股权成本 | `rf + β × [E(Rm) - rf]` | 最常用的股权成本 |
| 股息增长模型 | `D1/P0 + g` | 稳定派息公司 |
| WACC | `wd×rd(1-T) + wp×rp + we×re` | 公司整体资本成本 |
| MCC | 突破点后的加权成本 | 融资额超阈值时 WACC 上升 |

### 🛠️ 常见考点与解题思路

**考点1：计算 WACC**
- 先算税后债务成本，再按市场价值权重加权平均。

**考点2：选择正确的权重**
- **market-value weights** 优先于 book-value weights。

**考点3：CAPM 计算股权成本**
- `re = rf + β(rm - rf)`。注意是市场风险溢价，不是 rm 本身。

**考点4：判断折现率是否合适**
- 项目风险应与折现率匹配，高风险项目用更高折现率。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| 债务成本用税前利率 | 债务成本必须 ×(1-T)，用税后 |
| 使用账面价值权重 | 考试优先使用市场价值权重 |
| 发行费用应调整 WACC | 发行费用作为初始现金流出 |
| WACC 对所有项目都适用 | 项目风险不同，折现率应不同 |
| β 衡量总风险 | β 衡量系统性风险 |

### 🔄 跨模块关联

- WACC 作为折现率 → [[M04-Capital-Investments]] NPV 计算核心输入
- 资本结构权重 → [[M06-Capital-Structure-and-Leverage]] 债务比例影响 WACC
- 杠杆影响 β → [[M06-Capital-Structure-and-Leverage]] 财务杠杆放大股权 β
- 融资政策影响成本 → [[M03-Working-Capital-and-Liquidity]]
- 资本成本整合 → [[M08-Capital-Allocation-Integration]]

### Migrated from `CFA_tier1/Corporate_Issuers/M08-Capital-Allocation-Integration.md`

_Alignment score: 1.00. Original official module field: Module 5: Capital Investments and Capital Allocation._

#### M09: Capital Allocation Integration（资本配置整合）

### 🌳 核心知识树

```text
🏆 Corp M09: Capital Allocation Integration（资本配置整合）
│
├── ⭐ 资本配置主线逻辑
│   ├── 治理 → 谁决策？激励是否对齐？
│   ├── 营运资本 → 维持流动性，释放现金
│   ├── 资本预算 → 选择增值项目 (NPV > 0)
│   ├── 资本成本 → 设定风险匹配的折现率
│   ├── 资本结构 → 选择最优融资方式
│   └── 商业模式 → 收入与成本结构决定约束
│
├── ⭐ 各环节具体作用
│   ├── 治理: 确保决策者有能力且激励对齐
│   ├── 营运资本: 释放现金支持长期投资
│   ├── 资本预算: NPV > 0 是核心标准
│   ├── 资本成本: ⚠️ 项目风险调整不可忽视
│   └── 资本结构: 过度负债限制财务灵活性
│
├── ⭐ 资本配置常见错误
│   ├── 激励错配: 管理层薪酬与长期价值脱钩
│   ├── 过度乐观: 高估项目现金流
│   ├── 风险误判: 折现率与项目不匹配
│   ├── 忽视灵活性: 极端杠杆限制投资能力
│   └── 沉没成本谬误: 继续投资失败项目
│
├── ⭐ 整合分析框架
│   ├── ① 看治理 → ② 看资本状况 → ③ 评估投资机会
│   ├── ④ 考虑融资约束 → ⑤ 判断是否增加股东价值
│   └── 📐 回报率 > WACC 且治理机制合理 → 创造价值
│
├── 💡 关键洞察
│   ├── 资本配置不是一次性决策，需动态调整
│   ├── 不要孤立看待每个模块 — 它们是相互依赖的
│   ├── 增长 ≠ 价值创造（回报率需超过资本成本）
│   └── 管理层可能在配置决策中追求个人利益
│
└── ⚠️ 考试陷阱总结
    ├── 管理层可能在资本配置中追求个人利益
    ├── 治理失灵会影响资本预算质量
    ├── 过度杠杆限制投资能力
    └── 增长不等于价值创造
```

## 📖 知识点详解

### 知识点1：资本配置主线逻辑 (Capital Allocation Framework)

**核心概念**：资本配置是公司将有限资本分配到最能创造价值的领域的决策过程。它是连接Corporate Issuers所有模块的主线：治理决定决策质量→营运资本释放现金→资本预算选择项目→资本成本设定折现率→资本结构选择融资方式→商业模式决定约束。

- **治理 (Governance)** → 谁决策？激励是否对齐？弱治理导致资本错配
- **营运资本 (Working Capital)** → 维持经营流动性，释放被占用的现金
- **资本预算 (Capital Budgeting)** → 选择 NPV > 0的价值增值项目
- **资本成本 (Cost of Capital)** → 设定风险匹配的折现率（WACC/项目特定折现率）
- **资本结构 (Capital Structure)** → 选择最优融资方式，保持财务灵活性
- **商业模式 (Business Model)** → 收入与成本结构决定投资需求和风险偏好

**考试应用**：综合题要求使用上述框架分析公司决策。给定公司场景，逐一检查治理、流动性、资本预算、资本结构各环节的问题。

### 知识点2：资本配置的常见错误 (Common Capital Allocation Mistakes)

**核心概念**：资本配置过程中存在多种常见错误，包括激励错配、过度乐观、风险误判、忽视灵活性和沉没成本谬误。识别这些错误有助于提高资本配置效率。

- **激励错配**：管理层薪酬与长期价值脱钩→短期主义，采纳负NPV项目
- **过度乐观**：管理层高估项目现金流→资本配置效率低下
- **风险误判**：项目使用不匹配的折现率→错误接受或拒绝项目
- **忽视灵活性**：极端杠杆限制投资能力→错过市场低谷时的投资机会
- **沉没成本谬误**：继续投资失败项目→更大的价值损失（抛好钱追坏钱）
- 💡 **核心洞察**：资本配置不是一次性决策，需要动态调整。市场条件变化后需重新评估

**考试应用**：多模块综合分析题。给定公司场景，使用整合框架分析潜在问题。核心判断标准：项目回报率 > WACC 且 > 融资成本，同时治理机制确保决策合理。

### 📐 关键公式表

本模块无新增公式，但需灵活运用前述模块公式。综合示例链条：

1. 治理特点 → 影响 CAPM 中 β (风险溢价)
2. 经营模式和成本结构 → 计算 DOL
3. DOL + DFL → 确定项目折现率
4. WACC → 评估项目 NPV
5. 资本结构约束 → 判断融资可行性

### 🛠️ 常见考点与解题思路

**考点1：多模块综合分析**
- 使用整合分析框架，逐一检查治理、资本结构、资本预算各环节。

**考点2：判断资本配置是否创造价值**
- 项目回报率 > WACK 且 > 融资成本，同时治理合理 → 创造价值。

**考点3：财务灵活性分析**
- 过度负债 → 限制灵活性 → 错失正 NPV 投资机会。

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 |
|-----------|-----------|
| 资本配置是一次性决策 | 需动态调整，市场条件变化后重新评估 |
| 模块可以孤立分析 | 治理失灵影响资本预算，杠杆限制投资 |
| 增长 = 价值创造 | 只有回报率超过资本成本的增长才创造价值 |
| NPV 为正即最优选择 | 可能有更好的分配方式 |

### 🔄 跨模块关联

- 治理与决策质量 → [[M02-Corporate-Governance-and-ESG]]
- 营运资本管理效率 → [[M03-Working-Capital-and-Liquidity]]
- 资本预算方法 → [[M04-Capital-Investments]]
- 资本成本作为基准 → [[M05-Cost-of-Capital]]
- 杠杆约束融资能力 → [[M06-Capital-Structure-and-Leverage]]
- 商业模式特征 → [[M07-Business-Models]]
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
