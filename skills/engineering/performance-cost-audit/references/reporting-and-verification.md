# Reporting and Verification

Use this reference when producing the final audit, prioritizing findings, or designing validation.

## Severity

| Severity | Meaning |
|---|---|
| Critical | Outage risk, unbounded cost growth, severe N+1, or paid provider runaway. |
| High | Hot-path issue with large latency or cost reduction potential. |
| Medium | Noticeable inefficiency with moderate cost or latency impact. |
| Low | Cleanup or small optimization with limited measurable effect. |
| Info | Observation, instrumentation gap, or optional improvement. |

## Confidence

| Confidence | Meaning |
|---|---|
| Confirmed | Direct code evidence plus clear runtime/cost implication. |
| Probable | Strong code evidence; runtime frequency not proven. |
| Needs measurement | Code smell exists, but impact depends on production usage. |
| Speculative | Possible improvement, but more data is needed before changing. |

## Finding Template

```md
### 1. [Title]

**Severity:** High
**Confidence:** Confirmed
**Location:** `path/to/file.ts:120`
**Pattern:** N+1 query / sequential await / duplicate API call / etc.

**Current behavior:**
Describe current code behavior and operation count.

**Why it is expensive:**
Explain round trips, provider calls, payload size, compute, or latency waterfall.

**Recommended change:**
Describe the specific refactor.

**Estimated impact:**
DB calls: 101 -> 3
Reduction: about 97%
Assumptions: 50 rows per page.

**Risks / correctness notes:**
List auth, cache invalidation, transaction, rate-limit, ordering, or error-handling risks.

**Verification:**
- Add regression test.
- Compare query logs.
- Measure p95 latency and provider-call count.
```

## Patch Plan

Group work into:

1. Safe quick wins.
2. Medium-risk refactors.
3. Larger architecture changes.

Do not bury high-impact hot-path fixes below low-impact cleanup.

## Test Scenarios

For each optimization, recommend at least one.

- Same output before and after.
- Empty input returns quickly without avoidable queries.
- Duplicate IDs are de-duplicated while output order is preserved.
- Missing related records behave the same.
- Auth, tenant, role, and row-level-security boundaries are preserved.
- Errors still propagate or degrade as intended.
- Query count drops for a representative fixture.

Query-count example:

```text
Given 50 orders with customers:
Before: 51 queries.
After: 2 queries.
```

## Runtime Measurement

Measure:

- p50, p95, and p99 latency.
- database query count per route/job.
- slow query logs.
- external API call counts.
- cache hit rate.
- payload size.
- function duration.
- memory usage.
- error/retry rate.
- provider billable units.

## Instrumentation Plan

Add or verify:

- query count logging for hot routes.
- timing spans around expensive service calls.
- provider-call counters.
- cache hit/miss metrics.
- job queue depth and retry counters.
- before/after cost dashboard.

## Rollout Plan

For risky changes, include:

- feature flag name or scope.
- canary percentage or tenant cohort.
- metrics to watch.
- rollback trigger.
- data backfill or invalidation plan if needed.

## Validator

Run:

```bash
python skills/engineering/performance-cost-audit/scripts/validate_performance_audit.py path/to/audit.md
```

Use `--json` for machine-readable output.
