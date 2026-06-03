# Database and ORM Optimization

Use this reference when a review involves database round trips, ORM patterns, query shape, pagination, relation loading, or storage IO.

## N+1 Queries

Flag per-row lookups:

```ts
const orders = await db.order.findMany();

for (const order of orders) {
  order.customer = await db.customer.findUnique({
    where: { id: order.customerId },
  });
}
```

Prefer batched loading:

```ts
const orders = await db.order.findMany();
const customerIds = [...new Set(orders.map((order) => order.customerId))];

const customers = await db.customer.findMany({
  where: { id: { in: customerIds } },
});

const customersById = new Map(customers.map((customer) => [customer.id, customer]));

const result = orders.map((order) => ({
  ...order,
  customer: customersById.get(order.customerId) ?? null,
}));
```

Or use joins, relation includes, or eager loading when the ORM emits efficient SQL. Verify generated SQL; some relation loading is multiple-query but still acceptable, while uncontrolled per-row queries are not.

## Preserve Security Filters

Every optimized query must preserve:

- tenant/user/org filters
- role and permission constraints
- soft-delete predicates
- row-level-security assumptions
- ownership checks
- region/data-residency filters

Do not batch across tenants unless the output is partitioned and permission-safe.

## Over-Fetching

Flag full-row or full-tree fetches when only a few fields are used:

```ts
const users = await db.user.findMany();
```

Prefer projections:

```ts
const users = await db.user.findMany({
  select: {
    id: true,
    name: true,
  },
});
```

Avoid loading large JSON, blob, markdown, audit, or text fields in list views. Split list summaries from detail screens.

## Under-Fetching

Flag code that fetches too little and then performs follow-up calls:

```ts
const orders = await getOrders();
const customers = await Promise.all(orders.map((order) => getCustomer(order.customerId)));
```

Prefer a single relation-aware loader or a batched `getCustomersByIds` call.

## Count/List Double Work

This pattern can be correct but expensive:

```ts
const rows = await db.order.findMany({ where, skip, take });
const total = await db.order.count({ where });
```

Alternatives:

- Fetch `limit + 1` rows to compute `hasMore`.
- Use approximate counts when exact counts are not user-critical.
- Cache counts for stable filters.
- Use database-specific window functions when appropriate.
- Move exact counts behind explicit user action.

## Offset Pagination at Scale

Flag large-offset pagination:

```sql
SELECT *
FROM orders
ORDER BY created_at DESC
OFFSET 100000
LIMIT 50;
```

Prefer keyset pagination with a stable tie-breaker:

```sql
SELECT *
FROM orders
WHERE (created_at, id) < ($cursor_created_at, $cursor_id)
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

## Prisma and ORM Layers

Look for:

- `findUnique` inside loops.
- excessive `include` trees.
- missing `select` fields.
- separate writes that could use `createMany`, `updateMany`, or a transaction.
- count/list/aggregate duplication for the same filter.
- raw queries without parameterization.
- missing tenant/user scoping.

Transactions can reduce round trips, but they may increase lock time and transaction pressure. Recommend validation with query logs and database metrics.

## Supabase and PostgreSQL

Look for:

- repeated `.select()` calls per item.
- fetching full rows when only a few columns are needed.
- client-side joins that could be relational selects or an RPC.
- missing `.in()` batching.
- RLS policies causing repeated expensive checks.
- exact counts on large tables.
- overly broad realtime subscriptions.

Always verify RLS remains enforced, tenant filters are present, indexes support the new shape, and payload size is not larger than before.

## MongoDB and Mongoose

Look for:

- queries in loops.
- missing projections.
- large documents read for small fields.
- `$lookup` without supporting indexes.
- unbounded array growth.
- client-side grouping/sorting that belongs in aggregation.
- missing compound indexes for filter plus sort.

Use `.select(...)`, `.lean()`, aggregation pipelines, compound indexes, and `bulkWrite` where appropriate.
