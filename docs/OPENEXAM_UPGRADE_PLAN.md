# OpenExam 深度升级执行手册

> 版本: 1.0  
> 日期: 2026-06-03  
> 基于: 2.md 系统生态审计与升级计划  

---

## 1. 项目概述

### 1.1 核心目标

将 OpenExam 从"能生成学习材料"升级为"能筛选、验证、追踪、复习高价值学习资产"的系统。

### 1.2 战略判断

未来 OpenExam 的强大不在于抓更多网页、生成更多卡片、做更多 dashboard，而在于：

- 每个知识点是否来源清楚
- 每个公式是否完整
- 每个复习项是否真的被主动回忆
- 每个词是否有权威释义和真实语境
- 每个资源是否值得进入学习系统
- 每次复习是否真实改变下一次安排

### 1.3 升级范围

| 维度 | 现状 | 目标 |
|------|------|------|
| 学习闭环 | DailyReview 批量标记完成，无能量感知 | Per-unit 评分 + EnergyAwarePlanner + 反馈链路 |
| 知识来源 | 仅 MOC 表格抽取 | PDF 笔记扫描 + 公式库 + 覆盖率审计 |
| 语言学习 | front=answer 的浅层卡片 | Dictionary-driven + CEFR 过滤 + 西语形态学 |
| 资源质量 | 无门槛爬虫 | Quality Score + Candidate Queue + 四级门控 |
| 用户体验 | Markdown 阅读 | Recall-first Lab + 统一仪表盘 + PWA |

---

## 2. 多 Agent 团队架构

### 2.1 团队分工

| Agent | 职责 | Wave | 核心交付物 |
|-------|------|------|-----------|
| 架构师 | 技术规范、接口契约、事件格式 | 全阶段 | 架构规范文档、基类模型、Feature Flag 系统 |
| KnowledgeOS | 知识 PDF 解析 + 覆盖率审计 | Wave 1-2 | PDF 提取管道、Coverage Dashboard、Atom 模型 |
| DailyReview | 交互式复习实验室 | Wave 3 | Recall/Reveal 组件、Unit 评分、Formula Lab |
| LanguageOS | 词典系统 + 高质量卡片 | Wave 4-5 | DictionaryOS、Card Factory v2、西语形态学 |
| ResourceOS | 资源质量引擎 | Wave 6 | Quality Score、Candidate Queue、四级门控 |
| Dashboard | 统一仪表盘 + UI 整合 | Wave 7 | 学习指标、PWA 支持、信息架构重组 |
| QA | 测试策略 + 验收 | 全阶段 | 测试框架、E2E 用例、性能基准 |

### 2.2 协作机制

```
Phase 1 (Week 1): 架构规范产出
    ↓ 架构师 Agent 产出规范文档（事件 Schema、基类模型、目录约定）
Phase 2 (Week 2-3): 核心 Wave 并行
    ├─ KnowledgeOS Agent (Wave 1-2)
    ├─ DailyReview Agent (Wave 3，依赖 Wave 1-2 模型)
    └─ LanguageOS Agent (Wave 4-5，相对独立)
Phase 3 (Week 3-4): 质量与整合
    ├─ ResourceOS Agent (Wave 6，可并行)
    └─ Dashboard Agent (Wave 7，依赖前序数据)
Phase 4 (Week 5): 验收与调优
    └─ QA Agent 全量回归测试
```

---

## 3. 执行路线图

### 3.1 总时间线

