# Reporting and Regression

## Executive Summary

Include:

```text
Overall risk level
Number of confirmed/probable findings by severity
Highest-risk themes
Business impact
Most important fixes
Validation limits
```

## Findings Summary Table

```text
ID | Severity | Status | Confidence | Category | Affected area | Evidence | Fix priority
SEC-001 | High | Confirmed | High | Authz | GET /api/documents/:id | E2 | P0
```

Priority:

```text
P0 | Fix immediately before release or hotfix now.
P1 | Fix in current sprint.
P2 | Schedule soon; meaningful but not urgent.
P3 | Backlog hardening or best practice.
```

## Finding Template

```md
## [SEV-ID] Title

**Status:** Confirmed / Probable / Needs validation / Informational / Rejected
**Severity:** Critical / High / Medium / Low / Info
**Confidence:** High / Medium / Low
**Category:** Authn / Authz / Injection / XSS / SSRF / Secrets / Supply chain / Business logic / Config / Other
**Standards mapping:** CWE / OWASP / ASVS / CVSS if applicable
**Affected component:** Route, file, function, config, dependency

### Summary
One or two sentences explaining the issue.

### Impact
What an attacker could achieve, under what preconditions, and why it matters.

### Evidence
- Source:
- Sink:
- Missing or insufficient control:
- Evidence level:
- Relevant code/config excerpt or line reference:

### Safe reproduction or validation
Non-destructive local/staging steps or a unit/integration test outline. Do not include weaponized exploit chains.

### Remediation
Concrete fix recommendations, preferably with secure code or patch guidance.

### Regression test
A test that should fail before the fix and pass after the fix.

### Priority and owner
Suggested owner/team and remediation priority.
```

## Remediation Rules

A good fix must:

- Address the root cause, not only the observed instance.
- Preserve intended product behavior.
- Include a regression test.
- Avoid introducing a weaker compensating control.
- Consider migration/backward compatibility if data model changes are required.
- Include rollout/monitoring notes for high-risk changes.

Patch guidance:

```text
Before: what is wrong and why.
After: safer pattern.
Notes: assumptions and framework-specific caveats.
Test: how to verify.
```

Do not fabricate exact line numbers unless they are visible in the provided source.

## Regression Test Patterns

Authorization:

```text
Given user A in tenant A and user B in tenant B
And object X belongs to tenant A
When user B requests object X by ID
Then the API returns 404 or 403
And no object data is returned
And an audit/security event is recorded if appropriate
```

Injection:

```text
Given untrusted input reaches a query/command/template sink
When input contains syntax-significant characters
Then the value is treated as data, not code
And the operation succeeds or fails safely
And no unintended query/command/template behavior occurs
```

XSS:

```text
Given user-controlled content is rendered
When the content contains HTML/script-like text
Then the rendered output displays inert text or sanitized allowlisted markup
And no script execution or event handler execution occurs
```

SSRF:

```text
Given an endpoint fetches user-supplied URLs
When the URL resolves to loopback/private/link-local/metadata address ranges
Then the request is blocked before connection
And redirects and DNS changes are revalidated
```

Webhook:

```text
Given an unsigned, stale, replayed, or tampered webhook request
When it reaches the webhook endpoint
Then the endpoint rejects it before mutating state
And duplicate valid events are idempotently ignored
```

## Report Quality Bar

A report passes only if:

- Findings are deduplicated by root cause.
- Every serious finding has an impact statement.
- Every serious finding has concrete remediation.
- Evidence is specific enough for an engineer to reproduce or validate.
- False-positive risk is acknowledged.
- Sensitive data is redacted.
- The report avoids sensational language.
- It does not include unsafe exploit chains.
