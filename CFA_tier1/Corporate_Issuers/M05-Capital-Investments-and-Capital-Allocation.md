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

##### 1. 核心知识点

###### 1.1 现金流纪律 (Cash-Flow Discipline)

资本预算 (Capital Budgeting) 的核心是**识别和评估能增加股东价值的投资机会**。最关键的原则是：

- **使用增量税后现金流 (Use Incremental After-Tax Cash Flows)**：只考虑项目本身带来的额外现金流，而非公司整体的现金流。
- **忽略沉没成本 (Ignore Sunk Costs)**：已发生的、不可收回的成本与未来的增量决策无关。例如，市场调研费用不应计入项目现金流。
- **包含机会成本 (Include Opportunity Costs)**：公司已有资产如果用于新项目，其放弃的最佳替代用途的价值应作为成本计入。
- **考虑蚕食效应 (Cannibalization)**：新项目可能侵蚀现有产品的销售，这部分损失应计入。
- **包含营运资本变动 (Include Working Capital Changes)**：项目通常需要额外存货和应收账款投资，结束时可能收回。
- **考虑残值与税务影响 (Salvage Value & Tax Effects)**：项目结束时出售资产的净现金流，包括税务影响。

**决策类型**：
- **独立项目 (Independent Projects)**：接受或拒绝互不影响
- **互斥项目 (Mutually Exclusive Projects)**：只能选择其中一个
- **资本约束 (Capital Rationing)**：资金有限，需在竞争项目中择优分配

###### 1.2 决策标准 (Decision Criteria)

- **净现值 (Net Present Value, NPV)**：`NPV = Σ CFt/(1+r)^t - Initial Outlay`
  - 最可靠的决策标准。NPV > 0 创造价值。
  - **NPV 在兼容假设下最大化价值**，是互斥项目中的首选标准。

- **内部收益率 (Internal Rate of Return, IRR)**：`0 = Σ CFt/(1+IRR)^t - Initial Outlay`
  - 即使 NPV 为 0 的折现率。IRR > 资本成本则接受。
  - **非常规现金流 (Unconventional Cash Flows)** 下可能出现多个 IRR 或无 IRR。

- **盈利指数 (Profitability Index, PI)**：`PI = PV of future cash inflows / Initial investment`
  - PI > 1 则接受。适用于 **资本约束 (capital rationing)** 下的项目排序。

- **回收期 (Payback Period)**：累计未折现现金流收回初始投资的时间。
  - **不反映价值创造**，忽略时间价值和回收期后的现金流。

- **折现回收期 (Discounted Payback Period)**：考虑时间价值，但仍忽略回收期后现金流。

###### 1.3 实物期权 (Real Options)

传统 NPV 假设项目决策不可逆，而现实中管理层有灵活性：
- **时机期权 (Timing Option)**：延迟投资等待更有利条件
- **扩张期权 (Expansion Option)**：如果项目成功可追加投资
- **放弃期权 (Abandonment Option)**：项目失败时可退出减少损失
- **灵活性期权 (Flexibility Option)**：调整产出、投入或生产方式

实物期权**增大了项目的 NPV**，因为管理层可以在有利时行动、不利时止损。

##### 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| 净现值 (NPV) | `NPV = Σ_{t=0}^{N} CF_t/(1+r)^t` | 价值创造的绝对度量 |
| 内部收益率 (IRR) | `0 = Σ_{t=0}^{N} CF_t/(1+IRR)^t` | 项目本身的收益率 |
| 盈利指数 (PI) | `PI = PV of future cash inflows / Initial investment` | 每单位投资创造的现值 |
| 回收期 | 累计现金流 ≥ 0 的时间点 | 流动性指标而非价值指标 |
| 折现回收期 | 累计折现现金流 ≥ 0 的时间点 | 略好于回收期但仍不完整 |

##### 3. 常见考点与解题思路

**考点 1：NPV 计算**
- 给定初始投资、系列现金流和折现率，求 NPV。
- 解题：逐期折现后加总，减去初始投资。注意时间轴从 t=0 开始。

**考点 2：NPV vs IRR 冲突**
- 当互斥项目的规模 (scale) 或时间 (timing) 不同时，IRR 可能给出错误排序。
- 解题原则：**NPV 优先于 IRR**。NPV 反映的是绝对的财富增加量。

