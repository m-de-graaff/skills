# Skills For Real Engineers

Agent skills for real engineering work.

This repo is where I keep small, composable skills that help coding agents work with more discipline: clarifying intent, designing from real constraints, debugging deliberately, writing better tests, improving architecture, and handing work off cleanly.

The goal is not to hand control of the whole process to an agent. The goal is to give the agent sharper workflows that are easy to inspect, adapt, and combine.

The current skills cover workload-first database design, codebase refactoring, performance and cost optimization, disciplined frontend design systems, documentation maintenance, privacy/compliance workflows, and defensive application security review.

## Quickstart (30-second setup)

Run the skills.sh installer:

```bash
npx skills@latest add m-de-graaff/skills
```

Pick the skills you want, and choose which coding agents you want to install them on.

Then invoke the skill you need from your agent:

- `/database-schema-designer` for workload-aware SQL and NoSQL schema design.
- `/codebase-refactor-architect` for safe structural refactors, god-module splits, and duplication removal.
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

For example, `database-schema-designer` makes the agent start with access patterns, volume, latency targets, retention, and operational constraints before it proposes tables, collections, indexes, partitions, or migrations. `codebase-refactor-architect` makes the agent map god modules, duplicated logic, oversized files, public contracts, and test gaps before proposing incremental behavior-preserving refactors. `performance-cost-audit` makes the agent quantify expensive code paths before recommending batching, caching, query consolidation, or async refactors. `frontend-design-system` makes the agent specify product direction, layout, tokens, component states, accessibility, and implementation details instead of producing generic UI decoration. `documentation-maintainer` makes the agent compare docs against the current codebase before updating, merging, deleting, archiving, or creating documentation. The compliance skills force data mapping, current-source verification, and implementation-ready remediation instead of hand-wavy legal claims. `appsec-audit` keeps security work scoped, source-aware, evidence-driven, and safe.

## Repository Structure

Current structure:

```text
skills/
  compliance/
    cookie-consent-review/
      SKILL.md
      agents/
        openai.yaml
    data-map/
      SKILL.md
      agents/
        openai.yaml
      scripts/
        validate_data_map.py
    dpia/
      SKILL.md
      agents/
        openai.yaml
      references/
        dpia-screening.md
        dpia-template.md
      scripts/
        validate_dpia.py
    privacy-incident/
      SKILL.md
      agents/
        openai.yaml
    privacy-regime-review/
      SKILL.md
      agents/
        openai.yaml
      references/
        regime-checks.md
      scripts/
        validate_privacy_review.py
    privacy-requests/
      SKILL.md
      agents/
        openai.yaml
    vendor-dpa-review/
      SKILL.md
      agents/
        openai.yaml
  engineering/
    codebase-refactor-architect/
      SKILL.md
      agents/
        openai.yaml
      references/
        architecture-patterns.md
        god-modules-and-duplication.md
        refactor-inventory.md
        refactor-methodology.md
        reporting-and-quality.md
        stack-specific-guidance.md
      scripts/
        analyze_refactor_hotspots.py
        validate_refactor_report.py
    database-schema-designer/
      SKILL.md
      agents/
        openai.yaml
      references/
        migrations-and-operations.md
        nosql.md
        output-quality.md
        sql.md
        workload-first-design.md
      scripts/
        validate_schema_design.py
    frontend-design-system/
      SKILL.md
      agents/
        openai.yaml
      references/
        accessibility-and-qa.md
        component-system.md
        implementation-patterns.md
        layout-and-archetypes.md
        taste-and-anti-patterns.md
        themes-and-tokens.md
      scripts/
        validate_frontend_design.py
    performance-cost-audit/
      SKILL.md
      agents/
        openai.yaml
      references/
        async-and-waterfalls.md
        cloud-and-provider-costs.md
        database-and-orm.md
        frontend-and-api.md
        optimization-techniques.md
        reporting-and-verification.md
      scripts/
        validate_performance_audit.py
  productivity/
    documentation-maintainer/
      SKILL.md
      agents/
        openai.yaml
      references/
        decision-framework.md
        documentation-families.md
        inventory-and-source-map.md
        reporting-and-quality.md
        stack-specific-checks.md
      scripts/
        validate_documentation_report.py
  security/
    appsec-audit/
      SKILL.md
      agents/
        openai.yaml
      references/
        audit-workflow.md
        methodology.md
        reporting-and-regression.md
        scope-and-safety.md
        stack-checks.md
        vulnerability-modules.md
      scripts/
        validate_appsec_report.py
README.md
```

## Reference

### Engineering

- **[database-schema-designer](./skills/engineering/database-schema-designer/SKILL.md)** - Design workload-aware SQL and NoSQL schemas with indexes, migrations, ERDs, hot query examples, and performance rationale.
- **[codebase-refactor-architect](./skills/engineering/codebase-refactor-architect/SKILL.md)** - Find god modules, duplicated logic, oversized files, dead code, and tangled responsibilities; plan incremental behavior-preserving refactors with tests and rollback.
- **[frontend-design-system](./skills/engineering/frontend-design-system/SKILL.md)** - Design polished product UIs with semantic tokens, light/dark themes, responsive layouts, component states, and implementation guidance.
- **[performance-cost-audit](./skills/engineering/performance-cost-audit/SKILL.md)** - Audit hot paths for N+1 queries, request waterfalls, duplicate work, over-fetching, async bottlenecks, provider costs, and measurable safe refactors.

### Compliance

- **[data-map](./skills/compliance/data-map/SKILL.md)** - Build personal-data inventories, data-flow maps, and ROPA-style processing records from product, code, schema, infrastructure, and vendor context.
- **[privacy-regime-review](./skills/compliance/privacy-regime-review/SKILL.md)** - Review products, policies, data flows, code paths, vendors, or incidents against privacy regimes such as GDPR, UK GDPR, CCPA/CPRA, LGPD, PIPEDA, and US state privacy laws.
- **[dpia](./skills/compliance/dpia/SKILL.md)** - Screen, draft, or review DPIAs and similar privacy risk assessments for high-risk personal-data processing.
- **[privacy-requests](./skills/compliance/privacy-requests/SKILL.md)** - Design or review privacy rights workflows for access, deletion, correction, portability, opt-out, consent withdrawal, and audit evidence.
- **[vendor-dpa-review](./skills/compliance/vendor-dpa-review/SKILL.md)** - Review vendors, DPAs, subprocessors, transfer terms, security exhibits, deletion commitments, and service-provider arrangements.
- **[privacy-incident](./skills/compliance/privacy-incident/SKILL.md)** - Triage suspected personal-data incidents, preserve evidence, assess affected data and people, and prepare escalation materials.
- **[cookie-consent-review](./skills/compliance/cookie-consent-review/SKILL.md)** - Review cookies, pixels, SDKs, analytics, ads, CMP behavior, opt-out signals, and consent or disclosure gaps.

### Security

- **[appsec-audit](./skills/security/appsec-audit/SKILL.md)** - Perform authorized, source-aware application security audits with attack-surface mapping, safe validation, remediation guidance, and regression tests.

### Productivity

- **[documentation-maintainer](./skills/productivity/documentation-maintainer/SKILL.md)** - Audit project docs against current code and configuration, prune stale or duplicated docs, update canonical docs, create missing operational docs, and report remaining uncertainties.

### Misc

No miscellaneous skills added yet.
