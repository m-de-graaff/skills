---
name: access-control-policy-auditor
description: Reviews access control policy for roles, permissions, RBAC, ABAC, tenant isolation, Supabase RLS, Postgres policies, admin bypasses, server and client trust boundaries, IDOR or BOLA risk, ownership checks, organization and team membership, invite flows, and billing-plan permissions. Use when auditing authorization flows, tenant safety, or policy enforcement.
---

# Access Control Policy Auditor

Review authorization as a policy system with explicit enforcement points and tests.

## Core checks

- Roles, permissions, and group membership
- RBAC and ABAC rules
- Tenant isolation and org boundaries
- Supabase RLS and Postgres policies
- Admin bypasses and support tooling
- Server and client trust boundaries
- IDOR and BOLA risk
- Ownership checks
- Invite flows and membership transfer
- Billing-plan permission syncing

## Required output

Return a matrix in this form:

| Actor | Resource | Action | Allowed? | Enforced where? | Test exists? |
|---|---|---|---|---|---|

Call out any rule that exists in UI or route code but is missing from the authoritative policy layer.
