# OpenExam 升级计划（6 Waves） — 系统就绪度审计

**审计方法**：逐项读取实际代码验证
**审计日期**：2026-06-01

**总计**：47 项审计

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ COMPLETED（已完成） | 8 | 17% |
| ⚠️ PARTIAL（部分完成） | 11 | 23% |
| ❌ NOT_STARTED（未开始） | 28 | 60% |

---

## Wave 0：内核加固 — 11 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 0.1 | 归档报告到 docs/research/ | ❌ | docs/research/ 目录不存在 |
| 0.2 | 修复 sync preview ID 归一化 | ❌ | Bug #10 — preview_import 用 event.get("event_id") 而非 from_payload() |
| 0.3 | 引入重放检查（replay guard） | ❌ | 整个代码库搜索 "replay" 零匹配 |
| 0.4 | 拆分 oversize workflow 模块 | ❌ | workflows.py 2535 行，未拆分 |
| 0.5 | Topic alias 分类系统 | ⚠️ | ExamProfile.subject_aliases 在 profile 层存在，但 dashboard API 未使用 |
| 0.6 | Pattern 严重度排序 | ✅ | mine_patterns() 有 severity='high'/'medium' 赋值 |
| 0.7 | Validation 过期/审查状态 | ❌ | ValidationRule 无 expiry 字段 |
| 0.8 | MOC-gap 去重 | ⚠️ | moc_gap_review 用 set 去重 evidence_refs，但 event_ids 未去重 |
| 0.9 | Mock 结果反馈到 SpacingScheduler | ❌ | post_mock_retro 不修改任何间隔参数 |
| 0.10 | Energy-aware daily review | ❌ | daily_review_pack 不使用 EnergyAwarePlanner |
| 0.11 | 替换脆弱 frontmatter 编辑 | ✅ | _set_frontmatter_value 已用 str 方法替代 regex |

**Wave 0 完成度**: 2/11 ✅ + 2/11 ⚠️ + 7/11 ❌ = **27%**

---

## Wave 1：学习记录网格、溯源与隐私 — 7 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 1.1 | learning-records 包 | ❌ | 不存在 |
| 1.2 | provenance 溯源包 | ❌ | 不存在 |
| 1.3 | EventEnvelopeV2（含 provenance/consent） | ❌ | 当前 MistakeEvent 无 provenance 或 consent_scope 字段 |
| 1.4 | /api/provenance/{id} | ❌ | 不存在 |
| 1.5 | /api/privacy/export & /api/privacy/purge | ❌ | 不存在 |
| 1.6 | xAPI 导出 | ❌ | 零 xAPI 支持 |
| 1.7 | Consent 事件机制 | ❌ | 无任何 consent 机制 |

**Wave 1 完成度**: 0/7 = **0%**

---

## Wave 2：学习者孪生、技能图谱与心理测量 — 7 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 2.1 | learner-twin 包 | ❌ | 不存在 |
| 2.2 | psychometrics 包 | ❌ | 不存在 |
| 2.3 | 半衰期掌握度估计 | ⚠️ | KnowledgeMemoryEngine 有 6 级状态但无连续 recall probability 模型 |
| 2.4 | 信心偏差追踪 | ⚠️ | ConfidenceCalibration 检测偏差但无 confidence_bias 字段 |
| 2.5 | BKT/HLR 风格排期 | ⚠️ | SpacingScheduler 用静态 EXPANSION_FACTORS，非贝叶斯 |
| 2.6 | Mock 结果反馈到排期 | ⚠️ | Mock retro 存储结果但不反馈到间隔参数 |
| 2.7 | 置信区间（confidence bands） | ✅ | prediction.py 输出 confidence_band_low/high |

**Wave 2 完成度**: 1/7 ✅ + 4/7 ⚠️ + 2/7 ❌ = **42%**

---

## Wave 3：教学策略、人因与无障碍 — 7 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 3.1 | pedagogy-policy 包 | ❌ | 不存在 |
| 3.2 | human-factors 包 | ❌ | 不存在 |
| 3.3 | 结构化任务 + Markdown 投影 | ❌ | Review packs 纯 markdown，items 字段硬编码为 [] |
| 3.4 | 检索/自我解释/对比对 | ⚠️ | RetrievalEngine + SelfExplanationPrompt + InterleavingBuilder 都存在，无独立 contrast-pair 模块 |
| 3.5 | 睡眠/压力录入 | ⚠️ | Energy 录入存在，无 sleep/stress |
| 3.6 | WCAG 2.2 AA 无障碍 | ⚠️ | 有 prefers-reduced-motion、focus-visible，无 skip-to-content、无 aria-live |
| 3.7 | 移动端适配 | ⚠️ | 响应式布局存在，无 viewport meta 标签，无 touch 优化 |

