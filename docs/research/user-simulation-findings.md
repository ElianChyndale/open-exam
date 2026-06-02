# User Simulation Findings: CFA Level I Candidate Experience Audit

**Date:** 2026-06-02
**System:** OpenExam EXAMOS
**Exam Window:** Aug/Sep 2026 (approximately 60-90 days out)
**Mock Questions Available:** 872 CFA Level I questions across 10 subjects (FRA: 75, Ethics: 154, Quant: 43, Economics: 31, CorpIss: 55, Equity: 43, FI: 82, Derivatives: 56, AltInv: 38, Portfolio: 36, Unclassified: 259)

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Scenario A: The Diligent User](#2-scenario-a-the-diligent-user)
3. [Scenario B: The Lazy User](#3-scenario-b-the-lazy-user)
4. [Scenario C: The Last-Month Crammer](#4-scenario-c-the-last-month-crammer)
5. [Cross-Cutting Findings](#5-cross-cutting-findings)
6. [Recommendation Priority Matrix](#6-recommendation-priority-matrix)

---

## 1. System Architecture Overview

The EXAMOS system operates on a **manual-capture-first** architecture. Every downstream feature depends on user-entered data:

```
Question Capture (/capture)  ────>  Diagnosis (/diagnosis)
       │                                    │
       │                                    v
       └───>  Attempts Database  ───>  Spacing Scheduler
                                        │
                                        v
       Today Cockpit (/today)  <───  Daily Review Pack (/review)
              │
              v
       Dashboard (/dashboard)  <───  Mock Center (/mock)
```

**Critical pipeline dependency:** If the user does not record attempts via `/capture`, the following features produce empty/no-data states:
- `/review` — "暂无复习内容" (line 190)
- `/diagnosis` — empty pattern list (line 87-113)
- `/dashboard` — LOS risk heatmap "暂无足够数据" (line 225)
- `/today` — no danger LOS list (line 175)

---

## 2. Scenario A: The Diligent User

> **Profile:** Does 30 practice questions daily from UWorld. Uploads screenshots of wrong answers. Uses diagnosis. Does daily review faithfully. Exam 60 days out.

### 2.1 User Journey

**Daily pattern:**
1. Opens `/today` → checks energy, sees task plan
2. Goes to UWorld, does ~30 questions, gets ~8-10 wrong
3. Opens `/capture` → enters each wrong question manually
4. Optionally uploads screenshot after selecting topic
5. Opens `/diagnosis` → selects an attempt, clicks diagnose
6. Opens `/review` → reads the review pack, clicks "完成 Daily Review"

**Weekly pattern:**
1. Opens `/dashboard` → checks pass probability, calibration warnings
2. Opens `/mock` → enters a mock exam session result
3. Reviews weekly focus recommendations

### 2.2 Pain Points

#### P1. Screenshot Upload Requires Pre-Selected Topic (HIGH)
**File:** `apps/web/src/app/capture/page.tsx`, line 69
```typescript
if (!file || !form.topic) return;
```
A diligent user who takes a screenshot of a question during study must first navigate to `/capture`, select the topic from a dropdown, THEN upload. This breaks the natural workflow of "take screenshot first, classify later."

**Impact:** User takes screenshot of a Quant question while studying. Opens `/capture` later. Must remember which topic it was. If unsure, upload is blocked — they must guess a topic or abandon. Adds friction to the most efficient capture path.

#### P2. No Batch/Quick Capture Mode (HIGH)
The capture page (lines 29-65) presents a full form with 9+ fields. For a diligent user recording 8-10 wrong answers daily, entering each one individually takes 5-10 minutes. Fields like `prompt_or_question` (line 150) require full question text — a heavy burden.

**Impact:** User will either:
- Skip recording some wrong answers (data loss)
- Enter minimal/incomplete records (low-quality data)
- Abandon the habit entirely after 2-3 days

#### P3. No Auto-Suggest from Screenshot OCR (HIGH)
The screenshot upload endpoint (`/api/attempts/screenshot`, api.ts line 25-26) sends `topic`, `los`, `image_data`, and `filename` — but there is no client-side OCR or AI extraction before upload. The upload just stores the image; the user still must manually enter everything on the form.

**Impact:** Screenshot upload and manual form entry are parallel workflows that don't connect. User uploads a screenshot AND separately fills in the form — doubling effort.

#### P4. Review Completion is Self-Reported, Not Verified (MEDIUM)
**File:** `apps/web/src/app/review/page.tsx`, lines 181-187
```typescript
<button onClick={() => reviewId && reviewApi.complete(reviewId).then(() => setCompleted(true))}>
  {completed ? 'Reviewed once' : '完成 Daily Review'}
</button>
```
The user simply clicks a button to mark review as complete. The system has no way to know whether the user actually:
- Read the knowledge points
- Attempted the active recall (the "先遮答案想" sections)
- Solved the problems
- Or just clicked "完成" to get the badge

**Impact:** False-positive "review complete" signals pollute the spacing algorithm. The system thinks a topic was reviewed when it was only glanced at. Dashboard metrics (`due_review_completion_rate`, line 143 of dashboard) become unreliable.

#### P5. No Quick Navigation Between Capture and Review (MEDIUM)
After entering a wrong answer, the natural next step is to see if that error appears in the review pack. But there is no link from `/capture` success state to `/review`. The only path is via the Today Cockpit quick actions (today page line 219).

**Impact:** User finishes capture, wants to verify it appears in review. Must manually navigate to `/review`, possibly set the right parameters, and scan the pack.

#### P6. Diagnosis is One-at-a-Time (LOW-MEDIUM)
**File:** `apps/web/src/app/diagnosis/page.tsx`, lines 58-72
The user selects ONE attempt and clicks "诊断选中错题." For 8-10 daily wrong answers, running diagnosis individually on each is tedious. No batch diagnosis.

**Impact:** User will diagnose only the most "interesting" errors, leaving patterns undetected.

### 2.3 System Blind Spots

#### BS1. Unknown Knowledge — Correct Answers Not Tracked
The system ONLY records wrong answers (attempts with error). The user gets 20-22 questions right each day, but the system has zero data on these. This means:
- The system doesn't know what the user KNOWS, only what they GET WRONG
- Dashboard pass prediction is based on error data only — not balanced by success volume
- Spacing algorithm never extends intervals for correctly-known material

**File:** `packages/study-science/src/study_science/spacing.py`, lines 62-74 — intervals defined by (is_correct, confidence) tuple. But `is_correct=True` records are never created because only wrong answers are captured.

#### BS2. UWorld Data is Invisible
The user does questions from UWorld (a third-party platform). The system has zero integration with UWorld or any Qbank API. Every question must be manually re-entered. This creates:
- Massive capture friction (see P2)
- No automatic import of correct answers
- No tracking of questions done vs. questions captured

#### BS3. No "Not Captured" Detection
The user might do 30 questions, get 8 wrong, but only capture 5. The system has NO way to detect this gap. The user's Dashboard will show 5 attempted questions when reality is 30. Pass probability (dashboard line 93) will be wildly overconfident.

#### BS4. Time Spent Is Self-Reported and Often Wrong
**File:** capture page, lines 207-215
The user enters "time spent" manually as a number. Research consistently shows learners cannot accurately self-report time spent per question. The spacing algorithm uses `time_spent_seconds` (spacing.py line 166) as a correctness signal (fast wrong = careless). Self-reported times corrupt this signal.

#### BS5. Screenshot Evidence Decoupled from Error Record
When a user uploads a screenshot (capture page line 67-87), they get a success message, but the uploaded image is not linked to a specific error record. The `evidence_refs` field (line 57) uses a timestamp-based manual ID: `manual-${Date.now()}`. There is no way to navigate from an error in the review pack back to its original screenshot.

### 2.4 Feature Gaps

1. **Batch capture mode** — capture multiple errors in a single form session, reusing shared fields (topic, LOS, date)
2. **Screenshot → auto-form-fill** — use OCR/vision API to extract question text, topic hints, and answer choices from screenshots
3. **"Quick Capture" simplified form** — minimal fields: topic, LOS, confidence, correct answer. Everything else optional
4. **Review completion verification** — add a "skip this item" vs "I reviewed this" toggle, or require at least one interaction per card
5. **Correct answer logging** — allow user to log "I got these right" to balance the dataset
6. **External Qbank integration hooks** — even a simple "I did X questions in topic Y today" summary would capture volume data
7. **Screenshot gallery linked to errors** — ability to view original screenshot from diagnosis result or review card

---

## 3. Scenario B: The Lazy User

> **Profile:** Does questions from a paper mock exam. Never uploads screenshots. Only marks answers in a notebook. Logs into the system once a week. Has weak spots they don't know about because they never recorded mistakes.

### 3.1 User Journey

**Weekly pattern:**
1. Saturday: Does 90 questions from paper mock in notebook
2. Monday: Logs into `/today` — sees empty tasks, no plan generated
3. Clicks `/mock` → creates a mock session record: enters total 90, correct 45
4. Clicks `/review` → sees "暂无复习内容"
5. Clicks `/dashboard` → pass probability shown, but based on only 1 mock data point
6. Closes browser, doesn't return for a week

### 3.2 Pain Points

#### P1. No Quick Session Summary (HIGH)
The user did 90 questions on paper. The only way to log this is via `/mock`, which requires:
- Session ID (line 113-118: placeholder "e.g. mock-1")
- Session label
- Total questions
- Correct count

No way to break down by subject. No way to record which specific questions were wrong. The mock system is a **summary-only** tool — it stores aggregate scores, not per-question data.

**File:** `apps/web/src/app/mock/page.tsx`, lines 112-136 — `newMock` only has `total_questions`, `correct_count`, `total_minutes`.

**Impact:** The mock center shows a session as "90 questions, 50% correct" but cannot tell you that the user failed all FRA questions and aced Quant. The retro analysis (line 202-237) may produce generic advice.

#### P2. No Data = No Value (CRITICAL)
This user logs in once a week and enters almost nothing. The system generates:
- Empty review pack (review.tsx line 189-194)
- "暂无活跃错误模式" on diagnosis (diagnosis.tsx line 87)
- Dashboard with "暂无足够数据" on risk heatmap (dashboard line 224)
- Today Cockpit with "暂无高危LOS" (today line 175)

**File:** `apps/web/src/app/today/page.tsx`, lines 147-178 — warnings and danger LOS list are empty when no data exists.

**Impact:** The user sees empty screens and concludes the system provides no value. They stop logging in. Their study continues offline with zero feedback loops. This is a retention death spiral.

#### P3. No Reminders or Nudges (MEDIUM)
There is no notification system, no email/SMS reminder to log errors, no "you haven't logged in 3 days" message. The only engagement mechanism is the Today Cockpit's energy check-in, which only works if the user opens the app.

**File:** No push notification infrastructure found in the codebase. The scheduler task (`Resource Center` resources page lines 207-209) only handles RSS/crawl scheduling, not user engagement.

#### P4. Paper Mock Has No Resolution into the System (HIGH)
The user does 90 questions on paper with answers written in a notebook. To get any value from the system, they would need to:
1. Look up each wrong question in the 872-question mock bank (in `CFA_tier1/mock/`)
2. Find the topic and LOS for each
3. Manually enter each wrong question into `/capture`

This is 30-45 minutes of work for a mock exam. Realistically, no lazy user will do this.

#### P5. No Baseline Assessment (MEDIUM)
The user has no idea which subjects are their weakest. They chose to study by intuition (doing a paper mock). The system could help by providing a diagnostic assessment, but there is no "quick diagnostic" feature — only the mock center, which requires setting up a session.

**File:** `apps/web/src/app/mock/page.tsx` — the mock center is designed for full-length mocks, not for quick topic-level assessments.

### 3.3 System Blind Spots

#### BS6. Complete Blindness to Offline Activity (CRITICAL)
The lazy user is studying — doing questions, reading textbooks, attending classes. But the system sees NOTHING. It cannot differentiate between:
- "User hasn't studied at all" (abandoned)
- "User studied but didn't log" (data gap)

**Impact on the key insight:** "考生可能存在没有把错题上传的可能性" — This is the EXACT scenario. The user might have 20 weak knowledge points from their paper mock, but the system has zero signal. The Dashboard shows "70% pass probability" based on 90 mock questions, when the reality is the user failed every FRA question and passed by luck on others.

#### BS7. Mock Data Has No Subject Granularity
**File:** `apps/web/src/app/mock/page.tsx`, lines 150-168 — session display shows `total_questions` and `correct_count` only. No subject breakdown. The retro analysis (`.system/app/mock_exam.py`, lines 56-65) stores per-question answers, but the UI only displays aggregate.

**Blind spot:** A user could score 50% on a mock with wildly different subject performance (100% on Quant, 20% on FRA) and the system would only show "50%." The dashboard's LOS risk heatmap (dashboard.tsx lines 199-235) would have no data to populate.

#### BS8. No Session-to-Capture Pipeline
When a user creates a mock session, there is no follow-up prompt to "enter the questions you got wrong in this mock." The mock and capture systems are disconnected data silos.

#### BS9. No Trend Detection from Sparse Data
The lazy user enters data so infrequently that the system's trend analysis (dashboard calibration_trend, error_count_trend) has 1-3 data points. The trend direction is meaningless (dashboard line 168: "稳定" is the default when there's no data to trend).

### 3.4 Feature Gaps

1. **Paper mock answer sheet scanner** — scan a paper answer sheet, auto-grade, per-subject breakdown
2. **Bulk import from notebook** — "I answered 20 questions in Corporate Issuers, got 14 correct, missed these LOS:" — a weekly summary form
3. **Commitment reminders** — low-friction nudge to enter at least mock scores
4. **Missed data warning** — dashboard should show "We estimate you've studied XX hours offline. Enter at least your scores to get accurate feedback"
5. **Mock-to-capture bridge** — after recording a mock, prompt: "Enter the questions you got wrong"
6. **"No-action decay" notice** — if the system has no data for 7+ days, show a clear warning on every page
7. **Phone/tablet quick capture** — currently the UI is desktop-optimized; no mobile-friendly way to quickly log errors while studying

---

## 4. Scenario C: The Last-Month Crammer

> **Profile:** Exam is 30 days away. User has been studying for months but needs aggressive review + mock focus. Significant data may already exist in the system.

### 4.1 User Journey

1. Opens `/today` — sees standard daily plan, no urgency
2. Opens `/review` — sees 20 items, sets days_back=30, gets a much longer pack, but still no "exam countdown" mode
3. Opens `/dashboard` — sees pass probability, but no "you should be doing X mocks per week"
4. Opens `/mock` — sees past mock sessions, but no "schedule your next mock" recommendation
5. Wants a study plan for the final 30 days — no feature exists

### 4.2 Pain Points

#### P1. No Exam Countdown / Urgency Indicator (HIGH)
**File:** `apps/web/src/app/today/page.tsx` — the cockpit shows available minutes, energy level, and tasks. But there is NO:
- "Days until exam" countdown
- "You should have completed X% of your study by now" progress
- "Recommended study hours per week" for remaining time
- Any visual indicator that the exam is approaching

The spacing algorithm (`spacing.py` lines 132-147) DOES compress intervals for <30 day exams, but the UI never surfaces this urgency to the user.

#### P2. Normal Mode vs. Exam Mode — No Distinction (CRITICAL)
The system treats day 1 of studying the same as day 100. The Today Cockpit generates the same structure regardless of time-to-exam. There is no "冲刺模式" (sprint mode) or "final review mode" that:
- Prioritizes mock exams over new learning
- Recommends formula cramming sessions
- Switches from spaced expansion to massed review for critical items
- Suggests topic priority based on exam weights (weights defined in `mock_exam.py` line 9: `EXAM_WEIGHTS`)

**File:** `.system/app/mock_exam.py`, line 34 — `subject_distribution` uses exam weights for mock creation, but this weighting is NOT used for study planning.

#### P3. Review Pack Too Large, No Cull Strategy (MEDIUM)
With 30 days back (`daysBack=30`, review.tsx line 154), a diligent user who has been tracking errors for months could have 100+ review items. The review page generates ONE monolithic pack. No:
- Priority-based filtering (show only top-10 most dangerous items)
- Time-based suggestion ("you have 60 minutes today — here are the 8 most important items")
- "Skip mastered" option

**File:** `apps/web/src/app/review/page.tsx`, lines 131-169 — filters exist for subject and depth, but no priority filter. The spacing scheduler computes priority (spacing.py lines 150-163) but the review pack doesn't surface it as a filter.

#### P4. Mock Recommendations Are Missing (HIGH)
The mock center (mock page) tracks sessions and produces retros, but there is NO:
- Recommended mock schedule ("take Mock 3 this Saturday")
- Automatic progress tracking ("you've done 2 of 5 available mocks")
- Subject weakness identification from mock performance
- Comparison of mock scores over time

**File:** `apps/web/src/app/mock/page.tsx` — the retro panel (lines 197-237) shows per-question error count and bias count, but the pre-mock brief (lines 172-195) is generic.

#### P5. No What-If for Exam Readiness Path (MEDIUM)
The Dashboard has a "What-If" button (dashboard.tsx lines 244-255) that simulates improving review completion rate by 10%. But a crammer needs to know:
- "How many mocks should I take to pass?"
- "What if I improve my worst 3 LOS?"
- "What if I focus only on high-weight topics?"

The single what-if dimension (review_completion_rate) is too narrow.

**File:** `apps/web/src/app/dashboard/page.tsx`, line 251 — `runWhatIf({ review_completion_rate: 0.1 })` only tests one variable.

#### P6. Daily Review Marked Complete but Not Mastered (MEDIUM)
The review pack marks a review as "done" (review.tsx line 186) but doesn't track:
- Which items the user still doesn't know
- How many rounds of review a topic has had
- Whether the user needs re-review tomorrow vs. next week

**Impact for crammer:** A user might go through 100 review items, mark them all "done," but have no idea which ones they still need to focus on. The "done" status is misleading.

### 4.3 System Blind Spots

#### BS10. No Exam-Level Readiness Score
The dashboard shows `predicted_pass_probability` (dashboard.tsx line 93), but this is based on error-tracking data, not on:
- Mock exam scores (which are the best predictor)
- Coverage across all LOS
- Time management performance
- Subject weight alignment

A user could have good tracking data but fail the exam because they haven't done enough timed practice.

#### BS11. Mock Question Bank Is Disconnected from Review
The 872 CFA mock questions in `CFA_tier1/mock/` are **not connected** to the review or diagnosis pipeline. They exist as static markdown files in 10 subject folders. The system cannot:
- Pull a question from the bank for review practice
- Generate interleaved problem sets from the bank
- Track which bank questions have been attempted
- Recommend specific bank questions for weak LOS areas

**File:** `CFA_tier1/mock/*/` — subject folders (FRA, Economics, etc.) contain markdown questions, but there is no ingestion path from these files into the attempt/review pipeline.

#### BS12. No Recommended Schedule for Final Phase
There is no "30-day study plan" generator. The system has all the data to create one:
- `mock_exam.py` has exam weights
- `spacing.py` has urgency compression for <30 days  
- `calibration.py` knows dangerous topics
- `knowledge_memory.py` tracks mastery state

But no feature surfaces a structured 30-day plan.

#### BS13. Subject Weighting Ignored in Study Planning
**File:** `.system/app/mock_exam.py`, line 9 — CFA exam weights are defined as `EXAM_WEIGHTS`. These weights determine how many questions appear in the exam for each subject.
- FRA: 13-17%
- Ethics: 15-20%
- Quant: 6-9%
- Economics: 6-9%
- Corporate Issuers: 6-9%

In the final month, a crammer should spend more time on high-weight subjects. The system does not weight study recommendations.

### 4.4 Feature Gaps

1. **Exam countdown banner** — "30 days until exam" on every page with urgency-driven recommendations
2. **Sprint mode / 冲刺模式** — switches the system to mock-first, review-culled, massed-practice mode
3. **Priority culling for review** — "Show only my 10 most dangerous items" filter
4. **Mock schedule planner** — "You've done 2 mocks. based on your performance, take Mock 3 this Friday. Here's your predicted score range."
5. **Mock question bank integration** — pull specific questions from the 872-bank into review sessions based on weak LOS
6. **30-day study plan generator** — structured week-by-week plan balancing mocks, review, and weak-topic drilling
7. **Weight-adjusted pass prediction** — pass probability that accounts for mock scores by subject weight, not just overall
8. **Formula cram mode** — dedicated formula review with spaced recall of all key formulas
9. **"Last review before exam" feature** — a curated 24-hour-before-exam review pack focused on high-probability topics and common pitfalls
10. **Time management tracker** — track how long user spends per question in mocks, flag subjects where they're spending too long

---

## 5. Cross-Cutting Findings

### 5.1 The "Missing Upload" Blind Spot (Key Insight Validation)

The user's observation is confirmed: "考生可能存在没有把错题上传的可能性，或者是一边看答案一边做的题目导致有些知识点可能有薄弱的风险"

This manifests in three ways:

1. **Deliberate skip (Scenario A):** User does 30 questions, gets 8 wrong, but the manual entry burden means only 4-5 get captured. The system believes the user has 4-5 weak areas when reality is 8.

2. **Complete skip (Scenario B):** User does 90-question mock on paper, enters only aggregate score. System believes "90 questions done, 50% correct" but has ZERO visibility into which specific LOS are weak. Dashboard shows pass probability as "70%" based on thin data.

3. **Cheated answers (Key Insight Specific):** User who "looks at answers while doing questions" (一边看答案一边做) has an even worse problem: they might not realize they're weak because they got the answer right by reading the explanation. The system has NO mechanism to detect this — it only knows whether the user SELF-REPORTS a question as wrong. If the user checked the answer before submitting, they might self-assess as "confident" even though they couldn't have answered independently.

**Impact:** The system's pass probability and LOS risk heatmap are only as good as the user's self-reporting. There is no independent verification of knowledge.

### 5.2 Single-User / No Offline Mode

The entire system is web-based with no offline capability. The `API_BASE` in `api.ts` line 3 defaults to empty (same origin), but all API calls are HTTP fetch. A user studying on a train, plane, or in a cafe with intermittent internet cannot use the system.

### 5.3 No Mobile Responsiveness

The UI uses `max-w-5xl`, `max-w-4xl`, `max-w-3xl` containers (review.tsx line 113, mock.tsx line 94, capture.tsx line 90, today.tsx line 92). The forms use sm: grid breakpoints, but the overall experience is desktop-first. A user who wants to capture a question on their phone during a commute will struggle with small form fields and no mobile-optimized layout.

### 5.4 No Study Timer / Pomodoro

The energy planner (`energy_planner.py`) recommends tasks based on energy level and available_minutes, but there is no built-in study timer, pomodoro tracker, or focus session. The user must externally track their study time.

### 5.5 Data Silos

The system has multiple modules that would benefit from cross-referencing but don't:
- **Mock scores ↔ LOS mastery** — a user who scored 30% on FRA in Mock 1 should have FRA LOS automatically tagged as high-risk
- **Screenshot evidence ↔ review cards** — review cards reference "chat-screenshot-2026-05-25-bootstrap-standard-error" but there's no clickable link to the actual screenshot
- **Energy patterns ↔ error rates** — are errors higher when energy is low? The system could detect this but doesn't

---

## 6. Recommendation Priority Matrix

| Priority | Finding | Scenario(s) | Effort | Impact |
|----------|---------|------------|--------|--------|
| P0 | Screenshot auto-extraction (OCR/AI) | A | Medium | High |
| P0 | Quick capture / batch mode | A, B | Low | High |
| P0 | Mock-to-LOS breakdown | B, C | Medium | High |
| P1 | Exam countdown + urgency mode | C | Low | High |
| P1 | Review completion verification | A, C | Low | Medium |
| P1 | Correct answer logging | A | Low | Medium |
| P1 | Mock schedule recommendations | C | Medium | Medium |
| P1 | 30-day study plan generator | C | High | High |
| P2 | Notification/reminder system | B | Medium | Medium |
| P2 | Mock question bank integration | C | High | High |
| P2 | Offline/mobile capture | A, B | High | Medium |
| P2 | What-if simulation expansion | C | Low | Low |
| P3 | Study timer integration | A | Low | Low |
| P3 | Screenshot gallery | A | Medium | Low |

### Quick Win Matrix (Low Effort, High Impact)

| Win | File(s) | Change |
|-----|---------|--------|
| Remove topic pre-requisite for screenshot upload | `capture/page.tsx` line 69 | Remove `!form.topic` check |
| Add "days to exam" banner | `today/page.tsx` | Read exam_date from profile, add countdown |
| Add priority filter to review | `review/page.tsx` lines 131-169 | Add "only dangerous" filter option |
| Mock subject-level breakdown | `mock/page.tsx` | Add subject score fields to session creation |
| Review completion tracking | `review/page.tsx` lines 181-187 | Add per-item "I reviewed this" checkboxes |
| Link from capture success to review | `capture/page.tsx` line 234 | Add "查看此错误在复习包中" link |

---

## Appendix A: Files Referenced

| File | Line(s) | Relevance |
|------|---------|-----------|
| `apps/web/src/app/capture/page.tsx` | 28-250 | Full capture flow |
| `apps/web/src/app/review/page.tsx` | 1-198 | Daily review UI |
| `apps/web/src/app/diagnosis/page.tsx` | 1-205 | Error diagnosis flow |
| `apps/web/src/app/mock/page.tsx` | 1-242 | Mock exam center |
| `apps/web/src/app/today/page.tsx` | 1-272 | Today cockpit |
| `apps/web/src/app/dashboard/page.tsx` | 1-311 | Effectiveness dashboard |
| `apps/web/src/app/resources/page.tsx` | 1-265 | Resource center |
| `apps/web/src/lib/api.ts` | 1-358 | API client |
| `.system/app/mock_exam.py` | 1-122 | Mock exam engine |
| `packages/study-science/src/study_science/spacing.py` | 1-181 | Spacing algorithm |
| `packages/study-science/src/study_science/calibration.py` | 1-100 | Calibration detection |
| `packages/study-science/src/study_science/knowledge_memory.py` | 1-100 | Knowledge state machine |
| `packages/study-science/src/study_science/energy_planner.py` | 1-60 | Energy-aware planning |
| `.system/memory/strategy/daily-review.md` | 1-776 | Sample daily review pack (49 source events, 20 items) |
| `.system/memory/strategy/weekly-focus-2026-06-02.md` | 1-23 | Sample weekly focus |
| `CFA_tier1/mock/00-Mock-Source-Index.md` | 1-24 | Mock question inventory (872 questions) |
| `CFA_tier1/mock/FRA/00-FRA-Mock-Questions.md` | 1-50 | Sample subject question bank (75 FRA questions) |

## Appendix B: Key Numerical Observations

- 872 mock questions available in the bank, but NONE are accessible through the review/capture pipeline
- 259 of 872 questions (30%) are unclassified — assigned to "Unknown" bucket
- FRA has 75 questions, Ethics has 154 — significant imbalance
- Daily review pack (sample) contained 20 items from 49 source events
- Weekly focus identified Economics as top weakness (14 errors in 7 days)
- Missing options text appears in 4 of 20 review items (`_options_missing: 原错题卡未捕获选项`)
- The `manual-${Date.now()}` evidence ID pattern creates zero traceability
