from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests

API_BASE = "https://yc-oss.github.io/api"
META_URL = f"{API_BASE}/meta.json"
ALL_URL = f"{API_BASE}/companies/all.json"
OSS_REPOS_URL = "https://raw.githubusercontent.com/yc-oss/open-source-companies/main/repositories.json"
DEFAULT_DATA_DIR = Path("data")
DEFAULT_SPLIT_DIR = Path("yc-companies")
DEFAULT_MIRROR_DIR = Path("yc-oss-mirror")
CACHE_TTL_SECONDS = 24 * 60 * 60

_BATCH_RE = re.compile(r"^(winter|summer|spring|fall|w|s|x)\s*(\d{2}|\d{4})$", re.IGNORECASE)
_SEASON_ALIASES = {"w": "winter", "s": "summer", "x": "fall"}


def _get_json(url: str, retries: int = 1, timeout: int = 30) -> Any:
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(1.0)
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


def _is_fresh(path: Path, ttl: int = CACHE_TTL_SECONDS) -> bool:
    if not path.exists():
        return False
    return (time.time() - path.stat().st_mtime) < ttl


def fetch_meta(data_dir: Path = DEFAULT_DATA_DIR) -> dict[str, Any]:
    """Fetch the yc-oss metadata index (lists batches, industries, tags)."""
    meta = _get_json(META_URL)
    _write_json(Path(data_dir) / "meta.json", meta)
    return meta


def fetch_all(
    data_dir: Path = DEFAULT_DATA_DIR,
    force: bool = False,
    split: bool = True,
    split_dir: Path = DEFAULT_SPLIT_DIR,
) -> list[dict]:
    """Fetch every YC company. Cached for 24h unless force=True.

    If `split` is True, also writes one pretty JSON file per company under
    `split_dir/<year>-<season>/<slug>.json` for git-diff-friendly storage.
    """
    out = Path(data_dir) / "all.json"
    if not force and _is_fresh(out):
        print(f"Using cached {out} (<24h old). Pass force=True to refresh.")
        with out.open(encoding="utf-8") as fh:
            companies = json.load(fh)
    else:
        start = time.time()
        companies = _get_json(ALL_URL)
        elapsed = time.time() - start
        _write_json(out, companies)
        print(f"Fetched {len(companies):,} companies in {elapsed:.1f}s → {out}")

    if split:
        split_by_batch(companies, split_dir=split_dir)
    return companies


def split_by_batch(
    companies: list[dict],
    split_dir: Path = DEFAULT_SPLIT_DIR,
    clean: bool = True,
) -> dict[str, int]:
    """Write one pretty JSON file per company under split_dir/<batch>/<slug>.json.

    If `clean` is True, removes any pre-existing files in split_dir so renamed
    or removed companies don't linger.
    """
    split_dir = Path(split_dir)
    if clean and split_dir.exists():
        for path in split_dir.rglob("*.json"):
            path.unlink()

    counts: dict[str, int] = {}
    for company in companies:
        batch_slug = _batch_slug(company.get("batch") or "")
        slug = (company.get("slug") or "").strip() or _fallback_slug(company)
        if not slug:
            continue
        target = split_dir / batch_slug / f"{slug}.json"
        _write_json(target, company)
        counts[batch_slug] = counts.get(batch_slug, 0) + 1

    total = sum(counts.values())
    print(f"Split {total:,} companies into {len(counts)} batch folders under {split_dir}/")
    return counts


def _batch_slug(batch: str) -> str:
    """Normalize 'Winter 2021' → '2021-winter', 'W21' → '2021-winter'."""
    batch = (batch or "").strip()
    if not batch:
        return "unbatched"
    match = _BATCH_RE.match(batch)
    if not match:
        return "unbatched"
    season, year = match.group(1).lower(), match.group(2)
    season = _SEASON_ALIASES.get(season, season)
    if len(year) == 2:
        # YC's short codes: 05-99 → 19xx? In practice all YC batches are 2005+,
        # so any 2-digit year maps to 2000+. (S05 is the earliest batch.)
        year = f"20{year}"
    return f"{year}-{season}"


