from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit


_MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    summary: str
    details: tuple[str, ...] = ()


def _markdown_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    top_level = root / "README.md"
    if top_level.exists():
        paths.append(top_level)
    for directory in ("startup-library", "skills", "datasets"):
        target = root / directory
        if target.exists():
            paths.extend(sorted(target.rglob("*.md")))
    return paths


def check_internal_links(root: Path) -> CheckResult:
    broken: list[str] = []
    checked = 0
    for markdown in _markdown_files(root):
        text = markdown.read_text(encoding="utf-8", errors="replace")
        for match in _MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1).strip()
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1]
            target = raw_target.split(maxsplit=1)[0]
            parts = urlsplit(target)
            if parts.scheme or target.startswith(("#", "mailto:")):
                continue
            path_text = unquote(parts.path)
            if not path_text:
                continue
            checked += 1
            resolved = (markdown.parent / path_text).resolve()
            if not resolved.exists():
                relative = markdown.relative_to(root)
                broken.append(f"{relative} -> {target}")

    if broken:
        return CheckResult(
            "internal-links",
            "fail",
            f"{len(broken)} broken internal link(s) out of {checked}",
            tuple(broken[:50]),
        )
    return CheckResult("internal-links", "pass", f"{checked} internal links resolve")


def _read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_json_files(root: Path) -> CheckResult:
    targets = [root / "datasets" / "yc-companies", root / "datasets" / "yc-oss-mirror"]
    files = [path for target in targets if target.exists() for path in target.rglob("*.json")]
    failures: list[str] = []
    for path in files:
        try:
            _read_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{path.relative_to(root)}: {exc}")
    if failures:
        return CheckResult(
            "json-integrity",
            "fail",
            f"{len(failures)} invalid JSON file(s) out of {len(files)}",
            tuple(failures[:50]),
        )
    return CheckResult("json-integrity", "pass", f"{len(files)} JSON files parse")


def check_company_dataset(root: Path) -> CheckResult:
    split_dir = root / "datasets" / "yc-companies"
    mirror_file = root / "datasets" / "yc-oss-mirror" / "companies" / "all.json"
    if not split_dir.exists() or not mirror_file.exists():
        return CheckResult(
            "company-dataset",
            "fail",
            "tracked company dataset or mirror is missing",
        )

    mirror = _read_json(mirror_file)
    if not isinstance(mirror, list):
        return CheckResult("company-dataset", "fail", "mirror companies/all.json is not a list")

    mirror_slugs = {item.get("slug") for item in mirror if isinstance(item, dict) and item.get("slug")}
    split_files = list(split_dir.rglob("*.json"))
    split_slugs = {path.stem for path in split_files}
    missing = sorted(mirror_slugs - split_slugs)
    extra = sorted(split_slugs - mirror_slugs)
    duplicate_count = len(split_files) - len(split_slugs)
    details = [f"missing split record: {slug}" for slug in missing[:25]]
    details.extend(f"extra split record: {slug}" for slug in extra[:25])
    if duplicate_count:
        details.append(f"duplicate split filenames: {duplicate_count}")
    if details:
        return CheckResult(
            "company-dataset",
            "fail",
            f"mirror={len(mirror_slugs)}, split={len(split_files)}; datasets differ",
            tuple(details),
        )
    return CheckResult(
        "company-dataset",
        "pass",
        f"{len(mirror_slugs)} mirrored companies match {len(split_files)} split records",
    )


def build_report(root: Path, checks: Iterable[CheckResult] | None = None) -> dict[str, object]:
    selected = list(checks) if checks is not None else [
        check_internal_links(root),
        check_json_files(root),
        check_company_dataset(root),
    ]
    return {
        "status": "pass" if all(check.status == "pass" for check in selected) else "fail",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": str(root.resolve()),
        "checks": [asdict(check) for check in selected],
    }


def report_markdown(report: dict[str, object]) -> str:
    icon = "✅" if report["status"] == "pass" else "❌"
    lines = [f"# Startup KB Agent {icon}", "", f"Status: **{report['status']}**", ""]
    for check in report["checks"]:  # type: ignore[assignment]
        result = check  # type: ignore[assignment]
        marker = "✅" if result["status"] == "pass" else "❌"
        lines.append(f"- {marker} **{result['name']}** — {result['summary']}")
        for detail in result.get("details", []):
            lines.append(f"  - `{detail}`")
    return "\n".join(lines) + "\n"
