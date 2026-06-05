from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.feature_flags import FeatureFlags
from app.models import stable_id
from app.skill_upgrade import load_upgrade_proposals
from app.storage import Repository


LOOP_EVENT_STREAM = "codex_loop"
LOOP_MEMORY_DIR = Path(".system/memory/codex-loop")
LOOP_COMPLETION_DIR = LOOP_MEMORY_DIR / "completions"
TASK_DIR = Path("docs/codex_tasks")
ATTEMPTS_ROUTER_PATH = Path("apps/api/routers/attempts.py")
AUTH_ROUTER_PATH = Path("apps/api/routers/auth.py")
FRONTEND_API_PATH = Path("apps/web/src/lib/api.ts")
SECURITY_ROUTER_PATH = Path("apps/api/routers/security.py")
SECURITY_PAGE_PATH = Path("apps/web/src/app/review/security/page.tsx")
QUESTION_BANK_CONSOLE_PATH = Path("apps/web/src/components/capture/QuestionBankImportConsole.tsx")
CAPTURE_PAGE_PATH = Path("apps/web/src/app/capture/page.tsx")
MOCK_ROUTER_PATH = Path("apps/api/routers/mock.py")


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class CodexLoopCandidate:
    candidate_id: str
    title: str
    source: str
    phase: str
    layer: str
    priority: int
    expected_outputs: list[str]
    acceptance_criteria: list[str]
    safety_limits: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    risk_level: str = "safe"
    requires_human: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CodexLoopPlan:
    loop_id: str
    mode: str
    selected: CodexLoopCandidate | None
    candidates_considered: list[CodexLoopCandidate]
    task_path: str
    plan_json_path: str
    plan_markdown_path: str
    generated_at: str = field(default_factory=_now)
    status: str = "planned"
    stop_conditions: list[str] = field(default_factory=list)
    impact_controls: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["selected"] = self.selected.as_dict() if self.selected else None
        payload["candidates_considered"] = [candidate.as_dict() for candidate in self.candidates_considered]
        return payload


SELF_CYCLE_BOOTSTRAP = CodexLoopCandidate(
    candidate_id="self-cycle-skill-governance",
    title="Bootstrap governed Codex self-cycle workflow",
    source="plan_doc",
    phase="self-cycle",
    layer="Decision",
    priority=100,
    expected_outputs=[
        "Create a governed Codex loop planner that can choose the next safe task from local evidence.",
        "Add CLI commands for planning and completing autonomous loop steps.",
        "Document safety gates so unattended work cannot mutate core question-bank truth silently.",
    ],
    acceptance_criteria=[
        "A local command writes a traceable next-step plan and task artifact.",
        "Completed candidates are not selected again.",
        "Tests cover planning, completion, and proposal-driven task selection.",
    ],
    safety_limits=[
        "Do not auto-edit published question content, locked answer keys, secrets, or remote branches.",
        "Do not mark a task complete without tests or an explicit verification note.",
        "Do not bypass AGENTS Source of Truth ordering.",
    ],
    evidence_refs=["系统改革与刷题计划.docx", "AGENTS.md"],
    risk_level="safe",
)


