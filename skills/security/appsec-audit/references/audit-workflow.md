# Audit Workflow

## Stage 1: Architecture Baseline

Build a model before listing findings.

Analyze:

- Framework and routing model.
- API entry points.
- Authentication/session flow.
- Authorization enforcement points.
- Data model and tenant boundaries.
- External integrations.
- File upload/download paths.
- Background jobs and queues.
- Webhooks and callbacks.
- Admin-only functionality.
- Secrets and environment variable usage.
- Deployment topology.
- Security middleware.
- Logging and audit events.

Produce:

```text
Architecture baseline
- App type:
- Primary frameworks:
- Entry points:
- Authn model:
- Authz model:
- Data stores:
- Trust boundaries:
- High-value assets:
- External integrations:
- Security controls already present:
- Unknowns / assumptions:
```

## Stage 2: Attack Surface and Trust Boundaries

Map user-controllable inputs and sensitive outputs.

```text
Surface | Examples
HTTP routes | Pages, API endpoints, route handlers, controllers.
Auth flows | Login, signup, password reset, SSO, magic links, MFA.
Session flows | Cookies, JWTs, refresh tokens, CSRF tokens.
Authorization | Role checks, tenant checks, ownership checks, admin gates.
Data access | ORM queries, raw SQL, NoSQL filters, row-level security.
File handling | Upload, parse, transform, preview, download, delete.
Webhooks | Signature verification, replay protection, idempotency.
Background jobs | Queue consumers, cron jobs, retry handlers.
Browser/client | XSS sinks, CSP, postMessage, localStorage/sessionStorage.
Server-side fetch | SSRF, metadata access, internal network reachability.
Templates | Server-side rendering, markdown, HTML sanitization.
Commands | Shell execution, subprocesses, image/PDF tools.
Deserialization | JSON/XML/YAML/pickle/protobuf/custom parsers.
Infrastructure | CORS, headers, TLS, container, IaC, object storage, CDN.
Dependencies | Known CVEs, vulnerable reachable functions, supply chain.
Secrets | Hardcoded keys, leaked env vars, overbroad tokens.
```

For each surface identify:

```text
Route/file/function
User-controlled inputs
Trust boundary crossed
Security control expected
Security control observed
Potential vulnerability classes
Evidence available
```

## Stage 3: Vulnerability Analysis

Prioritize exploitability, business impact, and reachability over generic pattern matching.

Principles:

1. Trace data from source to sink.
2. Check whether validation, sanitization, encoding, or authorization is contextually correct.
3. Distinguish authentication from authorization.
4. Treat tenant isolation as a first-class invariant.
5. Prefer reachable vulnerabilities over theoretical dependency noise.
6. Treat secrets as sensitive even when old or test-like.
7. Consider abuse cases, not only malformed input.
8. Deduplicate findings by root cause.
9. Mark uncertainty explicitly.
10. Always provide a fix path.

Finding status:

```text
Status | Meaning
Confirmed | Evidence shows the issue is real in scoped code/environment.
Probable | Strong code evidence exists, but execution proof is unavailable.
Needs validation | Suspicious pattern requires more context or testing.
Informational | Hardening or best-practice gap without clear exploitability.
Rejected | Investigated and not exploitable due to a real control.
```

Severity model:

```text
Critical | Direct unauthorized admin/system access, cross-tenant data access at scale, RCE, credential/key compromise, broad account takeover or payment compromise.
High | Reliable sensitive data access, privilege escalation, auth bypass, exploitable injection, stored XSS in privileged contexts, SSRF to sensitive internal services.
Medium | Limited data exposure, reflected XSS with interaction, CSRF on meaningful action, plausible insecure config, reachable dependency vulnerability in limited context.
Low | Defense-in-depth issue, weak headers, minor information exposure, rate-limit gap without strong abuse impact.
Info | Hardening note, documentation gap, unreachable vulnerable dependency, logging improvement.
```

Include CVSS vector only when the user asks or when reporting to a formal security program.

## Output Modes

Full codebase audit:

```text
1. Scope and assumptions
2. Architecture baseline
3. Attack surface map
4. Findings summary table
5. Detailed findings
6. Cross-cutting remediation plan
7. Regression test plan
8. Open questions / validation gaps
```

PR/diff security review:

```text
1. Verdict: approve / approve with notes / request changes
2. Security-relevant changes
3. Blocking findings
4. Non-blocking hardening notes
5. Suggested patch comments
6. Tests to add before merge
```

Endpoint/API audit:

```text
1. Endpoint inventory
2. Authn/authz matrix
3. Input validation matrix
4. Data access checks
5. Abuse cases
6. Findings and fixes
```

Threat model:

```text
1. System overview
2. Assets
3. Actors
4. Trust boundaries
5. Abuse cases
6. Existing controls
7. Gaps
8. Security requirements
9. Test plan
```

Hardening checklist:

```text
1. Critical controls to verify
2. Framework-specific checks
3. Deployment checks
4. Dependency/secrets checks
5. Monitoring/audit checks
6. Recommended next steps
```
