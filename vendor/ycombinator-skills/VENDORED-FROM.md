# Vendored from upstream

This directory is a snapshot of [jona/ycombinator-skills](https://github.com/jona/ycombinator-skills) — a Claude Code plugin / skill marketplace bundling 19 Y Combinator startup frameworks distilled from talks by YC speakers (Sam Altman, Andrew Ng, Brad Fisher, Aaron Levie, Elon Musk, Andrej Karpathy, Fei-Fei Li, et al.).

- Upstream license: **MIT** (declared in upstream README; no `LICENSE` file in the repo as of snapshot date). Original copyright remains with the author (Jonathan).
- Upstream default branch: `main`
- Snapshot taken: 2026-05-16

## Layout

```
ycombinator-skills/
├── .claude-plugin/marketplace.json   # Claude Code plugin manifest
├── skills/
│   ├── yc-startup-fundamentals/SKILL.md
│   ├── ai-startup-insights-altman/SKILL.md
│   ├── first-principles-thinking-musk/SKILL.md
│   └── ... 16 more skills
└── README.md                          # upstream README
```

Each skill is a directory with a `SKILL.md` file containing frontmatter (`name`, `description`) and the framework content. These follow the Claude Code skill convention — they could be installed directly via the plugin system, but here they're vendored as plain markdown for offline reading and reference.

## Refresh from upstream

```bash
git clone --depth=1 https://github.com/jona/ycombinator-skills.git /tmp/yc-skills-vendor
rsync -a --delete --exclude='.git' --exclude='VENDORED-FROM.md' \
  /tmp/yc-skills-vendor/ ~/workplace/ycombinator/vendor/ycombinator-skills/
```
