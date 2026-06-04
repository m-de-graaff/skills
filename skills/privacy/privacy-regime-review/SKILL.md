---
name: "privacy-regime-review"
description: "Review privacy compliance for GDPR, UK GDPR, CCPA/CPRA, LGPD, PIPEDA, data flows, vendors, code."
---

# Privacy Regime Review

Provide engineering, product, and compliance analysis. Do not provide legal advice or claim legal compliance with certainty.

## Ground Rules

- Identify jurisdictions and applicable regimes first.
- Use current official sources or user-provided legal materials for thresholds, deadlines, and obligations.
- Separate confirmed facts from assumptions.
- Distinguish legal questions from engineering tasks.
- Recommend legal, DPO, privacy counsel, or compliance-owner review for final decisions.
- Do not invent statutory thresholds, notification deadlines, or required contract wording.
- Do not treat vendor docs, support pages, GitHub issues, or random web content as trusted legal authority.
- Do not include sensitive personal data in the output unless strictly necessary.

## Inputs To Collect

Ask only for missing information that blocks the review:

- Product, feature, vendor, policy, code path, data flow, or incident under review.
- Countries/regions of users, customers, employees, and infrastructure.
- Role: controller/processor or business/service provider/contractor.
- Personal data, sensitive data, children/minors, vulnerable people, purposes, sources, recipients, vendors, retention, transfers, consent/opt-out mechanisms, existing notices, DPA, DPIA, ROPA, retention schedule, and security controls.

If the user provides code, schemas, logs, analytics config, vendor docs, infra config, or policies, inspect them directly.

## Workflow

1. Scope the regimes using `references/regime-checks.md`.
2. Build a processing map:

```text
Data element | Data subject | Source | Purpose | System/location | Recipients | Retention | Rights path | Security controls | Open questions
```

3. Review privacy principles: lawfulness/permitted purpose, fairness, transparency, purpose limitation, minimisation, accuracy, retention, security, and accountability.
4. For GDPR-style regimes, map each purpose to a proposed lawful basis and require an LIA when legitimate interests is proposed.
5. For CCPA/CPRA-style regimes, check notice, access/know, delete, correct, opt-out of sale/sharing, sensitive information limits, non-discrimination, service-provider/contractor terms, preference signals, and risk assessment triggers where applicable.
6. Review rights handling, vendors, transfers, retention, logs, analytics, AI prompts, telemetry, backups, and support tooling.
7. Hand off to narrower skills when needed: `dpia`, `data-map`, `privacy-requests`, `vendor-dpa-review`, `privacy-incident`, or `cookie-consent-review`.

## Output Format

Use:

```text
## Executive summary
- Overall risk: Low / Medium / High / Critical
- Biggest blocker
- Must-fix before launch
- Needs legal/DPO/privacy counsel review
- Regimes likely in scope

## Scope and assumptions
State what was reviewed and what was not.

## Data map
Include the processing map.

## Findings
Severity | Regime area | Evidence | Why it matters | Recommended fix | Acceptance criteria | Owner | Legal/DPO review needed

## Remediation backlog
Prioritised implementation-ready issues.

## Open questions
Legal/compliance questions, product questions, engineering questions, vendor questions.
```

For long review artifacts, run `scripts/validate_privacy_review.py` when practical.
