#!/usr/bin/env python3
"""Generate a complexity inventory for review targets."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SOURCE_EXTENSIONS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".py",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".java",
    ".cs",
    ".kt",
    ".swift",
    ".vue",
    ".svelte",
}

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

GENERATED_HINTS = (".generated.", ".gen.", ".min.", ".snap", "generated", "__generated__")
TEST_HINTS = (".test.", ".spec.", "_test.", "__tests__", "/tests/", "\\tests\\")
GENERIC_NAMES = {"utils", "helper", "helpers", "common", "shared", "misc", "manager", "processor", "service", "core", "api"}


@dataclass
class FileRecord:
    path: str
    loc: int
    imports: int
    exports: int
    file_type: str
    size_status: str
    risk: str
    signals: list[str]


def is_source_file(path: Path) -> bool:
    return path.suffix.lower() in SOURCE_EXTENSIONS


def is_generated(path: Path) -> bool:
    lowered = str(path).lower()
    return any(hint in lowered for hint in GENERATED_HINTS)


def is_test_file(path: Path) -> bool:
    lowered = str(path).lower()
    return any(hint in lowered for hint in TEST_HINTS)


def should_skip(path: Path, include_tests: bool) -> bool:
    parts = {part.lower() for part in path.parts}
    if parts & EXCLUDED_DIRS:
        return True
    if is_generated(path):
        return True
    if not include_tests and is_test_file(path):
        return True
    return False


def count_loc(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def count_patterns(text: str, patterns: Iterable[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.MULTILINE)) for pattern in patterns)


def classify_file(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if is_test_file(path):
        return "test"
    if suffix in {".tsx", ".jsx", ".vue", ".svelte"}:
        if "page" in name or "route" in name:
            return "page/route"
        return "component"
    if "route" in name or "controller" in name or "handler" in name:
        return "route/controller"
    if "repository" in name or "query" in name or "dao" in name:
        return "repository/query"
    if "service" in name or "use-case" in name or "use_case" in name:
        return "service/use-case"
    if "schema" in name or "types" in name or name.endswith(".d.ts"):
        return "type/schema"
    if "util" in name or "helper" in name or "common" in name:
        return "utility"
    return "source"


def size_status(file_type: str, loc: int) -> str:
    thresholds = {
        "component": (300, 500, 1000),
        "page/route": (250, 500, 1000),
        "route/controller": (300, 600, 1000),
        "service/use-case": (500, 800, 1000),
        "repository/query": (600, 900, 1000),
        "utility": (300, 500, 1000),
        "type/schema": (700, 900, 1200),
        "test": (800, 1200, 1500),
        "source": (500, 750, 1000),
    }
    warn, request, block = thresholds.get(file_type, (500, 750, 1000))
    if loc >= 3000:
        return "critical"
    if loc >= block:
        return "block"
    if loc >= request:
        return "request changes"
    if loc >= warn:
        return "warning"
    return "healthy"


def score_record(path: Path, loc: int, imports: int, exports: int, file_type: str, status: str) -> tuple[str, list[str]]:
    signals: list[str] = []
    score = 0

    if loc >= 3000:
        score += 5
        signals.append("3,000+ LOC")
    elif loc >= 1000:
        score += 3
        signals.append("1,000+ LOC")
    elif status in {"request changes", "critical"}:
        score += 2
        signals.append("oversized for type")
    elif status == "warning":
        score += 1
        signals.append("large for type")

    if imports >= 20:
        score += 3
        signals.append("20+ imports")
    elif imports >= 12:
        score += 1
        signals.append("12+ imports")

    if exports >= 20:
        score += 3
        signals.append("20+ exports")
    elif exports >= 8:
        score += 1
        signals.append("8+ exports")

    lowered = path.name.lower()
    if any(name in lowered for name in GENERIC_NAMES):
        score += 1
        signals.append("generic name")

    if file_type in {"route/controller", "service/use-case", "component", "repository/query"} and loc >= 500:
        score += 2
        signals.append("likely mixed responsibilities")

    if file_type == "test" and loc >= 800:
        score += 1
        signals.append("large test file")

    risk = "critical" if score >= 6 else "high" if score >= 3 else "medium" if score >= 1 else "low"
    return risk, signals or ["no major signal"]


def analyze_file(path: Path, root: Path) -> FileRecord | None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None
    except OSError:
        return None

    loc = count_loc(text)
    imports = count_patterns(text, [r"^\s*import\s+", r"^\s*from\s+\S+\s+import\s+", r"require\(", r"^\s*using\s+"])
    exports = count_patterns(
        text,
        [
            r"^\s*export\s+(?:default\s+)?(?:async\s+)?(?:class|function|const|let|var|type|interface|enum)\b",
            r"^\s*export\s*\{",
            r"^\s*module\.exports",
            r"^\s*public\s+(?:class|interface|record|enum)",
        ],
    )
    file_type = classify_file(path)
    status = size_status(file_type, loc)
    risk, signals = score_record(path, loc, imports, exports, file_type, status)

    return FileRecord(
        path=str(path.relative_to(root)),
        loc=loc,
        imports=imports,
        exports=exports,
        file_type=file_type,
        size_status=status,
        risk=risk,
        signals=signals,
    )


def scan(root: Path, include_tests: bool) -> list[FileRecord]:
    records: list[FileRecord] = []
    for path in root.rglob("*"):
        if not path.is_file() or not is_source_file(path) or should_skip(path, include_tests):
            continue
        record = analyze_file(path, root)
        if record:
            records.append(record)
    return sorted(records, key=lambda item: (item.risk, item.loc, item.imports), reverse=True)


def summarize(records: list[FileRecord]) -> dict[str, object]:
    if not records:
        return {"files": 0, "largest": None, "over_500": 0, "over_750": 0, "over_1000": 0}
    return {
        "files": len(records),
        "largest": records[0].path,
        "over_500": sum(1 for item in records if item.loc > 500),
        "over_750": sum(1 for item in records if item.loc > 750),
        "over_1000": sum(1 for item in records if item.loc > 1000),
    }


def render_markdown(records: list[FileRecord], limit: int) -> str:
    summary = summarize(records)
    rows = records[:limit]
    lines = [
        "# Complexity Inventory",
        "",
        f"- Files scanned: {summary['files']}",
        f"- Files over 500 LOC: {summary['over_500']}",
        f"- Files over 750 LOC: {summary['over_750']}",
        f"- Files over 1,000 LOC: {summary['over_1000']}",
        f"- Largest file: {summary['largest'] or 'n/a'}",
        "",
        "| Path | LOC | Imports | Exports | Type | Status | Risk | Signals |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for item in rows:
        signals = ", ".join(item.signals)
        lines.append(
            f"| `{item.path}` | {item.loc} | {item.imports} | {item.exports} | {item.file_type} | {item.size_status} | {item.risk} | {signals} |"
        )
    if not rows:
        lines.append("| _No source files found_ | 0 | 0 | 0 | - | - | - | - |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Repository or source directory to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--limit", type=int, default=25, help="Maximum rows to print in Markdown output.")
    parser.add_argument("--include-tests", action="store_true", help="Include test files in the scan.")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        parser.error(f"path does not exist: {root}")
    if not root.is_dir():
        parser.error(f"path must be a directory: {root}")

    records = scan(root, include_tests=args.include_tests)
    payload = {"summary": summarize(records), "files": [asdict(item) for item in records]}

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(render_markdown(records, limit=max(args.limit, 0)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
