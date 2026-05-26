---
title: "M07 — Long-Term Assets"
description: "长期资产全面解析：无形资产来源（外购、内部开发、企业合并）、PP&E与无形资产减值终止确认及披露分析方法"
module: M07
official_module: "M7: Analysis of Long-Term Assets"
subject: Financial_Statement_Analysis
---

# M07: 长期资产分析 (Long-Term Assets Analysis)

## 1. 核心知识点

### 7.1 无形资产来源 (Intangible Asset Origin)

无形资产的会计处理取决于其来源，不同来源的确认条件差异显著：

**外购 (Purchased)：**
- 按购买成本(purchase cost)确认入账，符合资产确认条件(probable future economic benefits and reliable measurement)
- 外购无形资产的成本包括购买价格和直接归属于使资产达到预定用途的支出

**内部开发 (Internally Developed)：**
- US GAAP：研发支出(research and development, R&D)通常全部费用化，仅有特定的软件开发成本(software development costs)在技术可行性确立后资本化
- IFRS：研究阶段(research phase)支出费用化，开发阶段(development phase)支出在满足六项条件时资本化——分析师需注意这种准则差异导致的可比性问题
- 内部开发品牌、客户名单等不得确认为无形资产

**企业合并取得 (Acquired in Business Combination)：**
- 在企业合并(business combination)中，可辨认无形资产按公允价值(fair value)确认
- 这些资产包括客户关系(customer relationships)、技术(technology)、品牌(brands)等
- 合并中确认的无形资产往往比被收购方账面金额更高

### 7.2 PP&E 与无形资产减值/终止确认 (PP&E and Intangible Impairment / Derecognition)

- **PP&E 减值**：当资产的账面价值(carrying amount)超过可收回金额(recoverable amount)时确认减值损失
  - IFRS：可收回金额为公允价值减出售成本与使用价值(value in use)两者中的较高者
  - US GAAP：分两步测试——先比较账面价值与未折现现金流(un-discounted cash flows)，若低于则进行第二步测量减值金额
  - IFRS 允许转回减值(reversal of impairment)，US GAAP 不允许

- **无形资产减值**：有限寿命无形资产减值的处理与 PP&E 类似；无限寿命无形资产和商誉需每年进行减值测试(annual impairment test)

- **终止确认 (Derecognition)**：
  - 出售(disposal)：差额 = 出售收入 - 账面价值，计入利润表
  - 报废(abandonment)：剩余账面价值一次性计入费用

### 7.3 披露分析 (Disclosure Analysis)

- **折旧政策 (Depreciation Policy)**：折旧方法（直线法 straight-line、双倍余额递减法 DDB、产量法 units of production）的选择影响各期利润
- **使用寿命估计 (Useful Life Estimates)**：管理层对使用寿命的估计直接影响年度折旧费用
- **残值估计 (Residual Value Estimates)**：残值越高，年度折旧费用越低
- **分析师调整**：当可比公司的折旧政策存在差异时，分析师需进行调整以实现同口径比较

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| SL Depreciation | `(Cost - Residual Value) / Useful Life` | 直线法折旧 |
| DDB Depreciation | `2 / Useful Life x Net Book Value at Beginning of Year` | 双倍余额递减法折旧 |
| Carrying Amount | `Historical Cost - Accumulated Depreciation - Impairment` | 账面价值 |
| Impairment Loss (IFRS) | `Carrying Amount - Recoverable Amount` | IFRS 减值金额 |
| Gain/Loss on Disposal | `Sale Proceeds - Carrying Amount at Disposal` | 处置损益 |

## 3. 常见考点与解题思路

- **考点1**：内部开发无形资产的资本化条件。解题思路：区分研究阶段(费用化)和开发阶段(有条件资本化)，注意 IFRS 和 US GAAP 对研发支出的不同处理
- **考点2**：资产减值测试。解题思路：IFRS 用可收回金额(recoverable amount)；US GAAP 先用未折现现金流测试，再确认减值
- **考点3**：折旧方法对报表的影响。解题思路：加速折旧法前期折旧高利润低、后期折旧低利润高；直线法利润更平滑
- **考点4**：资产处置的损益计算。解题思路：账面价值与出售收入的差额计入利润表

## 4. 易错点提醒

- **资本化条件的系统化**: 不是所有研发支出都有资格资本化——IFRS 要求区分研究阶段和开发阶段，US GAAP 对大部分研发支出要求费用化
- **折旧估计的变动**: 使用寿命和残值的估计变更是会计估计变更(change in accounting estimate)，采用未来适用法(prospective application)而非追溯调整
- **减值测试差异**: IFRS 有转回机制而 US GAAP 没有——跨准则对比时需注意这一差异的影响
- **折旧不产生现金流**: 折旧是非现金费用(non-cash expense)，在计算 CFO 时需加回

## 5. 跨模块关联

- [[M03-Balance-Sheet|资产负债表]]：长期资产是资产负债表非流动资产(non-current assets)的核心组成部分
- [[M02-Income-Statement|利润表分析]]：折旧和摊销费用直接影响营业利润和净利润
- [[M04-Cash-Flow-Statements|现金流量表]]：折旧加回是间接法 CFO 的关键调整项；资产购买和处置属于投资活动现金流(CFI)
- [[M08-Income-Taxes|所得税]]：资产账面价值与计税基础(tax base)的差异产生递延所得税
