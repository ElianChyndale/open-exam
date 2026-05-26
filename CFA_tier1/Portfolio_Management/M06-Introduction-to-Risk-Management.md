---
title: "M06 — Introduction to Risk Management"
description: "CFA Level I 2026 official module: Introduction to Risk Management"
module: M06
subject: "Portfolio Management"
topic_area: Portfolio_Management
curriculum_year: 2026
official_module: "Module 6: Introduction to Risk Management"
official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25
note_type: official_module_projection
status: active
tags:
  - CFA_L1
  - Portfolio_Management
  - official_2026
---

# M06: Introduction to Risk Management

> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.

## Official Module Structure

- Learning Outcomes: Introduction to Risk Management
- 6.01 | Introduction
- 6.02 | Risk Management Process
- 6.03 | Risk Management Framework
- 6.04 | Risk Governance - An Enterprise View
- 6.05 | Risk Tolerance
- 6.06 | Risk Budgeting
- 6.07 | Identification of Risk - Financial Vs. Non-Financial Risk
- 6.08 | Interactions Between Risks
- 6.09 | Measuring and Modifying Risk: Drivers and Metrics
- 6.10 | Risk Modification: Prevention, Avoidance, and Acceptance
- 6.11 | Risk Modification: Transferring, Shifting, and How to Choose
- 6.12 | Summary

## Learning Outcome Statements

The candidate should be able to:

- define risk management
- describe features of a risk management framework
- define risk governance and describe elements of effective risk governance
- explain how risk tolerance affects risk management
- describe risk budgeting and its role in risk governance
- identify financial and non-financial sources of risk and describe how they may interact
- describe methods for measuring and modifying risk exposures and factors to consider in choosing among the methods

## Local Study Notes

### 🌳 核心知识树

```text
🏆 M06: 风险管理导论 (Introduction to Risk Management)
│
├── 🟢 核心主题：风险管理不是消灭风险
│   └── 目标是使风险与回报目标匹配
│
├── ⭐ 风险管理五步骤
│   ├── 🅰 风险治理 (Governance)
│   │   ├── 建立组织结构、政策、角色职责
│   │   ├── 独立性：风险管理职能与投资决策分离
│   │   └── 董事会层面监督风险框架
│   ├── 🅱 风险识别 (Identification)
│   │   └── 找出影响目标实现的各类风险
│   ├── 🅲 风险计量 (Measurement)
│   │   ├── VaR (风险价值): 给定置信水平下的最小可能损失
│   │   ├── P(ΔP ≤ -VaR) = 1 - α
│   │   └── 其他: 久期、Beta、跟踪误差
│   ├── 🅳 风险改变化 (Modification)
│   │   ├── 规避 (Avoid): 不参与
│   │   ├── 接受 (Accept): 自留风险
│   │   ├── 转移 (Transfer): 保险、衍生品
│   │   ├── 缓释 (Mitigate): 分散化、对冲
│   │   └── 预防 (Prevention): 降低损失概率
│   └── 🅴 风险监控 (Monitoring)
│       └── 持续追踪和报告
│
├── ⭐ 风险分类
│   ├── 金融风险 (Financial Risks)
│   │   ├── 市场风险 (Market risk): 资产价格变动
│   │   ├── 信用风险 (Credit risk): 交易对手违约
│   │   ├── 流动性风险 (Liquidity risk): 无法合理价格交易
│   │   └── 操作风险 (Operational risk): 流程/人员失误
│   └── 非金融风险 (Non-Financial Risks)
│       ├── 法律风险 (Legal risk)
│       ├── 监管风险 (Regulatory risk)
│       ├── 税务风险 (Tax risk)
│       ├── 会计风险 (Accounting risk)
│       ├── 模型风险 (Model risk)
│       ├── 声誉风险 (Reputational risk)
│       └── 尾部风险 (Tail risk)
│
├── ⭐ 风险预算 (Risk Budgeting)
│   ├── 将总风险限额分配到不同资产类别/策略
│   ├── 主动风险预算限制组合偏离基准的最大程度
│   ├── 不是资本预算，关注风险敞口而非资本分配
│   └── 应与投资者目标、资本实力一致
│
├── ⭐ 风险改变化方法比较
│   ├── 规避: 不产生风险，但可能失去收益
│   ├── 接受: 适用于可承受的小风险
│   ├── 转移: 通过保险/衍生品，改变风险承担方
│   ├── 缓释: 通过分散化降低非系统性风险
│   └── 预防: 降低操作风险概率
│
├── 💡 关键洞察
│   ├── 好的风险管理 = 赋能风险承担，不是消灭风险
│   ├── 风险转移 ≠ 风险消失（只是改变承担方）
│   ├── 风险预算 ≠ 资金预算
│   ├── 各风险类型相互关联（如流动性危机常伴随信用危机）
│
└── ⚠️ 考试陷阱
    ├── 风险管理目标不是把风险降到最低
    ├── 风险转移不是风险消失
    ├── 操作风险可能造成重大损失（不是小概率事件）
    ├── VaR 不是最大可能损失
    └── 流动性风险不仅在危机时存在
```

