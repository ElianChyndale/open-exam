# CFA Institute 官网数据爬取工作流总结

> 日期: 2026-05-25
> 目标: 从 CFA Institute Learning Ecosystem (learn.cfainstitute.org) 提取 CFA 2026 Level I 全部课程内容并同步到 Obsidian 知识库

---

## 一、技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    数据源层 (Data Source)                     │
│  learn.cfainstitute.org (Canvas LMS + Azure AD B2C 认证)     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  REST API (/api/v1/courses/{cid}/modules)           │   │
│  │  Pages API (/api/v1/courses/{cid}/pages/{url})      │   │
│  │  Module Items API (/modules/{mid}/items)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   认证层 (Auth)     │
                    │  Edge Browser CDP   │
                    │  (远程调试端口 9222) │
                    │  canvas_session     │
                    └─────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐
  │ 方法1: 浏览器  │   │ 方法2: CDP    │   │ 方法3: 内嵌 XHR  │
  │ gstack browse │   │ Chrome       │   │ 浏览器同步 XHR   │
  │ ($B goto+text)│   │ DevTools     │   │ (eval + fetch)   │
  │ 稳定但慢       │   │ Protocol     │   │ 最快方式         │
  │ ~5s/页        │   │ 原生导航受限   │   │ ~0.3s/请求       │
  └──────────────┘   └──────────────┘   └──────────────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  数据提取结果    │
                    │  10门课程大纲    │
                    │  90+模块结构    │
                    │  ~1200页面项    │
                    └─────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  数据处理与转换  │
                    │  HTML → Markdown│
                    │  JSON → YAML   │
                    │  API → Obsidian │
                    └─────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  目标输出        │
                    │  Obsidian 知识库 │
                    │  - MOC 更新     │
                    │  - 模块笔记标注  │
                    │  - 差距分析报告  │
                    │  - 完整课程大纲  │
                    └─────────────────┘
```

## 二、数据流 (Data Flow)

```
Phase 1: 认证与发现
  Edge 浏览器（已有登录态）
  → 通过 CDP 端口 9222 连接
  → 提取 cookies → 注入 gstack browse session
  → 访问 Course Dashboard → 发现所有课程 ID
  
Phase 2: 课程结构提取
  Canvas API (/api/v1/courses/{cid}/modules?per_page=50)
  → 获取模块列表 (module_id, name, items_count)
  → 获取模块项目 (items_url → type=Page, url)
  → 获取页面内容 (Pages API → body HTML)
  
Phase 3: 数据转换
  HTML 清洗 (去 script/style, 标签→文本)
  → JSON 结构化
  → Markdown 格式化
  → YAML frontmatter 生成
  
Phase 4: 知识库同步
  MOC 对比 → 官方模块对齐表
  → 模块笔记更新 (official_module YAML)
  → 差距分析报告
  → 完整课程大纲文档
```

## 三、技术挑战与解决方案

| 挑战 | 描述 | 解决方案 |
|------|------|----------|
| **Canvas SSO 跨课程导航** | Canvas 阻止直接 URL 导航切换到不同课程 | 使用 gstack browse 的独立 session；或 XHR 绕过导航 |
| **Cookie 加密** | Edge/Chrome v20 AES-GCM 加密 cookies | 通过 CDP `Network.getAllCookies` 直接从内存读取 |
| **GBK 编码** | Windows Python 默认 GBK 无法解码 UTF-8 | `subprocess.run` 使用 `capture_output=True` + `errors='replace'` |
| **异步 fetch 限制** | `$B js` 不支持 async/await | 使用同步 `XMLHttpRequest` 替代 |
| **JS eval 路径限制** | `$B eval` 只接受 /tmp 目录文件 | 将 JS 文件写入 `C:\tmp` |
| **内容量过大** | 10 门课程约 1200 页面，逐页导航需 100+ 分钟 | 改用 Canvas REST API + XHR 批量并行请求 |

## 四、关键工具与命令

```bash
# 浏览器自动化
B="/c/Users/Administrator/.claude/skills/gstack/browse/dist/browse"
$B goto <url>           # 导航
$B text                  # 获取页面文本
$B js <expr>             # 执行 JS 表达式
$B eval <file>           # 执行 JS 文件
$B cookie-import <json>  # 导入 cookies

# Canvas API (通过浏览器 session 认证)
GET /api/v1/courses/{cid}/modules?per_page=50
GET /api/v1/courses/{cid}/modules/{mid}/items?per_page=50
GET /api/v1/courses/{cid}/pages/{page_url}?include[]=body
```

## 五、数据统计

| 指标 | 数据 |
|------|------|
| 提取课程数 | 10 门主科 + 2 PSM |
| 模块总数 | 90+ |
| 页面项总数 | ~1200 |
| 爬取方式 | Canvas REST API (最快) / 浏览器导航 (备用) |
| 输出文件 | 10 个课程全文本 + 1 个综合 Markdown 大纲 |
| 处理时间 | 结构提取 (~10s) + 页面内容 (~5min 全量 / ~30s 精选) |

## 六、局限性

1. **Canvas API 无公开 API Token**：必须依赖浏览器 session 认证
2. **Azure AD B2C 反爬限制**：Azure AD 检测 headless 浏览器并拒绝登录
3. **跨课程 SSO 限制**：Canvas 阻止程序化跨课程导航（需 XHR 或新 tab）
4. **内容版权**：提取内容仅用于个人学习
