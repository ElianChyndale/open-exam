---
title: "00-Derivatives-MOC"
description: "CFA Level I 2026 Derivatives 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "Derivatives"
topic_area: "Derivatives"
level: "CFA Level I"
exam_year: 2026
exam_weight: "5-8%"
module_count: 10
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - Derivatives
---

# Derivatives MOC

> **一句话核心**：用无套利、复制和工具结构理解远期、期货、互换、期权的风险转移。

---

## 1. 科目定位

- **考试权重**：5-8%
- **官方模块数**：10
- **主线框架**：识别标的与到期现金流 -> 建立无套利关系 -> 定价/估值 -> 判断风险暴露
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |
|---|---|---|---|---|
| M01 | Derivative Instrument and Derivative Market Features | 概念+应用 | Introduction / Derivative Features | [[M01-Derivative-Instrument-and-Derivative-Market-Features]] |
| M02 | Forward Commitment and Contingent Claim Features and Instruments | 概念+应用 | Introduction / Forwards, Futures, and Swaps | [[M02-Forward-Commitment-and-Contingent-Claim-Features-and-Instruments]] |
| M03 | Derivative Benefits, Risks, and Issuer and Investor Uses | 概念+应用 | Introduction / Derivative Benefits | [[M03-Derivative-Benefits-Risks-and-Issuer-and-Investor-Uses]] |
| M04 | Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives | 概念+应用 | Introduction / Arbitrage | [[M04-Arbitrage-Replication-and-the-Cost-of-Carry-in-Pricing-Derivatives]] |
| M05 | Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities | 计算+解释 | Introduction / Pricing and Valuation of Forward Contracts | [[M05-Pricing-and-Valuation-of-Forward-Contracts-and-for-an-Underlying-with-Varying-Maturities]] |
| M06 | Pricing and Valuation of Futures Contracts | 计算+解释 | Introduction / Pricing of Futures Contracts at Inception | [[M06-Pricing-and-Valuation-of-Futures-Contracts]] |
| M07 | Pricing and Valuation of Interest Rates and Other Swaps | 计算+解释 | Introduction / Swaps vs. Forwards | [[M07-Pricing-and-Valuation-of-Interest-Rates-and-Other-Swaps]] |
| M08 | Pricing and Valuation of Options | 计算+解释 | Introduction / Option Value relative to the Underlying Spot Price | [[M08-Pricing-and-Valuation-of-Options]] |
| M09 | Option Replication Using Put-Call Parity | 概念+应用 | Introduction / Put–Call Parity | [[M09-Option-Replication-Using-Put-Call-Parity]] |
| M10 | Valuing a Derivative Using a One-Period Binomial Model | 概念+应用 | Introduction / Binomial Valuation | [[M10-Valuing-a-Derivative-Using-a-One-Period-Binomial-Model]] |

## 3. 核心知识树

```text
Derivatives (5-8%)
├─ 1. Derivative Instrument and Derivative Market Features
│  ├─ 1.1 Introduction
│  ├─ 1.2 Derivative Features
│  ├─ 1.3 Derivative Underlyings
├─ 2. Forward Commitment and Contingent Claim Features and Instruments
│  ├─ 2.1 Introduction
│  ├─ 2.2 Forwards, Futures, and Swaps
│  ├─ 2.3 Futures
├─ 3. Derivative Benefits, Risks, and Issuer and Investor Uses
│  ├─ 3.1 Introduction
│  ├─ 3.2 Derivative Benefits
│  ├─ 3.3 Derivative Risks
├─ 4. Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives
│  ├─ 4.1 Introduction
│  ├─ 4.2 Arbitrage
│  ├─ 4.3 Replication
├─ 5. Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities
│  ├─ 5.1 Introduction
│  ├─ 5.2 Pricing and Valuation of Forward Contracts
│  ├─ 5.3 Pricing and Valuation of Interest Rate Forward Contracts
├─ 6. Pricing and Valuation of Futures Contracts
│  ├─ 6.1 Introduction
│  ├─ 6.2 Pricing of Futures Contracts at Inception
│  ├─ 6.3 MTM Valuation: Forwards versus Futures
├─ 7. Pricing and Valuation of Interest Rates and Other Swaps
│  ├─ 7.1 Introduction
│  ├─ 7.2 Swaps vs. Forwards
│  ├─ 7.3 Swap Values and Prices
├─ 8. Pricing and Valuation of Options
│  ├─ 8.1 Introduction
│  ├─ 8.2 Option Value relative to the Underlying Spot Price
│  ├─ 8.3 Option Exercise Value
├─ 9. Option Replication Using Put-Call Parity
│  ├─ 9.1 Introduction
│  ├─ 9.2 Put–Call Parity
│  ├─ 9.3 Option Strategies Based on Put–Call Parity
├─ 10. Valuing a Derivative Using a One-Period Binomial Model
│  ├─ 10.1 Introduction
│  ├─ 10.2 Binomial Valuation
│  ├─ 10.3 The Binomial Model
```

