---
brief_id: chatgpt-brief-20260605-093751
generated_at: 2026-06-05T09:37:51.682522+00:00
chat_name: Codex ChatGPT 协同工作流
---

# ChatGPT Collaboration Brief

## How To Use
Paste the prompt block below into the ChatGPT chat, then bring the reply back here as planning input.

## Current Loop Snapshot
- latest_plan_id: ITER-009
- selected_candidate_id: none
- selected_title: none
- selected_task_path: none
- latest_completed_candidate_id: self-cycle-skill-governance
- latest_completion_summary: Implemented governed Codex self-cycle planner, CLI commands, skill, docs, and tests.

## Prompt For ChatGPT
```text
You are collaborating with local Codex in the ChatGPT chat named "Codex ChatGPT 协同工作流".
Use the repository rules below as hard constraints.

Constraints:
- Source of truth priority: .system/events -> .system/memory -> workflow code -> skills -> CFA_tier1 projections.
- Do not suggest changing locked question-bank prompts, answers, or explanations.
- Prefer Capture / Memory / Decision layer work before Projection-only work.
- Every recommendation must be traceable, bounded, and testable.

Current loop state:
- latest_plan_id: ITER-009
- selected_candidate_id: none
- selected_title: none
- latest_completed_candidate_id: self-cycle-skill-governance
- latest_completion_summary: Implemented governed Codex self-cycle planner, CLI commands, skill, docs, and tests.

Current task artifact:
(no active task file)

Your job:
No autonomous candidate is currently available. Please propose the next smallest bounded task that respects AGENTS.md and keeps core question-bank behavior stable.
Return:
1. A brief decision on whether the task should proceed unchanged, be narrowed, or be replaced.
2. A flat checklist of implementation steps.
3. A flat checklist of verification steps.
4. Any evidence gaps that block safe execution.
```

## Project Context Excerpts
### Collaboration Workflow
# ChatGPT × Codex Collaboration Workflow

This document adapts the external file `Codex ChatGPT 协同工作流.docx` to the
current OpenExam repository.

## Purpose

Use ChatGPT as a planning and review partner, while Codex remains the local
execution agent inside this repository. The collaboration goal is not remote
computer control. The goal is a stable loop:

1. ChatGPT critiques or narrows the next bounded task.
2. Codex implements inside the repo and verifies with tests.
3. Codex exports a new brief back to ChatGPT.
4. The cycle repeats without losing source-of-truth discipline.

## Hard Constraints

- `.system/events/` and `.system/memory/` stay above summaries and chat output.
- Core question-bank prompts, answers, explanations, and published ordering are
  treated as locked unless there is an explicit guarded path.
- Recommendation, analytics, and AI output belong to extension boundaries, not
  canonical evidence.
- Every planning suggestion must end in a bounded task with acceptance criteria
  and verification.

## Role Split

### ChatGPT

- Refine the next task.
- Shrink risky scope.
- Tighten acceptance criteria.
- Point out evidence gaps or test gaps.

### Codex

- Read local truth first.
- Modify code and docs locally.
- Run targeted verification.
- Export the next collaboration brief.

## Repo Workflow

1. Generate or inspect the latest local plan.
   `python scripts/cfa.py codex-loop-plan --mode unattended`
2. Export a ChatGPT brief.
   `python scripts/cfa.py chatgpt-brief`
3. Paste `.system/memory/collaboration/chatgpt/CURRENT_BRIEF.md` into the
   ChatGPT chat named `Codex ChatGPT 协同工作流`.
4. Bring ChatGPT's reply back as planning input for the next bounded change.
5. After implementation, mark the loop step complete if appropriate and export
   a fresh brief again.

## Phase Mapping From The Original Workflow

- Phase 1: environment and data model
- Phase 2: practice generation and answer capture
- Phase 3: frontend contract and interaction
- Phase 4: analytics and extension modules

In this repository, those phases must still respect the Capture / Memory /
Decision / Projection layering defined in `AGENTS.md`.

### PLAN.md
# ExamOS: 考试通过率操作系统 Plan

## Summary

目标不是做“AI 学习助手”，而是把现有 `CFA_learning` 升级成一个前后端一体、AI 驱动、认知科学支撑的 **考试通过率操作系统**。

首版选择：**双线并行商业化，但产品只先打穿 CFA Level I 完整闭环**。

核心定位：

- B2C：让考生每天知道该做什么、为什么错、是否真的变强。
- B2B：让机构证明交付效果、降低老师/班主任服务成本、提前发现掉队学员。
- 系统角色：课后执行层 / 备考交付层，不做课程平台，不做泛题库，不做普通 AI 问答。

