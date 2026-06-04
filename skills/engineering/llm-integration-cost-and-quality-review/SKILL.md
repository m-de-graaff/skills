---
name: llm-integration-cost-and-quality-review
description: Review LLM features for prompt bloat, model choice, token cost, caching, evals, PII, retries, fallbacks, validation.
---

# LLM Integration Cost and Quality Review

Review LLM features as a quality, safety, and spend control surface, not just a generic cost problem.

## Core checks

- Prompt and token bloat
- Repeated or cacheable model calls
- Unnecessary context and stale history
- Streaming behavior and partial-answer handling
- Fallback model policy and quality degradation
- Evals, golden tests, and prompt regression tests
- Hallucination-sensitive flows and human review gates
- PII in prompts, logs, and traces
- Structured output validation and retry loops
- Timeout, retry, and fallback cost
- Per-user and per-org usage caps

## Output

Return the highest-risk findings first, then a short control-gap summary. Include whether the issue is cost, quality, safety, or contract risk.
