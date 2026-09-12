from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .models import Company
from .scraper import DEFAULT_DATA_DIR, fetch_all


class YCData:
    """In-memory query layer over the cached YC company list."""

    def __init__(self, companies: list[Company]):
        self.companies = companies

    # ---------- loading ----------

    @classmethod
    def load(cls, data_dir: Path = DEFAULT_DATA_DIR, auto_fetch: bool = True) -> "YCData":
        path = Path(data_dir) / "all.json"
        if not path.exists():
            if not auto_fetch:
                raise FileNotFoundError(
                    f"{path} not found. Run `ycombinator fetch all` first."
                )
            fetch_all(data_dir=data_dir)
        with path.open(encoding="utf-8") as fh:
            raw = json.load(fh)
        return cls([Company.from_dict(item) for item in raw])

    # ---------- filtering ----------

    def filter(
        self,
        batch: str | None = None,
        industry: str | None = None,
        subindustry: str | None = None,
        status: str | None = None,
        stage: str | None = None,
        tags: Iterable[str] | None = None,
        region: str | None = None,
    ) -> "YCData":
        results = self.companies
        if batch:
            results = [c for c in results if _ieq(c.batch, batch)]
        if industry:
            results = [c for c in results if _ieq(c.industry, industry)]
        if subindustry:
            results = [c for c in results if _ieq(c.subindustry, subindustry)]
        if status:
            results = [c for c in results if _ieq(c.status, status)]
        if stage:
            results = [c for c in results if _ieq(c.stage, stage)]
        if tags:
            wanted = {t.lower() for t in tags}
            results = [
                c for c in results
                if wanted.issubset({(t or "").lower() for t in (c.tags or [])})
            ]
        if region:
            r = region.lower()
            results = [
                c for c in results
                if any(r == (x or "").lower() for x in (c.regions or []))
            ]
        return YCData(results)

    # ---------- search ----------

    def search(self, query: str) -> "YCData":
        """Case-insensitive substring match on name + one_liner."""
        q = query.lower()
        results = [
            c for c in self.companies
            if q in (c.name or "").lower() or q in (c.one_liner or "").lower()
        ]
        return YCData(results)

    def get(self, slug: str) -> Company | None:
        for c in self.companies:
            if c.slug == slug:
                return c
        return None

    # ---------- stats ----------

    def stats(self) -> dict[str, Any]:
        return {
            "total": len(self.companies),
            "by_status": dict(Counter(c.status for c in self.companies if c.status).most_common()),
            "by_batch": dict(Counter(c.batch for c in self.companies if c.batch).most_common(20)),
            "by_industry": dict(Counter(c.industry for c in self.companies if c.industry).most_common(20)),
        }

    # ---------- convenience ----------

    def __len__(self) -> int:
        return len(self.companies)

    def __iter__(self):
        return iter(self.companies)

    def to_list(self) -> list[dict]:
        return [c.to_dict() for c in self.companies]


def _ieq(a: str | None, b: str | None) -> bool:
    return (a or "").strip().lower() == (b or "").strip().lower()
