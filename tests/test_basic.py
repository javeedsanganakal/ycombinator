from pathlib import Path
from tempfile import TemporaryDirectory

from ycombinator.agent import CheckResult, build_report, check_internal_links, report_markdown
from ycombinator.cli import build_parser, search_markdown
from ycombinator.founders import build_founder_index
from ycombinator.models import Company
from ycombinator.query import YCData
from ycombinator.roles import classify_company, build_role_index


def _sample() -> YCData:
    return YCData([
        Company.from_dict({
            "name": "Stripe", "slug": "stripe", "batch": "S09",
            "industry": "Fintech", "status": "Active",
            "one_liner": "Payments infrastructure for the internet",
            "tags": ["fintech", "payments", "b2b"],
            "regions": ["United States"],
        }),
        Company.from_dict({
            "name": "Doordash", "slug": "doordash", "batch": "S13",
            "industry": "Consumer", "status": "Public",
            "one_liner": "Restaurant delivery",
            "tags": ["consumer", "logistics"],
            "regions": ["United States"],
        }),
        Company.from_dict({
            "name": "Replit", "slug": "replit", "batch": "W18",
            "industry": "B2B", "subindustry": "Engineering, Product and Design",
            "status": "Active",
            "one_liner": "Online IDE that runs anywhere",
            "tags": ["developer-tools", "ai", "b2b"],
        }),
    ])


def test_company_from_dict_keeps_unknown_fields_in_extra():
    c = Company.from_dict({"name": "X", "slug": "x", "future_field": 1})
    assert c.name == "X"
    assert c.extra == {"future_field": 1}
    assert c.to_dict()["future_field"] == 1


def test_filter_by_industry_and_status():
    data = _sample().filter(industry="Fintech", status="Active")
    assert len(data) == 1
    assert data.companies[0].slug == "stripe"


def test_filter_requires_all_tags():
    data = _sample().filter(tags=["ai", "b2b"])
    assert [c.slug for c in data] == ["replit"]


def test_search_matches_name_or_one_liner():
    data = _sample().search("restaurant")
    assert [c.slug for c in data] == ["doordash"]


def test_search_matches_tags_and_subindustry():
    assert [c.slug for c in _sample().search("developer-tools")] == ["replit"]
    assert [c.slug for c in _sample().search("engineering, product")] == ["replit"]


def test_stats_counts_total():
    assert _sample().stats()["total"] == 3


def test_get_by_slug():
    assert _sample().get("stripe").name == "Stripe"
    assert _sample().get("nope") is None


def test_filter_command_parses_combined_fields():
    args = build_parser().parse_args([
        "filter", "--industry", "B2B", "--tag", "AI",
        "--tag", "Developer Tools", "--status", "Active", "--json",
    ])
    assert args.industry == "B2B"
    assert args.tags == ["AI", "Developer Tools"]
    assert args.status == "Active"
    assert args.json is True


def test_search_markdown_returns_heading_and_line():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "guide.md"
        path.write_text("# Sales\n\nFounder-led discovery creates evidence.\n", encoding="utf-8")
        matches = search_markdown("discovery", [Path(directory)])
    assert matches == [{
        "path": str(path),
        "line": 3,
        "heading": "Sales",
        "text": "Founder-led discovery creates evidence.",
    }]


def test_agent_detects_broken_internal_markdown_link():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "README.md").write_text("[Missing](nope.md)\n", encoding="utf-8")
        result = check_internal_links(root)
    assert result.status == "fail"
    assert "README.md -> nope.md" in result.details


def test_agent_report_status_and_markdown():
    report = build_report(Path("."), checks=[
        CheckResult("one", "pass", "healthy"),
        CheckResult("two", "fail", "broken", ("reason",)),
    ])
    assert report["status"] == "fail"
    rendered = report_markdown(report)
    assert "Startup KB Agent" in rendered
    assert "reason" in rendered


def test_role_index_keeps_keyword_evidence():
    company = {
        "slug": "example",
        "name": "Example AI Sales",
        "one_liner": "Revenue infrastructure for developer teams",
        "industry": "B2B",
    }
    classification = classify_company(company)
    assert "sales" in classification["roles"]
    assert "monetization" in classification["roles"]
    assert "revenue" in classification["evidence"]["monetization"]


def test_role_index_counts_companies_once_per_role():
    index = build_role_index([
        {"slug": "a", "name": "A", "one_liner": "Sales software"},
        {"slug": "b", "name": "B", "one_liner": "Design tools"},
    ])
    assert index["company_count"] == 2
    assert index["roles"]["sales"]["count"] == 1
    assert index["roles"]["ux-ui"]["count"] == 1


def test_founder_index_uses_yc_top_company_flag_and_public_fields():
    calls = []

    def fake_fetcher(url):
        calls.append(url)
        return [{"full_name": "Ada Founder", "title": "Founder", "founder_bio": "Builder", "twitter_url": "", "linkedin_url": "", "latest_yc_company": "Example"}]

    index = build_founder_index([
        {"slug": "top", "name": "Top", "top_company": True, "url": "https://example.test/top"},
        {"slug": "ordinary", "name": "Ordinary", "top_company": False, "url": "https://example.test/ordinary"},
    ], fetcher=fake_fetcher, delay=0)
    assert index["company_count"] == 1
    assert index["founder_count"] == 1
    assert calls == ["https://example.test/top"]
    assert index["companies"][0]["founders"][0]["full_name"] == "Ada Founder"
