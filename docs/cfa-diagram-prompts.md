# CFA 图示生成提示词

## 提示词 1：爬取工作流与技术架构图

将以下提示词输入到 **Mermaid Live Editor** (https://mermaid.live)、**draw.io** 或 **Whimsical** 生成架构流程图：

````markdown
请生成一张技术架构与数据工作流图，描述以下 CFA Institute 官网爬取过程：

**系统组件**
- 数据源: learn.cfainstitute.org (Canvas LMS + Azure AD B2C 认证)
- 认证层: Edge 浏览器 (CDP 远程调试端口 9222)，依赖 canvas_session cookie
- 爬取引擎: gstack browse (headless Chromium) + CDP WebSocket 连接
- 数据提取: 三种方法并行
  方法A: gstack browse goto+text (稳定但慢，~5s/页)
  方法B: Chrome DevTools Protocol Page.navigate (受 Canvas SSO 限制)
  方法C: 浏览器内同步 XMLHttpRequest 调用 Canvas REST API (最快，~0.3s/请求)
- API 端点: /api/v1/courses/{cid}/modules, /modules/{mid}/items, /pages/{url}?include[]=body
- 数据处理: Python (HTML→Markdown 转换, JSON→YAML frontmatter)
- 目标: Obsidian 知识库 (10 科目 MOC + 90 模块笔记)

**数据流阶段**
Phase 1: 认证 — Edge CDP 连接 → 提取 cookies → 注入 gstack browse session → 访问 Course Dashboard
Phase 2: 结构提取 — 发现 10 门主科课程 ID (1645-1654) → 获取模块列表 → 获取模块项目 → 获取页面内容
Phase 3: 转换 — HTML 清洗 → JSON 结构化 → Markdown 格式化 → YAML frontmatter
Phase 4: 同步 — MOC 对比更新 → 模块笔记标注 → 差距分析 → 完整大纲生成

**技术挑战**
- Canvas SSO 阻止跨课程 URL 导航
- Edge cookies 使用 v20 AES-GCM 加密
- 中国区 Windows 默认 GBK 编码
- Azure AD B2C 检测 headless 浏览器

**数据指标**
- 10 门课程, 90+ 模块, ~1200 页面项
- 生成 1 份完整课程大纲 Markdown (~22k chars)
- 更新 90 个 Obsidian 笔记的 YAML frontmatter

请用合适的颜色编码不同技术栈：蓝色为数据源，绿色为爬取引擎，橙色为数据处理，紫色为目标输出。使用 Mermaid 流程图或更美观的架构图风格。
````

---

## 提示词 2：CFA Level I 知识体系全景图

将以下提示词输入到 **Mermaid**、**Xmind**、**MindMaster** 或 **GoDiagram** 生成 CFA 一级知识地图：

````markdown
生成一张 CFA Level I 知识体系全景图（2026 年最新大纲），包含 10 个科目及其模块结构：

**图形要求**
- 中心：CFA Level I (2026)
- 10 个一级分支，按权重排列：
  1. Ethical & Professional Standards (15-20%) — 5 模块
  2. Financial Statement Analysis (13-17%) — 12 模块
  3. Portfolio Management (11-15%) — 6 模块
  4. Corporate Issuers (10-15%) — 7 模块
  5. Equity (10-15%) — 8 模块
  6. Fixed Income (10-15%) — 19 模块
  7. Alternative Investments (7-10%) — 7 模块
  8. Economics (6-10%) — 8 模块
  9. Quantitative Methods (6-9%) — 11 模块
  10. Derivatives (6-9%) — 10 模块

**每个科目分支下标注核心关键词：**

Quant: HPR/MWRR/TWRR | TVM | Statistics | Probability | Portfolio Math | Monte Carlo | CLT | Hypothesis Testing | Regression | Big Data/ML

Economics: Market Structures | Business Cycles | Fiscal/Monetary Policy | Geopolitics | Intl Trade | FX

Corporate: Org Forms | Stakeholders | Governance | Working Capital | Capital Budgeting | Capital Structure | Business Models

FSA: 3 Statements | Income Tax | Inventories | Long-term Assets | CF Analysis | Financial Modeling

Equity: Market Structure | Indices | EMH | Securities | Industry Analysis | Forecasting | DDM/Multiples

FI: Features | Cash Flows | Markets | Valuation | Yield | Duration/Convexity | Credit | Securitization | ABS/MBS

Derivatives: Forward/Futures/Swaps | Options | Put-Call Parity | Binomial | Cost of Carry

Alt: Private Capital | Real Estate | Infrastructure | Hedge Funds | Natural Resources | Digital Assets

PM: Efficient Frontier | CAPM | IPS | Asset Allocation | Behavioral | Risk Management

Ethics: Code & Standards I-VII | GIPS | Professionalism | Conflicts of Interest

**视觉建议**
- 使用不同颜色区分科目权重（权重越大颜色越深）
- 模块数量用节点大小表示
- 展示科目间的关联关系（如 Quant → Portfolio, FSA → Equity/FI）
- 适合打印或放入 A3 尺寸文档
````

---

## 如何使用这些提示词

| 目标 | 推荐工具 | 链接 |
|------|----------|------|
| 技术架构流程图 | Mermaid Live Editor | https://mermaid.live |
| 知识体系思维导图 | Xmind / MindMaster | 桌面软件 |
| 美观的技术架构图 | draw.io / Excalidraw | https://draw.io / https://excalidraw.com |
| 专业 Visio 风格 | GoDiagram / Diagrams.net | 桌面 + 网页 |
| AI 生成 | Claude + Mermaid 渲染 | 直接在对话中输出 Mermaid 代码 |
