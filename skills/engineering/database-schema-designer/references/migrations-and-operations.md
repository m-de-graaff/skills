# Migrations and Operations

## Migration Standards

Every migration should include:

- Clear migration name and purpose.
- Up migration.
- Down or rollback migration when safe.
- Notes for large tables.
- Locking and downtime risk.
- Backfill plan for non-null columns and derived data.
- Batch size guidance for large backfills.
- Validation queries.
- Deployment order for expand/contract changes.

Use expand/contract migrations for risky production changes:

1. Add nullable column or new table.
2. Backfill in batches.
3. Dual-write or sync if needed.
4. Validate counts, constraints, and query results.
5. Switch reads.
6. Enforce NOT NULL and constraints.
7. Drop old column or table in a later release.

## Production Safety

- PostgreSQL: use CREATE INDEX CONCURRENTLY for large production indexes and remember it cannot run inside a transaction block.
- PostgreSQL: add large-table foreign keys and checks with NOT VALID, then VALIDATE CONSTRAINT.
- MySQL/MariaDB: verify online DDL support by version and storage engine.
- SQL Server: state lock, isolation, and online index rebuild implications when relevant.
- For large backfills, process batches by primary key or partition key and pause between batches when needed.
- Always include validation queries after data movement.

## Partitioning, Sharding, and Retention

Use partitioning only when it improves pruning, retention, bulk deletion, maintenance, write distribution, or index size.

Good reasons:

- Large append-only event, log, metric, order, or audit tables.
- Retention windows requiring fast drop/archive by time.
- Very large tenant-scoped datasets.
- Hot/cold data separation.
- Reducing index size per partition.

Avoid partitioning when:

- The table is small or moderate.
- Queries cannot prune partitions.
- It adds complexity without reducing query cost.
- It creates too many tiny partitions.

Common strategies:

- Time range partitioning for events, logs, orders, metrics, and audit records.
- Hash partitioning to distribute writes.
- Tenant/list partitioning only for very large tenants or strict isolation.
- Hybrid partitioning only with clear query and retention justification.

Retention guidance:

- Prefer dropping partitions over row-by-row deletes for large time-based retention.
- Use archived_at, cold storage export, or historical tables when lifecycle requires it.
- For soft deletes, pair deleted_at with partial indexes and cleanup jobs where supported.

## Operational Requirements

Capture:

- Migration downtime tolerance.
- Backup/restore requirements.
- RPO and RTO.
- High availability expectations.
- Read replica usage.
- Caching strategy and invalidation rules.
- Observability: slow query logs, index usage metrics, query plan validation, bloat monitoring, replication lag, and queue depth.

## Performance Validation

Include checks that fit the target database:

- EXPLAIN or EXPLAIN ANALYZE for hot queries.
- Benchmark at expected result sizes and tenant sizes.
- Confirm intended indexes are used.
- Confirm queries avoid unbounded sorts, scans, or cross-partition reads.
- Monitor slow query logs after deployment.
- Review unused and redundant indexes after realistic traffic.
- Track write latency and storage growth after adding secondary indexes.