```
Week 1: 架构基线
├── Day 1-2: 架构师产出 → EventEnvelopeV2、BaseAtom、Feature Flags
├── Day 2-3: KnowledgeOS Wave 1 → PDF 解析管道（可独立开发）
└── Day 3-5: DailyReview Wave 3 → 模型 + API（依赖架构规范）

Week 2: 核心闭环
├── Day 5-7: KnowledgeOS Wave 2 → Coverage Audit
├── Day 5-8: DailyReview Wave 3 → 前端组件 + 评分逻辑
└── Day 6-9: LanguageOS Wave 4 → DictionaryOS 导入管道（可并行）

Week 3: 语言内核
├── Day 8-12: LanguageOS Wave 5 → Card Factory v2 + 西语形态学
└── Day 10-12: ResourceOS Wave 6 → Quality Engine（可并行）

Week 4: 整合与界面
├── Day 12-14: Dashboard Wave 7 → 统一仪表盘
└── Day 13-14: PWA + 引导流程 + UI 整合

Week 5: 验收
├── Day 15-17: QA 回归测试 + 性能调优
└── Day 17-18: Feature Flag 灰度开启
```

### 3.2 依赖关系

```
架构规范（阻塞所有）
    │
    ├──→ KnowledgeOS W1-2 ──→ DailyReview W3
    │         │
    │         └──→ Coverage Dashboard (W7)
    │
    ├──→ LanguageOS W4-5 ──→ Dashboard LanguageTab (W7)
    │         │
    │         └──→ Dictionary Browser UI
    │
    ├──→ ResourceOS W6 ──→ Dashboard ResourcesTab (W7)
    │
    └──→ Dashboard W7（依赖所有 Wave 的 API）
```

**可并行开发组**：
- Group A: KnowledgeOS W1-2 + DailyReview W3（前后端协作）
- Group B: LanguageOS W4-5（相对独立，DictionaryOS 不依赖其他 Wave）
- Group C: ResourceOS W6（完全独立）

---

## 4. 跨 Wave 接口契约

### 4.1 事件 Schema v2（所有 Wave 必须遵守）

```python
class EventEnvelopeV2:
    event_id: str          # UUID
    event_type: str        # dot-notation: wave.entity.action
    timestamp: str         # ISO 8601
    idempotency_key: str   # SHA-256 of (event_type + payload_keys)
    source_span: dict      # {source_id, page, block_refs, locator}
    confidence: float      # 0.0-1.0, default 1.0
    payload: dict
```

### 4.2 关键事件类型

| Wave | 事件类型 | 说明 |
|------|---------|------|
| W1-2 | `knowledge.source.uploaded` | PDF 上传 |
| W1-2 | `knowledge.atom.extracted` | 原子提取 |
| W1-2 | `knowledge.quarantine.queued` | 进入隔离区 |
| W1-2 | `knowledge.atom.promoted` | 确认进入知识库 |
| W2 | `knowledge.coverage.report_generated` | 覆盖率报告 |
| W3 | `review_lab.session.started` | 复习会话开始 |
| W3 | `review_lab.unit.outcome` | 单个单元评分 |
| W3 | `review_lab.session.completed` | 会话完成 |
| W4 | `language.dictionary.imported` | 词典导入 |
| W4 | `language.dictionary.entry.indexed` | 词条索引 |
| W5 | `language.card.v2.created` | v2 卡片生成 |
| W5 | `language.card.invariant_violation` | 违反 front!=answer |
| W6 | `resource.candidate.scored` | 资源评分 |
| W6 | `resource.candidate.approved` | 用户审批通过 |
| W6 | `resource.promoted` | 升级为学习材料 |

### 4.3 基类模型

```python
class BaseAtom:
    atom_id: str
    source_id: str
    source_span_ids: list[str]   # 不可为空
    confidence: float
    promotion_status: Literal["draft", "quarantined", "confirmed", "rejected"]
    created_at: str
```

---

## 5. 质量红线（不可协商）

1. **每个知识 atom 必须有 `source_span_ids`** — 在基类构造函数中强制校验
2. **每个 formula 必须有 variables, conditions, example, trap, source** — FormulaLabCard schema 强制
3. **每个 review unit 独立评分** — `complete_daily_review()` 批量标记逻辑废弃，改为 per-unit
4. **front != answer** — CardFactoryV2 在 `create_card()` 中抛 `ValueError`
5. **资源必须通过 Quality Score >= threshold** 才能进入 corpus — `resource.candidate.approved` 事件前校验
6. **所有新功能 behind feature flags** — 默认 false，可独立回滚
7. **AI enrichment 必须有 source span + 置信度** — 所有 AI 生成内容标注来源

