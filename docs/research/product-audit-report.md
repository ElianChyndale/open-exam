# OpenExam EXAMOS Product Audit Report

> Date: 2026-06-02
> Scope: Full-stack product completeness audit against PLAN.md, ROADMAP.md, and competitive landscape
> Method: Line-by-line code review of all frontend pages, API routers, study-science engines, and workflows

---

## 1. Feature Coverage Matrix: Planned vs Built vs Missing

### 1.1 Frontend Pages

| Page | PLAN.md Required | Status | Notes |
|------|-----------------|--------|-------|
| Today Cockpit | Yes | BUILT | Energy check-in, tasks by energy tier, danger LOS, weekly focus, quick actions |
| Question Capture | Yes | BUILT | Manual entry, screenshot upload, batch import, confidence/time/error-type |
| Diagnosis | Yes | BUILT | Error classification, fix rules, pattern detection, spacing output |
| Review Pack | Yes | BUILT | Due review, low-confidence items, interleaved sets, formula/concept warmup |
| Mock Center | Yes | BUILT | Session creation, pre-mock brief, post-mock retro, stop-doing list |
| Effectiveness Dashboard | Yes | BUILT | 6 core metrics, LOS risk heatmap, what-if simulation, weekly trend, mastery radar |
| Institution Console | Yes | BUILT | Cohort management, risk report, dropout warnings, instructor recommendations |
| Learning Calendar | Yes | BUILT | Error heatmap, review-completion tracking, exam countdown, date settings |
| LanguageOS Cockpit | Not in PLAN.md (added later) | BUILT | 8 sub-pages for language learning (corpus, grammar, review, stats, etc.) |
| Resource Center | Not in PLAN.md (added later) | BUILT | Web crawl, RSS subscriptions, content audit, private search |

### 1.2 API Endpoints (47 endpoints, all verified working)

| Category | PLAN.md Specified | Built | Missing |
|----------|------------------|-------|---------|
| Attempts | POST /api/attempts, POST screenshot, batch-import, recent | yes | — |
| Diagnosis | POST /api/diagnose, GET /patterns | yes | — |
| Review Pack | GET /review-pack/today, POST /complete | yes | — |
| Study Plan | GET /study-plan/today, /weekly-focus | yes | — |
| Energy | POST /check-in, GET /history | yes | — |
| Mock | POST /create, POST /retro, GET /brief, GET /history | yes | — |
| Dashboard | 10 endpoints (effectiveness, summary, what-if, etc.) | yes | — |
| Institution | POST/GET cohorts, risk-report, weaknesses | yes | — |
| Export | Full export, weekly report, PDF, JSON | yes | — |
| Cards | POST /review, /fix-rule-feedback | yes | — |
| Privacy | Export and purge | yes | — |
| Provenance | GET /api/provenance/{id} | yes | — |
| Profiles | GET, GET active, PUT active | yes | — |
| Question Banks | Import, quarantine, review | yes | — |
| Todos | Full CRUD | yes | — |
| Resources | Full resource center API | yes | — |
| Language | Full LanguageOS API | yes | — |
| Waves | Feature flags | yes | — |

**API Coverage: 100% of PLAN.md specified endpoints are built and functional.**

### 1.3 Cognitive Science Engines

| Engine | PLAN.md Required | Status | Productization |
|--------|-----------------|--------|---------------|
| Retrieval Engine | Yes | BUILT | Not exposed in UI (backend-only) |
| Spacing Scheduler | Yes | BUILT | Static expansion factors, no personalization |
| Interleaving Builder | Yes | BUILT | Integrated into study plan and daily review |
| Worked Example Fader | Yes | BUILT | Not integrated into any UI |
| Self-Explanation Prompt | Yes | BUILT | Not integrated into Diagnosis or Review UI |
| Confidence Calibration | Yes | BUILT | Dashboard shows calibration warnings |
| Energy-Aware Planner | Yes | BUILT | Study plan uses it; Daily Review does NOT |
| Pedagogy Policy | Not required but useful | BUILT | Skeleton implementation |
| Psychometrics (IRT/BKT) | Not required but useful | BUILT | Skeleton implementation |
| Pass Predictor | Not required but useful | BUILT | What-if simulation, dashboard integration |
| Knowledge Memory Engine | Not required but useful | BUILT | 6-state model, decay sweep, dashboard integration |

