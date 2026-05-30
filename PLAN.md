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

- `orchestrator`
- `mistake_recorder`
- `review_coach`
- `pattern_miner`
- `strategy_coach`
- `validator`

不新增 agent，除非现有角色无法承担。

## Business Plan

商业策略：**B2C 做样板和数据，B2B/B2B2C 放大利润。**

B2C 定价：

- Free：错题诊断 3 次 / 每日计划基础版
- Pro：¥39-99/月
- Exam Pack：¥199-699/考试周期
- Premium Coaching OS：¥999-2999/完整备考期

B2B 定价：

- SaaS：¥10-50/学员/月
- 白标部署：setup fee + 月费
- 机构报告包：按班级或学员数收费
- 高阶版本：接入机构题库、CRM、班主任工作台

首批获客工具：

- 上传错题，判断真正错因
- CFA Level I 高频错因榜
- 7 天刷题诊断报告
- Mock 分数复盘报告生成器
- 下班党备考精力计算器
- 考纲-题型覆盖率扫描器
- 你现在离通过还差什么

核心卖点表达：

- 你不是缺资料，是缺把错题转成下一次决策的系统。
- 你以为刷了 1000 题，其实很多动作没有提高通过概率。
- 我们不卖课程，我们证明你每天有没有更接近通过。

## Roadmap

### Month 1-2: CFA ExamOS 内核

- 把现有 CLI 工作流升级为 API 服务。
- 完成 `QuestionAttempt`、`EnergyCheckIn`、`ReviewTask` 数据模型。
- 保留 `.system/events/` 和 `.system/memory/` 作为本地真相源。
- 完成 screenshot mistake capture 到 record-mistake 的闭环。
- 增强 daily-review-pack，使其支持 confidence、energy、interleaving。

### Month 3-4: 前端驾驶舱

- 实现 Today Cockpit。
- 实现 Question Capture。
- 实现 Diagnosis 页面。
- 实现 Review Pack。
- 实现 Effectiveness Dashboard。
- 把 Obsidian 页面作为高级阅读/投影，不作为主入口。

### Month 5: B2C MVP

- CFA 用户可以完整跑通：
  - 刷题
  - 错因诊断
  - 间隔复习
  - 今日计划
  - mock brief
  - mock retro
  - 学习有效性报告
- 内测 20-50 个 CFA Level I 用户。
- 追踪留存、每日使用、复习完成率、mock 提升、愿付价格。

### Month 6: B2B Pilot

- 增加机构班级视图。
- 输出学员掉队预警。
- 输出老师干预建议。
- 输出周报和交付证明。
- 找 2-3 个 CFA/FRM/财会培训机构试点。

## Test Plan

产品验证指标：

- D1/D7/D30 留存
- 每日任务完成率
- 到期错题复习完成率
- 高信心错误下降率
- 同一 `topic + los + error_type` 复发率
- mock 分数提升
- 用户是否每天知道下一步该做什么
- 机构是否减少人工跟进成本

工程测试：

- API 单元测试覆盖 attempt、diagnosis、review-pack、energy-plan、mock-retro。
- 回归测试确保旧 CLI 仍可运行。
- 数据一致性测试确保 dashboard、Obsidian、API 输出都回溯到同一 source of truth。
- Agent validation 测试确保无证据时不能生成高层策略。
- Screenshot capture 测试确保不脑补 LOS、题源和正确结论。

Acceptance Criteria：

- 用户不用懂学习法，也会被系统强制带入主动回忆、间隔复习、交错练习和信心校准。
- 每一道错题都能转成下一次行动。
- 每一个策略都能追溯到原始事件。
- B2C 用户看到的是“今天该做什么”。
- B2B 机构看到的是“谁在掉队、为什么、该怎么干预”。

## Assumptions & Evidence

Assumptions：

- 首个考试只做 CFA Level I。
- 商业线双线并行，但工程优先保证 B2C CFA 闭环完整。
- 现有 `.system/` 架构不推倒重来，而是产品化。
- Obsidian 继续存在，但降级为投影层。
- 不做课程内容平台，不做泛教育题库。

Evidence：

- AI 教育增长预期：多鲸 / 新浪教育报道 2025 中国 AI+教育市场超 700 亿元，2030 接近 3000 亿元。
  https://edu.sina.com.cn/l/2025-06-24/doc-infccuqs6862520.shtml

- 职业教育培训市场规模大：智研咨询报告提到 2024 年中国职业教育培训行业规模约 5946 亿元。
  https://www.chyxx.com/industry/1218669.html

- 教育投诉痛点集中在退款、售后、虚假宣传，说明机构需要可证明交付。
  https://data.eastmoney.com/report/zw_industry.jshtml?infocode=AP202507211712892813

- Spacing + retrieval 是高证据学习机制。
  https://www.nature.com/articles/s44159-022-00089-1

- MIT Open Learning 支持 spaced and interleaved practice。
  https://openlearning.mit.edu/mit-faculty/research-based-learning-findings/spaced-and-interleaved-practice

- MIT Learning Strategies Assessment 将时间/努力、认知、动机、wellbeing 纳入学习调节。
  https://tll.mit.edu/mit-learning-strategies-assessment/

- Worked examples 与 guidance fading 来自 cognitive load theory。
  https://journals.sagepub.com/doi/10.1177/0963721420922183
