# Stack-Specific Checks

## Next.js / React

Check:

- Server actions and route handlers enforce authz server-side.
- Middleware coverage does not exclude sensitive routes accidentally.
- API routes do not trust client-supplied user, tenant, or role fields.
- `dangerouslySetInnerHTML` is sanitized.
- Server-only secrets are not imported into client components.
- `NEXT_PUBLIC_` variables are intended to be public.
- Redirects validate destination URLs.
- Image/domain proxying does not enable SSRF.
- Preview/draft mode is protected.
- Cookies use Secure, HttpOnly, and SameSite where appropriate.

## Node.js / Express / Fastify / NestJS

Check:

- Global auth and validation middleware ordering.
- Per-route authz guards.
- Raw SQL and dynamic query construction.
- Request body size limits.
- CORS configuration.
- Helmet/security headers.
- File upload middleware limits.
- Error handlers do not leak stack traces in production.
- Prototype pollution risk in object merge/parsing utilities.

## Supabase / PostgreSQL

Check:

- Row Level Security is enabled on tenant/user-owned tables.
- Policies match intended ownership and role model.
- `service_role` key never reaches browser/client code.
- RPC functions use `SECURITY DEFINER` only with strict `search_path` and checks.
- Storage bucket policies enforce ownership.
- Client-side filters are not treated as authorization.
- JWT claims used in policies are stable and trustworthy.
- Admin operations run only server-side.

## Prisma / ORM-Backed Apps

Check:

- `where` clauses include tenant/user ownership filters.
- `findUnique`, `update`, `delete`, and nested writes do not bypass ownership.
- Raw queries are parameterized.
- Mass assignment is prevented.
- Includes/selects do not overexpose sensitive fields.
- Transactions preserve security invariants.

## GraphQL

Check:

- Resolver-level authorization.
- Field-level authorization for sensitive fields.
- Introspection exposure by environment.
- Query depth/complexity limits.
- Batched IDOR through node/global ID loaders.
- Mutations enforce state transitions server-side.

## Stripe / Payments / Subscriptions

Check:

- Prices, totals, quantities, currency, discounts, and plan IDs are validated server-side.
- Webhook signatures are verified.
- Webhook events are idempotent.
- Entitlements are based on trusted payment provider state, not client claims.
- Checkout/session completion cannot be forged.
- Refunds, credits, and coupons require authorization.

## Webhooks

Check:

- Signature verification before parsing/mutating state.
- Timestamp tolerance and replay protection.
- Idempotency keys or processed-event table.
- Provider-specific event type allowlists.
- Error handling does not leak secrets.
- Raw body handling is correct for signature verification.
