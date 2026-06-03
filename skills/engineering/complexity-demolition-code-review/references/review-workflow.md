# Review Workflow

## Step 1 - Determine Scope

Capture:

- Review target: repository, PR diff, branch, files, or folder
- Project type
- Languages
- Frameworks
- Critical paths touched
- Tests available
- Known generated or vendor paths
- Constraints provided by the user

## Step 2 - Build a Complexity Inventory

List risky files and modules.

| Path | LOC | Status | Main responsibility | Extra responsibilities | Risk | Action |
|---|---:|---|---|---|---|---|
| `src/features/billing/billing-service.ts` | 1,284 | Block | subscription orchestration | pricing, invoices, emails, webhooks, permissions | Critical | Split by use case and provider adapter |
| `app/api/orders/route.ts` | 612 | Request changes | order endpoint | auth, validation, SQL, payments, response mapping | High | Extract schema, use case, repository |

## Step 3 - Calculate Complexity Delta

For a diff, compare before and after:

- Files added
- Files deleted
- Net LOC
- Largest file before and after
- Files over 500, 750, and 1,000 LOC
- Functions over 50 and 100 LOC
- New public exports
- New dependencies
- New wrappers
- New generic helper files
- Duplicate logic clusters added or removed
- God modules improved or worsened
- Tests added or changed

## Step 4 - Review Boundaries

Classify touched modules as one of:

- UI / presentation
- Client state
- Transport / route / controller
- Validation / schema
- Use case / application service
- Domain policy / business rules
- Persistence / repository / query
- External provider adapter
- Infrastructure / config
- Shared primitives

Check whether each module owns logic from the wrong layer.

## Step 5 - Find Deletion Opportunities

Look for:

- Dead exports
- Unused components
- Unused feature flags
- Stale compatibility branches
- Duplicate type definitions
- Duplicate mapper functions
- Old API clients
- Deprecated code paths
- Redundant wrappers
- Manual transforms replaced by existing schema or parser
- Repeated null checks caused by overly loose types
- Repeated permission checks that should be centralized

## Step 6 - Classify Findings

Use:

- `P0` Blocker
- `P1` Required
- `P2` Recommended
- `P3` Note

Do not bury `P0` or `P1` findings under low-value suggestions.
