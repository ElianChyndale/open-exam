# OpenExam 生态系统审计报告

> 生成日期: 2026-06-01
> 范围: 全端（前端 8 页面 + API 47 端点 + study_science 10 引擎 + workflows + storage + CLI）

---

## 一、前端功能完整性（8/8 页面可访问，发现问题如下）

### ✅ 正常工作的页面

| 页面 | 路由 | 状态 | 说明 |
|------|------|------|------|
| 今日驾驶舱 | `/today` | ✅ | 侧边栏导航最前，QuickActions 全部可点击 |
| 题目录入 | `/capture` | ✅ | 表单完整，科目选择动态绑定 API |
| 错因诊断 | `/diagnosis` | ✅ | 错题列表 + AI 诊断 + 模式展示 |
| Daily Review | `/review` | ✅ | 完整的复习包渲染（知识点+错题+主动回忆） |
| 模拟中心 | `/mock` | ✅ | Mock 列表 + 创建 + Retro + Brief |
| 有效性仪表盘 | `/dashboard` | ✅ | 6 个指标卡片 + What-If 模拟 + 趋势图 |
| 机构控制台 | `/institution` | ✅ | 学习小组管理 + 风险报告 |
| 学习日历 | `/calendar` | ✅ | 热力图 + 考试倒计时 + 日期编辑 |

### 🔴 不可点击 / 功能缺失

| # | 位置 | 问题 | 影响 | 原因 |
|---|------|------|------|------|
| 1 | **侧边栏** | `/calendar` 页面无导航入口 | 用户无法从 UI 导航到日历页，只能直接输 URL | Sidebar.tsx 中写死了 7 个链接，calendar 不在其中 |
| 2 | **侧边栏** | `/api/profiles` 返回 404 | ProfileSwitcher 渲染不出列表 | 前端把 API_BASE 留空，通过 Next.js 代理 `/api/*`，但代理路由没配到 profiles 端点 |
| 3 | **今日驾驶舱** | `QuickAction` 使用 `<a>` 而非 `<Link>` | 每次点击触发全页刷新而非 CSR 跳转 | 使用了原生 HTML 标签 |
| 4 | **今日驾驶舱** | 能量录入 UI 不存在 | 用户无法在 UI 上录入精力数据 | `energyApi.checkIn` 在前端 import 了但从未调用 |
| 5 | **题目录入** | 语音输入按钮无声失败 | 不兼容语音 API 的浏览器上按钮无反馈 | `QuickCapture.tsx:61-68` 仅在 SpeechRecognition 可用时工作，无 fallback |
| 6 | **QuickCapture** | Cmd+Shift+E 快捷键盘无提示 | 用户永远不会发现这个快捷键 | layout.tsx 注册了 listener 但无 UI 提示 |
| 7 | **全部页面** | Service Worker 只缓存 3/8 页面 | 离线时 5 个页面不可用 | sw.js 仅预缓存 `/today /capture /review` |
| 8 | **Review 页** | 刷新按钮不刷新 API 数据 | 点击"刷新 Daily Review"调用了 `reviewApi.getToday()` 但 `useEffect` 依赖更新异常 | 可能缺少触发 re-fetch 的状态变量 |

---

## 二、API 端点完整性（47 端点，1 个崩溃）

### 测试结果

```
总计: 47 端点
  ✅ 200 OK: 45
  🔴 500 Internal Server Error: 1
  ✅ 422 正确拒绝: 1
```

### 🔴 Broken Endpoint

| 端点 | 方法 | 错误 | 根因 | 修复 |
|------|------|------|------|------|
| `/api/dashboard/knowledge-readiness` | GET | 500 — `NameError: name 'json' is not defined` | 新加的 `get_knowledge_readiness` 函数缺少 `import json` | ✅ 已修复：dashboard.py 模块级添加 `import json` |

### ⚠️ API 响应观察

| 端点 | 观察 | 建议 |
|------|------|------|
| `GET /api/dashboard/effectiveness` | `review_completion_rate` 使用 `days` 而非 `len(due_items)` 作为分母 | 需修复为 `completed_reviews / max(len(due_items), 1)` |
| `POST /api/attempts` | 返回的 `review_due_at` 总是 2 天后（Reviewed once 间隔） | 正常，KnowledgeMemoryEngine 与 SpacingScheduler 独立运作 |
| `GET /api/dashboard/knowledge-readiness` | 43 个知识点全部为 "Reviewed once" 或 "Proficient" | KnowledgeMemoryEngine 反馈循环正常工作 |

