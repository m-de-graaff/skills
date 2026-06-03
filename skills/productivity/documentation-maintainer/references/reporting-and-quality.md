# Reporting and Quality

Use this reference when producing the final audit, patch summary, documentation information architecture, and quality checks.

## Maintenance Report

Use this structure unless the user requests something narrower:

```md
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

For code/file patch output, include:

```md
## Files changed

| File | Change type | Summary |
|---|---|---|
```

For deletion proposals, include replacement paths and risk.

## Documentation Structure

Default small-project structure:

```text
README.md
CONTRIBUTING.md
CHANGELOG.md
SECURITY.md
docs/
  development.md
  deployment.md
  environment.md
  architecture.md
  api.md
  database.md
  testing.md
  troubleshooting.md
```

Default larger-project structure:

```text
README.md
CONTRIBUTING.md
CHANGELOG.md
SECURITY.md
docs/
  README.md
  getting-started.md
  development/
    local-setup.md
    commands.md
    testing.md
  deployment/
    README.md
    production.md
    rollback.md
  architecture/
    README.md
    adr/
  api/
    README.md
    webhooks.md
  operations/
    README.md
    runbooks/
  database/
    README.md
    migrations.md
  security/
    README.md
  troubleshooting.md
```

Rules:

- Small repos should not get a heavy docs hierarchy.
- Large or multi-app repos should not cram everything into one README.
- Each major doc should link to related docs.
- README should be an entry point, not a dumping ground.

## Canonical Link Policy

Every repository should have a clear docs entry point.

Rules:

- `README.md` links to the main docs index.
- `docs/README.md` links to all major docs when a docs directory is substantial.
- Deployment docs link to environment docs.
- Development docs link to environment, database, and testing docs.
- API docs link to auth/security docs.
- Architecture docs link to ADRs.
- Runbooks link to dashboards or log instructions where possible.
- Archived docs link to current replacements.

Docs index template:

```md
# Documentation

| Topic | Audience | Link |
|---|---|---|
| Getting started | New developers | ./getting-started.md |
| Development | Contributors | ./development.md |
| Deployment | Maintainers | ./deployment.md |
| Environment variables | Developers / operators | ./environment.md |
| Architecture | Engineers | ./architecture.md |
| API | Integrators | ./api.md |
| Testing | Contributors | ./testing.md |
| Troubleshooting | Developers / operators | ./troubleshooting.md |
```

## Writing Standards

Use documentation that is direct, concrete, operational, scannable, current-tense, and free of filler.

Prefer:

```text
Run `pnpm dev` to start the local app.
```

Avoid:

```text
Simply spin up the magic dev experience and start building amazing things.
```

Use:

- Clear H1/H2/H3 headings.
- Short paragraphs.
- Tables for commands, environment variables, endpoints, and ownership.
- Code blocks for commands and examples.
- Warnings before risky actions.
- Links to canonical docs.

Avoid:

- Fake setup commands.
- Unverified environment variables.
- Placeholder-heavy docs that look finished.
- Real secrets.
- Excessive prose.
- Duplicate instructions in multiple places.
- Minimizers like "just", "simply", or "obviously" in complex operational steps.
- Screenshots as the only source of instructions.

## Quality Gates

Accuracy:

- Commands exist in scripts or tooling.
- Package manager matches lockfile.
- Runtime versions are current.
- Environment variables match actual usage.
- Deployment docs match deployment config.
- API docs match route/controller/schema files.
- Database docs match schema/migration tooling.
- Test docs match test config and CI.

Usefulness:

- Each doc has a clear audience.
- README is a useful entry point.
- Docs index exists for larger repos.
- Setup path is complete for a new developer.
- Deployment path is complete for a maintainer.
- Troubleshooting docs cover common failures.

Maintainability:

- Duplicate docs are merged or removed.
- Canonical docs are linked.
- Archived docs are marked.
- Ownership or verification date is added where useful.
- Placeholder sections are removed or clearly marked.

Safety:

- No secrets are present.
- Destructive commands have warnings.
- Production-only steps are clearly labeled.
- Security-sensitive docs avoid unnecessary exposure.

Formatting:

- Headings are consistent.
- Internal links work.
- Tables are readable.
- Code fences specify language where useful.
- Markdown lint issues are minimized.

## Automation Recommendations

Recommend automation only when it fits the repo stack:

```text
Markdown lint
Broken link checker
Spell checker / cspell
Vale prose linting
OpenAPI generation validation
TypeDoc generation
Storybook docs build
Environment variable schema generation
Package script docs generation
Dead link detection
CI check for stale generated docs
```

Suggested CI docs job shape:

```yaml
name: Docs

on:
  pull_request:

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm docs:lint
      - run: pnpm docs:check-links
```

## PR Summary Template

```md
## PR summary

### What changed

- Updated setup instructions to match current workflow.
- Created deployment guide for production releases.
- Consolidated environment variable documentation.
- Removed obsolete deployment guide.

### Why

Existing docs referenced outdated commands or infrastructure. The new structure makes README the entry point and moves operational details into focused docs.

### Verification

- Compared commands against `package.json`.
- Compared env vars against `.env.example` and source usage.
- Compared deployment steps against deployment config and CI.
- Checked internal links.

### Follow-up

- Confirm production rollback owner.
- Add screenshots after UI stabilizes.
```
