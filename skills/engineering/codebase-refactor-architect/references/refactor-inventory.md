# Refactor Inventory

Use this reference to build the first-pass map before editing code.

## Project Shape

Detect and summarize:

```text
Project type: web app, API, library, CLI, mobile app, worker, monorepo, design system, data pipeline.
Languages: TypeScript, JavaScript, Python, Go, Rust, PHP, Ruby, Java, C#.
Frameworks: Next.js, React, Vue, Svelte, Remix, Express, Fastify, NestJS, Django, Flask, Rails, Laravel, Spring.
Package manager/build: npm, pnpm, yarn, bun, pip, uv, poetry, cargo, go, maven, gradle, composer.
Architecture style: feature folders, layered, MVC, hexagonal, clean architecture, package-by-type, package-by-feature, monolith, services.
Testing: unit, integration, E2E, snapshots, contract tests, coverage tooling.
Runtime-critical areas: routes, jobs, webhooks, server actions, API handlers, database layer, frontend data fetching, billing, auth, checkout, import/export.
```

## File and Module Inventory

Rank source files by refactor priority.

Track:

```text
Path:
Lines of code:
Exports:
Imports:
Primary responsibility:
Secondary responsibilities:
Public API or internal module:
Tests covering it:
Known callers:
Churn if git history is available:
Risk level:
Recommended action:
```

Example:

```md
| Path | LOC | Exports | Responsibilities | Risk | Action |
|---|---:|---:|---|---|---|
| app/api/orders/route.ts | 482 | 2 | auth, validation, SQL, payment, email, response mapping | High | Split into route, schema, use case, repository, notification service |
| src/lib/customer-service.ts | 3,184 | 47 | customers, billing, subscriptions, emails, imports, analytics | Critical | Decompose into domain modules; add compatibility facade temporarily |
| components/Dashboard.tsx | 1,126 | 1 | layout, data fetching, filtering, charts, table, modal state | High | Split container, hooks, charts, table, filters, dialogs |
```

## File Size Thresholds

Use thresholds as signals, not absolute laws. Review any file that exceeds warning levels.

| File/module type | Healthy range | Warning | Critical |
|---|---:|---:|---:|
| React component | 50-250 LOC | 300+ LOC | 600+ LOC |
| Next.js page/route handler | 50-200 LOC | 250+ LOC | 500+ LOC |
| API controller/handler | 50-250 LOC | 300+ LOC | 700+ LOC |
| Service/use-case module | 80-350 LOC | 500+ LOC | 1,000+ LOC |
| Repository/query module | 80-400 LOC | 600+ LOC | 1,000+ LOC |
| Utility module | 20-200 LOC | 300+ LOC | 600+ LOC |
| Type/schema file | 50-400 LOC | 700+ LOC | 1,200+ LOC |
| Test file | 50-500 LOC | 800+ LOC | 1,500+ LOC |
| Any source file | - | 1,000+ LOC | 3,000+ LOC |

A 3,000-line source file is a critical architecture smell unless generated, a checked-in snapshot, a migration, or a deliberate data fixture.

## Function and Class Thresholds

| Unit | Warning | Critical |
|---|---:|---:|
| Function length | 50+ LOC | 100+ LOC |
| Class length | 250+ LOC | 500+ LOC |
| Function parameters | 5+ | 8+ |
| Nested blocks | 3+ levels | 5+ levels |
| Branches in function | 6+ | 12+ |
| Responsibilities in a unit | 2+ | 4+ |
| Direct dependencies/imports | 12+ | 20+ |

## Export and Responsibility Thresholds

| Smell | Warning | Critical |
|---|---:|---:|
| Exports from one source file | 8+ | 20+ |
| Public exports from an `index.ts` barrel | 25+ | 75+ |
| Feature folders imported by one module | 4+ | 8+ |
| Distinct domains in one file | 2+ | 4+ |
| Different IO systems in one function | 2+ | 4+ |

## Priority Model

Impact factors:

```text
+3 File is 1,000+ LOC
+5 File is 3,000+ LOC
+3 Module mixes 4+ responsibilities
+3 Code is on hot path
+2 Code changes often
+2 Code has repeated bugs
+2 Duplicated business rule exists in 3+ places
+2 Module blocks other refactors
+1 Weak naming or folder placement causes confusion
```

Risk factors:

```text
+5 Payment, auth, permissions, billing, migrations, or data deletion
+4 Public API/package export
+4 Weak or missing tests
+3 Complex database transactions
+3 External provider side effects
+2 Async/concurrency behavior
+2 Framework convention file
+1 UI-only behavior with visual risk
```

Recommended action:

```text
High impact / low risk: refactor first.
High impact / high risk: add characterization tests, split into multiple PRs.
Low impact / low risk: batch with nearby cleanup.
Low impact / high risk: defer unless blocking current work.
```