---

## 三、业务逻辑生态优化机会

### 3.1 ✅ 已完成生态闭环

```
记录错题 → MistakeCard(SpacingScheduler) → 到期复习 → complete_daily_review
 ↓                                                          ↓
 知识点状态升级 (Reviewed→Familiar→Practiced→Proficient)    KnowledgeMemoryEngine
 ↓                                                          ↓
 衰减扫描 (decay_sweep)                                   下次复习排期
 ↓                                                          ↓
 daily_review_pack 纳入到期知识点                          遗忘曲线干预
```

**新增组件**:
- `KnowledgeMemoryEngine` — 6 级渐进状态 + Ebbinghaus 遗忘曲线
- `collect_due_knowledge_points` — 到期知识点自动进 warm start
- `_feed_card_outcome_to_knowledge` — 卡片复习结果反馈到知识点
- `GET /api/dashboard/knowledge-readiness` — 知识状态 API

### 3.2 🔄 半完成生态组件

#### EnergyAwarePlanner
- ✅ 引擎完整（`energy_planner.py` — 10 种任务类型 × 5 级能量映射）
- ⚠️ 集成了一半：`study_plan_service.py` 调用了 EnergyAwarePlanner 但 `daily_review_pack` 不使用它
- ❌ 无前端 UI 录入能量（`energyApi.checkIn` 在 api.ts 但前端未调用）

**建议**: 在 `/today` 页面添加一个简单的能量滑动条（5 级），用户选择后传给 `/api/study-plan/today?energy_level=N`

#### InterleavingBuilder
- ✅ 引擎完整（`interleaving.py` — 4 种 bucket: weak/old_mistakes/adjacent/maintenance）
- ⚠️ `GET /api/study-plan/today` 返回的 `interleaving_composition` 显示所有任务都在 "weak" bucket
- ❌ `daily_review_pack` 不使用 InterleavingBuilder

**建议**: 将 InterleavingBuilder 集成到 warm start 生成流程中替换 token-overlap 匹配

### 3.3 🆕 高价值新生态机会

#### 长期学习者模型
当前系统"健忘"——每次 API 请求都从 JSONL 文件重新加载事件。建议：

1. **SQLite 只读查询缓存**：对高频查询（`load_events()` 每天被 `daily_review_pack` 调用 3 次）做 60 秒 TTL 缓存
2. **学习者特性档案**：统计学习者的稳定特征（"公式类题目总是粗心"、"校准能力在提升"）写入 JSON 供 pass predictor 使用
3. **能量模式分析**：汇总 energy check-in 数据识别用户的昼夜高效时段，自动安排高难度任务

#### 复习间隔进化
当前 SpacingScheduler 使用静态 `EXPANSION_FACTORS = [1.0, 2.0, 3.5, 5.0, 7.0]`。建议：

1. 根据历史 recall 成功率动态调整每个用户的 expansion 倍率
2. 对连续成功 3+ 次的知识点自动提升状态（已通过 KnowledgeMemoryEngine 实现）
3. 将考试成绩（mock/exam）作为 feedback signal 调整所有间隔参数

#### 知识点与错题卡的交叉学习
当前 `_feed_card_outcome_to_knowledge` 使用 `topic` + `los` 匹配，匹配较松散。建议：

1. 在 write_daily_review_snapshot 时显式建立 `knowledge_id → card_ids` 映射表
2. 在知识状态更新时参考关联卡片的历史 recall 记录
3. 在卡片下次复习时显示关联知识点的当前记忆状态

---

## 四、代码质量与架构问题

### 4.1 代码异味

| # | 位置 | 问题 | 建议 |
|---|------|------|------|
| 1 | `workflows.py` (9 处) | `source_layer == "question" and not e.is_correct` 重复 9 次 | 抽取为 `repo.load_incorrect_question_events()` |
| 2 | `study_plan.py` + `study_plan_service.py` | `_map_to_task_type` 与 `_map_error_to_task` 完全重复 | 合并在一个文件 |
| 3 | `workflows.py` (3 处) | 事件信封字段手动构造 3 次 | 推广 `_review_event()` 为公共工厂 |
| 4 | `dashboard.py` (6 处) | `repo.load_events()` 每次 API 请求都读文件 | 加 TTL 缓存 |
| 5 | `storage.py` | `_set_frontmatter_value` 用 regex 替代 YAML 库 | PyYAML 已是依赖，直接使用 |
| 6 | `workflows.py:1782-1793` | `daily_review_pack` 调用 `load_events()` 3 次 | 加载一次后传递引用 |
| 7 | `repository.py` | `load_events()` + `load_attempt_records()` 独立加载 | 提供 `load_unified_events()` 合并视图 |

