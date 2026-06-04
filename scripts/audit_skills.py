#!/usr/bin/env python3
"""Validate skill frontmatter and description budget.

This intentionally avoids a YAML dependency. The repo keeps frontmatter simple:
single-line keys with single-line values. If a future skill needs complex YAML,
that should be a deliberate change to this audit script too.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


KNOWN_CLAUDE_FRONTMATTER_KEYS = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "hooks",
    "paths",
    "shell",
}


@dataclass
class SkillFrontmatter:
    path: Path
    fields: dict[str, str]


def parse_frontmatter(path: Path) -> SkillFrontmatter:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter opener")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing YAML frontmatter closer")

    frontmatter = text[4:end]
    fields: dict[str, str] = {}
    for line_number, raw_line in enumerate(frontmatter.splitlines(), start=2):
        line = raw_line.strip()
        if not line:
            continue
        if raw_line.startswith((" ", "\t")):
            raise ValueError(f"nested or multiline YAML is not supported in audit at line {line_number}")
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line {line_number}: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"empty frontmatter key at line {line_number}")
        fields[key] = value

    return SkillFrontmatter(path=path, fields=fields)


def audit(
    root: Path,
    max_description_chars: int,
    max_total_description_chars: int,
    warn_total_description_chars: int,
) -> int:
    failures: list[str] = []
    warnings: list[str] = []
    skills: list[SkillFrontmatter] = []

    for path in sorted(root.rglob("SKILL.md")):
        try:
            skill = parse_frontmatter(path)
        except ValueError as exc:
            failures.append(f"{path}: {exc}")
            continue

        skills.append(skill)
        fields = skill.fields
        for required in ("name", "description"):
            if not fields.get(required):
                failures.append(f"{path}: missing required `{required}` frontmatter")

        unknown = sorted(set(fields) - KNOWN_CLAUDE_FRONTMATTER_KEYS)
        if unknown:
            failures.append(f"{path}: unknown Claude Code frontmatter keys: {', '.join(unknown)}")

        name = fields.get("name", "")
        if name and name != path.parent.name:
            warnings.append(f"{path}: name `{name}` differs from directory `{path.parent.name}`")

        description = fields.get("description", "")
        if description.startswith(("|", ">")):
            failures.append(f"{path}: description must be single-line to keep listing compact")
        if len(description) > max_description_chars:
            failures.append(
                f"{path}: description is {len(description)} chars; max is {max_description_chars}"
            )

        when_to_use = fields.get("when_to_use", "")
        if when_to_use and len(description) + len(when_to_use) > max_description_chars:
            failures.append(
                f"{path}: description + when_to_use is {len(description) + len(when_to_use)} chars; "
                f"max is {max_description_chars}"
            )

    total_description_chars = sum(len(skill.fields.get("description", "")) for skill in skills)
    if total_description_chars > max_total_description_chars:
        failures.append(
            f"total description budget is {total_description_chars} chars; "
            f"max is {max_total_description_chars}"
        )
    elif total_description_chars > warn_total_description_chars:
        warnings.append(
            f"total description budget is {total_description_chars} chars; "
            f"warning threshold is {warn_total_description_chars}"
        )

    print(f"skills: {len(skills)}")
    print(f"total description chars: {total_description_chars}")
    print(f"max description chars: {max((len(s.fields.get('description', '')) for s in skills), default=0)}")

    if warnings:
        print("\nwarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if failures:
        print("\nfailures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nSkill audit passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="skills", help="Root directory containing skill folders.")
    parser.add_argument("--max-description-chars", type=int, default=180)
    parser.add_argument("--max-total-description-chars", type=int, default=4000)
    parser.add_argument("--warn-total-description-chars", type=int, default=3500)
    args = parser.parse_args()

    return audit(
        root=Path(args.root),
        max_description_chars=args.max_description_chars,
        max_total_description_chars=args.max_total_description_chars,
        warn_total_description_chars=args.warn_total_description_chars,
    )


if __name__ == "__main__":
    raise SystemExit(main())
