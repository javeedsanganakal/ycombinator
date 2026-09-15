# YC Dataset Research Guide

The local YC dataset supports market mapping, comparable-company discovery, positioning research, open-source discovery, batch analysis, and founder interview list-building. It must not be used to infer private revenue, product-market fit, valuation, customer satisfaction, or investment quality.

Snapshot reviewed: 2026-09-14.

## Coverage

| Asset | Current local coverage | Purpose |
| --- | --- | --- |
| `cache/all.json` | 6,220 company records | Fast local search and filtering |
| `yc-companies/` | One tracked JSON record per company | Git history and company-level inspection |
| `yc-oss-mirror/` | 455 endpoint payloads plus `meta.json` | Batches, industries, tags, curated views, and open-source mappings |
| `yc-oss-mirror/open-source-companies/repositories.json` | Public repository mappings | Find codebases to study by company |

Data comes from the community-maintained [`yc-oss/api`](https://github.com/yc-oss/api) and [`yc-oss/open-source-companies`](https://github.com/yc-oss/open-source-companies), not directly from Y Combinator. Verify current facts using the [official YC Company Directory](https://www.ycombinator.com/companies).

## Search commands

```bash
# Full-text company search across names, descriptions, industries, tags, and regions
ycombinator search "billing" --limit 30

# Structured filters; options can be combined
ycombinator filter --industry B2B --tag AI --status Active --limit 50
ycombinator filter --batch "Winter 2026" --region "United States" --json
ycombinator filter --industry Fintech --subindustry Payments --query API

# Search the startup knowledge base and local Stanford × YC lectures
ycombinator kb-search "founder-led sales"
ycombinator kb-search "user interview" --include-lectures --limit 40

# Inspect one company and available taxonomies
ycombinator show stripe
ycombinator list batches
ycombinator list industries
ycombinator list tags
ycombinator stats
```

## Research workflows

### Comparable-company map

1. Define the customer, job, category, business model, geography, and period.
2. Search several problem and outcome terms; filter by relevant tags and industries.
3. Inspect company descriptions and primary sites.
4. Code the comparison dimension: user, buyer, workflow, promise, pricing metric, channel, or moat.
5. Include failed, inactive, acquired, and differently positioned companies to reduce survivor bias.

### Positioning-language study

Export matching records, then compare one-liners and long descriptions for audience, category, painful job, outcome, differentiation, and proof. Company descriptions are claims; they do not establish customer value.

### Open-source pattern study

Start with `yc-oss-mirror/open-source-companies/repositories.json`, verify the company relationship and current repository ownership, then review license, releases, security policy, architecture, issues, and commercial model before including a project in the knowledge base.

### Batch or sector trend

Use counts to generate questions, not conclusions. Dataset coverage, taxonomy changes, batch sizes, company status, and missing fields can produce apparent trends. Record the snapshot date and denominator, and verify important findings against primary sources.

## Evidence record

```text
Research question:
Dataset snapshot/date:
Query and filters:
Eligible denominator:
Results reviewed:
Fields used and missing-data treatment:
Primary-source verification:
Observed pattern:
Alternative explanation or bias:
Decision affected:
Next evidence required:
```