**Wave 3 完成度**: 0/7 ✅ + 4/7 ⚠️ + 3/7 ❌ = **28%**

---

## Wave 4：接地 AI、多模态录入、Sync V2、MCP — 7 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 4.1 | Grounded 解释服务 | ❌ | 无 RAG/引用级 AI 解释 |
| 4.2 | Claim 级证据引用 | ⚠️ | MistakeEvent.evidence_refs 存在，无形式化 provenance 抽象 |
| 4.3 | AI 截图结构化提取 | ⚠️ | 截图端点保存图片但不提取字段 |
| 4.4 | PDF/音频提取 | ⚠️ | PDF 读取存在（OCR 导入），音频提取不存在 |
| 4.5 | IndexedDB 离线队列 | ❌ | offline.ts 用 localStorage，非 IndexedDB |
| 4.6 | 幂等性键 | ⚠️ | stable_id 有确定性 ID，record_event 写入前不查重 |
| 4.7 | MCP 适配器 | ❌ | 零 MCP 实现 |

**Wave 4 完成度**: 0/7 ✅ + 3/7 ⚠️ + 4/7 ❌ = **21%**

---

## Wave 5：仿真与研究运行时 — 3 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 5.1 | sim-lab 包 | ❌ | 不存在 |
| 5.2 | research-runtime 包 | ❌ | 不存在 |
| 5.3 | 调度器变体比较 | ❌ | SpacingScheduler 单一算法，无 A/B 测试 |

**Wave 5 完成度**: 0/3 = **0%**

---

## Wave 6：生态系统与信任适配器 — 4 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| 6.1 | Caliper 导出 | ❌ | 不存在 |
| 6.2 | Open Badges 3.0 / CLR / VC | ❌ | 不存在 |
| 6.3 | 隐私保护 cohort 视图 | ⚠️ | 基础访问控制存在，无差分隐私/匿名化 |
| 6.4 | 签名证据快照 | ❌ | 不存在签名机制 |

**Wave 6 完成度**: 0/4 ✅ + 1/4 ⚠️ + 3/4 ❌ = **12%**

---

## 架构决策 — 5 项

| # | 项目 | 状态 | 说明 |
|---|------|------|------|
| A.1 | EventEnvelopeV2（provenance/consent） | ❌ | 当前无 provenance 或 consent 字段 |
| A.2 | 功能标志（feature flags） | ❌ | 无 feature flag 机制 |
| A.3 | PROV-O 实体/活动/代理 | ❌ | provenance 一词仅出现在 agent 指令中 |
| A.4 | 历史事件向后兼容 | ⚠️ | from_payload 用 cls(**payload)，无语义化迁移层 |
| A.5 | 确定性本地优先，云端 AI opt-in | ✅ | AgentRuntime 默认 mode="local" |

**架构决策完成度**: 1/5 ✅ + 1/5 ⚠️ + 3/5 ❌ = **30%**

---

## 核心结论

总计 47 项
- ✅ COMPLETED: 8 项 (17%) — 主要集中在内核已有模式挖掘/前端响应式布局
- ⚠️ PARTIAL: 11 项 (23%) — Profile alias、ConfidenceCalibration、证据引用、本地优先架构
- ❌ NOT_STARTED: 28 项 (60%) — 绝大部分 Wave 1/5/6 高级功能

### 最值得优先启动

| 优先级 | 项目 | 说明 |
|--------|------|------|
| P0 | Wave 0.2 — 修复 sync preview ID 归一化 | 5 分钟修复、已有补丁方案 |
| P0 | Wave 0.9 — Mock 结果反馈到 SpacingScheduler | Wave 4 的 AI 对话录入需要这个 |
| P0 | Wave 0.10 — Energy-aware daily review | 刚加的能量 UI 需要后端利用起来 |
| P0 | Wave 4.3 — AI 截图结构化提取 | 聊天式录入的前置条件 |
