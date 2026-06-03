#!/usr/bin/env python3
"""Validate the structure of a database schema design Markdown document."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class Check:
    level: str
    code: str
    message: str


REQUIRED_SECTIONS = {
    "workload": [r"workload matrix", r"access patterns?"],
    "optimization": [r"optimization strategy", r"modeling strategy"],
    "definitions": [r"table / collection definitions", r"table definitions", r"collection definitions", r"schema definitions"],
    "integrity": [r"constraints and data integrity", r"data integrity"],
    "indexes": [r"index plan", r"indexes?"],
    "queries": [r"hot query examples", r"query examples"],
    "migrations": [r"migration scripts", r"migration"],
    "validation": [r"performance validation checklist", r"validation checklist"],
    "risks": [r"tradeoffs and risks", r"risks"],
}


WARN_PATTERNS = {
    "assumptions": [r"assumptions?"],
    "database": [r"database:"],
    "domain": [r"domain:"],
    "optimization_goal": [r"optimization goal"],
    "erd_or_map": [r"entity relationship diagram", r"\berd\b", r"access-pattern map", r"access pattern map"],
    "partition_retention": [r"partition", r"shard", r"retention", r"archive"],
}


RATIONALE_TERMS = [
    r"supports query",
    r"column order",
    r"selectivity",
    r"write cost",
    r"rationale",
    r"intended index",
    r"access path",
]


def normalize(text: str) -> str:
    return text.lower()


def any_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def validate(text: str) -> list[Check]:
    checks: list[Check] = []
    normalized = normalize(text)

    for code, patterns in REQUIRED_SECTIONS.items():
        if not any_pattern(normalized, patterns):
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required section or heading for {code.replace('_', ' ')}."))

    for code, patterns in WARN_PATTERNS.items():
        if not any_pattern(normalized, patterns):
            checks.append(Check("WARN", f"missing_{code}", f"Consider adding explicit {code.replace('_', ' ')} information."))

    if "operation |" not in normalized and "filters |" not in normalized:
        checks.append(Check("WARN", "weak_workload_matrix", "Workload matrix table headers were not detected."))

    if "create index" not in normalized and "createindex" not in normalized and "index |" not in normalized:
        checks.append(Check("FAIL", "missing_index_definitions", "No concrete index definitions or index rationale table detected."))

    rationale_hits = sum(1 for pattern in RATIONALE_TERMS if re.search(pattern, normalized))
    if rationale_hits < 2:
        checks.append(Check("WARN", "weak_index_rationale", "Index rationale appears thin; include query support, column order, selectivity, and write cost."))

    if "explain" not in normalized and "benchmark" not in normalized and "slow query" not in normalized:
        checks.append(Check("WARN", "weak_validation", "Add EXPLAIN, benchmark, or slow-query monitoring validation steps."))

    if "down migration" not in normalized and "rollback" not in normalized:
        checks.append(Check("WARN", "missing_rollback", "Add down migration or rollback guidance where safe."))

    if "tenant" in normalized and "unique" in normalized and not re.search(r"unique\s*\([^)]*tenant", normalized):
        checks.append(Check("WARN", "tenant_uniqueness", "Tenant-scoped uniqueness is mentioned but no tenant-scoped unique constraint pattern was detected."))

    if not checks:
        checks.append(Check("PASS", "complete", "Schema design includes the required structure and rationale signals."))

    return checks


def print_text(checks: list[Check]) -> None:
    for check in checks:
        print(f"{check.level}: {check.code} - {check.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a database schema design Markdown document.")
    parser.add_argument("path", help="Markdown file path, or '-' to read from stdin.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    try:
        text = read_input(args.path)
    except OSError as exc:
        print(f"FAIL: read_error - {exc}", file=sys.stderr)
        return 1

    checks = validate(text)

    if args.json:
        print(json.dumps([asdict(check) for check in checks], indent=2))
    else:
        print_text(checks)

    return 1 if any(check.level == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