---

## 6. Feature Flags 清单

```yaml
# .system/config/features.yaml
knowledge_pdf_ingestion: false
knowledge_atom_extraction: false
knowledge_coverage_audit: false
daily_review_lab: false
daily_review_unit_scoring: false
formula_lab: false
dictionary_os: false
dictionary_private_index: false
language_cards_v2: false
spanish_morphology_engine: false
resource_quality_gate: false
resource_candidate_queue: false
ai_knowledge_enrichment: false
unified_dashboard: false
pwa_offline: false
cfa_onboarding: false
```

**回滚原则**：所有新增内容都是事件和 projection，不改旧历史。关闭 flag 后退回旧行为。

---

## 7. Wave 详细设计

### 7.1 Wave 1: Knowledge PDF Ingestion

**目标**: 上传笔记 PDF，生成可确认的知识点/公式/例题/陷阱。

**核心组件**:

| 文件 | 职责 |
|------|------|
| `pdf_loader.py` | PyMuPDF4LLM 布局感知提取 + 降级到 PyMuPDF |
| `layout_parser.py` | 按字体/大小/位置分类 block（heading/paragraph/formula/table/note/list） |
| `formula_extractor.py` | 数学公式检测 + LaTeX 规范化 |
| `table_extractor.py` | 表格结构提取为 Markdown |
| `note_segmenter.py` | 侧边栏/标注框检测 |
| `atom_extractor.py` | 将 block 分组为候选 KnowledgeAtom |
| `atom_classifier.py` | 10 类型分类器（definition/formula/procedure/example/exam_trap/comparison/condition/exception/mnemonic） |

**数据模型**:

```python
class KnowledgeAtom:
    atom_id: str
    source_id: str
    atom_type: AtomType
    subject: str
    module_id: str
    los_codes: list[str]
    title: str
    content: str
    formula_latex: str
    table_markdown: str
    page_number: int
    block_refs: list[str]
    extraction_confidence: float
    verified: bool
```

**Quarantine 规则**:

| 条件 | 原因 |
|------|------|
| confidence < 0.6 | 分类不确定 |
| formula 类型但无 LaTeX | 公式提取失败 |
| 内容哈希重复 | 重复内容 |
| LOS 映射失败 | 无 LOS 标签 |
| 长度 >5000 或 <10 | 提取异常 |

**API 端点**:

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/knowledge/sources/upload` | 上传 PDF |
| GET | `/api/knowledge/sources` | 列出所有源 |
| GET | `/api/knowledge/quarantine` | 列出隔离区项目 |
| POST | `/api/knowledge/quarantine/{id}/resolve` | 审批/拒绝/编辑 |

---

### 7.2 Wave 2: Knowledge Coverage Audit

**目标**: 告诉你哪些重要知识没进 daily review。

**Coverage 评分公式**:

```python
coverage_score(los) = min(1.0,
    0.35 * type_diversity_score
  + 0.35 * min(atoms_found / target_atoms, 1.0)
  + 0.30 * avg_mastery_state
)

overall_score(subject) = sum(coverage_score(los) * exam_weight(los)) / sum(exam_weight(los))
```

**Gap 类型**:

| Gap 类型 | 条件 | 严重度 |
|----------|------|--------|
| missing | atoms_found == 0 | high |
| underrepresented | coverage_score < 0.3 | high |
| type_imbalance | type_diversity_score < 0.5 | medium |
| low_mastery | avg_mastery_state < 0.3 | medium |

**Dashboard 指标**:
- Subject coverage
- Module coverage
- LOS coverage
- Formula coverage
- Definition coverage
- Trap coverage
- Example coverage
- Review coverage
- Decay risk
- Unlinked mistakes
- Unlinked PDF notes
- Uncovered high-weight LOS

---

### 7.3 Wave 3: DailyReview Lab

**目标**: 从 Markdown review 变成交互式 recall-first 复习。

**核心问题**: `complete_daily_review()` 批量标记所有 knowledge 为 `confidence_after=2`，破坏 per-item 信号。

**新模型**:

```python
class DailyReviewUnit:
    unit_id: str
    unit_type: Literal["knowledge_recall", "formula_lab", "mistake_card", "worked_example", "interleaving_drill", "transfer_drill"]
    prompt: str                    # 用户先看到的问题
    recall_instruction: str        # 具体指令
    answer: str                    # 隐藏直到 reveal
    formula_latex: str
    worked_example: dict
    common_wrong_path: str
    exam_trap: str
    source_refs: list[str]
    source_spans: list[dict]
    memory_state: dict
    priority: int
    interaction_mode: Literal["recall_reveal", "formula_manipulate", "worked_fade", "mcq_transfer"]

