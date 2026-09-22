from __future__ import annotations

import html
import json
import re
import time
from pathlib import Path
from typing import Any, Callable

import requests


DEFAULT_COMPANIES_PATH = Path("datasets/yc-oss-mirror/companies/all.json")
DEFAULT_JSON_PATH = Path("datasets/yc-founders-index.json")
DEFAULT_MARKDOWN_PATH = Path("datasets/yc-founders-index.md")
PROFILE_USER_AGENT = "ycombinator-startup-kb/0.1 (public research index)"


def _profile_founders(page: str) -> list[dict[str, Any]]:
    """Extract the public founders payload embedded in a YC profile page."""
    decoded = html.unescape(page)
    marker = '"founders":'
    position = decoded.find(marker)
    if position < 0:
        raise ValueError("YC profile did not contain a founders payload")
    payload, _ = json.JSONDecoder().raw_decode(decoded[position + len(marker):])
    if not isinstance(payload, list):
        raise ValueError("YC founders payload was not a list")
    fields = ("full_name", "title", "founder_bio", "twitter_url", "linkedin_url", "latest_yc_company")
    result: list[dict[str, Any]] = []
    for founder in payload:
        if not isinstance(founder, dict) or not founder.get("full_name"):
            continue
        result.append({field: founder.get(field) or "" for field in fields})
    return result


def fetch_founders(url: str, *, timeout: float = 30) -> list[dict[str, Any]]:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": PROFILE_USER_AGENT})
    response.raise_for_status()
    return _profile_founders(response.text)


def build_founder_index(
    companies: list[dict[str, Any]],
    *,
    fetcher: Callable[[str], list[dict[str, Any]]] = fetch_founders,
    delay: float = 0.2,
) -> dict[str, Any]:
    """Build a public founder directory for YC's explicitly flagged top companies.

    ``top_company`` is an upstream YC directory field, not a claim that these
    founders are objectively the world's best. Keeping that boundary explicit
    makes the index useful for research without turning it into a ranking.
    """
    selected = [company for company in companies if company.get("top_company")]
    records: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for number, company in enumerate(selected):
        slug = str(company.get("slug") or "").strip()
        profile_url = str(company.get("url") or f"https://www.ycombinator.com/companies/{slug}")
        record = {
            "slug": slug,
            "name": company.get("name") or slug,
            "batch": company.get("batch") or "",
            "status": company.get("status") or "",
            "industry": company.get("industry") or "",
            "one_liner": company.get("one_liner") or "",
            "website": company.get("website") or "",
            "yc_profile_url": profile_url,
            "top_company": True,
            "founders": [],
            "fetch_status": "ok",
        }
        try:
            record["founders"] = fetcher(profile_url)
        except Exception as exc:  # preserve partial progress for the daily job
            record["fetch_status"] = "error"
            errors.append({"slug": slug, "url": profile_url, "error": str(exc)})
        records.append(record)
        if delay and number < len(selected) - 1:
            time.sleep(delay)
    records.sort(key=lambda item: (str(item["batch"]), str(item["name"]).casefold()), reverse=True)
    return {
        "schema_version": 1,
        "source": "official YC company profile pages",
        "selection": "companies where the YC directory sets top_company=true",
        "selection_note": "This is an upstream YC category, not an independent ranking of founder quality.",
        "company_count": len(records),
        "founder_count": sum(len(record["founders"]) for record in records),
        "error_count": len(errors),
        "companies": records,
        "errors": errors,
    }


def write_founder_index(
    companies_path: Path = DEFAULT_COMPANIES_PATH,
    json_path: Path = DEFAULT_JSON_PATH,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    *,
    delay: float = 0.2,
) -> dict[str, Any]:
    with Path(companies_path).open(encoding="utf-8") as handle:
        companies = json.load(handle)
    if not isinstance(companies, list):
        raise ValueError(f"Expected a list in {companies_path}")
    index = build_founder_index(companies, delay=delay)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_founder_index(index), encoding="utf-8")
    return index


def render_founder_index(index: dict[str, Any]) -> str:
    lines = [
        "# YC top-company founder index",
        "",
        f"Companies: {index['company_count']} | Public founders found: {index['founder_count']} | Fetch errors: {index['error_count']}",
        "",
        "This directory joins the local YC company mirror to public founder fields on official YC company profile pages. The selection follows YC's `top_company=true` field. That field is useful for discovery, but it is not an independent ranking or a claim that these are the world's best founders.",
        "",
        "Use the JSON file when you need bios or social links. Review the source profile before contacting anyone.",
        "",
    ]
    for company in index["companies"]:
        founders = company["founders"]
        names = ", ".join(
            founder["full_name"] + (f" ({founder['title']})" if founder["title"] else "")
            for founder in founders
        ) or "No public founder record returned"
        lines.append(f"## [{company['name']}]({company['yc_profile_url']})")
        lines.append("")
        lines.append(f"{company['batch'] or 'Unbatched'} | {company['status'] or 'Status unavailable'} | {company['industry'] or 'Industry unavailable'}")
        lines.append("")
        lines.append(f"{company['one_liner'] or 'No one-liner in the source record.'}")
        lines.append("")
        lines.append(f"Founders: {names}")
        lines.append("")
    if index["errors"]:
        lines.extend(["## Refresh errors", "", "Some profile pages could not be read during the last refresh:", ""])
        lines.extend(f"- `{error['slug']}`: {error['error']}" for error in index["errors"])
        lines.append("")
    return "\n".join(lines)
