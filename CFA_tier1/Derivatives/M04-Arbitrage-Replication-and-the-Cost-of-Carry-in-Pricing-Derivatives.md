---
title: "M04: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
description: "CFA Level I 2026 Derivatives 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Derivatives"
topic_area: "Derivatives"
level: "CFA Level I"
exam_year: 2026
exam_weight: "5-8%"
module: "M04"
official_module: "Module 4: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives"
los_count: 2
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Derivatives
---

# M04: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives

> **模块定位**：用无套利、复制和工具结构理解远期、期货、互换、期权的风险转移。 本模块聚焦 **Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

- Learning Outcomes: Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives
- 4.01 | Introduction
- 4.02 | Arbitrage
- 4.03 | Replication
- 4.04 | Costs and Benefits Associated with Owning the Underlying

## Learning Outcome Statements

1. explain how the concepts of arbitrage and replication are used in pricing derivatives
2. explain the difference between the spot and expected future price of an underlying and the cost of carry associated with holding the underlying asset

---

## 1. 模块定位

### 4.1 学习任务
- **核心问题**：考试希望你用 `Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### 4.2 考试角色
- **难度类型**：概念+应用。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### 4.3 关键英文术语
- **Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Introduction（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Arbitrage（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Replication（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。
- **Costs and Benefits Associated with Owning the Underlying（核心术语）**：本模块关键词，用于定位 LOS、题干条件和解题动作。

## 2. 官方 LOS 对应学习目标

| LOS | 官方要求 | 中文学习动作 | 做题输出 |
|---|---|---|---|
| 4.1 | explain how the concepts of arbitrage and replication are used in pricing derivatives | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |
| 4.2 | explain the difference between the spot and expected future price of an underlying and the cost of carry associated with holding the underlying asset | 解释机制、原因和后果 | 写出结论、依据、公式口径和限制条件。 |

## 3. 核心知识树

```text
4. Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives
├─ 4.1 核心内容
│  ├─ 4.1.1 Law of one price：相同未来现金流必须同价
│  ├─ 4.1.2 Arbitrage：零净投资、无风险、正收益机会；错价时买便宜现金流卖贵现金流
│  ├─ 4.1.3 Replication：用现货+借贷复制衍生品现金流，复制成本决定公平价格
│  ├─ 4.1.4 Cost of carry：financing + storage - income/yield - convenience benefit
│  └─ 4.1.5 公式选择：无收益、已知现金收入、收益率/便利收益三类不能混用
```

## 4. 知识点详解

### 4.1 核心内容

**无套利逻辑 (No-Arbitrage Logic)**
- **一价定律 (Law of One Price)**：相同未来现金流的资产应有相同价格 (identical future cash flows must have the same price)
- **复制组合 (Replication Portfolio)**：用现货+融资复制衍生品收益，确定公平价格 (replication portfolio pins fair derivative price)
- **套利行为 (Arbitrage Action)**：错误定价时，套利者交易将价格推回公平关系 (arbitrage pushes mispriced contract back to fair relation)

**持有成本关系 (Carry Relation)**

| 因素 | 对远期价格的影响 |
|------|-----------------|
| 融资成本 (Financing Cost) | 提高远期价格 (raises forward price) |
| 已知收入 (Known Income) | 减少持有成本 (reduces net carry) |
| 收益率/便利收益 (Yield/Convenience) | 减少持有成本 (reduces net carry) |

**关键公式**
- `Forward price = Spot + Carry - Benefit`
- `Carry = Financing cost - Income/Yield/Convenience`

## 5. 关键公式与计算框架

### 5.1 核心内容

无收益资产远期价格：
```
F0(T) = S0(1+r)^T
```

已知收入资产远期价格：
```
F0(T) = [S0 - PV(I)](1+r)^T
```

已知收益率资产远期价格：
```
F0(T) = S0[(1+r)/(1+q)]^T    或连续口径：S0e^((r-q)T)
```

| 节点 | 公式/框架 | 选择条件 | 考试判断 |
|---|---|---|---|
| 4.1.2 | Cash-and-carry | market forward price > fair forward price | buy underlying、short forward、borrow funding。 |
| 4.1.2 | Reverse cash-and-carry | market forward price < fair forward price | short underlying、long forward、invest proceeds。 |
| 4.1.4 | `F0 = S0(1+r)^T` | 标的无收入、离散复利 | financing cost 是唯一 carry。 |
| 4.1.4 | `F0 = [S0 - PV(I)](1+r)^T` | 已知现金收入 | 先扣收入现值，再滚到到期。 |
| 4.1.4 | `F0 = S0[(1+r)/(1+q)]^T` 或 `S0e^{(r-q)T}` | 已知收益率或连续收益率 | q 降低 net carry；复利口径必须与题干一致。 |
| 4.1.4 | `F0 = S0e^{(r+storage-convenience)T}` | 商品或储存/便利收益题 | storage 提高 forward price，convenience benefit 降低 forward price。 |

## 6. 常见考点与解题思路

| 重要性 | 考点 | 解题动作 |
|---|---|---|
| ⭐⭐⭐ | 4.1 Introduction | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐⭐ | 4.2 Arbitrage | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 4.3 Replication | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |
| ⭐⭐ | 4.4 Costs and Benefits Associated with Owning the Underlying | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |

### 6.9 ⭐⭐ Legacy 考点补充

### 6.1 核心内容

1. 先判断资产的收益类型（无收益 / 已知收入 / 已知收益率）
2. 代入对应 carry 公式计算 fair forward price
3. 若市场价格偏离公平价格，设计套利策略：
   - 价格偏高 → short forward + buy underlying + borrow (cash-and-carry)
   - 价格偏低 → long forward + short underlying + invest (reverse cash-and-carry)
4. 验证复制组合的现金流是否匹配

## 7. 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |
|---|---|---|
| ❌ 忽略：【考试陷阱】期初价格 (price at initiation) 与存续期价值 (value during life) 并非同一概念 —— 价格是使初始价值为零的公平交割价，价值… | ✅ 【考试陷阱】期初价格 (price at initiation) 与存续期价值 (value during life) 并非同一概念 —— 价格是使初始价值为零的公平交割价，价值… | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：已知收入要先折现再扣除，不能直接用未来值相减 | ✅ 已知收入要先折现再扣除，不能直接用未来值相减 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |
| ❌ 忽略：连续复利与离散复利公式不要混用，注意题目给的是年利率还是连续利率 | ✅ 连续复利与离散复利公式不要混用，注意题目给的是年利率还是连续利率 | 题干通常会用口径、顺序、定义边界或例外条件设置干扰。 |

## 8. 跨模块关联

| 连接 | 传递内容 | 做题用途 |
|---|---|---|
| `M03 -> M04` | arbitrage motive vs hedge/speculation | 只有无风险同现金流错价才是套利。 |
| `M04 -> M05/M06` | cost-of-carry and replication | 远期/期货价格公式的来源。 |
| `M04 -> M09` | same-payoff equality | put-call parity 是无套利复制关系。 |
| `M04 -> M10` | replication portfolio | binomial hedge ratio 和借贷头寸来自复制思想。 |
| `Economics/Fixed Income -> M04` | risk-free rate、income/yield、storage/convenience | 定价输入来自利率、收益率和持有成本。 |


## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：`M04-Arbitrage-and-Replication.md` (medium, 0.416)
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
