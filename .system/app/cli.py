from __future__ import annotations

import argparse
import json
import os
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

    for command in ("daily-review", "daily-review-pack"):
        review = subparsers.add_parser(command)
        review.add_argument("--date", default="")
        review.add_argument("--days-back", type=int, default=7)
        review.add_argument("--max-items", type=int, default=20)
        review.add_argument("--focus-topic", default="")
        review.add_argument("--knowledge-depth", choices=("standard", "expanded"), default="standard")
        review.add_argument("--energy-level", type=int, default=-1, choices=range(0, 5),
                            help="当前精力水平 0-4，默认自动从最近打卡获取")

    complete_review = subparsers.add_parser("complete-daily-review")
    complete_review.add_argument("--review-id", required=True)

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

    subparsers.add_parser("weekly-focus", help="生成本周学习重点建议")
    subparsers.add_parser("rebuild-catalog", help="从 JSONL 重建 SQLite 查询索引")
    subparsers.add_parser("migrate-catalog", help="升级 SQLite 查询索引 schema")
    subparsers.add_parser("knowledge-status", help="显示知识点的记忆状态（含衰减风险）")
    subparsers.add_parser("decay-knowledge", help="扫描知识点状态并衰减超期未复习项")

    sync_push = subparsers.add_parser("sync-push", help="导出全部学习数据到文件")
    sync_push.add_argument("--output", default="examos-backup.json", help="导出文件路径")

    sync_pull = subparsers.add_parser("sync-pull", help="从文件导入学习数据")
    sync_pull.add_argument("--input", required=True, help="导入文件路径")

    subparsers.add_parser("list-profiles", help="列出可用考试类型")

    profile_cmd = subparsers.add_parser("set-profile")
    profile_cmd.add_argument("--name", required=True, help="考试类型 short name (cfa-l1, frm-p1, ...)")
    profile_cmd.add_argument("--path", default="", help="自定义 profile 文件路径")

    print_cmd = subparsers.add_parser("print-cards", help="生成可打印复习卡 PDF")
    print_cmd.add_argument("--topic", default="", help="筛选 Topic")
    print_cmd.add_argument("--limit", type=int, default=20, help="最多卡片数")
    print_cmd.add_argument("--output", default="", help="输出 PDF 路径")

    return parser


