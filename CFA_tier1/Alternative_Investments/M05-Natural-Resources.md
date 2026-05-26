---
title: "M05: Natural Resources"
description: "CFA Level I 2026 Alternative Investments 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Alternative Investments"
topic_area: "Alternative_Investments"
level: "CFA Level I"
exam_year: 2026
exam_weight: "7-10%"
module: "M05"
official_module: "Module 5: Natural Resources"
los_count: 3
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Alternative_Investments
---

# M05: Natural Resources

> **模块定位**：识别另类投资结构、绩效、私募、实物资产、对冲基金与数字资产特征。 本模块聚焦 **Natural Resources**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Natural Resources
- 5.01 | Introduction
- 5.02 | Natural Resources Investment Features
- 5.03 | Commodity Investment Forms
- 5.04 | Natural Resource Investment Risk, Return, and Diversification

## Learning Outcome Statements

1. explain features of raw land, timberland, and farmland and their investment characteristics
2. describe features of commodities and their investment characteristics
3. analyze sources of risk, return, and diversification among natural resource investments

---

## 1. 模块定位

### 5.1 学习任务
- **核心问题**：考试希望你用 `Natural Resources` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 5.2 考试角色
- **难度类型**：计算+解释。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 5.3 关键英文术语
- **Natural Resources（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Natural Resources Investment Features（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Commodity Investment Forms（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Natural Resource Investment Risk, Return, and Diversification（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 5.1 | explain features of raw land, timberland, and farmland and their investment characteristics | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 5.2 | describe features of commodities and their investment characteristics | 描述定义、流程和适用场景 | 写出结论、依据、公式口径和限制条件。 |
| 5.3 | analyze sources of risk, return, and diversification among natural resource investments | 识别概念、解释机制并应用到题干。 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
5. Natural Resources
├─ 5.1 Natural resources investment features
│  ├─ 5.1.1 Raw land：收益依赖土地价格增值和开发选择权；现金流弱、流动性低、政策/规划风险高。
│  ├─ 5.1.2 Timberland：收益来自木材生长、采伐时点选择和土地价值；有通胀保护但有天气/病虫害风险。
│  └─ 5.1.3 Farmland：收益来自农产品销售/租金和土地升值；受天气、商品价格、补贴和水资源影响。
├─ 5.2 Commodity investment forms
│  ├─ 5.2.1 Physical spot：有存储、保险和运输成本，适合少数商品。
│  ├─ 5.2.2 Futures exposure：收益不等于 spot return，还包含 roll yield 和 collateral yield。
│  └─ 5.2.3 Commodity-linked equities/funds：含经营杠杆和公司风险，不是纯商品 beta。
├─ 5.3 商品期货 (Commodity Futures)【考试核心】
│  ├─ 5.3.1 Cost of carry：F0(T)=S0e^((r+s-y)T)，storage cost 提高期货价，convenience yield 降低期货价。
│  ├─ 5.3.2 Contango/backwardation：远期高于近月通常 contango，多头展期收益为负；反之 backwardation 通常为正。
│  └─ 5.3.3 Total return：spot return + roll yield + collateral yield；考试常要求分清三来源。
├─ 5.4 Risk, return, and diversification
│  ├─ 5.4.1 风险来源：weather、geopolitics、currency、storage、regulation、leverage、liquidity。
│  └─ 5.4.2 分散化：通胀和供需冲击可能带来低相关，但期货期限结构会改变投资结果。
```

## 4. 知识点详解

### 5.1 商品期货 (Commodity Futures)【考试核心】

#### 5.1.1 期货定价理论

**持有成本模型 (Cost of Carry)**:

期货价格 (Futures Price) = 现货价格 × e^{((r + s - y) × T)}

| 变量 | 含义 |
|------|------|
| r | 无风险利率 (Risk-Free Rate) |
| s | 存储成本 (Storage Cost) |
| y | 便利收益 (Convenience Yield) |
| T | 到期时间 |

**便利收益 (Convenience Yield)**: 持有实物商品的额外好处（如防止供应中断），是持有成本的对冲项

#### 5.1.2 Contango (正向市场) vs Backwardation (反向市场)

| 维度 | Contango (正向市场) | Backwardation (反向市场) |
|------|--------------------|------------------------|
| 价格关系 | 期货价格 > 现货价格 | 期货价格 < 现货价格 |
| Roll Yield | 负 (不利) | 正 (有利) |
| 驱动因素 | 存储成本高 / 便利收益低 | 便利收益高（现货稀缺） |
| 投资者影响 | 长期持期货有损耗（展期亏损） | 长期持期货有收益（展期获利） |
| 市场状态 | 期货溢价，远期贴水预期 | 期货贴水，现货稀缺 |

#### 5.1.3 Roll Yield (展期收益)

Roll Yield = (近期期货 - 远期期货) / 近期期货

- **Contango下**: 近期期货 < 远期期货 → Roll Yield为负
- **Backwardation下**: 近期期货 > 远期期货 → Roll Yield为正

**本质**: 展期收益/成本，由期货期限结构 (Term Structure) 决定

#### 5.1.4 商品期货投资策略

- **被动投资 (Passive)**: 指数跟踪，需考虑期限结构影响
- **主动投资 (Active)**: 期限结构套利、现货-期货套利

## 5. 关键公式与计算框架

### 5.1 核心内容

| 指标/框架 | 公式或判断链 | 知识树节点 | 考试说明 |
|------|------|------|------|
| 期货定价 | `F_0(T) = S_0e^((r + s - y)T)` | `5.3.1` | r=利率，s=存储成本，y=便利收益 |
| 持有成本率 | `ln[F_0(T)/S_0] / T = r + s - y` | `5.3.1` | 连续复利口径 |
| Roll Yield | `(near futures price - far futures price) / near futures price` | `5.3.2` | 多头展期：contango 通常负，backwardation 通常正 |
| Commodity futures total return | `spot return + roll yield + collateral yield` | `5.3.3` | 不要只看现货涨跌 |
| Natural resource screen | `income yield + biological/land growth + commodity price exposure - operating/weather/regulatory risk` | `5.1/5.4` | 用于 raw land/timberland/farmland 解释题 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 5.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 5.2 Natural Resources Investment Features | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.3 Commodity Investment Forms | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 5.4 Natural Resource Investment Risk, Return, and Diversification | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

1. **Contango vs Backwardation判断**: 给定近期和远期期货价格，判断市场状态。**思路**: 远期 > 近期 = Contango；近期 > 远期 = Backwardation。
2. **Roll Yield计算**: 给定近期和远期期货价格，计算Roll Yield。**思路**: Roll Yield = (Near - Far) / Near。Contango下为负，Backwardation下为正。
3. **便利收益影响分析**: 现货稀缺时便利收益高，导致Backwardation。**思路**: 便利收益高 → Backwardation → 正Roll Yield。
4. **期货定价计算**: 给定现货价格、利率、存储成本、便利收益和期限，计算期货价格。**思路**: 使用持有成本公式F = S × e^{(r+s-y)T}。

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：Contango ≠ 正Roll Yield: Contango（期货>现货）= 负Roll Yield（展期亏损） | ✅ Contango ≠ 正Roll Yield: Contango（期货>现货）= 负Roll Yield（展期亏损） | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：Backwardation ≠ 负Roll Yield: Backwardation（期货<现货）= 正Roll Yield（展期获利） | ✅ Backwardation ≠ 负Roll Yield: Backwardation（期货<现货）= 正Roll Yield（展期获利） | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：便利收益是持有成本的对冲项: 公式中便利收益(y)降低期货价格，而非增加 | ✅ 便利收益是持有成本的对冲项: 公式中便利收益(y)降低期货价格，而非增加 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：商品现货实物持有: 商品期货定价基础是实物商品的持有成本，与金融期货不同 | ✅ 商品现货实物持有: 商品期货定价基础是实物商品的持有成本，与金融期货不同 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：被动投资也有主动决策: 即使是被动指数跟踪，也需要考虑展期策略 | ✅ 被动投资也有主动决策: 即使是被动指数跟踪，也需要考虑展期策略 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

- **来自 M01**：自然资源可能通过 direct ownership、funds、commodity futures 或 commodity-linked equities 投资，结构决定风险。
- **来自 M04**：raw land/farmland 与 real estate 共享土地估值、流动性和宏观周期，但现金流驱动不同。
- **到 Derivatives**：commodity futures 的 cost of carry、roll yield、collateral yield 是最强接口。
- **到 Economics/PM**：通胀、供需冲击、汇率和商业周期影响商品价格和组合分散化。
- **到 Ethics**：commodity-linked 产品推荐要披露期货展期风险，不能只用现货价格叙事。


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M05-Natural-Resources.md` (medium, 0.406)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
