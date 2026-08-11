#!/usr/bin/env python3
"""Validate Rule-local Boundary Contracts and Registry provenance."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALID_STATES = {
    "APPLICABLE_VALID",
    "APPLICABLE_TRIGGERED",
    "APPLICABLE_MISSING_EVIDENCE",
    "NOT_APPLICABLE",
    "CONFLICTING_EVIDENCE",
    "EXPLICIT_EXCLUSION",
}
STATE_KEYS = {"A", "B", "C", "D", "E", "F"}
EXPECTED_STATE_IDS = {
    "A": "APPLICABLE_VALID",
    "B": "APPLICABLE_TRIGGERED",
    "C": "APPLICABLE_MISSING_EVIDENCE",
    "D": "NOT_APPLICABLE",
    "E": "CONFLICTING_EVIDENCE",
    "F": "EXPLICIT_EXCLUSION",
}
REQUIRED_FIELDS = {"applicable_when", "evidence_required", "states", "conflict_policy"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def validate_rule(rule_path: Path, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rule_path = rule_path.resolve()
    try:
        rule = load_yaml(rule_path)
    except Exception as exc:
        return [f"YAML parse error: {exc}"]

    contract = rule.get("boundary_contract")
    if not isinstance(contract, dict):
        return ["missing boundary_contract"]

    missing = sorted(REQUIRED_FIELDS - set(contract))
    if missing:
        errors.append(f"boundary_contract missing fields: {', '.join(missing)}")

    if not isinstance(contract.get("applicable_when"), list) or not contract.get("applicable_when"):
        errors.append("boundary_contract.applicable_when must be a non-empty list")

    evidence = contract.get("evidence_required")
    if not isinstance(evidence, list) or not evidence:
        errors.append("boundary_contract.evidence_required must be a non-empty list")
    if evidence != rule.get("evidence_required"):
        errors.append("boundary_contract.evidence_required must exactly mirror Rule evidence_required")

    states = contract.get("states")
    if not isinstance(states, dict):
        errors.append("boundary_contract.states must be a mapping")
    else:
        if set(states) != STATE_KEYS:
            errors.append("boundary_contract.states must declare exactly A, B, C, D, E, F")
        for key, expected_id in EXPECTED_STATE_IDS.items():
            actual = states.get(key, {})
            if not isinstance(actual, dict) or actual.get("state") != expected_id:
                errors.append(f"state {key} must map to {expected_id}")

    conflict = contract.get("conflict_policy")
    if not isinstance(conflict, dict) or conflict.get("enabled") is not True:
        errors.append("boundary_contract.conflict_policy.enabled must be true")
    else:
        resolution = conflict.get("resolution")
        if not isinstance(resolution, dict):
            errors.append("conflict_policy.resolution must be a mapping")
        else:
            if resolution.get("state") != "CONFLICTING_EVIDENCE":
                errors.append("conflict policy must resolve to CONFLICTING_EVIDENCE")
            if resolution.get("inference_used") is not False:
                errors.append("conflict policy must set inference_used: false")
            if resolution.get("decision") not in {"FAIL", "PASS", "SUPPRESSED", "NOT_APPLICABLE", "INSUFFICIENT_EVIDENCE", "POLICY_DEFINED"}:
                errors.append("conflict policy has invalid decision")
        if not isinstance(conflict.get("when"), dict):
            errors.append("conflict_policy.when must be a mapping")

    if contract.get("version") != "1.0.0":
        errors.append("unsupported boundary_contract.version; expected 1.0.0")

    rule_id = rule.get("id")
    entries = [item for item in registry.get("rules", []) if item.get("id") == rule_id]
    if len(entries) != 1:
        errors.append(f"registry must contain exactly one entry for {rule_id}")
    else:
        entry = entries[0]
        expected_path = rule_path.relative_to(ROOT).as_posix()
        if entry.get("path") != expected_path:
            errors.append("registry path does not match Rule path")
        if entry.get("knowledge") != rule.get("knowledge_dependencies"):
            errors.append("registry knowledge does not exactly mirror knowledge_dependencies")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Gate 2C Boundary Contracts.")
    parser.add_argument("--rules", type=Path, default=ROOT / "rules")
    parser.add_argument("--registry", type=Path, default=ROOT / "rules/registry.yaml")
    parser.add_argument("--rule-ids", nargs="*", default=[])
    args = parser.parse_args()

    registry = load_yaml(args.registry.resolve())
    failures = 0
    candidates = sorted(args.rules.resolve().rglob("*.yaml"))
    if args.rule_ids:
        requested = set(args.rule_ids)
        candidates = [p for p in candidates if load_yaml(p).get("id") in requested]

    for path in candidates:
        errors = validate_rule(path, registry)
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
