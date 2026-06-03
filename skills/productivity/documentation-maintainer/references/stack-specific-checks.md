# Stack-Specific Checks

Use this reference when the repository evidence suggests one of these stacks. Do not force stack-specific docs where the project does not need them.

## Next.js / React / Vercel

Check:

```text
app/** route handlers
pages/api/**
next.config.*
vercel.json
middleware.ts
server actions
NEXT_PUBLIC_* variables
package.json scripts
```

Docs to consider:

- Local development.
- Environment variables, especially public vs server-only variables.
- Vercel build/deploy flow.
- Preview deployments.
- Route handlers and API docs.
- Middleware/auth behavior.
- Image/domain config.
- ISR, revalidation, caching, and runtime selection when relevant.

## Supabase / PostgreSQL

Check:

```text
supabase/config.toml
supabase/migrations/**
supabase/seed.sql
RLS policies
SQL functions
Supabase client usage
```

Docs to consider:

- Local Supabase setup.
- Migration workflow.
- Seed data.
- RLS/security model.
- Edge functions.
- Storage buckets.
- Auth providers.
- Environment variables.
- Production migration warnings.

## Prisma / Drizzle / ORM

Check:

```text
prisma/schema.prisma
drizzle config
migrations
seed scripts
database client setup
```

Docs to consider:

- Migration commands.
- Generate commands.
- Seed and reset commands.
- Connection strings.
- Production migration process.
- Model overview.

## Docker / Compose

Check:

```text
Dockerfile
docker-compose.yml
compose.override.yml
.dockerignore
```

Docs to consider:

- Build command.
- Run command.
- Required environment variables.
- Ports.
- Volumes.
- Local services.
- Reset/rebuild instructions.
- Differences between development and production images.

## Kubernetes / Terraform / Infrastructure

Check:

```text
k8s/**
helm/**
terraform/**
infra/**
```

Docs to consider:

- Environment layout.
- Plan/apply process.
- State management.
- Secret management.
- Rollback.
- Access requirements.
- Operational runbooks.

Warn before documenting or running commands such as `terraform apply`, `kubectl apply`, or production secret changes.

## Monorepos

Check:

```text
apps/**
packages/**
turbo.json
nx.json
pnpm-workspace.yaml
lerna.json
```

Docs to consider:

- Workspace structure.
- Per-app commands.
- Shared package conventions.
- Build pipeline.
- Dependency boundaries.
- Ownership per app/package.
- How root commands differ from package-specific commands.

## API / SDK Libraries

Check:

```text
src public exports
openapi specs
typedoc/jsdoc
examples/**
tests/examples
```

Docs to consider:

- Installation.
- Quick start.
- API reference.
- Examples.
- Version compatibility.
- Migration guides.
- Changelog.
- Public export surface.
