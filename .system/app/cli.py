from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

from app.storage import Repository
from app.workflows import daily_review_pack, load_payload, mine_patterns, moc_gap_review, post_mock_retro, pre_mock_brief, record_event, record_progress, refresh_learning_outputs, write_todo


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
    review.add_argument("--knowledge-depth", choices=("standard", "expanded"), default="standard")

    progress = subparsers.add_parser("record-progress")
    progress.add_argument("--payload", required=True)

    todo = subparsers.add_parser("write-todo")
    todo.add_argument("--payload", required=True)

    retro = subparsers.add_parser("post-mock-retro")
    retro.add_argument("--session-id", required=True)

    fast = subparsers.add_parser("fast", help="快速录入: topic|LOS|wrong|correct [--error-type TYPE] [--confidence N]")
    fast.add_argument("record", help="topic|LOS|wrong|correct 管道分隔格式")
    fast.add_argument("--error-type", default="concept_confusion", choices=(
        "concept_confusion", "formula_misuse", "knowledge_gap",
        "careless_reading", "time_pressure", "prompt_misread",
        "constraint_miss", "constructed_response_weak_structure",
    ))
    fast.add_argument("--confidence", type=int, default=2, choices=range(0, 5))
    fast.add_argument("--time", type=int, default=120, help="时间花费（秒）")

    review_cmd = subparsers.add_parser("review", help="打开今日复习资料")
    review_cmd.add_argument("--focus-topic", default="")
    review_cmd.add_argument("--days-back", type=int, default=7)

    review = subparsers.add_parser("mark-reviewed")
    review.add_argument("--card-id", required=True)
    review.add_argument("--outcome", required=True, choices=("recalled", "struggled", "forgot"))
    review.add_argument("--confidence-after", type=int, default=0)

    import_cmd = subparsers.add_parser("import-qbank", help="批量导入错题")
    import_cmd.add_argument("--file", required=True, help="JSONL 文件路径")
    import_cmd.add_argument("--source", default="qbank-import", help="来源标签")

    set_exam = subparsers.add_parser("set-exam")
    set_exam.add_argument("--date", required=True, help="考试日期 YYYY-MM-DD")

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
        daily_review_pack(repo, review_date, args.days_back, args.max_items, args.focus_topic, args.knowledge_depth)
        return 0
    if args.command == "record-progress":
        record_progress(repo, load_payload(args.payload))
        return 0
    if args.command == "write-todo":
        write_todo(repo, load_payload(args.payload))
        return 0
    if args.command == "post-mock-retro":
        post_mock_retro(repo, args.session_id)
        return 0
    if args.command == "mark-reviewed":
        from app.workflows import mark_card_reviewed
        mark_card_reviewed(repo, args.card_id, args.outcome, args.confidence_after)
        print(f"✅ 已更新复习记录: {args.card_id}")
        return 0
    if args.command == "fast":
        parts = [p.strip() for p in args.record.split("|")]
        if len(parts) < 4:
            print("ERROR: 需要至少 4 段: topic|LOS|wrong|correct", file=sys.stderr)
            return 1
        topic, los, wrong, correct = parts[0], parts[1], parts[2], parts[3]
        payload = {
            "source_layer": "question",
            "topic": topic,
            "los": los,
            "prompt_or_question": f"Quick capture: {topic}/{los}",
            "wrong_choice_or_output": wrong,
            "correct_resolution": correct,
            "error_type": args.error_type,
            "confidence": args.confidence,
            "time_spent": args.time,
            "evidence_refs": [f"quick-capture-{datetime.now().isoformat()}"],
        }
        from app.workflows import record_event as fast_record_event
        fast_record_event(repo, payload, "record-mistake")
        print(f"✅ 已记录: {topic} | {los} | {args.error_type}")
        return 0
    if args.command == "review":
        from app.workflows import daily_review_pack as review_cmd_pack
        path = review_cmd_pack(repo, date.today(), args.days_back, 20, args.focus_topic)
        print(f"📖 复习资料已生成: {path}")
        print("在 CFA_tier1/dashboard/今日复习资料.md 查看")
        return 0
    if args.command == "import-qbank":
        import json
        path = Path(args.file)
        if not path.exists():
            print(f"ERROR: 文件不存在 {path}", file=sys.stderr)
            return 1
        payloads = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                payloads.append(json.loads(line))
        from app.workflows import batch_import_events
        ids = batch_import_events(repo, payloads, args.source)
        print(f"✅ 已导入 {len(ids)} 道错题")
        return 0
    if args.command == "set-exam":
        from datetime import date
        try:
            date.fromisoformat(args.date)
        except ValueError:
            print("ERROR: 日期格式错误，请使用 YYYY-MM-DD", file=sys.stderr)
            return 1
        exam_path = repo.root / ".system" / "exam_date.txt"
        exam_path.write_text(args.date, encoding="utf-8")
        print(f"✅ 考试日期已设置为 {args.date}")
        return 0
    parser.error(f"unsupported command: {args.command}")
    return 2
