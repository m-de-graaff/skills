# Cloud and Provider Costs

Use this reference for paid API usage, serverless/runtime spend, queues, logs, analytics, AI calls, embeddings, and provider-side billing units.

## Cost Model

Use actual numbers when available. Otherwise state assumptions:

```text
Current cost = executions * operations per execution * unit cost
Proposed cost = executions * optimized operations per execution * unit cost + added cache/storage/job cost
Savings = current cost - proposed cost
Reduction percent = savings / current cost
```

Latency estimates:

```text
Sequential latency ~= A + B + C
Parallel latency ~= max(A, B, C) + coordination overhead
Batched latency ~= batch query latency + mapping overhead
Cached latency ~= cache lookup latency on hit, origin latency on miss
```

## External API Calls Inside Loops

Flag:

```ts
for (const customer of customers) {
  customer.score = await enrichmentApi.score(customer.email);
}
```

Preferred fixes:

- provider batch endpoint.
- chunked requests with concurrency limits.
- cache lookup before provider call.
- deferred enrichment job.
- enrich only changed records.
- store provider response with TTL or version stamp.

If no batch endpoint exists, use bounded concurrency and backoff. Respect provider rate limits and retry semantics.

## AI and LLM Cost Waste

Scan for:

- sending full documents when snippets would work.
- re-sending unchanged context.
- no prompt/result cache for deterministic calls.
- high-cost model used for simple classification or formatting.
- recomputing embeddings for unchanged text.
- no batching for embeddings.
- large structured output where small JSON would do.
- verbose prompts or redundant system instructions.
- no token budget or max output limit.

Cost-reduction tactics:

1. Hash normalized input and cache deterministic responses.
2. Store embeddings by content hash.
3. Batch embedding requests.
4. Route simple tasks to cheaper models if quality permits.
5. Retrieve or summarize only relevant context before generation.
6. Strip HTML and boilerplate before sending text.
7. Cap output tokens.
8. Reuse intermediate results only when privacy-safe.

Evidence template:

```text
Current:
- 1,000 AI calls/day
- Average input: 8,000 tokens
- Average output: 1,000 tokens
- 40% of calls repeat identical normalized input

Proposed:
- Cache deterministic calls by normalized input hash
- Reduce average input to 3,500 tokens through retrieval/truncation
- Cap output at 400 tokens

Expected:
- Paid calls: 1,000 -> about 600
- Input tokens: 8M/day -> about 2.1M/day
- Output tokens: 1M/day -> about 240k/day
```

## Serverless and Runtime Costs

Look for:

- functions invoked once per tiny item instead of batching.
- long cold-start paths with unnecessary imports.
- internal HTTP calls between colocated server functions.
- expensive work in middleware that runs on every request.
- logs or analytics emitted for every retry or loop item.
- edge functions doing heavy CPU work better suited to a job worker.

Recommend:

- batch units of work.
- move non-critical work to durable queues.
- hoist static configuration to module scope.
- avoid self-HTTP inside the same backend.
- sample or aggregate high-volume logs.
- place CPU-heavy work on an appropriate runtime.

## Queues, Jobs, and Webhooks

Look for:

- one job per tiny item when batching is possible.
- retry storms.
- jobs repeatedly fetching the same account/config.
- webhooks performing full syncs instead of deltas.
- duplicate event processing without idempotency keys.
- high-severity logs for every normal retry.

Recommend:

- batch by tenant/account/time window.
- idempotency keys or processed-event tables.
- deduplication locks where appropriate.
- backoff and jitter.
- partial failure handling.
- storing provider payloads only when needed.

## Logs and Analytics

Do not remove needed observability. Instead:

- sample noisy debug logs.
- aggregate repeated metrics.
- redact large payloads, tokens, and personal data.
- lower severity for expected retries.
- move high-volume diagnostic detail to cheaper storage.
- avoid duplicate analytics events across client and server.

Track before/after event volume and billable ingestion units.
