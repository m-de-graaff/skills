# SQL Schema Guidance

Use database-specific syntax when the target database is known. Default to PostgreSQL style when the user does not specify a SQL engine.

## Index Design

Composite index order:

1. Equality filters: tenant_id, user_id, status.
2. Range filters: created_at >=, price BETWEEN, score >.
3. Sort keys: created_at DESC, id DESC.
4. Covering or INCLUDE columns when supported and useful.

Rules:

- Index foreign keys used in joins, cascades, or delete checks.
- Use unique indexes for natural uniqueness.
- Use partial/filtered indexes for sparse predicates such as active rows, unprocessed jobs, and soft-deleted rows.
- Use expression indexes for normalized lookups such as lower(email) only when queries use the same expression.
- Use covering indexes for hot read paths when they avoid expensive table lookups.
- Use full-text, trigram, GIN/GiST, spatial, vector, or BRIN indexes only when the query requires them.
- Prefer one well-ordered composite index over several single-column indexes when filters and sorts are used together.
- Avoid redundant indexes covered by another index prefix or unique constraint.
- Keep index names deterministic and descriptive.

Index rationale format:

```text
Index | Type | Supports Query | Column Order Rationale | Selectivity | Write Cost | Keep/Drop Reason
```

## Query Plan Awareness

For hot queries, provide example SQL and the intended access path:

```sql
-- Hot query: list latest orders for a tenant
SELECT id, status, total_amount, created_at
FROM orders
WHERE tenant_id = $1
  AND deleted_at IS NULL
ORDER BY created_at DESC, id DESC
LIMIT 50;

-- Intended index support:
-- idx_orders_tenant_active_created_id
-- ON orders (tenant_id, created_at DESC, id DESC)
-- WHERE deleted_at IS NULL
```

Include validation checks:

- EXPLAIN or EXPLAIN ANALYZE uses the intended index.
- Estimated and actual row counts are close enough to trust the plan.
- Sort nodes are avoided for hot ordered lists when the index can supply order.
- Heap/table lookups are acceptable or intentionally reduced through covering indexes.
- Slow query logs and index usage views are monitored after rollout.

## PostgreSQL Defaults

- Prefer TIMESTAMPTZ for absolute timestamps.
- Prefer BIGINT GENERATED ALWAYS AS IDENTITY or time-ordered UUIDs depending on distributed ID needs.
- Use CREATE INDEX CONCURRENTLY for production indexes on large existing tables.
- Remember CREATE INDEX CONCURRENTLY cannot run inside a transaction block.
- Use partial indexes for deleted_at IS NULL, sparse statuses, job queues, and active records.
- Use INCLUDE columns only when they materially reduce heap visits on hot reads.
- Use JSONB only for truly flexible attributes; add GIN or expression indexes only for queried paths.
- Use BRIN indexes for huge append-only timestamp tables when natural ordering exists.
- Use NOT VALID then VALIDATE CONSTRAINT for safer large-table constraint additions.
- Avoid trigger-heavy designs on very hot write tables unless the cost is acceptable.

PostgreSQL table style:

```sql
-- Table: table_name
-- Purpose: description
-- Hot queries supported: query names

CREATE TABLE table_name (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  field_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ,

  CONSTRAINT ck_table_rule CHECK (condition),
  CONSTRAINT fk_table_parent
    FOREIGN KEY (parent_id)
    REFERENCES parent_table(id)
    ON DELETE RESTRICT
);

-- Index: supports named query/access pattern
CREATE INDEX idx_table_columns
  ON table_name (tenant_id, created_at DESC, id DESC)
  WHERE deleted_at IS NULL;
```

Large existing table pattern:

```sql
CREATE INDEX CONCURRENTLY idx_table_columns
  ON table_name (tenant_id, created_at DESC, id DESC);

ALTER TABLE table_name
  ADD CONSTRAINT fk_table_parent
  FOREIGN KEY (parent_id) REFERENCES parent_table(id)
  NOT VALID;

ALTER TABLE table_name
  VALIDATE CONSTRAINT fk_table_parent;
```

## MySQL and MariaDB Defaults

- Keep primary keys narrow because InnoDB secondary indexes include the primary key.
- Prefer monotonic primary keys for high insert throughput unless distribution requires otherwise.
- Design composite indexes using the leftmost-prefix rule.
- Avoid redundant secondary indexes that duplicate prefixes.
- Use generated columns for indexing JSON paths or expressions where appropriate.
- Be explicit about ON DELETE and ON UPDATE actions.
- Account for online DDL limitations by version and engine.

## SQL Server Defaults

- Choose clustered indexes deliberately; the primary key does not have to be clustered.
- Use included columns for covering indexes when useful.
- Use filtered indexes for sparse hot predicates.
- Use computed columns for expression indexing where appropriate.
- Specify isolation and locking implications for high-concurrency workloads.

## Relationships

- Use foreign keys and junction tables for many-to-many relationships in relational databases.
- For high-volume join tables, use composite primary keys ordered by the access pattern, such as `(user_id, group_id)`, and add a reverse index only if reverse lookup is required.
- Avoid polymorphic foreign keys unless flexibility is worth the loss of referential integrity and query efficiency.
- For hierarchical data, choose adjacency lists, closure tables, materialized paths, or nested sets based on read/write patterns.
