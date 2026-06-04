---
name: dpia
description: Screen, draft, or review DPIAs/PIAs for high-risk processing, profiling, automated decisions, AI, sensitive data, GDPR.
---

# DPIA

Prepare DPIAs and similar privacy risk assessments. Do not provide legal advice or mark a DPIA as approved.

## Ground Rules

- Verify current official DPIA or risk-assessment guidance for the relevant regime.
- Focus on risks to people, not only risks to the organisation.
- Separate inherent risk, mitigations, and residual risk.
- Produce implementation-ready remediation issues.
- Escalate high residual risk to legal, DPO, privacy counsel, or a senior risk owner.
- Do not hide unknowns or treat security controls as sufficient if purpose, necessity, proportionality, or rights issues are unresolved.
- Do not copy sensitive personal data into the DPIA unless strictly necessary.

## Use Cases

Use for new personal-data features, AI/ML on personal data, profiling/scoring/ranking, automated decision support, sensitive data, children, employee monitoring, location tracking, large-scale processing, systematic monitoring, cross-context matching, adtech/tracking, biometrics, identity verification, surveillance, and high-impact decisions.

## Workflow

1. Screen whether a DPIA or similar assessment is likely needed. See `references/dpia-screening.md`.
2. Describe the processing: feature, owner, roles, data subjects, data categories, sources, purposes, operations, systems, recipients, retention, transfers, disclosures, rights paths, and security controls.
3. Assess necessity and proportionality: specific purpose, data minimisation, less intrusive alternatives, retention, transparency, rights, vendors, and transfers.
4. Identify risks to people:

```text
Risk | Affected people | Cause | Likelihood | Severity | Inherent risk | Existing controls | Residual risk | Owner
```

5. Define mitigations: minimisation, purpose narrowing, pseudonymisation, aggregation, local processing, shorter retention, access controls, encryption, audit logs, human review, appeal path, consent/opt-out, transparency, vendor restrictions, model safeguards, bias/fairness checks, accuracy validation, abuse monitoring, deletion/export support, and logging redaction.
6. Decide residual risk: Low, Medium, High, or Critical. High or Critical residual risk blocks launch or requires formal escalation.
7. Produce implementation issues.

Use `references/dpia-template.md` for full DPIA artifacts.

## Output Format

```text
## DPIA screening result
DPIA needed, rationale, legal/DPO review needed, blocking unknowns.

## Processing description
Data map and system overview.

## Necessity and proportionality
Purpose, data minimisation, rights, retention, transparency, vendor and transfer concerns.

## Risk assessment
Risk table.

## Mitigations
Required controls and product/code changes.

## Residual risk decision
Proceed / Proceed with conditions / Do not launch / Escalate before launch.

## Remediation backlog
Prioritised implementation issues.

## Open questions
Legal, product, engineering, and vendor questions.
```

For long DPIA artifacts, run `scripts/validate_dpia.py` when practical.
