# AGENTS

# CFA Level I 本地 Agent 学习操作系统

## 定位

这个仓库不是普通笔记仓库，而是一套面向 CFA Level I 备考的本地 Agent 学习操作系统。

它的目标不是“多记一点”，而是把每一次做题、卡壳、复盘、误判、agent 失误，都转成下一次更快、更准、更稳的行动规则。

核心原则：

- 记忆为了理解，理解也为了记忆
- 先沉淀结构化证据，再做总结和策略
- Obsidian 是展示层，不是主存储
- 错误必须分层处理，不能把所有问题都当成“题目做错”
- 经验只在能改变下次决策时才值得保留

---

## 系统目标

本系统服务 4 个直接结果：

1. 更快定位弱点：知道自己错在知识、过程还是复盘质量。
2. 更高质量复盘：每条错题都要转成可执行的 fix rule 和 next drill。
3. 更少重复犯错：高频错误自动升级为 pattern、strategy、validation。
4. 更强 agent 协作：agent 不是只会生成内容，而是参与记录、分析、提醒、校验。

---

## 当前架构

### 四层架构

| 层级 | 作用 | 主目录 |
|------|------|--------|
| Capture Layer | 捕获原始事件 | `.system/events/` |
| Memory Layer | 沉淀长期资产 | `.system/memory/` |
| Decision Layer | 生成策略与复盘结论 | `.system/app/` + `skills/` |
| Projection Layer | 导出为可阅读页面 | `CFA_tier1/` |

### 三类错误源

所有错误必须先归类到以下 3 层之一：

| 层级 | 含义 | 示例 |
|------|------|------|
| `question` | 题目层错误 | 选错、概念混淆、公式误用 |
| `bias` | 学习过程偏差 | 时间分配失衡、读题粗心、知识块混淆 |
| `agent` | agent 执行失误 | 幻觉、漏掉 root cause、总结错误 |

如果不能分清层级，先按 `question` 记录，再在复盘中升级为 `bias` 或 `agent`。

---

## Source of Truth

以下优先级必须固定：

1. `.system/events/` 和 `.system/events/catalog.sqlite3`
2. `.system/memory/`
3. `.system/app/` 的工作流逻辑
4. `skills/` 的行为规范
5. `CFA_tier1/` 导出页面
6. 任何人工摘要或临时聊天结论

这意味着：

- Obsidian 页面被视为投影视图，不是唯一真相。
- 若 `CFA_tier1/` 与 `.system/memory/` 冲突，以 `.system/memory/` 为准。
- 若策略总结与原始事件冲突，以 `.system/events/` 为准。

---

## 真实目录结构

```text
CFA_learning/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .obsidian/
├── CFA_tier1/
│   ├── 00-CFA_L1_备考指南.md
│   ├── 00-Index.md
│   ├── Alternative_Investments/
│   ├── Corporate_Issuers/
│   ├── Derivatives/
│   ├── Economics/
│   ├── Equity/
│   ├── Ethical_and_Professional_Standards/
│   ├── Financial_Statement_Analysis/
│   ├── Fixed_Income/
│   ├── Portfolio_Management/
│   ├── Quantitative_Methods/
│   ├── dashboard/
│   └── mock/
├── .system/
│   ├── app/
│   │   ├── agents_runtime.py
│   │   ├── cli.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── storage.py
│   │   └── workflows.py
│   ├── events/
│   │   ├── question/
│   │   ├── bias/
│   │   ├── agent/
│   │   └── catalog.sqlite3
│   ├── memory/
│   │   ├── question-errors/
│   │   ├── cognitive-bias/
│   │   ├── agent-failures/
│   │   ├── patterns/
│   │   ├── strategy/
│   │   └── validation/
│   ├── evals/
│   └── tests/
├── scripts/
├── log/
├── schedule/
├── skills/
│   ├── cfa-intent-router/
│   ├── cfa-question-captor/
│   ├── cfa-bias-detector/
│   ├── cfa-agent-auditor/
│   ├── cfa-review-synthesizer/
│   ├── cfa-pattern-miner/
│   ├── cfa-strategy-coach/
│   ├── cfa-validation-guard/
│   └── experience-hub/
```

---

## 本体系目前最关键的升级点

相较于旧版方案，这个系统必须补强以下 6 点：

1. 从“记录很多”升级到“只沉淀能改变决策的内容”。
2. 从“错题本中心”升级到“题目层 + 偏差层 + agent层”三层并行。
3. 从“事后总结”升级到“考前 brief + 考后 retro + 周期 pattern mining”。
4. 从“经验堆积”升级到“有晋升门槛、有淘汰机制的经验治理”。
5. 从“Obsidian 即系统”升级到“本地数据层为主，Obsidian 为投影”。
6. 从“只要求 agent 产出”升级到“要求 agent 先校验、再输出、可追责”。

