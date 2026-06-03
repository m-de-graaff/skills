# Stack-Specific Guidance

Use this reference when the repository uses one of these stacks.

## TypeScript / JavaScript

Look for:

- Giant `index.ts` barrels.
- Unused exports.
- `any` added to avoid refactor pain.
- Repeated DTOs and API response types.
- Long functions with mixed async side effects.
- Circular imports hidden by barrels.
- Default exports that make large-scale rename/refactor harder.

Prefer named exports for shared modules, feature-local types where possible, `satisfies` and explicit return types on public functions, small pure functions with focused tests, and path aliases only when they clarify architecture.

Avoid replacing every object with a class, generic abstractions that erase domain language, barrel files that expose private internals, and `types.ts` files containing every type in the app.

## React / Next.js

Look for:

- Page components over 300 LOC.
- Components that fetch data, transform data, own filters, render tables, open modals, and submit mutations.
- Repeated loading/error/empty state markup.
- Duplicate form schemas and client/server validation.
- Hooks with many unrelated responsibilities.
- Server components importing client-only code.
- Client components doing server-only work.

Prefer page/layout composition files, feature components with clear props, data hooks for client-side data only, server-side data functions for server components/actions, separate form schema/form component/submit action/result handling, and small UI primitives for repeated visual patterns.

Example:

```text
app/(dashboard)/orders/page.tsx
features/orders/components/orders-table.tsx
features/orders/components/orders-filters.tsx
features/orders/components/order-details-dialog.tsx
features/orders/data/get-orders.ts
features/orders/actions/update-order-status.ts
features/orders/schemas/order-filter.schema.ts
features/orders/types/order.types.ts
```

## Node API / Express / Fastify / NestJS

Look for routes/controllers containing validation, auth, database calls, business logic, email, and response mapping; services with dozens of unrelated methods; middleware doing domain-specific work; repeated error handling and response formatting.

Prefer thin route/controller adapters, dedicated validation schemas, policies/guards for authorization, use-case functions for workflows, repositories/providers for IO, and central error mapping.

## Prisma / Drizzle / SQL

Look for repeated query filters, business rules inside many query call sites, massive repository files, ORM includes copied across routes, and transaction logic mixed with controllers.

Prefer focused repositories by aggregate/domain, named query helpers for repeated filters, explicit transaction boundaries in use cases, mappers for DB-to-API conversions, and tests around complex query conditions.

## Supabase / Firebase

Look for repeated client creation, repeated auth/session/user/profile lookups, RLS assumptions duplicated across UI and server code, query builders copied in many components, and hardcoded collection paths/table names everywhere.

Prefer server/client factory modules with clear runtime boundaries, feature-owned query functions, central table/path constants when stable, permission-aware data-access wrappers, and small typed mappers for response shapes.

## Python

Look for large modules with many unrelated functions, classes used as namespaces only, import cycles between services, repeated Pydantic/serializer schemas, and business logic embedded in views/routes/tasks.

Prefer packages by domain, small modules with explicit imports, pure functions for transformations, service/use-case functions for workflows, repository modules for persistence, and fixtures/factories for repeated test setup.

## Go

Look for huge packages named `service`, `common`, or `utils`; interfaces created before there is more than one implementation; handlers doing persistence and business logic directly; and cyclic package pressure.

Prefer small packages with concrete ownership, interfaces at consumer boundaries, handler/use-case/repository separation for complex flows, explicit error wrapping, and narrow exported APIs.

## Rails / Laravel / Django

Look for fat models, fat controllers, callback-heavy side effects, repeated scopes/query filters, template logic containing business rules, and service objects that become god services.

Prefer query objects/scopes for repeated filters, form/request validators, use-case/service objects with one workflow each, presenters/serializers for response/view shaping, and jobs/events for side effects when appropriate.
