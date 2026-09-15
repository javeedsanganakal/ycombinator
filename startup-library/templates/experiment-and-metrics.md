# Experiment and Metrics Contract

Owner:
Decision date:
Product version and evidence window:

## Metric contract

| Field | Definition |
| --- | --- |
| Metric name and business question |  |
| Unit: event/person/account/logo/subscription/revenue |  |
| Numerator |  |
| Denominator and eligibility |  |
| Time window and timezone |  |
| Segment and cohort |  |
| Source tables/events and identity logic |  |
| Exclusions, late data, duplicates, refunds |  |
| Owner and validation query |  |

## Experiment brief

- Observed problem and baseline:
- Evidence for the proposed cause:
- Hypothesis: If `[change]` for `[eligible segment]`, then `[primary metric]` will change because `[mechanism]`.
- Control and treatment:
- Assignment unit and exposure event:
- Primary metric:
- Guardrail metrics:
- Sample/duration rationale and analysis method:
- Instrumentation QA:
- Operational, privacy, accessibility, and customer risks:
- Stop, continue, ship, rollback, or iterate rules:

## Result

| Item | Finding |
| --- | --- |
| Enrollment, exposure, and exclusions |  |
| Primary effect and uncertainty |  |
| Guardrails |  |
| Segment differences declared in advance |  |
| Data-quality issues |  |
| Decision |  |
| Follow-up owner and date |  |

Do not call a result causal when assignment, exposure, instrumentation, or analysis does not support that conclusion.
