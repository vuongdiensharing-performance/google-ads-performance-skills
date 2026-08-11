#!/usr/bin/env python3
"""Execute the 36 Gate 2C Boundary fixtures and determinism assertions."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rule_engine import evaluate_rule  # noqa: E402
from validate_boundary_contract import (  # noqa: E402
    EXPECTED_STATE_IDS,
    canonical_contract,
    load_yaml,
    validate_global_contract,
    validate_registry,
    validate_rule,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=ROOT / "evals/account-audit/boundary_matrix.yaml")
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    if args.runs < 2:
        print("FAIL --runs must be >= 2 for determinism testing")
        return 1

    schema = json.loads((ROOT / "schemas/boundary-contract.json").read_text(encoding="utf-8"))
    global_errors = validate_global_contract(schema)
    registry = load_yaml(ROOT / "rules/registry.yaml")
    global_errors.extend(validate_registry(registry))
    if global_errors:
        print("FAIL global Gate 2C contract")
        for error in global_errors:
            print(f"  - {error}")
        return 1

    precedence, decisions, findings = canonical_contract(schema)
    matrix = load_yaml(args.fixtures)
    cases = matrix.get("cases", [])
    if len(cases) != 36:
        print(f"FAIL expected 36 boundary fixtures, found {len(cases)}")
        return 1

    expected_rule_ids = {
        "STR-FRAG-001", "CV-TRACK-001", "BID-OBJ-001",
        "BUD-OPP-001", "ST-SPEND-001", "PMAX-GOAL-001",
    }
    expected_state_ids = set(EXPECTED_STATE_IDS.values())
    case_ids = [case.get("case_id") for case in cases]
    pairs = [(case.get("rule_id"), case.get("expected", {}).get("state")) for case in cases]
    failures = 0

    if len(set(case_ids)) != 36:
        print("FAIL boundary matrix contains duplicate case_id values")
        return 1
    if {case.get("rule_id") for case in cases} != expected_rule_ids:
        print("FAIL boundary matrix must cover exactly the six Gate 2C Rule IDs")
        return 1
    if set(state for _, state in pairs) != expected_state_ids:
        print("FAIL boundary matrix must cover all six A-F states")
        return 1
    if Counter(pairs).most_common(1)[0][1] != 1:
        print("FAIL boundary matrix must contain exactly one fixture per Rule/state pair")
        return 1
    if len(set(pairs)) != 36:
        print("FAIL boundary matrix must contain exactly 36 unique Rule/state pairs")
        return 1

    registry_by_id = {item.get("id"): item for item in registry.get("rules", [])}
    rules = {}
    for rule_id in expected_rule_ids:
        entry = registry_by_id.get(rule_id)
        if not entry:
            print(f"FAIL registry missing {rule_id}")
            return 1
        path = ROOT / entry["path"]
        rules[rule_id] = load_yaml(path)
        rules[rule_id]["_source"] = str(path)
        errors = validate_rule(path, registry, schema)
        if errors:
            failures += 1
            print(f"FAIL contract {rule_id}")
            for error in errors:
                print(f"  - {error}")

    if failures:
        return 1

    required_output = {
        "rule_id", "boundary_state", "decision", "inference_used",
        "evidence_sufficient", "finding_generated", "audit_trail",
    }

    for case in cases:
        rule_id = case["rule_id"]
        rule = rules[rule_id]
        expected = case["expected"]
        observed = [evaluate_rule(rule, case["context"])["boundary"] for _ in range(args.runs)]
        first = observed[0]

        if any(item != first for item in observed[1:]):
            failures += 1
            print(f"FAIL {case['case_id']}: non-deterministic boundary result")
            continue

        expected_state = expected["state"]
        expected_decision = expected["decision"]
        expected_finding = findings[expected_state]
        expected_evidence_sufficient = expected_state != "APPLICABLE_MISSING_EVIDENCE"

        if set(first) != required_output:
            failures += 1
            print(f"FAIL {case['case_id']}: machine-readable contract fields mismatch")
            continue
        if first["boundary_state"] != expected_state or first["decision"] != expected_decision:
            failures += 1
            print(f"FAIL {case['case_id']}: expected {expected_state}/{expected_decision}, got {first['boundary_state']}/{first['decision']}")
            continue
        if decisions.get(expected_state) != expected_decision and not (
            expected_state == "CONFLICTING_EVIDENCE" and expected_decision == rule["boundary_contract"]["conflict_policy"]["resolution"]["decision"]
        ):
            failures += 1
            print(f"FAIL {case['case_id']}: fixture decision conflicts with canonical state contract")
            continue
        if expected_state not in precedence:
            failures += 1
            print(f"FAIL {case['case_id']}: state missing from canonical precedence")
            continue
        if first["inference_used"] is not False:
            failures += 1
            print(f"FAIL {case['case_id']}: inference_used must be false")
            continue
        if first["evidence_sufficient"] is not expected_evidence_sufficient:
            failures += 1
            print(f"FAIL {case['case_id']}: evidence_sufficient invariant violated")
            continue
        audit = first["audit_trail"]
        if not isinstance(audit, dict) or not audit.get("rule") or not audit.get("knowledge") or "evidence" not in audit:
            failures += 1
            print(f"FAIL {case['case_id']}: incomplete audit trail")
            continue
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
