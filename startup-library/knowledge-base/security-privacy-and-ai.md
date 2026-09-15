# Security, Privacy, Accessibility, and AI

Use these primary references to create requirements and review risk. They do not establish that a product is compliant; applicable duties depend on data, users, industry, jurisdiction, contracts, and deployment.

Last reviewed: 2026-09-14.

## Security foundations

| Source | Use it for | Startup application |
| --- | --- | --- |
| [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) | Govern, identify, protect, detect, respond, and recover outcomes | Create a right-sized current and target security profile; assign owners and evidence |
| [NIST CSF 2.0 Small Business Quick-Start resources](https://www.nist.gov/cyberframework/quick-start-guides) | Practical adoption for organizations with modest security programs | Prioritize identity, backups, patching, vendor risk, incident preparation, and governance |
| [OWASP ASVS](https://owasp.org/projects/asvs) | Verifiable web-application security requirements | Select a risk-appropriate level and convert relevant requirements into acceptance tests |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Implementation guidance for common security controls | Review authentication, sessions, secrets, input handling, file uploads, APIs, and logging |
| [OpenSSF Scorecard](https://scorecard.dev/) | Open-source software supply-chain risk signals | Check dependency maintenance, branch protection, signed releases, vulnerabilities, and token permissions |
| [CISA Secure by Design](https://www.cisa.gov/securebydesign) | Product-provider security responsibility and safe defaults | Make MFA, logging, secure defaults, and vulnerability handling part of the product rather than customer cleanup |

## Privacy and accessibility

| Source | Use it for | Startup application |
| --- | --- | --- |
| [NIST Privacy Framework](https://www.nist.gov/privacy-framework) | Privacy-risk identification and management | Map data processing, purposes, roles, risks, controls, and communication |
| [EU GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | European personal-data obligations | Identify roles, lawful basis, rights, processors, transfers, retention, and breach duties with counsel |
| [California CCPA guidance](https://oag.ca.gov/privacy/ccpa) | California consumer privacy rights and business obligations | Determine applicability and required notices, requests, contracts, and controls with counsel |
| [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Current web-content accessibility success criteria | Define target conformance, test keyboard/focus/forms/content, and include people with disabilities in research |

## AI product risk

| Source | Use it for | Startup application |
| --- | --- | --- |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | Govern, map, measure, and manage AI risks | Maintain intended use, affected users, evaluation sets, failure modes, monitoring, and escalation |
| [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | Generative-AI-specific risks and actions | Address confabulation, data privacy, harmful content, information integrity, security, and misuse |
| [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Common LLM application vulnerabilities | Threat-model prompt injection, sensitive disclosure, supply chain, poisoning, output handling, agency, and consumption |
| [EU AI Act official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | EU risk categories and AI-system obligations | Determine role, system classification, prohibited or high-risk use, transparency, documentation, and timing with counsel |

## Minimum launch evidence

- Data inventory with purpose, sensitivity, retention, deletion, and subprocessors.
- Threat model covering users, assets, trust boundaries, abuse cases, and mitigations.
- Authentication, authorization, secrets, encryption, dependency, backup, logging, and incident controls tested in proportion to risk.
- Accessibility review with automated checks plus keyboard, screen-reader, zoom, contrast, error, and content testing.
- For AI: scoped intended use, representative evaluations, safety/security abuse tests, human escalation, cost limits, monitoring, and rollback.
- Public privacy, security contact, support, and truthful capability statements.