PLAN_PHASE_CANDIDATES: tuple[CodexLoopCandidate, ...] = (
    CodexLoopCandidate(
        candidate_id="phase-1-import-contract",
        title="Harden question-bank import contract and immutable published records",
        source="plan_doc",
        phase="1-environment-data-model",
        layer="Capture",
        priority=92,
        expected_outputs=[
            "Define import payload validation for exam, subject, chapter, knowledge tags, difficulty, and answer fields.",
            "Add a published-question immutability guard for prompts, choices, answers, and explanations.",
            "Emit an import report that separates accepted, rejected, duplicate, and locked records.",
        ],
        acceptance_criteria=[
            "Invalid imports are rejected with actionable errors.",
            "Published core question content cannot be changed without an explicit override path.",
            "Tests prove import order and explanation text stay stable after publish.",
        ],
        safety_limits=[
            "Do not rewrite existing core question text or answer explanations.",
            "Do not infer missing official answers from ambiguous source files.",
            "Keep import changes behind tests and local data only.",
        ],
        evidence_refs=["系统改革与刷题计划.docx#阶段1"],
        risk_level="guarded",
    ),
    CodexLoopCandidate(
        candidate_id="phase-2-practice-generation",
        title="Add governed practice generation with AND/OR tag filters",
        source="plan_doc",
        phase="2-question-bank-practice",
        layer="Decision",
        priority=88,
        expected_outputs=[
            "Create a deterministic practice-session request model with exam, topic, chapter, count, and tag filters.",
            "Support AND/OR tag semantics without changing the source question bank.",
            "Persist generated session metadata for answer submission and review.",
        ],
        acceptance_criteria=[
            "Practice generation can be reproduced in tests with a seeded random source.",
            "AND filters narrow results and OR filters broaden them as documented.",
            "The generated session references questions without copying or mutating canonical records.",
        ],
        safety_limits=[
            "Do not duplicate canonical question content into mutable session state.",
            "Do not use random behavior in tests without a fixed seed.",
            "Do not add recommendation logic inside the core question-bank module.",
        ],
        evidence_refs=["系统改革与刷题计划.docx#阶段2"],
        risk_level="guarded",
    ),
    CodexLoopCandidate(
        candidate_id="phase-2-answer-wrongbook-contract",
        title="Connect answer submission to attempts, wrongbook, notes, and favorites",
        source="plan_doc",
        phase="2-question-bank-practice",
        layer="Capture",
        priority=84,
        expected_outputs=[
            "Persist each answer attempt with correctness, selected answer, time spent, and session ID.",
            "Update wrongbook records idempotently when answers are incorrect.",
            "Add note and favorite records that remain attached to a stable question ID.",
        ],
        acceptance_criteria=[
            "Repeated incorrect answers increment wrongbook counters instead of creating duplicates.",
            "Correct retries can lower wrongbook priority without deleting history.",
            "Notes and favorites survive repeated answer submissions.",
        ],
        safety_limits=[
            "Do not delete historical attempts when wrongbook priority changes.",
            "Do not expose hidden correct answers before submission.",
            "Keep user notes separate from canonical question text.",
        ],
        evidence_refs=["系统改革与刷题计划.docx#阶段2"],
        risk_level="guarded",
    ),
    CodexLoopCandidate(
        candidate_id="phase-3-practice-ui-contract",
        title="Create practice UI API contract before changing frontend screens",
        source="plan_doc",
        phase="3-frontend-prototype",
        layer="Decision",
        priority=76,
        expected_outputs=[
            "Write a compact API contract for project selection, practice configuration, question display, and submission.",
            "Define frontend states for unanswered, answered, reviewed, noted, and favorited questions.",
            "Add a smoke-test checklist for browser verification.",
        ],
        acceptance_criteria=[
            "The contract names every backend field the practice UI needs.",
            "The checklist can be run before and after frontend work.",
            "No frontend route is changed before the contract exists.",
        ],
        safety_limits=[
            "Do not redesign UI until the API contract is stable.",
            "Do not introduce Chrome/browser dependency into backend-only tests.",
            "Preserve existing dashboard routes.",
        ],
        evidence_refs=["系统改革与刷题计划.docx#阶段3"],
        risk_level="safe",
    ),
    CodexLoopCandidate(
        candidate_id="phase-4-analytics-extension-boundary",
        title="Separate analytics and recommendation extension boundary from core practice",
        source="plan_doc",
        phase="4-analytics-extensions",
        layer="Decision",
        priority=72,
        expected_outputs=[
            "Document which statistics are core and which recommendations are extension-layer outputs.",
            "Add a local feature flag boundary for recommendation and adaptive-practice modules.",
            "Define rollback behavior when analytics extension code fails.",
        ],
        acceptance_criteria=[
            "Core answer submission works when recommendation flags are disabled.",
            "Analytics failures do not corrupt canonical attempts or question-bank records.",
            "Tests cover at least one disabled-extension path.",
        ],
        safety_limits=[
            "Do not make core practice depend on AI recommendation availability.",
            "Do not store generated strategy as canonical evidence.",
            "Keep extension outputs traceable to attempt and wrongbook events.",
        ],
        evidence_refs=["系统改革与刷题计划.docx#阶段4"],
        risk_level="safe",
    ),
)


