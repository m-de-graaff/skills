#!/usr/bin/env python3
"""Validate structure and safety coverage in a performance/cost audit report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = {
    "executive_summary": r"(?im)^##\s+executive summary\b",
    "cost_model": r"(?im)^##\s+current cost\s*/\s*operation model\b",
    "prioritized_findings": r"(?im)^##\s+prioritized findings\b",
    "finding_details": r"(?im)^##\s+finding details\b",
    "patch_plan": r"(?im)^##\s+suggested patch plan\b",
    "instrumentation": r"(?im)^##\s+instrumentation plan\b",
    "rollout": r"(?im)^##\s+rollout plan\b",
}

REQUIRED_FINDING_SIGNALS = {
    "severity": r"(?i)\bseverity\s*:",
    "confidence": r"(?i)\bconfidence\s*:",
    "location": r"(?i)\blocation\s*:",
    "pattern": r"(?i)\bpattern\s*:",
    "current_behavior": r"(?i)current behavior",
    "why_expensive": r"(?i)why (it )?is expensive",
    "recommended_change": r"(?i)recommended change",
    "estimated_impact": r"(?i)estimated impact",
    "risks": r"(?i)risks?\s*/\s*correctness notes?|correctness notes",
    "verification": r"(?i)verification",
}

SAFETY_TERMS = {
    "auth_or_tenant": r"(?i)\b(auth|authorization|permission|tenant|organization|org|rls|row-level-security|row level security)\b",
    "measurement": r"(?i)\b(p50|p95|p99|latency|query count|provider-call|provider call|billable|cost|metric|dashboard|trace|span)\b",
    "cache_or_invalidation": r"(?i)\b(cache|ttl|invalidation|stale|key|scope)\b",
    "concurrency_or_batching": r"(?i)\b(batch|bounded|concurrency|promise\.all|allsettled|rate limit|pool|chunk)\b",
}


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text) is not None


def validate(text: str) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not text.strip():
        errors.append("Report is empty.")
        return {"ok": False, "errors": errors, "warnings": warnings}

    for name, pattern in REQUIRED_SECTIONS.items():
        if not has(pattern, text):
            errors.append(f"Missing required section: {name.replace('_', ' ')}.")

    for name, pattern in REQUIRED_FINDING_SIGNALS.items():
        if not has(pattern, text):
            errors.append(f"Missing finding detail signal: {name.replace('_', ' ')}.")

    for name, pattern in SAFETY_TERMS.items():
        if not has(pattern, text):
            warnings.append(f"Missing safety/measurement signal: {name.replace('_', ' ')}.")

    if not has(r"(?i)\b(current|before)\b.*\b(proposed|after)\b", text):
        warnings.append("No obvious before/after comparison found.")

    if not has(r"(?i)\b(assumption|estimated|estimate|telemetry|runtime)\b", text):
        warnings.append("No assumption or telemetry caveat found.")

    if has(r"(?i)\bpromise\.all\b", text) and not has(
        r"(?i)\b(independent|bounded|concurrency|rate limit|pool|allsettled|fail-fast|fail fast)\b",
        text,
    ):
        errors.append("Promise.all is mentioned without independence, bounded concurrency, or error-semantics notes.")

    if has(r"(?i)\bcach(e|ing|ed)\b", text) and not has(
        r"(?i)\b(ttl|invalidation|key|tenant|user|permission|scope|stale)\b",
        text,
    ):
        errors.append("Caching is mentioned without key, scope, TTL, invalidation, or permission-safety notes.")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Markdown audit path, or '-' for stdin.")
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    args = parser.parse_args()

    try:
        text = read_input(args.path)
    except OSError as exc:
        result = {"ok": False, "errors": [str(exc)], "warnings": []}
    else:
        result = validate(text)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        if result["ok"]:
            print("OK: performance audit report passed validation.")
        else:
            print("FAIL: performance audit report did not pass validation.")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
