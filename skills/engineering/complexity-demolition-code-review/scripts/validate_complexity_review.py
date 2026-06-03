#!/usr/bin/env python3
"""Validate a complexity demolition review report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FULL_SECTIONS = [
    "Verdict",
    "Executive Summary",
    "Complexity Delta",
    "Blocking Findings",
    "Required Changes",
    "Deletion Opportunities",
    "God Module / Oversized File Report",
    "Thin Wrappers",
    "Leaked Logic",
    "Duplication",
    "Suggested Refactor Sequence",
    "Approval Conditions",
]


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
        return {"ok": False, "errors": ["Report is empty."], "warnings": []}

    verdict_match = re.search(r"(?im)^##\s*Verdict\b[:\s-]*(BLOCK|REQUEST CHANGES|APPROVE WITH NOTES|APPROVE)\b", text)
    if not verdict_match:
        errors.append("Missing verdict line.")

    if has(r"(?im)^#\s+Complexity Demolition Review\b", text):
        for section in FULL_SECTIONS:
            if not has(rf"(?im)^##\s+{re.escape(section)}\b", text):
                errors.append(f"Missing required section: {section}.")

    if has(r"(?im)^###\s+P[0-3]\b", text):
        required_signals = {
            "rule": r"(?im)^\*\*Rule:\*\*",
            "evidence": r"(?im)^\*\*Evidence:\*\*",
            "why": r"(?im)^\*\*Why this matters:\*\*",
            "required": r"(?im)^\*\*Required change:\*\*",
            "merge": r"(?im)^\*\*Merge condition:\*\*",
        }
        for name, pattern in required_signals.items():
            if not has(pattern, text):
                errors.append(f"Missing finding field: {name}.")

    if has(r"(?im)\bPromise\.all\b", text) and not has(r"(?im)\b(independent|bounded|rate limit|transaction|ordering|dependency)\b", text):
        warnings.append("Promise.all appears without dependency-order or concurrency notes.")

    if has(r"(?im)\bcache|cached|caching\b", text) and not has(r"(?im)\b(key|scope|ttl|invalidation|tenant|permission|stale)\b", text):
        warnings.append("Caching is mentioned without key, scope, TTL, or invalidation notes.")

    if not has(r"(?im)\b(evidence|file path|line range|loc)\b", text):
        warnings.append("No obvious evidence markers found.")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Review markdown path, or '-' for stdin.")
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
            print("OK: complexity review passed validation.")
        else:
            print("FAIL: complexity review did not pass validation.")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
