#!/usr/bin/env python3
"""Validate the read-only Google Analytics Evidence Contract fixture."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COMMIT = "a8ca729d4a8fa99bffe87962c17c0539c6aa9da7"
ALLOWED_TOOLS = {
    "get_account_summaries",
    "get_property_details",
    "list_google_ads_links",
    "run_report",
    "run_funnel_report",
    "get_custom_dimensions_and_metrics",
    "run_realtime_report",
}
PROPERTY_RE = re.compile(r"^properties/[0-9]+$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("contract root must be a mapping")
    return value


def require_mapping(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be a mapping")
        return {}
    return value


def validate(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if contract.get("contract_version") != "1.0.0":
        errors.append("contract_version must be 1.0.0")
    if contract.get("evidence_type") != "GA4_REPORT":
        errors.append("evidence_type must be GA4_REPORT")

    source = require_mapping(contract, "source", errors)
    request = require_mapping(contract, "request", errors)
    result = require_mapping(contract, "result", errors)
    provenance = require_mapping(contract, "provenance", errors)

    if source.get("provider") != "google_analytics":
        errors.append("source.provider must be google_analytics")
    if source.get("transport") != "mcp":
        errors.append("source.transport must be mcp")
    if source.get("tool") not in ALLOWED_TOOLS:
        errors.append("source.tool is not in the allowed read-only tool set")
    if not PROPERTY_RE.fullmatch(str(source.get("property_id", ""))):
        errors.append("source.property_id must match properties/<numeric_id>")

    if request.get("property_id") != source.get("property_id"):
        errors.append("request.property_id must match source.property_id")

    date_range = require_mapping(request, "date_range", errors)
    for key in ("start_date", "end_date"):
        value = date_range.get(key)
        try:
            datetime.strptime(str(value), "%Y-%m-%d")
        except (TypeError, ValueError):
            errors.append(f"request.date_range.{key} must be YYYY-MM-DD")

    if not isinstance(result.get("rows"), list):
        errors.append("result.rows must be a list")

    if provenance.get("source_verified") is not True:
        errors.append("provenance.source_verified must be true")
    if provenance.get("inference_used") is not False:
        errors.append("provenance.inference_used must be false")
    if provenance.get("provider_commit") != EXPECTED_COMMIT:
        errors.append("provenance.provider_commit does not match pinned upstream baseline")
    if not SHA256_RE.fullmatch(str(provenance.get("request_fingerprint", ""))):
        errors.append("provenance.request_fingerprint must be sha256:<64 lowercase hex chars>")

    try:
        datetime.fromisoformat(str(provenance.get("retrieved_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("provenance.retrieved_at must be an ISO-8601 datetime")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the GA4 Evidence Contract.")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=ROOT / "evals/ga4/ga4_evidence_contract.yaml",
    )
    args = parser.parse_args()

    try:
        contract = load(args.fixture.resolve())
    except Exception as exc:
        print(f"FAIL GA4 evidence contract: {exc}")
        return 1

    errors = validate(contract)
    if errors:
        print("FAIL GA4 evidence contract")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK   {args.fixture.resolve().relative_to(ROOT)}")
    print("     read-only provider contract validated")
    print("     inference_used=false")
    print("     source_verified=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
