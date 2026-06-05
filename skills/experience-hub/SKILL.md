---
name: experience-hub
description: |
  OpenExam 的治理层 skill。负责经验晋升、去重、淘汰、策略连接和 validation 治理，
  不负责充当日志桶或代替 `.system/events` / `.system/memory/`。
metadata:
  version: OpenExam Skill Pack v1
---

# Experience Hub

Experience Hub 是治理层，不是仓库垃圾回收站。

## SOUL

决策价值大于沉淀数量。

- 只保留会改变下一次决策的经验
- 重复就合并
- 失效就降级或淘汰

## When To Trigger

当用户或系统需要：

- 整理长期经验资产
- 判断某条经验该不该晋升
- 合并重复策略
- 清理过期 validation
- 连接 question / bias / agent / pattern / strategy / validation

时触发。

## Data And Persistence

重点读取：

- `.system/events/`
- `.system/memory/question-errors/`
- `.system/memory/cognitive-bias/`
- `.system/memory/agent-failures/`
- `.system/memory/patterns/`
- `.system/memory/strategy/`
- `.system/memory/validation/`

工作文件：

- `_registry.md`
- `review-checklist.md`
- `operating-rhythm.md`

## Workflow

1. 先确认相关事实已存在于 event / memory 层。
2. 判断该经验是否值得晋升：
   - 是否重复
   - 是否新增约束
   - 是否能改变下一次决策
3. 对已有资产做：
   - merge
   - downgrade
   - retire
   - connect
4. 保持 registry 清晰，不堆积无行动价值的条目。

## Output Contract

治理输出应明确说明：

- 保留什么
- 合并什么
- 淘汰什么
- 为什么这些决定会改变下次决策

## Guardrails

- 不把所有聊天内容搬进来
- 不代替 `.system/events/`
- 不代替 `.system/memory/question-errors`
- 不把 projection 页面当治理主事实

## Handoff

- 上游：
  - `cfa-pattern-miner`
  - `cfa-strategy-coach`
  - `cfa-validation-guard`
  - `cfa-agent-auditor`
- 下游：
  - 无固定下游；它主要做治理收束

