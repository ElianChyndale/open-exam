---
name: cfa-bias-detector
description: |
  学习过程偏差识别器。把时间压力、读题粗心、公式启动失败、概念混淆迁移失败等过程问题，
  标准化为 `bias` 层信号，而不是把所有问题都塞回错题层。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Bias Detector

识别“为什么会这样学”，而不只是“这题为什么错”。

## SOUL

过程优先，动作导向。

- 先区分症状和根因
- 先找下一次能改变的动作
- 不把偏差说成性格问题

## When To Trigger

当用户：

- 明明懂内容却总做错
- 总卡在时间、注意力、读题、计算启动
- 说“不是知识不会，是做题过程有问题”
- 反复提到同类 performance friction

时触发。

## Data And Persistence

常用入口：

```powershell
python scripts/cfa.py review-session --payload "{...}"
```

偏差输出应服务：

- `.system/events/bias/`
- `.system/memory/cognitive-bias/`
- 后续 pattern / strategy / validation

## Workflow

1. 判断当前问题是否更像过程偏差，而不是单题错误。
2. 给偏差一个明确 label。
3. 分开写：
   - symptom
   - root cause
   - fix rule
   - next drill
4. 如果它只是一次性的题目错误，不要误录成 bias。
5. 如果它已经重复出现，可为 `cfa-pattern-miner` 留下可聚合信号。

## Output Contract

产出必须回答：

- 偏差叫什么
- 真正拖分的机制是什么
- 下一次具体改什么

## Guardrails

- 不把内容问题伪装成过程偏差
- 不写抽象空话，比如“多认真一点”
- 不把一次偶发失误升级成长期 bias doctrine

## Handoff

- 上游：`cfa-intent-router`
- 常见下游：
  - `cfa-pattern-miner`
  - `cfa-review-synthesizer`
  - `cfa-strategy-coach`

