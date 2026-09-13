# Monetization System

Use for pricing, packaging, business models, trials, paywalls, billing, payments, retention, and expansion.

## Start with value

Separate five decisions:

1. **Value creation:** what customer outcome improves?
2. **Value metric:** what measurable unit grows with that outcome?
3. **Packaging:** which capabilities, limits, service, and risk belong together?
4. **Price:** how much is charged and in which currency/market?
5. **Billing:** when, how, and under which contractual rules money is collected?

Changing a price without understanding the other four produces noisy learning.

## Value metric test

Candidate metrics include account, seat, active user, workflow, transaction, volume, data, compute, asset, location, outcome, or a hybrid.

Score each candidate:

- Customer understands and can forecast it.
- It correlates with realized customer value.
- It grows when successful customers grow.
- It is measurable, auditable, and hard to game.
- It preserves healthy product behavior.
- It covers variable cost and supports margin.
- It works with procurement and budget ownership.
- It does not produce frightening surprise bills.

Avoid a metric chosen only because the product can technically meter it.

## Pricing architecture

| Model | Useful when | Main risk |
| --- | --- | --- |
| One-time | Deliverable/value is discrete | No recurring revenue for ongoing cost/value |
| Flat subscription | Value and usage are reasonably similar | Under-monetizes large customers or overprices small ones |
| Per-seat | Collaboration/value scales with users | Discourages adoption and shared accounts |
| Tiered packages | Segments have recognizable needs | Arbitrary feature fences and plan confusion |
| Usage-based | Value and cost scale with measurable use | Unpredictable bills, revenue volatility, usage anxiety |
| Credits | Several actions need a common commercial unit | Opaque conversion between credits and value |
| Transaction/take rate | Product participates directly in economic activity | Disintermediation and margin sensitivity |
| Outcome-based | Outcome is attributable, measurable, and valuable | Disputes, delayed collection, external confounders |
| Services | Expertise or implementation is part of value | Low software margin and difficult scaling |
| Hybrid | Base access plus variable value/cost | Operational and explanation complexity |

Recommend the simplest model that fits value and economics. Complexity needs a specific benefit.

## Packaging

Package around customer maturity or jobs:

- Entry package: fastest credible path to a narrow outcome.
- Core package: complete recurring workflow for the primary ICP.
- Advanced package: governance, scale, controls, integrations, or service required by more complex customers.
- Add-ons: independently valued capabilities with a different buyer or cost driver.

Good fences correspond to value, cost, risk, or operating complexity. Weak fences merely make the lower plan frustrating.

For each package define:

```text
Target segment/job:
Outcome:
Included capabilities:
Usage/scale limits:
Service/support:
Security/governance:
Primary value metric:
Price and billing cadence:
Upgrade trigger:
Gross-margin risk:
```

## Research willingness to pay

Use several evidence types:

- Existing spend on software, labor, services, risk, or lost opportunity.
- Customer budget ownership and approval thresholds.
- Actual purchase, paid pilot, deposit, preorder, or signed commercial intent.
- Won/lost behavior at different offers and segments.
- Structured pricing interviews that explore too-cheap, acceptable, expensive, and prohibitively expensive perceptions.
- Conjoint or choice testing when sample size and decision importance justify it.
- Competitive prices as context, not the final answer.

Ask pricing questions after understanding the workflow and value. Hypothetical willingness to pay is weaker than a real decision.

## Free, trial, demo, or paid entry

Choose based on time-to-value and buying complexity:

- **Ungated free:** value is fast, marginal cost is low, sharing/learning benefits exist, and free users can reach a meaningful limit.
- **Freemium:** a durable free job exists and an observable expansion trigger creates paid value.
- **Time-limited trial:** users can reach value within the window and urgency aids evaluation.
- **Usage/credit trial:** value is usage-driven and time is a poor limit; make the unit transparent.
- **Reverse trial:** users experience advanced value first, then retain a useful free state.
- **Demo/sales-assisted:** setup, risk, contract value, or multi-stakeholder buying makes unguided evaluation ineffective.
- **Paid pilot:** delivery has material cost and success must be jointly implemented.

Do not use a free plan merely because competitors do. Model support and infrastructure cost, abuse, conversion path, and opportunity cost.

## Price presentation

A pricing surface should clarify:

- Who each option is for.
- What outcome and meaningful capability each includes.
- The billing unit, cadence, minimum, limits, and overage behavior.
- Monthly versus annual total and renewal terms.
- Trial conversion behavior and cancellation.
- Taxes or fees that materially affect the buyer.
- What happens when usage grows or declines.
- The appropriate route for complex customers.

Avoid preselected expensive plans, hidden fees, disguised ads, obstructive cancellation, fake countdowns, and ambiguous units.

## Unit economics

Model by segment and plan:

```text
Revenue
- payment processing
- variable infrastructure/model/API cost
- customer-specific delivery/support
- refunds, credits, and fraud
= contribution margin

Contribution margin
- attributable acquisition and sales cost
= near-term customer contribution
```

Do not label all engineering or support cost as fixed when usage growth causes it to increase. For AI products, model input/output tokens, model/provider mix, retries, agent loops, storage, tools, and high-percentile usage—not only average inference cost.

## Usage-based and hybrid pricing

Usage billing requires:

- A customer-readable meter and aggregation rule.
- Idempotent, auditable event ingestion.
- Late, duplicate, corrected, and missing event handling.
- Usage visibility and threshold alerts.
- Spend controls, caps, or prepaid commitments where appropriate.
- Versioned prices and grandfathering/migration rules.
- Invoice preview and dispute process.
- Margin monitoring at account and cohort level.

Hybrid designs can combine a predictable platform fee or commitment with usage, seats, or overages. Use them when pure usage creates revenue volatility or customer budget anxiety.

## Conversion and paywalls

Before changing the paywall, determine:

- Whether the user reached value.
- Whether the user and buyer are the same person.
- Whether the gated capability maps to additional value.
- Whether the price, billing unit, and next step are understood.
- Whether checkout, tax, payment method, trust, or technical errors create friction.

Segment paywall conversion by activation state, ICP, source, device, geography, offer, and plan. Blended conversion can hide a strong offer sent to the wrong traffic.

## Retention and expansion

Revenue durability depends on repeated value:

- Define expected usage cadence and retained behavior.
- Separate voluntary churn, involuntary churn, contraction, and non-renewal.
- Record churn reason at a useful level; “too expensive” may mean weak value, wrong segment, missing capability, cash constraint, or poor price metric.
- Review retention by acquisition source, ICP, plan, vintage, and activation state.
- Tie expansion to more value: additional teams, use cases, volume, capabilities, locations, or outcomes.
- Use payment retries, card/account updates, and relevant payment methods to reduce involuntary churn without obscuring cancellation rights.

## Pricing changes

Treat a pricing change as a migration project:

1. State the hypothesis and target segment.
2. Model customer and company impact across real usage distributions.
3. Test comprehension and willingness to pay qualitatively.
4. Decide which cohorts change, when, and under what protection.
5. Update product entitlements, meters, checkout, contracts, invoices, tax, analytics, support, and communication.
6. Monitor conversion, activation, support, churn, expansion, margin, and trust signals.
7. Define rollback or remediation criteria.

Never change live customer pricing solely to obtain cleaner experiment data.

## Legal and operational boundary

Pricing and billing may implicate consumer protection, automatic renewal, cancellation, taxes, invoicing, sanctions, privacy, card-network, app-store, and accounting requirements. Verify current authoritative guidance for the relevant product, customer type, jurisdiction, and payment channel. Flag where qualified legal, tax, or accounting advice is required.
