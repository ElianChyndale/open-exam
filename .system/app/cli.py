from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from app.storage import Repository
from app.workflows import daily_review_pack, load_payload, mine_patterns, moc_gap_review, post_mock_retro, pre_mock_brief, record_event, refresh_learning_outputs, write_todo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cfa-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("record-mistake", "review-session", "audit-agent"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--payload", required=True)

    subparsers.add_parser("mine-patterns")
    subparsers.add_parser("moc-gap-review")
    subparsers.add_parser("pre-mock-brief")

    review = subparsers.add_parser("daily-review-pack")
    review.add_argument("--date", default="")
    review.add_argument("--days-back", type=int, default=7)
    review.add_argument("--max-items", type=int, default=20)
    review.add_argument("--focus-topic", default="")

    todo = subparsers.add_parser("write-todo")
    todo.add_argument("--payload", required=True)

    retro = subparsers.add_parser("post-mock-retro")
    retro.add_argument("--session-id", required=True)

    return parser


def run_cli(argv: list[str] | None = None, repo_root: Path | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = Repository(repo_root or Path.cwd())

    if args.command in {"record-mistake", "review-session", "audit-agent"}:
        event = record_event(repo, load_payload(args.payload), args.command)
        if event.source_layer == "question":
            mine_patterns(repo)
            moc_gap_review(repo)
        refresh_learning_outputs(repo)
        return 0
    if args.command == "mine-patterns":
        mine_patterns(repo)
        moc_gap_review(repo)
        refresh_learning_outputs(repo)
        return 0
    if args.command == "moc-gap-review":
        moc_gap_review(repo)
        refresh_learning_outputs(repo)
        return 0
    if args.command == "pre-mock-brief":
        pre_mock_brief(repo)
        return 0
    if args.command == "daily-review-pack":
        review_date = date.fromisoformat(args.date) if args.date else None
        daily_review_pack(repo, review_date, args.days_back, args.max_items, args.focus_topic)
        return 0
    if args.command == "write-todo":
        write_todo(repo, load_payload(args.payload))
        return 0
    if args.command == "post-mock-retro":
        post_mock_retro(repo, args.session_id)
        return 0
    parser.error(f"unsupported command: {args.command}")
    return 2
