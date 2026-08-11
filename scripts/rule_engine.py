#!/usr/bin/env python3
"""Deterministic Rule Engine for Google Ads Performance Skills."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

MUTATING_ACTIONS = {"pause", "increase", "decrease", "change"}
EXPRESSION_RE = re.compile(r"^\s*(?P<path>[A-Za-z0-9_.-]+)\s*(?P<op>==|!=|>=|<=|>|<|\bin\b|\bnot in\b)\s*(?P<value>.+?)\s*$")
BOUNDARY_DECISIONS = {
    "APPLICABLE_VALID": "PASS",
    "APPLICABLE_TRIGGERED": "FAIL",
    "APPLICABLE_MISSING_EVIDENCE": "INSUFFICIENT_EVIDENCE",
    "NOT_APPLICABLE": "NOT_APPLICABLE",
    "CONFLICTING_EVIDENCE": "POLICY_DEFINED",
    "EXPLICIT_EXCLUSION": "SUPPRESSED",
}


def get_path(data: Any, path: str) -> tuple[bool, Any]:
    current = data
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def resolve(value: Any, context: dict[str, Any]) -> Any:
    if isinstance(value, str) and value.startswith("$"):
        found, resolved = get_path(context, value[1:])
        return resolved if found else None
    return value


def parse_expression_value(raw: str) -> Any:
    raw = raw.strip().strip('"').strip("'")
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


def compare(actual: Any, expected: Any, operator: str, context: dict[str, Any]) -> bool:
    expected = resolve(expected, context)
    try:
        if operator in {"eq", "=="}:
            return actual == expected
        if operator in {"ne", "!="}:
            return actual != expected
        if operator in {"in"}:
            return actual in expected
        if operator in {"not_in", "not in"}:
            return actual not in expected
        if operator in {"gt", ">"}:
            return actual is not None and actual > expected
        if operator in {"gte", ">="}:
            return actual is not None and actual >= expected
        if operator in {"lt", "<"}:
            return actual is not None and actual < expected
        if operator in {"lte", "<="}:
            return actual is not None and actual <= expected
        if operator == "contains":
            return expected in actual if actual is not None else False
    except (TypeError, ValueError):
        return False
    return False


def evaluate_expression(expression: str, context: dict[str, Any]) -> bool:
    match = EXPRESSION_RE.match(expression)
    if not match:
        return False
    found, actual = get_path(context, match.group("path"))
    if not found:
        return False
    expected = parse_expression_value(match.group("value"))
    return compare(actual, expected, match.group("op"), context)


def evaluate_condition(condition: Any, context: dict[str, Any]) -> bool:
    """Evaluate Rule Spec v1 condition syntax, including expression-list rules."""
    if condition in (None, [], {}):
        return True
    if isinstance(condition, str):
        return evaluate_expression(condition, context)
    if isinstance(condition, list):
        return all(evaluate_condition(item, context) for item in condition)
    if not isinstance(condition, dict):
        return bool(condition)

    if "all" in condition:
        return all(evaluate_condition(item, context) for item in condition["all"])
    if "any" in condition:
        return any(evaluate_condition(item, context) for item in condition["any"])
    if "not" in condition:
        return not evaluate_condition(condition["not"], context)

    for key, expected in condition.items():
        found, actual = get_path(context, key)
        if isinstance(expected, dict):
            for operator, value in expected.items():
                op = {"equals": "eq", "not_equals": "ne"}.get(operator, operator)
                if not found or not compare(actual, value, op, context):
                    return False
        else:
            if not found or actual != resolve(expected, context):
                return False
    return True


def evidence_available(requirement: str, context: dict[str, Any]) -> bool:
    candidates = [requirement, f"evidence.{requirement}"]
    aliases = {
        "keyword_match_type": ["keyword.match_type", "match_type"],
        "campaign_bidding_strategy": ["campaign.bidding_strategy", "bidding_strategy"],
        "search_term_spend": ["search_term.spend", "spend"],
        "search_term_conversions": ["search_term.conversions", "conversions"],
        "lookback_window": ["lookback_days", "evidence.lookback_days"],
        "tracking_status": ["evidence.tracking_status", "conversion_tracking.status"],
        "primary_conversion_definition": ["conversion.primary_definition"],
        "campaign_type": ["campaign.type"],
        "primary_conversion_goal": ["conversion.primary_goal"],
        "business_outcome_definition": ["business.outcome"],
        "query_or_keyword_intent": ["query.intent", "keyword.intent"],
        "ad_content": ["ad.content"],
        "landing_page_content": ["landing_page.content"],
    }
    candidates.extend(aliases.get(requirement, []))
    for candidate in candidates:
        found, value = get_path(context, candidate)
        if found and value not in (None, "", []):
            return True
    return False


def evaluate_exclusions(exclusions: Any, context: dict[str, Any]) -> bool:
    return bool(exclusions) and any(evaluate_condition(item, context) for item in exclusions)


def _boundary_state(rule: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Resolve the explicit A-F Boundary Contract without model inference."""
    contract = rule.get("boundary_contract")
    if not isinstance(contract, dict):
        raise ValueError(f"Rule {rule.get('id')} has no boundary_contract")

    applicable = evaluate_condition({"all": contract.get("applicable_when", [])}, context)
    if not applicable:
        state = "NOT_APPLICABLE"
        evidence_sufficient = True
    else:
        required = contract.get("evidence_required", rule.get("evidence_required", []))
        missing = [item for item in required if not evidence_available(item, context)]
        if missing:
            state = "APPLICABLE_MISSING_EVIDENCE"
            evidence_sufficient = False
        elif evaluate_condition((contract.get("conflict_policy") or {}).get("when"), context):
            state = "CONFLICTING_EVIDENCE"
            evidence_sufficient = True
        elif evaluate_exclusions(rule.get("exclude_when"), context):
            state = "EXPLICIT_EXCLUSION"
            evidence_sufficient = True
        elif evaluate_condition(rule.get("when"), context):
            state = "APPLICABLE_TRIGGERED"
            evidence_sufficient = True
        else:
            state = "APPLICABLE_VALID"
            evidence_sufficient = True

    policy = (contract.get("conflict_policy") or {}).get("resolution", {})
    decision = BOUNDARY_DECISIONS[state]
    if state == "CONFLICTING_EVIDENCE":
        if policy.get("state") != state:
            raise ValueError(f"Rule {rule.get('id')} conflict policy must resolve to {state}")
        decision = policy.get("decision", decision)

    finding_generated = state == "APPLICABLE_TRIGGERED"
    return {
        "rule_id": rule.get("id"),
        "boundary_state": state,
        "decision": decision,
        "inference_used": False,
        "evidence_sufficient": evidence_sufficient,
        "finding_generated": finding_generated,
        "audit_trail": {
            "evidence": context.get("evidence", context),
            "rule": str(rule.get("_source")),
            "knowledge": rule.get("knowledge_dependencies", []),
        },
    }


