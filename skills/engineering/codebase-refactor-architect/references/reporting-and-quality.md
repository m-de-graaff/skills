# Reporting and Quality

Use this reference for final reports, PR sequencing, metrics, validation, and review.

## Refactor Report

Use this structure for full scans and plans:

~~~md
# Codebase Refactor Report

## Executive Summary

- Highest-impact refactor:
- Biggest god module:
- Biggest duplication source:
- Highest-risk area:
- Recommended PR sequence:

## Current Architecture Snapshot

| Area | Current shape | Problem | Risk |
|---|---|---|---|

## File/Module Hotspots

| Path | LOC | Smells | Action | Priority |
|---|---:|---|---|---|

## God Modules

| Module | Why it is a god module | Split plan | Safety approach |
|---|---|---|---|

## Duplication Findings

| Duplicate pattern | Locations | Consolidation target | Risk |
|---|---|---|---|

## Proposed Target Structure

```text
src/
  ...
```

## Refactor Plan

### PR 1 - Mechanical extraction

- Move:
- Rename:
- Compatibility exports:
- Tests:

### PR 2 - Responsibility split

- Extract:
- Update callers:
- Tests:

### PR 3 - Deduplicate and delete old code

- Consolidate:
- Delete:
- Tests:

## Before/After Metrics

| Metric | Before | After target |
|---|---:|---:|
| Largest file LOC | 3,184 | < 450 |
| Files over 1,000 LOC | 4 | 0 |
| Duplicate rule implementations | 9 | 1 |
| Circular dependencies | 3 | 0 |
| Average route handler LOC | 310 | < 120 |

## Code Changes

Before/after snippets or patch.

## Validation Plan

- Typecheck:
- Lint:
- Unit tests:
- Integration tests:
- E2E/manual checks:

## Risks and Rollback

- Risk:
- Mitigation:
- Rollback:
~~~

Use tildes for outer fences if embedding this template in Markdown that contains nested code fences.

## Final Response Requirements

Always include:

1. Biggest structural problems found.
2. God modules or oversized files to split first.
3. Duplication patterns worth removing.
4. Proposed target structure.
5. Safest PR sequence.
6. Before/after metrics where possible.
7. Exact code patches or representative before/after snippets when code was provided.
8. Tests or validation steps.
9. Risks and what not to change.

## Review Checklist

Structure:

- No modified source file remains above the agreed size threshold unless justified.
- No 3,000-line source file remains unaddressed unless generated or explicitly exempted.
- Every extracted module has one clear responsibility.
- No new vague `utils/helpers/common` dumping ground was created.
- Imports point in the intended architectural direction.
- No new circular dependencies were introduced.
- Public APIs remain compatible or migration wrappers are provided.

Duplication:

- Duplicated business rules are consolidated.
- Duplicated validation is consolidated or intentionally local.
- Duplicated query filters/includes are consolidated where safe.
- Duplicated UI patterns are componentized where useful.
- Removed code is actually unused or obsolete.

Behavior:

- Tests cover moved behavior.
- Authorization behavior is unchanged.
- Error behavior is unchanged unless explicitly changed.
- Database transaction behavior is unchanged.
- External side effects are unchanged.
- User-facing UI behavior is unchanged unless explicitly changed.

Quality:

- Typecheck passes.
- Lint passes.
- Relevant unit tests pass.
- Relevant integration/E2E tests pass.
- Build passes.
- The refactor can be reviewed in logical commits or PRs.
- Rollback path is clear.

## Example Summary

~~~md
## Refactor Summary

The main issue is `src/services/customer-service.ts` at 3,184 LOC. It is a critical god module because it handles customer profiles, billing, subscriptions, emails, imports, analytics, and permission checks in one file.

Recommended split:

```text
features/customers/customer.repository.ts
features/customers/update-customer.use-case.ts
features/billing/subscription.repository.ts
features/billing/calculate-proration.ts
features/notifications/customer-email.service.ts
features/imports/customer-import.service.ts
auth/customer.policy.ts
```

PR sequence:

1. Add characterization tests for the current public methods.
2. Extract pure billing calculations and status mapping.
3. Extract repositories without changing callers.
4. Create focused use cases and keep a temporary compatibility facade.
5. Migrate callers.
6. Delete the old god module.
~~~
