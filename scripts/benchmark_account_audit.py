#!/usr/bin/env python3
"""Execute the account-audit golden benchmark against the deterministic Rule Engine."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rule_engine import evaluate_rule, load_rules  # noqa: E402


def load_registry(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def account_audit_rules(all_rules: list[dict]) -> list[dict]:
    return [rule for rule in all_rules if "account-audit" in rule.get("related_skills", [])]


def expected_priority(matched: list[dict]) -> str:
    if any(item.get("severity") == "critical" for item in matched):
        return "P0"
    return "P3"


def evaluate_case(case: dict, rules: list[dict]) -> tuple[bool, dict]:
    results = [evaluate_rule(rule, case.get("context", {})) for rule in rules]
    matched = [r for r in results if r["status"] == "matched"]
    insufficient = [r for r in results if r["status"] == "insufficient_evidence"]
    excluded = [r for r in results if r["status"] == "excluded"]

    expected = case.get("expected", {})
    expected_ids = set(expected.get("required_findings", []))
    actual_ids = {r["rule_id"] for r in matched}
    excluded_ids = {r["rule_id"] for r in excluded}

    klass = case["class"]
    if klass == "PASS":
        ok = not matched and not insufficient
    elif klass == "FAIL":
        ok = expected_ids.issubset(actual_ids)
    elif klass == "INSUFFICIENT_EVIDENCE":
        ok = bool(insufficient) and not matched
    elif klass == "FALSE_POSITIVE":
        excluded_expected = set(expected.get("excluded_findings", []))
        ok = not matched and excluded_expected.issubset(excluded_ids)
    else:
        return False, {"error": f"unknown class: {klass}"}

    approval = any(item.get("action", {}).get("human_approval_required") for item in matched)
    if "approval_required" in expected:
        ok = ok and approval == expected["approval_required"]

    if klass == "FAIL" and "priority" in expected:
        ok = ok and expected_priority(matched) == expected["priority"]

    detail = {
        "class": klass,
        "matched": sorted(actual_ids),
        "insufficient_evidence": sorted(r["rule_id"] for r in insufficient),
        "excluded": sorted(excluded_ids),
        "derived_priority": expected_priority(matched),
        "approval_required": approval,
    }
    return ok, detail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default="evals/account-audit/benchmark.yaml", type=Path)
    parser.add_argument("--rules", default="rules", type=Path)
    parser.add_argument("--registry", default="skills/registry.yaml", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    benchmark = yaml.safe_load(args.benchmark.read_text(encoding="utf-8"))
    registry = load_registry(args.registry)
    assert any(item.get("name") == benchmark["skill"] for item in registry["skills"]), "account-audit missing from registry"

    rules = account_audit_rules(load_rules(args.rules))
    if not rules:
        raise SystemExit("No rules are wired to account-audit")

    results = []
    passed = 0
    for case in benchmark.get("cases", []):
        ok, detail = evaluate_case(case, rules)
        passed += int(ok)
        results.append({"id": case["id"], "pass": ok, **detail})
        print(f"{'PASS' if ok else 'FAIL'} {case['id']} — matched={detail.get('matched')} excluded={detail.get('excluded')} insufficient={detail.get('insufficient_evidence')}")

    summary = {
        "benchmark": benchmark["benchmark"],
        "skill": benchmark["skill"],
        "rule_count": len(rules),
        "cases": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": passed / len(results) if results else 0,
        "results": results,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