**考点 3：识别应计入的现金流**
- 题目列出若干项目相关和无关的成本，要求选择应计入的。
- 关键：排除沉没成本，包含机会成本、营运资本变动、残值等。

**考点 4：资本约束下的项目选择**
- 用 PI 排序。在资本限额内依次选择 PI 最高的项目。

##### 4. 易错点提醒

- **融资成本不应重复计算**：折现率已经反映了融资成本，项目现金流中一般不应再包含利息支出等融资现金流。
- **IRR 在非常规现金流下会误导**：现金流正负交替多次时可能出现多个 IRR 或无 IRR。
- **回收期短 ≠ 项目好**：回收期忽略时间价值和后期现金流，可能拒绝 NPV 高但回收慢的项目。
- **NPV 与 IRR 对再投资率假设不同**：NPV 假设以资本成本再投资，IRR 假设以 IRR 本身再投资，NPV 的假设更合理。

##### 5. 跨模块关联

- 折现率 → [[M05-Cost-of-Capital]] WACC 是资本预算中最常用的折现率
- 项目风险调整 → [[M05-Cost-of-Capital]] 风险不同的项目应使用不同折现率
- 经营杠杆影响项目风险 → [[M06-Capital-Structure-and-Leverage]] 固定成本高的项目经营杠杆大
- 实物期权概念 → [[M07-Business-Models]] 不同商业模式的灵活性不同
- 资本配置整合 → [[M08-Capital-Allocation-Integration]] 资本预算应纳入公司整体价值创造策略

### Migrated from `CFA_tier1/Corporate_Issuers/M05-Cost-of-Capital.md`

_Alignment score: 1.00. Original official module field: Module 5: Capital Investments and Capital Allocation._

#### M06: Cost of Capital（资本成本）

##### 1. 核心知识点

###### 1.1 各要素成本 (Component Costs)

资本成本是公司为融资支付的**必要回报率 (required return)**，也是投资者提供资金所要求的回报。不同来源的资本成本不同：

- **债务成本 (Cost of Debt, rd)**：公司借入资金所需支付的利率。
  - **税后债务成本 (After-Tax Cost of Debt)** = `rd × (1 - T)`
  - 由于利息费用可税前扣除 (tax-deductible)，债务有**税盾 (tax shield)** 效应，因此税后成本低于税前成本。
  - 对于公开发行债券的公司，可以用债券的到期收益率 (Yield to Maturity, YTM) 作为税前债务成本。

- **优先股成本 (Cost of Preferred Stock, rp)** = `Dp / Pp`
  - 优先股股息是固定的，且支付优先于普通股。优先股没有到期日，因此用永续年金公式。
  - 优先股股息通常不可税前扣除（除非特定结构），因此不调整税。

- **普通股成本 (Cost of Common Equity, re)**：估算方法有三种：
  1. **CAPM 法**：`re = rf + β × [E(Rm) - rf]`，这是 CFA L1 最常使用的方法。rf 为无风险利率，β 衡量系统性风险，E(Rm) - rf 为市场风险溢价。
  2. **股息增长模型 (Dividend Growth Model, DGM)**：`re = D1/P0 + g`，其中 D1 为预期下期股息，g 为股息增长率。适用于稳定派息的公司。
  3. **债券收益率加风险溢价法 (Bond Yield Plus Risk Premium)**：`re = rd + Risk Premium`，简略估算方法。

###### 1.2 WACC 构建 (WACC Construction)

**加权平均资本成本 (Weighted Average Cost of Capital, WACC)** 是公司整体融资成本的加权平均：

`WACC = wd × rd(1-T) + wp × rp + we × re`

其中 wd、wp、we 分别为债务、优先股和普通股在资本结构中的权重。

**权重选择的关键规则**：
- **使用市场价值权重 (Market-Value Weights)**，而非账面价值权重 (Book-Value Weights)。市场价值反映的是当前的机会成本。
- **使用目标权重 (Target Weights)**，如果公司有明确的长期目标资本结构。
- **边际资本成本 (Marginal Cost of Capital, MCC)**：每多筹集一元新资本的成本。当融资额超过某个阈值时，MCC 会上升。

**常见陷阱**：**公司的 WACC 不能作为所有项目的通用折现率。** 如果项目风险与公司整体风险显著不同，应使用**项目特定折现率 (project-specific hurdle rate)**。

###### 1.3 发行费用与摩擦成本 (Flotation Costs)

发行新股或债券会产生承销费、法律费用等。在资本预算中，发行费用应作为项目初始现金流出处理，而非调整 WACC。

