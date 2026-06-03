# Frontend and API Optimization

Use this reference for browser, React, Next.js, REST, tRPC, GraphQL, payload, and client/server round-trip issues.

## Next.js and React

Look for:

- client components fetching data that could load at the route/server layer.
- child components each fetching session, user, org, feature flags, or permissions.
- sequential server component waterfalls.
- duplicate `fetch` calls with unstable URLs/options.
- missing caching or revalidation strategy.
- large client bundles from server-only dependencies imported into client components.
- API routes proxying internal calls unnecessarily.
- images, fonts, analytics, or SDKs loaded on every page without need.

Recommend:

- hoist route-critical data loading.
- parallelize independent server reads before rendering.
- use stable cache keys.
- split summary and detail payloads.
- keep data-heavy logic on the server.
- avoid client-side request waterfalls after first render.
- use streaming only when it improves perceived latency without multiplying backend work.

Example:

```ts
const [user, org, dashboard] = await Promise.all([
  getCurrentUser(),
  getCurrentOrg(),
  getDashboardSummary(),
]);

return <DashboardPage user={user} org={org} dashboard={dashboard} />;
```

## REST APIs and tRPC

Look for:

- multiple endpoints always called together.
- chained endpoint calls where IDs from the first call feed later calls.
- expensive internal HTTP calls that could be direct server-side service calls.
- missing batch endpoint for common list-detail shapes.
- duplicate validation/auth work across internal calls.

Recommend:

- batch endpoints for common shapes.
- server-side composition for page-level data.
- request coalescing.
- cache headers or revalidation strategy.
- direct service calls inside the backend instead of HTTP-to-self.

Preserve API compatibility unless the user explicitly wants an API change. If changing the API shape, provide migration notes for clients.

## GraphQL

Look for:

- resolver-level N+1 queries.
- missing per-request DataLoader.
- unbounded nested query depth.
- large default fields in list queries.
- duplicate fragments causing payload bloat.
- expensive computed fields requested by default.

Recommend:

- DataLoader per request, keyed by tenant/user-safe identifiers.
- field-level cost awareness.
- persisted queries for high-volume clients.
- query depth and complexity limits.
- lightweight list fragments separate from detail fragments.

DataLoader pattern:

```ts
const userLoader = new DataLoader(async (userIds: readonly string[]) => {
  const users = await db.user.findMany({
    where: { id: { in: [...userIds] } },
  });

  const byId = new Map(users.map((user) => [user.id, user]));
  return userIds.map((id) => byId.get(id) ?? null);
});
```

Scope loaders per request. Never share permissioned loader caches across users or tenants.

## Payload Reduction

Use when network, serialization, hydration, or memory dominates.

Tactics:

- select only needed columns.
- avoid sending large text, blob, JSON, or relation trees in list views.
- paginate large arrays.
- use counts/summaries instead of nested details.
- compress responses.
- resize images through a CDN or image service.
- avoid returning internal-only fields.
- remove duplicate analytics payloads.

Measure:

- response size.
- transferred bytes.
- hydration cost.
- client bundle size.
- cache hit rate.
- p95 route transition time.
