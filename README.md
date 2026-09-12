# Startup Directory

A private, non-personal knowledge base for understanding, building, launching, and scaling startups.

This repository combines a structured startup library with Y Combinator company data, reusable tools, and carefully attributed third-party learning material. It is organized by startup function so founders, product managers, designers, engineers, and operators can find the right material quickly.

## Start here

- [Startup library](startup-library/README.md) — guides, frameworks, checklists, templates, and curated resources by function
- [YC datasets](datasets/README.md) — company records and the complete `yc-oss` mirror
- [Python toolkit](src/ycombinator/README.md) — fetch, search, filter, and inspect YC company data
- [Vendored resources](vendor/README.md) — attributed third-party courses and startup skills

## Repository map

```text
.
├── startup-library/             # Functional startup knowledge directory
│   ├── founders/
│   ├── product-management/
│   ├── ux-ui/
│   ├── engineering/
│   ├── go-to-market/
│   ├── fundraising/
│   ├── finance/
│   ├── legal/
│   ├── hiring-and-culture/
│   ├── operations/
│   ├── accelerators-and-investors/
│   ├── case-studies/
│   ├── templates/
│   ├── tools/
│   └── resources/
├── datasets/
│   ├── cache/                   # Local fetch cache; generated and gitignored
│   ├── yc-companies/            # One JSON file per company, grouped by batch
│   └── yc-oss-mirror/           # Full mirror of the public yc-oss API
├── src/ycombinator/             # Installable Python package and CLI
├── tests/                       # Python package tests
└── vendor/                      # Preserved third-party material with provenance
```

## Scope

Include material that is broadly useful for startups: founder fundamentals, customer discovery, product management, UX/UI, MVP engineering, go-to-market, sales, growth, fundraising, finance, legal, hiring, culture, and operations.

Do not include personal journals, private company plans, or source code for individual products. Those belong in their own repositories.

## Python toolkit

Python 3.10+ is required. The only runtime dependency is `requests`.

```bash
git clone <this-repo>
cd ycombinator
python -m pip install -e .
```

Common commands:

```bash
ycombinator fetch all
ycombinator fetch mirror
ycombinator list batches
ycombinator stats
ycombinator search "restaurant"
ycombinator show stripe
```

| Path | Tracked? | Purpose |
| --- | --- | --- |
| `datasets/cache/all.json` | No | Fast local cache used by the Python library |
| `datasets/yc-companies/<batch>/<slug>.json` | Yes | Git-friendly company records grouped by batch |
| `datasets/yc-oss-mirror/` | Yes | Complete mirror of published `yc-oss` endpoints |

See [the package guide](src/ycombinator/README.md) for the complete CLI and Python API reference.

## Content principles

1. Organize by startup function, not by personality or source.
2. Prefer concise summaries, actionable checklists, and reusable templates.
3. Record the source, author, license, and retrieval date for imported material.
4. Keep personal projects and confidential company-specific information out.
5. Preserve upstream attribution when vendoring third-party work.

## Upstream data

The data toolkit wraps community-maintained resources from [yc-oss/api](https://github.com/yc-oss/api) and [yc-oss/open-source-companies](https://github.com/yc-oss/open-source-companies). Vendored resources retain their original licenses and provenance files.
