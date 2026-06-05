# Practice UI API Contract

This contract must exist before changing frontend practice screens. It keeps the
core question bank stable while giving the UI a clear path for project selection,
practice configuration, question display, answer submission, notes, and favorites.

## Scope

- Backend source of truth: `.system/private/question-banks/questions.json`.
- Practice sessions store references only, not copied question text or answers.
- Frontend may render learner state, but it must not mutate canonical question
  records.
- Recommendation and adaptive practice remain extension modules, not part of
  this core practice contract.

## Project Selection

Current usable endpoints:

- `GET /api/profiles`
- `GET /api/profiles/active`
- `PUT /api/profiles/active`

UI fields needed:

| Field | Source | Notes |
|------|--------|-------|
| `profile.short_name` | active profile | Example: `cfa-l1` |
| `profile.name` | active profile | Display label |
| `profile.subjects[]` | active profile | Subject selector |
| `profile.passing_score` | active profile | Optional context, not needed for practice generation |

## Practice Configuration

Endpoint:

```http
POST /api/question-banks/practice-sessions
```

Request:

```json
{
  "exam": "CFA Level I",
  "topic": "Fixed Income",
  "chapter": "M01",
  "difficulty": "medium",
  "count": 10,
  "tags": ["duration", "callable"],
  "tag_mode": "and",
  "seed": 7
}
```

Required UI controls:

| Control | Backend field | Notes |
|------|------|------|
| Exam/project | `exam` | Default can be active profile display name while CFA-only |
| Subject | `topic` | Matches question `topic` or `subject` |
| Chapter/module | `chapter` | Matches question `module` or `chapter` |
| Question count | `count` | Must be greater than zero |
| Difficulty | `difficulty` | Optional; omit or empty for any |
| Tags | `tags` | Optional list |
| Tag mode | `tag_mode` | `and` narrows; `or` broadens |
| Seed | `seed` | Use deterministic seed for replayable sessions |

Response:

```json
{
  "session_id": "practice-session-...",
  "status": "generated",
  "created_at": "2026-06-05T00:00:00+00:00",
  "request": {},
  "candidate_count": 3,
  "question_count": 2,
  "question_ids": ["private-question-..."],
  "question_refs": [
    {
      "question_id": "private-question-...",
      "source_file": "bank.csv",
      "exam": "CFA Level I",
      "topic": "Fixed Income",
      "module": "M01",
      "los": "FI.1"
    }
  ]
}
```

Important: `question_refs` intentionally excludes `prompt`, `choices`, `answer`,
and `explanation`. The UI must not treat the session payload as the display
payload.

## Question Display

Implemented backend display endpoint:

```http
GET /api/question-banks/practice-sessions/{session_id}/questions/{question_id}
```

Pre-submission response should include:

```json
{
  "session_id": "practice-session-...",
  "question_id": "private-question-...",
  "state": "unanswered",
  "prompt": "Question stem",
  "choices": ["A. ...", "B. ...", "C. ..."],
  "topic": "Fixed Income",
  "module": "M01",
  "los": "FI.1",
  "note_count": 0,
  "favorite": false
}
```

Pre-submission response must not include:

- `answer`
- `correct_answer`
- `explanation`
- `rationale`
- prior wrong-answer diagnostics

Post-submission display can merge the answer response below.

## Answer Submission

Endpoint:

```http
POST /api/question-banks/practice-sessions/{session_id}/answer
```

Request:

```json
{
  "question_id": "private-question-...",
  "selected_answer": "B",
  "time_spent": 45,
  "confidence": 2,
  "note": "I confused callable duration.",
  "favorite": true
}
```

Response:

```json
{
  "attempt": {
    "attempt_id": "practice-attempt-...",
    "session_id": "practice-session-...",
    "question_id": "private-question-...",
    "selected_answer": "B",
    "is_correct": true,
    "time_spent": 45,
    "confidence": 2,
    "created_at": "2026-06-05T00:00:00+00:00",
    "topic": "Fixed Income",
    "module": "M01",
    "los": "FI.1"
  },
  "wrongbook_record": null,
  "note": {
    "note_id": "question-note-...",
    "question_id": "private-question-...",
    "attempt_id": "practice-attempt-...",
    "note": "I confused callable duration.",
    "created_at": "2026-06-05T00:00:00+00:00"
  },
  "favorite": {
    "question_id": "private-question-...",
    "favorite": true,
    "last_attempt_id": "practice-attempt-..."
  },
  "feedback": {
    "is_correct": true,
    "correct_answer": "B"
  }
}
```

## Frontend States

| State | Trigger | Required UI behavior |
|------|---------|----------------------|
| `unanswered` | Question display loaded, no local answer | Show prompt and choices, hide answer/explanation |
| `answered` | Submission response received | Lock selected answer for that attempt and show correctness |
| `reviewed` | User opens feedback/explanation once backend display supports it | Show answer-side panel, keep canonical content read-only |
| `noted` | `note` returned or existing note count > 0 | Show note indicator attached to `question_id` |
| `favorited` | `favorite.favorite == true` | Show favorite indicator attached to `question_id` |

## Browser Smoke Checklist

Run this checklist before and after frontend practice UI work:

1. Start API and web app with `.\start-examos.ps1`.
2. Open `http://localhost:3000`.
3. Select CFA Level I, a subject, count, tag mode, and seed.
4. Generate a practice session and confirm the UI receives `session_id`.
5. Open the first question and verify no answer/explanation appears before submit.
6. Submit an answer and verify answer state becomes `answered`.
7. Add a note and favorite; refresh; verify both remain attached to the same `question_id`.
8. Submit an incorrect answer twice; verify wrongbook count increments once per attempt, not as duplicate records.
9. Submit a correct retry; verify wrongbook priority is lowered but historical attempts remain.
10. Check dashboard routes still load.

Use Browser/Chrome verification only after frontend routes exist. Backend-only
contract work should stay covered by pytest and deterministic storage inspection.
