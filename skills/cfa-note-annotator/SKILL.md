---
name: cfa-note-annotator
description: Add personal simplified annotations (笔记/记忆口诀/简化标注) to CFA knowledge tree nodes in MOC and module files across all 10 subjects. Trigger when the user shares exam tips, memory aids, simplified formulas, or annotated knowledge points — especially phrases like "记一下", "笔记", "标注", "记住", or brief concept summaries in Chinese. Also trigger when the user sends compressed knowledge like "X离X̄越远，区间越宽" that looks like a personal note rather than a question. Do NOT trigger for general study questions, explanations, or problem-solving — only for recording personal annotations into the knowledge base.
---

# CFA Note Annotator

Record the user's personal simplified annotations (笔记/简化标注) into the CFA knowledge base at the correct knowledge tree nodes in both the MOC and the module file.

## When this skill should trigger

Invoke this skill whenever the user sends a message that is primarily a **personal note, memory aid, or annotation** about a CFA concept — especially:

- "记一下：..." / "笔记：..." / "标注：..."
- A compressed formula note like "X离X̄越远，区间越宽；SEE越大，区间越宽"
- An exam tip or personal insight phrased as a note to self
- Clarification that "这个知识点" should be recorded

**Do NOT trigger** when the user is asking a question, requesting an explanation, or solving a problem — those are routed through `cfa-intent-router` instead.

## Workflow

### Step 1: Identify the matching knowledge tree node

1. **Parse keywords** from the user's note — extract:
   - English terms (e.g., "prediction interval", "callable bond", "gross profit margin")
   - Chinese terms (e.g., "预测区间", "久期", "毛利率")
   - Formula fragments (e.g., "SEE", "X̄")
   - Module numbers if mentioned (e.g., "M10", "10.3.5")

2. **Identify subject** using the CFA registry at `.system/memory/strategy/cfa-2026-official-module-registry.json`:
   - Search all subjects' module LOS text for keyword matches
   - The registry contains all 10 subjects with module-level LOS descriptions
   - Score each subject by keyword match density

3. **Read the MOC knowledge tree** — in `CFA_tier1/<topic_area>/00-<Subject-Name>-MOC.md`:
   - Find the `## 3. 核心知识树` section
   - The tree is inside a ````text` code block
   - Lines use `├─` / `└─` with hierarchical numbering like `N.K.L`
   - Search for nodes matching the concept keywords

4. **Read the module knowledge tree** — in `CFA_tier1/<topic_area>/M<nn>-*.md`:
   - Same `## 3. 核心知识树` structure
   - Locate the corresponding node with matching number (e.g., `10.3.5`)

5. **If ambiguous** (multiple subjects match, or no clear match):
   - Use conversation context (recent topics discussed) to disambiguate
   - If still unclear, ask the user for confirmation

### Step 2: Format the annotation

- Format: ` ↳ 笔记：<simplified annotation text>`
- Append to the **end of the matching knowledge tree node line**
- If the node already has a `↳ 笔记：` annotation, append with `；` separator
- Keep annotations concise and in the user's original wording
- Do not add extra line breaks within the tree node

### Step 3: Write to MOC

Edit the MOC file's knowledge tree code block line. Example:

**Before:**
```
│  ├─ 10.3.5 Prediction：`Ŷ=b0+b1X`，prediction interval 宽于 confidence interval
```
**After:**
```
│  ├─ 10.3.5 Prediction：`Ŷ=b0+b1X`，prediction interval 宽于 confidence interval ↳ 笔记：X离X̄越远区间越宽；SEE越大区间越宽
```

### Step 4: Write to module file

Edit the module file's knowledge tree code block line the same way.

### Step 5: Verify

- Confirm the annotation was appended correctly
- Verify tree structure (indentation, `│`, `├─`, `└─`) is intact
- Confirm both MOC and module file were updated

## Topic mapping

Subject directory name → MOC file:

| Directory | MOC File |
|---|---|
| `Quantitative_Methods` | `00-Quantitative-Methods-MOC.md` |
| `Economics` | `00-Economics-MOC.md` |
| `Corporate_Issuers` | `00-Corporate-Issuers-MOC.md` |
| `Financial_Statement_Analysis` | `00-Financial-Statement-Analysis-MOC.md` |
| `Equity` | `00-Equity-MOC.md` |
| `Fixed_Income` | `00-Fixed-Income-MOC.md` |
| `Derivatives` | `00-Derivatives-MOC.md` |
| `Alternative_Investments` | `00-Alternative-Investments-MOC.md` |
| `Portfolio_Management` | `00-Portfolio-Management-MOC.md` |
| `Ethical_and_Professional_Standards` | `00-Ethical-and-Professional-Standards-MOC.md` |

Module files follow `M<nn>-<Module-Topic>.md` inside each subject directory (e.g., `Quantitative_Methods/M10-Simple-Linear-Regression.md`).

MOC knowledge tree nodes use subject-wide numbering (e.g., `10.3.5`). Module knowledge tree nodes use the same numbering. Cross-reference between them by the node number.

## Examples

**Example 1 — Prediction interval note:**
> User: "Prediction interval：X离X̄越远，区间越宽；SEE越大，区间越宽"
> 
> Action:
> 1. Keyword "prediction interval" → Quantitative Methods, M10
> 2. Find `10.3.5 Prediction` in MOC tree
> 3. Append ` ↳ 笔记：X离X̄越远区间越宽；SEE越大区间越宽`
> 4. Same edit in M10 module tree

**Example 2 — Fixed income note:**
> User: "记一下：callable bond 在利率下降时价格涨不上去因为有 call cap"
> 
> Action:
> 1. Keywords "callable bond", "call cap" → Fixed Income
> 2. Search for callable/赎回 node in FI MOC tree (likely `1.3`)
> 3. Append annotation

**Example 3 — FRA note:**
> User: "FRA 毛利率的坑：gross profit margin 分母是 revenue 不是 COGS"
> 
> Action:
> 1. "FRA", "gross profit margin" → Financial Statement Analysis
> 2. Search income statement analysis nodes
> 3. Append annotation

## Boundaries

- **One annotation per invocation** unless the user explicitly sends multiple notes
- **Do not modify** formula tables, exam traps sections, or other non-tree content
- **Preserve original wording** of the user's note — the annotation is their personal memory aid
- **If regex matching fails** to find the exact node line, fall back to line-by-line text search before asking the user
