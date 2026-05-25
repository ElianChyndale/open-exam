---
title: "M09 — Curve-Based and Empirical Risk"
description: 曲线与实证风险度量——有效久期、有效凸性、关键利率久期与曲线非平行移动（中英双语 CFA 备考）
module: M12
subject: Fixed_Income
official_module: "Module 13: Curve-Based and Empirical Fixed-Income Risk Measures"
---

# M12: 曲线与实证风险度量 (Curve-Based and Empirical Risk Measures)

## 1. 核心知识点

### 1.1 期权感知风险 (Option-Aware Risk)

- **有效久期/有效凸性在现金流可能变化时重新定价 (effective duration/effective convexity reprice when cash flows may change)**：对于含嵌入期权（可赎回、可回售）的债券，现金流会随利率变化而改变，因此不能使用基于固定现金流的修正久期，而应使用有效久期 (effective duration) 和有效凸性 (effective convexity)。
- **嵌入期权改变可赎回/提前还款行为 (embedded option changes callability/prepayment behavior)**：利率下降时，可赎回债券的发行人倾向于赎回并再融资，限制了价格上涨空间（负凸性）；利率上升时，MBS 的提前还款减慢（展期风险）。
- **分析久期可能与观察到的经验久期不同 (analytical duration may differ from observed empirical duration)**：基于模型的久期（分析久期）可能不同于从历史数据回归得出的经验久期 (empirical duration)，原因包括模型假设误差、市场摩擦等。

### 1.2 曲线风险 (Curve Risk)

- **关键利率久期隔离期限区间的敏感度 (key rate duration isolates maturity-bucket sensitivity)**：关键利率久期 (key rate duration / partial duration) 衡量收益率曲线上特定期限点的利率变动对债券价格的影响，帮助识别非平行移动的风险暴露。
- **非平行曲线移动打破单一久期直觉 (non-parallel curve shifts break single-duration intuition)**：实际收益率曲线变动往往不是平行的（如长端上升幅度大于短端），此时单一久期指标无法准确描述风险。
- **基准利率变动与信用利差变动是独立问题 (benchmark shift and credit spread shift are separate questions)**：债券收益率变动 = 基准收益率变动 + 信用利差变动，两者驱动因素不同，需要分开分析。

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| 有效久期 | `EffDur = (P_- - P_+) / (2 x P_0 x Δy)` |
| 有效凸性 | `EffCon = (P_- + P_+ - 2P_0) / (P_0 x (Δy)^2)` |
| 关键利率久期 | `KRD_k = -(1/P) x (ΔP/Δy_k)`（仅移动第 k 个期限点） |
| 收益率分解 | `Δy_bond = Δy_benchmark + Δy_spread` |

## 3. 常见考点与解题思路

- **判断何时使用有效久期 vs 修正久期**：债券含嵌入期权（可赎回、可回售、MBS）→ 用有效久期；无期权固定利率债券 → 用修正久期。
- **分析非平行移动的影响**：给定的曲线变化情境（如 flattening、steepening），判断哪种债券受影响最大。
- **计算有效久期**：分别计算利率向上和向下移 Δy 后的价格，代入公式。
- **区分 benchmark shift 与 spread shift 的驱动因素**：benchmark shift 由宏观经济和货币政策驱动；spread shift 由信用状况、流动性等因素驱动。

## 4. 易错点提醒

- **可赎回债券和 MBS 的风险不能完全依赖普通修正久期 (callable and MBS risk cannot be fully trusted to plain modified duration)**：修正久期高估了可赎回债券在利率下降时的价格上涨，因为这些债券有价格上限 (call price)。
- **Effective duration ≠ modified duration**：只有当现金流不随利率变化时两者才相等。考试常考区分适用场景。
- **Non-parallel shift 是常态而非例外**：组合久期加权平均只适用于平行移动假设，对于 twist 或 butterfly 变动的分析需要 key rate duration。
- **Empirical duration 可能低于 analytical duration**：因为现实中利率变动往往伴随信用利差反向变动，部分抵消了纯利率效应。

## 5. 跨模块关联

- 有效久期 → [[M08-Duration-and-Convexity]] 的修正久期对比
- 嵌入期权 → [[M01-Instrument-Features]] 的或有条款
- Spread shift → [[M10-Credit-Risk]] 的信用利差分析
