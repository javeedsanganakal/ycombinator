# Sales and Customer Success Projects

Use these projects to study commercial workflows and data models. Start with the sales motion and required evidence; choose software afterward.

Last reviewed: 2026-09-14.

| Project | Study it for | Inspect closely | Important limitation |
| --- | --- | --- | --- |
| [Twenty](https://github.com/twentyhq/twenty) | Modern CRM objects and extensible account workflows | People, companies, opportunities, views, workflows, APIs | A flexible CRM does not define your ICP or stages for you |
| [EspoCRM](https://github.com/espocrm/espocrm) | Mature lead, account, opportunity, campaign, and support concepts | Lead conversion, pipeline reporting, permissions, metadata, REST API | Broad CRM scope may be excessive before a motion is repeatable |
| [Erxes](https://github.com/erxes/erxes) | Connected marketing, sales, service, and engagement workflows | Customer profiles, pipelines, inbox, automation, plugin model | Validate maintenance, deployment, and module fit before adoption |
| [Cal.com](https://github.com/calcom/cal.com) | Scheduling as part of acquisition, sales, onboarding, and support | Routing forms, availability, event types, team assignment, webhooks | Meetings are not pipeline progress unless qualification and next steps are defined |
| [Chatwoot](https://github.com/chatwoot/chatwoot) | Omnichannel sales and support conversations | Inbox assignment, contacts, conversation states, automation, reporting | Conversation volume is not customer value or retention |
| [Formbricks](https://github.com/formbricks/formbricks) | Customer discovery and in-product feedback | Targeting, survey triggers, response schema, segmentation, privacy | Survey answers should be checked against observed behavior and purchase decisions |

## Suggested sequence

1. Model the minimum account, contact, opportunity, stage, and next-action objects.
2. Connect scheduling and conversations to those objects.
3. Add feedback only where a response can change a product or commercial decision.
4. Instrument activation, realized value, renewal risk, and expansion outside the CRM when necessary.