class ReviewUnitOutcome:
    unit_id: str
    confidence_before: int         # 0-4
    time_spent_seconds: int
    needed_hint: bool
    outcome: Literal["recalled", "partial", "forgot", "skipped"]
    confidence_after: int          # 0-4
    answer_quality: float          # 0.0-1.0
    fix_rule_helpful: bool
    next_action: Literal["advance", "maintain", "retreat", "drill_more", "schedule_transfer"]
```

**Recall-First 状态机**:

```
IDLE → HIDDEN → ATTEMPT → REVEALED → SCORING → SUBMIT → NEXT
```

**键盘快捷键**:

| 按键 | 动作 | 状态 |
|------|------|------|
| Space | 显示答案 | Hidden |
| 1 | Again / Forgot | Revealed |
| 2 | Hard / Partial | Revealed |
| 3 | Good / Recalled | Revealed |
| 4 | Easy / Recalled+ | Revealed |
| H | 请求提示 | Hidden |
| S | 跳过 | Any |
| P | 暂停 | Any |

**Outcome 到 KnowledgeMemoryEngine 映射**:

| Outcome | KMEngine 输入 |
|---------|--------------|
| recalled | reviewed |
| partial | struggled |
| forgot | forgot |
| skipped | struggled |

**迁移策略**:
- Phase 1: 部署新端点，旧流程不变
- Phase 2: `/review` 页面添加"Try Lab Mode"按钮
- Phase 3: `/review/lab` 设为默认，保留 `/review?mode=classic`
- Phase 4: 30 天后移除 classic mode

---

### 7.4 Wave 4: DictionaryOS

**目标**: 上传英英词典和西英词典，建立语言学习权威内核。

**存储布局**:

```
.system/private/language-dictionaries/
  english_english/
    wordnet/              # Princeton WordNet 3.1
    freedict/             # FreeDict en-en
    custom/               # 用户上传
  spanish_english/
    spanish_data/         # spanish_data 项目
    freedict/             # FreeDict spa-eng
    wikidata/             # Wikidata Lexeme
  manifests/
    {source_id}.json      # 词典元数据
  indexes/
    lemma_index.db        # SQLite FTS5
    cefr_index.db         # CEFR 映射
    morphology_cache.db   # 变位/性数缓存
```

**数据模型**:

```python
class LexicalEntry:
    entry_id: str
    lemma: str
    pos: str
    language: str
    source_id: str
    etymology: str
    pronunciation: str      # IPA
    audio_ref: str
    inflections: list[dict]
    gender: str             # masculine/feminine
    senses: list[Sense]

class Sense:
    sense_id: str
    definition: str
    examples: list[str]
    synonyms: list[str]
    antonyms: list[str]
    register: str           # formal/informal/slang
    domain: str             # finance/law/medicine
    cefr_level: str         # A1-C2
    frequency_band: str
    translations: list[BilingualMapping]