def _contract_gap_candidates(repo: Repository) -> list[CodexLoopCandidate]:
    contract_path = repo.root / "docs" / "practice_ui_api_contract.md"
    if not contract_path.exists():
        return []
    return [
        CodexLoopCandidate(
            candidate_id="phase-3-safe-question-display-endpoint",
            title="Implement safe practice question display endpoint from UI contract",
            source="contract_gap",
            phase="3-frontend-prototype",
            layer="Decision",
            priority=86,
            expected_outputs=[
                "Add a session-scoped question display endpoint for practice UI use.",
                "Return prompt, choices, learner state, note count, and favorite state before submission.",
                "Keep answer, explanation, and correct-answer fields hidden from display payloads.",
            ],
            acceptance_criteria=[
                "Display endpoint returns 404 or 422 for missing sessions or mismatched question IDs.",
                "Pre-submission payload includes prompt and choices but excludes answer/explanation fields.",
                "Post-submission display reflects answered/noted/favorited state without exposing canonical answers.",
            ],
            safety_limits=[
                "Do not duplicate display payloads into practice session metadata.",
                "Do not expose answer, correct_answer, explanation, rationale, or hidden diagnostics.",
                "Do not change frontend routes until backend contract tests pass.",
            ],
            evidence_refs=["docs/practice_ui_api_contract.md#Question Display"],
            risk_level="guarded",
        )
    ]


