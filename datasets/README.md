# Datasets

YC company data used for research and by the Python toolkit.

Current snapshot: 2026-09-22 — 6,245 company records, 455 mirrored `yc-oss` endpoint payloads, and `meta.json` (456 JSON files total). See the [recent YC startup snapshot](recent-yc-startups.md) for the newest batches and research notes.

- `cache/` contains generated local downloads and is ignored except for `.gitkeep`.
- `yc-companies/` contains one tracked JSON record per company, grouped by batch.
- `yc-oss-mirror/` preserves the complete public API layout, including batches, industries, tags, and open-source repositories.

Refresh these datasets with the commands documented in [`src/ycombinator/README.md`](../src/ycombinator/README.md).

Use the [`YC Dataset Research Guide`](yc-research-guide.md) for structured filters, knowledge-base search, comparable-company research, positioning analysis, open-source discovery, and evidence guardrails.
