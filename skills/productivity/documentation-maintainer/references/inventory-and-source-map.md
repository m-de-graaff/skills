# Inventory and Source Map

Use this reference when auditing a repository before updating, deleting, merging, archiving, or creating docs.

## Table of Contents

- [Project Shape](#project-shape)
- [Documentation Inventory](#documentation-inventory)
- [Source-of-Truth Map](#source-of-truth-map)
- [Drift Analysis](#drift-analysis)
- [Freshness Model](#freshness-model)

## Project Shape

Detect and summarize the current system before trusting existing docs.

```text
Project type: web app, API, library, CLI, monorepo, mobile app, data pipeline, infra repo, design system.
Languages: TypeScript, JavaScript, Python, Go, Rust, PHP, Ruby, Java, C#, Swift, Kotlin.
Frameworks: Next.js, React, Remix, Express, Fastify, NestJS, Django, Rails, Laravel, Spring, .NET.
Package manager: npm, pnpm, yarn, bun, pip, uv, poetry, cargo, go, composer, bundler.
Deployment: Vercel, Netlify, Render, Railway, Fly.io, AWS, GCP, Azure, Docker, Kubernetes, Terraform.
Database: PostgreSQL, MySQL, SQLite, MongoDB, Supabase, Firebase, Redis, DynamoDB.
API style: REST, GraphQL, tRPC, RPC, OpenAPI, webhooks, internal services.
Docs tooling: Markdown, MDX, Docusaurus, Nextra, Mintlify, MkDocs, Storybook, TypeDoc, Swagger/OpenAPI.
```

Inspect likely evidence:

```text
package.json, lockfiles, workspace files, pyproject.toml, go.mod, Cargo.toml
README.md, docs/**, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md
app/**, src/**, pages/**, routes/**, controllers/**, server/**, api/**
Dockerfile, docker-compose.yml, vercel.json, netlify.toml, fly.toml, render.yaml
.github/workflows/**, .gitlab-ci.yml, Makefile, Taskfile.yml, justfile
prisma/**, drizzle/**, supabase/**, migrations/**, schema.sql
test configs, Playwright/Cypress/Vitest/Jest configs
.env.example, config schemas, deployment config, env usage
```

## Documentation Inventory

Create an inventory before editing:

```md
| Path | Type | Audience | Status | Action | Reason | Canonical replacement |
|---|---|---|---|---|---|---|
| README.md | General overview | New devs/users | partially stale | update | Scripts differ from package.json | README.md |
| docs/deploy.md | Deployment | Maintainers | stale | delete/archive | Mentions old provider | docs/deployment.md |
| docs/api.md | API | Integrators | incomplete | update | New route handlers found | docs/api.md |
```

Status values:

```text
current
partially stale
stale
duplicated
conflicting
incomplete
missing
unsafe
orphaned
historical
unverified
```

Action values:

```text
keep
update
delete
merge
archive
create
split
rename
move
needs owner confirmation
```

Common documentation surfaces:

```text
README.md
CONTRIBUTING.md
CHANGELOG.md
LICENSE
SECURITY.md
CODE_OF_CONDUCT.md
.env.example / .env.template
docs/**
apps/**/README.md
packages/**/README.md
api-docs/**
storybook docs
MDX pages
OpenAPI / Swagger files
GraphQL schemas
ADRs
runbooks
migration guides
release notes
comments containing setup, deployment, or operational instructions
```

## Source-of-Truth Map

Use stronger evidence than prose when docs disagree with the system.

```md
| Documentation topic | Primary source of truth | Secondary evidence |
|---|---|---|
| Install commands | package.json, lockfiles, packageManager | CI install steps |
| Local dev commands | package.json scripts, Makefile, Taskfile, justfile | README, Docker Compose |
| Runtime versions | .nvmrc, .node-version, mise.toml, .tool-versions, setup actions | README |
| Environment variables | env schema, process.env/import.meta.env/Deno.env usage, .env.example | deployment docs |
| Deployment | vercel.json, netlify.toml, Dockerfile, CI/CD, Terraform, Helm | deploy docs |
| Database migrations | migrations folder, ORM schema/config | seed scripts, CI migration step |
| API endpoints | route files, controllers, OpenAPI, GraphQL schema, RPC routers | tests, API docs |
| Auth behavior | auth middleware, guards, policies, RLS | security docs |
| Testing | test scripts, configs, CI | contributing docs |
| Design system | tokens, components, Storybook | design docs |
```

## Drift Analysis

Search for these inconsistencies:

- Commands in docs that do not exist in `package.json`, `Makefile`, `Taskfile`, `justfile`, or CI.
- Package manager mismatch between docs and lockfiles.
- Runtime version mismatch between docs, tool-version files, and CI setup.
- Deployment provider mismatch, such as Heroku docs with Vercel/Docker/AWS config.
- Documented environment variables that are unused.
- Used environment variables that are undocumented.
- Public client variables not marked as public, or secrets exposed as public variables.
- Ports, service names, database names, queue names, paths, domains, and environment names that disagree.
- API endpoints in docs that no longer exist.
- API endpoints, webhooks, or public SDK methods in code that lack docs.
- Auth, role, tenant, RLS, or permission behavior missing from docs.
- Outdated screenshots or UI descriptions.
- "TODO", "coming soon", "temporary", "legacy", or "WIP" language that has become permanent.
- Duplicated onboarding instructions across root, app, package, and docs READMEs.
- Old architecture diagrams that contradict modules, packages, dependencies, or services.
- Security, deployment, infrastructure, or database instructions that are unsafe for production.
- Stale branch names, package names, customer names, domains, product names, or owner names.

Use this drift table:

```md
| Doc | Claim | Evidence | Decision |
|---|---|---|---|
| README.md | Uses `npm install` | `pnpm-lock.yaml` and `packageManager: pnpm` | Update to `pnpm install` |
| docs/deploy.md | Deploys to Heroku | `vercel.json` exists; no Heroku config found | Archive or delete |
```

## Freshness Model

Assign every major doc a freshness class.

```md
| Class | Meaning | Action |
|---|---|---|
| A | Verified against source/config in this pass | Keep/update |
| B | Mostly verified; minor uncertainty remains | Keep with note or update |
| C | Useful but partially stale | Update soon |
| D | Conflicts with current evidence | Update/delete/archive |
| E | No current owner/evidence/use | Delete/archive/needs confirmation |
```

Use optional frontmatter for long-lived operational docs, not every small Markdown file:

```yaml
---
title: Deployment
owner: Platform
last_verified: YYYY-MM-DD
verified_against:
  - vercel.json
  - .github/workflows/deploy.yml
  - package.json
---
```
