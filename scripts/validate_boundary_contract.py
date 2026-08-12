#!/usr/bin/env python3
"""Validate Gate 2C Rule-local Boundary Contracts and provenance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/boundary-contract.json"
STATE_KEYS = ("A", "B", "C", "D", "E", "F")
EXPECTED_STATE_IDS = {
    "A": "APPLICABLE_VALID",
    "B": "APPLICABLE_TRIGGERED",
    "C": "APPLICABLE_MISSING_EVIDENCE",
    "D": "NOT_APPLICABLE",
    "E": "CONFLICTING_EVIDENCE",
    "F": "EXPLICIT_EXCLUSION",
}
REQUIRED_FIELDS = {"version", "applicable_when", "evidence_required", "states", "conflict_policy"}
ALLOWED_DECISIONS = {"FAIL", "PASS", "SUPPRESSED", "NOT_APPLICABLE", "INSUFFICIENT_EVIDENCE", "POLICY_DEFINED"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def canonical_contract(schema: dict[str, Any]) -> tuple[list[str], dict[str, str], dict[str, bool]]:
    precedence = schema.get("x-canonical-resolution-precedence")
    decisions = schema.get("x-canonical-decisions")
    findings = schema.get("x-canonical-finding-generated")
    if precedence is None or decisions is None or findings is None:
        raise ValueError("boundary-contract.json is missing canonical invariant annotations")
    if not isinstance(precedence, list) or not isinstance(decisions, dict) or not isinstance(findings, dict):
        raise ValueError("canonical invariant annotations have invalid types")
    return precedence, decisions, findings


def validate_global_contract(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    precedence, decisions, findings = canonical_contract(schema)
    expected_precedence = [
        "NOT_APPLICABLE",
        "APPLICABLE_MISSING_EVIDENCE",
        "CONFLICTING_EVIDENCE",
        "EXPLICIT_EXCLUSION",
        "APPLICABLE_TRIGGERED",
        "APPLICABLE_VALID",
    ]
    if precedence != expected_precedence:
        errors.append("canonical resolution precedence does not match Gate 2C contract")
    if set(decisions) != set(EXPECTED_STATE_IDS.values()):
        errors.append("canonical decision map must cover exactly A-F state IDs")
    if set(findings) != set(EXPECTED_STATE_IDS.values()):
        errors.append("canonical finding map must cover exactly A-F state IDs")
    if any(not isinstance(value, bool) for value in findings.values()):
        errors.append("canonical finding map values must be booleans")
    return errors


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    entries = registry.get("rules")
    if not isinstance(entries, list):
        return ["registry.rules must be a list"]
    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    duplicates = sorted({rule_id for rule_id in ids if rule_id is not None and ids.count(rule_id) > 1})
    if duplicates:
        errors.append(f"registry contains duplicate Rule IDs: {', '.join(duplicates)}")
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("id") or not entry.get("path"):
            errors.append("every registry entry must declare id and path")
    return errors


def validate_schema_contract(contract: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Apply the canonical JSON Schema before any semantic cross-checks."""
    document = {
        "boundary_contract": contract,
        "resolution_precedence": schema["x-canonical-resolution-precedence"],
    }
    validator = Draft202012Validator(schema)
    return [
        error.message
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path))
    ]


