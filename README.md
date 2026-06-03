# Skills For Real Engineers

Agent skills for real engineering work.

This repo is where I keep small, composable skills that help coding agents work with more discipline: clarifying intent, designing from real constraints, debugging deliberately, writing better tests, improving architecture, and handing work off cleanly.

The goal is not to hand control of the whole process to an agent. The goal is to give the agent sharper workflows that are easy to inspect, adapt, and combine.

The current skills cover workload-first database design, codebase refactoring, strict code-quality review gating, AI integration review, worker and queue safety, billing hardening, config auditing, analytics hygiene, product-flow friction review, API contract enforcement, frontend performance profiling, runtime observability, release readiness, test strategy, access control, performance and cost optimization, disciplined frontend design systems, documentation maintenance, privacy workflows, and defensive application security review.

## Quickstart (30-second setup)

Run the skills.sh installer:

```bash
npx skills@latest add m-de-graaff/skills
```

Pick the skills you want, and choose which coding agents you want to install them on.

Then invoke the skill you need from your agent:

- `/database-schema-designer` for workload-aware SQL and NoSQL schema design.
- `/codebase-refactor-architect` for safe structural refactors, god-module splits, and duplication removal.
- `/complexity-demolition-code-review` for strict code-quality review gates that block avoidable complexity, oversized files, and thin wrappers.
- `/llm-integration-cost-and-quality-review` for AI features, prompt budgets, fallback models, evals, and prompt regressions.
- `/background-jobs-queue-review` for queues, workers, retries, idempotency, and cron overlap.
- `/billing-payments-hardening-review` for Stripe, subscriptions, invoices, credits, webhooks, and billing edge cases.
- `/environment-config-auditor` for env vars, `.env.example`, secret hygiene, and staging/prod parity.
- `/analytics-event-hygiene-auditor` for analytics events, naming hygiene, PII leakage, and funnel coverage.
- `/product-flow-friction-review` for signup, onboarding, checkout, invites, cancellation, and error-recovery flow friction.
- `/api-contract-enforcer` for REST, tRPC, GraphQL, and webhook contract consistency.
- `/frontend-performance-profiler` for bundle, hydration, render, image, font, and Core Web Vitals risk.
- `/runtime-observability-engineer` for logs, traces, metrics, alerts, dashboards, and incident readiness.
- `/release-readiness-gate` for deploy safety, rollback, migrations, previews, and canary rollout checks.
- `/test-suite-architect` for missing tests, brittle tests, and coverage strategy on risky code.
- `/access-control-policy-auditor` for roles, permissions, tenant isolation, RLS, and IDOR/BOLA risk.
- `/performance-cost-audit` for source-aware latency, query-count, provider-cost, and async bottleneck reviews.
- `/frontend-design-system` for polished product UI, design tokens, component states, and light/dark themes.
- `/data-map` for personal-data inventories and data-flow maps.
- `/privacy-regime-review` for GDPR/CCPA-style privacy regime reviews.
- `/dpia` for privacy impact assessment screening and drafting.
- `/appsec-audit` for authorized source-aware AppSec audits and remediation-ready security reports.
- `/documentation-maintainer` for auditing, pruning, updating, and creating source-aligned project docs.

## Suggested Skill Run Order

Use these as practical sequences, not rigid rules. Pick the path that matches the work in front of you.

