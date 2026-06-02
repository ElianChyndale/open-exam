# OpenExam EXAMOS 全维度审计总报告

> **日期:** 2026-06-02  
> **审计维度:** 算法/数据科学 · 架构/代码质量 · UX/设计 · 产品完整度 · CFA 备考适配  
> **审计团队:** 5 位独立审计官  
> **审计范围:** 683 源文件, 18,500+ Python 行, 4,500+ TS 行, 187 测试用例

---

## 一、总体评分

| 维度 | 评分 | 核心结论 |
|------|------|---------|
| 🧮 **算法与数据科学** | 6/10 | 2 个 FAIL（Pedagogy、Distractor 为存根），6 个 WARN，核心遗忘曲线模型需替换 |
| 🏗️ **架构与代码质量** | 6.5/10 | 1 CRITICAL（模块覆盖），5 HIGH（2650 行单文件、路径遍历等），41 总问题 |
| 🎨 **UX 与视觉设计** | 6.4/10 | 15 页面均分；视觉系统扎实，信息架构不成熟，双语混用，新用户无引导 |
| 📊 **产品完整度** | 7/10 | 前端 100% 完成 PLAN.md 页面，API 47 端点全部就绪；但核心学习闭环 3 处中断 |
| 📘 **CFA 备考适配** | 4.5/10 | 错误诊断和间隔重复架构领先，但零内置题库、无法实际模考、干扰项分析为存根 |

---

## 二、最高优先级问题（Critical + High）

### 🔴 CRITICAL（4 项）

| # | 问题 | 维度 | 文件位置 | 影响 |
|---|------|------|---------|------|
| C1 | **PedagogyPolicy 完全非功能** — 4 分支 if-else，无状态、无学习、无法使用 | 算法 | `study_science/pedagogy.py` | 自适应教学系统不存在，"contrast_pair" 策略从未实现 |
| C2 | **DistractorAnalyzer 为存根** — `classify_distractor()` 始终返回 `"concept_pair"` 忽略所有输入 | 算法 | `study_science/distractor.py:22-25` | 干扰项分析系统完全失效 |
| C3 | **workflows/core.py 2650 行单文件** — 包含 ~45 个函数，严重违反单一职责 | 架构 | `.system/app/workflows/core.py` | 代码难以维护，模块边界混乱 |
| C4 | **write_todo 函数静默覆盖** — wildcard import 导致 todo.py 隐式覆盖 core.py | 架构 | `.system/app/workflows/__init__.py:5-13` | 同一函数名不同实现，行为不可预测 |

### 🟠 HIGH（12 项）

| # | 问题 | 维度 | 位置 |
|---|------|------|------|
| H1 | **截图 AI 提取未实现** — 保存图片但不做结构化提取 | 产品 | `apps/api/routers/attempts.py` |
| H2 | **Daily Review 未集成 EnergyAwarePlanner** — 复习忽略精力状态 | 产品 | `workflows/core.py` |
| H3 | **模考复盘未反馈到 SpacingScheduler** — 模考成绩不影响复习间隔 | 产品 | `mock.py`, `spacing.py` |
| H4 | **诊断未反馈到 KnowledgeMemoryEngine** — 两个系统独立运行 | 产品 | `diagnosis_service.py` |
| H5 | **截图文件名未做路径遍历防护** — 恶意文件名可导致目录穿越 | 架构 | `apps/api/routers/attempts.py:72` |
| H6 | **SpacingScheduler 使用查表法而非遗忘曲线** — 无 R=2^(-t/H) | 算法 | `study_science/spacing.py` |
| H7 | **DifficultyAnalyzer 贝叶斯修正数学错误** — Beta-Bernoulli 实现有误 | 算法 | `language_science/difficulty.py` |
| H8 | **ExtractionEngine 置信度公式不合理** — 0.3+freq*0.02 无归一化 | 算法 | `language_science/extraction.py` |
| H9 | **CFA Workflows 考试权重污染难度空间** — 权重应用于 difficulty 而非 priority | 算法 | `cfa_workflows.py` |
| H10 | **两套间隔系统并行** — MistakeCard 用 SpacingScheduler，CFA 卡用 FSRS6，可导致内存状态分裂 | 算法 | `spacing.py` vs `scheduler.py` |
| H11 | **零内置题库** — 用户无法做任何练习，所有内容需自带 | 产品/CFA | 系统级 |
| H12 | **Resource Center 信息架构灾难** — 7 个数据节 + 6 个 List 压缩到单页 | UX | `resources/page.tsx:157-248` |

---

## 三、跨维度交叉发现

### 3.1 核心学习环中断（3 个断点）

```
用户刷题 → 诊断分析 → 间隔复习 → 学习仪表板
  ↑                      ↓
  └──── KnowledgeMemoryEngine ────┘
         ↑                        ↑
        诊断结果不写入 KMS   复习不调用 EnergyAwarePlanner
        模考结果不反馈到 Spacing
```

**影响**：系统承诺的"诊断→复习→掌握"闭环在 3 个关键节点断裂，学习的证据链不完整。

### 3.2 算法潜力和实现缺口

| 5 个审计官一致认同 | 细节 |
|-------------------|------|
| ✅ **错误诊断分类法** 业界领先 | 8 类错因 + 模式检测，无竞品做到 |
| ✅ **Knowledge Memory Engine** 独特且有深度 | 6 状态 + Ebbinghaus 衰减，但未完全集成 |
| ✅ **FSRS-6 + 交错练习** 组合有竞争力 | 但 CFA 端和新卡片端用不同间隔系统 |
| ✅ **通过概率预测** 独特价值 | What-if 仿真仪表板中已实现 |
| ❌ **零题库 = 系统性缺陷** | 所有竞品（UWorld/CFAI/Kaplan）都有数千道题 |
| ❌ **教学法引擎未实现** | PedagogyPolicy 和 DistractorAnalyzer 都是存根 |
| ❌ **IRT/BKT 死代码** | psychometrics.py 中的 IRT 和 BKT 从未被调用 |