```

**支持格式**:

| 格式 | 优先级 | 说明 |
|------|--------|------|
| WordNet | 高 | en-en 语义网络底座 |
| FreeDict | 高 | TEI XML，多语言 |
| Wikidata Lexemes | 高 | 形态、false friends |
| CSV/TSV | 中 | 用户自定义 |
| JSON | 中 | 结构化导出 |
| TEI XML | 中 | 学术词典 |
| StarDict | 低 | 开源词典格式 |
| MDict | 可选 | MDX 转换器 |
| PDF | 低置信度 | 结构复杂 |

**CEFR 过滤**:

```python
CEFR_BANDS = {
    "A1": ["A1", "limited A2"],
    "A2": ["A1", "A2", "limited B1"],
    "B1": ["A2", "B1", "limited B2"],
    "B2": ["B1", "B2", "selected C1"],
    "C1": ["B2", "C1", "selected C2"],
    "C2": ["all", "nuance/register"],
}
```

---

### 7.5 Wave 5: Language Card Factory 2.0

**目标**: 彻底淘汰低质量词卡。

**关键规则**: `front != answer` 对所有卡片类型强制执行。

**新卡片类型**:

| # | 类型 | 正面 | 背面 |
|---|------|------|------|
| 1 | Definition -> Word | 释义 | 单词 |
| 2 | Word -> Sense | 单词 + 语境 | 定义/用法 |
| 3 | Example Cloze | 填空句 | 目标词 |
| 4 | Collocation Completion | 搭配缺词 | 缺失词 |
| 5 | Reverse Translation | 母语翻译 | 目标语 |
| 6 | Audio Dictation | 音频 | 书面形式 |
| 7 | Shadowing | 音频 + 文本 | 自录音 |
| 8 | Spanish Gender | 西语名词 | el/la + 名词 |
| 9 | Spanish Conjugation | 不定式 + 时态提示 | 变位形式 |
| 10 | False Friend Warning | 假朋友对 | 正确含义 |
| 11 | Register Choice | 语境 + 选项 | 适当语域 |
| 12 | Domain Usage | 词 + 领域语境 | 领域特定含义 |

**CFA 金融例句**:

```
Front:
Definition: to reduce the value of existing shares by issuing more shares.
Context: The new share issue may ___ existing shareholders.

Back:
dilute / dilutive
Sense: finance
Collocations: dilutive effect, diluted EPS, anti-dilutive
CFA link: EPS / share issuance
Source: dictionary + CFA segment
```

**西语 False Friend 例句**:

```
Front:
Choose the right meaning:
actualmente

Back:
currently / at present
Not: actually
False friend warning: English "actually" = en realidad
```

---

### 7.6 Wave 6: Resource Quality Engine

**目标**: 解决"爬取内容质量极低"。

**四级内容门**:

```
Level 0: discovered metadata
Level 1: candidate resource
Level 2: imported corpus
Level 3: promoted learning material
Level 4: reviewed and validated item
```

**Quality Score 公式**:

```python
final_score =
  0.20 * authority_score
