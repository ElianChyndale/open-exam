---
title: "M04 — Yield and Spread Measures"
description: 固定利率债券收益率与利差——YTM、当期收益率、年化转换与利差度量（中英双语 CFA 备考）
module: M04
subject: Fixed_Income
---

# M04: 固定利率债收益率与利差 (Fixed-Rate Yield and Spread Measures)

## 1. 核心知识点

### 1.1 收益率视角 (Yield Lens)

- **YTM 是承诺现金流和再投资假设下的 IRR (YTM is IRR under promised cash flows and reinvestment assumptions)**：到期收益率 (YTM) 是使债券现值等于价格的贴现率，隐含假设：持有至到期且所有票息收入按 YTM 再投资。
- **当期收益率仅捕捉票息收入 (current yield captures coupon income only)**：`Current Yield = 年票息收入 / 债券价格`，忽略资本利得/损失和再投资收入。
- **年化收益率转换取决于复利频率 (annual yield conversion depends on compounding frequency)**：不同复利频率下的收益率需要标准化比较。`EAY = (1 + periodic rate)^m - 1`。

### 1.2 利差视角 (Spread Lens)

- **国债基准利差/插值利差/G-利差 (government benchmark spread/interpolated spread/G-spread)**：利差衡量信用风险/流动性风险溢价。G-spread 是在国债即期曲线上插值计算的利差，比简单基准利差更精确。
- **利差包含信用、流动性、期权、税收、技术面因素 (spread embeds credit, liquidity, option, tax, technical factors)**：利差不是纯信用补偿，它综合了多种风险因素。
- **无期权固定利率债券的价格与收益率呈反向关系 (price and yield move inversely for option-free fixed-rate bonds)**：这是固定收益投资最基础的直觉——利率上升时债券价格下降。

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| 到期收益率 YTM | `P = Σ_{t=1}^{N} C/(1+YTM/m)^t + FV/(1+YTM/m)^N` |
| 当期收益率 | `Current Yield = 年票息 / 债券价格` |
| 有效年化收益率 | `EAY = (1 + periodic rate)^m - 1` |
| G-spread | `G-spread = YTM_{bond} - YTM_{benchmark}`（需插值匹配期限） |

## 3. 常见考点与解题思路

- **YTM 近似计算**：给出债券价格、票息率、期限、面值，反推 YTM。考试中可使用金融计算器。
- **比较不同复利频率的收益率**：统一转换为 EAY 或 BEY (bond equivalent yield) 后比较。
- **计算 G-spread**：确定目标债券的期限后在国债曲线上插值得到对应期限的基准收益率，计算差值。
- **判断利差变化的含义**：利差走阔 → 债券价格下降（相对基准）；利差收窄 → 债券价格上升。

## 4. 易错点提醒

- **Same YTM 不代表 same value if timing/risk structure differs**：即使两只债券有相同的 YTM，若现金流时间分布不同或含嵌入期权，它们的价格风险和再投资风险也不同。
- **Current yield 不是总回报**：它忽略 price change 和 reinvestment income，这一点考试常考。
- **YTM 的再投资假设在现实中无法严格满足**：如果市场利率变化，实际持有期回报将不同于 YTM。
- **Spread widening 不一定等于违约风险上升**：也可能是流动性恶化或市场风险偏好转变。

## 5. 跨模块关联

- YTM → [[M03-Bond-Valuation]] 的定价逆运算
- 利差分析 → [[M10-Credit-Risk]] 的信用风险度量
- 年化转换 → [[M05-Floating-Rate-and-Money-Market]] 的货币市场指标
