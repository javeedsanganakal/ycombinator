# Always-on startup revenue agent

An always-on agent is a scheduled decision loop, not one model request that stays alive forever. The scheduler wakes it, deterministic checks establish facts, the agent recommends or performs bounded work, and every run leaves an audit trail.

## Two operating loops

### Repository heartbeat

This repository includes `.github/workflows/startup-kb-agent.yml`.

- Every six hours: run tests, validate internal links, parse every tracked JSON file, compare the company mirror with the per-company dataset, and retain a report for 30 days.
- Daily: refresh the public YC company mirror, repeat all validation, and commit only verified dataset changes.
- On failure: create or update one GitHub incident issue rather than silently retrying forever.
- On recovery: comment on and close the incident automatically.
- On demand: run `ycombinator agent`, or start the workflow manually with an optional full data refresh.

This loop is deterministic and does not need an AI API key.

To activate it, enable GitHub Actions for the repository and run **Startup KB Agent** once from the Actions tab. The scheduled workflow then runs from the default branch. GitHub can delay scheduled runs during busy periods, and scheduled workflows in public repositories can be disabled after 60 days without repository activity, so treat the incident channel—not exact cron timing—as the reliability contract.

## Product revenue loop

For a specific product, connect read-only data sources first. Keep the product configuration in its own private repository; this public startup directory should contain only reusable methods.

Use the [Revenue Agent Control Plane](../templates/revenue-agent-control-plane.md) to configure three specialist loops:

1. **Sales agent:** ICP, qualification, pipeline movement, win/loss evidence, activation, and retained accounts.
2. **Marketing agent:** positioning, qualified demand, channel quality, acquisition-to-activation, and cohort retention.
3. **Monetization agent:** pricing and packaging evidence, paid conversion, revenue movement, margin, churn, and expansion.

An orchestrator checks data quality, diagnoses the earliest material constraint in the shared journey, and selects one primary experiment. It does not allow three agents to optimize conflicting local metrics.

| Cadence | Inputs | Agent output | Human decision |
| --- | --- | --- | --- |
| Hourly | uptime, checkout errors, lead-routing failures | incident with evidence | intervene when a stop threshold fires |
| Daily | visitors, activation, qualified leads, pipeline, trials, paid conversion | bottleneck brief and anomaly list | select the day's one corrective action |
| Weekly | cohorts, retention, expansion, channel cost, sales stages | revenue review and ranked experiments | stop, continue, or iterate each experiment |
| Monthly | pricing realization, gross margin, churn reasons, segment performance | packaging and segment review | change positioning, package, price, or motion |

### Required metric contract

Define each metric before connecting tools:

- event or table of record;
- unit: person, account, opportunity, order, or revenue;
- numerator and denominator;
- time window and timezone;
- owner;
- warning and stop thresholds;
- data freshness expectation.

Never let the agent mix visitors with accounts, leads with opportunities, bookings with collected revenue, or logo retention with revenue retention.

### Autonomy boundary

Safe automatic actions include reading approved sources, calculating metrics, comparing thresholds, drafting reports, updating an internal backlog, and opening an incident. Require explicit authorization for contacting customers, publishing content, changing prices, spending budget, merging code, altering production, or deleting data.

Use idempotent actions, a run identifier, a retry limit, and one deduplicated incident per failure class. Store secrets in the deployment platform, never in this repository. Log source timestamps, assumptions, calculations, recommendations, and actions taken.

## Optional AI reasoning

Use AI after deterministic collection and validation. Give the model a compact evidence packet and request structured output containing: observed facts, primary bottleneck, confidence, recommended action, expected evidence, stop condition, and actions requiring approval. A long-running model response can execute asynchronously, but a scheduler or webhook still owns the continuing 24/7 lifecycle.

## Deployment choices

- GitHub Actions: best for this repository's periodic maintenance and reports.
- A scheduled serverless job: best for short product-metric reviews with managed secrets.
- A queue plus worker service: best when events arrive continuously or jobs can overlap.
- A self-hosted daemon: use only when sub-minute response time or private-network access is essential; add health checks, restarts, durable state, and alerting.

Do not use a permanently running hosted CI job as the agent. Run short, restartable heartbeats and persist state outside the process.

## Primary references

- [GitHub scheduled workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [GitHub workflow token permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
- [OpenAI background mode](https://developers.openai.com/api/docs/guides/background)
