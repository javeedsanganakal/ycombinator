# ycombinator

Fetch, mirror, and query the entire Y Combinator company directory (~6,220 companies in the current snapshot) locally.

Three layers of data live in this repo:

| Path | Tracked in git? | Purpose |
| --- | --- | --- |
| `datasets/cache/all.json` | no (gitignored) | Bulk file the library loads for fast in-memory queries |
| `datasets/yc-companies/<year>-<season>/<slug>.json` | **yes** | One pretty-printed JSON per company, organized by batch — for git-friendly diffs |
| `datasets/yc-oss-mirror/` | **yes** | Full mirror of [yc-oss/api](https://github.com/yc-oss/api): 455 endpoint payloads plus `meta.json` (456 JSON files, ~68 MB) |
| `vendor/how-to-start-a-startup/` | **yes** | Vendored snapshot of [iqiancheng/how-to-start-a-startup](https://github.com/iqiancheng/how-to-start-a-startup) — Stanford × YC lecture transcripts, slide PDFs, and figures (~22 MB, Unlicense) |
| `vendor/ycombinator-skills/` | **yes** | Vendored snapshot of [jona/ycombinator-skills](https://github.com/jona/ycombinator-skills) — 19 YC startup frameworks distilled into Claude Code skills (~200 KB, MIT per upstream README) |

## Install

```bash
git clone <this-repo>
cd ycombinator
pip install -e .
```

Python 3.10+. The only runtime dependency is `requests`.

## CLI

```bash
# Main fetch — writes datasets/cache/all.json and splits records by batch
ycombinator fetch all

# Full mirror — pulls every yc-oss endpoint into datasets/yc-oss-mirror/
ycombinator fetch mirror

# Targeted fetches (write under datasets/cache/)
ycombinator fetch batch winter-2024         # → datasets/cache/batches/winter-2024.json
ycombinator fetch industry fintech          # → datasets/cache/industries/fintech.json
ycombinator fetch tag ai                    # → datasets/cache/tags/ai.json
ycombinator fetch meta                      # → datasets/cache/meta.json (index of slugs)

# Re-split cached all.json without re-fetching
ycombinator split

# Query / inspect
ycombinator list batches                    # batch slugs + counts (also: industries, tags)
ycombinator stats                           # totals, by status, by batch, by industry
ycombinator search "restaurant"             # full-text company search
ycombinator filter --industry B2B --tag AI   # structured, combinable filters
ycombinator kb-search "pricing"              # search startup-library Markdown
ycombinator kb-search "sales" --include-lectures
ycombinator show stripe                     # pretty-print a single company by slug
```

`fetch all` caches for 24h; pass `--force` to bypass. Add `--no-split` to skip the per-company split. Override directories with `--data-dir`, `--split-dir`, `--mirror-dir`.

## Library

```python
from ycombinator import YCData, fetch_all, fetch_mirror

fetch_all()                                  # bulk file + per-company split
fetch_mirror()                               # mirror all current yc-oss endpoints

data = YCData.load()                         # loads from ./datasets/cache/all.json
fintech = data.filter(batch="Winter 2024", industry="Fintech", status="Active")
ai_b2b  = data.filter(tags=["AI", "B2B"])    # AND across tags (case-insensitive)
matches = data.search("restaurant")          # public text fields, tags, and regions
stripe  = data.get("stripe")                 # by slug
print(data.stats())                          # {"total": ..., "by_batch": {...}, ...}
```

Each `Company` is a dataclass; unknown fields from upstream are preserved on the `.extra` dict so the package never silently drops new fields.

## Per-company file layout

`ycombinator fetch all` writes a tree like:

```
datasets/yc-companies/
├── 2005-summer/
│   ├── reddit.json
│   └── loopt.json
├── 2021-winter/
│   ├── zepto.json
│   └── ...
├── 2024-summer/
└── unbatched/        # for records with no/odd batch field
```

Folder = `<year>-<season>` (lowercased), so it sorts chronologically. Filename = upstream `slug`. Splitter is idempotent — it cleans existing files first so renamed/removed companies don't linger. When YC updates a record, `git diff` shows only the changed fields.

## Full upstream mirror

`ycombinator fetch mirror` downloads every endpoint listed in [`meta.json`](https://yc-oss.github.io/api/meta.json) in parallel (~5s with 16 workers):

```
datasets/yc-oss-mirror/
├── meta.json                          # index of all slugs + counts
├── companies/                         # 7 curated views
│   ├── all.json                       # all 6,220 in the current snapshot
│   ├── top.json                       # YC "top companies"
│   ├── hiring.json                    # currently hiring
│   ├── nonprofit.json
│   ├── women-founded.json
│   ├── hispanic-latino-founded.json
│   └── black-founded.json
├── batches/                           # 50 slices (winter-2021.json, ...)
├── industries/                        # 59 slices (fintech.json, ...)
├── tags/                              # 331 slices (ai.json, b2b.json, ...)
└── open-source-companies/
    └── repositories.json              # from yc-oss/open-source-companies
```

Re-run any time to refresh — files are overwritten in place.

## Upstream references

This package is a thin wrapper over the community-maintained yc-oss org:

- **[yc-oss/api](https://github.com/yc-oss/api)** — the canonical JSON API for YC companies (rebuilt daily). Endpoints live at `https://yc-oss.github.io/api/`.
- **[yc-oss/open-source-companies](https://github.com/yc-oss/open-source-companies)** — list of YC startups with public open-source repositories.
- **[yc-oss org](https://github.com/yc-oss)** — root org page.
- **[iqiancheng/how-to-start-a-startup](https://github.com/iqiancheng/how-to-start-a-startup)** — source of `vendor/how-to-start-a-startup/`. See its `VENDORED-FROM.md` for refresh instructions.
- **[jona/ycombinator-skills](https://github.com/jona/ycombinator-skills)** — source of `vendor/ycombinator-skills/`. See its `VENDORED-FROM.md`.

If yc-oss adds new endpoints, `fetch mirror` will pick them up automatically because it iterates `meta.json` rather than hard-coding slugs.

## Field reference (upstream schema)

Most-used fields on each company record:

| Field | Example |
| --- | --- |
| `name`, `slug` | `"Stripe"`, `"stripe"` |
| `batch` | `"Winter 2021"` (full names, not `W21`) |
| `status` | `"Active"`, `"Acquired"`, `"Public"`, `"Inactive"` |
| `industry`, `subindustry` | `"Fintech"`, `"Consumer -> Food and Beverage"` |
| `tags` | `["AI", "B2B", "Developer Tools"]` (title case) |
| `regions` | `["United States", "Remote"]` |
| `team_size`, `stage` | `1300`, `"Growth"` |
| `one_liner`, `long_description` | short tagline + longer pitch |
| `website`, `url` | company site + YC profile URL |

Filtering is case-insensitive via `YCData.filter()`, so you can pass `"fintech"` or `"Fintech"` interchangeably.
