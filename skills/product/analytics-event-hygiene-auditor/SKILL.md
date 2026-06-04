---
name: "analytics-event-hygiene-auditor"
description: "Audit analytics events: duplicates, funnels, naming, PII leakage, attribution, revenue metrics, volume cost."
---

# Analytics Event Hygiene Auditor

Review instrumentation as a product-data contract and a vendor-cost surface.

## Core checks

- Duplicate events and event storms
- Missing funnel events
- Inconsistent event names and schemas
- PII leakage into event payloads
- Over-tracking and noisy instrumentation
- High-cost event volume
- Analytics in hot render paths
- Server and client event mismatch
- Missing attribution fields
- Revenue and conversion tracking correctness

## Output

Return an event inventory grouped by funnel or surface, then call out duplicate, missing, inconsistent, or privacy-sensitive events first.
