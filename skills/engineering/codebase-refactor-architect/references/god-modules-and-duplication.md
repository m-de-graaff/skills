# God Modules and Duplication

Use this reference to identify modules that do too much and duplication that should be consolidated.

## God Module Signals

Flag a module when several signs are present:

- 1,000+ lines, especially 3,000+ lines.
- Many unrelated exports.
- Handles multiple domains such as users, billing, orders, analytics, notifications, and permissions.
- Mixes UI rendering, data fetching, validation, transformation, authorization, side effects, logging, and persistence.
- Contains many feature flags or branching paths for unrelated behavior.
- Imports from many layers and features.
- Causes circular dependencies.
- Has a vague name: `manager`, `service`, `helper`, `utils`, `controller`, `core`, `common`, `processor`.
- Requires many unrelated tests to change one small behavior.
- Frequently appears in merge conflicts.
- Has comments like "do not touch", "temporary", "legacy", "special case", or "TODO refactor".
- Cannot be explained in one sentence.

## God Module Classification

```text
God component: UI file doing rendering, state, data fetching, forms, tables, modals, and business logic.
God hook: hook managing unrelated async operations, global state, effects, routing, forms, and data transforms.
God service: backend service containing many use cases, repositories, providers, and side effects.
God controller/route: request handler doing auth, validation, orchestration, database work, provider calls, and response shaping.
God repository: database layer mixing unrelated tables/domains and business rules.
God util: generic helper file that became a junk drawer.
God type file: giant type/schema file where unrelated concepts accumulate.
God store: global state module containing unrelated feature state and actions.
God package: shared package that imports the world and becomes a cross-app coupling point.
```

## Decomposition Strategy

Do not split randomly by line number. Split by responsibility.

Preferred extraction order:

1. Types and schemas: move validation schemas, DTOs, types, and constants near the feature/domain that owns them.
2. Pure helpers: extract deterministic transformations and calculations into named modules with focused tests.
3. IO boundaries: separate database queries, external API calls, file/storage access, queue publishing, email, and analytics.
4. Use cases: isolate business workflows as functions/classes that orchestrate pure logic and IO ports.
5. UI subcomponents: split large components into layout, filters, lists/tables, dialogs, forms, cards, and empty/error/loading states.
6. State hooks: extract local state machines, form state, filtering/sorting state, and data-loading hooks only when they have a coherent purpose.
7. Compatibility facade: for risky public modules, keep a temporary facade that re-exports or delegates to new modules while callers migrate.
8. Caller migration: update imports gradually, then delete the facade when no callers remain.

## Duplication Types

Find duplication at multiple levels:

```text
Exact duplication: identical blocks copied across files.
Near duplication: same structure with renamed variables or small condition differences.
Semantic duplication: same business rule expressed differently in multiple places.
Validation duplication: repeated schemas, regexes, required-field lists, or error messages.
Query duplication: repeated database filters, includes, joins, select lists, or authorization constraints.
API duplication: repeated fetch wrappers, headers, auth handling, retry logic, or error parsing.
UI duplication: repeated cards, tables, modals, form rows, empty states, status badges, or loading states.
Type duplication: repeated DTOs, enums, unions, interfaces, and response shapes.
Constant duplication: repeated magic strings, status names, event names, route paths, permission names, feature flags, and configuration values.
Test duplication: repeated setup factories, mocks, fixtures, and assertions.
```

## Duplication Rules

- Business rules need one owner. Consolidate billing, permissions, inventory, eligibility, validation, pricing, or compliance rules into named domain modules.
- Do not create vague abstractions. Prefer `calculateSubscriptionProration` over `calculateThing` or `processData`.
- Abstract only the stable part. If two flows share parsing but differ in authorization and side effects, extract parsing only.
- Keep tests readable. Test duplication is acceptable when it makes behavior explicit; abstract setup only when repetition obscures intent.
- Avoid kitchen-sink utilities. Create focused modules such as `orders/status.ts`, `billing/proration.ts`, `auth/permissions.ts`, or `ui/status-badge.tsx`.

## Common Anti-Patterns

- 3K-line files treated as normal.
- One `services.ts` file containing the whole backend.
- One `Dashboard.tsx` component containing an entire product area.
- `utils.ts` with unrelated business logic.
- `types.ts` with every type in the application.
- Barrels that export private internals and hide dependency cycles.
- Components that fetch data, mutate data, own complex state, and render large UI all at once.
- API routes that do everything inline.
- Copy-pasted permission checks, status mappings, form validation, and database filters.
- Boolean parameters that change entire workflows.
- Long functions with many hidden side effects.
- Deeply nested conditionals.
- Circular dependencies between features.
- Global state stores containing unrelated domains.
- Comments explaining confusing code instead of improving the structure.
