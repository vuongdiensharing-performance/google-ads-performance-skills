#!/usr/bin/env python3
"""Minimal rule engine for Google Ads Performance Skills.

The engine evaluates YAML rules against a JSON-compatible context. It is
intentionally deterministic and evidence-first; it does not invent missing
values or infer thresholds that are not encoded in a rule.

Usage:
    python scripts/rule_engine.py --rules rules --input examples/rule-engine/context.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

MUTATING_ACTIONS = {"pause", "increase", "decrease", "change"}


def get_path(data: Any, path: str) -> tuple[bool, Any]:
    """Read dotted paths from nested dictionaries."""
    current = data
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def resolve(value: Any, context: dict[str, Any]) -> Any:
    """Resolve a context reference written as `$path`."""
    if isinstance(value, str) and value.startswith("$"):
        found, resolved = get_path(context, value[1:])
        return resolved if found else None
    return value


def compare(actual: Any, expected: Any, operator: str, context: dict[str, Any]) -> bool:
    expected = resolve(expected, context)
    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if operator == "in":
        return actual in expected
    if operator == "not_in":
        return actual not in expected
    if operator == "gt":
        return actual is not None and actual > expected
    if operator == "gte":
        return actual is not None and actual >= expected
    if operator == "lt":
        return actual is not None and actual < expected
    if operator == "lte":
        return actual is not None and actual <= expected
    if operator == "contains":
        return expected in actual if actual is not None else False
    return False


def evaluate_condition(condition: Any, context: dict[str, Any]) -> bool:
    """Evaluate the small declarative condition language used by Rule Spec v1."""
    if condition in (None, [], {}):
        return True

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
            if "not_in" in expected:
                if not found or actual in [resolve(v, context) for v in expected["not_in"]]:
                    return False
            elif "in" in expected:
                if not found or actual not in [resolve(v, context) for v in expected["in"]]:
                    return False
            else:
                for operator, value in expected.items():
                    op = operator
                    if op == "equals":
                        op = "eq"
                    if op == "not_equals":
                        op = "ne"
                    if not found or not compare(actual, value, op, context):
                        return False
        else:
            if not found or actual != resolve(expected, context):
                return False
    return True


def evidence_available(requirement: str, context: dict[str, Any]) -> bool:
    """Check whether a declared evidence item is present and non-null.

    Evidence names are intentionally semantic. A caller can satisfy them with
    either an exact context key or a nested `evidence` key.
    """
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
    if not exclusions:
        return False
    return any(evaluate_condition(item, context) for item in exclusions)


def load_rules(rule_dir: Path) -> list[dict[str, Any]]:
    rules = []
    for path in sorted(rule_dir.rglob("*.yaml")):
        with path.open("r", encoding="utf-8") as handle:
            rule = yaml.safe_load(handle) or {}
        rule["_source"] = str(path)
        rules.append(rule)
    return rules


def evaluate_rule(rule: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    required = rule.get("evidence_required", [])
    missing = [item for item in required if not evidence_available(item, context)]
    if missing:
        return {
            "rule_id": rule.get("id"),
            "status": "insufficient_evidence",
            "missing_evidence": missing,
            "source": rule.get("_source"),
        }

    if evaluate_exclusions(rule.get("exclude_when"), context):
        return {"rule_id": rule.get("id"), "status": "excluded", "source": rule.get("_source")}

    matched = evaluate_condition(rule.get("when"), context)
    if not matched:
        return {"rule_id": rule.get("id"), "status": "not_matched", "source": rule.get("_source")}

    action_type = (rule.get("action") or {}).get("type", "recommend")
    declared_approval = bool(rule.get("human_approval_required", False))
    approval_required = declared_approval or action_type in MUTATING_ACTIONS

    return {
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


def run(rule_dir: Path, context: dict[str, Any]) -> dict[str, Any]:
    results = [evaluate_rule(rule, context) for rule in load_rules(rule_dir)]
    return {
        "engine_version": "1.0.0",
        "matched": [r for r in results if r["status"] == "matched"],
        "insufficient_evidence": [r for r in results if r["status"] == "insufficient_evidence"],
        "excluded": [r for r in results if r["status"] == "excluded"],
        "not_matched": [r for r in results if r["status"] == "not_matched"],
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
