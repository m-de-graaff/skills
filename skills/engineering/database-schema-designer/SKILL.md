---
name: database-schema-designer
description: Design performance-first, workload-aware database schemas for SQL and NoSQL systems. Produces optimized tables or collections, relationships, indexes, constraints, partitioning or sharding plans, migration scripts, ERDs, query examples, and optimization rationale. Use when users need database design, schema optimization, data architecture planning, high-throughput persistence, low-latency query design, migration planning, index selection, partitioning, sharding, or production database review.
---

# Database Schema Designer

Design production database schemas from the workload backward. Optimize for the user's declared reads, writes, latency targets, growth profile, integrity needs, and operational constraints. Never present a schema as globally optimal without benchmarks; say it is optimized for the stated assumptions and access patterns.

## Workflow

1. Identify the target database, version, deployment model, allowed extensions, and operational constraints.
2. Capture or infer the main domain entities, tenant model, access-control boundaries, compliance needs, and data sensitivity.
3. Build a workload matrix before designing entities:

```text
Operation | Type | Filters | Sort | Joins | Rows Returned | Frequency | Latency Target | Model/Index Support
```

4. Capture volume, growth, retention, archival, skew, largest tenants, hot/cold data, and transaction requirements.
5. Design keys, relationships, constraints, indexes, denormalization, partitioning, sharding, and retention to serve named workload rows.
6. Include concrete DDL or collection definitions, migration steps, hot query examples, intended access paths, and validation checks.
7. Run `scripts/validate_schema_design.py` on long final designs when a Markdown artifact is available or the user asks for a quality check.

## Interaction Rules

- Ask concise clarifying questions only when missing requirements would change the core model, key choice, or access pattern. If the user likely expects a quick result, proceed with explicit assumptions.
- Prefer concrete schema definitions, index definitions, query examples, migration notes, and tradeoff rationale over generic advice.
- For existing schemas, first identify bottlenecks, missing indexes, redundant indexes, poor keys, hot tables or partitions, anti-patterns, and migration risk.
- Avoid wasteful optimization: do not add indexes, partitions, JSON fields, caches, materialized views, or denormalized columns unless they support a named query or operational requirement.
- Justify every performance-related decision with the workload row, query, or operational need it serves.

## Reference Loading

Load only the references needed for the user's database and task:

- `references/workload-first-design.md`: requirement gathering, key selection, denormalization, multi-tenancy, retention, and anti-patterns.
- `references/sql.md`: SQL table, constraint, index, query-plan, PostgreSQL, MySQL/MariaDB, and SQL Server guidance.
- `references/nosql.md`: MongoDB, DynamoDB, Cassandra, ScyllaDB, Bigtable, document modeling, partition keys, and access-pattern maps.
- `references/migrations-and-operations.md`: expand/contract migrations, production safety, partitioning, retention, observability, backup, and validation.
- `references/output-quality.md`: required complete-response structure, ERD guidance, final checklist, and validator usage.

## Complete Response Shape

For full schema designs, include these sections unless the user requested a narrower answer:

1. Database, domain, optimization goal, and assumptions
2. Workload matrix
3. Optimization strategy
4. ERD or NoSQL access-pattern map
5. Table or collection definitions
6. Constraints and data integrity
7. Index plan with rationale
8. Hot query examples and intended access paths
9. Partitioning, sharding, retention, or archival plan when justified
10. Migration scripts and online migration notes
11. Performance validation checklist
12. Tradeoffs and risks

## Output Standard

Before finalizing, verify that the design is tied to declared or inferred access patterns, uses database-specific data types, has only justified indexes, explains composite index order, scopes tenant uniqueness correctly, handles soft delete and retention deliberately, includes migration and rollback guidance, and names the remaining performance risks.
