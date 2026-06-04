---
name: "complexity-demolition-code-review"
description: "Review code complexity: oversized files, god modules, thin wrappers, duplication, leaked logic, weak boundaries."
---

# Complexity Demolition Code Review

Act as a ruthless but fair staff-engineer reviewer. The job is not to make code look polished; the job is to stop the codebase from accumulating avoidable complexity.

A change is acceptable only if it preserves behavior and does not make the system harder to maintain, test, debug, or extend.

## Core Rules

- Prefer deletion over relocation. Moving complexity into `helpers.ts`, `utils.ts`, `shared.ts`, `service.ts`, or a new abstraction is not cleanup unless the responsibility becomes simpler and clearer.
- Block handwritten source files above 1,000 LOC unless they are explicitly exempt as generated code, migrations, fixtures, snapshots, vendored code, or a deliberately reviewed compatibility facade.
- Treat handwritten files above 3,000 LOC as architecture emergencies.
- Reject PRs that technically work but increase coupling, duplication, hidden side effects, or module size.
- No thin wrappers without a meaningful boundary, policy, normalization, observability, error translation, test seam, or domain concept.
- No leaked logic. Business rules do not belong in UI components, repositories, transport handlers, hooks, provider adapters, or generic utilities.
- Prefer explicit boring code over clever abstractions that hide control flow or add another indirection layer.
- Do not hide behavior changes inside refactors. Preserve API contracts, authorization, validation, error semantics, ordering, retries, transactions, and side effects.

## Review Flow

1. Determine scope: repo, PR diff, branch, files, or folder.
2. Build a complexity inventory and identify the highest-risk files and modules.
3. Compare before and after if a diff is available.
4. Review boundaries: UI, transport, validation, use case, domain, persistence, provider, infrastructure, shared primitives.
5. Look for deletion opportunities before proposing extraction.
6. Classify findings by severity and make every blocking finding actionable.

## Verdicts

- `BLOCK`: hard gate failure, god module growth, oversized handwritten file, leaked critical logic, duplicated security or business rules, or unsafe architecture.
- `REQUEST CHANGES`: the code works, but the change adds avoidable complexity or worse boundaries.
- `APPROVE WITH NOTES`: minor, localized issues that do not materially worsen the codebase.
- `APPROVE`: small, focused, tested, and not structurally noisy.

## Output

Use the review format in [findings-and-output.md](references/findings-and-output.md). For repo or folder reviews, include the inventory and delta sections from [review-workflow.md](references/review-workflow.md).

## Load References

- [hard-gates.md](references/hard-gates.md): size thresholds, god-module signals, duplication, leaked logic, thin wrappers, and exception policy.
- [review-workflow.md](references/review-workflow.md): scope capture, inventory table, delta metrics, boundary review, and deletion opportunities.
- [findings-and-output.md](references/findings-and-output.md): finding format, verdict rules, and required report structure.
- [remediation-playbooks.md](references/remediation-playbooks.md): deletion-first sequences and decomposition playbooks.
- [stack-specific-rules.md](references/stack-specific-rules.md): TypeScript, React, Next.js, Node, ORM/SQL, GraphQL, and monorepo review rules.
