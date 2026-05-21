# MOC Auto-Patch Workflow

## 定位

本工作流在 `record-mistake` 完成后运行。当错题暴露出知识树（MOC）中的**主公式缺失**、**公式表变体缺失**、**概念树断层**或**考试陷阱缺口**时，先产出 taxonomy-aware 的 `moc-gap-review`，再由 Codex 按目标类型补全 MOC 的对应章节。

## 触发条件

每次用户输入错题后，当前 `record-mistake` → `mine-patterns` → `moc-gap-review` → `refresh-learning-outputs` 链之后，附加执行：

1. 检查 `moc-gap-review` 产出的 gap_type
2. 检查更细的 `gap_target`
3. 判断是补知识树、补公式表，还是两边都补
4. 对应更新 `00-*-MOC.md`

## Gap Target Taxonomy

`moc-gap-review` 当前使用以下 `gap_target`：

| gap_target | 含义 | 默认补丁动作 |
|------|------|------|
| `knowledge_tree_core_formula` | 该知识点的主公式没有进入知识树节点 | 补节点下的 `核心公式` |
| `formula_table_variant` | 主公式已在树里，但变形/换算公式缺在公式表 | 只补 `核心公式速查` |
| `both` | 主公式不在树里，公式表也没有足够支撑 | 同时补知识树节点和公式表 |
| `knowledge_tree_concept` | 主要缺口是概念结构、概念对比或知识树分支 | 补知识树分支 / 对比 / 注释 |
| `exam_trap` | 更像审题陷阱、口径提醒或高频误判 | 补“高频考试陷阱速查”或节点注意项 |

## 科目分流

不是所有科目都默认适合公式目标。

- `Quant / Fixed Income / Derivatives / Equity / FSA / Corporate Issuers / Portfolio Management / Economics / 部分 Alternative Investments` 可以走公式型 target
- `Ethical and Professional Standards` 属于 concept-first subject，即使错题被标成 `formula_misuse`，也不应自动落到公式补丁，而应回到 `knowledge_tree_concept`

## 判断规则

| 条件 | 动作 |
|------|------|
| `gap_target = knowledge_tree_core_formula` | 在对应知识点下新增 `核心公式` |
| `gap_target = formula_table_variant` | 只更新「核心公式速查」表 |
| `gap_target = both` | 同时补知识树节点和公式表 |
| `gap_target = knowledge_tree_concept` | 新增知识树分支、定义/直觉、概念对比 |
| `gap_target = exam_trap` | 更新「高频考试陷阱速查」或节点注意项 |

## 调用链

```text
用户输入错题
  └→ record-mistake (持久化事件+卡片)
       ├→ mine-patterns (模式检测)
       ├→ moc-gap-review (缺口审查)
       ├→ moc-auto-patch ← 本工作流 (更新 MOC 文件)
       └→ refresh-learning-outputs (刷新 Obsidian dashboard)
```

## 代理职责

| 角色 | 职责 |
|------|------|
| **Agent (Claude Code)** | 读取 `moc-gap-review` 产出 → 定位 MOC 中缺失位置 → 执行文案写入 |
| **cfa-question-captor (skill)** | 标准化错题结构 → 标记需要补 MOC 的字段（`moc_target` + `fix_rule` 含公式） |
| **cfa-review-synthesizer (skill)** | 在复盘产出中明确写出建议插入 MOC 的公式或对比项 |

## MOC 写入规范

1. **`knowledge_tree_core_formula`**：在对应知识树节点下补 `核心公式`，只写主公式，不堆所有变形
2. **`formula_table_variant`**：仅追加到「核心公式速查」对应模块的表格中，并维护 `知识树节点` 反向映射
3. **`both`**：先补知识树节点，再补公式表，保证树和表双向对齐
4. **`knowledge_tree_concept`**：追加知识树分支、定义/直觉、概念对比，必要时标注 `← 高频错因`
5. **`exam_trap`**：追加到「高频考试陷阱速查」表格，格式为 `错误理解 | 正确理解`
6. **跨模块关联**：如果涉及跨主题概念，在「跨模块关联」部分新增连线

## 禁止规则

- 不删除 MOC 现有内容
- 不修改非当前错题相关的 LOS 区域
- 不写入无法回追溯到事件的结论
- 不改动 MOC 的 YAML frontmatter
