# Documentation Families

Use this reference when deciding which documentation types a project needs. Do not create every family by default; use only the docs that fit the repository and audience.

## General / Product Overview

Typical files:

```text
README.md
docs/README.md
docs/overview.md
docs/product.md
```

Must answer:

- What is this project?
- Who is it for?
- What problem does it solve?
- What are the main apps, packages, or services?
- How does a new reader get started quickly?
- Where are deeper docs?

Recommended README structure:

```md
# Project Name

One-paragraph description.

## Quick start
## Requirements
## Project structure
## Common commands
## Documentation

| Topic | Link |
|---|---|
| Development | docs/development.md |
| Deployment | docs/deployment.md |
| Environment variables | docs/environment.md |
| API | docs/api.md |
| Architecture | docs/architecture.md |
| Troubleshooting | docs/troubleshooting.md |

## Support / ownership
```

## Development

Typical files:

```text
docs/development.md
docs/local-setup.md
CONTRIBUTING.md
```

Include required runtime versions, package manager, install command, environment setup, local services, database setup, seed data, dev server command, test/lint/typecheck/format commands, branch/PR workflow where relevant, and common setup troubleshooting.

Validation sources:

```text
package.json scripts
lockfiles
.nvmrc / .node-version / mise.toml / .tool-versions
Dockerfile / docker-compose.yml
Makefile / Taskfile.yml / justfile
CI workflows
test config files
ORM schema and migrations
.env.example
```

Template:

~~~md
# Development

## Requirements

| Tool | Version | Source |
|---|---:|---|
| Node.js | 20.x | `.nvmrc` |
| pnpm | 9.x | `packageManager` in `package.json` |

## Install dependencies

```bash
pnpm install
```

## Environment

```bash
cp .env.example .env.local
```

See [Environment variables](./environment.md).

## Run locally

```bash
pnpm dev
```

## Common commands

| Command | Purpose |
|---|---|
| `pnpm dev` | Start local development server. |
| `pnpm test` | Run tests. |

## Database
## Testing
## Troubleshooting
~~~

## Deployment

Typical files:

```text
docs/deployment.md
docs/deployment/vercel.md
docs/deployment/docker.md
docs/deployment/aws.md
docs/release.md
```

Include deployment target, environments, required secrets, build command, migration command, release process, rollback process, health checks, smoke tests, logs/observability, ownership, and escalation.

Validation sources:

```text
vercel.json, netlify.toml, render.yaml, fly.toml, Procfile
Dockerfile, docker-compose.yml
GitHub Actions / GitLab CI / CircleCI
Terraform / Pulumi / CDK
Helm charts / Kubernetes manifests
package.json scripts
migration scripts
```

Add warnings around production migrations and irreversible deploy steps.

## Environment and Configuration

Typical files:

```text
docs/environment.md
.env.example
.env.template
```

Document every required runtime variable without exposing secrets:

```md
| Variable | Required | Scope | Example | Used by | Notes |
|---|---:|---|---|---|---|
| `DATABASE_URL` | Yes | Server | `postgres://...` | Server, migrations | Use pooled connection in production. |
| `NEXT_PUBLIC_APP_URL` | Yes | Public client/server | `http://localhost:3000` | Client/server | Public variable; do not store secrets. |
```

Compare docs against `process.env`, `import.meta.env`, `Deno.env`, config schemas, CI secrets references, deployment config, and `.env.example`. Distinguish public client-exposed variables from server-only secrets.

## API

Typical files:

```text
docs/api.md
docs/api/*.md
openapi.yaml
swagger.json
graphql.schema
```

Include base URL or route prefix, authentication, authorization/tenant model, operations, request params/bodies, response shape, errors, rate limits if known, pagination/filtering/sorting, webhooks, versioning, and deprecation.

Endpoint template:

~~~md
## `GET /api/orders`

Returns the authenticated user's orders.

### Auth

Requires a valid session.

### Query parameters

| Name | Type | Required | Description |
|---|---|---:|---|
| `cursor` | string | No | Pagination cursor. |
| `limit` | number | No | Maximum number of results. |

### Response

```json
{
  "items": [],
  "nextCursor": null
}
```

### Errors

| Status | Meaning |
|---:|---|
| 401 | User is not authenticated. |
| 403 | User lacks access. |
~~~

## Architecture

Typical files:

```text
docs/architecture.md
docs/adr/*.md
docs/system-overview.md
```

Include system boundaries, major apps/services/packages, data flow, dependency graph, database/storage model, auth flow, background jobs/queues, external integrations, constraints, and tradeoffs.

Use diagrams where useful. Text diagrams are acceptable:

```text
Client -> Web app -> API routes -> Database
                 -> Jobs/queues -> External providers
```

## Operations and Runbooks

Typical files:

```text
docs/operations.md
docs/runbooks/*.md
docs/incidents/*.md
```

Runbooks must include alert meaning, customer impact, first checks, read-only triage commands, dashboards/logs, mitigation, rollback, escalation, recovery validation, and post-incident follow-up.

## Troubleshooting

Typical files:

```text
docs/troubleshooting.md
docs/faq.md
```

Make troubleshooting symptom-based:

~~~md
## `pnpm install` fails with lockfile errors

### Symptoms
### Cause
### Fix

```bash
corepack enable
pnpm install --frozen-lockfile
```

### Still failing?
~~~

Avoid dumping random error messages without fixes.

## Testing and QA

Typical files:

```text
docs/testing.md
docs/qa.md
```

Include test types, commands, required services, test data setup, CI behavior, coverage expectations if present, and manual QA checklist for critical flows.

Validation sources:

```text
vitest.config.*
jest.config.*
playwright.config.*
cypress.config.*
package.json scripts
CI workflows
test folders
```

## Security

Typical files:

```text
SECURITY.md
docs/security.md
docs/auth.md
```

Include supported versions, vulnerability reporting, auth model overview, permissions/roles, secret handling, security-sensitive deployment notes, and dependency update process if known. Do not disclose exploit details, private keys, live credentials, or sensitive infrastructure maps.

## Database and Data

Typical files:

```text
docs/database.md
docs/data-model.md
docs/migrations.md
```

Include database provider, schema/ORM location, migration workflow, seed workflow, backup/restore if relevant, RLS/policies if relevant, retention/archival if relevant, and high-risk migration warnings.

## Frontend / Design System

Typical files:

```text
docs/design-system.md
docs/frontend.md
storybook docs
tokens docs
```

Include UI framework, styling system, token usage, component conventions, accessibility rules, theme behavior, and common component patterns. Structure design system docs by tokens, components, accessibility, migration, and review checklists.

## Performance and Cost

Typical files:

```text
docs/performance.md
docs/costs.md
docs/scaling.md
```

Include known hot paths, cost-sensitive providers, query/caching conventions, rate limits, background jobs, monitoring dashboards, performance budgets, and regression checks.

## Release and Changelog

Typical files:

```text
CHANGELOG.md
docs/release.md
docs/releases/*.md
```

Include versioning policy, release steps, migration notes, breaking changes, rollback notes, and customer-facing release summary where relevant. Do not delete old changelogs unless the user explicitly confirms they are disposable.
