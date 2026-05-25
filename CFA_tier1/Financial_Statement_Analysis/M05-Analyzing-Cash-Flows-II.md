---
title: "M05 — Analyzing Statements of Cash Flows II"
description: "现金流量表分析II：自由现金流（FCFF与FCFE）、现金流比率分析、同比例现金流量表及现金流趋势分析"
module: M05
official_module: "M5: Analyzing Statements of Cash Flows II"
subject: Financial_Statement_Analysis
---

# M05: 现金流量表分析 II (Analyzing Statements of Cash Flows II)

## 1. 核心知识点

### 5.1 报告式与同比例现金流量表 (Reported vs Common-Size Cash Flow Statements)

- **报告式现金流量表 (Reported Cash Flow Statement)**：按 CFO、CFI、CFF 三大分类列示现金收支，反映企业现金的实际来源与运用
- **同比例现金流量表 (Common-Size Cash Flow Statement)**：可将各项目表示为收入(revenue)或总现金流入/流出的百分比，便于跨期和跨公司比较
- 同比例分析有助于识别现金流结构的异常变化，如经营现金流占比持续下降可能是盈利质量恶化的信号

### 5.2 自由现金流 (Free Cash Flow)

**公司自由现金流 (FCFF — Free Cash Flow to the Firm)：**
- 定义：衡量公司对所有资本提供者（股东和债权人）的可供现金流
- 特点：在满足经营和投资需求后，可供分配给所有资本提供者的剩余现金流
- 用途：企业价值评估(DCF 模型)的输入变量

**股权自由现金流 (FCFE — Free Cash Flow to Equity)：**
- 定义：衡量公司对普通股股东的可供现金流
- 特点：在满足经营、投资和偿债需求后，可供分配给股东的剩余现金流
- 用途：股权价值评估的输入变量

#### 核心公式 (English)
- `FCFF = CFO + Interest(1 - T) - FCInv`
- `FCFE = CFO - FCInv + Net Borrowing`

### 5.3 现金流比率分析 (Cash Flow Ratio Analysis)

**业绩现金流比率 (Performance Cash Flow Ratios)：**
- 经营现金流比率 (CFO / Current Liabilities)：衡量经营现金流覆盖短期债务的能力
- 现金流覆盖比率 (Cash Flow Coverage Ratio)：衡量经营现金流覆盖总债务的能力
- 现金流利润率 (Cash Flow Margin)：CFO / Revenue，衡量每单位收入转化为经营现金流的效率

**覆盖现金流比率 (Coverage Cash Flow Ratios)：**
- 债务覆盖比率 (Debt Coverage Ratio)：CFO / Total Debt
- 利息覆盖比率 (Cash Interest Coverage)：(CFO + Interest Paid + Taxes Paid) / Interest Paid

**现金流趋势分析 (Cash Flow Trend Analysis)：**
- 多期 CFO 趋势：CFO 增长应与利润增长趋势基本一致，显著背离可能暗示盈利质量下降
- CFO 与 NI 的关系：CFO > NI 通常意味着盈利质量较高；CFO 持续低于 NI 可能反映激进的收入确认或营运资本恶化
- 自由现金流趋势：FCFF/FCFE 长期为负可能表明公司需要外部融资

## 2. 关键公式

| 指标 | 公式 | 说明 |
|------|------|------|
| FCFF | `CFO + Interest(1 - T) - FCInv` | 公司自由现金流 |
| FCFE | `CFO - FCInv + Net Borrowing` | 股权自由现金流 |
| CFO / CL | `CFO / Current Liabilities` | 经营现金流比率，衡量短期偿债能力 |

## 3. 常见考点与解题思路

- **考点1**：FCFF/FCFE 的计算与区别。解题思路：FCFF 给所有资本提供者，FCFE 只给股东；两者关系为 FCFF - Interest(1-T) + Net Borrowing = FCFE
- **考点2**：现金流比率的计算与解读。解题思路：CFO 比率衡量的是现金流层面的偿债能力，比利润层面的比率更真实
- **考点3**：同比例现金流量表分析。解题思路：关注各分类现金流的占比趋势，尤其注意经营现金流占比的持续变化
- **考点4**：现金流与盈利质量的判断。解题思路：CFO 与 NI 的长期背离是盈利质量分析的重要线索

## 4. 易错点提醒

- **FCFF vs FCFE 的调整差异**: 计算 FCFF 时加回税后利息，FCFE 不再加回——很多考生在调整细节上丢分
- **FCInv (资本支出) 的扣减**: 计算 FCFF 和 FCFE 时都需扣减 FCInv，这是维持经营所必需的现金支出
- **Net Borrowing 的方向**: 净借款为正(新增借款)增加 FCFE，为负(偿还借款)减少 FCFE
- **现金流比率 vs 利润比率**: 现金流比率基于已实现现金，不易被会计政策操纵，但波动性可能更大

## 5. 跨模块关联

- [[M04-Analyzing-Cash-Flows-I|现金流量表分析 I]]：FCFF/FCFE 的计算以 CFO 为基础，需先掌握间接法编制
- [[M11-Financial-Analysis-Techniques|财务分析技术]]：现金流比率是偿债能力和盈利质量分析的重要工具，与 DuPont 分析互为补充
