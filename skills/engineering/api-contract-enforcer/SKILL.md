---
name: "api-contract-enforcer"
description: "Audit API contracts for REST, tRPC, GraphQL, and webhooks: schemas, errors, pagination, idempotency, compatibility."
---

# API Contract Enforcer

Review API boundaries as compatibility contracts, not just implementation details.

## Core checks

- REST route consistency
- OpenAPI or schema coverage
- tRPC/router shape
- GraphQL schema hygiene
- Request validation and response envelopes
- Pagination contracts
- Error format consistency
- Idempotency and retry semantics
- Webhook verification and replay behavior
- Rate-limit behavior and backpressure
- Backwards compatibility and SDK generation

## Output

Return a contract matrix per endpoint or operation with request, response, pagination, errors, idempotency, compatibility, and test coverage.
