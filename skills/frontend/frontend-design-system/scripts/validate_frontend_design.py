#!/usr/bin/env python3
"""Validate the structure of a frontend design system response."""

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
    "design_direction": [r"design direction"],
    "information_architecture": [r"information architecture", r"\bia\b"],
    "layout_specification": [r"layout specification", r"\blayout\b"],
    "visual_system": [r"visual system", r"color", r"typography"],
    "component_specifications": [r"component specifications", r"component", r"state matrix"],
    "theme_tokens": [r"theme tokens", r"light/dark", r"css variables", r"--background"],
    "implementation_guidance": [r"implementation guidance", r"react", r"next\.js", r"tailwind"],
    "accessibility_qa": [r"accessibility", r"qa checklist", r"keyboard", r"focus"],
}


QUALITY_WARNINGS = {
    "theme_modes": [r"data-theme", r"light", r"dark", r"system"],
    "semantic_tokens": [r"--background", r"--surface", r"--foreground", r"--border", r"--accent"],
    "component_states": [r"hover", r"active", r"focus-visible", r"disabled"],
    "loading_error_states": [r"loading", r"error"],
    "responsive": [r"responsive", r"breakpoint", r"mobile", r"desktop"],
    "reduced_motion": [r"reduced motion", r"prefers-reduced-motion"],
    "contrast": [r"contrast", r"wcag"],
    "keyboard": [r"keyboard", r"focus"],
}


ANTI_PATTERNS = {
    "generic_ai_copy": [r"unlock the power of ai", r"revolutionize your workflow", r"seamless experience"],
    "gradient_blob": [r"gradient blob", r"neon glow", r"glassmorphism"],
    "fake_social_proof": [r"trusted by.*teams", r"10,000\+ customers", r"fake logo", r"testimonial"],
}


def any_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def validate(text: str) -> list[Check]:
    checks: list[Check] = []
    normalized = text.lower()

    for code, patterns in REQUIRED_SECTIONS.items():
        if not any_pattern(normalized, patterns):
            checks.append(Check("FAIL", f"missing_{code}", f"Missing required design section for {code.replace('_', ' ')}."))

    for code, patterns in QUALITY_WARNINGS.items():
        if not any_pattern(normalized, patterns):
            checks.append(Check("WARN", f"weak_{code}", f"Add or strengthen {code.replace('_', ' ')} guidance."))

    for code, patterns in ANTI_PATTERNS.items():
        if any_pattern(normalized, patterns):
            checks.append(Check("WARN", f"anti_pattern_{code}", f"Potential generic/frontend anti-pattern detected: {code.replace('_', ' ')}."))

    raw_hex_count = count_pattern(text, r"#[0-9a-fA-F]{6}")
    css_var_count = count_pattern(text, r"--[a-zA-Z][a-zA-Z0-9-]*")
    if raw_hex_count > 8 and css_var_count < 6:
        checks.append(Check("WARN", "raw_hex_without_tokens", "Many raw hex values detected without enough CSS variable tokens."))

    state_words = ["default", "hover", "active", "focus", "disabled", "loading", "error"]
    found_states = sum(1 for word in state_words if re.search(rf"\b{word}\b", normalized))
    if found_states < 5:
        checks.append(Check("WARN", "incomplete_state_matrix", "Component state coverage appears incomplete."))

    if not checks:
        checks.append(Check("PASS", "complete", "Frontend design spec includes the required structure and quality signals."))

    return checks


def print_text(checks: list[Check]) -> None:
    for check in checks:
        print(f"{check.level}: {check.code} - {check.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a frontend design system Markdown response.")
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