### 3.3 UX 体验分层

| 层 | 评分 | 表现 |
|----|------|------|
| LanguageOS | 8/10 | 最成熟，有引导流程、一致英文设计语言、GSAP 动效 |
| CFA 驾驶舱 | 6.5/10 | 功能完整，双语混用，无新用户引导 |
| Resource Center | 4/10 | 暴露所有内部技术概念，无抽象层 |

**核心矛盾**：视觉系统（Glassmorphism 设计语言、暗色模式、GSAP 动效）是 **7/10** 水平，但信息架构和交互细节是 **5/10**。视觉 > 交互的落差给用户"看起来很高级但用起来别扭"的感受。

---

## 四、行动路线图

### 立即行动（P0，1-2 天）

| 优先级 | 操作 | 维度 | 影响 |
|--------|------|------|------|
| P0 | 🔧 修复 `workflows/__init__.py` wildcard import + `write_todo` 覆盖 | 架构 | 消除模块隐式覆盖风险 |
| P0 | 🔧 截图上传路径遍历防护 | 安全 | 消除安全隐患 |
| P0 | 🔧 替换 `classify_distractor()` 存根 | 算法 | 恢复干扰项分析功能 |

### 高优先级（P1，本周内）

| 优先级 | 操作 | 维度 | 预计工期 |
|--------|------|------|---------|
| P1 | 🔧 连接 Diagnosis → KnowledgeMemoryEngine | 产品 | 2 天 |
| P1 | 🔧 连接 EnergyAwarePlanner → Daily Review | 产品 | 1 天 |
| P1 | 🔧 连接 Mock Retro → SpacingScheduler | 产品 | 1 天 |
| P1 | 🔧 统一双语 UI 为中文 | UX | 2 天 |
| P1 | 🔧 Resource Center 信息架构重设计（分 tab） | UX | 2 天 |
| P1 | 🔧 替换 SpacingScheduler 查表法为指数遗忘模型 | 算法 | 2 天 |
| P1 | 🔧 合并两套间隔系统（MistakeCard + CFACard 共用 FSRS6） | 算法 | 2 天 |
| P1 | 🔧 添加骨架屏加载状态到所有页面 | UX | 1 天 |

### 中期（P2，未来 2 周）

| 优先级 | 操作 | 维度 |
|--------|------|------|
| P2 | 🔧 分割 `workflows/core.py` 2650 行为领域模块 | 架构 |
| P2 | 🔧 实现 CFA 题库集成（模板化生成 + 用户导入） | CFA |
| P2 | 🔧 实现全真模考（计时器 + 题目选择 + 自动评分） | CFA |
| P2 | 🔧 实现 IRT/BKT 参数拟合（从死代码到产品化） | 算法 |
| P2 | 🔧 实现 PedagogyPolicy 完整版（Bayesian Knowledge Tracing 驱动） | 算法 |
| P2 | 🔧 添加新用户引导流程到 CFA 驾驶舱 | UX |
| P2 | 🔧 实现 Markdown 渲染器升级（`react-markdown`） | UX |

### 长期（P3，未来 1 个月）

| 优先级 | 操作 | 维度 |
|--------|------|------|
| P3 | 🏗️ 迁移所有事件到 EventEnvelopeV2 统一格式 | 架构 |
| P3 | 🏗️ `load_jsonl_events` 添加分页和流式读取 | 架构 |
| P3 | 🎨 直觉图改为真实节点-连接图（vis-network） | UX |
| P3 | 🎨 复习页面添加键盘快捷键（1-2-3-4 评分） | UX |
| P3 | 📘 构建 CFA 公式检索系统 | CFA |
| P3 | 📘 实现伦理准则专项工作流 | CFA |

---

## 五、竞品定位总结

**EXAMOS 的不可替代优势**（无竞品做到）：
- 错误诊断 8 分类法 + 模式检测
- 7 认知科学引擎协同工作
- Energy-Aware 精力感知规划
- 通过概率预测 + What-if 仿真
- 机构班级风险预警

**必须补齐的生死项**（否则无法独立竞争）：
- 零题库 → 至少题库模板/导入机制
- 无全真模考 → 90 题限时 + 计时器 + 评分
- 双语混用 → 统一语言策略
- 新用户零引导 → 移植 LanguageOS 的 GuidedOnboarding

**总体建议定位**：不做课程平台，不做泛题库；做 **"让所有 QBank 变聪明的认知层"** — 用户用 UWorld/CFAI/Kaplan 刷题，EXAMOS 做诊断 → 间隔 → 预测。但前提是先把核心闭环接通。

---

## 六、审计数据汇总

| 指标 | 值 |
|------|-----|
| 审计源文件数 | 80+（20 + 20 + 40 + 30 + 30 每 agent） |
| 发现问题总数 | 77+（20 算法 + 41 架构 + 12 UX + 12 产品 + 多 CFA） |
| CRITICAL | 4 |
| HIGH | 12 |
| MEDIUM | 30+ |
| LOW | 20+ |
| 已有测试覆盖 | 187 全通过（但缺 API 集成测试和属性测试） |
| 产出的改进路线图项 | 22 项（P0:3 + P1:8 + P2:7 + P3:4） |
