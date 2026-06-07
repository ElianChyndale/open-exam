"""Assistant Drawer Service — lightweight intent router for the global AI drawer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AssistantIntent:
    workflow: str
    reason: str


class AssistantDrawerService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def handle_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        message = str(payload.get("message") or "").strip()
        lowered = message.lower()

        if lowered.startswith("open ") or "review lab" in lowered:
            return {
                "intent": AssistantIntent("quick-command", "navigation request").__dict__,
                "assistant_reply": {
                    "kind": "action_result",
                    "text": "Opening Review Lab.",
                },
                "action": {
                    "action_type": "open_route",
                    "status": "completed",
                    "summary": "Opened Review Lab.",
                    "launch_route": "/review/lab",
                },
            }

        if any(token in lowered for token in ("explain", "step by step", "ba ii", "calculator")):
            from study_science.tutor import TutorService

            answer = TutorService(self.repo.root).ask(
                profile_id="default",
                mode="formula_help",
                query=message,
                context_node_id=None,
            )
            return {
                "intent": AssistantIntent("tutor", "grounded explanation request").__dict__,
                "assistant_reply": {
                    "kind": "tutor_answer",
                    "text": answer["answer"],
                },
                "action": {
                    "action_type": "tutor_answer",
                    "status": "completed",
                    "summary": "Generated grounded tutor answer.",
                    "launch_route": "/review/tutor",
                },
                "conversation": answer.get("conversation"),
            }

        if "wrong" in lowered or "got this" in lowered:
            has_question = "question:" in lowered or "prompt:" in lowered
            has_correct = "correct answer:" in lowered or "correct resolution:" in lowered
            has_wrong = "wrong answer:" in lowered or "%" in lowered

            if not (has_question and has_correct and has_wrong):
                return {
                    "intent": AssistantIntent("record-mistake", "insufficient capture evidence").__dict__,
                    "assistant_reply": {
                        "kind": "follow_up",
                        "question": "Paste the question or upload the screenshot.",
                    },
                    "action": None,
                }

            from app.workflows import record_question_attempt

            result = record_question_attempt(
                self.repo,
                {
                    "topic": "Financial Statement Analysis",
                    "los": "FSA.2.2",
                    "prompt_or_question": message,
                    "wrong_choice_or_output": "captured-from-chat",
                    "correct_resolution": "captured-from-chat",
                    "error_type": "concept_confusion",
                    "confidence": 2,
                    "time_spent": 60,
                    "evidence_refs": ["assistant-drawer"],
                    "question_source": "assistant_drawer",
                    "source_type": "chat",
                    "is_correct": False,
                },
            )
            return {
                "intent": AssistantIntent("record-mistake", "question error evidence").__dict__,
                "assistant_reply": {
                    "kind": "action_result",
                    "text": "Recorded this as question evidence.",
                },
                "action": {
                    "action_type": "record_mistake",
                    "status": "completed",
                    "summary": f"Recorded mistake {result['attempt_id']}.",
                    "attempt_id": result["attempt_id"],
                    "card_id": result["card_id"],
                },
            }

        return {
            "intent": AssistantIntent("tutor", "fallback conversational support").__dict__,
            "assistant_reply": {
                "kind": "follow_up",
                "question": "Tell me whether you want capture, tutor help, review guidance, or a quick command.",
            },
            "action": None,
        }