##### 2. 关键公式

| 指标 | 公式 | 应用场景 |
|------|------|----------|
| 税后债务成本 | `rd(1-T)` | 计算债务要素成本 |
| 优先股成本 | `Dp/Pp` | 计算优先股要素成本 |
| CAPM 股权成本 | `rf + β × [E(Rm) - rf]` | 最常用的股权成本估计方法 |
| 股息增长模型 | `D1/P0 + g` | 稳定派息公司 |
| WACC | `wd×rd(1-T) + wp×rp + we×re` | 公司整体资本成本 |
| 边际资本成本 (MCC) | 突破点后的加权成本 | 当融资额超过某一点时 WACC 上升 |

##### 3. 常见考点与解题思路

**考点 1：计算 WACC**
- 给定各资本来源的金额（或权重）、税前债务成本、税率、股权成本，计算 WACC。
- 步骤：先算税后债务成本，再按市场价值权重加权平均。

**考点 2：选择正确的权重**
- 题目给 book value 和 market value，要求选择。
- 答案：**market-value weights**。

**考点 3：CAPM 计算股权成本**
- 给定无风险利率、市场收益和 β，计算 re。
- 公式：`re = rf + β(rm - rf)`。注意是**市场风险溢价** (rm - rf)，不是 rm 本身。

**考点 4：判断折现率是否合适**
- 问：公司 WACC 为 8%，一个高风险的创新项目是否应该用 8% 折现？
- 答案：不应该。**项目风险应与折现率匹配**，高风险项目应使用更高的折现率。

##### 4. 易错点提醒

- **债务成本必须用税后**：乘以 (1-T) 是必做步骤，忘记调整是最常见的失误。
- **不要用账面权重**：**考试强烈优先使用市场价值权重。**
- **发行费用不是调 WACC，而是调现金流**：发行费用作为初始流出，减少初始净现金流。
- **WACC 不是固定不变的**：随着融资额增加，MCC 会上升，WACC 也会变化。
- **β 衡量的是系统性风险**：不是总风险。充分分散的投资者只关心 β。

##### 5. 跨模块关联

- WACC 作为折现率 → [[M04-Capital-Investments]] 资本预算中 NPV 计算的核心输入
- 资本结构权重 → [[M06-Capital-Structure-and-Leverage]] 债务比例影响 WACC
- 杠杆影响 β → [[M06-Capital-Structure-and-Leverage]] 财务杠杆放大了股权 β
- 融资政策影响成本 → [[M03-Working-Capital-and-Liquidity]] 短期融资成本与长期不同
- 资本成本整合 → [[M08-Capital-Allocation-Integration]] WACC 是资本配置决策的基准

### Migrated from `CFA_tier1/Corporate_Issuers/M08-Capital-Allocation-Integration.md`

_Alignment score: 1.00. Original official module field: Module 5: Capital Investments and Capital Allocation._

#### M09: Capital Allocation Integration（资本配置整合）

##### 1. 核心知识点

###### 1.1 资本配置的主线逻辑

资本配置 (Capital Allocation) 是公司**将有限资本分配到最能创造价值的领域**的决策过程。它是连接 Corporate Issuers 所有模块的主线：

```text
治理 (Governance) → 谁决策，激励是否对齐
    ↓
营运资本管理 (Working Capital) → 维持日常运营的流动性
    ↓
资本预算 (Capital Budgeting) → 选择增值项目
    ↓
资本成本 (Cost of Capital) → 设定风险匹配的折现率
    ↓
资本结构 (Capital Structure) → 选择最优融资方式
    ↓
商业模式 (Business Model) → 收入与成本结构特征决定约束
```

###### 1.2 各环节的具体作用

1. **治理 → 明确决策责任人**：良好的公司治理确保资本配置决策由有能力和激励合适的决策者做出。弱治理可能导致管理层过度投资（建立"帝国"）、规避风险的正 NPV 项目或偏爱短期项目。

2. **营运资本 → 维持经营流动性**：有效的营运资本管理释放被占用的现金，为长期投资提供资金来源。过度堆积营运资本会降低资本回报效率。

3. **资本预算 → 选择价值增值项目**：NPV > 0 是项目创造价值的核心判断标准。但在执行中需结合战略考量——有些低 NPV 项目可能是未来高增长机会的"入场券"（实物期权逻辑）。

