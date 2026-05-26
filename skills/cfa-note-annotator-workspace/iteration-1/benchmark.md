# Skill Benchmark: cfa-note-annotator

**Model**: DeepSeek-V4-flash
**Date**: 2026-05-26
**Evals**: 3 (prediction-interval-note, callable-bond-note, gordon-growth-note)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|---------------|-------|
| Pass Rate | 100% ± 0% | 20% ± 0% | **+80%** |
| Time | 80.8s ± 24.2s | 31.8s ± 6.7s | +49.0s |
| Tokens | 51,218 ± 13,713 | 24,949 ± 4,992 | +26,270 |

## Per-Eval Results

### prediction-interval-note
- **With skill**: 5/5 passed — annotated MOC node 10.4 and module node 10.3.5
- **Without skill**: 1/5 passed — educational explanation, no tree edits

### callable-bond-note
- **With skill**: 5/5 passed — annotated FI MOC node 1.3 and module node 1.3.1
- **Without skill**: 1/5 passed — educational explanation, no tree edits

### gordon-growth-note
- **With skill**: 5/5 passed — annotated Equity MOC node 8.2 and module node 8.1.2
- **Without skill**: 1/5 passed — educational explanation, no tree edits

## Key Observations

- **100% accuracy** in node matching across all 3 test cases (Quant, FI, Equity)
- **No ambiguity errors** — each run identified the correct subject, MOC node, and module node
- **Annotation format consistently correct** — all used `↳ 笔记：` prefix
- **Tree structure preserved** in all edits
- Baseline runs uniformly produced educational explanations instead of annotations — natural behavior without the skill
- The "trivial pass" (1/5) in baselines is from the structure-preservation assertion (no edits = trivially preserved)
