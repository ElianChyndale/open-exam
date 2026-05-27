# CFA Tier 1 Vault

## 入口

- `00-CFA_L1_备考指南.md`：总备考思路、方法和学科体感
- `00-CFA_L1_Formula_Audit.md`：2026 考纲公式覆盖审计、缺失公式补全记录、超纲/扩展标记
- `.system/memory/strategy/cfa-2026-epub-textbook-index.md`：原版教材 `ePub` 章节总索引
- 各科唯一主框架：
  - [[00-Quantitative-Methods-MOC|Quantitative Methods]]
  - [[00-Ethical-and-Professional-Standards-MOC|Ethical and Professional Standards]]
  - [[00-Economics-MOC|Economics]]
  - [[00-Financial-Statement-Analysis-MOC|Financial Statement Analysis]]
  - [[00-Corporate-Issuers-MOC|Corporate Issuers]]
  - [[00-Equity-MOC|Equity Investments]]
  - [[00-Fixed-Income-MOC|Fixed Income]]
  - [[00-Derivatives-MOC|Derivatives]]
  - [[00-Alternative-Investments-MOC|Alternative Investments]]
  - [[00-Portfolio-Management-MOC|Portfolio Management]]
- `mock/`：按科目拆分的 mock 题目与练习入口
- `dashboard/`：系统自动生成的复盘与统计页面

## 官方来源链

当前知识库的推荐回看顺序：

1. 科目入口：`00-*-MOC.md`
2. 模块正文：`M01...Mxx...md`
3. 模块内 `Textbook Signal Topics`
4. 基础题入口：`dashboard/Subject-Question-Banks.md`
5. mock 入口：`mock/00-Mock-Source-Index.md`

如果同一知识点在多个地方出现，优先级固定为：

1. 原版教材 `ePub` 索引与教材正文
2. 科目 MOC
3. 模块正文笔记
4. 基础题 / mock 承接页
5. 备考经验性总结

## 如何使用这些知识框架

每科主框架现在按 2026 CFA Institute Learning Ecosystem 官方模块注册表组织：

1. `Official Module Table`
2. `Official Knowledge Tree`
3. 每个 `Mxx-*` 文件的官方页面目录
4. 可追溯的本地学习笔记迁移内容
5. 错题驱动的后续补强入口

建议用法：

- 第一次学：先看对应科目的 `00-*-MOC.md`
- 第二次学：只刷 `Official Knowledge Tree`
- 做题前：扫对应模块的 `Official Module Structure`
- 做题后：把错因写回 `.system/events/` 和 `.system/memory/`

## 使用约定

- 学习内容优先放在 `CFA_tier1/` 内对应主题目录
- 各科根目录只保留 2026 官方模块；旧拆分或自定义模块放在 `_legacy/`
- 自动生成页面只放在 `CFA_tier1/dashboard/`
- 原始证据与长期记忆仍以 `.system/events/` 和 `.system/memory/` 为准
