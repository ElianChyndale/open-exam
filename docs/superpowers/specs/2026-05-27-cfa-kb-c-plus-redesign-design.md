# CFA Knowledge Base C+ Redesign Design

Date: 2026-05-27
Status: approved blueprint, pending implementation plan
Scope: active CFA Level I knowledge base only

## 1. Goal

把现有 CFA Level I 知识库从“模块笔记 + 后置补强表格”升级为教材驱动的完整学习系统。

最终页面应满足：

- 原版教材结构进入正文，而不是孤立地插入锚点表格。
- 每个知识点都出现在它该讲的位置，按教材逻辑展开，再转成考试动作。
- 保留中英双语表达：中文用于理解和判断，English terms 用于识题、公式、LOS 和官方概念。
- MOC 是科目作战地图，其中最重要的部分是 `Formula & Framework Map`。
- Module 是完整学习章节，能够独立支持首轮学习、刷题补洞、mock 前复盘和错题回炉。
- 不修改 `_legacy/`、`_archive/` 等旧版文件。

## 2. Source Priority

本次重构遵守仓库的 Source of Truth 顺序：

1. `.system/events/` and `.system/events/catalog.sqlite3`
2. `.system/memory/`
3. `.system/app/`
4. `skills/`
5. `CFA_tier1/`

教材索引和教材内容作为知识库补强来源，落在 `.system/memory/strategy/` 作为长期证据资产；`CFA_tier1/` 是投影层，不应成为唯一真相。

## 3. Design Principles

### 3.1 Curriculum First

原版教材 chapter sections 是模块正文的主骨架。

当前的 `Textbook Signal Topics`、`教材驱动补强`、`教材驱动解题动作`、`教材驱动易错清单` 不应作为独立尾部补丁长期存在。它们的内容应被拆解并融入对应教材小节的正文知识块中。

### 3.2 Exam Translation Second

每个教材小节必须被翻译成考试语言：

- 题干触发词 / question triggers
- LOS 动词对应动作
- 公式选择规则 / formula selection rule
- 判断路径 / decision framework
- 常见陷阱 / trap check
- 输出格式 / answer output

### 3.3 Evidence Anchored

基础题、mock、错题和复盘反思不能漂浮在独立列表中。

它们应回填到对应知识点：

- Practice evidence: 基础题如何考这个点
- Mock evidence: 模拟题如何组合或变形这个点
- Mistake evidence: 用户错题暴露的误区
- Fix rule: 下一次如何避免
- Next drill: 下一步练什么

### 3.4 Bilingual By Design

页面语言结构固定为：

- 中文解释优先，用于讲清概念、因果、限制条件和做题动作。
- English terms 必须保留在概念、公式、LOS、题干触发词和官方名词中。
- 不把双语变成重复翻译；英文承担精确索引功能，中文承担理解功能。

## 4. MOC C+ Structure

MOC 的定位是科目作战地图。它不应承担大段正文讲解，也不应只是模块目录。

MOC 的最高优先级是 `Formula & Framework Map`。模块导航、教材主线和题库入口都服务于这一张地图：学习者打开 MOC 时，应该能快速知道本科目有哪些公式、框架、判断模型，它们分别在哪个模块、什么时候用、什么时候不能用。

### 4.1 Required MOC Sections

每个现役 `00-*-MOC.md` 应采用以下结构：

```text
# <Subject> MOC

## 1. Subject Brief 科目定位
## 2. Formula & Framework Map 公式与框架地图
## 3. Module Atlas 模块地图
## 4. Curriculum Spine 教材主线
## 5. Exam Routes 做题路线
## 6. Practice & Mock Evidence Map 题库证据地图
## 7. Review Routes 复习路线
## 8. Cross-Subject Interfaces 跨科目接口
```

### 4.2 Formula & Framework Map Requirements

`Formula & Framework Map` 是 MOC 最重要的部分，必须比其他导航段更完整。

它至少包含：

| Field | Purpose |
|---|---|
| Formula / Framework | 公式、模型、判断框架或流程 |
| Module | 对应模块 |
| Knowledge Node | 对应知识树节点或教材小节 |
| Use When | 题干满足什么条件时使用 |
| Do Not Use When | 什么条件下不能用或要换口径 |
| Inputs | 变量、单位、现金流方向、会计口径或统计假设 |
| Output | 计算结果或判断结论 |
| Trap Check | 最容易错的口径、顺序或解释 |
| Links | Module、Practice、Mock、mistake card 或 dashboard |

### 4.3 MOC Module Atlas

`Module Atlas` 以模块为单位，但每行必须服务于公式与框架地图：

- Module number
- Official module name
- Textbook chapter
- Core task
- Main formulas / frameworks
- High-frequency question types
- Practice page link
- Mock page link
- Module note link

### 4.4 MOC Curriculum Spine

`Curriculum Spine` 不是教材锚点表，而是科目级学习主线。

例如 Quant 可分成：

- return and discount-rate layer
- probability and portfolio mathematics layer
- sampling and inference layer
- regression and model-risk layer

每一层说明：

- 包含哪些模块
- 对应教材主线
- 主要公式/框架
- 与其他科目的接口

## 5. Module C+ Structure

Module 的定位是完整学习章节。它可以更长，但必须更有秩序。

### 5.1 Required Module Sections