### 📐 关键公式表

| 公式 | 解释 | 使用场景 | ⚠️ 注意 |
|------|------|----------|---------|
| `P(ΔP ≤ -VaR) = 1 - α` | VaR 定义：在 1-α 置信水平下最大损失不超过 VaR | 衡量市场风险 | VaR 不是最大可能损失，是给定置信水平下的分位点 |
| `Tracking Error = σ(Rp - Rb)` | 跟踪误差 = 主动风险 | 衡量主动管理的风险 | 信息比率 = (Rp-Rb)/TE |
| `风险预算偏差 = 实际风险 - 预算限额` | 风险预算执行监控 | 确保主动风险不超限 | 正值为超出预算 |
| `Sharpe = (Rp-Rf)/σp` | 夏普比率 | 风险调整后收益 | 用总风险衡量 |

### 🛠️ 常见考点与解题思路

**考点1：风险分类判断**
- **步骤**：给一个风险描述 → 判断属于哪类风险
- **常见题型**：
  - "市场价格下跌" → 市场风险
  - "交易对手破产" → 信用风险
  - "无法以合理价格平仓" → 流动性风险
  - "交易员误操作" → 操作风险
  - "法规变化" → 监管风险

**考点2：风险管理流程排序**
- **步骤**：给一系列风险管理动作 → 按正确顺序排列
- **正确顺序**：治理 → 识别 → 计量 → 改变化 → 监控

**考点3：风险改变化方式选择**
- **步骤**：给定风险情景 → 选择最合适的方式
- **关键判断**：
  - 保险/衍生品 → 风险转移 (Transfer)
  - 分散化 → 风险缓释 (Mitigate)
  - 不参与 → 风险规避 (Avoid)
  - 自留 → 风险接受 (Accept)

**考点4：VaR 的理解**
- **步骤**：VaR 是给定置信水平下的**最小可能损失**
  - 例如：95% VaR = $1M 意味着有 5% 的概率损失超过 $1M
  - 或者：有 95% 的概率损失不超过 $1M
- **常见陷阱**：误以为 VaR 是最大可能损失

### 🚨 易错点与考试陷阱

| ❌ 错误理解 | ✅ 正确理解 | 原因 |
|-----------|-----------|------|
| 风险管理目标 = 风险最小化 | 目标是使风险与回报目标匹配 | 风险承担才能获得收益 |
| 风险转移 = 风险消失 | 风险转移只是改变了承担方，系统性风险无法转移 | 对手仍可能违约 |
| 操作风险是次要的 | 操作风险（如交易员错误、系统故障）可能造成重大损失 | 巴塞尔协议重点监管 |
| VaR 是最大损失 | VaR 是给定置信水平下的最小可能损失 | 尾部损失可能远大于 VaR |
| 风险预算 = 资金预算 | 风险预算分配风险限额，不是资金 | 概念用途不同 |
| 流动性风险只在危机时 | 流动性风险在正常市场也可能存在 | 某些资产本身流动性差 |
| 风险管理只是风控部门的事 | 风险管理是每个投资决策的一部分 | 嵌入到全流程 |
| 各种风险独立存在 | 风险之间相互关联（信用风险 → 流动性风险） | 风险传染效应 |

### 🔄 跨模块关联

- **[[M01-Portfolio-Risk-and-Return-Part-I]]** — 风险概念源于组合收益的波动性，分散化是风险缓释的核心方法
- **[[M02-Portfolio-Risk-and-Return-Part-II]]** — 系统性风险是 CAPM 的定价基础，也是风险管理的重要维度
- **[[M04-Basics-of-Portfolio-Planning-and-Construction]]** — 风险预算是组合构建的关键组成部分（修复旧链接 `[[M04-Market-Efficiency-and-Portfolio-Construction]]`）
- **[[M05-The-Behavioral-Biases-of-Individuals]]** — 行为偏差可能误导风险判断（修复旧链接 `[[M06-Behavioral-Biases]]`）
- **[[M03-Derivative-Benefits-Risks-and-Issuer-and-Investor-Uses]]** (Derivatives) — 衍生品作为风险转移工具
- **[[00-Portfolio-Management-MOC]]** — 返回科目总览

### 📋 复习与刷题提示

- M06 是 Portfolio Management 的**最后一个模块**，以概念为主
- **核心能力**：风险分类、风险管理流程理解、改变化方法选择
- **必考题型**：风险类型判断、流程排序、风险改变化选择、VaR 理解
- **最常犯错误**：风险管理目标理解偏差（以为最小化就是目标）、VaR 定义混淆
- 记忆重点：
  - 五步骤：治理 → 识别 → 计量 → 改变化 → 监控
  - 金融风险四类: 市场、信用、流动性、操作
  - 改变化五方式: 规避、接受、转移、缓释、预防
  - VaR = "至少有 1-α 的把握损失不超过 X"
- 核心原则：风险管理是赋能（enable），不是束缚（constrain）
