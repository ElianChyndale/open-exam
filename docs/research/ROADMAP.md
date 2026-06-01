# OpenExam — 后续开发路线图

> 生成日期: 2026-06-01
> 基线: `pytest -q` 97 passed, TypeScript 编译通过
> 已完成 Bug 修复: 15/15, 代码异味: 7/7, Wave 0 内核加固: 11/11

---

## 执行证据

| 日期 | Gate | 证据 |
|------|------|------|
| 2026-06-02 | Foundation | 新增 `learning-records` 包、`EventEnvelopeV2`、集中式 feature flags；`pytest -q` 为 `99 passed`，`npm run typecheck` 与 `npm run build` 通过 |
| 2026-06-02 | Todo | JSONL reducer、快照、Markdown 投影、归档、CLI/API parity 与 `/today` 交互面板完成；`pytest -q` 为 `105 passed`，Web typecheck/build 通过，并经浏览器验证新增、deadline、完成与刷新持久化 |
| 2026-06-02 | Wave 1-6 local-first adapters | IndexedDB 队列、Todo 离线重试、provenance、consent、隐私导出/二次确认清除、xAPI、learner twin、psychometrics、structured tasks、pedagogy、grounded claims、Sync V2、只读 MCP、simulation/research 与 trust exports 基线完成；`pytest -q` 为 `110 passed`，Web typecheck/build 通过 |
| 2026-06-02 | LanguageOS basis | 从 `docs/superpowers/specs/languangePlan.md`、仓库模式与官方 GSAP React 文档冻结 LanguageOS 实现基线：`docs/superpowers/specs/2026-06-02-openexam-languageos-implementation-basis.md` |

---

## 一、已完成（参考基线）

### Bug 修复（15/15）
| # | 位置 | 问题 | 状态 |
|---|------|------|------|
| 1 | workflows.py | `**payload` 覆盖事件信封字段 | ✅ |
| 2 | dashboard.py | completion_rate 分母用天数→待办数 | ✅ |
| 3 | requirements.txt | 缺少 PyYAML 依赖 | ✅ |
| 4 | storage.py | frontmatter replace 无换行文件失败 | ✅ |
| 5 | diagnosis.py | attempt_id/event_id 混淆 | ✅ |
| 6 | institution.py | 子串匹配导致误匹配 | ✅ |
| 7 | workflows.py | `int(x or 50)` 吃掉 0 值 | ✅ |
| 8 | workflows.py | overlay 覆盖丢弃额外字段 | ✅ |
| 9 | workflows.py | add_review_item 无拷贝 | ✅ |
| 10 | sync_service.py | preview_import 未用 from_payload | ✅ |
| 11 | workflows.py | `_as_source_refs` 未处理 tuple | ✅ |
| 12 | workflows.py | 返回类型标注不一致 | ✅ |
| 13 | card_printer.py | date.fromisoformat 无保护 | ✅ |
| 14 | workflows.py | calibration 用 timezone-naive | ✅ |
| 15 | storage.py | migrate_catalog 无操作 | ✅ |

### Wave 0 内核加固（11/11）
| # | 项目 | 状态 |
|---|------|------|
| 0.1 | 归档报告到 docs/research/ | ✅ |
| 0.2 | 修复 sync preview ID 归一化 | ✅ |
| 0.3 | 引入重放检查（replay guard） | ✅ |
| 0.4 | 拆分 workflow 模块为包结构 | ✅ |
| 0.5 | Topic alias 分类系统接入 dashboard | ✅ |
| 0.6 | Pattern 严重度排序 | ✅ (已有) |
| 0.7 | Validation 过期/审查状态 | ✅ |
| 0.8 | MOC-gap 去重（event_ids） | ✅ |
| 0.9 | Mock 结果反馈到 SpacingScheduler | ✅ |
| 0.10 | Energy-aware daily review | ✅ |
| 0.11 | 替换脆弱 frontmatter 编辑（PyYAML） | ✅ |

### 其他已完成
| # | 项目 | 状态 |
|---|------|------|
| — | 动态 expansion 因子（校准个性化） | ✅ |
| — | Sleep/stress 字段加入能量录入 | ✅ |
| — | WCAG skip-to-content + aria-live | ✅ |
| — | 移动端 viewport meta | ✅ |
| — | JSONL 流幂等性键 | ✅ |
| — | 知识点闭环（KnowledgeMemoryEngine） | ✅ (已有) |
| — | 置信区间 confidence bands | ✅ (已有) |
| — | 确定性本地优先架构 | ✅ (已有) |

---

## 二、待实现功能

### Wave 1：学习记录网格、溯源与隐私
优先级: **中** | 依赖: 无 | 预估工作量: 大

