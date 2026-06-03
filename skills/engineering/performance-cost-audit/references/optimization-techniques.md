# Optimization Techniques

Use this reference when recommending concrete refactors.

## Batch Many Reads

Use when fetching many records by ID or foreign key.

```ts
const ids = [...new Set(items.map((item) => item.relatedId))];
const related = await getRelatedByIds(ids);
```

Impact:

```text
DB/API round trips: N -> 1 or N -> chunks.
Risk: larger single query payload, parameter limits, memory usage.
```

Preserve output order by mapping results back to the original item order.

## Bulk Writes

Use when writing many independent records:

```ts
await db.event.createMany({ data: events });
```

Risks:

- different error granularity.
- constraint conflict behavior.
- transaction size.
- lock duration.
- retry behavior.

## Request Context

Use when nested helpers repeat current user, tenant, organization, settings, or permission lookups.

```ts
type RequestContext = {
  user: User;
  organization: Organization;
  permissions: PermissionSet;
};

async function buildRequestContext(request: Request): Promise<RequestContext> {
  const user = await requireUser(request);
  const [organization, permissions] = await Promise.all([
    getCurrentOrganization(user.id),
    getPermissionsForUser(user.id),
  ]);

  return { user, organization, permissions };
}
```

Pass the context through service functions instead of re-fetching.

## Persistent Caching

Good candidates:

- feature flags.
- public catalog data.
- pricing tables.
- organization settings.
- permission templates.
- static CMS content.
- deterministic AI responses.
- embeddings by content hash.
- computed aggregates.

Cache keys must include:

```text
tenant/user scope if permissioned
input parameters
version or updated_at marker
locale/currency/region
feature flag variant
prompt/model/version for AI calls
```

Avoid caching secrets, rapidly changing balances/inventory, and permissioned data without safe scope and invalidation.

## Read Models and Materialized Views

Use when expensive joins or aggregates are executed frequently.

Candidates:

- dashboard totals.
- billing usage summaries.
- tenant overview cards.
- feed snapshots.
- search index documents.
- notification counts.

Risks:

- eventual consistency.
- refresh jobs.
- invalidation complexity.
- backfills.
- stale reads.

Include refresh strategy, owner, verification, and fallback behavior.

## Deferred Work

Move non-critical work out of the user response:

- analytics.
- email sending.
- CRM sync.
- recommendations.
- derived-data refresh.
- webhook fan-out.

Prefer durable queues for important work. Post-response tasks can be dropped on some platforms.

## Conditional Work

Skip expensive work when it is not needed:

```ts
if (!includeAnalytics) {
  return basicResult;
}
```

Common gates:

- feature flag disabled.
- user lacks permission to see a section.
- empty input list.
- data unchanged since last run.
- cache hit.
- client did not request optional expansion.

## Remove Duplicate Work Across Layers

Look for the same operation in:

- middleware and route handler.
- server component and client component.
- API route and service function.
- job scheduler and worker.
- webhook handler and downstream sync.

Recommend a single owner for each expensive operation.
