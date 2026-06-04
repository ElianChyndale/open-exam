# TASK-024 Performance Baseline

Date: 2026-06-03
Scope: commercial readiness freeze gate baseline for local deterministic fixture.

## Method

- Harness: FastAPI `TestClient` against a temporary `Repository` root.
- Fixture: deterministic WACC-centered study graph seeded from existing API test helpers, with model-field normalization for current syllabus topic, transfer-gap, and source-segment schemas.
- Setup calls before measuring: syllabus coverage recompute, knowledge graph recompute, learning analytics recompute, study planner generation, focus session start, and Anki interop export.
- Samples: one warm request per endpoint, followed by nine timed requests.
- Timing unit: milliseconds measured with `time.perf_counter()` in the local Python process.
- All measured endpoints returned HTTP 200.

## Results

| Endpoint | Status | Samples | Min ms | Median ms | P95 ms | Max ms | Bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| `GET /api/navigation/cockpit?profile_id=default` | 200 | 9 | 3.35 | 3.54 | 3.68 | 3.70 | 1468 |
| `GET /api/focus/current?profile_id=default` | 200 | 9 | 5.14 | 5.31 | 5.47 | 5.51 | 7957 |
| `GET /api/review-lab/mission-control` | 200 | 9 | 146.54 | 149.89 | 176.45 | 190.63 | 6536 |
| `GET /api/learning-analytics/summary?profile_id=default&range=30d` | 200 | 9 | 6.70 | 7.06 | 9.05 | 10.25 | 4186 |
| `GET /api/knowledge-graph/search?profile_id=default&q=WACC&limit=10` | 200 | 9 | 6.30 | 6.59 | 23.01 | 33.80 | 23593 |
| `GET /api/tutor/search-context?profile_id=default&q=WACC&mode=formula_help&limit=8` | 200 | 9 | 152.61 | 162.64 | 178.72 | 179.72 | 7117 |
| `GET /api/data-governance/inventory?profile_id=default` | 200 | 9 | 34.25 | 35.56 | 36.84 | 37.30 | 6939 |
| `GET /api/interop/artifacts` | 200 | 9 | 3.28 | 3.45 | 3.61 | 3.62 | 752 |

## Observations

- Navigation, focus current, analytics, graph search, and interop artifact registry are comfortably sub-40 ms on the deterministic fixture.
- Mission Control and Tutor search context are the heaviest freeze-gate surfaces, both because they aggregate multiple subsystem views and perform cross-boundary sanitization. Their local p95 values remained below 180 ms in this run.
- The performance baseline did not require a persistent server and did not read or write the user's real repository memory.