+ 0.20 * domain_relevance_score
+ 0.15 * level_fit_score
+ 0.15 * signal_density_score
+ 0.15 * extractability_score
+ 0.10 * license_safety_score
- 0.05 * duplicate_penalty
- 0.10 * spam_penalty
```

**各维度说明**:

| 维度 | 计算方式 |
|------|---------|
| authority_score | 来源权威性（官方 > 学术 > 媒体 > 博客） |
| domain_relevance | 与 CFA/语言学习主题的相关度 |
| level_fit | CEFR 匹配度 |
| signal_density | 信息密度（公式/定义/例题 占比） |
| extractability | 结构化提取难度 |
| license_safety | 版权安全度 |
| duplicate_penalty | 与现有 corpus 重复度 |
| spam_penalty | 广告/噪声内容检测 |

**推荐理由展示**:

每条资源显示：
- 为什么适合你
- CEFR 匹配度
- 领域匹配度
- 是否有字幕/文本
- 预计可产出多少高质量词条
- 版权状态
- 适合听力/阅读/写作
- 是否已有重复内容

---

### 7.7 Wave 7: Unified Dashboard

**目标**: 让用户看到"我是不是变强了"。

**新增指标**:

| 指标 | 数据源 |
|------|--------|
| Knowledge coverage | LOS atom coverage |
| Formula mastery | 30 天内 formula 召回率 |
| Review quality | 每会话平均 confidence delta |
| Forgotten important atoms | decay_risk = "high" 的知识点 |
| Language retention | FSRS retrievability 平均 |
| Dictionary-backed vocabulary | 有词典释义的词条数 |
| Output gap | 目标词汇 - 活跃词汇 |
| Listening accuracy | 听写/听力卡片正确率 |
| Spanish morphology accuracy | 语法分析准确率 |
| Resource quality distribution | 按 license mode 分布 |

**PWA 实现**:

```json
// manifest.json
{
  "name": "OpenExam",
  "short_name": "OpenExam",
  "start_url": "/today",
  "display": "standalone",
  "background_color": "#f5f5f7",
  "theme_color": "#007aff"
}
```

**Service Worker 三级缓存**:

| 缓存 | 策略 | 内容 |
|------|------|------|
| shell-v3 | Cache-first | HTML/JS/CSS |
| data-v1 | Stale-while-revalidate | API 响应 |
| projection-v1 | Cache-first + background sync | JSONL 事件 + Markdown 投影 |

**新用户引导 (CFA Cockpit)**:

```
Step 1: Welcome
Step 2: Set Exam Date
Step 3: Choose Subjects
Step 4: Capture First Question
Step 5: Dashboard Tour (coach marks)
Step 6: Done
```

**无障碍 (WCAG 2.2)**:
- 所有图表有 aria-label
- KPI 卡片使用语义化 article/header/footer
- 对比度 4.5:1 (文本), 3:1 (大号文本)
- 键盘可操作，Tab 顺序合理
- Touch target >= 44x44px
- prefers-reduced-motion 禁用 GSAP

---

## 8. 文件创建总清单

### Wave 1-2 (KnowledgeOS) — 28 个文件

```
packages/knowledge-ingestion/
  pyproject.toml
  src/knowledge_ingestion/
    __init__.py
    models.py
    pdf_loader.py
    layout_parser.py
    formula_extractor.py
    table_extractor.py
    note_segmenter.py
    atom_extractor.py
    atom_classifier.py
    los_mapper.py
    coverage_auditor.py
    enrichment_planner.py

.system/app/
  knowledge_source_models.py
  knowledge_source_workflows.py
  knowledge_coverage.py
  knowledge_promotion.py

apps/api/routers/
  knowledge_sources.py
  knowledge_coverage.py

apps/web/src/app/knowledge/
  page.tsx
  upload/page.tsx
  quarantine/page.tsx
  coverage/page.tsx

apps/web/src/components/knowledge/
  AtomCard.tsx
  CoverageHeatmap.tsx
  PipelineStatus.tsx
```

### Wave 3 (DailyReview) — 12 个文件

```
packages/study-science/src/study_science/
  review_lab.py
  review_lab_models.py

apps/api/routers/
  review_lab.py

apps/web/src/app/review/lab/
  page.tsx

apps/web/src/components/review-lab/
  RecallRevealCard.tsx
  FormulaLabCard.tsx
  ReviewOutcomeButtons.tsx
  LabCompletionModal.tsx

apps/web/src/hooks/
  useKeyboardShortcuts.ts
  useLabSession.ts
```

### Wave 4-5 (LanguageOS) — 16 个文件

```
packages/language-science/src/language_science/
  dictionary_models.py
  dictionary_importers.py
  dictionary_index.py
  cards_v2.py
  spanish_morphology.py
  false_friends.py
  cefr.py
  lexical_graph.py

apps/web/src/app/language/dictionary/
  page.tsx
  import/page.tsx

apps/web/src/components/language/
  DictionaryReviewCard.tsx
  SpanishConjugationTable.tsx

.system/tests/
  test_dictionary_card_invariant.py
  test_spanish_morphology.py
  test_dictionary_import.py
```

### Wave 6 (ResourceOS) — 6 个文件

```
packages/resource-ingestion/src/resource_ingestion/
  quality.py
  candidate_queue.py

