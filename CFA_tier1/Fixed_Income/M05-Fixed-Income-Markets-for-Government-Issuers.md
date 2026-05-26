---
title: "M05: Fixed-Income Markets for Government Issuers"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M05"
official_module: "Module 5: Fixed-Income Markets for Government Issuers"
los_count: 2
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M05: Fixed-Income Markets for Government Issuers

> **模块定位**：从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。 本模块聚焦 **Fixed-Income Markets for Government Issuers**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Fixed-Income Markets for Government Issuers
- 5.01 | Introduction
- 5.02 | Sovereign Debt
- 5.03 | Sovereign Debt Issuance and Trading
- 5.04 | Non-Sovereign, Quasi-Government, and Supranational Agency Debt

## Learning Outcome Statements

1. describe funding choices by sovereign and non-sovereign governments, quasi-government entities, and supranational agencies
2. contrast the issuance and trading of government and corporate fixed-income instruments

---

## 1. 模块定位

### 5.1 学习任务
- **核心问题**：考试希望你用 `Fixed-Income Markets for Government Issuers` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 5.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 5.3 关键英文术语
- **Fixed-Income Markets for Government Issuers（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Sovereign Debt（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Sovereign Debt Issuance and Trading（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Non-Sovereign, Quasi-Government, and Supranational Agency Debt（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Fixed Income（固定收益）**：以约定现金流为核心的债务类证券。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 5.1 | describe funding choices by sovereign and non-sovereign governments, quasi-government entities, and supranational agencies | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 5.2 | contrast the issuance and trading of government and corporate fixed-income instruments | 识别概念、解释机制并应用到题干。 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
5. Fixed-Income Markets for Government Issuers
├─ 5.1 主权债券 (Sovereign Bonds)
│  ├─ 5.1.1 Sovereign bonds 是中央政府债务；发达市场常作 risk-free benchmark，新兴市场需看信用/外汇风险
│  ├─ 5.1.2 Local currency vs foreign currency：本币债有货币政策灵活性，外币债依赖外汇收入与储备
│  └─ 5.1.3 T-bills/notes/bonds 构成 benchmark curve，连接 M09 term structure
├─ 5.2 政府机构债券 (Government Agency Debt)
│  ├─ 5.2.1 Agency/quasi-government debt 可能有显性担保、隐性支持或无政府担保
│  ├─ 5.2.2 Spread 取决于支持强度、使命重要性、独立财务状况和流动性
│  └─ 5.2.3 不要把所有 agency debt 直接当 sovereign risk-free
├─ 5.3 超国家债券 (Supranational Bonds)
│  ├─ 5.3.1 Supranational issuers 由多个国家支持，如 World Bank、EIB、ADB
│  ├─ 5.3.2 信用品质来自成员国资本承诺、preferred creditor status 和资产质量
│  └─ 5.3.3 常作为高信用质量跨国债券，与 sovereign curve 仍可能有 spread
├─ 5.4 市政债券 (Municipal Bonds)
│  ├─ 5.4.1 GO bonds 由一般税收支持；revenue bonds 由项目收入支持
│  ├─ 5.4.2 Taxable equivalent yield = tax-exempt yield/(1 - tax rate)
│  └─ 5.4.3 判断应税/免税收益率时，先确认投资者税率和收益是否 tax-exempt
├─ 5.5 国债期限结构 (Treasury Maturity Structure)
│  ├─ 5.5.1 Bills/notes/bonds 区分短中长期政府融资，也提供 curve construction 的市场输入
│  └─ 5.5.2 Inflation-linked：adjusted principal = original principal x current CPI/base CPI；保护 purchasing power
```

## 4. 知识点详解

### 5.1 主权债券 (Sovereign Bonds)

- **主权债券 (sovereign bonds)**：由中央政府发行的本币或外币债务工具。本币主权债券通常被视为该国无风险利率的基准。外币主权债券面临汇率风险和主权违约风险。
- **发达经济体主权债**：美国国债 (Treasuries)、英国金边债券 (Gilts)、日本国债 (JGBs)、德国国债 (Bunds) 等。信用风险极低，是全球固定收益市场的定价基准。
- **新兴市场主权债**：信用风险高于发达经济体，收益率更高。发行货币可以是本币或外币（多为美元）。新兴市场主权债受大宗商品价格、政治稳定性和资本流动影响大。
- **通胀挂钩主权债券 (inflation-linked sovereign bonds)**：本金随通胀指数调整的政府债券。典型产品包括美国的 TIPS (Treasury Inflation-Protected Securities)、英国的 Index-Linked Gilts。提供对通胀风险的直接对冲。

### 5.2 政府机构债券 (Government Agency Debt)

- **准政府/政府机构债券 (quasi-government / agency bonds)**：由政府设立或资助的机构发行的债务工具，信用质量接近但不等同于主权信用。发行主体包括开发银行、出口信贷机构和住房金融机构。
- **美国机构债券**：Fannie Mae（房利美）、Freddie Mac（房地美）发行的机构债券和 MBS。金融危机后处于政府监护 (conservatorship) 状态，带有隐性政府担保。Ginnie Mae（吉利美）则由美国政府完全信用担保。
- **机构债券的特点**：收益率略高于同等期限国债（反映隐性而非显性政府担保），流动性通常较好，适合追求高流动性和高信用质量的投资者。

### 5.3 超国家债券 (Supranational Bonds)

- **超国家债券 (supranational bonds)**：由多个国家共同设立的国际金融机构发行的债券。主要发行机构包括世界银行 (World Bank / IBRD)、国际货币基金组织 (IMF)、欧洲投资银行 (EIB)、亚洲开发银行 (ADB) 等。
- **超国家债券的特点**：信用评级通常为 AAA，因成员国资本支持和优先债权人地位。收益率接近但略高于同等期限主权债券。发行用途多为支持成员国的开发项目。
- **社会与绿色债券**：超国家机构是绿色债券和社会债券的主要发行人，募集资金专门用于环境或社会效益项目。

### 5.4 市政债券 (Municipal Bonds)

- **市政债券 (municipal bonds / munis)**：由地方政府、州、市或特区发行的债务工具，用于为公共项目（学校、公路、医院、公用事业）融资。仅存在于部分国家（以美国最为发达）。
- **一般义务债券 (general obligation bonds, GO bonds)**：以发行人的全部信用和征税权作为担保，还款来源为税收收入。信用质量取决于发行人的财政健康状况和税基。
- **收益债券 (revenue bonds)**：以特定项目产生的收入（如通行费、水电费、机场费用）作为还款来源，而非发行人的一般税收。风险高于 GO 债券，取决于项目的现金流产生能力。
- **市政债券的税收优势**：在美国，多数市政债券的利息收入免征联邦所得税，部分还免征州和地方税（对同一州居民）。这一税收优惠使市政债券的税前收益率低于应税债券但税后收益率具有竞争力。

### 5.5 国债期限结构 (Treasury Maturity Structure)

- **短期国债 (T-bills, Treasury bills)**：期限1年以内，贴现发行，无票息。货币市场工具，流动性极高。
- **中期国债 (T-notes, Treasury notes)**：期限2至10年，每半年付息一次。是美国国债市场的主要品种。
- **长期国债 (T-bonds, Treasury bonds)**：期限10年以上（通常20年或30年），每半年付息一次。
- **STRIPS (Separate Trading of Registered Interest and Principal of Securities)**：将国债的每期票息和最终本金分离为独立的零息债券进行交易。

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标 | 公式/关系 | 说明 |
|------|-----------|------|
| TIPS 实际收益率 | `Nominal Yield ≈ Real Yield + Expected Inflation + Risk Premium` | 费雪效应的近似 |
| TIPS 本金调整 | `Adjusted Principal = Original Principal × (Current CPI / Base CPI)` | 通胀挂钩债券的本金 |
| 市政债券税收等价收益率 | `Taxable Equivalent Yield = Tax-Exempt Yield / (1 - Tax Rate)` | 比较市政债与应税债 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 5.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 5.2 Sovereign Debt | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.3 Sovereign Debt Issuance and Trading | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.4 Non-Sovereign, Quasi-Government, and Supranational Agency Debt | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

- **区分不同类型政府债务的信用风险**：主权（中央）> 机构（准政府）> 超国家 > 市政。但具体等级取决于发行人的财政实力。
- **计算市政债券的税收等价收益率**：给定市政债券收益率和投资者边际税率，计算同等应税债券所需收益率。考试中常比较市政债券和公司债券的税后收益。
- **区分一般义务债券 vs 收益债券**：GO 以税收支持，收益债券以项目收入支持。收益债券风险更高。
- **理解 TIPS 的功能**：TIPS 保护购买力，实际收益率在发行时确定，通胀调整体现在本金上。
- **区分不同类型国债的期限和特征**：T-bill（短期、贴现）、T-note（中期、附息）、T-bond（长期、附息）。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：主权债券不一定是无风险的【考试陷阱】：即使是美国国债，从利率风险和通胀风险角度看并非无风险。主权违约风险在新兴市场中真实存在。 | ✅ 主权债券不一定是无风险的【考试陷阱】：即使是美国国债，从利率风险和通胀风险角度看并非无风险。主权违约风险在新兴市场中真实存在。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：机构债券的隐性担保不等于显性担保：Fannie Mae / Freddie Mac 的债券并非由美国政府全额信用担保（金融危机时被接管证明了隐性担保的部分有效性）。 | ✅ 机构债券的隐性担保不等于显性担保：Fannie Mae / Freddie Mac 的债券并非由美国政府全额信用担保（金融危机时被接管证明了隐性担保的部分有效性）。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：市政债券的税收优势不适用于所有投资者：税收优惠对高税率投资者最有价值；免税地位可能因投资者所在州而不同。 | ✅ 市政债券的税收优势不适用于所有投资者：税收优惠对高税率投资者最有价值；免税地位可能因投资者所在州而不同。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：通胀挂钩债券的收益率不是名义收益率的直接替代：实际收益率和通货膨胀补偿的分离是理解 TIPS 定价的关键。 | ✅ 通胀挂钩债券的收益率不是名义收益率的直接替代：实际收益率和通货膨胀补偿的分离是理解 TIPS 定价的关键。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：超国家债券的 AAA 评级受益于成员国支持和优先债权人地位，但这不意味着零风险。超国家机构可能因成员国违约而遭受损失。 | ✅ 超国家债券的 AAA 评级受益于成员国支持和优先债权人地位，但这不意味着零风险。超国家机构可能因成员国违约而遭受损失。 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 接口 | 连接模块 | 本模块输出 | 做题用途 |
|---|---|---|---|
| Benchmark curve | [[M09-The-Term-Structure-of-Interest-Rates-Spot-Par-and-Forward-Curves]] | sovereign yield curve、T-bills/notes/bonds | 构造 spot/par/forward curve |
| Government spread | [[M07-Yield-and-Yield-Spread-Measures-for-Fixed-Rate-Bonds]] | government benchmark yield | 计算 benchmark/G-spread |
| Sovereign credit | [[M15-Credit-Analysis-for-Government-Issuers]] | local vs foreign currency、agency support | 判断主权/准政府信用风险 |
| 税收与通胀 | Portfolio Management / Economics | taxable equivalent yield、TIPS CPI adjustment | 比较 after-tax/real return |

- **上游模块**：[[M04-Fixed-Income-Markets-for-Corporate-Issuers]]。先用它提供定义、变量或基础框架。
- **下游模块**：[[M06-Fixed-Income-Bond-Valuation-Prices-and-Yields]]。本模块输出会被后续更复杂题型调用。

### Legacy 关联补充

- 国债收益率基准 → [[M04-Yield-and-Spread-Measures]] 利差度量以国债为基准
- 主权信用分析 → [[M15-Credit-Analysis-for-Government-Issuers]] 主权评级因素
- 通胀保护 → [[M02-Fixed-Income-Cash-Flows]] 通胀挂钩现金流结构
- 短期国债 → [[M05-Floating-Rate-and-Money-Market]] 货币市场工具与收益率
- 市政债税收 → [[M14-Credit-Risk]] 信用风险与税收维度的区分


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M05-FI-Markets-Government-Issuers.md` (high, 0.587)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
