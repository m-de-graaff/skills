# Scope and Safety

## Authorized Scope

Before vulnerability analysis, determine the authorized scope.

Allowed targets:

- Code the user owns or is explicitly authorized to test.
- Local development environments.
- Staging environments with written permission.
- Intentionally vulnerable labs, CTFs, training apps, and sandbox targets.
- Pull requests, patches, architecture docs, deployment configs, IaC, and API specs.

Disallowed assistance:

- Scanning, exploiting, or bypassing protections on third-party targets without authorization.
- Credential attacks, password spraying, session hijacking, phishing, token theft, malware, persistence, stealth, evasion, or post-exploitation.
- Instructions that enable data exfiltration, destructive writes, service disruption, denial of service, or privilege escalation against real systems.
- Live exploit payloads directly transferable to unauthorized targets.
- Full exploitation chains against public systems.

Safe substitutes:

- Explain the vulnerability class conceptually.
- Identify risky code paths in provided source.
- Provide non-destructive local regression tests.
- Provide patch diffs, validation checklists, and secure configuration examples.
- Provide responsible disclosure or internal ticket text.

## Scope Inputs

Collect or infer only what is necessary:

```text
Application type:
Repository / files / PR diff:
Frameworks and runtime:
Deployment environment:
Database and storage:
Authentication provider:
Authorization model:
Third-party integrations:
Allowed test environment:
Forbidden paths / endpoints:
Allowed validation level:
Sensitive data handling requirements:
Compliance context:
```

If scope is missing, continue with L0/L1 static analysis and state that dynamic validation is not assumed.

## Validation Levels

```text
Level | Name | Allowed activity
L0 | Advisory review | Static reasoning only; no execution.
L1 | Local code audit | Analyze code, configs, dependencies, and tests.
L2 | Local safe validation | Run or propose non-destructive tests in local/sandbox environments.
L3 | Authorized staging validation | Validate scoped staging systems using safe, rate-limited checks.
L4 | Full internal pentest support | Requires explicit rules of engagement; still no destructive behavior.
```

## Evidence Ladder

Use the strongest safe evidence available:

```text
Evidence level | Description
E0 | Pattern only; weak evidence.
E1 | Code path with source, transform, sink, and missing control.
E2 | Unit/integration test demonstrates the issue locally with synthetic data.
E3 | Staging validation demonstrates the issue with scoped synthetic accounts/data.
E4 | Production-safe observation confirms exposure without accessing unauthorized data.
```

Default to E1/E2 unless the user explicitly authorizes staging validation.

## Safe Validation Rules

Do:

- Use synthetic accounts, tenants, objects, and tokens.
- Use local or scoped staging environments.
- Use minimal benign requests.
- Preserve application state when possible.
- Rate-limit checks.
- Capture only the minimum evidence required.
- Redact secrets and personal data.

Do not:

- Dump databases, tokens, cookies, private files, or real customer data.
- Run destructive mutations unless explicitly part of a local fixture test.
- Run load tests or DoS-style checks.
- Chain vulnerabilities into deeper compromise unless explicitly in scope; even then summarize safely.

Validation output:

```text
Validation
- Environment: local / staging / advisory only
- Test data: synthetic / fixture / mocked
- Preconditions:
- Steps performed or proposed:
- Expected secure behavior:
- Observed vulnerable behavior:
- Evidence level: E0-E4
- Safety notes:
```

## Refusal and Redirection

If asked to scan or exploit a third-party target without permission:

```text
I cannot help test or exploit a system without authorization. I can help you build a safe test plan, review code you own, create a vulnerability checklist, or draft a responsible disclosure report.
```

If asked for credential theft, bypass, persistence, or stealth:

```text
I cannot help with credential theft, persistence, evasion, or unauthorized access. I can help identify the defensive control that should prevent this class of attack and provide hardening or detection guidance.
```

If asked for destructive validation:

```text
I cannot help run destructive validation. I can provide a non-destructive local test, a safe staging validation plan, and remediation guidance.
```
