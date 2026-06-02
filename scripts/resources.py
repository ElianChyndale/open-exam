from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT / ".system",
    ROOT / "packages" / "learning-records" / "src",
    ROOT / "packages" / "resource-ingestion" / "src",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.resource_workflows import (  # noqa: E402
    build_script_discovery_url,
    create_subscription,
    crawl_resource_url,
    discover_resource_urls,
    discover_resources_ai,
    list_providers,
    rebuild_resource_index,
    run_due_subscriptions,
    run_resource_audit,
    scheduler_status,
)
from app.storage import Repository  # noqa: E402


def _print(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenExam ResourceOS public-resource ingestion CLI.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("providers")

    crawl = commands.add_parser("crawl")
    crawl.add_argument("--lane", choices=["language", "cfa"], required=True)
    crawl.add_argument("--url", required=True)
    crawl.add_argument("--provider", default="generic_web")
    crawl.add_argument("--license-mode", default="metadata_only")
    crawl.add_argument("--title", default="")
    crawl.add_argument("--language", default="")
    crawl.add_argument("--topic", default="")
    crawl.add_argument("--answer-bearing", action="store_true")

    discover = commands.add_parser("discover")
    discover.add_argument("--lane", choices=["language", "cfa"], required=True)
    discover.add_argument("--mode", choices=["script", "ai"], default="script")
    discover.add_argument("--provider", default="generic_web")
    discover.add_argument("--query", default="")
    discover.add_argument("--url", default="")
    discover.add_argument("--max-cost", type=float, default=1.0)

    subscribe = commands.add_parser("subscribe")
    subscribe.add_argument("--provider", required=True)
    subscribe.add_argument("--lane", choices=["language", "cfa"], required=True)
    subscribe.add_argument("--url", required=True)
    subscribe.add_argument("--schedule", default="0 */6 * * *")
    subscribe.add_argument("--budget", type=int, default=50)

    due = commands.add_parser("run-due")
    due.add_argument("--scheduled", action="store_true")

    audit = commands.add_parser("audit")
    audit.add_argument("--scope", choices=["content", "runtime", "code"], required=True)

    commands.add_parser("rebuild-index")
    commands.add_parser("scheduler-status")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo = Repository(ROOT)
    if args.command == "providers":
        _print({"providers": list_providers()})
    elif args.command == "crawl":
        _print(asyncio.run(crawl_resource_url(repo, **{key: value for key, value in vars(args).items() if key != "command"})))
    elif args.command == "discover":
        if args.mode == "ai":
            _print(discover_resources_ai(repo, lane=args.lane, query=args.query, max_cost=args.max_cost))
        else:
            target = args.url or build_script_discovery_url(args.provider, args.query)
            _print({"mode": "script", "provider": args.provider, "urls": asyncio.run(discover_resource_urls(args.provider, target))})
    elif args.command == "subscribe":
        _print(create_subscription(repo, lane=args.lane, provider=args.provider, target=args.url, schedule=args.schedule, budget=args.budget))
    elif args.command == "run-due":
        _print(asyncio.run(run_due_subscriptions(repo)))
    elif args.command == "audit":
        _print(run_resource_audit(repo, scope=args.scope))
    elif args.command == "rebuild-index":
        _print(rebuild_resource_index(repo))
    elif args.command == "scheduler-status":
        _print(scheduler_status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