### 1.4 Data Models (from PLAN.md)

| Model | Required | Status |
|-------|----------|--------|
| ExamAdapter | Yes | PARTIAL (profile system exists but no adapter pattern) |
| SyllabusNode | Yes | PARTIAL (subjects/LOS exist, no formal node system) |
| QuestionAttempt | Yes | BUILT |
| MistakeEvent | Yes | BUILT |
| MistakeCard | Yes | BUILT |
| ErrorDiagnosis | Yes | BUILT |
| ReviewTask | Yes | BUILT |
| EnergyCheckIn | Yes | BUILT |
| StudyPlan | Yes | BUILT |
| MockSession | Yes | BUILT |
| PatternInsight | Yes | BUILT |
| InstitutionCohort | Yes | BUILT |
| LearnerProgressReport | Yes | PARTIAL (per-cohort only, no per-learner report) |

---

## 2. Gap Analysis with Severity

### CRITICAL Gaps (blocking the core learning loop)

| # | Gap | Location | Impact | Root Cause |
|---|-----|----------|--------|------------|
| G1 | **Screenshot AI extraction not implemented** | `/api/attempts/screenshot` | User uploads screenshot but gets no structured extraction — just saves the image. The PLAN.md promises "AI-powered structured extraction." | Router saves file, returns placeholder payload. No vision model integration. |
| G2 | **Daily Review pack does NOT use EnergyAwarePlanner** | `workflows/core.py` (daily_review_pack) | Energy-dependent task ordering only works in Study Plan. Daily Review ignores energy level entirely. | Audit finding confirmed: `energy_planner.py` is complete but `daily_review_pack` doesn't call it. |
| G3 | **Mock retro does not feed back into spacing scheduler** | `mock.py`, `spacing.py` | Mock performance has zero effect on review intervals. A terrible mock score doesn't trigger urgent review. | PLAN.md Wave 0.9 says this is done, but `post_mock_retro` doesn't modify spacing parameters. |
| G4 | **No feedback loop from Diagnosis to KnowledgeMemoryEngine** | `diagnosis_service.py` | Diagnosing an error doesn't update the knowledge state. The KnowledgeMemoryEngine runs independently. | Two separate systems that should be connected. |

### HIGH Gaps (significant product impact)

| # | Gap | Location | Impact |
|---|-----|----------|--------|
| G5 | **7 cognitive science engines exist but only 4 are productized in the UI** | All pages | Retrieval prompts, worked example fading, self-explanation prompts, and pedagogy selection exist as backend engines but have NO UI. Users can't access them. |
| G6 | **No spaced repetition visualization** | Dashboard, Review, Calendar | Users cannot see: what's due next week, what's been mastered, forgetting curves, or review intervals. Only available via raw API (`/api/dashboard/knowledge-readiness`). |
| G7 | **Static expansion factors** | `spacing.py` | `EXPANSION_FACTORS = [1.0, 2.0, 3.5, 5.0, 7.0]` is hardcoded. No personalization per learner. PLAN.md specifies this should be personalized. |
| G8 | **No user auth or multi-user support** | System-wide | Entire system runs as single local user (`learner_id: "local"`). No login, no authentication, no multi-user isolation. Blocks B2C and B2B deployment. |
| G9 | **No learner profile/persistence** | System-wide | No persistent learner characteristic model (calibration bias, learning speed, energy patterns). Dashboard resets on app restart. |

### MEDIUM Gaps (reduced quality, not blocking)