## 4. 跨模块依赖关系

- **M01 Derivative Instrument and Derivative Market Features**：承接 `本科目入口`，输出到 `Forward Commitment and Contingent Claim Features and Instruments`。
- **M02 Forward Commitment and Contingent Claim Features and Instruments**：承接 `Derivative Instrument and Derivative Market Features`，输出到 `Derivative Benefits, Risks, and Issuer and Investor Uses`。
- **M03 Derivative Benefits, Risks, and Issuer and Investor Uses**：承接 `Forward Commitment and Contingent Claim Features and Instruments`，输出到 `Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives`。
- **M04 Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives**：承接 `Derivative Benefits, Risks, and Issuer and Investor Uses`，输出到 `Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities`。
- **M05 Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities**：承接 `Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives`，输出到 `Pricing and Valuation of Futures Contracts`。
- **M06 Pricing and Valuation of Futures Contracts**：承接 `Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities`，输出到 `Pricing and Valuation of Interest Rates and Other Swaps`。
- **M07 Pricing and Valuation of Interest Rates and Other Swaps**：承接 `Pricing and Valuation of Futures Contracts`，输出到 `Pricing and Valuation of Options`。
- **M08 Pricing and Valuation of Options**：承接 `Pricing and Valuation of Interest Rates and Other Swaps`，输出到 `Option Replication Using Put-Call Parity`。
- **M09 Option Replication Using Put-Call Parity**：承接 `Pricing and Valuation of Options`，输出到 `Valuing a Derivative Using a One-Period Binomial Model`。
- **M10 Valuing a Derivative Using a One-Period Binomial Model**：承接 `Option Replication Using Put-Call Parity`，输出到 `本科目总结`。

## 5. 核心对比专题

- **概念 vs 应用**：先确认官方定义，再把定义放入题干情境判断。
- **计算 vs 解释**：计算结果只是中间步骤，CFA Level I 经常要求解释方向、限制和投资含义。
- **静态知识 vs 决策流程**：把每个模块压缩成“输入 -> 工具 -> 输出 -> 陷阱”的流程。
- **英文术语 vs 中文理解**：英文保留用于识题，中文解释用于防止机械背诵。

## 6. 公式与框架速查

| 编号 | 工具 / Formula | 中文用途 |
|---|---|---|
| F1 | `Forward value: Vt = St - PV(forward price)` | 远期合约价值随标的价格和折现变化。 |
| F2 | `Put-call parity: c + PV(X) = p + S` | 欧式期权无套利关系，高频判断式。 |
| F3 | `Option payoff: call = max(0, S - X), put = max(0, X - S)` | 先画到期收益，再考虑期权费。 |

## 7. 高频考试陷阱

- **模块名和旧笔记不一致**：以 2026 官方 module 名称、编号和顺序为准。
- **只背公式不解释**：凡是 `calculate and interpret`，必须同时会算和解释。
- **忽略 LOS 动词**：`describe`、`explain`、`compare`、`evaluate` 对答案深度要求不同。
- **跨模块断裂**：做错题时记录它关联到哪个 MOC 节点，必要时触发 MOC gap review。

## 8. 通用分析框架

1. **识别任务**：读 LOS 动词和题干问法。
2. **定位节点**：回到 `## 3. 核心知识树` 的编号节点。
3. **选择工具**：概念框架、公式、表格比较或合规流程。
4. **输出结论**：中文结论 + 英文关键词 + 必要限制条件。
5. **复盘缺口**：若错因重复出现，进入 `.system/events/` 和 `.system/memory/` 闭环。

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

- 本科目高置信 legacy 映射：14 条；中置信候选：27 条。
- 详细来源与处理建议见 [[cfa-legacy-to-official-enrichment-map]]。
- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。