| Situation | Run these skills in order | Why |
|---|---|---|
| Designing a new product feature | `/frontend-design-system` -> `/database-schema-designer` -> `/data-map` -> `/appsec-audit` | Shape the UI and data model first, then identify personal-data flows and security risks before implementation hardens around bad assumptions. |
| Building a database-heavy feature | `/database-schema-designer` -> `/codebase-refactor-architect` -> `/performance-cost-audit` -> `/appsec-audit` | Start from workload and schema, keep the structure maintainable, then check query/cost shape and authorization or tenant-isolation risks. |
| Making a dashboard, admin panel, or SaaS screen | `/frontend-design-system` -> `/codebase-refactor-architect` -> `/performance-cost-audit` -> `/appsec-audit` | Design the interface, split large components or tangled modules, then check for over-fetching, request waterfalls, expensive loaders, and exposed privileged operations. |
| Breaking up large files or tangled modules | `/codebase-refactor-architect` -> `/performance-cost-audit` when structure creates runtime waste -> `/appsec-audit` for auth-sensitive areas | Preserve behavior first, split responsibilities incrementally, then verify performance and security-sensitive boundaries. |
| Auditing an AI feature or agent workflow | `/llm-integration-cost-and-quality-review` -> `/appsec-audit` when prompts or outputs touch sensitive data | Catch prompt bloat, fallback mistakes, eval gaps, and usage caps before the AI feature becomes expensive or unreliable. |
| Hardening queues, workers, or cron jobs | `/background-jobs-queue-review` -> `/performance-cost-audit` if throughput or batch size is a concern | Review retries, idempotency, overlap, and backpressure before production failures become noisy and expensive. |
| Hardening billing or subscription logic | `/billing-payments-hardening-review` -> `/appsec-audit` for plan or permission coupling | Catch webhook, invoice, credit, and subscription edge cases before money-moving bugs ship. |
| Reviewing authorization or tenant safety | `/access-control-policy-auditor` -> `/appsec-audit` for exploit paths | Verify policy at the source of truth, not just in UI or route checks. |
| Checking release safety before deploy | `/release-readiness-gate` -> `/performance-cost-audit` or `/appsec-audit` when the release is risky | Make sure the change can be shipped, rolled back, and observed safely. |
| Reviewing a PR or repository for maintainability debt | `/complexity-demolition-code-review` -> `/codebase-refactor-architect` if the review calls for a split or cleanup plan | Catch unnecessary complexity, then only refactor when there is a concrete architectural payoff. |
| Adding analytics, cookies, pixels, or tracking SDKs | `/data-map` -> `/cookie-consent-review` -> `/privacy-regime-review` | Inventory what is collected, verify consent/opt-out behavior, then review regime-specific obligations. |
| Adding a vendor or subprocessors | `/data-map` -> `/vendor-dpa-review` -> `/privacy-regime-review` | Identify the data shared, review contract/transfer/security gaps, then map obligations by regime. |
| Shipping AI, profiling, risk scoring, or sensitive-data processing | `/data-map` -> `/privacy-regime-review` -> `/dpia` -> `/appsec-audit` | Establish data flows and legal triggers, assess risks to people, then review technical controls. |
| Before a release | `/performance-cost-audit` -> `/appsec-audit` -> `/privacy-regime-review` | Check hot-path cost/latency, security regressions, and privacy obligations before launch. Add `/dpia`, `/cookie-consent-review`, or `/vendor-dpa-review` when the release touches those areas. |
| Cleaning up repository docs | `/documentation-maintainer` -> `/appsec-audit` or `/privacy-regime-review` when docs expose security or privacy-sensitive behavior | Align docs with code/config first, then review sensitive operational, security, or privacy claims when the cleanup touches those areas. |
| Responding to a suspected data leak or exposure | `/privacy-incident` -> `/data-map` -> `/appsec-audit` | Triage and preserve facts first, map affected data and systems, then find and fix the technical control failure. |

## Why These Skills Exist

Coding agents are useful, but they fail in predictable ways:

- They misunderstand the goal.
- They produce too much vague output.
- They make changes without tight feedback loops.
- They add complexity faster than they remove it.
- They apply generic patterns where the workload calls for a more specific design.

Skills are a lightweight way to correct those failure modes. Each skill should do one job well, document the workflow clearly, and leave enough room for the engineer to stay in control.

For example, `database-schema-designer` makes the agent start with access patterns, volume, latency targets, retention, and operational constraints before it proposes tables, collections, indexes, partitions, or migrations. `codebase-refactor-architect` makes the agent map god modules, duplicated logic, oversized files, public contracts, and test gaps before proposing incremental behavior-preserving refactors. `complexity-demolition-code-review` makes the agent reject avoidable complexity, fake cleanup, thin wrappers, leaked logic, and oversized handwritten files before they become normal. `performance-cost-audit` makes the agent quantify expensive code paths before recommending batching, caching, query consolidation, or async refactors. `frontend-design-system` makes the agent specify product direction, layout, tokens, component states, accessibility, and implementation details instead of producing generic UI decoration. `documentation-maintainer` makes the agent compare docs against the current codebase before updating, merging, deleting, archiving, or creating documentation. The compliance skills force data mapping, current-source verification, and implementation-ready remediation instead of hand-wavy legal claims. `appsec-audit` keeps security work scoped, source-aware, evidence-driven, and safe.

## Repository Structure

Current structure:

```text
skills/
  compliance/
    cookie-consent-review/
    data-map/
    dpia/
    privacy-incident/
    privacy-regime-review/
    privacy-requests/
    vendor-dpa-review/
  engineering/
    analytics-event-hygiene-auditor/
    api-contract-enforcer/
    background-jobs-queue-review/
    billing-payments-hardening-review/
    codebase-refactor-architect/
    complexity-demolition-code-review/
    database-schema-designer/
    environment-config-auditor/
    frontend-design-system/
    frontend-performance-profiler/
    llm-integration-cost-and-quality-review/
    performance-cost-audit/
    product-flow-friction-review/
    runtime-observability-engineer/
    test-suite-architect/
  productivity/
    documentation-maintainer/
    release-readiness-gate/
  security/
    access-control-policy-auditor/
    appsec-audit/
README.md
```

## Reference

### Engineering

