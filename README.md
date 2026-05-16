# ycombinator

Fetch, mirror, and query the entire Y Combinator company directory (~5,909 companies) locally.

Three layers of data live in this repo:

| Path | Tracked in git? | Purpose |
| --- | --- | --- |
| `data/all.json` | no (gitignored) | Bulk file the library loads for fast in-memory queries |
| `yc-companies/<year>-<season>/<slug>.json` | **yes** | One pretty-printed JSON per company, organized by batch — for git-friendly diffs |
| `yc-oss-mirror/` | **yes** | Full mirror of every endpoint published by [yc-oss/api](https://github.com/yc-oss/api) (449 files, ~64 MB) |
| `how-to-start-a-startup/` | **yes** | Vendored snapshot of [iqiancheng/how-to-start-a-startup](https://github.com/iqiancheng/how-to-start-a-startup) — Stanford × YC lecture transcripts, slide PDFs, and figures (~22 MB, Unlicense) |
| `ycombinator-skills/` | **yes** | Vendored snapshot of [jona/ycombinator-skills](https://github.com/jona/ycombinator-skills) — 19 YC startup frameworks distilled into Claude Code skills (~200 KB, no license declared) |

## Install

```bash
git clone <this-repo>
cd ycombinator
pip install -e .
```

Python 3.10+. The only runtime dependency is `requests`.

## CLI

```bash
# Main fetch — writes data/all.json AND splits into yc-companies/<batch>/<slug>.json
ycombinator fetch all

# Full mirror — pulls every yc-oss endpoint (~449 files) into yc-oss-mirror/
ycombinator fetch mirror

# Targeted fetches (write under data/)
ycombinator fetch batch winter-2024         # → data/batches/winter-2024.json
ycombinator fetch industry fintech          # → data/industries/fintech.json
ycombinator fetch tag ai                    # → data/tags/ai.json
ycombinator fetch meta                      # → data/meta.json (index of slugs)

# Re-split cached all.json without re-fetching
ycombinator split

# Query / inspect
ycombinator list batches                    # batch slugs + counts (also: industries, tags)
ycombinator stats                           # totals, by status, by batch, by industry
ycombinator search "restaurant"             # full-text search on name + one_liner
ycombinator show stripe                     # pretty-print a single company by slug
```

`fetch all` caches for 24h; pass `--force` to bypass. Add `--no-split` to skip the per-company split. Override directories with `--data-dir`, `--split-dir`, `--mirror-dir`.

## Library

```python
from ycombinator import YCData, fetch_all, fetch_mirror

fetch_all()                                  # bulk file + per-company split
fetch_mirror()                               # mirror all 449 yc-oss endpoints

data = YCData.load()                         # loads from ./data/all.json
fintech = data.filter(batch="Winter 2024", industry="Fintech", status="Active")
ai_b2b  = data.filter(tags=["AI", "B2B"])    # AND across tags (case-insensitive)
matches = data.search("restaurant")          # substring on name + one_liner
stripe  = data.get("stripe")                 # by slug
print(data.stats())                          # {"total": ..., "by_batch": {...}, ...}
```

Each `Company` is a dataclass; unknown fields from upstream are preserved on the `.extra` dict so the package never silently drops new fields.

## Per-company file layout

`ycombinator fetch all` writes a tree like:

```
yc-companies/
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
yc-oss-mirror/
├── meta.json                          # index of all slugs + counts
├── companies/                         # 7 curated views
│   ├── all.json                       # all 5,909
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
- **[iqiancheng/how-to-start-a-startup](https://github.com/iqiancheng/how-to-start-a-startup)** — source of the `how-to-start-a-startup/` folder. 20-lecture Stanford × YC course covering ideas, product, team, fundraising, growth, mechanics, culture. See `how-to-start-a-startup/VENDORED-FROM.md` for refresh instructions.
- **[jona/ycombinator-skills](https://github.com/jona/ycombinator-skills)** — source of the `ycombinator-skills/` folder. 19 distilled YC speaker frameworks (Altman, Musk, Karpathy, Levie, Ng, Li, …) packaged as Claude Code skills. See `ycombinator-skills/VENDORED-FROM.md`.

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
