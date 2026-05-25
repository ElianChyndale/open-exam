---
title: "M08 — Duration and Convexity"
description: 基于收益率的久期与凸性——修正久期、货币久期、PVBP 与凸性调整（中英双语 CFA 备考）
module: M08
subject: Fixed_Income
official_module: "Module 11: Yield-Based Bond Duration Measures and Properties, Module 12: Yield-Based Bond Convexity and Portfolio Properties"
---

# M08: 基于收益率的久期与凸性 (Yield-Based Duration and Convexity)

## 1. 核心知识点

### 1.1 久期家族 (Duration Family)

- **核心公式 (English)**
  - 修正久期: `D_mod = D_mac/(1+y/m)`
  - 货币久期: `Money Duration = D_mod x Full Price`
  - PVBP: `PVBP ≈ Money Duration x 0.0001`
  - 价格变化近似: `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2`
- **修正久期估计价格对收益率变动的百分比敏感度 (modified duration estimates % price sensitivity to yield)**：修正久期 = Macaulay 久期 / (1 + y/m)，表示收益率变动 1% 时债券价格变动的百分比。
- **货币久期估计每单位收益率变动的货币价格变化 (money duration estimates currency price change per yield unit)**：货币久期 = 修正久期 x 全价，以货币金额（而非百分比）表示利率敏感度。
- **PVBP = 收益率变动 1bp 的价格变化 (PVBP = price change for 1 bp yield shift)**：PVBP (price value of a basis point) 也称为 DV01。

### 1.2 凸性 (Convexity)

- **凸性修正久期遗漏的曲率 (convexity corrects curvature missed by duration)**：久期是一阶线性近似，凸性补偿二阶曲率效应。当收益率变动较大时，凸性校正至关重要。
- **正凸性有利于对称收益率变动 (positive convexity helps for symmetric yield moves)**：正凸性债券在利率下降时价格上升的幅度大于在利率等幅上升时价格下降的幅度。
- **组合久期/凸性使用价值权重但有局限性 (portfolio duration/convexity use value weights with limitations)**：组合久期 = Σ 债券权重 x 债券久期，但仅适用于平行收益率曲线移动。

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| 修正久期 | `D_mod = D_mac / (1 + y/m)` |
| 货币久期 | `Money Duration = D_mod x Full Price` |
| PVBP | `PVBP = (P_- - P_+)/2` 或 `≈ Money Duration x 0.0001` |
| 价格变化（含凸性） | `%ΔP ≈ -D_mod x Δy + 0.5 x Convexity x (Δy)^2` |
| 凸性计算 | `Convexity = (P_- + P_+ - 2P_0) / (P_0 x (Δy)^2)` |
| 组合久期 | `D_p = Σ w_i x D_i`（价值权重） |

## 3. 常见考点与解题思路

- **用修正久期估计价格变化**：给定 D_mod 和 Δy，计算 `%ΔP ≈ -D_mod x Δy`。
- **用凸性改进估计**：收益率变动较大时（如 > 100bp），必须加入凸性项。
- **计算 PVBP/DV01**：可用近似公式 `Money Duration x 0.0001`，或直接计算收益率上下移 1bp 后的价格差。
- **组合久期计算**：以各债券市场价值占组合总价值的比例为权重，加权平均各债券的久期。

## 4. 易错点提醒

- **久期是局部的、基于收益率的；勿将其视为完整曲线压力测试 (duration is local and yield-based; do not treat it as a full curve stress test)**：久期假设收益率曲线平行移动且变动幅度很小，对于非平行移动或大幅变动不准确。
- **Duration 和 maturity 不是一回事**：零息债券的 Macaulay duration = maturity；但付息债券的 duration < maturity。高票息债券的 duration 更短。
- **正凸性对投资者有利**：但获得正凸性通常要付出代价（如放弃部分收益），市场不会免费提供正凸性。
- **凸性用 decimals 计算时 Δy 也要用小数**：Δy = 0.01 表示 1%（不是 1）。常见错误是忘记将百分比转换为小数。

## 5. 跨模块关联

- D_mod 来自 D_mac → [[M07-Interest-Rate-Risk]] 的 Macaulay 久期
- 有效久期 → [[M09-Curve-Based-and-Empirical-Risk]] 的 option-aware 风险
- 组合久期 → [[M04-Yield-and-Spread-Measures]] 的收益率分析
