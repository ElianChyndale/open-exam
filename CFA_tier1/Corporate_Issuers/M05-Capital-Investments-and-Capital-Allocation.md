---
title: "M05: Capital Investments and Capital Allocation"
description: "CFA Level I 2026 Corporate Issuers 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Corporate Issuers"
topic_area: "Corporate_Issuers"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M05"
official_module: "Module 5: Capital Investments and Capital Allocation"
los_count: 4
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Corporate_Issuers
---

# M05: Capital Investments and Capital Allocation

## 0. Reading Contract 阅读契约

- **Official scope**: capital investment types, capital allocation process, NPV, IRR, ROIC, principles/pitfalls, real options.
- **C+ output**: 能用 NPV-first discipline 判断 capital allocation，并说明 IRR/payback/PI/ROIC 的限制。
- **Evidence anchor**: V3 Module 5, practice and solutions available in the 2026 ePub index.

## 1. Module Brief 模块定位

Capital allocation decides whether scarce capital should be committed to projects. 考试高频是 calculation plus interpretation: not only compute NPV/IRR, but also explain why a rule can mislead。

## 2. Curriculum Spine 教材主线

1. Investment types: going concern, regulatory compliance, expansion, new lines/other projects.
2. Capital allocation process: identify, evaluate, choose, implement, monitor.
3. NPV, IRR and ROIC.
4. Principles and pitfalls: value maximization, opportunity cost, cognitive errors and behavioral biases.
5. Real options: delay, expand, abandon, switch.

## 3. Exam Translation 考试转译

- `independent project` -> accept if NPV > 0, IRR > required return if conventional.
- `mutually exclusive conflict` -> NPV dominates IRR.
- `capital rationing` -> rank by value per constrained resource, often PI.
- `payback` -> liquidity/risk screen, not value-maximizing.
- `real option` -> flexibility can increase project value.

### Project Type Classifier 项目类型识别

| Project type | Core meaning | Exam trigger | Not this when... |
|---|---|---|---|
| Going concern project | Required to continue current operations and maintain the existing business size | maintain current operations, replace/repair existing assets, keep the business running | The project is driven by new regulation or safety standards. |
| Compliance project | Required by third parties to meet legal, safety, environmental, or regulatory standards | government/regulator requirement, improved safety standards, mandatory technology upgrade | The project mainly increases business size or adds new products/services. |
| Expansion project | Increases business size, product/service scope, capacity, market reach, or may involve acquisitions | new products/services, larger capacity, entering/acquiring markets | The project only preserves current operations or satisfies compliance. |

Fast rule: if the stem says `new technology to meet improved safety standards`, classify it as `compliance project`, not expansion.

### Real Option Classifier 实物期权识别

| Real option type | Core meaning | Exam trigger | Common trap |
|---|---|---|---|
| Sizing option | Change project scale after investment | abandon project, expand capacity, growth option | Abandonment is sizing, not operating flexibility. |
| Timing option | Delay or sequence investment decisions | delay investment, wait for better information, invest in stages | It is about when to invest, not how to operate current capacity. |
| Flexibility option | Alter operations using current capacity | overtime, add shifts, change production mix, adjust inputs | Operational adjustment is flexibility; exiting or expanding the project is sizing. |

Fast rule: `abandoning after poor financial results` = sizing option, because the company changes the scale/existence of the investment.

## 4. Formula & Decision Bench 公式与决策台

| Trigger | Formula / Decision rule | Check |
|---|---|---|
| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | Accept positive NPV. |
| IRR | rate where `NPV = 0` | Can fail with nonconventional cash flows or scale conflicts. |
| Payback | time until cumulative cash flows recover outlay | Ignores later cash flows and often time value. |
| Discounted payback | time until discounted cash flows recover outlay | Still ignores cash flows after payback. |
| PI | `PV future cash flows / initial investment` | Useful under capital rationing. |
| ROIC | operating profit after tax / invested capital | Performance metric, not direct project value. |
| Real options | delay/expand/abandon/switch | Flexibility has value when uncertainty exists. |

## 5. Practice & Mock Evidence 题库证据

- Expected item types: compute NPV/IRR/PI/payback/ROIC, rank projects, identify pitfall or bias, classify real option.
- Review tag: `Corporate-M05-capital-allocation`.
- Miss log fields: cash-flow timing, discount rate, project relation, constraint, method limitation.

## 6. Trap Ledger 易错账本

- NPV is the main shareholder wealth rule。
- IRR assumes conventional cash flows; multiple IRRs can occur with sign changes。
- PI can help capital rationing but may not solve indivisible project sets alone。
- Sunk costs should be excluded; opportunity costs and externalities included。
- New technology is not automatically expansion; if the purpose is improved safety/regulatory standards, it is a compliance project。
- Abandoning or expanding a project changes project size, so it is a sizing option; overtime/shifts are flexibility options。
- In table-heavy capital allocation items, first identify the governing criterion: if management sets a minimum ROIC/target return, a positive NPV alone may not satisfy the stated criterion。

## 7. Final Recall Sheet 终局速记

- NPV > 0 creates value.
- IRR > hurdle works only when cash flows are conventional and projects are not conflicting.
- Payback = risk/liquidity screen.
- Real option = managerial flexibility.
- Safety/regulatory requirement = compliance project; current operation maintenance = going concern; business-size increase = expansion.
- Real option classifier: sizing = abandon/expand; timing = delay/sequence; flexibility = operate differently within current capacity.
- Table scan: circle `minimum / target / criterion / hurdle / required` before ranking projects by NPV or IRR.
