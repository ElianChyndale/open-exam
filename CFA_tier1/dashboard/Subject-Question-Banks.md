---
title: "CFA L1 Subject Question Banks"
description: 各科目练习题库索引，来源于 CFA Institute Practice Tool
generated: 2026-05-25
source: cfa-practi-pdx-prod.insproserv.net
---

# CFA L1 Subject Question Banks

> 本文件汇总各科目 Practice 工具中可用题目数量及记录链接。
> 使用 Edge 浏览器登录 [Practice Tool](https://learn.cfainstitute.org/accounts/1/external_tools/261) 可直接练习。

## 题目数量概览

| 科目 | 模块数 | 总题数 | 题库文件 |
|------|--------|--------|----------|
| 📊 Quantitative Methods | 11 | ~212 | [[00-Quant-Practice-Questions]] |
| 🏛️ Economics | 8 | TBD | 待创建 |
| 🏢 Corporate Issuers | 7 | TBD | 待创建 |
| 📋 Financial Statement Analysis | 12 | TBD | 待创建 |
| 📈 Equity | 8 | TBD | 待创建 |
| 💰 Fixed Income | 19 | TBD | 待创建 |
| 🔀 Derivatives | 10 | TBD | 待创建 |
| 🏠 Alternative Investments | 7 | TBD | 待创建 |
| 📊 Portfolio Management | 6 | TBD | 待创建 |
| ⚖️ Ethics | 5 | TBD | 待创建 |

## 如何使用 Edge 提取更多题目

1. 确保 Edge 浏览器已登录 CFA Institute (learn.cfainstitute.org)
2. 导航到 Practice 工具 (全局导航 → Practice)
3. 选择科目 → 选择模块 → 点击 `Take`
4. 题目加载后，运行以下 CDP 命令提取：

```python
# 通过 Edge CDP 提取当前页面题目
python -c "
import json, requests, websocket
pages = requests.get('http://127.0.0.1:9222/json').json()
target = [p for p in pages if 'panda_token' in p['url']][0]
ws = websocket.create_connection(target['webSocketDebuggerUrl'], timeout=15)
# ... 提取逻辑
ws.close()
"
```

## 题目记录模板

每个模块使用以下格式记录题目：

```markdown
### Q[N]: [题目简述]
**知识点**: [相关知识点]
**题型**: Multiple Choice

**题干**:
...

**选项**:
A. ...
B. ...
C. ...

**答案**: [A/B/C]
**解析**: ...
```
