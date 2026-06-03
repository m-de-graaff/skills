---
name: billing-payments-hardening-review
description: Reviews billing and payments code for webhook idempotency, duplicate event processing, invoice state transitions, subscription downgrade and upgrade edge cases, failed payment recovery, credits balance logic, usage metering, race conditions, refund logic, plan permission syncing, and test clock or sandbox coverage. Use when reviewing Stripe, subscriptions, credits, invoices, or usage-based billing flows.
---

# Billing and Payments Hardening Review

Review money-moving code as a state-machine and edge-case problem, not just a payment-provider integration.

## Core checks

- Webhook idempotency and duplicate delivery
- Invoice, subscription, and payment state transitions
- Upgrade, downgrade, cancel, pause, and resume edge cases
- Failed payment recovery and grace periods
- Credits balance and ledger correctness
- Usage metering and quota reconciliation
- Race conditions between webhooks and user actions
- Refund and dispute handling
- Plan permission syncing
- Test clocks, sandbox coverage, and replay coverage

## Output

Return a money-flow map or state-transition table first. Then call out the highest-risk billing invariants that are missing or duplicated.
