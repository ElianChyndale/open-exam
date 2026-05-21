---
name: experience-hub
description: Connect question mistakes, cognitive bias, agent failures, patterns, strategy, and validation into one local learning system. Use whenever the user wants a holistic view of what has been learned from prior errors.
---

# Experience Hub

Experience Hub is the governance layer of the CFA local-agent system.

It should connect:

- question errors
- cognitive bias
- agent failures
- patterns
- strategy
- validation

## Core rule

Do not store everything.
Only promote experience that will change the next decision.

## Promotion order

1. Capture the raw event.
2. Distill it into a card or failure record.
3. Promote it to pattern only after repetition.
4. Promote it to strategy only if it changes review order, mock pacing, or intervention.
5. Promote it to validation whenever an agent failure could mislead later outputs.

## Anti-rot rule

Before adding a new long-term experience:

- check whether it already exists
- check whether it is still valid
- check whether it has action value

If it fails any of these checks, merge, downgrade, or discard it.

## Operating files

When using this skill, consult:

- `_registry.md` for what is already active
- `review-checklist.md` for governance
- `operating-rhythm.md` for cadence

Favor connection over repetition, and decision value over archive size.
