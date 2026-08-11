#!/usr/bin/env python3
"""Execute the 36 Gate 2C Boundary fixtures and determinism assertions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rule_engine import evaluate_rule  # noqa: E402
from validate_boundary_contract import load_yaml, validate_rule  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=ROOT / "evals/account-audit/boundary_matrix.yaml")
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()

    registry = load_yaml(ROOT / "rules/registry.yaml")
    registry_by_id = {item.get("id"): item for item in registry.get("rules", [])}
    matrix = load_yaml(args.fixtures)
    cases = matrix.get("cases", [])
    if len(cases) != 36:
        print(f"FAIL expected 36 boundary fixtures, found {len(cases)}")
        return 1

    rules = {}
    for rule_id, entry in registry_by_id.items():
        if rule_id in {case["rule_id"] for case in cases}:
            path = ROOT / entry["path"]
            rules[rule_id] = load_yaml(path)
            rules[rule_id]["_source"] = str(path)

    failures = 0
    for rule_id, rule in rules.items():
        errors = validate_rule(Path(rule["_source"]), registry)
        if errors:
            failures += 1
            print(f"FAIL contract {rule_id}")
            for error in errors:
                print(f"  - {error}")

    if failures:
        return 1

    for case in cases:
        rule_id = case["rule_id"]
        if rule_id not in rules:
            print(f"FAIL {case['case_id']}: Rule {rule_id} is not present in registry")
            return 1
        rule = rules[rule_id]
        expected = case["expected"]
        observed = []
        for _ in range(args.runs):
            result = evaluate_rule(rule, case["context"])
            observed.append(result["boundary"])

        first = observed[0]
        if any(item != first for item in observed[1:]):
            failures += 1
            print(f"FAIL {case['case_id']}: non-deterministic boundary result")
            continue

        expected_state = expected["state"]
        expected_decision = expected["decision"]
        if first["boundary_state"] != expected_state or first["decision"] != expected_decision:
            failures += 1
            print(f"FAIL {case['case_id']}: expected {expected_state}/{expected_decision}, got {first['boundary_state']}/{first['decision']}")
            continue
        if first["inference_used"] is not False:
            failures += 1
            print(f"FAIL {case['case_id']}: inference_used must be false")
            continue
        if not first.get("audit_trail", {}).get("rule"):
            failures += 1
            print(f"FAIL {case['case_id']}: missing audit trail rule")
            continue
        if not first.get("audit_trail", {}).get("knowledge"):
            failures += 1
            print(f"FAIL {case['case_id']}: missing audit trail knowledge")
            continue
        expected_finding = expected_state == "APPLICABLE_TRIGGERED"
        if first["finding_generated"] is not expected_finding:
            failures += 1
            print(f"FAIL {case['case_id']}: finding_generated invariant violated")
            continue
        print(f"PASS {case['case_id']} {expected_state} {expected_decision}")

    print(f"\nBoundary matrix: {len(cases) - failures}/36 passed")
    print(f"Determinism runs per case: {args.runs}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
