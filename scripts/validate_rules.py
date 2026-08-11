#!/usr/bin/env python3
"""Validate Rule Spec v1 YAML assets."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

REQUIRED = {
    "id", "name", "version", "category", "description", "when",
    "exclude_when", "evidence_required", "severity", "confidence",
    "finding", "recommendation", "impact", "action",
    "human_approval_required", "related_skills",
}
MUTATING_ACTIONS = {"pause", "increase", "decrease", "change"}


def validate(path: Path) -> list[str]:
    errors = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"YAML parse error: {exc}"]
    if not isinstance(data, dict):
        return ["Rule must be a YAML mapping"]
    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if not isinstance(data.get("evidence_required", []), list):
        errors.append("evidence_required must be a list")
    if data.get("severity", {}).get("level") not in {"critical", "high", "medium", "low", "info"}:
        errors.append("invalid severity.level")
    if data.get("confidence", {}).get("level") not in {"high", "medium", "low"}:
        errors.append("invalid confidence.level")
    action = data.get("action", {}).get("type")
    if action not in {"investigate", "recommend", "prepare", "pause", "increase", "decrease", "change"}:
        errors.append("invalid action.type")
    if action in MUTATING_ACTIONS and data.get("human_approval_required") is not True:
        errors.append("mutating actions require human_approval_required: true")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", default="rules", type=Path)
    args = parser.parse_args()
    failures = 0
    for path in sorted(args.rules.rglob("*.yaml")):
        if path.resolve() == (args.rules / "registry.yaml").resolve():
            print(f"SKIP {path} (Rule registry is validated by provenance checks)")
            continue
        errors = validate(path)
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
