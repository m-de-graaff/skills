# Workload-First Design

## Requirement Gathering

Collect or infer these facts before designing. Ask only for missing details that would materially change the schema.

### Database Context

- Target database: PostgreSQL, MySQL, MariaDB, SQL Server, SQLite, MongoDB, DynamoDB, Cassandra, Redis, or another system.
- Version or managed service when relevant.
- Deployment model: single node, managed cloud database, replicated cluster, multi-region, serverless, or embedded.
- Allowed features: PostGIS, pg_trgm, pg_partman, generated columns, materialized views, full-text search, JSONB, vector indexes, TTL indexes, or table partitioning.

### Application Domain

- Product or application type.
- Main resources and ownership boundaries.
- Tenant model: single-tenant, multi-tenant, organization scoped, workspace scoped, or region scoped.
- User roles, access-control boundaries, compliance, and data sensitivity.

### Workload and Access Patterns

For each important operation capture:

- Operation name and business purpose.
- Read/write type.
- Filters, joins, sort order, pagination method, aggregations, and expected result size.
- Frequency or QPS.
- Latency target: p50, p95, or p99 when known.
- Consistency requirement.
- Whether it is user-facing, background, admin-only, or analytical.

Use this matrix:

```text
Operation | Type | Filters | Sort | Joins | Rows Returned | Frequency | Latency Target | Model/Index Support
```

### Data Volume and Growth

- Initial rows/documents per entity.
- Growth per day, month, and year.
- Hot/cold data ratio.
- Retention and deletion policy.
- Archival requirements.
- Largest expected tenants or customers.
- Cardinality and skew for keys such as tenant_id, status, created_at, user_id, and region.

### Transactions and Integrity

- Transaction boundaries and isolation needs.
- Read-after-write requirements.
- Idempotency requirements.
- Uniqueness and referential integrity rules.
- Cascade, restrict, set-null, or soft-delete behavior.
- Audit trail and history requirements.

## Performance-First Principles

- Start with hot query paths, not an entity list.
- Ensure each user-facing hot path has a direct access path through a primary key, composite index, partition key, shard key, or precomputed read model.
- Avoid full table scans, unbounded joins, in-memory filtering, and large OFFSET pagination for high-volume paths.
- Prefer keyset/cursor pagination for large ordered lists.
- Normalize first, then denormalize only for a named latency or throughput requirement.
- Minimize write amplification: every secondary index must support a named query, constraint, sort, or maintenance operation.
- Use constraints for integrity when the database supports them and the application requires it.

## Primary Keys

### SQL

- Prefer narrow, stable, immutable primary keys.
- Use BIGINT identity when centralized monotonic keys are acceptable.
- Use UUIDv7 or ULID-style time-ordered IDs for distributed ID generation when supported by the stack.
- Avoid random UUIDv4 as the clustered/hot primary key in write-heavy systems unless distribution matters more than locality.
- In MySQL/InnoDB, keep the primary key narrow because secondary indexes include it.
- In multi-tenant schemas, consider tenant-scoped uniqueness and tenant-leading secondary indexes.

### NoSQL

- Choose partition keys that distribute writes evenly.
- Avoid hot partitions from low-cardinality keys such as status, country, or a single global tenant.
- Use sort keys that match range and ordering queries.
- Avoid cross-partition queries for user-facing paths unless the database is designed for them.

## Data Types

- Use the smallest type that safely fits expected values and growth.
- Use BIGINT for high-growth identifiers, counters, and event tables.
- Use fixed-precision DECIMAL/NUMERIC for money; never use floating point for currency.
- Use absolute timestamp types: TIMESTAMPTZ in PostgreSQL and DATETIME(6) or TIMESTAMP(6) in MySQL-like systems when sub-second precision matters.
- Use booleans for true flags, but avoid plain low-cardinality boolean indexes unless filtered/partial.
- Prefer lookup tables when values change often; use enums only for stable finite sets.
- Keep large blobs, unbounded text, and rarely accessed JSON out of hot rows when they can be split into side tables or collections.

## Denormalization

For every denormalized field or read model, specify:

- Source of truth.
- Synchronization mechanism.
- Consistency model.
- Repair/backfill strategy.
- Query or index it supports.

Use materialized views, summary tables, cached counters, or read models for expensive aggregations only with a refresh or invalidation strategy.

## Multi-Tenancy

- Put tenant_id, organization_id, or workspace_id on tenant-owned tables.
- Lead hot tenant-scoped indexes with the tenant key, such as `(tenant_id, created_at DESC, id DESC)`.
- Scope natural uniqueness by tenant, such as `UNIQUE (tenant_id, slug)`.
- Consider row-level security where supported.
- Identify noisy-neighbor risks and large-tenant escape strategies.

## Retention and Lifecycle

- Separate hot operational data from cold historical data when it improves query cost or maintenance.
- Use archived_at, partition retention, cold storage export, historical tables, or TTL where lifecycle requirements demand it.
- Avoid soft deleting very large tables without partial indexes and cleanup strategy.
- For soft-deleted rows, prefer partial indexes such as `WHERE deleted_at IS NULL` where supported.

## Anti-Patterns

- Adding single-column indexes for every column.
- Missing indexes on hot join/filter columns.
- Using random UUID primary keys for write-heavy clustered tables without reason.
- Using OFFSET pagination on large ordered result sets.
- Cascading every relationship by default.
- Storing unbounded arrays in one document.
- Using JSON/JSONB for strongly relational data that needs joins and constraints.
- Soft deleting rows without partial indexes or cleanup.
- Partitioning small tables.
- Choosing low-cardinality shard or partition keys.
- Ignoring tenant scope in indexes and unique constraints.
- Creating materialized views without refresh or invalidation strategy.
