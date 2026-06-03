#!/usr/bin/env python3
"""Validate the structure of a DPIA Markdown document."""

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
    "screening": [r"dpia screening", r"screening result"],
    "processing": [r"processing description"],
    "necessity": [r"necessity", r"proportionality"],
    "risk_assessment": [r"risk assessment", r"risk register"],
    "mitigations": [r"mitigations?", r"mitigation plan"],
    "residual_risk": [r"residual risk"],
    "remediation": [r"remediation backlog", r"implementation issues"],
    "open_questions": [r"open questions"],
}


WARNINGS = {
    "people_risk": [r"affected people", r"risks to people", r"individuals"],
    "inherent_residual": [r"inherent risk", r"residual risk"],
    "legal_dpo": [r"legal", r"dpo", r"privacy counsel"],
    "launch_decision": [r"proceed", r"do not launch", r"escalate"],
    "evidence": [r"evidence"],
    "owner": [r"owner"],
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
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required DPIA section for {code.replace('_', ' ')}."))

    for code, patterns in WARNINGS.items():
        if not any_pattern(lowered, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Add or strengthen {code.replace('_', ' ')} coverage."))

    if "likelihood" not in lowered or "severity" not in lowered:
        checks.append(Check("WARN", "weak_risk_scoring", "Risk assessment should include likelihood and severity."))

    if "not legal advice" not in lowered and "legal advice" not in lowered:
        checks.append(Check("WARN", "missing_legal_disclaimer", "Include legal-advice limitation or escalation language."))

    if not checks:
        checks.append(Check("PASS", "complete", "DPIA includes the required structure and risk signals."))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a DPIA Markdown document.")
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
