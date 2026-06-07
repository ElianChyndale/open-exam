# Experience Hub Registry

这个注册表只登记“已经值得影响下次决策”的经验资产。

## 资产类型

| 类型 | 进入条件 | 退出条件 |
|------|----------|----------|
| `pattern` | 同一模式出现至少 3 次 | 30 天未被引用且不再高频 |
| `strategy` | 能改变下一次复习顺序或 mock 行为 | 被更强策略替代 |
| `validation` | 同类 agent 风险需要前置校验 | 对应风险长期未再出现或规则失效 |

## 当前登记规则

- 先证据，后登记。
- 先去重，后新增。
- 先说明触发条件，后写建议。
- 不登记只有情绪价值、没有决策价值的内容。

## OpenExam Intake Register

| 场景 | 默认解释 | 默认动作 | 升级条件 |
|------|----------|----------|----------|
| 用户发送短 CFA 碎片句、口诀、箭头关系、中英混合压缩理解 | 先视为 `note`，不是普通 tutoring | 先走 `cfa-intent-router`，再优先考虑 `cfa-note-annotator` | 若同时出现错题 / 卡壳 / 非独立作答信号，则改走 capture |
| 用户发送短句但带“又错了 / 靠提示 / 看了解析 / 没独立做出” | 先视为 `question` 或 `bias` 证据 | `record-mistake` 或 `review-session` | 事件落地后才允许再做 pattern / strategy |
| 用户发送短句要求“帮我记一下 / 加到知识树 / 写到 MOC” | 明确视为注释写入 | `cfa-note-annotator` | 若节点不唯一，则先停在路由与释义 |

## Register Rule

- 在 `open-exam` workspace 中，短输入先分类，再回答。
- 默认先判断是否为注释型输入，避免把用户的压缩记忆句误答成普通解释。
- 只有在证据明确时，才把短输入升级为 pattern、strategy 或长期治理资产。

