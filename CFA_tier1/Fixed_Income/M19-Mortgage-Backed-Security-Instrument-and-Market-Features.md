---
title: "M19: Mortgage-Backed Security (MBS) Instrument and Market Features"
description: "CFA Level I 2026 Fixed Income 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Fixed Income"
topic_area: "Fixed_Income"
level: "CFA Level I"
exam_year: 2026
exam_weight: "11-14%"
module: "M19"
official_module: "Module 19: Mortgage-Backed Security (MBS) Instrument and Market Features"
los_count: 4
difficulty: "概念+应用"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Fixed_Income
---

# M19: Mortgage-Backed Security (MBS) Instrument and Market Features

> **Module job**：把 mortgage cash flows 的 prepayment risk, time tranching, RMBS pass-through, CMO, and CMBS structures 分清。核心是 contraction risk vs extension risk and tranche priority。

## 0. Reading Contract 阅读契约

- **Official LOS**：define prepayment risk and time tranching；describe residential mortgage loan features；describe RMBS pass-throughs and CMOs；describe CMBS characteristics and risks。
- **Textbook anchors**：Time Tranching；Prepayment Risk；Mortgage Loans；Agency and Non-Agency RMBS；Mortgage Contingency Features；Mortgage Pass-Through Securities；CMOs；Sequential-Pay CMO；Other CMO Structures；CMBS Structure；Call Protection；Balloon Maturity；CMBS Risks。
- **Output standard**：能追踪 mortgage borrower payments 如何变成 MBS investor cash flows, and who bears timing risk。

## 1. Module Brief 模块定位

M19 是 fixed income C+ 中证券化最容易失分的模块。它不只是背 RMBS/CMBS 名称，而是判断 prepayment speed 如何改变 tranche cash-flow timing。

## 2. Curriculum Spine 教材主线

1. **Prepayment risk**：borrowers may repay early, changing timing and reinvestment outcome。
2. **Contraction risk**：rates fall -> prepayments speed up -> investors get principal back early。
3. **Extension risk**：rates rise -> prepayments slow -> investors stuck longer。
4. **RMBS pass-through**：principal and interest passed through after servicing/guarantee fees。
5. **CMO time tranching**：sequential or other structures redistribute principal timing risk。
6. **CMBS**：commercial property loans, call protection, balloon maturity, property and refinance risk。

## 3. Exam Translation 考试翻译

- If rates fall, expect faster prepayment and contraction risk for many MBS investors。
- If rates rise, expect slower prepayment and extension risk。
- If sequential-pay CMO appears, earlier tranche gets principal first, later tranche waits。
- If CMBS appears, focus on property cash flows, balloon risk, call protection, and refinance risk。

## 4. Formula & Decision Bench 公式与决策台

| Concept | Decision rule |
|---|---|
| Prepayment risk | Uncertainty about timing of principal repayment |
| Contraction risk | Principal returned sooner than expected |
| Extension risk | Principal returned later than expected |
| Pass-through MBS | Investors receive pro rata mortgage cash flows after fees |
| Sequential CMO | Principal paid to Tranche A, then B, then later tranches |
| PAC/support concept | Some tranches get more stable schedule; support absorbs variability |
| CMBS balloon risk | Borrower may need refinancing at maturity |

## 5. Practice & Mock Evidence 练习与模考证据

- **EOC anchor**：`CFA2448-eorq-q.xhtml` / `CFA2448-eorq-a.xhtml`。
- **Evidence to capture**：contraction/extension reversed；sequential tranche order missed；RMBS vs CMBS collateral confused；call protection ignored。
- **Review tag**：`Fixed Income / MBS / prepayment tranching CMBS`。

## 6. Trap Ledger 陷阱账本

- Lower rates usually increase prepayment, creating contraction risk。
- Higher rates usually slow prepayment, creating extension risk。
- Time tranching reallocates timing risk across tranches, not total mortgage pool risk。
- CMBS prepayment behavior differs because commercial loans often have call protection and balloon maturities。

## 7. Final Recall Sheet 最终速记

- MBS key risk = timing of principal。
- Rates down -> prepay faster -> contraction。
- Rates up -> prepay slower -> extension。
- CMO tranche order decides who receives principal first。
- CMBS = property cash flow + refinance/balloon/call protection risk。
