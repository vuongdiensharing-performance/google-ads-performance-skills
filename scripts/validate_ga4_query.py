#!/usr/bin/env python3
"""Validate and canonicalize a GA4 Query Contract against the registered catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/ga4-query-contract.json"
REGISTRY_PATH = ROOT / "queries/google_analytics/registry.yaml"


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def catalog_for_query(registry: dict[str, Any], query_id: str) -> dict[str, Any]:
    matches = [item for item in registry.get("queries", []) if item.get("id") == query_id]
    if len(matches) != 1:
        raise ValueError(f"query_id must resolve to exactly one registered query: {query_id}")
    path = ROOT / matches[0]["path"]
    catalog = load_mapping(path)
    if catalog.get("query_id") != query_id:
        raise ValueError(f"registry/local query ID mismatch: {query_id}")
    return catalog


def validate_schema(contract: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(contract), key=lambda item: list(item.path))]


def _dimension_filter(filters: dict[str, str]) -> dict[str, Any] | None:
    """Translate the repository filter shorthand to the pinned MCP shape."""
    if not filters:
        return None
    if len(filters) != 1:
        raise ValueError("GA4-CV-001 currently permits at most one dimension filter")
    field_name, value = next(iter(filters.items()))
    return {
        "filter": {
            "field_name": field_name,
            "string_filter": {
                "match_type": "EXACT",
                "value": value,
                "case_sensitive": False,
            },
        }
    }


def canonical_request(contract: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    """Build the exact snake_case request accepted by the pinned MCP server."""
    request: dict[str, Any] = {
        "property_id": contract["property_id"],
        "date_ranges": [
            {
                "start_date": contract["date_range"]["start_date"],
                "end_date": contract["date_range"]["end_date"],
            }
        ],
        "dimensions": catalog.get("allowed_dimensions", []),
        "metrics": catalog.get("required_metrics", []),
    }
    dimension_filter = _dimension_filter(contract.get("filters", {}))
    if dimension_filter is not None:
        request["dimension_filter"] = dimension_filter
    return {"tool": catalog["tool"], "request": request}


def fingerprint(canonical: dict[str, Any]) -> str:
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def validate_semantics(contract: dict[str, Any], catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if catalog.get("tool") != "run_report":
        errors.append("query catalog must use read-only run_report")
    if catalog.get("output", {}).get("evidence_type") != "GA4_REPORT":
        errors.append("query output must produce GA4_REPORT evidence")

    filters = contract.get("filters", {})
    allowed_filters = set(catalog.get("allowed_filters", []))
    unknown_filters = set(filters) - allowed_filters
    if unknown_filters:
        errors.append(f"filters are not allowlisted: {sorted(unknown_filters)}")

    start = date.fromisoformat(contract["date_range"]["start_date"])
    end = date.fromisoformat(contract["date_range"]["end_date"])
    if start > end:
        errors.append("date_range.start_date must not be after end_date")

    if catalog.get("constraints", {}).get("property_id_required") and not contract.get("property_id"):
        errors.append("property_id is required by query policy")
    if catalog.get("constraints", {}).get("date_range_required") and not contract.get("date_range"):
        errors.append("date_range is required by query policy")
    return errors


def validate(contract: dict[str, Any], schema: dict[str, Any], registry: dict[str, Any]) -> tuple[list[str], dict[str, Any] | None]:
    errors = validate_schema(contract, schema)
    if errors:
        return errors, None
    try:
        catalog = catalog_for_query(registry, contract["query_id"])
        errors.extend(validate_semantics(contract, catalog))
        if errors:
            return errors, None
        canonical = canonical_request(contract, catalog)
        return [], {**canonical, "query_id": contract["query_id"], "request_fingerprint": fingerprint(canonical)}
    except Exception as exc:
        return [str(exc)], None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GA4 Query Contract.")
    parser.add_argument("--fixture", type=Path, default=ROOT / "evals/ga4/ga4_query_contract.yaml")
    args = parser.parse_args()

    try:
        contract = load_mapping(args.fixture.resolve())
        schema = load_json(SCHEMA_PATH)
        registry = load_mapping(REGISTRY_PATH)
        errors, canonical = validate(contract, schema, registry)
    except Exception as exc:
        print(f"FAIL GA4 query contract: {exc}")
        return 1

    if errors:
        print("FAIL GA4 query contract")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK   {args.fixture.resolve().relative_to(ROOT)}")
    print(f"     query_id={canonical['query_id']}")
    print(f"     tool={canonical['tool']}")
    print(f"     request={json.dumps(canonical['request'], sort_keys=True)}")
    print(f"     request_fingerprint={canonical['request_fingerprint']}")
    print("     inference_used=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
