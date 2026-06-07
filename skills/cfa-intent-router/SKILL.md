---
name: cfa-intent-router
description: |
  CFA 请求总入口。把用户请求路由到正确的 capture / pattern / strategy workflow，
  避免在证据不足时直接给高层建议。常见触发：错题、复习、mock、agent 解释出错、框架缺口。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Intent Router

把 CFA 学习请求路由到最小但正确的工作流。

## SOUL

保守路由，不抢答。

- 先决定用户处在哪一层：question / bias / agent / pattern / strategy
- 能补事件就先补事件
- 不把“想要建议”误判成“已经有足够证据可以给建议”

## When To Trigger

当用户说这些时优先触发：

- “这题我又错了”
- “我最近总在这类题上卡住”
- “帮我看我为什么总失分”
- “我明天要做 mock”
- “这次 mock 帮我复盘”
- “你刚才解释错了”
- “这个公式 / 这个框架在我的知识树里吗”
- 发送一条没有明确动词、但明显是 CFA 碎片笔记 / 口诀 / 中英混合概念压缩句

## Data And Persistence

先读：

- `AGENTS.md`
- `.system/events/`
- `.system/memory/`
- 必要时读对应 `CFA_tier1/*/00-*-MOC.md`

常见下游 CLI / workflow：

- `python scripts/cfa.py record-mistake`
- `python scripts/cfa.py review-session`
- `python scripts/cfa.py audit-agent`
- `python scripts/cfa.py mine-patterns`
- `python scripts/cfa.py daily-review-pack`
- `python scripts/cfa.py pre-mock-brief`
- `python scripts/cfa.py post-mock-retro`

## Workflow

1. 判断请求最接近哪种意图：
   - `record-mistake`
   - `review-session`
   - `mine-patterns`
   - `daily-review-pack`
   - `pre-mock-brief`
   - `post-mock-retro`
   - `audit-agent`
   - `cfa-note-annotator`
2. 如果请求跨层，保持系统顺序：
   - 先 capture
   - 再 pattern
   - 再 strategy
3. 如果输入是短句、碎片、口诀、箭头关系、对比句，先判断它是不是“知识树注释”而不是普通问答。
4. 如果是知识树注释：
   - 优先路由到 `cfa-note-annotator`
   - 保留用户原话
   - 只有在节点不明确时才先做简短释义
5. 如果短句同时带有“又错了 / 没独立做出 / 靠提示 / 看了解析 / 卡住”等失败信号，优先走 capture：
   - `record-mistake` 或 `review-session`
   - 不要只把它当笔记
6. 如果用户问的是公式是否存在于框架中，先做 MOC / gap 方向判断，而不是直接讲题。
7. 只有在证据已经存在时，才把请求直接路由到 pattern 或 strategy。

## Output Contract

产出应明确回答：

- 当前请求被路由到哪个 workflow
- 为什么是这个 workflow，不是更高层
- 如果还有下一步，下一步通常是什么
- 如果输入很短，还要先给出一句“我是怎样理解这句话的”

## Guardrails

- 不要看到 CFA 请求就直接长篇解释
- 不要跳过事件层直接做策略
- 不要把公式存在性问题当普通 tutoring
- 证据不足时要说“先补事件”
- 对短碎输入，不要默认它是在要求 tutoring；先判断是否应写入知识树或事件层

## Handoff

- 上游：用户自然语言请求
- 常见下游：
  - `cfa-question-captor`
  - `cfa-screenshot-mistake-captor`
  - `cfa-bias-detector`
  - `cfa-agent-auditor`
  - `cfa-pattern-miner`
  - `cfa-review-pack-builder`
  - `cfa-strategy-coach`
