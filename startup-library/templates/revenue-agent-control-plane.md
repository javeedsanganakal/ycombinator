# Revenue Agent Control Plane

Use this template in a private product repository. It coordinates three specialist loops—Sales, Marketing, and Monetization—through one shared funnel and decision log.

Do not place customer records, credentials, private analytics exports, or billing data in this public startup directory.

## 1. Product truth

| Field | Current evidence |
| --- | --- |
| Product | unknown |
| Initial ICP | unknown |
| User | unknown |
| Buyer | unknown |
| Trigger event | unknown |
| Painful job | unknown |
| Current alternative | unknown |
| Promised outcome | unknown |
| Time to first value | unknown |
| Proof | unknown |
| Primary commercial motion | unknown |
| Reporting timezone | unknown |

## 2. Shared revenue journey

Define one observable event for every transition. Keep the entity consistent: person, account, opportunity, subscription, invoice, or revenue.

```text
Qualified reach
  → engaged demand
  → qualified account
  → evaluation or signup
  → activation
  → paid conversion
  → retained value
  → renewal
  → expansion or referral
```

| Transition | Event/table of record | Entity | Window | Owner | Current baseline |
| --- | --- | --- | --- | --- | --- |
| Qualified reach → engaged demand | unknown | unknown | unknown | Marketing | unknown |
| Engaged demand → qualified account | unknown | unknown | unknown | Marketing/Sales | unknown |
| Qualified account → evaluation | unknown | unknown | unknown | Sales | unknown |
| Evaluation → activation | unknown | unknown | unknown | Sales/Product | unknown |
| Activation → paid conversion | unknown | unknown | unknown | Monetization | unknown |
| Paid → retained value | unknown | unknown | unknown | Product/Success | unknown |
| Retained → renewal | unknown | unknown | unknown | Sales/Monetization | unknown |
| Renewal → expansion/referral | unknown | unknown | unknown | All | unknown |

## 3. Sales agent

**Mission:** turn well-matched demand into activated, retained customers while learning why accounts buy, stall, or decline.

**Read-only inputs**

- CRM accounts, contacts, opportunities, stages, values, owners, and timestamps.
- Call notes, objections, loss reasons, and customer-owned next steps.
- Product activation and retained-use signals by account.
- Contract, security, procurement, and implementation status.

**Daily checks**

- New qualified accounts and trigger evidence.
- Opportunities without a dated customer-owned next step.
- Stage aging beyond the segment's observed baseline.
- Evaluations blocked by product, trust, security, legal, or implementation issues.
- Won accounts that have not reached first value.

**Weekly decisions**

- Keep, narrow, or revise the ICP.
- Change targeting, discovery, demo, proof, offer, or qualification.
- Disqualify low-fit pipeline instead of inflating forecasts.

**Scorecard**

| Metric | Formula/source | Warning threshold | Stop/escalate threshold |
| --- | --- | --- | --- |
| Qualified conversations | qualified conversations / eligible outreach | unknown | unknown |
| Opportunity creation | new qualified opportunities / qualified conversations | unknown | unknown |
| Stage conversion | accounts reaching next stage / eligible accounts entering stage | unknown | unknown |
| Win rate | closed-won / all closed opportunities | unknown | unknown |
| Sales cycle | median days from qualified to won/lost | unknown | unknown |
| Activated wins | won accounts reaching first value / eligible wins | unknown | unknown |
| No-decision rate | no-decision / all closed opportunities | unknown | unknown |

## 4. Marketing agent

**Mission:** create qualified demand from an initial segment and message that the product can truthfully fulfill.

**Read-only inputs**

- Website/product analytics by source, segment, campaign, and landing page.
- Search, content, community, partnership, lifecycle, launch, or paid-channel data actually in use.
- Customer language, objections, sales loss reasons, and proof assets.
- Activation, paid conversion, retention, and revenue joined back to acquisition source where valid.

**Daily checks**

- Qualified reach, engaged demand, and high-intent actions by source.
- Sudden tracking, landing-page, form, signup, or attribution failures.
- Message/channel combinations producing traffic without activation.
- Customer questions that reveal unclear positioning or missing proof.

**Weekly decisions**

- Continue one primary channel and at most two supporting channels.
- Revise audience, problem, promise, mechanism, difference, proof, or call to action.
- Stop channels that fail their predefined time, cost, or quality rule.

**Scorecard**

| Metric | Formula/source | Warning threshold | Stop/escalate threshold |
| --- | --- | --- | --- |
| Qualified reach | segment-qualified people/accounts reached | unknown | unknown |
| Engaged-demand rate | engaged qualified entities / qualified reach | unknown | unknown |
| Qualified-demand rate | qualified entities / engaged demand | unknown | unknown |
| Activation by source | activated entities / eligible new entities by source | unknown | unknown |
| Paid conversion by source | paying accounts / eligible acquired accounts | unknown | unknown |
| Cost per activated account | attributable channel cost / activated accounts | unknown | unknown |
| Retained acquisition | retained acquired accounts / eligible acquired cohort | unknown | unknown |

