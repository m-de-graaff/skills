#!/usr/bin/env python3
"""Validate the structure of a documentation maintenance report."""

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
    "executive_summary": [r"executive summary", r"summary"],
    "evidence_reviewed": [r"repository evidence reviewed", r"evidence reviewed", r"sources reviewed"],
    "inventory_decisions": [r"inventory and decisions", r"documentation inventory"],
    "uncertainties": [r"remaining uncertainties", r"unverified", r"needs owner confirmation", r"open questions"],
}

RECOMMENDED_SECTIONS = {
    "proposed_structure": [r"proposed documentation structure", r"proposed structure"],
    "changed_files": [r"files changed", r"updated files", r"created files", r"deleted or archived files"],
    "link_fixes": [r"broken links", r"references fixed", r"links fixed"],
    "follow_up": [r"recommended follow-up", r"follow-up", r"next steps"],
}

QUALITY_SIGNALS = {
    "status_action_table": [r"path\s*\|\s*status\s*\|\s*action", r"path\s*\|\s*type\s*\|\s*audience"],
    "source_truth": [r"source of truth", r"package\.json", r"lockfile", r"ci", r"workflow", r"route", r"migration", r"config"],
    "safety": [r"warning", r"destructive", r"production", r"secret", r"credential", r"rollback", r"risk"],
    "canonical": [r"canonical", r"replacement", r"archive", r"merge"],
}

WEAK_PATTERNS = {
    "unsupported_certainty": [r"\bshould be fine\b", r"\bprobably\b", r"\bi assume\b"],
    "minimizers": [r"\bsimply\b", r"\bjust run\b", r"\bobviously\b"],
    "finished_placeholders": [r"\btbd\b", r"\bcoming soon\b", r"\bTODO\b"],
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
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required report coverage for {code.replace('_', ' ')}."))

    for code, patterns in RECOMMENDED_SECTIONS.items():
        if not any_pattern(text, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Add or strengthen {code.replace('_', ' ')} coverage when applicable."))

    for code, patterns in QUALITY_SIGNALS.items():
        if not any_pattern(text, patterns):
            checks.append(Check("WARN", f"missing_{code}", f"Report should include a {code.replace('_', ' ')} signal."))

    for code, patterns in WEAK_PATTERNS.items():
        if any_pattern(text, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Review language for {code.replace('_', ' ')}."))

    if "delete" in text.lower() and not any_pattern(text, [r"replacement", r"risk", r"content preserved", r"evidence"]):
        checks.append(Check("WARN", "weak_delete_safety", "Deletion recommendations should include evidence, replacement, preserved content, and risk."))

    archive_recommended = any_pattern(text, [r"\|\s*[^|\n]+\s*\|\s*[^|\n]*\s*\|\s*archive\b", r"\bArchived:\s", r"\barchive\s+`"])
    if archive_recommended and not any_pattern(text, [r"archived on", r"current guidance", r"historical"]):
        checks.append(Check("WARN", "weak_archive_context", "Archived docs should include historical context and current guidance."))

    if not checks:
        checks.append(Check("PASS", "complete", "Documentation maintenance report includes the required structure and quality signals."))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a documentation maintenance report Markdown file.")
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