def _fallback_slug(company: dict) -> str:
    name = (company.get("name") or "").strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-")


def fetch_batch(slug: str, data_dir: Path = DEFAULT_DATA_DIR) -> list[dict]:
    payload = _get_json(f"{API_BASE}/batches/{slug}.json")
    out = Path(data_dir) / "batches" / f"{slug}.json"
    _write_json(out, payload)
    print(f"Fetched {len(payload):,} companies from batch '{slug}' → {out}")
    return payload


def fetch_industry(slug: str, data_dir: Path = DEFAULT_DATA_DIR) -> list[dict]:
    payload = _get_json(f"{API_BASE}/industries/{slug}.json")
    out = Path(data_dir) / "industries" / f"{slug}.json"
    _write_json(out, payload)
    print(f"Fetched {len(payload):,} companies in industry '{slug}' → {out}")
    return payload


def fetch_tag(slug: str, data_dir: Path = DEFAULT_DATA_DIR) -> list[dict]:
    payload = _get_json(f"{API_BASE}/tags/{slug}.json")
    out = Path(data_dir) / "tags" / f"{slug}.json"
    _write_json(out, payload)
    print(f"Fetched {len(payload):,} companies with tag '{slug}' → {out}")
    return payload


def fetch_mirror(
    mirror_dir: Path = DEFAULT_MIRROR_DIR,
    workers: int = 16,
) -> dict[str, int]:
    """Mirror every endpoint exposed by yc-oss/api into mirror_dir/, plus the
    open-source-companies repositories list. Returns a count per category.

    Layout:
        mirror_dir/meta.json
        mirror_dir/companies/{all,top,hiring,...}.json
        mirror_dir/batches/{winter-2021,...}.json
        mirror_dir/industries/{fintech,...}.json
        mirror_dir/tags/{ai,...}.json
        mirror_dir/open-source-companies/repositories.json
    """
    mirror_dir = Path(mirror_dir)
    start = time.time()

    meta = _get_json(META_URL)
    _write_json(mirror_dir / "meta.json", meta)

    jobs: list[tuple[str, Path]] = []
    for category in ("companies", "batches", "industries", "tags"):
        entries = meta.get(category) or {}
        if isinstance(entries, dict):
            iterable = entries.items()
        else:
            iterable = ((item.get("slug"), item) for item in entries if item.get("slug"))
        for slug, entry in iterable:
            url = entry.get("api") if isinstance(entry, dict) else None
            if not url or not slug:
                continue
            jobs.append((url, mirror_dir / category / f"{slug}.json"))

    # open-source-companies (separate repo)
    jobs.append((OSS_REPOS_URL, mirror_dir / "open-source-companies" / "repositories.json"))

    counts = {"meta": 1}
    failed: list[tuple[str, str]] = []

    def _one(url: str, target: Path) -> tuple[str, Path, Exception | None]:
        try:
            payload = _get_json(url)
            _write_json(target, payload)
            return url, target, None
        except Exception as exc:  # noqa: BLE001
            return url, target, exc

    print(f"Mirroring {len(jobs)} files from yc-oss/api into {mirror_dir}/ ...")
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_one, url, target) for url, target in jobs]
        for fut in as_completed(futures):
            url, target, err = fut.result()
            done += 1
            if err is not None:
                failed.append((url, str(err)))
            else:
                category = target.parent.name
                counts[category] = counts.get(category, 0) + 1
            if done % 50 == 0 or done == len(jobs):
                print(f"  {done}/{len(jobs)} fetched")

    elapsed = time.time() - start
    summary = ", ".join(f"{k}={v}" for k, v in counts.items())
    print(f"Mirror complete in {elapsed:.1f}s — {summary}")
    if failed:
        print(f"  WARNING: {len(failed)} URLs failed:")
        for url, err in failed[:10]:
            print(f"    {url}: {err}")
    return counts
