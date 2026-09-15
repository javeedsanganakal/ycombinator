# Analytics and Experimentation Projects

Use these projects to study the path from raw events to product decisions. Define the question, unit of analysis, and decision rule before selecting a dashboard.

Last reviewed: 2026-09-14.

| Project | Study it for | Inspect closely | Important limitation |
| --- | --- | --- | --- |
| [PostHog](https://github.com/PostHog/posthog) | Integrated product analytics and qualitative evidence | Events, persons, groups, funnels, retention, replay, surveys | Identity design and event quality determine whether reports are trustworthy |
| [GrowthBook](https://github.com/growthbook/growthbook) | Feature flags and statistically grounded experiments | Metric definitions, assignment, exposure, guardrails, sample-ratio checks | Experimentation requires enough traffic and valid instrumentation |
| [Matomo](https://github.com/matomo-org/matomo) | Broad web analytics with data-control options | Visits, goals, attribution, consent, reporting, plugin architecture | Web visits should not be mixed with users, accounts, or revenue denominators |
| [Metabase](https://github.com/metabase/metabase) | Accessible business intelligence over operational data | Models, metrics, questions, dashboards, permissions, embedding | Dashboard flexibility can hide inconsistent definitions without governance |
| [Apache Superset](https://github.com/apache/superset) | Large-scale SQL exploration and visualization | Semantic layer, datasets, charts, dashboards, roles | It assumes analytics and data-engineering capability |
| [OpenReplay](https://github.com/openreplay/openreplay) | Session replay and frontend diagnostics | Replay capture, privacy controls, errors, performance, assist | Replays are samples of behavior, not causal evidence or customer consent by default |

## Minimum product event model

Track acquisition source, signup or install, first value, activation, core repeated behavior, collaboration or expansion, pricing exposure, checkout, payment, cancellation, and churn reason. Keep person, workspace/account, subscription, and revenue identities distinct.
