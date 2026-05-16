from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

API_BASE = "https://yc-oss.github.io/api"
META_URL = f"{API_BASE}/meta.json"
ALL_URL = f"{API_BASE}/companies/all.json"
DEFAULT_DATA_DIR = Path("data")
CACHE_TTL_SECONDS = 24 * 60 * 60


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


def fetch_all(data_dir: Path = DEFAULT_DATA_DIR, force: bool = False) -> list[dict]:
    """Fetch every YC company. Cached for 24h unless force=True."""
    out = Path(data_dir) / "all.json"
    if not force and _is_fresh(out):
        print(f"Using cached {out} (<24h old). Pass force=True to refresh.")
        with out.open(encoding="utf-8") as fh:
            return json.load(fh)

    start = time.time()
    companies = _get_json(ALL_URL)
    elapsed = time.time() - start
    _write_json(out, companies)
    print(f"Fetched {len(companies):,} companies in {elapsed:.1f}s → {out}")
    return companies


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
