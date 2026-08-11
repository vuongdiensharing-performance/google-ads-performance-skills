#!/usr/bin/env python3
"""Minimal runtime that wires a Core Skill registry entry to the Rule Engine."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import yaml

from rule_engine import evaluate_rule, load_rules


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the declared Rules for a Core Skill.")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--registry", default="skills/registry.yaml", type=Path)
    parser.add_argument("--rules", default="rules", type=Path)
    args = parser.parse_args()

    registry = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    entry = next((item for item in registry.get("skills", []) if item["name"] == args.skill), None)
    if not entry:
        raise SystemExit(f"Unknown Core Skill: {args.skill}")

    context = json.loads(args.input.read_text(encoding="utf-8"))
    all_rules = load_rules(args.rules)
    selected = [r for r in all_rules if args.skill in r.get("related_skills", [])]
    results = [evaluate_rule(rule, context) for rule in selected]

    output = {
        "runtime_version": "1.0.0",
        "skill": entry,
        "rule_count": len(selected),
        "matched": [r for r in results if r["status"] == "matched"],
        "insufficient_evidence": [r for r in results if r["status"] == "insufficient_evidence"],
        "excluded": [r for r in results if r["status"] == "excluded"],
        "not_matched": [r for r in results if r["status"] == "not_matched"],
        "next_stage": "Skill output contract must classify, prioritize, recommend, and define measurement.",
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
