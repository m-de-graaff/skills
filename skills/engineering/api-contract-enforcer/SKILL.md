---
name: api-contract-enforcer
description: Reviews API boundaries for REST, tRPC, GraphQL, and webhooks, checking route consistency, OpenAPI coverage, router shape, schema hygiene, request validation, response envelopes, pagination contracts, error format consistency, idempotency, webhook verification, retry behavior, rate-limit behavior, backwards compatibility, and SDK or client generation. Use when reviewing API boundaries or integration surfaces.
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
