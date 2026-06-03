---
name: vendor-dpa-review
description: Reviews vendors, processors, subprocessors, service providers, contractors, DPAs, SCCs, transfer terms, deletion commitments, security exhibits, and subprocessor disclosures for privacy compliance risk. Use when the user mentions vendor review, DPA, data processing agreement, processor, subprocessor, service provider, contractor, SCCs, international transfers, subprocessors, third-party sharing, procurement privacy review, or AI vendor data use.
---

# Vendor DPA Review

Determine whether a vendor can safely receive or process personal data and what contractual, technical, or operational gaps must be resolved. This is not legal advice; final contract decisions need legal/privacy-owner review.

## Workflow

1. Identify vendor role and whether it is a processor, subprocessor, service provider, contractor, third party, data broker, or independent controller.
2. Identify data shared, purpose, users affected, region, and integration path.
3. Review contract/DPA status, subprocessors, transfer mechanism, deletion/return terms, breach notification terms, audit/security evidence, and AI/training/product-improvement use.
4. Flag technical controls needed: minimisation, field filtering, pseudonymisation, access controls, logging, deletion hooks, retention limits, and consent/opt-out propagation.
5. Produce approval recommendation and remediation issues.

## Vendor Table

```text
Vendor | Role | Data shared | Purpose | Region | Subprocessors | Contract/DPA | Transfer mechanism | Security evidence | Deletion support | Risk
```

## Red Flags

- No signed DPA or equivalent.
- Vendor can use data for its own purposes without clear limits.
- Vendor can train AI models on customer data by default.
- Unclear subprocessors, data location, deletion/return support, breach notification, audit/security evidence, or transfer mechanism.
- Adtech, enrichment, analytics, or AI vendor receiving identifiable data without clear necessity.

## Output

- Approve / Approve with conditions / Reject / Escalate
- Required contract changes
- Required technical changes
- Required product disclosures
- Required procurement/legal review
