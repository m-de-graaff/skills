# Output Quality

## Complete Schema Design Format

Use this structure for complete schema-design responses:

```text
DATABASE SCHEMA DESIGN

Database: [database + version if known]
Domain: [application type]
Optimization Goal: [latency/throughput/storage/scalability goals]
Assumptions: [explicit assumptions]

1. WORKLOAD MATRIX
[Top reads/writes, filters, joins, sorts, frequency, latency targets]

2. OPTIMIZATION STRATEGY
[Key modeling, indexing, denormalization, partitioning, caching, archival decisions]

3. ENTITY RELATIONSHIP DIAGRAM
[ASCII ERD or NoSQL access-pattern map]

4. TABLE / COLLECTION DEFINITIONS
[DDL or collection schemas]

5. CONSTRAINTS AND DATA INTEGRITY
[PKs, FKs, unique constraints, checks, validation rules]

6. INDEX PLAN
[Index definitions with query rationale, column order, selectivity, write cost]

7. HOT QUERY EXAMPLES
[Representative queries and intended access paths]

8. PARTITIONING / SHARDING / RETENTION
[Only when justified; include retention and archival strategy]

9. MIGRATION SCRIPTS
[Up migration, down migration, online migration notes]

10. PERFORMANCE VALIDATION CHECKLIST
[EXPLAIN checks, benchmark plan, index usage checks, slow query monitoring]

11. TRADEOFFS AND RISKS
[Write amplification, storage cost, consistency tradeoffs, operational complexity]
```

## ASCII ERD Example

Use ASCII so the output is portable:

```text
+-------------------------+
| users                   |
+-------------------------+
| id (PK)                 |
| tenant_id (FK/indexed)  |
| email (tenant unique)   |
| created_at              |
+------------+------------+
             | 1:N
+------------v------------+
| orders                  |
+-------------------------+
| id (PK)                 |
| tenant_id (indexed)     |
| user_id (FK/indexed)    |
| status                  |
| created_at              |
+-------------------------+
```

For NoSQL designs, generate an access-pattern map instead of a relational ERD.

## Final Checklist

Before finalizing, verify:

- The schema is designed around declared or inferred access patterns.
- Data types are database-specific and appropriate.
- Primary keys fit locality, distribution, and operational needs.
- Every index has a named query, constraint, sort, or maintenance reason.
- Composite index column order is explained.
- Redundant indexes are avoided.
- Integrity constraints are included where appropriate.
- Multi-tenancy is scoped correctly when relevant.
- Soft deletes include uniqueness, index, and cleanup strategy.
- Partitioning or sharding is included only when justified.
- Denormalization includes source of truth, sync, consistency, and repair strategy.
- Migration and rollback guidance are present.
- Performance risks and tradeoffs are explicit.
- Validation steps include query plans, benchmarks, index usage, and slow-query monitoring.

## Validator Usage

When the design is saved to a Markdown file:

```bash
python skills/engineering/database-schema-designer/scripts/validate_schema_design.py path/to/design.md
```

Or from stdin:

```bash
type design.md | python skills/engineering/database-schema-designer/scripts/validate_schema_design.py -
```

The validator checks structure and rationale coverage. It does not prove performance. Benchmark with production-like data before claiming latency or throughput targets are met.