| # | 项目 | 说明 | 优先级 |
|---|------|------|--------|
| 1.1 | `learning-records` 包 | 规范化 attempt/review/energy/mock/bias 流通过 EventEnvelopeV2 投射 | P1 |
| 1.2 | `provenance` 溯源包 | PROV-O 风格的实体/活动/代理模型，证据谱系追踪 | P1 |
| 1.3 | EventEnvelopeV2 | 新增 provenance/consent_scope 字段，向后兼容迁移 | P1 |
| 1.4 | `/api/provenance/{id}` | 证据溯源查询端点 | P2 |
| 1.5 | `/api/privacy/export` & `/api/privacy/purge` | 隐私数据导出和清除（含删除清单） | P1 |
| 1.6 | xAPI 导出 | Experience API 语句生成（`actor verb object` 格式） | P2 |
| 1.7 | Consent 事件机制 | 用户同意数据模型、事件类型、Provider-use 记录 | P1 |

**实现提示**:
- `EventEnvelopeV2` 可以直接在 `models.py` 新增 dataclass，保留 `MistakeEvent` 兼容
- provenance 可以复用现有的 `stable_id` + 新增 `ProvenanceRecord` 模型
- 隐私端点可以参考现有的 `/api/export` 模式

---

### Wave 2：学习者孪生、技能图谱与心理测量
优先级: **高** | 依赖: Wave 1 的数据规范化 | 预估工作量: 大

| # | 项目 | 说明 | 优先级 |
|---|------|------|--------|
| 2.1 | `learner-twin` 包 | 学习者的持久化特征模型：掌握度、半衰期、校准偏差、迁移分数 | P1 |
| 2.2 | `psychometrics` 包 | IRT 模型（Rasch 1PL → 2PL shadow），BKT/HLR 风格排期 | P1 |
| 2.3 | 半衰期掌握度估计 | 当前 KnowledgeMemoryEngine 有 6 级离散状态，需添加连续 recall probability | P1 |
| 2.4 | 信心偏差追踪 | 添加显式 `confidence_bias` 字段，记录系统性能偏差指标 | P2 |
| 2.5 | BKT/HLR 排期 | SpacingScheduler 当前用静态 EXPANSION_FACTORS，可添加贝叶斯变体 | P2 |
| 2.6 | Mock → 排期深度反馈 | 已实现基础反馈（0.9），可进一步结合 IRT 能力估计 | P3 |

**实现提示**:
- `learner-twin` 可以从 `exam_profile.py` 的 `ExamProfile` 模式扩展
- 半衰期估计可以添加 `HalfLifeEstimator` 类，使用 `scipy.optimize` 拟合
- BKT 可以用简单的 2 参数模型起步，不作贝叶斯推断

---

### Wave 3：教学策略、人因与无障碍
优先级: **中** | 依赖: 无 | 预估工作量: 中

| # | 项目 | 说明 | 优先级 |
|---|------|------|--------|
| 3.1 | `pedagogy-policy` 包 | 教学策略选择器：何种情景使用检索/自我解释/渐隐/对比对 | P1 |
| 3.2 | `human-factors` 包 | 认知负荷、疲劳模型、学习时段优化 | P2 |
| 3.3 | 结构化任务 + Markdown 投影 | ReviewPackResponse.items 当前硬编码 `[]`，需添加结构化任务类型 | P2 |
| 3.4 | 独立 contrast-pair 模块 | InterleavingBuilder 已有邻近映射，可提取为独立对比对生成器 | P3 |
| 3.5 | WCAG 2.2 AA 完整审计 | 已添加 skip-to-content + aria-live，剩余：颜色对比验证、heading 层级、焦点顺序 | P2 |
| 3.6 | 移动端适配完善 | 已添加 viewport meta，剩余：touch 事件、swipe 手势、底部导航触控优化 | P3 |

**实现提示**:
- `pedagogy-policy` 可以用决策表或简单的 if-else 规则引擎
- 结构化任务可以定义 `StructuredTask` dataclass，支持 completion_state、response、score

---

### Wave 4：接地 AI、多模态录入、Sync V2、MCP
优先级: **中** | 依赖: Wave 0 (已完成) | 预估工作量: 大

| # | 项目 | 说明 | 优先级 |
|---|------|------|--------|
| 4.1 | Grounded 解释服务 | RAG/引用级 AI 解释，claim-level evidence refs，工具调用记录 | P1 |
| 4.2 | Claim 级证据引用形式化 | `evidence_refs` 已存在，需形式化为 `EvidenceClaim` 模型 | P2 |
| 4.3 | AI 截图结构化提取 | 截图端点当前只保存图片，需调用视觉模型提取字段 | P2 |
| 4.4 | PDF/音频提取 | PDF 读取已存在（OCR），需添加音频→文字提取（Whisper 等） | P3 |
| 4.5 | IndexedDB 离线队列 | `offline.ts` 当前用 localStorage，需迁移到 IndexedDB 以支持大容量+游标 | P1 |
| 4.6 | MCP 适配器 | Model Context Protocol 只读适配器：到期复习查询、证据查找、溯源检查 | P2 |

