# Findings and Output

## Verdicts

- `BLOCK` for hard gate failures and serious architecture risk
- `REQUEST CHANGES` for avoidable complexity or weak boundaries
- `APPROVE WITH NOTES` for minor issues that do not materially worsen the codebase
- `APPROVE` only when the change is focused and structurally clean

## Finding Format

Every material finding should use this shape:

```md
### P0 - [Short title]

**Rule:** [Hard gate or principle violated]
**Evidence:** [File path, line range, function/module name, LOC, imports, duplicated snippets]
**Why this matters:** [Concrete maintainability, correctness, security, performance, or reviewability impact]
**Required change:** [Minimum acceptable fix]
**Suggested shape:** [Optional target structure or code sketch]
**Merge condition:** [What must be true before approval]
```

## Full Review Shape

Use this structure for repo, branch, or large folder reviews:

```md
# Complexity Demolition Review

## Verdict
`BLOCK` / `REQUEST CHANGES` / `APPROVE WITH NOTES` / `APPROVE`

## Executive Summary

## Complexity Delta

## Blocking Findings

## Required Changes

## Deletion Opportunities

## God Module / Oversized File Report

## Thin Wrappers

## Leaked Logic

## Duplication

## Suggested Refactor Sequence

## Approval Conditions
```

## Compact Review Shape

For small snippets, use:

```md
## Verdict: REQUEST CHANGES

This works, but it adds unnecessary indirection and moves logic into a generic helper instead of simplifying it.

### Required fixes

1. [fix]
2. [fix]
3. [fix]
```

## Reporting Rules

- Lead with blocking findings.
- Include file or line evidence.
- Make the minimum acceptable change explicit.
- If there are no findings, state that clearly and mention any residual risk or test gap.
