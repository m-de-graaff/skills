---
name: release-readiness-gate
description: Review release readiness: CI/CD, migrations, env vars, rollback, deploy config, flags, smoke tests, prod risk.
---

# Release Readiness Gate

Review release safety separately from code quality. Clean code can still deploy unsafely.

## Verdicts

- `BLOCK RELEASE`
- `RELEASE WITH FIXES`
- `SAFE TO DEPLOY`
- `SAFE TO DEPLOY WITH MONITORING`

## Core checks

- CI/CD pipeline correctness
- Deploy config for Vercel, GitHub Actions, or Docker
- Database migration safety and rollback
- Environment variable correctness
- Feature flag rollout and kill switch
- Release notes and operator visibility
- Smoke tests and preview deployments
- Canary rollout or staged deployment plan
- Production-only risk and blast radius

## Output

Return the verdict first, then a short release-risk list with the minimum fix needed to ship safely.