已有本地资产保留为内核：

- `.system/events/` = 原始学习证据
- `.system/memory/` = 长期认知资产
- `.system/app/` = 诊断和调度工作流
- `CFA_tier1/` = Obsidian / 内容投影
- 新增 Web 前后端作为产品驾驶舱

认知科学依据嵌入默认机制：retrieval practice、spaced practice、interleaving、worked example fading、self-explanation、metacognitive calibration、energy-aware planning。参考来源包括 Dunlosky 2013、Nature Reviews Psychology 2022、MIT Open Learning、MIT Learning Strategies Assessment、SAGE cognitive load theory。

## Key Changes

### 1. 产品架构

采用一个 integrated monorepo：

- `apps/web/`：前端驾驶舱，建议 Next.js + React + Tailwind/shadcn。
- `apps/api/`：后端 API，建议 FastAPI。
- `packages/exam-core/`：考试引擎，抽象 CFA 后未来可接 FRM/CPA/法考。
- `packages/study-science/`：认知科学调度器。
- `packages/agent-runtime/`：复用现有 6 个 agent 角色。
- `.system/`：继续作为 local-first source of truth。
- `CFA_tier1/`：继续作为 Obsidian / Markdown 投影层。

架构原则：

- 不让前端成为真相源。
- 不让 AI 直接给策略，必须先有事件证据。
- 不让笔记系统替代学习调度系统。
- 所有结论必须能追溯到 attempt、event、memory card 或 mock record。

### 2. 核心用户闭环

首版必须跑通一条完整 CFA 学习链：

1. 用户设置考试日期、当前阶段、每日可用时间、精力模式。
2. 系统生成 CFA Exam Map：topic、LOS、module、formula、trap、question type。
3. 用户刷题或上传错题截图。
4. 系统生成 `QuestionAttempt` 和 `MistakeEvent`。
5. Error Diagnosis Engine 判断错因：
   - knowledge gap
   - concept confusion
   - formula misuse
   - careless reading
   - time pressure
   - confidence calibration failure
   - fatigue / energy mismatch
   - agent failure
6. 每道错题转成：
   - fix rule
   - next drill
   - review due date
   - linked LOS
   - linked MOC node
   - pattern candidate
7. Daily Planner 生成今日任务：
   - 高精力：新知识、难题、交错题组、mock
   - 中精力：错题复盘、公式应用、worked example fading
   - 低精力：主动回忆卡、易混判断、轻量复习
8. Mock 前生成 pre-mock brief。
9. Mock 后生成 post-mock retro。
10. Dashboard 展示学习有效性，而不是单纯学习时长。

### 3. 前端模块

首版前端不做营销页，直接进入操作系统。

主要页面：

- `Today Cockpit`
  - 今日学习预算
  - 今日任务
  - 到期错题
  - 今日主动回忆目标
  - 当前最危险 3 个 LOS

- `Question Capture`
  - 手动录题
  - 截图上传
  - 信心选择：确定 / 不确定 / 猜的
  - 耗时记录
  - 错因快速选择

- `Diagnosis`
  - 错因分层：question / bias / agent
  - fix rule
  - next drill
  - 是否进入 pattern
  - 是否触发 MOC gap review

- `Review Pack`
  - 到期复习
  - 低信心题
  - 高信心错题
  - 交错题组
  - 公式 / 概念 warm start

- `Mock Center`
  - pre-mock brief
  - mock attempt upload
  - post-mock retro
  - 停止做的事
  - 下次 mock 策略

- `Effectiveness Dashboard`
  - 到期错题完成率
  - 高信心错误数量
  - interleaving 正确率
  - 同类错误下降趋势
  - LOS 风险热力图
  - 预计通过概率区间

- `Institution Console`
  - 班级风险榜
  - 掉队预警
  - 学员周报
  - 老师干预建议
  - 续费/交付证明报告

### 4. 后端能力与接口

新增核心类型：

- `ExamAdapter`
- `SyllabusNode`
- `QuestionAttempt`
- `MistakeEvent`
- `MistakeCard`
- `ErrorDiagnosis`
- `ReviewTask`
- `EnergyCheckIn`
- `StudyPlan`
- `MockSession`
- `PatternInsight`
- `InstitutionCohort`
- `LearnerProgressReport`

关键 API：

- `POST /api/attempts`
  - 记录刷题结果、信心、耗时、来源。

- `POST /api/attempts/screenshot`
  - 保存截图证据，交给 agent 做结构化提取。

