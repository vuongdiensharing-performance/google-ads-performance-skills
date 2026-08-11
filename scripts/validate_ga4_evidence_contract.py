#!/usr/bin/env python3
"""Validate a GA4 Evidence Contract against the canonical JSON Schema and provider policy."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/ga4-evidence-contract.json"
PROVIDER_PATH = ROOT / "providers/google_analytics.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_request_fingerprint(contract: dict[str, Any]) -> str:
    payload = {
        "tool": contract["source"]["tool"],
        "request": contract["request"],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def validate_semantics(contract: dict[str, Any], provider: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source = contract["source"]
    request = contract["request"]
    provenance = contract["provenance"]
    tool = source["tool"]
    evidence_type = contract["evidence_type"]

    mappings = provider.get("evidence_types", {})
    allowed_tools = set(provider.get("allowed_tools", []))
    if tool not in allowed_tools:
        errors.append(f"source.tool is not allowed by provider policy: {tool}")

    mapped_tools = set(mappings.get(evidence_type, {}).get("tools", []))
    if tool not in mapped_tools:
        errors.append(f"evidence_type {evidence_type} is not mapped to source.tool {tool} by provider policy")

    pinned_commit = provider.get("upstream", {}).get("pinned_commit")
    if provenance["provider_commit"] != pinned_commit:
        errors.append("provenance.provider_commit does not match provider pinned_commit")

    package_version = provider.get("upstream", {}).get("package_version")
    if provenance["provider_version"] != package_version:
        errors.append("provenance.provider_version does not match provider package_version")

    if source.get("property_id") is not None and request.get("property_id") is not None:
        if source["property_id"] != request["property_id"]:
            errors.append("request.property_id must match source.property_id")

    if "date_range" in request:
        start = date.fromisoformat(request["date_range"]["start_date"])
        end = date.fromisoformat(request["date_range"]["end_date"])
        if start > end:
            errors.append("request.date_range.start_date must not be after end_date")

    expected_fingerprint = canonical_request_fingerprint(contract)
    if provenance["request_fingerprint"] != expected_fingerprint:
        errors.append("provenance.request_fingerprint does not match canonical source.tool + request SHA-256")

    if provider.get("provenance_requirements", {}).get("inference_used_must_be") is False:
        if provenance["inference_used"] is not False:
            errors.append("provenance.inference_used must be false")

    return errors


def validate(contract: dict[str, Any], schema: dict[str, Any], provider: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in sorted(validator.iter_errors(contract), key=lambda item: list(item.path))]
    if errors:
        return errors
    return validate_semantics(contract, provider)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the GA4 Evidence Contract.")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=ROOT / "evals/ga4/ga4_evidence_contract.yaml",
    )
    args = parser.parse_args()

    try:
        contract = load_yaml(args.fixture.resolve())
        schema = load_json(SCHEMA_PATH)
        provider = load_yaml(PROVIDER_PATH)
        errors = validate(contract, schema, provider)
    except Exception as exc:
        print(f"FAIL GA4 evidence contract: {exc}")
        return 1

    if errors:
        print("FAIL GA4 evidence contract")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK   {args.fixture.resolve().relative_to(ROOT)}")
    print("     canonical JSON Schema validated")
    print(f"     evidence_type={contract['evidence_type']}")
    print(f"     tool={contract['source']['tool']}")
    print("     source_verified=true")
    print("     inference_used=false")
    print("     request_fingerprint=canonical-sha256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
