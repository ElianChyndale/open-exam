---
name: cfa-agent-auditor
description: Audit local agent review failures such as hallucinated rules, missed root causes, shallow summaries, or unsupported conclusions. Use whenever the agent itself gave a wrong study explanation or risky summary.
---

# CFA Agent Auditor

Convert agent failures into:

- a failure record
- a validation rule
- a safer replacement explanation

## Workflow

1. Identify exactly what the agent got wrong:
   - hallucinated rule
   - missed root cause
   - shallow summary
   - unsupported conclusion
2. Store the failure through `audit-agent`.
3. Produce the replacement explanation in a more conservative form.
4. If the same failure class recurs, strengthen validation rather than merely restating the answer.

## Guardrails

- Quote or restate the incorrect agent claim before correcting it.
- Prefer textbook-safe wording over elegant but risky synthesis.
- If evidence is thin, say the conclusion is uncertain instead of acting confident.
