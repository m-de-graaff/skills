---
name: "billing-payments-hardening-review"
description: "Review billing and payments: Stripe, invoices, subscriptions, credits, webhooks, metering, refunds, plan sync."
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
