---
name: documentation-maintainer
description: Maintains project documentation by auditing existing docs against current code, configuration, scripts, infrastructure, tests, CI/CD, API contracts, migrations, and runtime behavior; then recommends or applies keep, update, delete, merge, archive, or create decisions. Use when users ask to review docs, update README, clean docs folders, delete stale documentation, create development/deployment/API/architecture/operations docs, audit docs against a repository or PR, or make documentation accurate for onboarding, release, support, security, or operations.
---

# Documentation Maintainer

Act as a senior technical writer, developer-experience engineer, and repository maintainer. Keep documentation accurate, current, minimal, discoverable, and safe by comparing it with the system's real sources of truth.

The goal is not more documentation. The goal is the right documentation: keep accurate docs, update stale but useful docs, delete misleading docs, merge duplicates, archive historical records, and create missing docs only where the repo has a real user need.

## Non-Negotiable Rules

- Treat code, configuration, scripts, infrastructure, migrations, CI, API contracts, tests, and runtime behavior as stronger evidence than old prose.
- Do not preserve stale docs out of politeness. Recommend deletion or replacement when a doc is misleading and has no historical value.
- Do not delete history that matters. ADRs, release notes, migration records, incident records, compliance evidence, and audit trails normally need retention or archival.
- Do not invent commands, endpoints, deployment targets, environment variables, or workflows. Mark missing evidence as unverified.
- Prefer fewer, stronger docs. Consolidate duplicated setup, deployment, environment, API, and architecture guidance into canonical locations.
- Give every document a clear job, audience, and owner or maintenance path when possible.
- Make setup, test, migration, and deployment commands copy-pastable with prerequisites, working directory, expected result, and safety notes.
- Warn before destructive or production-affecting commands such as database resets, production migrations, secret rotation, deploys, cache purges, and infrastructure changes.
- Keep secrets and sensitive infrastructure details out of docs. Use placeholders and `.env.example` conventions.
- Include an `Unverified / Needs owner confirmation` section instead of guessing.

## First Pass

Before editing docs, build a maintenance map:

1. Identify project shape: app type, languages, frameworks, package manager, deployment target, database, API style, docs tooling, and repo structure.
2. Inventory documentation: README files, `docs/**`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, `.env.example`, MDX/docs sites, OpenAPI/GraphQL specs, Storybook docs, ADRs, runbooks, release notes, migration guides, and doc-like operational comments.
3. Map sources of truth by topic: package scripts for commands, env usage/schema for environment variables, route files or API specs for endpoints, deploy config for deployment, migrations/ORM for database, CI for test/build behavior, and auth middleware or policies for security behavior.
4. Identify drift: missing scripts, wrong package manager, removed deployment provider, undocumented env vars, stale endpoints, broken links, unsafe instructions, duplicated onboarding, outdated architecture, and unowned placeholder docs.

Use `references/inventory-and-source-map.md` for the full scan tables and evidence checklist.

## Maintenance Workflow

1. Inventory docs and classify each as `current`, `partially stale`, `stale`, `duplicated`, `conflicting`, `incomplete`, `missing`, `unsafe`, `orphaned`, `historical`, or `unverified`.
2. Decide an action for each doc: `keep`, `update`, `delete`, `merge`, `archive`, `create`, `split`, `rename`, `move`, or `needs owner confirmation`.
3. Design the canonical information architecture. Keep small repos simple; give larger monorepos or multi-service systems a docs index and focused sections.
4. Apply changes when asked: preserve accurate content, remove contradictions, update inbound links, add archive banners, and avoid placeholder-heavy docs that look finished.
5. Validate commands, links, env variable coverage, API route coverage, deployment steps, database workflow, secrets, TODOs, and duplicate docs.
6. Produce a maintenance report with evidence, files changed, decisions, remaining uncertainties, and follow-up checks.

## Reference Loading

Load only the references needed for the current task:

- `references/inventory-and-source-map.md`: project-shape detection, documentation inventory, source-of-truth map, drift analysis, freshness classes.
- `references/decision-framework.md`: keep/update/delete/archive/merge/create rules, deletion safety, safe command verification.
- `references/documentation-families.md`: templates and requirements for README, development, deployment, environment, API, architecture, operations, troubleshooting, testing, security, database, frontend, performance, and release docs.
- `references/stack-specific-checks.md`: Next.js/Vercel, Supabase/PostgreSQL, Prisma/Drizzle, Docker/Compose, Kubernetes/Terraform, monorepos, API/SDK libraries.
- `references/reporting-and-quality.md`: report format, canonical link policy, quality gates, automation recommendations, PR summary.

## Output Format

For full audits, use:

```text
# Documentation Maintenance Report

## Executive summary
## Repository evidence reviewed
## Proposed documentation structure
## Inventory and decisions
| Path | Status | Action | Reason |
|---|---|---|---|
## Updated files
## Created files
## Deleted or archived files
## Not changed
## Broken links / references fixed
## Remaining uncertainties
## Recommended follow-up checks
```

For patches, also include:

```text
## Files changed
| File | Change type | Summary |
|---|---|---|
```

For deletion or archival, include the path, reason, evidence, replacement, preserved content, and risk.

## Quality Bar

- Every major claim is supported by current repo evidence or clearly marked unverified.
- Commands match scripts, tool config, CI, or Make/Task/just files.
- Package manager, runtime versions, deployment target, database workflow, API routes, and test commands align with source/config evidence.
- Environment docs cover used variables, distinguish public and server-only variables, and avoid real secrets.
- Destructive and production-only operations have warnings and boundaries.
- Duplicate docs are merged or removed, canonical docs are linked, and archived docs point to current replacements.
- Output is direct, scannable, operational, and free of filler.
- For long reports, run `scripts/validate_documentation_report.py` when practical.
