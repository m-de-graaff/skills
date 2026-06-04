---
name: test-suite-architect
description: Improve test strategy: missing coverage, brittle tests, characterization, regressions, suite design.
---

# Test Suite Architect

Review the test suite as a product guardrail, not just a coverage number.

## Core checks

- Critical code with no tests
- Characterization tests before risky refactors
- Brittle or over-coupled tests
- Duplicate setup and fixture sprawl
- Missing unit coverage
- Missing integration coverage
- Missing E2E coverage on core flows
- Missing regression coverage for past failures
- Missing smoke tests for deploy-critical paths

## Protected flows

Protect auth, checkout, billing, dashboard loading, permissions, webhooks, and migrations first.

## Output

Return a test-strategy map that names the missing coverage type, the risk it protects, and the smallest useful test to add.
