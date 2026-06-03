#!/usr/bin/env python3
"""Validate the structure of a personal-data map Markdown document."""

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
    "system_inventory": [r"system inventory", r"systems reviewed"],
    "data_map": [r"data element", r"data map"],
    "data_flow": [r"data flow", r"collection", r"sharing"],
    "findings": [r"findings"],
    "remediation": [r"remediation backlog", r"implementation issues"],
    "open_questions": [r"open questions"],
}


WARNINGS = {
    "retention": [r"retention"],
    "delete_export": [r"delete path", r"export path", r"deletion", r"export"],
    "vendors": [r"vendor", r"recipient", r"third party"],
    "region": [r"region", r"location"],
    "sensitive": [r"sensitive"],
    "logs_backups": [r"logs?", r"backups?"],
    "ai_telemetry": [r"ai prompt", r"telemetry", r"analytics"],
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
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required data-map section for {code.replace('_', ' ')}."))

    for code, patterns in WARNINGS.items():
        if not any_pattern(lowered, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Add or strengthen {code.replace('_', ' ')} coverage."))

    if "source" not in lowered or "purpose" not in lowered:
        checks.append(Check("WARN", "weak_core_fields", "Data map should include source and purpose for each data element."))

    if not checks:
        checks.append(Check("PASS", "complete", "Data map includes the required structure and privacy discovery signals."))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a personal-data map Markdown document.")
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