| # | Gap | Location | Impact |
|---|-----|----------|--------|
| G10 | **No pre-mock brief customization** | `mock.py` | Brief is one generic rule. Should use the learner's current weakest areas. |
| G11 | **No formula reference library UI** | System-wide | Formula drill tasks are generated but there's no reference UI for formulas. |
| G12 | **Institution risk report uses approximation** | `institution.py` | In MVP mode, all learners share one repo. Risk report is approximated from events, not learner-specific data. |
| G13 | **What-if simulation only tests review_completion_rate** | Dashboard | Can only adjust one factor. Should support multiple simultaneous adjustments. |
| G14 | **KnowledgeMemoryEngine not connected to study plan generation** | Various | Knowledge state should influence what's scheduled for review, but the connection is loose (topic-based, not knowledge-state-based). |
| G15 | **Batch import endpoint exists but no batch import UI** | Capture page | Only manual entry UI exists. Batch import API works but requires direct API calls. |
| G16 | **Preview import still broken** | `sync_service.py:147` | Known bug from audit findings — `from_payload()` not called, underestimating dedup counts. |

### LOW Gaps (nice-to-have)

| # | Gap | Location |
|---|-----|----------|
| G17 | Frontmatter editor still uses regex (not PyYAML) | `storage.py` |
| G18 | No interleaving composition visualization | Dashboard/Review |
| G19 | No study plan history/calendar view | Study Plan |
| G20 | No WCAG 2.2 AA full audit completed | System-wide |
| G21 | No mobile app or PWA | System-wide |
| G22 | No dark/light theme toggle | Frontend |

---

## 3. Competitive Comparison

### vs Anki (Spaced Repetition Gold Standard)

| Feature | Anki | EXAMOS | Gap |
|---------|------|--------|-----|
| Spaced repetition | Mature, FSRS-5 algorithm | Basic static expansion factors | **Significant** — EXAMOS needs FSRS or similar |
| Card creation | Manual + browser addons | Automated from mistakes | **Advantage EXAMOS** |
| Card types | Rich (Basic, Cloze, Image, Audio) | Markdown-based only | EXAMOS is behind |
| Analytics | Review count, retention rate, cards due | Pass probability, calibration errors, risk heatmap | **Advantage EXAMOS** (better analytics) |
| Sync | AnkiWeb, multiple devices | Local-only (localStorage + JSONL) | **Significant gap** for EXAMOS |
| Mobile | Excellent native apps | None | **Significant gap** |
| Active recall | Core mechanic | Built as backend engine, no UI | EXAMOS engine exists but not user-facing |
| Community decks | Massive library | None (CFA-specific via import) | Not directly comparable |

### vs UWorld (CFA/CPA Exam Prep Leader)

| Feature | UWorld | EXAMOS | Gap |
|---------|--------|--------|-----|
| Question bank | 5000+ CFA questions | No built-in questions (import only) | **Critical gap** |
| Explanations | Detailed, expert-written | AI-generated from user data | EXAMOS has advantage on personalization |
| Performance tracking | Per-topic percentage | Multi-factor pass probability + calibration | **Advantage EXAMOS** |
| Mock exams | Full simulation | Manual mock entry | **Significant gap** |
| Mobile | Good native apps | None | **Significant gap** |
| Price | $200-400/exam | Free-$39/month | **Advantage EXAMOS** |
| Spaced repetition | Not core | Core differentiation | **Advantage EXAMOS** |
| Error diagnosis | Basic | 8-category taxonomy with pattern detection | **Advantage EXAMOS** |

### vs Schweser (Kaplan CFA Prep)

