from ycombinator.models import Company
from ycombinator.query import YCData


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


def test_stats_counts_total():
    assert _sample().stats()["total"] == 3


def test_get_by_slug():
    assert _sample().get("stripe").name == "Stripe"
    assert _sample().get("nope") is None
