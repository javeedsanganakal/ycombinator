# Vendored from upstream

This directory is a snapshot of [iqiancheng/how-to-start-a-startup](https://github.com/iqiancheng/how-to-start-a-startup) — the markdown transcripts, slide decks, and figures from Stanford / Y Combinator's *How to Start a Startup* lecture series (Sam Altman, Dustin Moskovitz, Paul Graham, et al.).

- Upstream license: **Unlicense** (public domain — see `LICENSE`)
- Upstream default branch: `master`
- Snapshot taken: 2026-05-16

To refresh from upstream:

```bash
cd /tmp && rm -rf how-to-start-a-startup
git clone --depth=1 https://github.com/iqiancheng/how-to-start-a-startup.git
rsync -a --delete --exclude='.git' --exclude='VENDORED-FROM.md' \
  /tmp/how-to-start-a-startup/ ~/workplace/ycombinator/how-to-start-a-startup/
```
