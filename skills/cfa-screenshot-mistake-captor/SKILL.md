---
name: cfa-screenshot-mistake-captor
description: Capture a CFA wrong-question screenshot as a structured question mistake and persist it through the local CLI. Use whenever the user sends a screenshot from official mocks, practice packs, question banks, or similar drill material.
---

# CFA Screenshot Mistake Captor

Treat the screenshot as **raw evidence**, not as already-clean data.

Your job is to convert that evidence into a `record-mistake` payload that is as complete as possible without inventing facts.

## Required outputs

Always normalize screenshot mistakes into:

- `topic`
- `los`
- `prompt_or_question`
- `wrong_choice_or_output`
- `correct_resolution`
- `error_type`
- `confidence`
- `time_spent`
- `evidence_refs`
- `question_source`
- `source_type`
- `evidence_assets`
- `moc_target`

## Source rules

- `source_type` should normally be `screenshot`
- `question_source` should reflect the real source when known:
  - `official_mock`
  - `official_practice_pack`
  - `official_qbank`
  - `third_party_qbank`
  - `custom_drill`
- If the source is unclear, use the most conservative truthful value you can justify. Do not pretend certainty.

## Evidence rules

- Preserve the screenshot identity in `evidence_assets`
- Keep any session or mock grouping token in `evidence_refs`
- If the user names the mock or question set, keep that label

## MOC targeting

Map the mistake to the single best subject MOC path, for example:

- `CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md`
- `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`

If the subject is unclear, leave `moc_target` empty rather than guessing.

## Error discipline

- Prefer incomplete truth over hallucinated precision
- If LOS cannot be determined exactly, use the best honest approximation and say so in the explanation to the user
- Do not fabricate the correct answer if the screenshot is unreadable or incomplete

## Persistence step

After building the payload, call:

```powershell
python scripts/cfa.py record-mistake --payload "{...}"
```

The local runtime is the storage engine. Your responsibility is accurate normalization before calling it.
