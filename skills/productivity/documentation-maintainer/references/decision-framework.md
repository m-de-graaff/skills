# Decision Framework

Use this reference to decide whether to keep, update, delete, merge, archive, or create documentation.

## Keep

Keep a document when it is:

- Accurate against current code/configuration.
- Useful to a clear audience.
- Not duplicated elsewhere.
- Easy to find from README or the docs index.
- Written at the right level of detail.
- Safe to follow.

When keeping a doc, still normalize headings, formatting, links, and metadata if needed.

## Update

Update a document when it is mostly useful but has drifted.

Common update reasons:

- Commands changed.
- Dependencies or runtime versions changed.
- Environment variables changed.
- API routes, schemas, or auth behavior changed.
- Deployment provider or release process changed.
- Folder structure changed.
- Screenshots or product behavior changed.
- Missing prerequisites, safety notes, or troubleshooting steps.
- Vague steps need operational commands and expected results.

Preserve useful context, replace incorrect claims with verified instructions, and mark unknowns instead of filling gaps with guesses.

## Delete

Recommend deletion when a document is actively harmful or useless:

- It documents a removed system.
- It points users to the wrong deployment provider.
- It contains failing or dangerous commands without warnings.
- It duplicates another doc but is less complete.
- It is abandoned generated output with no reader.
- It has no inbound links, owner, historical value, or current use.
- It conflicts with canonical docs and would cause mistakes.

Deletion note template:

```md
Deleted: docs/old-deployment.md
Reason: Obsolete deployment guide. Current repo uses Vercel (`vercel.json`) and GitHub Actions.
Replacement: docs/deployment.md
Risk: Low, because no current config references the old provider.
```

## Archive

Archive rather than delete when a document has historical, customer, legal, audit, or compliance value:

- Architecture Decision Records.
- Release notes and changelogs.
- Migration records.
- Incident postmortems.
- Security review history.
- Compliance evidence.
- Deprecated integration guides needed through a sunset period.

Recommended archive path:

```text
docs/archive/YYYY-MM-DD-topic.md
```

Archive banner:

```md
> Archived on YYYY-MM-DD. This document is retained for historical context and should not be used as current implementation guidance. Current guidance: [link].
```

## Merge

Merge when multiple docs cover the same topic with partial or conflicting information.

Rules:

- Choose one canonical location.
- Preserve unique accurate content.
- Delete, archive, or redirect duplicates.
- Add links from related docs to the canonical doc.
- Update README, docs indexes, and inbound links.

## Create

Create documentation when the codebase has a real user need that is not covered.

Create docs for:

- First-time setup.
- Development workflow.
- Deployment, rollback, smoke tests, and release.
- Environment variables and secrets.
- Database migrations, seed data, backup, and restore.
- Architecture and service boundaries.
- API endpoints, auth, webhooks, SDKs, and integrations.
- Testing strategy and QA.
- Troubleshooting common failures.
- Operations and incident response.
- Security model and vulnerability reporting.
- Design system or frontend conventions.
- Cost/performance-sensitive workflows.
- Contribution workflow.

Do not create docs for imaginary future systems unless clearly marked as a proposal.

## Deletion Safety Checklist

Before deleting a doc, verify:

- It is not the only record of a historical decision.
- It is not required for compliance, support, customers, or audit.
- It is not linked from external public documentation unless redirects are planned.
- Accurate content has been moved to a canonical doc.
- Inbound links are updated or removed.
- The deletion reason appears in the maintenance report.

Deletion decision template:

```md
## Delete `docs/old-setup.md`

Reason: Duplicates `docs/development.md` and references removed `npm run start:dev` script.
Evidence: `package.json` contains `dev`, `build`, and `test`, but no `start:dev`.
Content preserved: Node version and database setup were moved to `docs/development.md`.
Replacement: `docs/development.md`
Risk: Low.
```

## Safe Command Verification

Prefer read-only or low-risk checks:

```bash
cat package.json
pnpm --version
pnpm lint --help
pnpm test --help
ls docs
find docs -name '*.md'
```

Context-dependent checks:

```bash
pnpm install
pnpm test
pnpm lint
pnpm typecheck
pnpm build
```

Do not run risky commands without explicit permission and clear environment boundaries:

```bash
pnpm db:reset
pnpm db:push
pnpm db:migrate:prod
terraform apply
kubectl apply
vercel --prod
supabase db reset
rm -rf
```

If commands cannot be run, validate by static evidence and label runtime verification as pending.