def _runtime_gap_candidates(repo: Repository) -> list[CodexLoopCandidate]:
    candidates: list[CodexLoopCandidate] = []
    attempts_router = repo.root / ATTEMPTS_ROUTER_PATH
    if attempts_router.exists():
        text = attempts_router.read_text(encoding="utf-8")
        if '"status": "screenshot_saved"' in text and '"suggested_payload"' in text:
            candidates.append(
                CodexLoopCandidate(
                    candidate_id="gap-screenshot-structured-extraction",
                    title="Replace screenshot placeholder flow with structured extraction handoff",
                    source="runtime_gap",
                    phase="capture-screenshot",
                    layer="Capture",
                    priority=96,
                    expected_outputs=[
                        "Create a local structured extraction artifact for screenshot uploads instead of returning only a placeholder payload.",
                        "Preserve raw image evidence and mark uncertain fields explicitly instead of guessing LOS or conclusions.",
                        "Keep the extraction handoff traceable so a later agent step can complete record-mistake safely.",
                    ],
                    acceptance_criteria=[
                        "Screenshot upload returns a durable extraction draft reference, not only a generic saved status.",
                        "Draft output stores evidence path plus clearly empty or uncertain fields when the image cannot support them.",
                        "Tests cover safe filename handling and the structured handoff contract.",
                    ],
                    safety_limits=[
                        "Do not hallucinate LOS, source, choices, or correct answers from unclear screenshots.",
                        "Do not delete or rewrite the original screenshot evidence asset.",
                        "Do not claim full AI extraction unless the workflow persists an explicit draft artifact.",
                    ],
                    evidence_refs=[
                        "apps/api/routers/attempts.py",
                        "docs/research/product-audit-report.md#G1",
                        "AGENTS.md",
                    ],
                    risk_level="guarded",
                )
            )
    auth_router = repo.root / AUTH_ROUTER_PATH
    if not auth_router.exists():
        candidates.append(
            CodexLoopCandidate(
                candidate_id="gap-admin-auth-boundary",
                title="Add local auth scaffold and admin boundary for private question-bank APIs",
                source="runtime_gap",
                phase="1-environment-data-model",
                layer="Decision",
                priority=94,
                expected_outputs=[
                    "Create local bootstrap/login/session/logout endpoints for development-safe auth.",
                    "Protect admin-only question-bank import and review routes with explicit role checks.",
                    "Write security audit events for bootstrap, login, logout, and denied access.",
                ],
                acceptance_criteria=[
                    "Admin bootstrap and login succeed through API tests.",
                    "Anonymous access to private import/review routes returns 401.",
                    "Authorized admin access preserves existing import/review behavior.",
                ],
                safety_limits=[
                    "Do not add remote auth dependencies or secrets for the local-first MVP.",
                    "Do not break learner-facing practice endpoints while adding admin boundaries.",
                    "Keep auth state explicit and auditable in local storage.",
                ],
                evidence_refs=[
                    "docs/research/product-audit-report.md#G8",
                    "apps/api/routers/question_banks.py",
                    "AGENTS.md",
                ],
                risk_level="guarded",
            )
        )
    frontend_api = repo.root / FRONTEND_API_PATH
    if auth_router.exists() and frontend_api.exists():
        frontend_text = frontend_api.read_text(encoding="utf-8")
        if "/api/auth/" not in frontend_text:
            candidates.append(
                CodexLoopCandidate(
                    candidate_id="gap-auth-ui-session-integration",
                    title="Expose local auth session and admin entry flow in the frontend",
                    source="runtime_gap",
                    phase="3-frontend-prototype",
                    layer="Projection",
                    priority=82,
                    expected_outputs=[
                        "Add frontend API helpers for bootstrap-admin, login, logout, and session lookup.",
                        "Create a minimal admin auth entry surface so protected import/review tools have a session path.",
                        "Keep learner practice flow separate from admin import/review flow.",
                    ],
                    acceptance_criteria=[
                        "Frontend API layer includes auth session helpers.",
                        "Admin-facing UI can create or resume a session without touching learner practice pages.",
                        "Tests or deterministic checks confirm the admin auth surface is wired to the local API.",
                    ],
                    safety_limits=[
                        "Do not block anonymous learner practice until a broader auth migration is planned.",
                        "Do not mix admin import controls into learner-only panels.",
                        "Keep the first UI step local-only and explicit about development scope.",
                    ],
                    evidence_refs=[
                        "apps/api/routers/auth.py",
                        "apps/web/src/lib/api.ts",
                        "docs/research/product-audit-report.md#G8",
                    ],
                    risk_level="safe",
                )
            )
    security_router = repo.root / SECURITY_ROUTER_PATH
    security_page = repo.root / SECURITY_PAGE_PATH
    security_events = repo.root / ".system" / "events" / "security" / "security-events.jsonl"
    if auth_router.exists() and security_events.exists() and (not security_router.exists() or not security_page.exists()):
        candidates.append(
            CodexLoopCandidate(
                candidate_id="gap-security-audit-visibility",
                title="Expose security audit events for local admin review",
                source="runtime_gap",
                phase="resources-management-safety",
                layer="Projection",
                priority=78,
                expected_outputs=[
                    "Add a read-only API endpoint for recent security/auth audit events.",
                    "Create a small review surface so admins can inspect bootstrap/login/logout and denied-access traces.",
                    "Keep the endpoint admin-only and local-first.",
                ],
                acceptance_criteria=[
                    "Admin-authenticated API requests can list recent security events.",
                    "Frontend review page renders recent events without mixing them into learner views.",
                    "Tests or deterministic checks prove the endpoint/page wiring works.",
                ],
                safety_limits=[
                    "Do not expose security audit events to anonymous or learner-only flows.",
                    "Do not store raw passwords, secrets, or session tokens in the page output.",
                    "Keep the first version read-only.",
                ],
                evidence_refs=[
                    ".system/events/security/security-events.jsonl",
                    "apps/api/routers/auth.py",
                    "AGENTS.md",
                ],
                risk_level="safe",
            )
        )
    question_bank_console = repo.root / QUESTION_BANK_CONSOLE_PATH
    if auth_router.exists() and question_bank_console.exists():
        console_text = question_bank_console.read_text(encoding="utf-8")
        if "/review/admin-auth" not in console_text:
            candidates.append(
                CodexLoopCandidate(
                    candidate_id="gap-import-console-admin-guidance",
                    title="Make question-bank import console aware of admin session requirements",
                    source="runtime_gap",
                    phase="3-frontend-prototype",
                    layer="Projection",
                    priority=74,
                    expected_outputs=[
                        "Show explicit admin-session guidance inside the question-bank import console.",
                        "Surface 401/403 failures as actionable prompts instead of silent loading failures.",
                        "Link import/review operators to the admin auth page without affecting learner practice.",
                    ],
                    acceptance_criteria=[
                        "Import console displays a clear path to `/review/admin-auth` when no admin session is active.",
                        "Protected API failures produce a readable UI state instead of disappearing silently.",
                        "Learner-facing practice screens remain unchanged.",
                    ],
                    safety_limits=[
                        "Do not require admin auth for learner-only screens.",
                        "Do not expose session tokens in the UI.",
                        "Keep the first pass focused on guidance, not a full auth redesign.",
                    ],
                    evidence_refs=[
                        "apps/web/src/components/capture/QuestionBankImportConsole.tsx",
                        "apps/web/src/app/review/admin-auth/page.tsx",
                    ],
                    risk_level="safe",
                )
            )
        if 'type="file"' not in console_text and "import_qbank_excel.py" in console_text:
            candidates.append(
                CodexLoopCandidate(
                    candidate_id="gap-import-console-file-bridge",
                    title="Add CSV/XLSX file bridge to the question-bank import console",
                    source="runtime_gap",
                    phase="1-environment-data-model",
                    layer="Projection",
                    priority=73,
                    expected_outputs=[
                        "Add a file picker flow for CSV/XLSX import guidance in the admin question-bank console.",
                        "Bridge the frontend to an existing local import path instead of forcing raw JSON paste only.",
                        "Keep the imported-question immutability and admin-session rules intact.",
                    ],
                    acceptance_criteria=[
                        "Console clearly supports choosing a CSV/XLSX file or shows the exact local import path workflow.",
                        "The UI no longer implies JSON paste is the only realistic admin import route.",
                        "Typecheck or deterministic verification confirms the new flow compiles.",
                    ],
                    safety_limits=[
                        "Do not bypass admin auth or question-bank validation rules.",
                        "Do not invent remote upload storage when the repo still uses local-first import.",
                        "Keep the first pass scoped to a bridge, not a full ingestion redesign.",
                    ],
                    evidence_refs=[
                        "apps/web/src/components/capture/QuestionBankImportConsole.tsx",
                        "scripts/import_qbank_excel.py",
                    ],
                    risk_level="safe",
            )
            )
    capture_page = repo.root / CAPTURE_PAGE_PATH
    if capture_page.exists():
        capture_text = capture_page.read_text(encoding="utf-8")
        if "/api/attempts/batch-import" not in capture_text and "batch import" not in capture_text.lower():
            candidates.append(
                CodexLoopCandidate(
                    candidate_id="gap-capture-batch-import-ui",
                    title="Expose batch attempt import in the capture workflow",
                    source="runtime_gap",
                    phase="1-environment-data-model",
                    layer="Projection",
                    priority=72,
                    expected_outputs=[
                        "Add a batch import surface to Question Capture for multiple attempts or mistake records.",
                        "Bridge the UI to the existing batch-import API instead of keeping it API-only.",
                        "Keep single-question manual capture and screenshot capture intact.",
                    ],
                    acceptance_criteria=[
                        "Capture UI exposes a clear batch import path.",
                        "The batch import route is no longer hidden behind direct API usage only.",
                        "Typecheck or deterministic verification confirms the added UI compiles.",
                    ],
                    safety_limits=[
                        "Do not disrupt the existing manual or screenshot capture flow.",
                        "Do not invent remote file storage if the first pass can use pasted JSON.",
                        "Keep the first version minimal and local-first.",
                    ],
                    evidence_refs=[
                        "apps/web/src/app/capture/page.tsx",
                        "apps/api/routers/attempts.py",
                        "docs/research/product-audit-report.md#G15",
                    ],
                    risk_level="safe",
                )
            )
    mock_router = repo.root / MOCK_ROUTER_PATH
    if mock_router.exists():
        mock_text = mock_router.read_text(encoding="utf-8")
        if 'next_strategy = "下次 mock 前 24 小时' in mock_text:
            candidates.append(
                CodexLoopCandidate(
                    candidate_id="gap-pre-mock-brief-personalization",
                    title="Personalize pre-mock brief and next-strategy from recent weak signals",
                    source="runtime_gap",
                    phase="4-analytics-extensions",
                    layer="Decision",
                    priority=71,
                    expected_outputs=[
                        "Use recent question/bias patterns to surface focus topics in the pre-mock brief.",
                        "Replace fixed next-strategy copy with signal-aware guidance.",
                        "Keep the change local-first and traceable to events.",
                    ],
                    acceptance_criteria=[
                        "Pre-mock brief response includes current weak-topic or weak-error context when evidence exists.",
                        "Mock retro next-strategy is no longer a single hard-coded sentence for every learner.",
                        "Tests or deterministic checks prove the route now uses local evidence.",
                    ],
                    safety_limits=[
                        "Do not fabricate weakness claims without supporting events.",
                        "Keep the first pass heuristic and transparent, not opaque AI scoring.",
                        "Preserve the existing mock routes and payload compatibility.",
                    ],
                    evidence_refs=[
                        "apps/api/routers/mock.py",
                        "docs/research/product-audit-report.md#G10",
                    ],
                    risk_level="safe",
                )
            )
    return candidates


