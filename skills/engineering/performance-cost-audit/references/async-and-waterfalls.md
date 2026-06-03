# Async and Request Waterfalls

Use this reference when a review involves async latency, duplicate fetches, request waterfalls, IO inside loops, or `Promise.all` recommendations.

## Sequential Independent Awaits

Flag independent awaits performed one after another:

```ts
const user = await getUser(userId);
const settings = await getSettings(userId);
const notifications = await getNotifications(userId);
```

If all calls depend only on already-known inputs and do not mutate shared state, use bounded parallelism:

```ts
const [user, settings, notifications] = await Promise.all([
  getUser(userId),
  getSettings(userId),
  getNotifications(userId),
]);
```

Expected impact:

```text
Latency: roughly sum(A, B, C) -> max(A, B, C) plus coordination overhead.
Operation count: unchanged.
Risk: fail-fast semantics and downstream concurrency pressure.
```

## Promise Decision Tree

Before suggesting `Promise.all`, answer:

```text
1. Are operations independent?
   - No: do not parallelize.
2. Are there side effects or ordering requirements?
   - Yes: preserve order or use transactions/queues.
3. Is the number of operations bounded and small?
   - No: batch or use a concurrency limiter.
4. Should one failure fail the whole operation?
   - Yes: Promise.all.
   - No: Promise.allSettled or per-task fallback.
5. Can the downstream service handle parallel load?
   - No: batch, limit, cache, or queue.
```

Use `Promise.allSettled` when partial success is acceptable:

```ts
const results = await Promise.allSettled([
  getOptionalRecommendations(userId),
  getOptionalAnnouncements(userId),
]);
```

Use a concurrency limiter for dynamic lists:

```ts
import pLimit from "p-limit";

const limit = pLimit(8);
const results = await Promise.all(
  items.map((item) => limit(() => processItem(item)))
);
```

Do not replace a loop with unbounded `Promise.all` if it could open hundreds or thousands of database connections, HTTP requests, browser requests, file handles, or paid provider calls.

## IO Inside Loops

Flag `await` inside `for`, `for...of`, `map`, `filter`, or `reduce` when the operation performs IO:

```ts
for (const record of records) {
  await syncRecord(record);
}
```

Preferred fixes, in order:

1. Batch the work into one call if the provider or database supports it.
2. Chunk into provider-safe batches.
3. Use bounded concurrency.
4. Queue or defer when the user response should not block.

## Duplicate Fetches

Detect repeated fetches with the same cache key, URL, or inputs:

```ts
await fetch("/api/me");
await fetch("/api/me");
await fetch("/api/me");
```

Fixes:

- Hoist a shared loader to the route/server boundary.
- Use React Query, SWR, Relay, Apollo, or framework-level request deduping with stable keys.
- Add request-scoped memoization for repeated reads inside one request.
- Combine API routes only when the UI always needs the data together.

Request-scoped memoization pattern:

```ts
const requestCache = new Map<string, Promise<unknown>>();

export function oncePerRequest<T>(key: string, load: () => Promise<T>): Promise<T> {
  if (!requestCache.has(key)) {
    requestCache.set(key, load());
  }

  return requestCache.get(key) as Promise<T>;
}
```

Only use this when the cache is scoped to one request or safely keyed by tenant, user, role, permissions, locale, and feature flag state.

## Request Waterfalls

Look for data loading where one client or server component waits for another component to discover IDs before fetching required data. Common fixes:

- Fetch page-critical data at the route boundary.
- Split list summaries from details.
- Fetch relation data with the initial page query when it is always needed.
- Precompute or cache stable settings, feature flags, and permission templates.
- Keep optional panels behind conditional fetches.
