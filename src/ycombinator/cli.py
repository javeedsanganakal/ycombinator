from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from .agent import build_report, report_markdown
from .query import YCData
from .roles import write_role_index
from .scraper import (
    DEFAULT_DATA_DIR,
    DEFAULT_MIRROR_DIR,
    DEFAULT_SPLIT_DIR,
    fetch_all,
    fetch_batch,
    fetch_industry,
    fetch_meta,
    fetch_mirror,
    fetch_tag,
    split_by_batch,
)


def _meta(data_dir: Path) -> dict:
    path = data_dir / "meta.json"
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    return fetch_meta(data_dir)


def cmd_fetch(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    target = args.target
    if target == "all":
        fetch_all(
            data_dir=data_dir,
            force=args.force,
            split=not args.no_split,
            split_dir=Path(args.split_dir),
        )
    elif target == "batch":
        fetch_batch(args.slug, data_dir=data_dir)
    elif target == "industry":
        fetch_industry(args.slug, data_dir=data_dir)
    elif target == "tag":
        fetch_tag(args.slug, data_dir=data_dir)
    elif target == "meta":
        fetch_meta(data_dir=data_dir)
    elif target == "mirror":
        fetch_mirror(mirror_dir=Path(args.mirror_dir), workers=args.workers)
    return 0


def cmd_split(args: argparse.Namespace) -> int:
    """Re-split datasets/cache/all.json without re-fetching."""
    path = Path(args.data_dir) / "all.json"
    if not path.exists():
        print(f"{path} not found. Run `ycombinator fetch all` first.", file=sys.stderr)
        return 1
    with path.open(encoding="utf-8") as fh:
        companies = json.load(fh)
    split_by_batch(companies, split_dir=Path(args.split_dir), clean=not args.no_clean)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    meta = _meta(data_dir)
    key = args.kind  # batches | industries | tags
    items = meta.get(key) or meta.get(key.rstrip("s")) or []
    # yc-oss meta entries usually look like {"name": "...", "slug": "...", "count": N}
    if items and isinstance(items[0], dict):
        for item in items:
            name = item.get("name") or item.get("slug") or ""
            slug = item.get("slug") or ""
            count = item.get("count")
            count_str = f" ({count})" if count is not None else ""
            print(f"{slug:40s}  {name}{count_str}")
    else:
        for item in items:
            print(item)
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    data = YCData.load(data_dir=Path(args.data_dir))
    print(json.dumps(data.stats(), indent=2))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    data = YCData.load(data_dir=Path(args.data_dir)).search(args.query)
    return _print_companies(data, args.limit, as_json=args.json, empty_query=args.query)


def cmd_filter(args: argparse.Namespace) -> int:
    data = YCData.load(data_dir=Path(args.data_dir)).filter(
        batch=args.batch,
        industry=args.industry,
        subindustry=args.subindustry,
        status=args.status,
        stage=args.stage,
        tags=args.tags,
        region=args.region,
    )
    if args.query:
        data = data.search(args.query)
    return _print_companies(data, args.limit, as_json=args.json)


def _print_companies(
    data: YCData,
    limit: int,
    *,
    as_json: bool = False,
    empty_query: str | None = None,
) -> int:
    if not len(data):
        if empty_query:
            print(f"No companies match '{empty_query}'.")
        else:
            print("No companies match the selected filters.")
        return 0

    selected = list(data)[:limit]
    if as_json:
        print(json.dumps([c.to_dict() for c in selected], indent=2, ensure_ascii=False))
        return 0

    for c in selected:
        print(f"{c.slug:40s} {(c.batch or ''):18s} {c.name}")
        if c.one_liner:
            print(f"  → {c.one_liner}")
    if len(data) > limit:
        print(f"...and {len(data) - limit} more. Use --limit to see more.")
    return 0


def search_markdown(query: str, roots: Iterable[Path]) -> list[dict[str, object]]:
    """Return contextual, line-level matches from Markdown files under roots."""
    needle = query.casefold()
    matches: list[dict[str, object]] = []
    seen: set[Path] = set()
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        paths = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for path in paths:
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            heading = ""
            with path.open(encoding="utf-8", errors="replace") as fh:
                for lineno, raw in enumerate(fh, 1):
                    line = raw.strip()
                    if line.startswith("#"):
                        heading = line.lstrip("#").strip()
                    if needle in line.casefold():
                        matches.append({
                            "path": str(path),
                            "line": lineno,
                            "heading": heading,
                            "text": line,
                        })
    return matches


def cmd_kb_search(args: argparse.Namespace) -> int:
    roots = [Path(args.kb_dir)]
    if args.include_lectures:
        roots.append(Path(args.lectures_dir))
    matches = search_markdown(args.query, roots)
    selected = matches[:args.limit]
    if args.json:
        print(json.dumps(selected, indent=2, ensure_ascii=False))
        return 0
    if not selected:
        print(f"No knowledge-base entries match '{args.query}'.")
        return 0
    for match in selected:
        context = f" — {match['heading']}" if match["heading"] else ""
        print(f"{match['path']}:{match['line']}{context}")
        print(f"  {match['text']}")
    if len(matches) > args.limit:
        print(f"...and {len(matches) - args.limit} more. Use --limit to see more.")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    data = YCData.load(data_dir=Path(args.data_dir))
    company = data.get(args.slug)
    if not company:
        print(f"No company with slug '{args.slug}'.", file=sys.stderr)
        return 1
    print(json.dumps(company.to_dict(), indent=2, ensure_ascii=False))
    return 0


def cmd_agent(args: argparse.Namespace) -> int:
    report = build_report(Path(args.root))
    if args.format == "json":
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    else:
        rendered = report_markdown(report)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


def cmd_role_index(args: argparse.Namespace) -> int:
    index = write_role_index(
        companies_path=Path(args.companies_path),
        json_path=Path(args.json_path),
        markdown_path=Path(args.markdown_path),
    )
    print(f"Indexed {index['company_count']:,} companies across {len(index['roles'])} roles.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ycombinator",
        description="Fetch and query the Y Combinator company directory (data from yc-oss/api).",
    )
    parser.add_argument(
        "--data-dir", default=str(DEFAULT_DATA_DIR),
        help="Where to read/write JSON files (default: ./datasets/cache)",
    )
    parser.add_argument(
        "--split-dir", default=str(DEFAULT_SPLIT_DIR),
        help="Where to write per-company batch files (default: ./datasets/yc-companies)",
    )
    parser.add_argument(
        "--mirror-dir", default=str(DEFAULT_MIRROR_DIR),
        help="Where to write the full yc-oss mirror (default: ./datasets/yc-oss-mirror)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # fetch
    p_fetch = sub.add_parser("fetch", help="Download YC data")
    fetch_sub = p_fetch.add_subparsers(dest="target", required=True)
    p_all = fetch_sub.add_parser("all", help="All companies in the current upstream snapshot")
    p_all.add_argument("--force", action="store_true", help="Bypass 24h cache")
    p_all.add_argument(
        "--no-split", action="store_true",
        help="Skip writing per-company files under --split-dir",
    )
    fetch_sub.add_parser("meta", help="Index of batches/industries/tags")
    p_mirror = fetch_sub.add_parser(
        "mirror",
        help="Mirror every yc-oss/api endpoint (~448 files) into --mirror-dir",
    )
    p_mirror.add_argument(
        "--workers", type=int, default=16,
        help="Parallel HTTP workers (default: 16)",
    )
    for kind in ("batch", "industry", "tag"):
        p = fetch_sub.add_parser(kind, help=f"One {kind} by slug (e.g. winter-2024, fintech, ai)")
        p.add_argument("slug")
    p_fetch.set_defaults(func=cmd_fetch)

    # split
    p_split = sub.add_parser(
        "split", help="Re-split cached company data into per-company files",
    )
    p_split.add_argument(
        "--no-clean", action="store_true",
        help="Don't delete existing split files first (default: clean)",
    )
    p_split.set_defaults(func=cmd_split)

    # list
    p_list = sub.add_parser("list", help="List available batches/industries/tags from meta")
    p_list.add_argument("kind", choices=["batches", "industries", "tags"])
    p_list.set_defaults(func=cmd_list)

    # stats
    sub.add_parser("stats", help="Summary counts").set_defaults(func=cmd_stats)

    # search
    p_search = sub.add_parser("search", help="Full-text search across public company fields")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=25)
    p_search.add_argument("--json", action="store_true", help="Print selected records as JSON")
    p_search.set_defaults(func=cmd_search)

    # structured company filtering
    p_filter = sub.add_parser("filter", help="Filter companies by structured fields")
    p_filter.add_argument("--batch")
    p_filter.add_argument("--industry")
    p_filter.add_argument("--subindustry")
    p_filter.add_argument("--status")
    p_filter.add_argument("--stage")
    p_filter.add_argument("--tag", dest="tags", action="append", help="Require tag; repeat for AND filtering")
    p_filter.add_argument("--region")
    p_filter.add_argument("--query", help="Also require a full-text match")
    p_filter.add_argument("--limit", type=int, default=25)
    p_filter.add_argument("--json", action="store_true", help="Print selected records as JSON")
    p_filter.set_defaults(func=cmd_filter)

    # repository knowledge-base search
    p_kb = sub.add_parser("kb-search", help="Search local startup Markdown knowledge")
    p_kb.add_argument("query")
    p_kb.add_argument("--kb-dir", default="startup-library")
    p_kb.add_argument("--include-lectures", action="store_true")
    p_kb.add_argument("--lectures-dir", default="vendor/how-to-start-a-startup")
    p_kb.add_argument("--limit", type=int, default=25)
    p_kb.add_argument("--json", action="store_true", help="Print matches as JSON")
    p_kb.set_defaults(func=cmd_kb_search)

    # show
    p_show = sub.add_parser("show", help="Pretty-print a single company by slug")
    p_show.add_argument("slug")
    p_show.set_defaults(func=cmd_show)

    # autonomous repository health heartbeat
    p_agent = sub.add_parser("agent", help="Run the startup knowledge-base health agent once")
    p_agent.add_argument("--root", default=".", help="Repository root (default: current directory)")
    p_agent.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_agent.add_argument("--output", help="Write the report to a file instead of stdout")
    p_agent.set_defaults(func=cmd_agent)

    # role-based YC discovery map
    p_roles = sub.add_parser("role-index", help="Map YC companies to startup roles from public descriptions")
    p_roles.add_argument("--companies-path", default="datasets/yc-oss-mirror/companies/all.json")
    p_roles.add_argument("--json-path", default="datasets/yc-role-index.json")
    p_roles.add_argument("--markdown-path", default="datasets/yc-role-index.md")
    p_roles.set_defaults(func=cmd_role_index)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