def _check_enabled(repo: Repository) -> None:
    if not FeatureFlags.load(repo.root).enabled("codex_self_loop_enabled"):
        raise RuntimeError("codex_self_loop_enabled feature flag is disabled")


def _loop_memory_root(repo: Repository) -> Path:
    path = repo.root / LOOP_MEMORY_DIR
    path.mkdir(parents=True, exist_ok=True)
    (repo.root / LOOP_COMPLETION_DIR).mkdir(parents=True, exist_ok=True)
    return path


def _completed_candidate_ids(repo: Repository) -> set[str]:
    completed: set[str] = set()
    for event in repo.load_jsonl_events(LOOP_EVENT_STREAM):
        if event.get("event_type") == "codex.loop.completed" and event.get("candidate_id"):
            completed.add(str(event["candidate_id"]))
    completion_dir = repo.root / LOOP_COMPLETION_DIR
    if completion_dir.exists():
        for path in completion_dir.glob("*.json"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            candidate_id = str(payload.get("candidate_id") or path.stem)
            completed.add(candidate_id)
    return completed


def _proposal_candidates(repo: Repository) -> list[CodexLoopCandidate]:
    candidates: list[CodexLoopCandidate] = []
    for proposal in load_upgrade_proposals(repo.root):
        if proposal.status not in {"proposed", "approved", "open"}:
            continue
        candidates.append(
            CodexLoopCandidate(
                candidate_id=f"proposal-{proposal.proposal_id}",
                title=proposal.title,
                source="skill_upgrade_proposal",
                phase="skill-self-improvement",
                layer="Decision",
                priority=95,
                expected_outputs=list(proposal.requested_changes),
                acceptance_criteria=list(proposal.acceptance_criteria),
                safety_limits=list(proposal.limits),
                evidence_refs=[proposal.proposal_id, *proposal.reflection_ids],
                risk_level="guarded",
                requires_human=False,
            )
        )
    return candidates


def collect_codex_loop_candidates(repo: Repository) -> list[CodexLoopCandidate]:
    completed = _completed_candidate_ids(repo)
    candidates = [
        SELF_CYCLE_BOOTSTRAP,
        *_proposal_candidates(repo),
        *_runtime_gap_candidates(repo),
        *_contract_gap_candidates(repo),
        *PLAN_PHASE_CANDIDATES,
    ]
    return [candidate for candidate in candidates if candidate.candidate_id not in completed]


def _risk_rank(candidate: CodexLoopCandidate) -> int:
    return {"safe": 0, "guarded": 1, "blocked": 2}.get(candidate.risk_level, 3)


def select_codex_loop_candidate(
    candidates: list[CodexLoopCandidate],
    *,
    mode: str = "unattended",
) -> CodexLoopCandidate | None:
    eligible = []
    for candidate in candidates:
        if candidate.requires_human:
            continue
        if mode == "unattended" and candidate.risk_level == "blocked":
            continue
        eligible.append(candidate)
    if not eligible:
        return None
    return sorted(eligible, key=lambda item: (-item.priority, _risk_rank(item), item.candidate_id))[0]


def _next_loop_number(root: Path) -> int:
    existing = sorted(root.glob("ITER-*.json"))
    if not existing:
        return 1
    numbers = []
    for path in existing:
        match = re.match(r"ITER-(\d+)\.json$", path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def _next_task_number(repo: Repository) -> int:
    task_root = repo.root / TASK_DIR
    existing = sorted(task_root.glob("TASK-*.md"))
    numbers = []
    for path in existing:
        match = re.match(r"TASK-(\d+)\.md$", path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def _write_task_markdown(repo: Repository, loop_id: str, candidate: CodexLoopCandidate | None) -> str:
    if candidate is None:
        return ""
    task_root = repo.root / TASK_DIR
    task_root.mkdir(parents=True, exist_ok=True)
    task_number = _next_task_number(repo)
    path = task_root / f"TASK-{task_number:03d}.md"
    lines = [
        f"# TASK-{task_number:03d}",
        "",
        "## Goal",
        candidate.title,
        "",
        "## Why This Is Next",
        f"- loop_id: {loop_id}",
        f"- candidate_id: {candidate.candidate_id}",
        f"- source: {candidate.source}",
        f"- phase: {candidate.phase}",
        f"- layer: {candidate.layer}",
        "",
        "## Outputs",
        *[f"- {item}" for item in candidate.expected_outputs],
        "",
        "## Acceptance",
        *[f"- {item}" for item in candidate.acceptance_criteria],
        "",
        "## Safety Limits",
        *[f"- {item}" for item in candidate.safety_limits],
        "",
        "## Evidence",
        *[f"- {item}" for item in candidate.evidence_refs],
    ]
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return str(path.relative_to(repo.root)).replace("\\", "/")


def _render_plan_markdown(plan: CodexLoopPlan) -> str:
    selected = plan.selected
    lines = [
        "---",
        f"loop_id: {plan.loop_id}",
        f"generated_at: {plan.generated_at}",
        f"mode: {plan.mode}",
        f"status: {plan.status}",
        "---",
        "",
        "# Codex Self-Cycle Plan",
        "",
    ]
    if selected:
        lines.extend(
            [
                "## Selected Next Work",
                f"- candidate_id: {selected.candidate_id}",
                f"- title: {selected.title}",
                f"- phase: {selected.phase}",
                f"- layer: {selected.layer}",
                f"- risk_level: {selected.risk_level}",
                f"- task_path: {plan.task_path}",
                "",
                "## Expected Outputs",
                *[f"- {item}" for item in selected.expected_outputs],
                "",
                "## Acceptance",
                *[f"- {item}" for item in selected.acceptance_criteria],
                "",
                "## Safety Limits",
                *[f"- {item}" for item in selected.safety_limits],
            ]
        )
    else:
        lines.extend(
            [
                "## Selected Next Work",
                "No eligible candidate was found. The autonomous loop should stop instead of inventing work.",
            ]
        )
    lines.extend(
        [
            "",
            "## Stop Conditions",
            *[f"- {item}" for item in plan.stop_conditions],
            "",
            "## Impact Controls",
            *[f"- {item}" for item in plan.impact_controls],
            "",
            "## Candidates Considered",
        ]
    )
    for candidate in plan.candidates_considered:
        lines.append(
            f"- {candidate.candidate_id} | {candidate.priority} | {candidate.risk_level} | {candidate.title}"
        )
    return "\n".join(lines).strip() + "\n"


def plan_codex_loop(repo: Repository, *, mode: str = "unattended", max_candidates: int = 8) -> CodexLoopPlan:
    _check_enabled(repo)
    root = _loop_memory_root(repo)
    loop_number = _next_loop_number(root)
    loop_id = f"ITER-{loop_number:03d}"
    candidates = collect_codex_loop_candidates(repo)
    selected = select_codex_loop_candidate(candidates, mode=mode)
    task_path = _write_task_markdown(repo, loop_id, selected)
    considered = sorted(candidates, key=lambda item: (-item.priority, _risk_rank(item), item.candidate_id))[
        :max_candidates
    ]
    json_path = root / f"{loop_id}.json"
    markdown_path = root / f"{loop_id}.md"
    plan = CodexLoopPlan(
        loop_id=loop_id,
        mode=mode,
        selected=selected,
        candidates_considered=considered,
        task_path=task_path,
        plan_json_path=str(json_path.relative_to(repo.root)).replace("\\", "/"),
        plan_markdown_path=str(markdown_path.relative_to(repo.root)).replace("\\", "/"),
        stop_conditions=[
            "No eligible non-human candidate remains.",
            "The same blocker repeats for three consecutive goal turns.",
            "A task would modify locked question-bank content, secrets, destructive filesystem state, or remote GitHub refs.",
            "Targeted verification cannot be run or replaced by an explicit verification note.",
        ],
        impact_controls=[
            "Prefer Capture/Memory/Decision Layer changes before Projection changes.",
            "Write plan and completion events before selecting the next task.",
            "Keep core brushing-question flow stable; put recommendations and analytics behind extension boundaries.",
            "Use tests or deterministic validation before marking work complete.",
        ],
    )
    markdown_path.write_text(_render_plan_markdown(plan), encoding="utf-8")
    json_path.write_text(json.dumps(plan.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    repo.append_jsonl_event(
        LOOP_EVENT_STREAM,
        {
            "event_type": "codex.loop.planned",
            "loop_id": loop_id,
            "candidate_id": selected.candidate_id if selected else "",
            "task_path": task_path,
            "mode": mode,
            "created_at": plan.generated_at,
        },
    )
    return plan


def complete_codex_loop_candidate(
    repo: Repository,
    *,
    candidate_id: str,
    summary: str,
    artifacts: list[str] | None = None,
    verification: str = "",
) -> Path:
    _check_enabled(repo)
    _loop_memory_root(repo)
    if not candidate_id.strip():
        raise ValueError("candidate_id is required")
    if not summary.strip():
        raise ValueError("summary is required")
    payload = {
        "event_type": "codex.loop.completed",
        "candidate_id": candidate_id.strip(),
        "summary": summary.strip(),
        "artifacts": artifacts or [],
        "verification": verification.strip(),
        "created_at": _now(),
    }
    payload["event_id"] = stable_id("codex-loop-complete", candidate_id, summary)
    completion_path = repo.root / LOOP_COMPLETION_DIR / f"{candidate_id}.json"
    completion_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    repo.append_jsonl_event(LOOP_EVENT_STREAM, payload)
    return completion_path
