from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .query import YCData
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
    """Re-split data/all.json into per-company files without re-fetching."""
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
    if not len(data):
        print(f"No companies match '{args.query}'.")
        return 0
    for c in list(data)[: args.limit]:
        print(f"{c.slug:40s} {c.batch:8s} {c.name}")
        if c.one_liner:
            print(f"  → {c.one_liner}")
    if len(data) > args.limit:
        print(f"...and {len(data) - args.limit} more. Use --limit to see more.")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    data = YCData.load(data_dir=Path(args.data_dir))
    company = data.get(args.slug)
    if not company:
        print(f"No company with slug '{args.slug}'.", file=sys.stderr)
        return 1
    print(json.dumps(company.to_dict(), indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ycombinator",
        description="Fetch and query the Y Combinator company directory (data from yc-oss/api).",
    )
    parser.add_argument(
        "--data-dir", default=str(DEFAULT_DATA_DIR),
        help="Where to read/write JSON files (default: ./data)",
    )
    parser.add_argument(
        "--split-dir", default=str(DEFAULT_SPLIT_DIR),
        help="Where to write per-company batch files (default: ./yc-companies)",
    )
    parser.add_argument(
        "--mirror-dir", default=str(DEFAULT_MIRROR_DIR),
        help="Where to write the full yc-oss mirror (default: ./yc-oss-mirror)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # fetch
    p_fetch = sub.add_parser("fetch", help="Download YC data")
    fetch_sub = p_fetch.add_subparsers(dest="target", required=True)
    p_all = fetch_sub.add_parser("all", help="All ~5,900 companies")
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
        "split", help="Re-split cached data/all.json into per-company files",
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
    p_search = sub.add_parser("search", help="Full-text search on name + one_liner")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=25)
    p_search.set_defaults(func=cmd_search)

    # show
    p_show = sub.add_parser("show", help="Pretty-print a single company by slug")
    p_show.add_argument("slug")
    p_show.set_defaults(func=cmd_show)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
