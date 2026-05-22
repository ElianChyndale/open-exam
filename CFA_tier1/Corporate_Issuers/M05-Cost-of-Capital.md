---
title: "M05 — Cost of Capital"
description: 资本成本 — 各要素成本计算、WACC构建、边际资本成本
module: M05
subject: Corporate_Issuers
---

# M05: Cost of Capital（资本成本）

## 1. 核心知识点

### 1.1 各要素成本 (Component Costs)

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

### 1.2 WACC 构建 (WACC Construction)

**加权平均资本成本 (Weighted Average Cost of Capital, WACC)** 是公司整体融资成本的加权平均：

`WACC = wd × rd(1-T) + wp × rp + we × re`

其中 wd、wp、we 分别为债务、优先股和普通股在资本结构中的权重。

**权重选择的关键规则**：
- **使用市场价值权重 (Market-Value Weights)**，而非账面价值权重 (Book-Value Weights)。市场价值反映的是当前的机会成本。
- **使用目标权重 (Target Weights)**，如果公司有明确的长期目标资本结构。
- **边际资本成本 (Marginal Cost of Capital, MCC)**：每多筹集一元新资本的成本。当融资额超过某个阈值时，MCC 会上升。

**常见陷阱**：**公司的 WACC 不能作为所有项目的通用折现率。** 如果项目风险与公司整体风险显著不同，应使用**项目特定折现率 (project-specific hurdle rate)**。

### 1.3 发行费用与摩擦成本 (Flotation Costs)

发行新股或债券会产生承销费、法律费用等。在资本预算中，发行费用应作为项目初始现金流出处理，而非调整 WACC。

## 2. 关键公式

| 指标 | 公式 | 应用场景 |
|------|------|----------|
| 税后债务成本 | `rd(1-T)` | 计算债务要素成本 |
| 优先股成本 | `Dp/Pp` | 计算优先股要素成本 |
| CAPM 股权成本 | `rf + β × [E(Rm) - rf]` | 最常用的股权成本估计方法 |
| 股息增长模型 | `D1/P0 + g` | 稳定派息公司 |
| WACC | `wd×rd(1-T) + wp×rp + we×re` | 公司整体资本成本 |
| 边际资本成本 (MCC) | 突破点后的加权成本 | 当融资额超过某一点时 WACC 上升 |

## 3. 常见考点与解题思路

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

## 4. 易错点提醒

- **债务成本必须用税后**：乘以 (1-T) 是必做步骤，忘记调整是最常见的失误。
- **不要用账面权重**：**考试强烈优先使用市场价值权重。**
- **发行费用不是调 WACC，而是调现金流**：发行费用作为初始流出，减少初始净现金流。
- **WACC 不是固定不变的**：随着融资额增加，MCC 会上升，WACC 也会变化。
- **β 衡量的是系统性风险**：不是总风险。充分分散的投资者只关心 β。

## 5. 跨模块关联

- WACC 作为折现率 → [[M04-Capital-Investments]] 资本预算中 NPV 计算的核心输入
- 资本结构权重 → [[M06-Capital-Structure-and-Leverage]] 债务比例影响 WACC
- 杠杆影响 β → [[M06-Capital-Structure-and-Leverage]] 财务杠杆放大了股权 β
- 融资政策影响成本 → [[M03-Working-Capital-and-Liquidity]] 短期融资成本与长期不同
- 资本成本整合 → [[M08-Capital-Allocation-Integration]] WACC 是资本配置决策的基准
