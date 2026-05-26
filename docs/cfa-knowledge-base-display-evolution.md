---
title: "CFA Knowledge Base Display Evolution"
description: "CFA Level I 知识库从 Markdown 稳态展示到 Canvas、Dashboard、Web、知识图谱与 Agent 系统的演进路线"
note_type: strategy
status: active
updated: 2026-05-26
---

# CFA Knowledge Base Display Evolution

> 当前阶段仍以 Markdown 稳态为主。本文只记录未来展示形态的可能性、边界和风险，不把任何未来界面提前写成 source of truth。

## 1. 当前 Markdown 稳态层

- **目标**：让 `CFA_tier1/` 的 10 科 MOC 和 93 个 module 成为可阅读、可链接、可复习的 Obsidian 投影视图。
- **边界**：Markdown 是展示层，不是主存储；官方 module 名称、顺序、LOS 和权重来自 registry。
- **Source of truth**：
  1. `.system/events/` 与 `.system/events/catalog.sqlite3`
  2. `.system/memory/`
  3. 官方 registry：`.system/memory/strategy/cfa-2026-official-module-registry.json`
  4. `CFA_tier1/` Markdown 投影视图
- **当前不做**：不引入 CSS snippet、HTML grid、复杂 Web app 或手工 Canvas 维护。

## 2. 可升级展示形态

| 形态 | 目标 | 适用场景 | 数据源 | 实现门槛 | 优先级 | 风险 |
|---|---|---|---|---|---|---|
| Obsidian Canvas 知识地图 | 把 10 科 MOC、93 个 module、错题 pattern 连成可视化地图。 | 复习全局结构、发现跨模块依赖。 | 官方 registry、MOC、module frontmatter、.system/memory/patterns | 中：需要稳定节点 ID 与 Canvas JSON 生成脚本。 | P1 | Canvas 容易变成手工图；必须可重复生成。 |
| Dataview / Dashboard 自动聚合 | 按 topic、LOS、错因、复习日期自动汇总当前弱点。 | 每日复盘、周度 pattern mining、考前 brief。 | .system/events/catalog.sqlite3、.system/memory、CFA_tier1/dashboard | 中：需要 frontmatter 规范和导出脚本。 | P1 | 不要让 dashboard 成为 source of truth。 |
| 静态网站或本地 Web app | 把 Markdown 投影为可搜索、可筛选、可跳转的学习应用。 | 长时间复习、手机/平板阅读、跨模块检索。 | registry、CFA_tier1、.system/memory 生成的 JSON API | 高：需要路由、搜索索引和构建流程。 | P2 | 维护成本上升，且可能偏离备考主线。 |
| 可交互公式卡片 | 把公式、变量、口径、陷阱拆成可翻转卡片和小计算器。 | Quant、FSA、Fixed Income、Derivatives 高频计算复习。 | module `## 5. 关键公式与计算框架`、错题事件。 | 中高：需要公式结构化抽取和输入校验。 | P2 | 公式卡不能替代题干判断，避免机械刷卡。 |
| 错题驱动知识图谱 | 用错题事件连接 topic、LOS、error_type、fix_rule 和 MOC 节点。 | 定位重复犯错、生成 mock 前高风险提醒。 | .system/events、.system/memory/patterns、MOC 节点编号。 | 高：需要稳定 taxonomy 和图数据库/JSON 图。 | P1.5 | 同义词会造成图谱碎裂，需要 Topic alias 治理。 |
| Agent 复盘/提醒/校验界面 | 让 agent 基于事件证据生成 brief、retro、validation checklist。 | mock 前后、错题批量复盘、agent 输出审计。 | .system/app workflows、skills、.system/memory/validation。 | 中：已有 CLI，可先做薄 UI 或命令面板。 | P2 | 不能让 agent 跳过事件层直接给策略。 |
| Spaced repetition 与 quiz 模式 | 把术语、公式、陷阱、错题 fix rule 转成间隔复习卡和小测。 | 考前冲刺、碎片时间、薄弱 LOS 反复练。 | module section 3/5/7、question-errors、patterns。 | 中：需要卡片生成、复习状态和淘汰机制。 | P2 | 卡片过多会稀释重点，必须按决策价值治理。 |

## 3. 数据源与架构边界

- **Capture Layer**：`.system/events/` 捕获错题、偏差和 agent 失误，是动态学习证据。
- **Memory Layer**：`.system/memory/` 沉淀长期资产、pattern、strategy 和 validation。
- **Decision Layer**：`.system/app/` 与 `skills/` 生成复盘、策略和校验。
- **Projection Layer**：`CFA_tier1/`、Dashboard、Canvas、Web app 都只是投影。
- 任何新展示形态都必须能回溯到 registry、事件或 memory，不能手工创造无法验证的结论。

## 4. 推荐演进路线

1. **P1：稳定 Markdown + Dataview 聚合**。先让 frontmatter、module 编号和 MOC 节点稳定，生成 dashboard。
2. **P1.5：错题驱动知识图谱原型**。以 topic alias、LOS、error_type、moc_target 为节点，验证是否真的改善复盘。
3. **P2：公式卡片与 quiz**。只从高频计算模块和重复错题生成，避免卡片泛滥。
4. **P2：Agent brief UI**。在 CLI 工作流稳定后，再做薄界面展示 pre-mock brief、post-mock retro 和 validation。
5. **P3：本地 Web app**。只有当 Markdown + dashboard 已无法支撑检索和交互时再启动。

## 5. 不建议立即做的方向

- **大型 Web app 重写**：会把注意力从备考内容治理转移到界面工程。
- **手工 Canvas 大图**：短期漂亮，但难以复跑，容易和 registry 脱节。
- **全自动 agent 改 MOC**：必须经过 `moc-gap-review`，不能让 pattern mining 直接改 Projection 层。
- **无筛选的卡片化**：所有段落都做成 flashcard 会制造噪音，违背“只沉淀能改变决策的内容”。

## 6. 下一步候选项目

- 为 93 个 module 的编号知识树生成稳定 node id，例如 `QM.M10.10.2`。
- 建立 topic alias taxonomy，减少同义词导致的 pattern 碎裂。
- 从 `.system/events/catalog.sqlite3` 生成 `CFA_tier1/dashboard/Topic弱点页.md`。
- 为高频计算模块抽取公式 JSON，用于未来公式卡片和 quiz。
- 设计 `moc_target` 自动建议规则，把错题更稳定地挂回 MOC 节点。
