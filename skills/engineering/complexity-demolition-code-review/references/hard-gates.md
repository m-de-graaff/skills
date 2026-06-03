# Hard Gates

Use these as the default release gates unless the file is explicitly exempt.

## File Size Thresholds

| Source file type | Healthy | Warning | Request changes | Block |
|---|---:|---:|---:|---:|
| React component | 50-250 LOC | 300+ | 500+ | 1,000+ |
| React hook | 20-150 LOC | 200+ | 350+ | 700+ |
| Next.js route/page/server action | 50-200 LOC | 250+ | 500+ | 1,000+ |
| API controller/handler | 50-250 LOC | 300+ | 600+ | 1,000+ |
| Service/use-case module | 80-350 LOC | 500+ | 800+ | 1,000+ |
| Repository/query module | 80-400 LOC | 600+ | 900+ | 1,000+ |
| Utility/helper module | 20-200 LOC | 300+ | 500+ | 1,000+ |
| Type/schema file | 50-400 LOC | 700+ | 900+ | 1,200+ |
| Test file | 50-500 LOC | 800+ | 1,200+ | 1,500+ |
| Any handwritten source file | - | 500+ | 750+ | 1,000+ |
| Any handwritten source file | - | - | - | 3,000+ is critical |

## Exemptions

Allowed exemptions must be explicit.

Valid exemptions:

- Generated code with a generation header
- Database migrations
- Schema snapshots
- Lockfiles
- Vendored third-party code
- Large static fixtures
- Generated API clients
- Generated GraphQL types
- Localization dictionaries
- Checked-in snapshots
- Temporary compatibility facade with owner, removal condition, and no-new-callers rule

Invalid exemptions:

- It was already big
- We needed to ship fast
- This is easier
- The framework generated the initial file, then we added logic
- We will refactor later
- It is just one more function

## God Module Signals

Block when a module does several of these at once:

- 1,000+ LOC
- 20+ exports
- 20+ direct imports
- Multiple unrelated domains in one file
- UI, data fetching, validation, auth, business rules, provider calls, persistence, logging, and response shaping in one module
- Unrelated feature flags or state machines
- Circular dependencies
- Vague names such as `manager`, `processor`, `service`, `utils`, `helpers`, `common`, or `core`
- Changes in one behavior require unrelated tests to change

## Other Hard Gates

- Duplicate critical logic for authorization, tenant scoping, billing, security checks, persistence visibility, idempotency, webhooks, or state transitions.
- Thin wrappers that only rename, forward, or catch-and-rethrow.
- Leaked business rules in the wrong layer.
- Fake cleanup that moves a problem into a new generic file.
- Temporary compatibility facades without a removal plan.
- Behavior changes hidden inside a refactor.

## Exception Policy

Any exception must state:

- Reason
- Owner
- Expiration or removal condition
- Why alternatives were rejected
- Risk
- Tests or monitoring
- Follow-up issue
