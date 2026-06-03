---
name: environment-config-auditor
description: Reviews environment and configuration sanity, including .env.example, required versus optional env vars, staging and production parity, secret naming, unused env vars, leaked secrets, duplicated config, feature flags, public or private env var misuse, Next.js NEXT_PUBLIC_ misuse, and local onboarding setup. Use when reviewing runtime configuration, deployment variables, or onboarding docs.
---

# Environment Config Auditor

Review config as code: validate shape, scope, exposure, and onboarding completeness.

## Core checks

- `.env.example` completeness and accuracy
- Required versus optional env vars
- Staging and production parity
- Secret naming and secret handling
- Unused or dead env vars
- Leaked secrets or committed credentials
- Duplicated config and conflicting defaults
- Feature flags and flag ownership
- Public versus private env var misuse
- Next.js `NEXT_PUBLIC_` exposure
- Local onboarding and setup docs

## Output

Return a config matrix with key, required?, environments, secret?, used where, exposed to client?, and docs/test coverage.
