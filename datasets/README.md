# Datasets

YC company data used for research and by the Python toolkit.

- `cache/` contains generated local downloads and is ignored except for `.gitkeep`.
- `yc-companies/` contains one tracked JSON record per company, grouped by batch.
- `yc-oss-mirror/` preserves the complete public API layout, including batches, industries, tags, and open-source repositories.

Refresh these datasets with the commands documented in [`src/ycombinator/README.md`](../src/ycombinator/README.md).
