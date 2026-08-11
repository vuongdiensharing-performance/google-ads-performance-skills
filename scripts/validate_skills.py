#!/usr/bin/env python3
"""Validate Core Skill directories against SKILL_SPEC v1.1."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import yaml

REQUIRED = [
    "# ", "## Purpose", "## Use When", "## Do Not Use When",
    "## Required Inputs", "## Preconditions", "## Knowledge Dependencies",
    "## Rule Dependencies", "## Workflow", "## Output Contract",
    "## Confidence", "## Safety", "## Related Skills", "## Examples"
]


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", default="skills", type=Path)
    parser.add_argument("--registry", default="skills/registry.yaml", type=Path)
    args = parser.parse_args()

    registry = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    entries = registry.get("skills", [])
    errors: list[str] = []

    for entry in entries:
        name = entry["name"]
        path = args.skills / name / "SKILL.md"
        if not path.exists():
            errors.append(f"{name}: missing SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        if not meta.get("version"):
            errors.append(f"{name}: missing version")
        for marker in REQUIRED:
            if marker not in text:
                errors.append(f"{name}: missing section {marker}")
        if "Rule Engine Contract" not in text:
            errors.append(f"{name}: missing Rule Engine Contract")
        if "human approval" not in text.lower() and "approval" not in text.lower():
            errors.append(f"{name}: safety/approval behavior not explicit")

    if errors:
        print("SKILL VALIDATION FAILED")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"SKILL VALIDATION PASSED: {len(entries)} Core Skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