**实现提示**:
- IndexedDB 迁移是前端 Max 优先级：localStorage 5MB 限制在大量错题数据下会满
- MCP 适配器可以参考 MCP 规范 https://modelcontextprotocol.io/specification/2025-11-25
- Grounded 解释可以复用现有的 agent-runtime 指令

---

### Wave 5：仿真与研究运行时
优先级: **低** | 依赖: Wave 2 | 预估工作量: 大

| # | 项目 | 说明 | 优先级 |
|---|------|------|--------|
| 5.1 | `sim-lab` 包 | 模拟学习者行为的沙箱环境 | P3 |
| 5.2 | `research-runtime` 包 | 离线 A/B 测试调度器变体，策略决策记录 | P3 |
| 5.3 | 调度器变体比较 | SpacingScheduler 当前单一算法，需支持多种策略离线对比 | P3 |

---

### Wave 6：生态系统与信任适配器
优先级: **低** | 依赖: Wave 1, 4 | 预估工作量: 大

| # | 项目 | 说明 | 优先级 |
|---|------|------|--------|
| 6.1 | Caliper 导出 | IMS Caliper 标准分析事件导出 | P3 |
| 6.2 | Open Badges 3.0 / CLR / VC | 可验证凭证导出（成就、能力） | P3 |
| 6.3 | 隐私保护 cohort 视图 | 差分隐私/匿名化聚合视图 | P3 |
| 6.4 | 签名证据快照 | 本地签名（GPG/Ed25519）的证据完整性快照 | P3 |

---

## 三、推荐启动顺序

```
高优先级 (P1) ─────────────────────────────────────────► 低优先级 (P3)
┌──────────────────────────────────────────────────────────┐
│  Wave 1: 隐私/溯源  ← 监管合规基础                        │
│  ├ 1.5 隐私导出/清除（最简 MVP：JSON + 删除确认）          │
│  ├ 1.3 EventEnvelopeV2（数据模型先行）                    │
│  └ 1.1 learning-records 包（规范化事件流）                 │
│                                                           │
│  Wave 4.5: IndexedDB  ← 离线体验基础                      │
│  └ 替换 offline.ts localStorage → IndexedDB              │
│                                                           │
│  Wave 2: 心理测量  ← 核心差异化竞争力                     │
│  ├ 2.1 learner-twin 包（先建模型壳）                      │
│  ├ 2.3 半衰期估计（提高遗忘预测精度）                      │
│  └ 2.2 psychometrics 包（IRT 起步）                      │
│                                                           │
│  Wave 3: 教学策略  ← 学习效果改善                         │
│  ├ 3.1 pedagogy-policy 包（规则引擎）                     │
│  ├ 3.3 结构化任务（推进前端交互）                          │
│  └ 3.5 WCAG 审计                                          │
│                                                           │
│  Wave 4: AI/多模态 ← 增强录入体验                         │
│  ├ 4.1 Grounded 解释                                      │
│  └ 4.6 MCP 适配器                                         │
│                                                           │
│  Wave 5 + 6: 仿真/信任适配器 ← 长期愿景                   │
│  └ 所有 P3 项目                                           │
└──────────────────────────────────────────────────────────┘
```

### 快速启动建议（< 1 天可实现）

| 项目 | 预估算量 | 关键文件 |
|------|----------|----------|
| IndexedDB 离线队列 | 4-6h | `apps/web/src/lib/offline.ts` |
| EventEnvelopeV2 数据模型 | 2-3h | `.system/app/models.py` |
| 隐私导出 MVP | 3-4h | `apps/api/routers/export.py` 扩展 |
| 半衰期估计原型 | 4-6h | `packages/study-science/src/` 新文件 |

---

## 四、技术债务 / 小优化

这些不是功能缺失，但值得在下一次改动时顺手修复：

| # | 位置 | 问题 | 建议 |
|---|------|------|------|
| S1 | `offline.ts` | localStorage → IndexedDB 迁移 | 参见 Wave 4.5 |
| S2 | `workflows/core.py` | 2535 行 → 可进一步提取为子系统模块 | 已创建包结构，`review.py`/`patterns.py`/`mock.py` 可逐个提取 |
| S3 | `pyproject.toml` | 检查依赖版本是否最新 | `pip list --outdated` |
| S4 | 测试覆盖率 | 目标 >80% | `pytest --cov=.system/` |
| S5 | TypeScript strict mode | 当前可能未启用 | `tsconfig.json` strict: true |

---

## 参考

- 审计报告: `docs/research/2026-06-01-audit-report.md`
- 升级计划: `docs/research/2026-06-01-upgrade-plan.md`
- 生态审计: `docs/ecosystem-audit-findings.md`
- 原始审计数据: `docs/research/audit-findings.json`
