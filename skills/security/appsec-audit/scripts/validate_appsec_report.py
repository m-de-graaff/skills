#!/usr/bin/env python3
"""Validate the structure and safety signals of an AppSec audit report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Check:
    level: str
    code: str
    message: str


REQUIRED = {
    "scope": [r"scope", r"rules of engagement", r"assumptions"],
    "architecture": [r"architecture baseline", r"system overview"],
    "attack_surface": [r"attack surface", r"trust boundar"],
    "findings": [r"findings", r"findings summary"],
    "severity_status": [r"severity", r"status", r"confidence"],
    "evidence": [r"evidence", r"evidence level"],
    "remediation": [r"remediation", r"recommended fix", r"patch guidance"],
    "regression": [r"regression test", r"tests to add"],
    "validation_limits": [r"validation limits", r"evidence limits", r"validation gaps"],
}


WARNINGS = {
    "authorized_scope": [r"authorized", r"owned", r"local", r"staging", r"rules of engagement"],
    "safe_validation": [r"synthetic", r"non-destructive", r"safe validation", r"fixture"],
    "redaction": [r"redact", r"masked", r"no secrets", r"sensitive data"],
    "root_cause": [r"root cause", r"deduplicat"],
    "standards": [r"cwe", r"owasp", r"asvs", r"cvss"],
    "owner_priority": [r"owner", r"priority", r"p0", r"p1"],
}


UNSAFE_PATTERNS = {
    "credential_theft": [r"steal cookies", r"dump tokens", r"password spraying", r"credential theft"],
    "destructive": [r"drop table", r"delete all", r"destructive payload", r"denial of service", r"\bdos\b"],
    "exfiltration": [r"exfiltrat", r"dump database", r"download all"],
    "stealth": [r"persistence", r"evad", r"stealth", r"bypass detection"],
}


def any_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def validate(text: str) -> list[Check]:
    checks: list[Check] = []
    lowered = text.lower()

    for code, patterns in REQUIRED.items():
        if not any_pattern(lowered, patterns):
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required AppSec report section or signal for {code.replace('_', ' ')}."))

    for code, patterns in WARNINGS.items():
        if not any_pattern(lowered, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Add or strengthen {code.replace('_', ' ')} coverage."))

    for code, patterns in UNSAFE_PATTERNS.items():
        if any_pattern(lowered, patterns):
            checks.append(Check("WARN", f"unsafe_language_{code}", f"Potentially unsafe language detected: {code.replace('_', ' ')}. Ensure this is defensive, redacted, and non-actionable."))

    if "confirmed" in lowered and "evidence level" not in lowered:
        checks.append(Check("WARN", "confirmed_without_evidence_level", "Confirmed findings should include evidence level."))

    if "critical" in lowered or "high" in lowered:
        if "impact" not in lowered:
            checks.append(Check("WARN", "serious_without_impact", "High/Critical findings should include impact."))

    if not checks:
        checks.append(Check("PASS", "complete", "AppSec report includes required structure and safety signals."))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AppSec audit report Markdown document.")
    parser.add_argument("path", help="Markdown path, or '-' for stdin.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    try:
        checks = validate(read_input(args.path))
    except OSError as exc:
        print(f"FAIL: read_error - {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps([asdict(check) for check in checks], indent=2))
    else:
        for check in checks:
            print(f"{check.level}: {check.code} - {check.message}")

    return 1 if any(check.level == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