---

## 技能与职责

### 核心技能

| Skill | 职责 |
|------|------|
| `cfa-intent-router` | 把请求路由到正确工作流 |
| `cfa-question-captor` | 把题目错题转成结构化事件和错题卡 |
| `cfa-bias-detector` | 识别学习偏差和过程性失误 |
| `cfa-agent-auditor` | 审计 agent 幻觉、错因遗漏、错误总结 |
| `cfa-review-synthesizer` | 输出单次复盘结论 |
| `cfa-pattern-miner` | 识别高频错误模式 |
| `cfa-strategy-coach` | 生成复习顺序、mock 节奏、补强建议 |
| `cfa-validation-guard` | 生成反幻觉和防漏检校验规则 |
| `experience-hub` | 管理经验晋升、去重、淘汰和跨层连接 |

### Agent 角色

`.system/app/agents_runtime.py` 中保留以下 6 个角色：

- `orchestrator`
- `mistake_recorder`
- `review_coach`
- `pattern_miner`
- `strategy_coach`
- `validator`

任何后续增强都应先复用这些角色边界，而不是随意增加新 agent。

---

## CLI 工作流

本项目当前以 CLI 作为标准入口：

| 动作 | 作用 |
|------|------|
| `record-mistake` | 记录题目层错误 |
| `review-session` | 记录学习偏差 / 卡壳点 |
| `audit-agent` | 审计 agent 失误 |
| `mine-patterns` | 识别重复模式 |
| `pre-mock-brief` | 生成考前简报 |
| `post-mock-retro` | 生成 mock 后复盘 |

标准调用示例：

```powershell
python scripts/cfa.py record-mistake --payload "{...}"
python scripts/cfa.py review-session --payload "{...}"
python scripts/cfa.py audit-agent --payload "{...}"
python scripts/cfa.py mine-patterns
python scripts/cfa.py pre-mock-brief
python scripts/cfa.py post-mock-retro --session-id mock-2
```

---

## 数据对象约束

### MistakeEvent

每条事件必须尽量补全以下字段：

- `source_layer`
- `topic`
- `los`
- `prompt_or_question`
- `wrong_choice_or_output`
- `correct_resolution`
- `error_type`
- `confidence`
- `time_spent`
- `evidence_refs`
- `question_source`
- `source_type`
- `evidence_assets`
- `moc_target`

### MistakeCard

每张卡必须回答 5 个问题：

1. 错在哪？
2. 为什么会错？
3. 下次如何避免？
4. 什么时候复习？
5. 它和哪些模式或策略有关？

---

## 学习闭环节奏

旧版体系的主要不足，是“有沉淀，没有节奏”。现在固定为 5 个层级的运行节奏：

### 1. 即时层

每次出现错误后立即做一件事：

- 题错了：`record-mistake`
- 学习卡住了：`review-session`
- agent 解释错了：`audit-agent`

如果用户提供的是错题截图：

- 先把截图视为原始证据
- 由 Codex 提取结构化字段后再执行 `record-mistake`
- 不允许因为截图模糊而脑补 LOS、题源或正确结论

### 2. 单次会话层

每次学习块结束后必须判断：

- 今天的错误主要是知识问题，还是过程问题？
- 今天是否出现可复用 fix rule？
- 今天是否出现需要升级为 validation 的 agent 失误？

### 3. Mock 层

每次 mock 必做：

- 开始前：`pre-mock-brief`
- 结束后：`post-mock-retro --session-id <id>`

### 4. 周度层

每周至少一次：

- 执行 `mine-patterns`
- 检查是否有 Topic 连续出现 3 次以上错误
- 生成下周的 Topic 优先级

### 5. 月度治理层

每月执行一次经验治理：

- 清理不再产生决策价值的经验
- 合并重复策略
- 撤销已经失效的 validation
- 审查 `experience-hub/_registry.md`

---

## 经验晋升门槛

不是每条记录都应该升级成“经验”。

### 晋升规则

| 资产类型 | 晋升条件 |
|------|------|
| `question-errors` | 单次记录即可生成 |
| `cognitive-bias` | 单次记录即可生成 |
| `agent-failures` | 单次记录即可生成 |
| `patterns` | 同一 `topic + los + error_type` 至少出现 3 次 |
| `strategy` | 至少能改变下一次 mock 或复习顺序 |
| `validation` | 同类 agent 风险出现 1 次且会造成误导时立即创建 |

### MOC 反馈规则

