# Continuous revenue agent

Use this mode when a founder wants ongoing monitoring or an agent that operates around the clock.

Read the repository's [always-on agent architecture](../../../startup-library/knowledge-base/always-on-revenue-agent.md). Define the metric contract and autonomy boundary before recommending infrastructure. Prefer short, restartable, idempotent runs triggered by schedules or events. Separate deterministic collection and validation from model reasoning.

Produce:

1. a cadence table for hourly, daily, weekly, and monthly jobs that are justified by the product's actual sales cycle;
2. source-to-metric mappings with freshness expectations;
3. alert thresholds and deduplication rules;
4. actions the agent may perform automatically and actions requiring approval;
5. durable state, audit log, retry, cost-cap, and failure-recovery requirements;
6. a smallest deployable version that works without fabricated or unavailable data.

Do not describe a single endlessly running model call as a 24/7 agent. A scheduler, event source, or worker lifecycle must invoke bounded agent runs. Never put customer data or credentials into prompts, source control, or logs without an explicit data-handling design.
