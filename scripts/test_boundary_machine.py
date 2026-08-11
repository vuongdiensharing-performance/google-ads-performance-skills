#!/usr/bin/env python3
"""Execute the 36 Gate 2C Boundary fixtures and determinism assertions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rule_engine import evaluate_rule, load_rules  # noqa: E402
from validate_boundary_contract import load_yaml, validate_rule  # noqa: E402

EXPECTED_IDS = {
    "A": "APPLICABLE_VALID",
    "B": "APPLICABLE_TRIGGERED",
    "C": "APPLICABLE_MISSING_EVIDENCE",
    "D": "NOT_APPLICABLE",
    "E": "CONFLICTING_EVIDENCE",
    "F": "EXPLICIT_EXCLUSION",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=ROOT / "evals/account-audit/boundary_matrix.yaml")
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()

    registry = load_yaml(ROOT / "rules/registry.yaml")
    rules = {rule.get("id"): rule for rule in load_rules(ROOT / "rules")}
    matrix = load_yaml(args.fixtures)
    cases = matrix.get("cases", [])
    if len(cases) != 36:
        print(f"FAIL expected 36 boundary fixtures, found {len(cases)}")
        return 1

    target_ids = sorted({case["rule_id"] for case in cases})
    for rule_id in target_ids:
        rule = rules.get(rule_id)
        if rule is None:
            print(f"FAIL missing Rule {rule_id}")
            return 1
        errors = validate_rule(Path(rule["_source"]), registry)
        if errors:
            print(f"FAIL contract {rule_id}")
            for error in errors:
                print(f"  - {error}")
            return 1

    failures = 0
    for case in cases:
        rule = rules[case["rule_id"]]
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
            print(
                f"FAIL {case['case_id']}: expected {expected_state}/{expected_decision}, "
                f"got {first['boundary_state']}/{first['decision']}"
            )
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
