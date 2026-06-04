---
name: "data-map"
description: "Map personal data: inventories, ROPA, vendors, retention, logs, databases, privacy flows."
---

# Data Map

Produce a practical personal-data map that can feed privacy reviews, DPIAs, privacy request workflows, retention work, vendor reviews, and incident assessments.

## Ground Rules

- This is engineering and compliance support, not legal advice.
- Inspect provided code, schemas, infra, event payloads, logs, vendor lists, analytics config, and policies directly.
- Separate confirmed facts from assumptions and unknowns.
- Do not include live personal data values unless strictly necessary; describe categories instead.
- Flag legal or compliance decisions for privacy-owner review.

## Workflow

1. Identify systems: databases, APIs, logs, queues, object storage, analytics, support tools, CRM, email, payments, warehouses, backups, AI prompts/completions, uploads, webhooks, and vendors.
2. Identify personal data, sensitive data, inferred data, identifiers, telemetry, and derived profiles.
3. Map collection, transmission, storage, access, processing, sharing, retention, deletion, export, and backup expiry paths.
4. Flag unknowns and risky flows: undefined retention, personal data in logs, overbroad analytics, vendor exposure, missing delete/export path, unowned systems, excessive collection, region ambiguity, and AI/training reuse.
5. Produce remediation issues with acceptance criteria.

## Output

Use this table:

```text
Data element | Category | Sensitive? | Source | Purpose | System | Vendor/recipient | Region | Retention | Delete path | Export path | Risk | Open questions
```

Then include:

```text
## System inventory
Systems reviewed and evidence sources.

## Data flow summary
Collection, processing, sharing, retention, deletion, export, backup, and logging paths.

## Findings
Evidence | Risk | Recommended fix | Acceptance criteria | Owner

## Remediation backlog
Implementation-ready issues.

## Open questions
Legal/compliance, product, engineering, and vendor questions.
```

For large data maps, run `scripts/validate_data_map.py` when practical.
