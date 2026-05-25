---
title: "M03 — Balance Sheet"
description: "资产负债表深度解析：无形资产、商誉、金融工具、非流动负债的确认与计量，以及同比例资产负债表分析技术"
module: M03
official_module: "M3: Analyzing Balance Sheets"
subject: Financial_Statement_Analysis
---

# M03: 资产负债表分析 (Balance Sheet Analysis)

## 1. 核心知识点

### 3.1 无形资产 (Intangible Assets)

**外购 vs 内部产生 (Purchased vs Internally Generated)：**
- 外购无形资产(purchased intangibles)按购买成本确认，符合资产确认条件
- 内部产生无形资产(internally generated intangibles)的会计处理因准则而异：US GAAP 下研发支出(research and development)通常全部费用化；IFRS 下开发阶段支出符合条件的可资本化
- 对分析师而言，内部产生的无形资产往往被低估，导致资产回报率(ROA)被高估

**有限寿命 vs 无限寿命的分析含义 (Finite-Life vs Indefinite-Life Analysis Implications)：**
- 有限寿命无形资产(finite-life intangibles)需在预计使用寿命内摊销(amortization)，摊销费用影响利润
- 无限寿命无形资产(indefinite-life intangibles)不摊销，但需每年进行减值测试(impairment test)
- 分类直接影响报告利润：无限寿命无形资产无周期性摊销费用，利润波动更小

### 3.2 商誉 (Goodwill)

- **收购剩余 (Acquisition Residual)**：商誉是收购价格超过可辨认净资产公允价值(fair value of net identifiable assets)的部分
- **减值风险 (Impairment Risk)**：IFRS 和 US GAAP 均采用减值测试法(impairment approach)，而非系统摊销。减值发生时直接计入当期损失

### 3.3 金融工具与非流动负债 (Financial Instruments and Non-Current Liabilities)

- 金融资产分类：按摊余成本(amortized cost)、FVOCI(公允价值计入其他综合收益)、FVTPL(公允价值计入当期损益)
- 金融负债的确认和计量，包括债券(bonds)的溢价(premium)和折价(discount)摊销
- 负债的流动性分类(liquidity classification)影响流动比率(current ratio)等短期偿债指标

### 3.4 同比例资产负债表与相关比率 (Common-Size Balance Sheet and Related Ratios)

- 同比例资产负债表将所有项目表示为总资产(total assets)的百分比
- 核心分析维度：资产结构(asset composition)、资本结构(capital structure)、营运资本(working capital)效率

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| 会计等式 | `Assets = Liabilities + Equity` | 资产负债表恒等式 |
| Working Capital | `Current Assets - Current Liabilities` | 营运资本，衡量短期财务健康 |
| Debt-to-Equity | `Total Debt / Total Equity` | 杠杆率，衡量偿债结构 |
| Book Value per Share | `(Total Equity - Pref Equity) / Common Shares Outstanding` | 每股账面价值 |

## 3. 常见考点与解题思路

- **考点1**：外购 vs 内部产生无形资产的会计处理差异。解题思路：区分是 IFRS 还是 US GAAP，再判断资本化条件是否满足
- **考点2**：商誉减值的判断和计算。解题思路：比较报告单元(reporting unit)的账面价值与公允价值——低于公允价值时才确认减值
- **考点3**：金融资产分类对利润表的影响。解题思路：FVOCI 资产公允价值变动计入 OCI 而非利润表，FVTPL 则计入利润表
- **考点4**：同比例资产负债表分析。解题思路：关注资产和负债结构的跨期变化，识别异常变动

## 4. 易错点提醒

- **商誉不减值不摊销**: 现行 IFRS/US GAAP 下，商誉不进行系统摊销，只在出现减值迹象时进行减值测试
- **无形资产分类**: 无形资产是有寿命还是无限寿命，决定了后续处理是摊销还是只做减值测试
- **优先股分类**: 优先股(preferred stock)可能被分类为负债或权益，取决于其经济实质而非法律形式
- **资产负债表外的项目**: 某些租赁(operating leases)和或有负债(contingent liabilities)可能在表外，分析师应查看附注

## 5. 跨模块关联

- [[M06-Long-Term-Assets|长期资产]]：无形资产和 PP&E 的确认、计量与减值处理在本模块基础上进一步展开
- [[M07-Long-Term-Liabilities-and-Equity|长期负债与权益]]：非流动负债的细分类型（租赁、养老金、股权激励）在 M07 详细讨论
- [[M10-Financial-Analysis-Techniques|财务分析技术]]：资产负债表数据是计算 solvency 和 liquidity 比率的直接来源
