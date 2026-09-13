# Metrics and Experiments

Use to define the revenue model, instrument a funnel, diagnose performance, or create an experiment backlog.

## Measurement contract

For every metric define:

```text
Name:
Business question:
Entity: person, account, workspace, subscription, invoice, or revenue
Population and exclusions:
Numerator:
Denominator:
Event/property source:
Time window:
Segmentation dimensions:
Owner:
Known limitations:
```

Do not compare conversion rates with different entities, attribution rules, eligibility criteria, or time windows.

## Revenue journey

Customize this canonical journey:

```text
Qualified reach
  → engaged demand
  → qualified account/user
  → evaluation or signup
  → activation
  → paid conversion
  → retained value
  → renewed revenue
  → expansion or referral
```

Define one observable transition for each arrow. “Engaged” and “activated” are product-specific behaviors, not universal events.

## Core conversion formulas

Use cohort-based denominators when conversion can take time.

```text
Stage conversion = entities reaching stage B / eligible entities reaching stage A

Activation rate = eligible new entities reaching activation within window
                  / eligible new entities starting within window

Trial-to-paid = trials converting within allowed conversion window
                / eligible trials started in the cohort

Win rate = closed-won opportunities / all closed opportunities

Sales velocity = qualified opportunities × win rate × average deal value
                 / average sales-cycle length
```

Report counts beside rates. A high rate with a tiny denominator should not dominate decisions.

## Recurring revenue

Define revenue treatment before calculating:

```text
Ending MRR = Starting MRR
           + New MRR
           + Expansion MRR
           + Reactivation MRR
           - Contraction MRR
           - Churned MRR

GRR = (Starting recurring revenue - contraction - churn)
      / Starting recurring revenue

NRR = (Starting recurring revenue + expansion + reactivation
       - contraction - churn)
      / Starting recurring revenue

Logo retention = retained customer logos / customer logos eligible to renew

ARPA = recurring revenue / active paying accounts
```

State whether reactivation belongs in NRR; organizations differ. Never silently mix bookings, billings, cash, recognized revenue, contracted ARR, and recurring run rate.

For usage businesses, show committed recurring revenue and variable consumption separately. Do not annualize unstable experimental usage without a clear label.

## Acquisition economics

```text
CAC = attributable sales and marketing cost / new customers acquired

Gross-margin-adjusted CAC payback months
  = CAC / (new-customer monthly recurring revenue × gross margin rate)

Contribution payback
  = cumulative customer contribution after variable costs
    compared with acquisition cost
```

Include salaries, tools, agencies, media, commissions, events, and an allocation rule appropriate to the decision. Blended CAC can hide an unviable channel.

Avoid a single LTV estimate when retention history is short. Show realized cohort contribution and scenario ranges. If using a simple steady-state model, label its assumptions:

```text
Illustrative LTV = ARPA × gross margin rate / monthly revenue churn rate
```

This formula is highly sensitive to churn, ignores timing and cohort change, and is often misleading for young or usage-based businesses.

## Sales metrics

Track:

- Eligible accounts and contact coverage.
- Positive response and qualified-conversation rate.
- Opportunity creation by source and segment.
- Stage conversion and days in stage.
- Win rate, no-decision rate, and loss reasons.
- Average/median contract value and discount.
- Sales cycle and implementation cycle.
- Pipeline created, committed, won, activated, and retained.
- Forecast accuracy by category and rep/founder.

Meetings are a useful activity diagnostic, not the final outcome.

## Marketing metrics

Track by source and segment:

- Qualified reach, not impressions alone.
- Engaged demand and high-intent actions.
- Qualified pipeline or activated self-serve accounts.
- Cost per qualified/activated/paying account.
- Activation and retention of acquired cohorts.
- Content-assisted journeys without claiming false causal attribution.
- Loop coefficient and cycle time where a real growth loop exists.
- Incremental lift for paid or lifecycle programs when measurable.

Attribution allocates credit; it does not automatically prove causation.

## Product and monetization metrics

- Time-to-first-value.
- Activation rate and completion of critical steps.
- Retained behavior by natural usage interval.
- Free/trial-to-paid conversion by activation state.
- Checkout completion, payment authorization, and payment recovery.
- New, expansion, contraction, reactivation, and churned revenue.
- GRR, NRR, logo retention, ARPA, and contribution margin.
- Usage distribution and unit cost by plan/account.
- Limit encounters, upgrade intent, and expansion realization.
- Refund, dispute, involuntary churn, and support rates.

## Cohorts and segmentation

At minimum consider:

- Start or purchase cohort.
- ICP versus non-ICP.
- Acquisition source/campaign.
- Self-serve versus sales-assisted.
- Package and price version.
- Activated versus not activated.
- Geography/currency and device where relevant.
- Company size or customer value band.

Do not over-segment until every cell is noise. Show denominator and uncertainty.

## Experiment brief

```text
Decision:
Observed evidence:
Primary constraint:
Hypothesis:
Target population:
Change:
Control/comparison:
Primary metric:
Guardrail metrics:
Eligibility and assignment unit:
Minimum detectable effect or practical threshold:
Expected runtime/sample limitations:
Instrumentation QA:
Decision rule:
Rollback condition:
Owner:
```

Run an experiment to resolve a decision, not to create activity.

## Choosing a method

- Use customer interviews and sales tests when demand is low and the question concerns pain, language, workflow, or willingness to engage.
- Use prototype or concierge tests when the product capability is expensive to build.
- Use sequential offer tests carefully when simultaneous randomization is impractical; account for seasonality and segment differences.
- Use randomized controlled experiments when traffic, assignment, instrumentation, and decision value justify them.
- Use staged rollouts for operational risk; do not mislabel them causal experiments without a valid comparison.

For A/B tests, predefine assignment unit, exposure, metric windows, exclusions, guardrails, practical significance, and stopping rule. Check sample-ratio mismatch and instrumentation before interpreting results. Do not repeatedly peek and stop at a favorable result without a method that supports sequential decisions.

## Prioritization

Rank work using:

- Expected revenue or learning impact.
- Confidence based on evidence quality.
- Time to signal.
- Effort and cash cost.
- Dependency and reversibility.
- Risk to customers, trust, compliance, and operations.

A simple score may help compare similar experiments:

```text
Priority = impact × confidence / effort
```

Do not let pseudo-precise scores overrule dependencies or a severe downside. Show the rationale behind each rating.

## Decision log

After every meaningful test record:

```text
Date:
Decision:
Evidence reviewed:
Result and uncertainty:
What changed:
What did not change:
Follow-up:
Owner and review date:
```

The goal is cumulative learning. Repeated tests without recorded decisions create motion without progress.
