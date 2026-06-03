---
name: background-jobs-queue-review
description: Reviews queues, cron jobs, workers, and scheduled tasks for retries, idempotency, dead-letter queues, job locking, duplicate execution, race conditions, timeout behavior, queue cost, batch size, memory usage, observability, cron overlap, and backpressure. Use when reviewing worker systems, scheduled jobs, or asynchronous processing.
---

# Background Jobs and Queue Review

Review production job systems for failure handling and repeat-execution safety.

## Core checks

- Retry policy and retry storms
- Idempotency and duplicate execution
- Dead-letter queues and poison jobs
- Job locking and lease expiry
- Race conditions and overlapping schedules
- Timeout behavior and partial progress
- Queue cost, batch size, and throughput
- Memory usage and payload size
- Observability, logs, and replayability
- Cron overlap and backpressure

## Output

Return a job-by-job matrix with trigger, retry, idempotency, lock, timeout, DLQ, overlap risk, observability, and cost notes.