- 当同一 `topic + los + error_type` 的 `question` 事件重复出现，且事件带有 `moc_target` 时，可以执行 `moc-gap-review`
- `moc-gap-review` 只生成框架补强建议，不直接修改 `00-*-MOC.md`
- MOC 更新必须在阅读 review artifact 后，由 Codex 二次判断再执行

### 淘汰规则

以下内容优先淘汰：

- 只是描述现象、不能指导行动的总结
- 与现有策略重复，且没有新增约束的信息
- 已经过教材核验为错误的 agent 经验
- 与当前复习阶段无关、长期不再引用的弱价值笔记

---

## 质量门槛

每次输出复盘或策略前，至少过这 5 道门：

1. 这条结论能回溯到原始事件吗？
2. 这是知识错误、过程偏差，还是 agent 失误？
3. 结论是否包含可执行动作，而不只是抽象建议？
4. 如果这是规则性结论，是否需要验证？
5. 这条沉淀是否真的会影响下一次决策？

任一问题回答为“不能”，就不应直接升级为 strategy 或长期经验。

---

## Obsidian 导出原则

Obsidian 页面的目标是“便于回看”，不是“承载主逻辑”。

固定导出以下页面：

- `今日新增错题.md`
- `高频错因榜.md`
- `Topic弱点页.md`
- `Agent失误页.md`
- `策略手册页.md`

导出要求：

- 可重复生成
- 同名页面必须覆盖更新，不重复创建
- 页面内容来自 `.system/events/` 和 `.system/memory/`，不手工拼接虚构结论
- 固定写入 `CFA_tier1/dashboard/`

MOC 缺口建议不属于 dashboard 导出页，它属于治理和补强决策资产，固定写入：

- `.system/memory/strategy/moc-gap-review.md`

---

## 用户请求到工作流的映射

| 用户意图 | 首选动作 |
|------|------|
| “这题我又做错了” | `record-mistake` |
| “我最近总在某类题上卡住” | `review-session` 或 `mine-patterns` |
| “帮我看下我为什么总失分” | `mine-patterns` |
| “我明天要做 mock，先给我重点” | `pre-mock-brief` |
| “这次 mock 帮我系统复盘” | `post-mock-retro` |
| “你刚才的解释有问题” | `audit-agent` |
| “这几类错题是不是说明知识框架有缺口” | `moc-gap-review` |

如果用户请求跨多个层级，顺序必须是：

1. 先补事件
2. 再做模式
3. 再给策略

不能跳过事件层，直接给高层建议。

---

## Agent 行为约束

- 先路由，再执行，不要看到 CFA 问题就直接生成长答案。
- 每次涉及复盘时，优先问“错因类别”而不是“输出形式”。
- 如果是规则性解释，优先保守、可验证，不追求语言华丽。
- 若发现已有事件不足以支撑结论，应明确说“证据不足”，而不是脑补模式。
- 修改已有 markdown 前必须先读取当前文件，避免覆盖用户手工改动。
- 用户发截图时，优先做结构化提取和证据保留，再进入事件层。
- 不要让 pattern mining 直接自动改写 MOC，必须经过 `moc-gap-review` 这一层。

---

## experience-hub 的职责边界

`experience-hub` 不是日志桶，而是治理层。

它只负责：

- 经验晋升
- 经验去重
- 经验淘汰
- 策略连接
- validation 治理

它不负责：

- 存放所有原始聊天内容
- 代替 `.system/events/`
- 代替 `.system/memory/question-errors`
- 代替 Obsidian 页面

---

## 当前版本建议优先执行的增强

如果后续继续升级，优先级按以下顺序走：

1. 引入 Topic 别名与统一 taxonomy，减少同义词导致的模式碎裂。
2. 给 `pre-mock-brief` 增加时间分配建议和高风险题型提醒。
3. 给 `post-mock-retro` 增加“本次最该停止做的事”栏目。
4. 增加 pattern 的严重度排序规则。
5. 为 validation 规则增加失效日期和复核状态。
6. 在 `moc-gap-review` 基础上增加更细的 gap type 推断与去重逻辑。

---

## 维护原则

- 任何新增目录或工作流，必须先回答“它属于 Capture / Memory / Decision / Projection 哪一层”。
- 任何新增沉淀，必须回答“它将如何改变下一次决策”。
- 任何新增 agent，必须先证明现有 6 角色无法承担。
- 任何新增页面，必须先证明不能由现有 `CFA_tier1/` 页面组合得到。

---

## 更新记录

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-04 | 初始版本 | 1.0 |
| 2026-05-01 | 引入 Harness-First、自进化与防腐机制 | 2.0 |
| 2026-05-21 | 对齐本地 agent 仓库真实结构，升级为四层架构、三类错误源、五级节奏、经验晋升门槛与治理规范 | 3.0 |