Do not optimize impressions, clicks, followers, email sends, or opens as final outcomes.

## 5. Monetization agent

**Mission:** turn repeated customer value into understandable, durable revenue with healthy customer and company economics.

**Read-only inputs**

- Product usage, activation, limits, plan, price version, and retained behavior.
- Checkout, subscriptions, invoices, payments, refunds, disputes, and recovery events.
- Variable infrastructure, model/API, payment, support, and delivery costs.
- Churn, contraction, renewal, and expansion reasons by segment and cohort.

**Hourly checks**

- Checkout, payment authorization, billing, entitlement, and lead-to-payment failures.
- Unexpected usage, cost, refund, dispute, or involuntary-churn spikes.

**Weekly/monthly decisions**

- Improve activation or value delivery before adding acquisition.
- Revise packaging, value metric, entry offer, limits, or upgrade path.
- Treat live price changes as migration projects requiring approval and rollback criteria.

**Scorecard**

| Metric | Formula/source | Warning threshold | Stop/escalate threshold |
| --- | --- | --- | --- |
| Trial-to-paid | converted trials / eligible trial cohort | unknown | unknown |
| Ending MRR | starting + new + expansion + reactivation − contraction − churn | unknown | unknown |
| GRR | (starting recurring revenue − contraction − churn) / starting recurring revenue | unknown | unknown |
| NRR | (starting + expansion + reactivation − contraction − churn) / starting recurring revenue | unknown | unknown |
| ARPA | recurring revenue / active paying accounts | unknown | unknown |
| Contribution margin | revenue − variable delivery/payment/product cost | unknown | unknown |
| Involuntary churn | payment-failure churn / eligible paying accounts | unknown | unknown |

## 6. Orchestrator

The orchestrator does not average the three functions. It identifies the earliest material constraint in the shared journey.

Decision order:

1. Confirm data freshness and instrumentation.
2. Check whether the product reliably delivers first value and retained value.
3. Find the largest meaningful transition loss relative to the product's own baseline, target, and cohort evidence.
4. Determine whether that loss is primarily Sales, Marketing, Monetization, Product, or Operations.
5. Select one primary experiment and name its dependency, owner, decision rule, and rollback condition.
6. Keep other ideas in the backlog unless they unblock the primary experiment.

### Daily orchestrator brief

```text
Run ID:
Data through:
Data freshness/status:
Verified facts:
Primary bottleneck:
Evidence and denominator:
Confidence:
Recommended action:
Owner:
Expected evidence:
Decision date:
Stop/rollback condition:
Approval required:
```

## 7. Agent cadence

| Cadence | Sales | Marketing | Monetization | Orchestrator output |
| --- | --- | --- | --- | --- |
| Hourly | routing failures | tracking/form failures | checkout/payment failures | deduplicated incident |
| Daily | stalled deals and activation | qualified demand and anomalies | conversion/revenue anomalies | one bottleneck brief |
| Weekly | pipeline and learning review | channel/message experiments | funnel, retention, and unit economics | one prioritized experiment |
| Monthly | ICP, cycle, win/loss | cohort/channel quality | packaging, pricing realization, NRR/GRR | strategy and resource decision |

## 8. Autonomy ledger

| Action | Default permission |
| --- | --- |
| Read approved sources and calculate metrics | Automatic |
| Draft briefs, messages, experiments, and backlog items | Automatic |
| Open/deduplicate incidents and request approval | Automatic |
| Change a dashboard or private draft | Automatic only when reversible and scoped |
| Contact prospects or customers | Approval required |
| Publish content or launch a campaign | Approval required |
| Spend advertising or tool budget | Approval required |
| Change production pricing, packaging, billing, or entitlements | Approval required |
| Merge code, alter production, export customer data, or delete data | Approval required |

## 9. Experiment queue

| Rank | Function | Evidence | Hypothesis | Primary metric | Guardrail | Time to signal | Owner | Decision rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown |

## 10. Decision log

| Date | Decision | Evidence reviewed | Result/uncertainty | What changed | Owner | Review date |
| --- | --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | unknown | unknown | unknown | unknown | unknown | YYYY-MM-DD |

## Next three actions

1. Complete product truth and the shared journey. Evidence: agreed ICP, buyer, alternative, activation event, retained behavior, and table of record. Decision unlocked: which commercial motion the agent should monitor.
2. Connect one read-only source per specialist and validate entity joins. Evidence: one trustworthy daily snapshot with counts and timestamps. Decision unlocked: whether automation can begin without misleading metrics.
3. Record baselines and set warning/stop thresholds from product evidence. Evidence: denominators, cohorts, ranges, and owners. Decision unlocked: which alerts may run automatically and which require human review.
