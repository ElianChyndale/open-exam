---
title: "M08 — Equity Valuation Concepts and Tools"
description: 权益估值概念与工具：戈登增长模型、合理倍数、相对估值法、DDM 与 multiples 应用
module: M08
subject: Equity
official_module: "Module 8: Equity Valuation: Concepts and Basic Tools"
---

# M08: 权益估值概念与工具 (Equity Valuation Concepts and Tools)

## 1. 核心知识点

### 内在价值 (Intrinsic value)
- **现值逻辑 (present value logic)**：资产价值 = 未来现金流按**必要收益率 (required return)** 折现
- **戈登增长模型 (Gordon Growth Model, GGM)**：适用于**稳定永续股息增长 (stable perpetual dividend growth)** 的公司
- **合理倍数 (justified multiples)**：将**基本面 (fundamentals)** 与价格比率联系起来 — 如合理市盈率 = `Payout Ratio / (r - g)`

### 相对估值 (Relative valuation)
- **常用倍数**：**市盈率 (P/E)**、**市净率 (P/B)**、**市销率 (P/S)**、**市现率 (P/CF)**、**企业价值/EBITDA (EV/EBITDA)**
- **领先 vs trailing 分母**：**领先 (forward)** 使用预期盈利，**trailing** 使用历史盈利 — 周期性与会计可比性影响选择
- **估值信号检验**：低倍数可能是真便宜（价值股）、也可能是合理的（高风险/低增长）、或两者兼有 — 必须对照**增长 (growth)**、**风险 (risk)**、**质量 (quality)** 三重检验

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| 戈登增长模型 (GGM) | `P_0 = D_1 / (r - g)`，必须 `r > g` |
| 隐含必要收益率 | `r = D_1 / P_0 + g` |
| 可持续增长率 | `g = Retention Ratio × ROE` |
| 合理领先市盈率 (Justified Leading P/E) | `P_0 / E_1 = Payout Ratio / (r - g)` |
| 合理 trailing 市盈率 | `P_0 / E_0 = Payout Ratio(1 + g) / (r - g)` |
| 企业价值 (EV) | `Equity + Debt + Preferred + Minority Interest - Cash` |
| P/B 市净率 | `Price per Share / BVPS` |
| P/S 市销率 | `Price per Share / Sales per Share` |
| EV/EBITDA | `Enterprise Value / EBITDA` |

## 3. 常见考点与解题思路

- **GGM 计算**：先确认 r > g → 代入 `D_1/(r-g)` → 检查答案合理性
- **justified P/E 推导**：从 GGM 变形得到 — 理解 payout ratio、r、g 如何影响倍数
- **相对估值步骤**：选同类可比公司 → 计算行业平均倍数 → 对比目标公司 → 调整增长/风险差异

## 4. 易错点提醒

- **低市盈率可能是真便宜，也可能是应得的，或两者兼有**【考试陷阱】
- **DDM 不适用于所有公司**：股息政策不稳定的公司（如高增长不分红公司）不适合
- **高增长不一定等于高价值**：还要看必要收益率和可持续性
- **EV/EBITDA 并非总是优于 P/E**：只是适用场景不同 — EBITDA 为正但盈利为负的公司更适用
- **trailing 与 forward 倍数不可直接比较**：口径不同，预期也不同

## 5. 跨模块关联

- **估值依赖盈利预测** → [[M07-Company-Analysis-Forecasting]]
- **公司质量与竞争优势支撑估值倍数** → [[M05-Company-Analysis-Past-and-Present]]
- **行业特征影响估值参数选择** → [[M06-Industry-and-Competitive-Analysis]]
- **指数作为估值比较基准** → [[M02-Security-Market-Indexes]]