| Feature | Schweser | EXAMOS | Gap |
|---------|----------|--------|-----|
| Content | Complete CFA curriculum notes | No built-in content (user's own notes) | Schweser wins for content |
| Video lectures | Yes | No | **Not in scope** (EXAMOS is post-classroom execution layer) |
| QBank | 4000+ questions | No built-in questions | **Critical gap** |
| Pass guarantee | Conditional | No guarantee | Schweser wins |
| AI error analysis | None | 8-category + pattern detection | **Advantage EXAMOS** |
| Performance prediction | Basic percentage | Multi-factor probability with what-if | **Advantage EXAMOS** |
| Instructor dashboard | None | Cohorts, risk alerts, interventions | **Advantage EXAMOS** |

### vs AnalystPrep / Mark Meldrum

| Feature | AnalystPrep/MM | EXAMOS | Gap |
|---------|---------------|--------|-----|
| Video content | Excellent | None | Not in scope |
| Practice questions | Good | Manual import only | **Critical gap** |
| Mock exams | Good | Manual entry | **Significant gap** |
| AI features | None/minimal | Comprehensive | **Advantage EXAMOS** |
| Pricing | Moderate | Free to cheap | **Advantage EXAMOS** |

### Competitive Positioning Summary

**EXAMOS doesn't compete on content — it competes on process.** The unique value is:

1. **Error diagnosis depth** — 8-category taxonomy + pattern detection. No competitor has this.
2. **Cognitive science integration** — 7 engines working together. Unique.
3. **Institution visibility** — cohort risk alerts and instructor interventions. Schweser/UWorld don't offer this.
4. **Energy-aware planning** — unique to EXAMOS and evidence-backed.
5. **Pass probability prediction with what-if simulation** — unique.

**Critical weaknesses vs competitors:**
1. No built-in question bank (requires user to import or manually enter)
2. No mobile app
3. No spaced repetition UI (algorithm exists but users can't see or control it)
4. Mock exams require manual entry — no built-in mock environment

---

## 4. User Journey Audit

### Full Learning Loop: Question Capture -> Diagnosis -> Review -> Improvement

#### Step 1: Question Capture
**Status: FUNCTIONAL but limited**

| Action | Works | Quality |
|--------|-------|---------|
| Manual question entry | Yes | Good — 8 error types, confidence 0-4, time tracking, LOS |
| Screenshot upload | Yes | **Broken promise** — saves image but no AI extraction |
| Batch import | API only | No UI for batch |
| Voice input | Partial | Error message on incompatible browsers |

**Friction points:**
- No question type selector (MCQ, constructed response, calculation)
- No auto-complete for LOS from CFA curriculum
- Screenshot upload asks for topic/LOS upfront — should auto-detect

#### Step 2: Diagnosis
**Status: FUNCTIONAL but missing depth**

| Action | Works | Quality |
|--------|-------|---------|
| Error category identification | Yes | 8-category taxonomy |
| Fix rule generation | Yes | Context-dependent |
| Next drill suggestion | Yes | Topic/LOS-specific |
| Spacing scheduling | Yes | Links to SpacingScheduler |
| Pattern detection | Yes | Scans existing patterns |
| Self-explanation prompt | Engine exists | **NOT shown in UI** |
| Retrieval prompts | Engine exists | **NOT shown in UI** |
| Worked example fading | Engine exists | **NOT shown in UI** |
| KnowledgeMemoryEngine update | No | **Not called** |

**Friction points:**
- User has to select an attempt and click "diagnose" — not automatic
- Diagnosis result doesn't trigger system updates (no KnowledgeMemory update)
- Self-explanation and retrieval prompts hidden from user

#### Step 3: Review / Daily Review
**Status: FUNCTIONAL but missing energy-awareness**

| Action | Works | Quality |
|--------|-------|---------|
| Due review items | Yes | Includes spaced items, patterns, low-confidence |
| Interleaved practice | Yes | 4-bucket composition |
| Filter by topic/days | Yes | Topic selector, 1-30 day range |
| Knowledge depth option | Yes | Standard/expanded |
| Mark review complete | Yes | Tracks completion |
| Energy-aware prioritization | No | **Confirmed gap** — not integrated |
| Retrieval-first review | No | Shows content directly, no "try to recall first" |
| Worked example fading | Engine exists | **NOT in review UI** |
| Self-explanation | Engine exists | **NOT in review UI** |

**Friction points:**
- Review content is raw Markdown — not interactive
- No "recall first, reveal later" mechanism
- No scoring/reporting on review quality
- No link from review item back to diagnosis

#### Step 4: Effectiveness Dashboard
**Status: EXCELLENT — best part of the system**

| Metric | Display | Quality |
|--------|---------|---------|
| Due review completion rate | Percentage + target | Good |
| High-confidence errors | Count + danger indicator | Good |
| Interleaving accuracy | Percentage + target | Good |
| Same-error recurrence rate | Percentage + target | Good |
| LOS risk heatmap | Visual bar chart | Great |
| Predicted pass probability | Percentage + confidence band | Great |
| Calibration trend | Trend indicator | Good |
| Weekly trend comparison | Week-over-week | Good |
| Topic mastery radar | Radar chart | Great |
| What-if simulation | Button + result | Good |
| Review streaks | Days + weekly goal | Good |
| Calibration warnings | List | Good |

**Friction points:**
- What-if only tests review_completion_rate
- No trend lines over 30+ days
- No export/save dashboard snapshots

#### Step 5: Mock Exam
**Status: FUNCTIONAL but basic**

| Action | Works | Quality |
|--------|-------|---------|
| Create mock session | Yes | Manual entry |
| Pre-mock brief | Yes | Generic, not personalized |
| Post-mock retro | Yes | Basic analysis |
| Stop-doing list | Yes | Rule-based generation |
| Next-mock strategy | Yes | Template-based |
| Mock -> Spacing feedback | No | **Confirmed gap** |
| Mock -> KnowledgeMemory | No | **Not connected** |

#### Full Loop Traceability

```
User captures question → /capture ✓
  ↓
Event saved as MistakeEvent ✓
  ↓
User selects attempt → /diagnosis ✓
  ↓
Diagnosis returned (fix_rule, next_drill, spacing) ✓
  ↓
Card created with review_due_at ✓
  ↓ (gap)
KnowledgeMemoryEngine NOT updated ← ⚠️ 
  ↓ (gap)
Self-explanation/retrieval prompts NOT shown ← ⚠️ 
  ↓
Study plan includes due items ✓ (but not energy-aware in review)
  ↓ (gap)
Daily Review shows items BUT ignores energy level ← ⚠️ 
  ↓
User completes review → KnowledgeMemoryEngine MAY update (if caught by sweep) ✓
  ↓ (gap)
Mock scores don't affect spacing ← ⚠️ 
  ↓
Dashboard aggregates everything ✓
```

**The loop BREAKS at 3 points:**
1. Diagnosis -> KnowledgeMemoryEngine (no update)
2. Study Plan -> Daily Review (energy not integrated)
3. Mock -> Spacing (no feedback)

---

## 5. Top 10 Product Improvements Ranked by Impact/Effort

### T1: Connect Diagnosis to KnowledgeMemoryEngine
**Impact: CRITICAL | Effort: SMALL (2-3 days)**
- When a diagnosis is made, automatically call `KnowledgeMemoryEngine.update()` with the error type
- This closes the feedback loop and makes the Knowledge Memory state machine meaningful
- Files: `diagnosis_service.py`, `workflows/core.py`

### T2: Screenshot AI Extraction
**Impact: HIGH | Effort: MEDIUM (5-7 days)**
- Integrate a vision model (Claude Vision, GPT-4V) to extract question text, choices, answer, topic, LOS from screenshots
- The current implementation saves the image but does nothing with it
- Files: `attempts.py`, new agent integration

### T3: Integrate Energy-Aware Planning into Daily Review
**Impact: HIGH | Effort: SMALL (1-2 days)**
- Call `EnergyAwarePlanner.allocate()` from `daily_review_pack`
- Reorder review items based on current energy level
- Files: `workflows/core.py`, `review.py`

### T4: Personalize Spacing with Dynamic Expansion Factors
**Impact: HIGH | Effort: SMALL (2-3 days)**
- Track per-learner review intervals and compute personalized expansion factors
- Replace static `EXPANSION_FACTORS` with learner-adaptive values
- Files: `spacing.py`, new learner profile

### T5: Productize Missing Engines in UI (Retrieval, Worked Example, Self-Explanation)
**Impact: HIGH | Effort: MEDIUM (5-8 days)**
- Add retrieval-first interaction to Review Pack (show prompt, hide answer, reveal on click)
- Add worked example fading for formula errors
- Add self-explanation prompt after marking a review item complete
- Files: `review/page.tsx`, new components

### T6: Build Mock -> Spacing Feedback Loop
**Impact: MEDIUM | Effort: SMALL (1-2 days)**
- After post-mock retro, adjust spacing intervals based on mock performance
- Low mock score -> compress all intervals, increase priority
- Files: `mock.py`, `spacing.py`

### T7: Add Built-in Question Bank
**Impact: CRITICAL | Effort: LARGE (2-4 weeks)**
- Create a `packages/question-bank/` with CFA-style questions
- Include answer explanations, LOS mapping, difficulty levels
- This is the single biggest gap vs UWorld, Schweser, AnalystPrep
- Alternatively: partner with a question bank provider

### T8: Spaced Repetition Visualization
**Impact: MEDIUM | Effort: SMALL (2-3 days)**
- Show review intervals, due dates, and forgetting curves on Dashboard
- Add a "Reviews Due Next 7 Days" preview to Today Cockpit
- Cards: show review history (when reviewed, next review, interval growth)

### T9: Mobile-First PWA
**Impact: HIGH | Effort: LARGE (2-3 weeks)**
- Add service worker offline support (already partially done)
- Add install prompt, mobile navigation, touch-optimized UI
- Critical for the "capture mistake immediately" use case (e.g., taking a photo of a wrong answer)

### T10: User Authentication and Multi-User Support
**Impact: CRITICAL for B2B/B2C | Effort: LARGE (2-3 weeks)**
- Add user registration, login, session management
- Multi-tenant data isolation
- This is a prerequisite for any commercial deployment

### Impact/Effort Matrix

```
HIGH IMPACT
  │
  │  T1 (Diagnosis→Knowledge)    T7 (Question Bank)***
  │  T2 (Screenshot AI)          T9 (PWA)
  │  T3 (Energy→Daily Review)    T10 (Auth)
  │  T4 (Dynamic Spacing)
  │  T5 (Productize Engines)
  │
  │  T6 (Mock→Spacing)
  │  T8 (Spacing Visualization)
  │
  └───────────────────────────
  LOW EFFORT         HIGH EFFORT

  *** T7 is highest impact but largest effort.
      Consider partnership/licensing instead of building.
```

### Immediate Quick Wins (< 3 days each)

| Task | Effort | Impact |
|------|--------|--------|
| T1: Diagnose -> KnowledgeMemoryEngine | 2-3 days | CRITICAL |
| T3: Energy-aware Daily Review | 1-2 days | HIGH |
| T4: Dynamic expansion factors | 2-3 days | HIGH |
| T6: Mock -> Spacing feedback | 1-2 days | MEDIUM |
| T8: Spacing visualization | 2-3 days | MEDIUM |

**Total: 8-13 days for 5 improvements that close the 3 major loop breaks.**

---

## Summary

### What ExamOS Does Well
- **Dashboard is excellent** — multi-factor pass probability, what-if simulation, calibration tracking, LOS risk heatmap
- **API coverage is complete** — 47 endpoints, all functional
- **Cognitive science engines are comprehensive** — 15 engines, 7 core from PLAN.md all built
- **Institution console is differentiated** — cohort risk, dropout alerts, instructor recommendations
- **Energy-aware planning is unique** — no competitor does this
- **Architecture is sound** — local-first, events-driven, provenance-tracked

### What Needs Fixing
1. **3 loop breaks** in the core learning flow (Diagnosis->Knowledge, Energy->Review, Mock->Spacing)
2. **5 of 7 cognitive science engines are invisible to users** (backend-only)
3. **No built-in question bank** — critical vs competitors
4. **No user auth** — can't go commercial
5. **No spaced repetition visualization** — users can't see their progress

### Competitive Positioning
ExamOS wins on **process intelligence** (error diagnosis, calibration tracking, energy-aware planning, pass prediction). It loses on **content** (no question bank, no video, no curriculum notes) and **platform maturity** (no mobile, no auth, no sync). The strategy of "process over content" is defensible if the core loop is truly closed — but it's not yet. Fix the 3 loop breaks and this becomes a viable product.
