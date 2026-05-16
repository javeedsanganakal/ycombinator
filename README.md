# ycombinator

Fetch and query the entire Y Combinator company directory (~5,900 companies) locally.

Data comes from the community-maintained [`yc-oss/api`](https://github.com/yc-oss/api), which mirrors YC's public company list and is updated daily.

## Install

```bash
git clone <this-repo>
cd ycombinator
pip install -e .
```

Python 3.10+. The only runtime dependency is `requests`.

## CLI

```bash
ycombinator fetch all                       # all companies → data/all.json
ycombinator fetch batch winter-2024         # one batch → data/batches/winter-2024.json
ycombinator fetch industry fintech          # one industry → data/industries/fintech.json
ycombinator fetch tag ai                    # one tag → data/tags/ai.json
ycombinator list batches                    # list batch slugs + counts
ycombinator stats                           # totals, by status, by batch, by industry
ycombinator search "restaurant"             # full-text search on name + one_liner
ycombinator show stripe                     # pretty-print a single company
```

`fetch all` caches for 24 hours; pass `--force` to re-fetch. Override the data directory with `--data-dir /some/path`.

## Library

```python
from ycombinator import YCData, fetch_all

fetch_all()                                  # downloads to ./data/

data = YCData.load()                         # loads from ./data/all.json
fintech = data.filter(batch="Winter 2024", industry="Fintech", status="Active")
ai_b2b  = data.filter(tags=["AI", "B2B"])    # AND across tags
matches = data.search("restaurant")          # substring on name + one_liner
stripe  = data.get("stripe")                 # by slug
print(data.stats())                          # {"total": ..., "by_batch": {...}, ...}
```

Each `Company` is a dataclass; unknown fields from the upstream API are preserved on the `.extra` dict so this package doesn't silently drop new fields.

## Data source

All JSON is fetched from `https://yc-oss.github.io/api/`. Files written to `./data/` are gitignored so a clone is small; regenerate them with `ycombinator fetch all`.
