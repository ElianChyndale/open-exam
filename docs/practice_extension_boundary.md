# Practice Analytics And Recommendation Boundary

This boundary keeps core brushing-question behavior independent from analytics,
recommendations, adaptive practice, and AI-generated strategy. Core practice must
continue working when every extension flag is disabled.

## Feature Flags

Default-disabled extension flags:

- `question_bank_recommendations_enabled`
- `question_bank_adaptive_practice_enabled`

Related existing analytics flags:

- `learning_analytics_enabled`
- `correct_only_analytics_enabled`
- `adaptive_assessment_enabled`
- `assessment_analytics_integration_enabled`

Core endpoints must not depend on the default-disabled question-bank extension
flags:

- `POST /api/question-banks/practice-sessions`
- `POST /api/question-banks/practice-sessions/{session_id}/answer`
- `POST /api/question-banks/import`
- `POST /api/question-banks/{question_id}/review`

## Core Statistics

Core statistics can be computed directly from canonical local records and may be
shown in the practice UI:

| Statistic | Source | Core or extension |
|------|------|------|
| Session question count | practice session metadata | Core |
| Candidate count | practice generation result | Core |
| Attempt correctness | answer submission attempt | Core |
| Time spent | answer submission attempt | Core |
| Wrong count per question | wrongbook record | Core |
| Correct retry count | wrongbook record | Core |
| Favorite and note indicators | notes/favorites stores | Core |

These values describe what happened. They do not decide what the learner should
do next.

## Extension Outputs

The following are extension-layer outputs and must stay outside canonical
question-bank records:

| Output | Why extension-only |
|------|------|
| Recommended next questions | Depends on strategy, analytics, or AI policy |
| Adaptive difficulty changes | Can alter learner path but not source bank |
| Weakness explanations generated from multiple attempts | Derived interpretation, not raw evidence |
| Study strategy suggestions | Decision Layer artifact |
| AI-generated hints | Must be validation-gated and correct-only |

Extension outputs should be stored under extension-specific memory paths, for
example `.system/memory/strategy/` or future `.system/memory/question-bank-extensions/`,
and must include source refs to attempts, sessions, or wrongbook records.

## Rollback Behavior

If analytics or recommendations fail:

1. Keep importing questions, generating practice sessions, and submitting answers.
2. Do not roll back canonical attempts or question-bank records.
3. Write the extension failure as a diagnostic event, not as question-bank truth.
4. Hide recommendation UI modules while preserving core practice UI.
5. Retry extension jobs from source refs after the bug is fixed.

## Implementation Rules

- Core modules may emit events that extensions consume.
- Core modules must not call AI recommendation providers.
- Extension modules may read attempts, wrongbook records, notes, and favorites.
- Extension modules must not mutate `questions.json`, answer keys, explanations,
  or historical attempts.
- Any extension patch must include a disabled-flag test proving core practice
  still works without the extension.
