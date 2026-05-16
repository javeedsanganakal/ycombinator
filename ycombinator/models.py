from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Company:
    """A single Y Combinator company record from yc-oss/api."""

    name: str = ""
    slug: str = ""
    batch: str = ""
    status: str = ""
    industry: str = ""
    subindustry: str = ""
    one_liner: str = ""
    long_description: str = ""
    website: str = ""
    team_size: int | None = None
    location: str = ""
    regions: list[str] = field(default_factory=list)
    stage: str = ""
    url: str = ""
    tags: list[str] = field(default_factory=list)
    # Anything yc-oss adds later lands here so we don't silently drop fields.
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Company":
        known = {f for f in cls.__dataclass_fields__ if f != "extra"}
        kwargs: dict[str, Any] = {}
        extra: dict[str, Any] = {}
        for key, value in raw.items():
            if key in known:
                kwargs[key] = value
            else:
                extra[key] = value
        kwargs["extra"] = extra
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        extra = data.pop("extra", {}) or {}
        data.update(extra)
        return data
