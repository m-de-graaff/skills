# NoSQL Schema Guidance

Design NoSQL schemas from access patterns first. Do not begin with normalized entities and then search for queries afterward.

## General Rules

- Define access patterns before attributes.
- Choose partition keys that avoid hot partitions and distribute writes.
- Use sort keys for range queries and ordering.
- Avoid cross-partition queries for user-facing paths.
- Precompute alternate access patterns with GSIs, LSIs, materialized views, duplicate documents, or read models only when the workload needs them.
- Model write amplification from secondary indexes and materialized views.
- Include item/document size, TTL, consistency, and conditional write considerations.

## MongoDB and Document Databases

- Embed data that is read together and has bounded growth.
- Reference data that grows without bound, changes independently, or is shared widely.
- Avoid unbounded arrays in hot documents.
- Keep document size limits and update contention in mind.
- Use compound indexes matching equality, sort, then range access patterns.
- Use sparse or partial indexes for optional fields when supported.
- Use TTL indexes for expiring data where appropriate.
- Choose shard keys with high cardinality, even distribution, and query locality.
- Avoid shard keys that monotonically increase unless the system mitigates hot shards.

MongoDB collection format:

```javascript
// Collection: collection_name
// Purpose: description
// Main access patterns: query names
{
  _id: ObjectId,
  tenant_id: ObjectId,
  field_name: "type",
  embedded_object: {
    field1: "type"
  },
  created_at: ISODate,
  updated_at: ISODate
}

// Indexes with rationale
db.collection.createIndex({ tenant_id: 1, created_at: -1, _id: -1 })
db.collection.createIndex({ tenant_id: 1, status: 1, created_at: -1 })
```

Document design output should state:

- Why each field is embedded or referenced.
- Maximum expected embedded array size.
- Update contention risks.
- Indexes and the queries they support.
- Shard key choice and expected distribution, if sharded.

## DynamoDB

For DynamoDB, output access patterns before the item model:

```text
Access Pattern | PK | SK | Index | Consistency | Expected Items | Hot Partition Risk
```

Design notes:

- Prefer high-cardinality partition keys.
- Use sort keys for time windows, hierarchy, and ordered lists.
- Use GSIs for alternate partitioning only when reads justify write amplification.
- Use conditional writes for idempotency and uniqueness patterns.
- Use TTL for expiration when eventual deletion is acceptable.
- Avoid scans for user-facing paths.
- Account for item collection size limits and adaptive capacity behavior.

## Cassandra, ScyllaDB, and Wide-Column Stores

- Model one table per query shape when necessary.
- Choose partition keys that keep partitions bounded and distribute writes.
- Use clustering columns for ordering and range reads within a partition.
- Avoid high-cardinality clustering that creates unbounded wide rows.
- Avoid ALLOW FILTERING-style query plans for hot paths.
- Duplicate data deliberately and specify write/update synchronization.
- Include compaction, TTL, tombstone, and read-repair considerations when relevant.

## NoSQL Access-Pattern Map

Use an access-pattern map instead of forcing a relational ERD:

```text
users collection
  Query: get user by id
  Key/index: _id
  Consistency: strong enough for profile reads

tenant_orders collection
  Query: list latest orders for tenant
  Key/index: { tenant_id: 1, created_at: -1, _id: -1 }
  Pagination: cursor using created_at + _id
```
