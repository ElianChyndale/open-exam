# OpenExam Intake Protocol

目的：减少用户发送短句、碎片、中英混合 CFA 表达时的误判，先决定“这是什么输入”，再决定“怎么处理”。

## Default Rule

在 `open-exam` workspace 中，若用户发送的是短 CFA 片段而不是完整问题，默认不要直接进入普通 tutoring。

先按下面顺序分类：

1. `note`
2. `question`
3. `bias`
4. `agent`
5. `pattern`
6. `strategy`

## Note-Type Signals

满足以下任一条，先按 `note` 处理，再判断是否还需要别的 workflow：

- 句子很短，像口诀、箭头关系、对照表述、压缩理解
- 中英混合术语明显，如 `CFO / CFI / IFRS / goodwill / intangible asset`
- 没有显式提问词，但内容像“我想记住这个”
- 重点在记忆辅助，而不是求完整解题

默认动作：

- 先用 `cfa-intent-router` 判断
- 若是知识树注释，交给 `cfa-note-annotator`
- 若节点不明确，先做一句保守释义，再说明卡点

## Failure Signals Override Note

若短句同时出现以下信号，不能只当注释：

- “又错了”
- “没独立做出来”
- “直接看了解析”
- “靠提示才完成”
- “总卡在这”

默认动作：

- `question` 证据 -> `record-mistake`
- `bias` 证据 -> `review-session`

## Response Shape For Short Inputs

处理短输入时，回复顺序固定为：

1. 一句复述：我如何理解这句话
2. 一句路由：它属于 note / question / bias / agent 的哪类
3. 一句动作：我会写入哪里，或还缺什么证据

## Guardrails

- 不因为用户语法简短就脑补题源、LOS、正确结论
- 不把所有碎片都升级成长期经验
- 不把所有碎片都当一般问答
- 若无法唯一定位节点，说明歧义，不硬写