- **[database-schema-designer](./skills/engineering/database-schema-designer/SKILL.md)** - Design workload-aware SQL and NoSQL schemas with indexes, migrations, ERDs, hot query examples, and performance rationale.
- **[codebase-refactor-architect](./skills/engineering/codebase-refactor-architect/SKILL.md)** - Find god modules, duplicated logic, oversized files, dead code, and tangled responsibilities; plan incremental behavior-preserving refactors with tests and rollback.
- **[complexity-demolition-code-review](./skills/engineering/complexity-demolition-code-review/SKILL.md)** - Enforce strict review gates for oversized handwritten files, god modules, thin wrappers, leaked logic, and unnecessary complexity before merge.
- **[llm-integration-cost-and-quality-review](./skills/engineering/llm-integration-cost-and-quality-review/SKILL.md)** - Review AI features for prompt bloat, eval gaps, hallucination-sensitive flows, PII exposure, structured outputs, retries, and usage caps.
- **[api-contract-enforcer](./skills/engineering/api-contract-enforcer/SKILL.md)** - Enforce API consistency across REST, tRPC, GraphQL, and webhooks with validation, envelopes, pagination, idempotency, and compatibility.
- **[test-suite-architect](./skills/engineering/test-suite-architect/SKILL.md)** - Repair test strategy, protect critical flows, add characterization tests, and reduce brittle setup.
- **[frontend-design-system](./skills/engineering/frontend-design-system/SKILL.md)** - Design polished product UIs with semantic tokens, light/dark themes, responsive layouts, component states, and implementation guidance.
- **[performance-cost-audit](./skills/engineering/performance-cost-audit/SKILL.md)** - Audit hot paths for N+1 queries, request waterfalls, duplicate work, over-fetching, async bottlenecks, provider costs, and measurable safe refactors.

### Frontend

- **[frontend-performance-profiler](./skills/frontend/frontend-performance-profiler/SKILL.md)** - Review Core Web Vitals, hydration, bundles, image and font loading, render cost, and blocking scripts.

### Operations

- **[background-jobs-queue-review](./skills/operations/background-jobs-queue-review/SKILL.md)** - Review queues, workers, cron jobs, retries, idempotency, DLQs, locking, overlap, backpressure, and observability.
- **[environment-config-auditor](./skills/operations/environment-config-auditor/SKILL.md)** - Audit env vars, `.env.example`, secret hygiene, staging/prod parity, feature flags, and client/public exposure.
- **[runtime-observability-engineer](./skills/operations/runtime-observability-engineer/SKILL.md)** - Review logs, traces, metrics, alerts, dashboards, and runbooks so production failures are observable.

### Product

- **[analytics-event-hygiene-auditor](./skills/product/analytics-event-hygiene-auditor/SKILL.md)** - Audit analytics events for duplication, missing funnels, inconsistent names, PII leakage, and tracking cost.
- **[product-flow-friction-review](./skills/product/product-flow-friction-review/SKILL.md)** - Review product flows for step count, unclear CTAs, missing states, dead ends, and mobile friction.

### Privacy

- **[data-map](./skills/privacy/data-map/SKILL.md)** - Build personal-data inventories, data-flow maps, and ROPA-style processing records from product, code, schema, infrastructure, and vendor context.
- **[privacy-regime-review](./skills/privacy/privacy-regime-review/SKILL.md)** - Review products, policies, data flows, code paths, vendors, or incidents against privacy regimes such as GDPR, UK GDPR, CCPA/CPRA, LGPD, PIPEDA, and US state privacy laws.
- **[dpia](./skills/privacy/dpia/SKILL.md)** - Screen, draft, or review DPIAs and similar privacy risk assessments for high-risk personal-data processing.
- **[privacy-requests](./skills/privacy/privacy-requests/SKILL.md)** - Design or review privacy rights workflows for access, deletion, correction, portability, opt-out, consent withdrawal, and audit evidence.
- **[vendor-dpa-review](./skills/privacy/vendor-dpa-review/SKILL.md)** - Review vendors, DPAs, subprocessors, transfer terms, security exhibits, deletion commitments, and service-provider arrangements.
- **[privacy-incident](./skills/privacy/privacy-incident/SKILL.md)** - Triage suspected personal-data incidents, preserve evidence, assess affected data and people, and prepare escalation materials.
- **[cookie-consent-review](./skills/privacy/cookie-consent-review/SKILL.md)** - Review cookies, pixels, SDKs, analytics, ads, CMP behavior, opt-out signals, and consent or disclosure gaps.

### Security

- **[access-control-policy-auditor](./skills/security/access-control-policy-auditor/SKILL.md)** - Review roles, permissions, tenant isolation, RLS, admin bypasses, and IDOR/BOLA risk with explicit enforcement matrices.
- **[appsec-audit](./skills/security/appsec-audit/SKILL.md)** - Perform authorized, source-aware application security audits with attack-surface mapping, safe validation, remediation guidance, and regression tests.

### Productivity

- **[documentation-maintainer](./skills/productivity/documentation-maintainer/SKILL.md)** - Audit project docs against current code and configuration, prune stale or duplicated docs, update canonical docs, create missing operational docs, and report remaining uncertainties.
- **[release-readiness-gate](./skills/productivity/release-readiness-gate/SKILL.md)** - Review deploy safety, rollback paths, migrations, feature flags, preview or canary plans, smoke tests, and production-only risk before shipping.

### Misc

No miscellaneous skills added yet.
