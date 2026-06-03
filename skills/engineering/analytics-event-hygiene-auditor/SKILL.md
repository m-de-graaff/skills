---
name: analytics-event-hygiene-auditor
description: Reviews analytics and tracking for duplicate events, missing funnel events, inconsistent event names, PII leakage, over-tracking, high-cost event volume, analytics in hot render paths, server and client event mismatch, missing attribution fields, and bad revenue or conversion tracking. Use when reviewing product analytics, telemetry, or event schemas.
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