def evaluate_rule(rule: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    boundary = _boundary_state(rule, context) if "boundary_contract" in rule else None
    required = rule.get("evidence_required", [])
    missing = [item for item in required if not evidence_available(item, context)]
    if missing:
        result = {"rule_id": rule.get("id"), "status": "insufficient_evidence", "missing_evidence": missing, "source": rule.get("_source")}
    elif evaluate_exclusions(rule.get("exclude_when"), context):
        result = {"rule_id": rule.get("id"), "status": "excluded", "source": rule.get("_source")}
    elif not evaluate_condition(rule.get("when"), context):
        result = {"rule_id": rule.get("id"), "status": "not_matched", "source": rule.get("_source")}
    else:
        action_type = (rule.get("action") or {}).get("type", "recommend")
        approval_required = bool(rule.get("human_approval_required", False)) or action_type in MUTATING_ACTIONS
        result = {
            "rule_id": rule.get("id"),
            "status": "matched",
            "severity": (rule.get("severity") or {}).get("level"),
            "confidence": (rule.get("confidence") or {}).get("level"),
            "finding": rule.get("finding", {}),
            "recommendation": rule.get("recommendation", []),
            "impact": rule.get("impact", {}),
            "action": {"type": action_type, "human_approval_required": approval_required},
            "related_skills": rule.get("related_skills", []),
            "source": rule.get("_source"),
        }
    if boundary is not None:
        result["boundary"] = boundary
    return result


def run(rule_dir: Path, context: dict[str, Any]) -> dict[str, Any]:
    results = [evaluate_rule(rule, context) for rule in load_rules(rule_dir)]
    boundary_results = [r["boundary"] for r in results if "boundary" in r]
    return {
        "engine_version": "1.1.0",
        "matched": [r for r in results if r["status"] == "matched"],
        "insufficient_evidence": [r for r in results if r["status"] == "insufficient_evidence"],
        "excluded": [r for r in results if r["status"] == "excluded"],
        "not_matched": [r for r in results if r["status"] == "not_matched"],
        "boundary": boundary_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Google Ads Performance rule files.")
    parser.add_argument("--rules", default="rules", type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    with args.input.open("r", encoding="utf-8") as handle:
        context = json.load(handle)
    print(json.dumps(run(args.rules, context), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
