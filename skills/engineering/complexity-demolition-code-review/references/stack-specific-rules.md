# Stack-Specific Rules

## TypeScript / JavaScript

- Block `any`, broad `Record<string, any>`, and `object` when the shape is known.
- Treat type assertions after validation as a smell unless they clearly follow a parser or schema.
- Avoid barrel files that expose internals.
- Prefer explicit exported APIs and small pure functions.
- Watch for `Promise.all` without dependency-order, rate-limit, or transaction notes.
- Treat broad `try/catch` blocks that hide control flow as a defect.

## React

- Block components that mix fetching, mutation orchestration, rendering, forms, filters, tables, dialogs, and permissions.
- Block huge prop bags and derived state that should be computed.
- Keep business rules out of render functions and column definitions.
- Prefer focused composition components and narrow hooks.

## Next.js

- Keep route and page files thin.
- Move business workflows out of route handlers and server actions.
- Do not import server-only code into client components.
- Make cache and revalidation behavior explicit.

## Node APIs

- Controllers should not contain inline queries or provider calls.
- Transport files should translate input and output, not own business workflows.
- Move error mapping and persistence logic out of routes and controllers.

## ORM / SQL

- Repositories should answer data questions, not decide business policy.
- Do not duplicate tenant or visibility filters in random call sites.
- Flag N+1 loops and hidden query waterfalls.

## GraphQL

- Keep resolvers thin.
- Use DataLoader or batching when needed.
- Do not turn schema files into domain dumps.

## Monorepos

- Do not let `common`, `shared`, or `utils` become dumping grounds.
- Flag cross-package circular dependencies.
- Keep package APIs intentional and minimal.