- `POST /api/diagnose`
  - 生成错因、fix rule、next drill。

- `GET /api/review-pack/today`
  - 输出今日复习包。

- `POST /api/energy/check-in`
  - 记录今日精力预算。

- `GET /api/study-plan/today`
  - 输出今日任务清单。

- `POST /api/mock/{session_id}/retro`
  - 生成 mock 复盘。

- `GET /api/dashboard/effectiveness`
  - 输出学习有效性指标。

- `GET /api/institution/cohorts/{id}/risk-report`
  - 输出机构班级风险报告。

数据策略：

- 本地 MVP 继续 SQLite + JSONL。
- SaaS 版使用 Postgres + object storage。
- Obsidian Markdown 继续作为投影，不作为主存储。
- 所有 AI 输出写入 audit trail，支持追责和重算。

### 5. AI 与认知科学引擎

必须产品化 7 个引擎：

- `Retrieval Engine`
  - 每次学习先 recall / question，不先看答案。

- `Spacing Scheduler`
  - 根据信心、正确性、耗时、考试日期安排复习。

- `Interleaving Builder`
  - 默认配比：60% 当前弱点、20% 旧错题、10% 易混邻近点、10% 保鲜题。

- `Worked Example Fader`
  - 连续失败时进入：完整例题 → 隐藏步骤 → 独立解题。

- `Self-Explanation Prompt`
  - 每道错题只问极短复盘，不要求写长文。

- `Confidence Calibration`
  - 高信心错误优先级最高，因为它代表危险误解。

- `Energy-Aware Planner`
  - 根据精力安排任务，不让疲劳状态继续硬学新知识。

现有 6 个 agent 角色继续保留：

- `orchestrato...

### README.md
# OpenExam

OpenExam is a local-first, AI-augmented exam operating system for CFA Level I.
It combines a FastAPI backend, a Next.js cockpit, and cognitive-science study
engines (spaced repetition, retrieval practice, interleaving, self-explanation,
worked-example fading) to turn every question attempt into diagnosis, review
scheduling, daily planning, mock retros, and measurable progress.

This is not a generic flashcards app. It is a full learning evidence kernel —
your mistakes, patterns, calibration, and knowledge states are tracked locally,
analyzed algorithmically, and closed into a feedback loop powered by an
Ebbinghaus graduated knowledge memory model.

## Author

**Elian** — 计算机本科生，正在学习 CFA，目标留学爱尔兰。  
欢迎交流学习经验、备考方法、代码协作。  
这个系统是我边学 CFA 边写出来的，希望能帮到同样在备考的朋友，
也欢迎大佬们提 PR 和 Issue。

## Project Layout

- `apps/api/` — FastAPI backend: attempts, diagnosis, review packs, study plans,
  mock retros, dashboards, institution reports, knowledge memory.
- `apps/web/` — Next.js frontend cockpit, including LanguageOS and ResourceOS.
- `packages/study-science/` — retrieval, spacing, interleaving,
  worked-example fading, self-explanation, calibration, energy planning,
  and **knowledge memory** engines.
- `packages/agent-runtime/` — six AI agent role boundaries.
- `packages/resource-ingestion/` — policy-guarded public resource ingestion,
  deterministic fetching, discovery providers, and private FTS5 indexing.
- `.system/` — canonical local event stream, memory overlay, workflow kernel,
  exam profiles, and 40+ tests.
- `CFA_tier1/` — Obsidian/Markdown vault projection layer.

## Quick Start

```powershell
.\start-examos.ps1
```

Starts the API (port 8000), web app (port 3000), imports the 613 CFA mock
question bank, checks all dependencies, and opens `http://localhost:3000`.
Press `Ctrl+C` in the terminal to stop all services.

### What's included

| Service | URL | Description |
|---------|-----|-------------|
| **Web Cockpit** | `http://localhost:3000` | Today, review, mock, LanguageOS |
| **API** | `http://localhost:8000` | FastAPI with 47+ endpoints |
| **Mock Bank** | auto-imported | 613 CFA L1 questions across 10 subjects |
| **Logs** | `.system/logs/` | stdout/stderr for both processes |

**Health check:**

```powershell
Invoke-RestMethod http://localhost:8000/api/health
# → {"status":"ok","version":"0.1.0","exam":"CFA Level I"}
```

## CLI Still Works

```powershell
# Record a mistake
python scripts/cfa.py record-mistake --payload "{\"source_layer\":\"ques...

## Active Task
No active `docs/codex_tasks/TASK-*.md` file is linked to the latest plan.
