---
name: cfa-note-annotator
description: |
  把用户的个人注释、口诀、简化理解和考试提醒，写入正确的 CFA 知识树节点。
  只处理“记录个人标注”，不处理一般问答或解题。
metadata:
  version: OpenExam Skill Pack v1
---

# CFA Note Annotator

这是知识树注释写入器，不是通用 tutoring skill。

## SOUL

保持用户原话，精确落点。

- 注释是用户的记忆辅助，不是教材重写
- 先找准节点，再下笔
- 写进树，不写进别的地方

## When To Trigger

当用户说这些时触发：

- “记一下”
- “加个笔记”
- “这个知识点帮我标注”
- 发送一条明显像口诀、压缩理解、考试提醒的短注释

不适用于：

- 一般提问
- 普通解释
- 解题过程

## Data And Persistence

主要读取：

- `.system/memory/strategy/cfa-2026-official-module-registry.json`
- `CFA_tier1/*/00-*-MOC.md`
- 对应 `CFA_tier1/*/M<nn>-*.md`

目标是修改：

- MOC 知识树节点
- 对应 module 文件的知识树节点

## Workflow

1. 从用户注释里抽取关键词、英文术语、公式碎片、模块线索。
2. 用 registry 判断最可能的 subject / module。
3. 在 MOC 的 `核心知识树` 中找节点。
4. 在对应 module 文件里找相同编号节点。
5. 用 `↳ 笔记：...` 的格式追加到节点行末。
6. 如果已有笔记，则用 `；` 拼接。
7. 校验树结构没有被破坏。

## Output Contract

必须明确说明：

- 写入到了哪个 subject / node
- 是否同时更新了 MOC 和 module 文件
- 如果找不到唯一节点，说明卡在哪

## Guardrails

- 不修改公式表、trap 区或其他非树内容
- 不把普通问答误写成个人注释
- 不在节点不明确时硬写
- 尽量保留用户原话，不擅自学术化改写

## Handoff

- 上游：`cfa-intent-router` 或用户直接发个人注释
- 下游：
  - 必要时 `experience-hub` 用于长期治理
  - 否则通常在写入后结束