def validate_rule(rule_path: Path, registry: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        rule = load_yaml(rule_path)
    except Exception as exc:
        return [f"YAML parse error: {exc}"]

    contract = rule.get("boundary_contract")
    if not isinstance(contract, dict):
        return ["missing boundary_contract"]

    errors.extend(f"schema: {error}" for error in validate_schema_contract(contract, schema))

    missing = sorted(REQUIRED_FIELDS - set(contract))
    if missing:
        errors.append(f"boundary_contract missing fields: {', '.join(missing)}")

    if contract.get("version") != "1.0.0":
        errors.append("unsupported boundary_contract.version; expected 1.0.0")

    applicable = contract.get("applicable_when")
    if not isinstance(applicable, list) or not applicable:
        errors.append("boundary_contract.applicable_when must be a non-empty list")

    evidence = contract.get("evidence_required")
    if not isinstance(evidence, list) or not evidence:
        errors.append("boundary_contract.evidence_required must be a non-empty list")
    if evidence != rule.get("evidence_required"):
        errors.append("boundary_contract.evidence_required must exactly mirror Rule evidence_required")

    states = contract.get("states")
    if not isinstance(states, dict) or tuple(states.keys()) != STATE_KEYS:
        errors.append("boundary_contract.states must declare exactly A, B, C, D, E, F")
    else:
        for key, expected_id in EXPECTED_STATE_IDS.items():
            state = states.get(key)
            if not isinstance(state, dict) or state.get("state") != expected_id:
                errors.append(f"state {key} must map to {expected_id}")

    conflict = contract.get("conflict_policy")
    if not isinstance(conflict, dict) or conflict.get("enabled") is not True:
        errors.append("boundary_contract.conflict_policy.enabled must be true")
    else:
        if not isinstance(conflict.get("when"), dict):
            errors.append("conflict_policy.when must be a mapping")
        resolution = conflict.get("resolution")
        if not isinstance(resolution, dict):
            errors.append("conflict_policy.resolution must be a mapping")
        else:
            if resolution.get("state") != "CONFLICTING_EVIDENCE":
                errors.append("conflict policy must resolve to CONFLICTING_EVIDENCE")
            if resolution.get("inference_used") is not False:
                errors.append("conflict policy must set inference_used: false")
            if resolution.get("decision") not in ALLOWED_DECISIONS:
                errors.append("conflict policy has invalid decision")

    rule_id = rule.get("id")
    entries = [item for item in registry.get("rules", []) if item.get("id") == rule_id]
    if len(entries) != 1:
        errors.append(f"registry must contain exactly one entry for {rule_id}")
    else:
        entry = entries[0]
        expected_path = rule_path.resolve().relative_to(ROOT).as_posix()
        if entry.get("path") != expected_path:
            errors.append("registry path does not match Rule path")
        if entry.get("knowledge") != rule.get("knowledge_dependencies"):
            errors.append("registry knowledge does not exactly mirror knowledge_dependencies")
        if not (ROOT / entry.get("path", "")).is_file():
            errors.append("registry path does not resolve to an existing Rule file")

    _, decisions, findings = canonical_contract(schema)
    for state_id, decision in decisions.items():
        if decision not in ALLOWED_DECISIONS:
            errors.append(f"canonical decision for {state_id} is invalid")
    for state in states.values() if isinstance(states, dict) else []:
        if isinstance(state, dict):
            state_id = state.get("state")
            if state_id in decisions and state.get("decision", decisions[state_id]) != decisions[state_id]:
                errors.append(f"Rule-local decision for {state_id} conflicts with canonical decision")
            if state_id in findings and state.get("finding_generated", findings[state_id]) != findings[state_id]:
                errors.append(f"Rule-local finding_generated for {state_id} conflicts with canonical contract")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Gate 2C Boundary Contracts.")
    parser.add_argument("--rules", type=Path, default=ROOT / "rules")
    parser.add_argument("--registry", type=Path, default=ROOT / "rules/registry.yaml")
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    parser.add_argument("--rule-ids", nargs="*", default=[])
    args = parser.parse_args()

    global_errors: list[str] = []
    try:
        schema = json.loads(args.schema.resolve().read_text(encoding="utf-8"))
        global_errors.extend(validate_global_contract(schema))
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        global_errors.append(f"boundary schema error: {exc}")
        schema = {}

    registry = load_yaml(args.registry.resolve())
    global_errors.extend(validate_registry(registry))
    if global_errors:
        print("FAIL global Gate 2C contract")
        for error in global_errors:
            print(f"  - {error}")
        return 1

    registry_by_id = {item.get("id"): item for item in registry.get("rules", [])}
    if args.rule_ids:
        missing = [rule_id for rule_id in args.rule_ids if rule_id not in registry_by_id]
        if missing:
            print(f"FAIL registry missing requested Rule IDs: {', '.join(missing)}")
            return 1
        candidates = [ROOT / registry_by_id[rule_id]["path"] for rule_id in args.rule_ids]
    else:
        candidates = sorted(args.rules.resolve().rglob("*.yaml"))
        candidates = [path for path in candidates if path.resolve() != args.registry.resolve()]

    failures = 0
    for path in candidates:
        errors = validate_rule(path, registry, schema)
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
