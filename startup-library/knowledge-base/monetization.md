# Monetization and Commerce Projects

Use these projects to understand how value becomes entitlements, charges, invoices, payments, and recognized operational events. Pricing strategy comes before billing implementation.

Last reviewed: 2026-09-14.

| Project | Study it for | Inspect closely | Important limitation |
| --- | --- | --- | --- |
| [Lago](https://github.com/getlago/lago) | Subscription, usage, hybrid, credit, entitlement, invoice, and payment orchestration | Billable metrics, plans, wallets, invoices, idempotent events, provider integrations | Powerful infrastructure can be premature for a simple flat subscription |
| [OpenMeter](https://github.com/openmeterio/openmeter) | Metering and billing for AI, API, and infrastructure products | CloudEvents, meters, usage attribution, credits, entitlements, invoice lifecycle | Usage pricing is harmful when customers cannot predict or control the bill |
| [Kill Bill](https://github.com/killbill/killbill) | Mature subscription billing and account lifecycle concepts | Catalogs, subscriptions, invoicing, payments, plugins, state transitions | Operational complexity is substantial for an early product |
| [Polar](https://github.com/polarsource/polar) | Developer-product checkout, subscriptions, benefits, and merchant operations | Products, benefits, orders, subscriptions, webhooks, tax/merchant model | Verify current commercial terms and supported jurisdictions |
| [Hyperswitch](https://github.com/juspay/hyperswitch) | Payment routing and payment operations | Connectors, authorization, retries, routing, fraud, reconciliation | Orchestration is not needed before processor complexity justifies it |
| [Stripe Samples](https://github.com/stripe-samples) | Official payment and subscription implementation examples | Checkout, webhooks, idempotency, customer portal, subscription states | Samples must be matched to current Stripe documentation and production controls |
| [Medusa](https://github.com/medusajs/medusa) | Modular commerce for physical and digital products | Cart, pricing, promotions, inventory, orders, fulfillment, plugins | Commerce primitives do not validate demand, assortment, or unit economics |
| [Saleor](https://github.com/saleor/saleor) | API-first, multi-channel commerce | Products, channels, checkout, taxes, promotions, orders, GraphQL | Enterprise commerce scope can exceed an MVP's needs |
| [Invoice Ninja](https://github.com/invoiceninja/invoiceninja) | Invoicing and payment collection for service businesses | Quotes, recurring invoices, payment status, expenses, client portal | It is an operating reference, not accounting or tax advice |

## Monetization decision order

1. Customer outcome and willingness to pay.
2. Segment and value metric.
3. Packaging, limits, entry model, and expansion.
4. Price level and billing cadence.
5. Entitlement, metering, checkout, invoice, payment, tax, and recovery implementation.
6. Activation, retention, margin, and revenue-cohort review.
