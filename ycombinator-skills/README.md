# YCombinator Skills

Apply proven startup strategies and frameworks popularized by Y Combinator guest speakers and founders.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add jona/ycombinator-skills
```

Then install the skills:

```bash
/plugin install ycombinator-skills
```

## Available Skills

| Skill                           | Description                                                               |
| ------------------------------- | ------------------------------------------------------------------------- |
| agi-framework-chollet           | François Chollet's framework for understanding intelligence and AGI paths |
| ai-accelerated-building-ng      | Andrew Ng's AI-accelerated startup development strategies                 |
| ai-product-building-heller      | Jake Heller's Casetext playbook for AI products ($650M exit)              |
| ai-scaling-laws-amodei          | Dario Amodei on AI scaling laws and capability forecasting                |
| ai-scientific-discovery-jumper  | John Jumper on AI for scientific research breakthroughs                   |
| ai-search-strategy-srinivas     | Aravind Srinivas on building AI search and agentic browsers               |
| ai-startup-insights-altman      | Sam Altman's guidance for AI startup founders                             |
| ai-startup-questions-fisher     | Jordan Fisher's strategic questioning framework for AI startups           |
| b2b-ai-startup-levie            | Aaron Levie on B2B AI startup defensibility and timing                    |
| claude-code-guidance-cherny     | Boris Cherny's best practices for using Claude Code effectively           |
| design-tool-scaling-field       | Dylan Field on scaling design tools and Figma's journey                   |
| developer-tools-strategy-truell | Michael Truell on building developer tools (Cursor)                       |
| enterprise-ai-strategy-nadella  | Satya Nadella's enterprise AI deployment frameworks                       |
| first-principles-thinking-musk  | Elon Musk's first principles reasoning for ambitious projects             |
| robotics-ai-learning-finn       | Chelsea Finn on general-purpose robot learning                            |
| software-democratization-masad  | Amjad Masad on AI agents and software democratization                     |
| software-paradigms-karpathy     | Andrej Karpathy's Software 1.0/2.0/3.0 framework                          |
| spatial-intelligence-li         | Fei-Fei Li on spatial intelligence and 3D world modeling                  |
| yc-startup-fundamentals         | Y Combinator methodology for team formation, MVP, growth, and fundraising |

## Structure

```
ycombinator-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace catalog
├── skills/                   # Individual skills
│   ├── agi-framework-chollet/
│   ├── ai-accelerated-building-ng/
│   ├── ai-product-building-heller/
│   └── ...
├── registry/                 # Searchable skill index
├── scripts/                  # Validation and build tools
└── docs/                     # Documentation
```

## License

MIT
