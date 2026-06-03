# Refactor Methodology

Use this reference for significant behavior-preserving refactors.

## Phase 0: Baseline and Safety

Before changing behavior-sensitive code:

- Identify existing tests.
- Run or recommend relevant tests.
- Capture current behavior for fragile paths.
- Add characterization tests if behavior is undocumented.
- Identify public APIs, route contracts, exported functions, CLI flags, event names, database writes, and side effects.
- Identify consumers/callers before moving exports.

Baseline output:

```md
## Baseline

- Existing tests:
- Missing tests:
- Public contracts:
- Risky side effects:
- Suggested characterization tests:
```

## Phase 1: Mechanical Moves

Start with low-risk changes that do not alter logic:

- Move types to focused files.
- Move constants to domain-owned files.
- Extract pure functions without changing implementation.
- Rename ambiguous files only when imports can be updated safely.
- Create folders around coherent features/domains.
- Add compatibility re-exports when many callers depend on old paths.

## Phase 2: Responsibility Split

Separate mixed concerns:

```text
Input validation       -> schema/validation module
Authorization          -> policy/permission module
Business workflow      -> use-case/application module
Database access        -> repository/query module
External provider call -> provider/client module
Response formatting    -> presenter/serializer/mapper module
UI rendering           -> component module
State management       -> hook/store module
```

## Phase 3: Deduplicate

After responsibilities are visible:

- Consolidate duplicate business rules.
- Replace duplicate query fragments with named query builders or repository methods.
- Replace duplicate UI chunks with focused components.
- Replace duplicate validation with shared schema composition.
- Replace duplicate fetch/error/retry code with a small API client wrapper.
- Delete obsolete duplicates after all callers are migrated.

## Phase 4: Simplify Control Flow

Reduce complexity:

- Use guard clauses to remove deep nesting.
- Replace long `if/else` chains with maps only when the mapping is simple and static.
- Split functions by decision, transformation, and side effect.
- Isolate error handling.
- Replace boolean-parameter behavior switches with explicit functions.
- Remove unnecessary state and derived-state duplication.

Guard-clause pattern:

```text
if (!input) return invalidInput();
if (!input.user) return missingUser();
if (!input.user.active) return inactiveUser();
return runWorkflow(input);
```

## Phase 5: Improve Obvious Structural Waste

Only fix waste revealed by the refactor when semantics are clear:

- Avoid repeated expensive calculations inside loops.
- Use `Map`/`Set` for repeated lookups instead of nested scans.
- Move invariant work outside loops.
- Consolidate duplicate fetches/queries through existing data layers.
- Avoid repeated serialization/deserialization.
- Avoid rebuilding schemas, regexes, or clients on every request when safe.
- Replace sequential independent async work with safe concurrency only when dependencies allow it.

Do not turn a structural refactor into a broad performance rewrite. For deeper cost work, produce a separate performance optimization plan.

## Phase 6: Delete, Verify, and Document

After the refactor:

- Delete unused old modules.
- Remove compatibility facades when no callers remain.
- Update imports.
- Update tests.
- Update docs if file paths or architecture changed.
- Run typecheck, lint, unit tests, integration tests, relevant E2E tests, and build.
- Provide rollback notes.

## Dead Code Removal

Dead code signals:

- No imports/callers.
- Exported only through a barrel but never consumed.
- Feature flag permanently disabled or removed.
- Deprecated function with no callers.
- Old API route not linked or registered.
- Old migration helper no longer used.
- Duplicate component replaced by a newer one.
- Comments referencing removed systems.
- Tests for behavior that no longer exists.

Safe deletion process:

1. Confirm no callers through static search.
2. Confirm not used dynamically by string name, route registration, reflection, plugin loading, or framework convention.
3. Confirm not part of a public API or package export.
4. Remove code and related tests only if behavior is obsolete.
5. Run typecheck/tests/build.
6. Document deletion in the refactor summary.

If unsure, mark as `candidate for deletion` instead of deleting immediately.

## Public API and Import Safety

Internal module:

- Move directly if all imports are updated and tests pass.

Public package export:

```ts
// old path, temporary compatibility facade
export { createOrder } from "../features/orders/use-cases/create-order";
```

Route/API contract:

- Do not change URL path, HTTP method, request shape, response shape, status codes, error codes/messages if consumed externally, auth/session semantics, cache headers, or side effects unless explicitly requested.

## Testing Strategy

Before refactoring, add or identify tests for public functions, API routes/controllers, important UI flows, business rules being moved, permission checks, serialization/mapping logic, error cases, and side effects such as emails, jobs, payments, webhooks, and audit logs.

For legacy code with unclear behavior, write characterization tests:

```text
Given current input X
When current module runs
Then current output/side effect Y occurs
```

Do not fix odd behavior during a structural refactor unless the user explicitly asks for a behavior change.
