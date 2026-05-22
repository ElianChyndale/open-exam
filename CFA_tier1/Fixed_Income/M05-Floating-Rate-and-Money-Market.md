---
title: "M05 — Floating-Rate and Money Market Measures"
description: 浮动利率与货币市场指标——FRN 利差、贴现收益率、货币市场收益率与债券等价收益率（中英双语 CFA 备考）
module: M05
subject: Fixed_Income
---

# M05: 浮动利率与货币市场指标 (Floating-Rate and Money Market Measures)

## 1. 核心知识点

### 1.1 浮动利率工具 (Floating-Rate Instruments)

- **核心公式 (English)**
  - 银行贴现收益率: `BDY = (FV - P)/FV x 360/t`
  - 货币市场收益率: `MMY = (FV - P)/P x 360/t`
  - 债券等价收益率: `BEY = (FV - P)/P x 365/t`
- **参考利率 + 报价利差；重置缓释但未消除利率风险 (reference rate + quoted margin; reset mitigates but does not erase rate risk)**：FRN 的票息 = 参考利率 + 报价利差 (quoted margin)。定期重置减少但未完全消除利率风险——重置间隔期间价格仍会因市场利率变化而波动。
- **贴现利差连接偏离面值的价格与所需利差 (discount margin connects price away from par with required spread)**：当 FRN 交易价格不等于面值时，贴现利差 (discount margin / required margin) 是使定价等式成立的利差，反映了信用风险变化。
- **信用恶化可在重置后仍使 FRN 低于面值 (credit deterioration can push FRN below par despite resets)**：即使票息重置，若报价利差低于市场要求的利差，FRN 仍会折价交易。

### 1.2 货币市场工具 (Money Market Instruments)

- **贴现基础 vs 加息基础 (discount basis vs add-on basis)**：贴现基础工具（如 T-bill）以面值折价发行，收益体现在买入价与面值之差；加息基础工具（如 FRN）支付利息。
- **银行贴现收益率 vs 货币市场收益率 vs 债券等价收益率 (bank discount yield vs money market yield vs bond equivalent yield)**：三者都是用于报价的年化收益率，但计算公式不同。BDY 以面值为分母、360 天；MMY 以购买价为分母、360 天；BEY 以购买价为分母、365 天。
- **分母陷阱：面值或购买价格；360 天或 365 天 (denominator matters: par or purchase price; 360-day or 365-day year)**：考试中收益率类型转换的考点高度集中于分母是面值还是价格，以及 year basis 是 360 还是 365。

## 2. 关键公式

| 指标 | 公式 |
|------|------|
| 银行贴现收益率 (BDY) | `BDY = (FV - P)/FV x 360/t` |
| 货币市场收益率 (MMY) | `MMY = (FV - P)/P x 360/t` |
| 债券等价收益率 (BEY) | `BEY = (FV - P)/P x 365/t` |
| HPY（持有期收益率） | `HPY = (FV - P)/P` |
| BDY 转 MMY | `MMY = (365 x BDY) / (360 - t x BDY)` |
| BDY 转 BEY | `BEY = (365 x BDY) / (360 - t x BDY)` |

## 3. 常见考点与解题思路

- **收益率类型转换**：题目给出 BDY，要求计算 MMY 或 BEY。步骤：先算 HPY，再用 HPY 换算目标收益率。
- **FRN 的 discount margin 计算**：FRN 价格偏离面值时，需要求解贴现利差使定价等式成立，类似于 YTM 的逆运算。
- **判断 FRN 的交易状态**：报价利差 > 市场要求的利差 → premium；报价利差 < 市场要求的利差 → discount。

## 4. 易错点提醒

- **货币市场报价偏爱分母陷阱【考试陷阱】**：BDY 分母是 FV，MMY 分母是 P，年天数也有 360 和 365 的区别。做题时必须先看题目用的是哪种报价。
- **HPY 是中间桥梁**：不同收益率之间的转换，都先经过 HPY = (FV - P)/P，再转换为目标收益率。
- **FRN 的 reset 频率不等于无利率风险**：两个 reset 日期之间价格仍会随参考利率变化而波动。
- **Discount margin 不同于 quoted margin**：quoted margin 是合约中固定的；discount margin 是市场要求的利差，随信用状况变化。

## 5. 跨模块关联

- FRN 定价 → [[M03-Bond-Valuation]] 的 DCF 框架
- 货币市场收益率 → [[M04-Yield-and-Spread-Measures]] 的 yield conversion
- 贴现利差 → [[M10-Credit-Risk]] 的信用风险定价