.system/app/
  resource_promotion.py

apps/api/routers/
  resource_candidates.py

apps/web/src/app/resources/candidates/
  page.tsx

.system/tests/
  test_resource_quality.py
```

### Wave 7 (Dashboard) — 15 个文件

```
apps/web/src/components/dashboard/
  UnifiedDashboard.tsx
  KPISection.tsx
  KPICard.tsx
  DashboardTabs.tsx
  OverviewTab.tsx
  CFATab.tsx
  LanguageTab.tsx
  ReviewTab.tsx
  ResourcesTab.tsx
  KnowledgeCoverageDonut.tsx
  ReviewQualityGauge.tsx
  ForgottenAtomsAlert.tsx
  RetentionTrendLine.tsx
  ForgettingCurveChart.tsx
  MiniCalendar.tsx
  LanguageToggle.tsx
  OnboardingModal.tsx
```

---

## 9. 测试策略

### 9.1 测试金字塔

| 层级 | 占比 | 目标 | 位置 |
|------|------|------|------|
| 单元测试 | 70% | 核心逻辑覆盖 | `apps/api/tests/`, `.system/tests/` |
| 集成测试 | 20% | API 端点 | `apps/api/tests/test_api_*.py` |
| E2E 测试 | 10% | 用户流程 | `apps/web/tests/*.spec.ts` |

### 9.2 关键不变量测试

```python
# 1. source_span_ids 必须存在
def test_every_atom_has_source_span_ids(): ...

# 2. formula 完整性
def test_every_formula_has_variables_conditions_example_trap(): ...

# 3. per-unit 评分
def test_every_review_unit_records_outcome_individually(): ...

# 4. front != answer
def test_no_card_has_front_equal_answer(): ...

# 5. 词典丰富度
def test_dictionary_entries_have_senses_examples_collocations(): ...

# 6. 资源质量门
def test_resources_pass_quality_gate_before_promotion(): ...

# 7. AI 引用
def test_ai_enrichment_has_source_span_and_confidence(): ...

# 8. Feature Flag 保护
def test_all_new_features_behind_flags(): ...

# 9. 投影可重建
def test_projections_rebuildable_from_jsonl(): ...
```

### 9.3 CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
jobs:
  api-tests:
    - pytest -q                    # 单元测试 < 30s
    - pytest test_api_*.py -v      # 集成测试 < 60s
    - pytest test_invariants.py -v # 不变量测试 < 30s
    - pytest test_regression_*.py  # 回归测试 < 45s

  web-tests:
    - npm run typecheck
    - npm run lint
    - npx playwright test          # E2E < 3min
    - npx playwright test a11y.spec.ts  # 无障碍 < 2min

  cross-agent:
    - pytest test_cross_agent.py -v  # 跨 Wave 集成 < 60s
```

---

## 10. 对标竞品启示

| 竞品 | 优势 | 需借鉴 |
|------|------|--------|
| Anki | 成熟 FSRS-5、丰富卡片类型、移动端同步 | FSRS 个性化调度、多卡片类型、PWA |
| UWorld/Schweser | 庞大题库、详细解释、模考评分 | 题库导入模板、全真模考、错题高质量解释 |
| Quizlet/Duolingo | 简洁 UI、游戏化、多语言课程 | 界面友好度、游戏化元素、完整语言课程 |

---

## 11. 结论

OpenExam/EXAMOS 已建立完整技术框架，但要从"设想很好"变成"每天真的提高效率"，需从闭环完成、内容升级、语言学习、用户体验、代码架构五个维度优化。

**核心判断**: 你现在不缺"宏大设计"，你缺的是**学习对象的质量控制**。

通过引入高质量词典数据、PDF 笔记扫描、统一 FSRS 调度、加强反馈和可视化、提升资源质量以及改善 UI/UX，可使系统更科学、更高效、更易用。

---

*本文档由多 Agent 协作团队根据 2.md 审计报告制定。各 Wave 详细实现方案请参考各 Agent 的设计输出。*