每个现役 `Mxx-*.md` 应采用以下结构：

```text
# Mxx: <Module Name>

## 0. Reading Contract 学习契约
## 1. Module Brief 模块定位
## 2. Curriculum Spine 教材正文主线
## 3. Exam Translation 考试翻译
## 4. Formula & Decision Bench 公式与决策台
## 5. Practice & Mock Evidence 题库证据
## 6. Trap Ledger 陷阱账本
## 7. Final Recall Sheet 最后回忆页
```

### 5.2 Knowledge Block Template

`## 2. Curriculum Spine` 下的每个教材小节应生成一个知识块。

每个知识块使用以下结构：

```text
### <Textbook Section Number> <English Section Title> / <中文标题>

**Textbook Position**:
**Core Meaning 中文解释**:
**English Terms**:
**Why It Matters**:
**Formula / Rule**:
**Exam Translation**:
**Question Triggers**:
**Practice / Mock Evidence**:
**Trap & Fix Rule**:
```

说明：

- `Textbook Position` 保留原版教材小节位置。
- `Core Meaning 中文解释` 是正文主体，不能只是标题解释。
- `English Terms` 保留官方概念，不做过度翻译。
- `Formula / Rule` 包含使用条件和变量口径。
- `Exam Translation` 把教材内容转成做题动作。
- `Practice / Mock Evidence` 回填基础题和 mock 的考法。
- `Trap & Fix Rule` 连接错题复盘语言。

### 5.3 Formula & Decision Bench

Module 内的公式区不是公式堆表，而是本模块的决策台。

每个公式或框架必须说明：

- 变量定义
- 输入口径
- 题干触发条件
- 禁用条件
- 计算顺序
- 解释结果的句式
- 常见错误

### 5.4 Practice & Mock Evidence

题库证据必须按知识块归属。

允许的形式：

```text
### Evidence: <Knowledge Block>

- Practice: Qxx-Qyy
  - Tested idea:
  - Stem pattern:
  - Detail to remember:
- Mock: Mock <source> Qxx
  - Tested idea:
  - Stem pattern:
  - Trap:
```

如果题目还不能高置信归类，保留在 unclassified mock 中，不强行写入模块。

## 6. Migration Strategy

### 6.1 Phase 1: Prototype

先重构：

- `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`
- `CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md`

目标：

- 验证 MOC 的 `Formula & Framework Map` 是否足够好用。
- 验证 Module 的教材正文主线是否自然、双语是否清楚、题库证据是否放对位置。
- 清理上一轮机械补强段落在样板页中的痕迹。

### 6.2 Phase 2: Subject Expansion

确认样板后，按科目扩展：

1. Quantitative Methods
2. Financial Statement Analysis
3. Fixed Income
4. Equity
5. Economics
6. Corporate Issuers
7. Derivatives
8. Portfolio Management
9. Alternative Investments
10. Ethical and Professional Standards

优先顺序依据：

- 公式与框架密度
- mock 和基础题对该科目的覆盖程度
- 知识点之间的跨科目依赖

### 6.3 Phase 3: Full Audit

完成后执行覆盖审计：

- 现役 MOC 是否都包含 `Formula & Framework Map`
- 现役 Module 是否都包含 C+ required sections
- 是否仍存在机械的“教材驱动补强表格”
- 是否修改了 `_legacy/` 或 `_archive/`
- ePub 教材小节是否能在模块正文中找到对应知识块
- Practice/mock 是否至少能链接到科目和模块
- 中英双语是否保留

## 7. Constraints

- 不修改 `_legacy/`、`_archive/`。
- 不把教材全文复制进笔记；只抽取结构、概念、公式、判断规则和考试相关表达。
- 不凭空生成来源不明的结论；教材来源、题库来源、错题来源必须能回溯。
- 不自动把 pattern mining 结果直接写入 MOC；错题模式仍需经过 review/gap 判断。
- 不牺牲中英双语风格。

## 8. Acceptance Criteria

### MOC Acceptance

- 每个现役 MOC 都有完整 `Formula & Framework Map`。
- MOC 打开后可以直接回答：
  - 本科目有哪些关键公式和框架？
  - 每个公式什么时候用？
  - 什么时候不能用？
  - 对应哪个模块和教材小节？
  - 有哪些题库/mock证据？

### Module Acceptance

- 每个现役 Module 都按教材小节形成正文知识块。
- 每个知识块都有中文解释和 English terms。
- 每个知识块都能转成考试动作。
- 公式区包含变量口径、使用条件和禁用条件。
- 基础题和 mock 证据不再漂浮，尽量回填到对应知识块。
- 机械补强表格被移除或重排进正文。

### Quality Acceptance

- 不触碰旧版文件。
- 不破坏已有 frontmatter。
- 不覆盖用户手工修改。
- 能通过脚本审计现役文件覆盖率。
- 样板页经用户确认后再批量扩散。

## 9. Open Decision

样板阶段默认选择 Quant MOC + Quant M01。

如果用户希望先验证其他科目，可以改为：

- FSA M02, because it has strong textbook section structure and reporting traps.
- Fixed Income M06, because it stresses formula/framework map quality.
- Ethics M03, because it tests whether non-formula modules can still use a framework-first MOC.

当前推荐仍是 Quant MOC + Quant M01，因为它最能验证 `Formula & Framework Map` 的核心质量。
