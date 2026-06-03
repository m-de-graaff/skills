---
name: llm-integration-cost-and-quality-review
description: Reviews AI and LLM features for prompt/token bloat, repeated model calls, cacheable calls, unnecessary context, streaming behavior, fallback models, evals, prompt regression tests, hallucination-sensitive flows, PII in prompts, structured output validation, retry and timeout cost, and per-user or per-org usage caps. Use when reviewing prompt chains, agent flows, model wrappers, or AI product features.
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
