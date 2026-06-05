# OpenExam Skill Conventions

## 1. System Model

所有本地 skill 都建立在同一套四层架构上：

| Layer | 作用 | 主目录 |
|------|------|------|
| Capture | 捕获原始事件 | `.system/events/` |
| Memory | 沉淀长期资产 | `.system/memory/` |
| Decision | 生成判断、策略、复习材料 | `.system/app/` + `skills/` |
| Projection | 导出可读页面 | `CFA_tier1/` |

Skill 文档应明确自己主要服务哪个层级。

## 2. Source of Truth

优先级固定为：

1. `.system/events/` 与 `catalog.sqlite3`
2. `.system/memory/`
3. `.system/app/` 工作流逻辑
4. `skills/`
5. `CFA_tier1/`
6. 临时聊天结论

任何 skill 都不能反过来把第 5、6 层当成主事实来源。

## 3. Required SKILL.md Shape

每个 `SKILL.md` 默认包含：

1. frontmatter
2. 标题 + 一句角色声明
3. `SOUL` / operating stance
4. `When to trigger`
5. `Data and persistence`
6. `Workflow`
7. `Output contract`
8. `Guardrails`
9. `Handoff`

## 4. Trigger Rules

- 触发描述要写“用户说了什么 / 正在做什么”
- 如果一个 skill 只是子技能，也要写清它通常由谁路由进来
- 如果请求先需要证据，不得直接生成高层建议

## 5. Persistence Language

技能包统一使用这些表达：

- “persist through CLI/workflow”
- “read from `.system/events/` / `.system/memory/`”
- “project to `CFA_tier1/` only after decision layer work”

不要使用：

- `~/.ielts/`
- 云端数据库
- 未在仓库中存在的 helper runtime

## 6. Workflow Writing Style

Workflow 必须是顺序步骤，而不是抽象口号。

推荐写法：

1. 先读哪些本地事实
2. 怎么判断是否适合本 skill
3. 调哪个 CLI / workflow
4. 产出什么
5. 何时交给下一个 skill

## 7. Guardrails

每个 skill 至少写清三类约束：

- 不要脑补
- 不要越层
- 不要做不属于本 skill 的事

如果 skill 会修改知识树、复习材料或治理资产，必须明确写：

- 什么时候能改
- 什么时候只能建议不能改

## 8. Handoff Rules

每个 skill 应声明：

- 常见上游 skill
- 常见下游 skill
- 什么情况下结束，不继续升级

默认升级顺序：

1. route
2. capture
3. pattern
4. strategy
5. governance

## 9. Naming Expectations

- `cfa-*`：学习系统相关技能
- `codex-*`：代理自循环或系统维护技能
- `experience-*`：治理层技能

目录名保持稳定，除非重命名能消除真实歧义。

## 10. Reality Check

Skill 不能声称做到下面这些，除非仓库里真有实现：

- 自动 OCR/视觉提取完整结论
- 远程多用户鉴权
- 自动修改所有知识树页面
- 远程任务调度
- 未实现的 UI / API / CLI

如果能力尚未完全产品化，skill 必须保守描述为：

- “prepare a draft”
- “route to workflow”
- “persist a handoff artifact”
- “recommend, not auto-apply”