def run_cli(argv: list[str] | None = None, repo_root: Path | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = Repository(repo_root or Path.cwd())

    if args.command in {"record-mistake", "review-session", "audit-agent"}:
        if args.command == "record-mistake":
            from app.workflows import record_question_attempt
            event = record_question_attempt(repo, load_payload(args.payload))["event"]
        else:
            event = record_event(repo, load_payload(args.payload), args.command)
        if event is None:
            return 0
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
    if args.command in {"daily-review", "daily-review-pack"}:
        review_date = date.fromisoformat(args.date) if args.date else None
        energy = args.energy_level if args.energy_level >= 0 else None
        daily_review_pack(repo, review_date, args.days_back, args.max_items, args.focus_topic, args.knowledge_depth, energy_level=energy)
        return 0
    if args.command == "complete-daily-review":
        from app.workflows import complete_daily_review
        result = complete_daily_review(repo, args.review_id)
        print(f"✅ Daily Review 已完成: {result['review_id']}")
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
        from app.workflows import record_question_attempt
        record_question_attempt(repo, payload)
        print(f"✅ 已记录: {topic} | {los} | {args.error_type}")
        return 0
    if args.command == "review":
        from app.workflows import daily_review_pack as review_cmd_pack
        path = review_cmd_pack(repo, date.today(), args.days_back, 20, args.focus_topic)
        print(f"📖 复习资料已生成: {path}")
        print("在 CFA_tier1/dashboard/Daily Review.md 查看")
        return 0
    if args.command == "import-qbank":
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
        try:
            date.fromisoformat(args.date)
        except ValueError:
            print("ERROR: 日期格式错误，请使用 YYYY-MM-DD", file=sys.stderr)
            return 1
        exam_path = repo.root / ".system" / "exam_date.txt"
        exam_path.write_text(args.date, encoding="utf-8")
        print(f"✅ 考试日期已设置为 {args.date}")
        return 0
    if args.command == "weekly-focus":
        from app.workflows import weekly_focus_recommendation
        result = weekly_focus_recommendation(repo)
        print(result)
        print(f"\n📄 已保存到 .system/memory/strategy/")
        return 0

    if args.command == "rebuild-catalog":
        print(repo.rebuild_catalog())
        return 0

    if args.command == "migrate-catalog":
        print(repo.migrate_catalog())
        return 0

    if args.command == "knowledge-status":
        from study_science.knowledge_memory import KnowledgeMemoryEngine
        overlay_path = repo.memory_root / "review" / "knowledge-status.json"
        if not overlay_path.exists():
            print("No knowledge-status.json found. Complete a daily review first.")
            return 0
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        kp = overlay.get("knowledge_points", {})
        if not kp:
            print("No knowledge points tracked yet.")
            return 0
        print(f"Knowledge Memory Status ({len(kp)} points)")
        print(f"{'State':<20} {'Subject':<25} {'Heading':<40} {'Next Review':<15} {'Decay Risk'}")
        print("-" * 120)
        for kid, entry in sorted(kp.items()):
            state = entry.get("status", "?")
            subj = entry.get("subject", "")[:24]
            head = entry.get("heading", "")[:39]
            next_rev = (entry.get("next_review_at", "") or "")[:10]
            risk = entry.get("decay_risk", "?")
            print(f"{state:<20} {subj:<25} {head:<40} {next_rev:<15} {risk}")
        return 0

    if args.command == "decay-knowledge":
        from study_science.knowledge_memory import KnowledgeMemoryEngine
        overlay_path = repo.memory_root / "review" / "knowledge-status.json"
        if not overlay_path.exists():
            print("No knowledge-status.json found.")
            return 0
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        engine = KnowledgeMemoryEngine()
        overlay, decayed = engine.decay_sweep(overlay, date.today())
        if decayed:
            overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ Decayed {len(decayed)} overdue knowledge points:")
            for kid in decayed:
                print(f"  - {kid}")
        else:
            print("No knowledge points needed decay.")
        return 0

    if args.command == "list-profiles":
        from app.exam_profile import list_available_profiles
        profiles = list_available_profiles()
        print(f"可用考试类型 ({len(profiles)}):")
        for p in profiles:
            print(f"  {p['short_name']}: {p['name']} ({p['subject_count']} subjects)")
        print("\n设置考试类型: python scripts/cfa.py set-profile --name cfa-l1")
        return 0

    if args.command == "set-profile":
        from app.exam_profile import load_profile, set_profile
        profile = load_profile(args.name)
        # Save to .system/active_profile.txt
        profile_path = repo.root / ".system" / "active_profile.txt"
        profile_path.write_text(args.name, encoding="utf-8")
        print(f"考试类型已切换为: {profile.name}")
        print(f"   科目数: {len(profile.subjects)}")
        print(f"   及格线: {profile.passing_score}%")
        # Set environment for current session
        os.environ["EXAMOS_PROFILE"] = args.name
        set_profile(profile)
        return 0

    if args.command == "sync-push":
        from app.sync_service import push_to_file
        push_to_file(repo, args.output)
        print(f"📁 保存至: {args.output}")
        return 0

    if args.command == "sync-pull":
        from app.sync_service import pull_from_file
        try:
            counts = pull_from_file(repo, args.input)
            print(f"📁 来源: {args.input}")
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        return 0

    if args.command == "print-cards":
        from app.card_printer import generate_print_cards
        try:
            path = generate_print_cards(repo, args.topic, args.limit, args.output or None)
            print(f"✅ 已生成复习卡 PDF: {path}")
        except ImportError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            print("请先安装: pip install reportlab", file=sys.stderr)
            return 1
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2
