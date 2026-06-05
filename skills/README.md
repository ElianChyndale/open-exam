# OpenExam Skills Pack

> 一套面向 OpenExam 的本地技能包。  
> 目标不是“写更多说明”，而是让每个 skill 都更容易被发现、路由、执行、校验和协作。

---

## 这是什么

这个 `skills/` 目录是 OpenExam 的 **Decision Layer 行为规范包**。

它借鉴了 `ielts-claude-skills` 的产品化组织方式，但完全适配 OpenExam 的 CFA-first、本地优先、证据驱动架构：

- `.system/events/` 是原始证据
- `.system/memory/` 是长期资产
- `.system/app/` 是工作流和执行逻辑
- `skills/` 规定代理应该如何判断、调用、升级和交接
- `CFA_tier1/` 是投影视图，不是主存储

---

## 技能分组

### Capture Skills

| Skill | 作用 | 常见触发 |
|------|------|------|
| `cfa-intent-router` | CFA 请求总入口与路由器 | “这题我又错了”“今天复习什么” |
| `cfa-question-captor` | 题目证据标准化录入 | 错题、非独立作答、低质量完成 |
| `cfa-screenshot-mistake-captor` | 截图题目证据录入 | 截图错题、模考截图 |
| `cfa-bias-detector` | 过程性偏差识别 | 时间压力、读题粗心、卡壳 |
| `cfa-agent-auditor` | agent 失误审计 | 幻觉、漏根因、错总结 |
| `cfa-note-annotator` | 个人知识树注释写入 | “记一下”“加个口诀”“补个标注” |

### Decision Skills

| Skill | 作用 | 常见触发 |
|------|------|------|
| `cfa-review-synthesizer` | 单次复盘总结 | 一次学习块或一次 mock 的 retro |
| `cfa-pattern-miner` | 重复错误模式识别 | “我为什么总错这个” |
| `cfa-strategy-coach` | 复习顺序 / mock 节奏 / 下步策略 | “我接下来先学什么” |
| `cfa-review-pack-builder` | 今日复习资料与 warm start | “给我今天复习资料” |
| `cfa-daily-todo-planner` | 每日任务压缩成执行面 | “今天安排”“更新 todo” |
| `cfa-validation-guard` | 校验规则生成与治理 | agent 风险、防漏检、防误补 |
| `codex-self-cycle` | 自循环任务编排 | “自己继续做”“不要停” |

### Governance Skills

| Skill | 作用 | 常见触发 |
|------|------|------|
| `experience-hub` | 经验晋升、去重、淘汰、连接 | 治理、长期资产整理 |
| `cfa-note-annotator-workspace` | note annotator 的评测/迭代工作区规范 | 调优、评测、对比结果 |

### IELTS Companion Skills

| Skill | 作用 | 常见触发 |
|------|------|------|
| `ielts` | IELTS 路由入口 | “我要备考雅思”“IELTS” |
| `ielts-writing` | 写作批改与改写对比 | “批改作文”“审题” |
| `ielts-reading` | 阅读错题与同义替换分析 | “分析阅读”“这题为什么错” |
| `ielts-speaking` | 口语素材与万能故事 | “口语素材”“Part 2” |
| `ielts-listening` | 听力错题与精听任务 | “听力错题”“精听” |
| `ielts-vocab` | 间隔复习与同义替换训练 | “背单词”“词汇复习” |
| `ielts-diagnosis` | IELTS 数据诊断与计划 | “诊断”“备考计划” |
| `ielts-dashboard` | IELTS 本地 Dashboard | “Dashboard”“看数据” |

---

## 它们如何协作

默认协作顺序是：

1. **先路由**：`cfa-intent-router`
2. **先补证据**：question / bias / agent capture
3. **再做模式**：`cfa-pattern-miner`
4. **再做策略**：`cfa-strategy-coach` / `cfa-review-pack-builder` / `cfa-daily-todo-planner`
5. **最后治理**：`experience-hub` / `cfa-validation-guard`

绝大多数情况下都不应该跳过事件层，直接生成高层建议。

---

## 数据与边界

### 本地数据层

- `.system/events/`：原始事件
- `.system/memory/`：长期卡片、patterns、strategy、validation
- `.system/events/catalog.sqlite3`：可查询索引

### 工作流层

- `python scripts/cfa.py record-mistake`
- `python scripts/cfa.py review-session`
- `python scripts/cfa.py audit-agent`
- `python scripts/cfa.py mine-patterns`
- `python scripts/cfa.py daily-review-pack`
- `python scripts/cfa.py write-todo`
- `python scripts/cfa.py pre-mock-brief`
- `python scripts/cfa.py post-mock-retro`
- `python scripts/cfa.py codex-loop-plan`
- `python scripts/cfa.py codex-loop-complete`

### 投影视图

- `CFA_tier1/dashboard/`
- `CFA_tier1/*/00-*-MOC.md`

### IELTS Companion Data

为尽快把 `ielts-claude-skills` 功能接入当前系统，IELTS companion pack 目前保留它自己的本地数据层：

- 命令入口：`python scripts/ielts.py ...`
- 数据目录：`~/.ielts/`

这部分是 **repo-local 可调用**，但尚未迁移进 OpenExam 的 `.system/` 数据模型。

---

## 统一约定

所有 skill 都应遵守 [SHARED-CONVENTIONS.md](D:/AmyProjects/New%20folder/open-exam/skills/SHARED-CONVENTIONS.md)。

重点包括：

- 四层架构
- Source of Truth 优先级
- 触发方式写法
- 数据持久化写法
- 工作流步骤结构
- guardrails / handoff 约定

---

## 不该发生的事

- 把 Obsidian 页面当主存储
- 没有事件证据却直接做策略
- skill 自己声称能做仓库里实际上不存在的动作
- 把 `experience-hub` 当日志桶
- 把 `codex-self-cycle` 当普通学习 skill

---

## 当前目标

这套技能包的目标是：

- 更容易被代理正确触发
- 更容易被人类快速理解
- 更容易跨 skill 交接
- 更容易对齐到 OpenExam 的真实工作流与本地数据层
