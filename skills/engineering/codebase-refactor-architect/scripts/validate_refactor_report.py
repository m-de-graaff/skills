#!/usr/bin/env python3
"""Validate the structure of a codebase refactor report."""

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


REQUIRED_SECTIONS = {
    "executive_summary": [r"executive summary", r"refactor summary"],
    "hotspots": [r"file/module hotspots", r"hotspots", r"oversized files"],
    "god_modules": [r"god modules?", r"god components?", r"god services?"],
    "refactor_plan": [r"refactor plan", r"pr sequence", r"pull request sequence"],
    "validation_plan": [r"validation plan", r"typecheck", r"unit tests", r"integration tests"],
    "risks_rollback": [r"risks? and rollback", r"rollback", r"risk"],
}

RECOMMENDED_SECTIONS = {
    "architecture_snapshot": [r"current architecture snapshot", r"architecture snapshot"],
    "duplication_findings": [r"duplication findings", r"duplicate pattern", r"duplicated"],
    "target_structure": [r"proposed target structure", r"target structure"],
    "metrics": [r"before/after metrics", r"largest file loc", r"files over"],
    "code_changes": [r"code changes", r"before/after", r"patch"],
}

QUALITY_SIGNALS = {
    "behavior_preservation": [r"preserve behavior", r"behavior-preserving", r"unchanged", r"characterization"],
    "public_contracts": [r"public contract", r"api contract", r"route contract", r"compatibility", r"facade"],
    "security_boundaries": [r"auth", r"authorization", r"permission", r"tenant", r"role"],
    "side_effects": [r"side effect", r"transaction", r"email", r"webhook", r"payment", r"job"],
    "incremental_sequence": [r"pr 1", r"pr 2", r"mechanical", r"incremental", r"compatibility"],
    "tests": [r"typecheck", r"lint", r"unit", r"integration", r"e2e", r"build"],
}

WEAK_PATTERNS = {
    "cosmetic_only": [r"make it cleaner", r"clean this up", r"tidy"],
    "unsupported_certainty": [r"\bshould be fine\b", r"\bprobably safe\b", r"\bno risk\b"],
    "vague_modules": [r"\butils\.ts\b", r"\bhelpers\.ts\b", r"\bcommon\.ts\b"],
}


def any_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for pattern in patterns)


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def validate(text: str) -> list[Check]:
    checks: list[Check] = []

    for code, patterns in REQUIRED_SECTIONS.items():
        if not any_pattern(text, patterns):
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required refactor report coverage for {code.replace('_', ' ')}."))

    for code, patterns in RECOMMENDED_SECTIONS.items():
        if not any_pattern(text, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Add or strengthen {code.replace('_', ' ')} coverage when applicable."))

    for code, patterns in QUALITY_SIGNALS.items():
        if not any_pattern(text, patterns):
            checks.append(Check("WARN", f"missing_{code}", f"Report should include a {code.replace('_', ' ')} safety signal."))

    for code, patterns in WEAK_PATTERNS.items():
        if any_pattern(text, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Review language or proposed structure for {code.replace('_', ' ')}."))

    if any_pattern(text, [r"delete", r"remove dead code"]) and not any_pattern(text, [r"callers", r"dynamic", r"public api", r"framework convention"]):
        checks.append(Check("WARN", "weak_deletion_safety", "Deletion recommendations should discuss callers, dynamic usage, public APIs, or framework conventions."))

    if any_pattern(text, [r"3,000", r"3000"]) and not any_pattern(text, [r"critical", r"god module", r"generated", r"snapshot", r"migration"]):
        checks.append(Check("WARN", "weak_3000_loc_handling", "3,000-line files should be classified as critical or explicitly exempted."))

    if not checks:
        checks.append(Check("PASS", "complete", "Refactor report includes the required structure and safety signals."))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a codebase refactor report Markdown file.")
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