### 4.2 🔴 已发现的 Bug（代码审计阶段）

| # | 严重度 | 位置 | 问题 | 状态 |
|---|--------|------|------|------|
| 1 | 🔴 高 | `workflows.py:1153` | `**payload` 覆盖事件信封字段 | 待修复 |
| 2 | 🔴 高 | `dashboard.py:68` | review completion 分母用天数而非待办数 | 待修复 |
| 3 | 🔴 高 | `requirements.txt` | 缺少 PyYAML 依赖（硬依赖） | 待修复 |
| 4 | 🟡 中 | `storage.py:21` | `_set_frontmatter_value` replace 在无换行的文件后失败 | 待修复 |
| 5 | 🟡 中 | `diagnosis.py:39` | attempt_id (attempt-xxx) 与 event_id (evt-xxx) 混用导致诊断失败 | 待修复 |
| 6 | 🟡 中 | `institution.py:74` | `learner_id in str(event_id)` 子串匹配导致误匹配 | 待修复 |
| 7 | 🟡 中 | `workflows.py:353` | `int(x or 50)` 吃掉显式 0 值 | 待修复 |
| 8 | 🟡 中 | `workflows.py:1864` | `complete_daily_review` overlay 覆盖丢弃额外字段 | 待修复 |
| 9 | 🟡 中 | `workflows.py:320` | `add_review_item` 无拷贝导致调用方数据被修改 | 待修复 |
| 10 | 🟡 中 | `sync_service.py:145` | `preview_import` 低估重复数 | 待修复 |
| 11 | 🟡 中 | `workflows.py:1572` | `_as_source_refs` 未处理 tuple | 待修复 |
| 12 | 🟡 中 | `workflows.py:1278` | `mark_card_reviewed` 返回类型由 Path 变为 dict | 待修复 |
| 13 | 🟢 低 | `card_printer.py:22` | `date.fromisoformat()` 无 try/except | 待修复 |
| 14 | 🟢 低 | `workflows.py:1120` | calibration warning 使用 timezone-naive 时间戳 | 待修复 |
| 15 | 🟢 低 | `storage.py:170` | `migrate_catalog` 无操作 | 待修复 |

---

## 五、生态系统状态总结

```
KnowledgeMemoryEngine      ✅ 已集成（6 级状态 + 衰减 + 反馈）
SpacingScheduler           ✅ 全部卡片排期用此引擎
RetrievalEngine            ✅ 主动回忆提示集成到 review 中
SelfExplanationPrompt      ✅ 每道错题附带自我解释提示
WorkedExampleFader         ✅ 高频错误触发渐进式引导
ConfidenceCalibration      ✅ 仪表盘校准 + 危险警告
EnergyAwarePlanner         ⚠️ 引擎完整 + study-plan 使用 + 无前端 UI
InterleavingBuilder        ⚠️ 引擎完整 + study-plan 使用 + 未用于 daily-review
PassPredictor              ✅ 仪表盘 + What-If 集成
Profile System             ✅ CFA L1 + FRM P1 + YAML 配置
```

## 六、推荐优先级

### P0（立即修复）
1. requirements.txt 添加 PyYAML — 当前 500 风险
2. dashboard.py `completion_rate` 分母修复 — pass predictor 数据错误
3. diagnosis.py attempt_id/event_id 混用 — 诊断功能完全失效

### P1（本周）
4. 侧边栏添加 /calendar 导航
5. 今日驾驶舱能量录入 UI
6. `daily_review_pack` 的 3 次 `load_events()` 合并为 1 次

### P2（本月）
7. InterleavingBuilder 集成到 daily review
8. `_set_frontmatter_value` 改用 PyYAML
9. 学习者长期特性档案
10. 离线缓存覆盖全部页面

### P3（季度）
11. 动态 expansion 因子（用户个性化）
12. Mock 考试成绩回馈到所有间隔参数
13. 知识点 × 错题卡交叉映射
