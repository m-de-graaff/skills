#!/usr/bin/env python3
"""Rank source files by refactor hotspot signals."""

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

GENERATED_HINTS = (
    ".generated.",
    ".gen.",
    ".min.",
    ".snap",
    "generated",
    "__generated__",
)

TEST_HINTS = (
    ".test.",
    ".spec.",
    "_test.",
    "__tests__",
    "/tests/",
    "\\tests\\",
)


@dataclass
class Hotspot:
    path: str
    loc: int
    imports: int
    exports: int
    file_type: str
    size_severity: str
    hotspot_score: int
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
    if suffix in {".tsx", ".jsx", ".vue", ".svelte"}:
        if "page" in name or "route" in name:
            return "page/route"
        return "component"
    if "route" in name or "controller" in name or "handler" in name:
        return "route/controller"
    if "repository" in name or "queries" in name or "dao" in name:
        return "repository/query"
    if "service" in name or "use-case" in name or "use_case" in name:
        return "service/use-case"
    if "schema" in name or "types" in name or name.endswith(".d.ts"):
        return "type/schema"
    if "util" in name or "helper" in name or "common" in name:
        return "utility"
    if is_test_file(path):
        return "test"
    return "source"


def severity_for(file_type: str, loc: int) -> str:
    thresholds = {
        "component": (300, 600),
        "page/route": (250, 500),
        "route/controller": (300, 700),
        "service/use-case": (500, 1000),
        "repository/query": (600, 1000),
        "utility": (300, 600),
        "type/schema": (700, 1200),
        "test": (800, 1500),
        "source": (1000, 3000),
    }
    warning, critical = thresholds.get(file_type, (1000, 3000))
    if loc >= 3000:
        return "critical"
    if loc >= critical:
        return "critical"
    if loc >= warning:
        return "warning"
    return "normal"


def score_hotspot(path: Path, loc: int, imports: int, exports: int, file_type: str, severity: str) -> tuple[int, list[str]]:
    score = 0
    signals: list[str] = []

    if loc >= 3000:
        score += 5
        signals.append("3,000+ LOC")
    elif loc >= 1000:
        score += 3
        signals.append("1,000+ LOC")
    elif severity == "critical":
        score += 3
        signals.append("critical size for type")
    elif severity == "warning":
        score += 1
        signals.append("large for type")

    if exports >= 20:
        score += 3
        signals.append("20+ exports")
    elif exports >= 8:
        score += 1
        signals.append("8+ exports")

    if imports >= 20:
        score += 3
        signals.append("20+ imports")
    elif imports >= 12:
        score += 1
        signals.append("12+ imports")

    lowered = path.name.lower()
    if any(name in lowered for name in ("utils", "helpers", "common", "manager", "processor", "service")):
        score += 1
        signals.append("vague name")

    if file_type in {"route/controller", "service/use-case", "component", "repository/query"} and loc >= 500:
        score += 2
        signals.append("likely mixed responsibilities")

    return score, signals or ["no major signal"]


def analyze_file(path: Path, root: Path) -> Hotspot | None:
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
    imports = count_patterns(
        text,
        [
            r"^\s*import\s+",
            r"^\s*from\s+\S+\s+import\s+",
            r"require\(",
            r"^\s*using\s+",
        ],
    )
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
    severity = severity_for(file_type, loc)
    score, signals = score_hotspot(path, loc, imports, exports, file_type, severity)

    return Hotspot(
        path=str(path.relative_to(root)),
        loc=loc,
        imports=imports,
        exports=exports,
        file_type=file_type,
        size_severity=severity,
        hotspot_score=score,
        signals=signals,
    )


def scan(root: Path, include_tests: bool) -> list[Hotspot]:
    hotspots: list[Hotspot] = []
    for path in root.rglob("*"):
        if not path.is_file() or not is_source_file(path) or should_skip(path, include_tests):
            continue
        hotspot = analyze_file(path, root)
        if hotspot:
            hotspots.append(hotspot)
    return sorted(hotspots, key=lambda item: (item.hotspot_score, item.loc, item.imports), reverse=True)


def render_markdown(hotspots: list[Hotspot], limit: int) -> str:
    rows = hotspots[:limit]
    lines = [
        "# Refactor Hotspots",
        "",
        "| Path | LOC | Imports | Exports | Type | Severity | Score | Signals |",
        "|---|---:|---:|---:|---|---|---:|---|",
    ]
    for item in rows:
        signals = ", ".join(item.signals)
        lines.append(
            f"| `{item.path}` | {item.loc} | {item.imports} | {item.exports} | {item.file_type} | {item.size_severity} | {item.hotspot_score} | {signals} |"
        )
    if not rows:
        lines.append("| _No source files found_ | 0 | 0 | 0 | - | - | 0 | - |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank source files by refactor hotspot signals.")
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

    hotspots = scan(root, include_tests=args.include_tests)

    if args.json:
        print(json.dumps([asdict(item) for item in hotspots], indent=2))
    else:
        print(render_markdown(hotspots, limit=max(args.limit, 0)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