4. **资本成本 → 设定风险匹配的最低收益率**：WACC 作为基准折现率，但**项目风险调整 (risk-adjusted hurdle rate)** 不可忽视。误用折现率会扭曲资本配置。

5. **资本结构 → 融资而不过度消耗缓冲**：最优资本结构平衡税盾收益与财务困境成本。过度负债会限制公司在市场低迷时投资价值项目的能力——**财务灵活性 (financial flexibility)** 本身是有价值的。

###### 1.3 资本配置的常见错误

| 错误类型 | 表现 | 后果 |
|----------|------|------|
| 激励错配 | 管理层薪酬与长期价值脱钩 | 短期主义，NPV 为负的项目被采纳 |
| 过度乐观 | 管理层高估项目现金流 | 资本配置效率低下 |
| 风险误判 | 项目使用不匹配的折现率 | 错误地接受或拒绝项目 |
| 忽视灵活性 | 极端杠杆限制投资能力 | 错过市场低谷时的投资机会 |
| 沉没成本谬误 | 继续投资失败项目 | 更大的价值损失（"抛好钱追坏钱"） |

###### 1.4 整合分析框架

回答 Corporate Issuers 综合题时，可遵循以下思维链：

1. **首先看治理**：公司决策机制是否健全？管理层激励是否与股东一致？
2. **再看资本状况**：公司有足够的流动性吗？资本结构是否可持续？
3. **评估投资机会**：项目产生的现金流是否超过资本成本？NPV 是否为正？
4. **考虑融资约束**：公司能否以合理成本筹集所需资本？
5. **最终判断**：总体来看，公司决策是否增加了股东价值？

##### 2. 关键公式

本模块无新增公式，但需要灵活运用之前所有模块的公式进行综合计算。最常见的是将 NPV 计算与 WACC、杠杆分析结合：

**综合示例链条**：
1. 给定公司治理特点 → 影响折现率中的风险溢价 (re 的 CAPM 中的 β)
2. 给定经营模式和成本结构 → 计算 DOL，判断项目风险
3. 根据 DOL 和 DFL → 确定项目适用的折现率
4. 结合 WACC 计算 → 评估项目 NPV
5. 考虑资本结构约束 → 判断融资可行性

##### 3. 常见考点与解题思路

**考点 1：多模块综合分析**
- 题目描述一个公司场景（如"管理层薪酬与短期利润挂钩，同时公司正考虑一个高杠杆收购"），要求分析潜在问题。
- 解题：使用上述整合分析框架，逐一检查治理、资本结构、资本预算各环节。

**考点 2：判断资本配置是否为股东创造价值**
- 题目提供公司的一系列决策信息（如投资规模、融资方式、回报率等），要求判断是否增加了股东价值。
- 核心判断标准：项目产生的回报率 > WACC 且 > 融资成本，同时治理机制确保决策合理。

**考点 3：财务灵活性分析**
- 问：为什么过度负债的公司可能错失价值创造机会？
- 答案：高负债限制财务灵活性，公司可能无法在最佳时机筹集资金投资于正 NPV 项目。

##### 4. 易错点提醒

- **资本配置不是一次性决策**：动态调整比一次定终身更重要。市场条件变化后需重新评估。
- **管理层可能在资本配置决策中追求个人利益**：即使项目 NPV 为正，如果不是"最优"选择，仍可能有更好的分配方式。
- **不要孤立地看每个模块**：治理失灵会影响资本预算质量，过度杠杆会限制投资能力。**这些模块是相互依赖的。**
- **增长不等于价值创造**：只有回报率超过资本成本的增长才创造价值。

##### 5. 跨模块关联

- 治理与决策质量 → [[M02-Corporate-Governance-and-ESG]] 治理影响资本配置决策
- 营运资本管理效率 → [[M03-Working-Capital-and-Liquidity]] 释放现金支持长期投资
- 资本预算方法 → [[M04-Capital-Investments]] 资本配置的核心工具
- 资本成本作为基准 → [[M05-Cost-of-Capital]] WACC 是投资的门槛
- 杠杆约束融资能力 → [[M06-Capital-Structure-and-Leverage]] 过高杠杆限制灵活性
- 商业模式特征 → [[M07-Business-Models]] 决定投资需求和风险偏好
## Review Hooks

- Add mistake-driven traps only after they can be traced back to `.system/events/`.
- Keep module naming and order locked to the official 2026 curriculum registry.
