# Engineering and Operations Projects

Use these projects to study implementation choices that affect time-to-value, reliability, security, support, and company operations. Prefer the smallest architecture that can validate the product.

Last reviewed: 2026-09-14.

## Product engineering

| Project | Study it for | Inspect closely | Important limitation |
| --- | --- | --- | --- |
| [Supabase](https://github.com/supabase/supabase) | Integrated database, auth, storage, realtime, and edge functions | Postgres model, row-level security, auth, local development | Platform convenience does not remove schema, security, or migration design |
| [Appwrite](https://github.com/appwrite/appwrite) | Backend services for web and mobile products | Auth, databases, storage, functions, messaging, permissions | Compare operational footprint and service fit before self-hosting |
| [Hasura GraphQL Engine](https://github.com/hasura/graphql-engine) | Data APIs, permissions, events, and metadata-driven systems | Authorization, relationships, actions, events, migrations | Fast API creation can expose a weak data or authorization model faster |
| [Coolify](https://github.com/coollabsio/coolify) | Self-hosted application and database deployment | Deployments, environments, secrets, backups, observability | Self-hosting transfers availability and security work to the team |
| [Trigger.dev](https://github.com/triggerdotdev/trigger.dev) | Durable background jobs and product workflows | Retries, idempotency, schedules, concurrency, observability | Workflow infrastructure should follow a real reliability requirement |
| [Sentry](https://github.com/getsentry/sentry) | Error monitoring and application performance | Issues, traces, releases, ownership, alerts, privacy controls | Instrumentation volume and sensitive data require governance |
| [OpenStatus](https://github.com/openstatusHQ/openstatus) | Synthetic monitoring and public status communication | Monitors, regions, incidents, status pages, alerts | A status page does not replace incident response and recovery design |

## Business operations and finance systems

| Project | Study it for | Inspect closely | Important limitation |
| --- | --- | --- | --- |
| [ERPNext](https://github.com/frappe/erpnext) | Integrated accounting, CRM, inventory, projects, support, and HR | Document model, ledgers, approvals, roles, workflows | ERP implementation can overwhelm an early startup |
| [Bigcapital](https://github.com/bigcapitalhq/bigcapital) | Double-entry accounting and financial reporting workflows | Accounts, journals, invoices, bills, inventory, statements | Software does not replace qualified accounting and tax guidance |
| [Akaunting](https://github.com/akaunting/akaunting) | Small-business accounting and invoicing workflows | Banking, invoices, expenses, reports, modules | Verify current license, extensions, jurisdiction, and controls before adoption |
