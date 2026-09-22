from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROLE_RULES: dict[str, tuple[str, ...]] = {
    "founders": (
        "founder", "cofounder", "entrepreneur", "startup", "small business",
        "business owner", "company building", "owners",
    ),
    "product": (
        "product manager", "product team", "product analytics", "product development",
        "product workflow", "product operations", "roadmap", "workflow", "platform",
    ),
    "ux-ui": (
        "user experience", "ux", "ui", "interface", "design", "designer",
        "frontend", "front-end", "creative tools",
    ),
    "engineering": (
        "engineer", "engineering", "developer", "software", "coding", "code",
        "api", "sdk", "infrastructure", "devops", "cloud", "data pipeline",
        "robotics", "machine learning", "developer tools",
    ),
    "sales": (
        "sales", "go-to-market", "gtm", "revenue", "crm", "outbound", "pipeline",
        "prospecting", "business development", "lead generation", "account executive",
    ),
    "marketing": (
        "marketing", "growth", "content", "search engine", "seo", "advertising",
        "brand", "social media", "customer acquisition", "campaign", "creator",
    ),
    "monetization": (
        "pricing", "billing", "payment", "payments", "subscription", "revenue",
        "fintech", "insurance", "accounting", "commerce", "marketplace", "transaction",
        "payroll", "lending", "credit", "banking", "financial", "expense management",
    ),
}


def _text(company: dict[str, Any]) -> str:
    fields = (
        company.get("name"), company.get("one_liner"), company.get("long_description"),
        company.get("industry"), company.get("subindustry"),
        " ".join(company.get("tags") or []) if isinstance(company.get("tags"), list) else company.get("tags"),
    )
    return " ".join(str(field) for field in fields if field).casefold()


def classify_company(company: dict[str, Any]) -> dict[str, list[str]]:
    """Return role matches and the keywords that created each match.

    This is a transparent discovery heuristic, not a claim about a company's
    internal org chart. Every match retains the keyword evidence for review.
    """
    text = _text(company)
    roles: list[str] = []
    evidence: dict[str, list[str]] = {}
    for role, keywords in ROLE_RULES.items():
        matched = [keyword for keyword in keywords if re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text)]
        if matched:
            roles.append(role)
            evidence[role] = matched
    return {"roles": roles, "evidence": evidence}


def build_role_index(companies: list[dict[str, Any]]) -> dict[str, Any]:
    index: dict[str, list[dict[str, Any]]] = {role: [] for role in ROLE_RULES}
    unclassified: list[str] = []
    for company in companies:
        slug = str(company.get("slug") or "").strip()
        if not slug:
            continue
        classification = classify_company(company)
        entry = {
            "slug": slug,
            "name": company.get("name") or slug,
            "batch": company.get("batch") or "",
            "industry": company.get("industry") or "",
            "one_liner": company.get("one_liner") or "",
            "evidence": classification["evidence"],
        }
        if not classification["roles"]:
            unclassified.append(slug)
        for role in classification["roles"]:
            index[role].append(entry)

    for entries in index.values():
        entries.sort(key=lambda item: (item["batch"], item["name"].casefold()), reverse=True)
    return {
        "rules_version": 1,
        "source": "datasets/yc-oss-mirror/companies/all.json",
        "company_count": len(companies),
        "roles": {
            role: {"count": len(entries), "companies": entries}
            for role, entries in index.items()
        },
        "unclassified": {"count": len(unclassified), "slugs": sorted(unclassified)},
    }


def write_role_index(
    companies_path: Path = Path("datasets/yc-oss-mirror/companies/all.json"),
    json_path: Path = Path("datasets/yc-role-index.json"),
    markdown_path: Path = Path("datasets/yc-role-index.md"),
) -> dict[str, Any]:
    with Path(companies_path).open(encoding="utf-8") as handle:
        companies = json.load(handle)
    if not isinstance(companies, list):
        raise ValueError(f"Expected a list in {companies_path}")
    index = build_role_index(companies)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_role_index(index), encoding="utf-8")
    return index


def render_role_index(index: dict[str, Any]) -> str:
    lines = [
        "# YC startup role index",
        "",
        f"Source: `{index['source']}`",
        f"Companies classified: {index['company_count']}",
        "",
        "This index is a transparent keyword map of public YC descriptions. It is a research aid, not a claim about a company's internal hiring or organization. Review the evidence field in `yc-role-index.json` before using a match.",
        "",
        "## Role counts",
        "",
        "| Role | Companies |",
        "| --- | ---: |",
    ]
    for role, payload in index["roles"].items():
        lines.append(f"| {role} | {payload['count']} |")
    lines.extend([
        f"| Unclassified | {index['unclassified']['count']} |",
        "",
        "## Recent examples",
        "",
    ])
    for role, payload in index["roles"].items():
        lines.append(f"### {role}")
        lines.append("")
        for company in payload["companies"][:12]:
            description = company["one_liner"] or "No one-liner in the source record."
            evidence = ", ".join(company["evidence"].get(role, []))
            lines.append(f"- **{company['name']}** ({company['batch'] or 'Unbatched'}, {company['industry'] or 'Unspecified'}): {description} [evidence: {evidence}]")
        lines.append("")
    lines.extend([
        "## Search commands",
        "",
        '```bash',
        'ycombinator filter --batch "Fall 2026"',
        'ycombinator search "agent"',
        'ycombinator search "sales"',
        '```',
        "",
    ])
    return "\n".join(lines)
