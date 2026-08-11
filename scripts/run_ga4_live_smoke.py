#!/usr/bin/env python3
"""Run a credentialed, read-only GA4-CV-001 smoke test.

This is intentionally a manual/runtime verification tool. It is not invoked by
CI and it never writes to Google Analytics. Credentials are read from the local
environment, not stored in the repository.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from integrations.google_analytics.adapter import GoogleAnalyticsMCPAdapter
from integrations.google_analytics.client import StdioMCPClient
from scripts.validate_ga4_evidence_contract import load_json as load_evidence_schema
from scripts.validate_ga4_evidence_contract import load_yaml as load_evidence_yaml
from scripts.validate_ga4_evidence_contract import validate as validate_evidence
from scripts.validate_ga4_query import (
    REGISTRY_PATH,
    SCHEMA_PATH,
    load_json,
    load_mapping,
    validate,
)

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_PATH = ROOT / "providers/google_analytics.yaml"
QUERY_FIXTURE = ROOT / "evals/ga4/ga4_query_contract.yaml"


def load_provider() -> dict[str, Any]:
    value = yaml.safe_load(PROVIDER_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("provider policy must be a mapping")
    return value


def build_mcp_command(provider: dict[str, Any]) -> list[str]:
    upstream = provider["upstream"]
    repository = upstream["repository"]
    commit = upstream["pinned_commit"]
    package = upstream["package"]
    return [
        "pipx",
        "run",
        "--no-cache",
        "--spec",
        f"git+{repository}@{commit}",
        package,
    ]


def validate_query(property_id: str, start_date: str, end_date: str) -> dict[str, Any]:
    contract = load_mapping(QUERY_FIXTURE)
    contract["property_id"] = property_id
    contract["date_range"] = {"start_date": start_date, "end_date": end_date}
    schema = load_json(SCHEMA_PATH)
    registry = load_mapping(REGISTRY_PATH)
    errors, canonical = validate(contract, schema, registry)
    if errors or canonical is None:
        raise RuntimeError("GA4-CV-001 validation failed: " + "; ".join(errors))
    return canonical


def validate_live_evidence(envelope: dict[str, Any], schema: dict[str, Any], provider: dict[str, Any]) -> None:
    errors = validate_evidence(envelope, schema, provider)
    if errors:
        raise RuntimeError("live evidence failed the canonical contract: " + "; ".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the GA4-CV-001 live read-only smoke test.")
    parser.add_argument("--property-id", required=True, help="GA4 property resource, e.g. properties/123456789")
    parser.add_argument("--start-date", required=True, help="ISO date, e.g. 2026-08-01")
    parser.add_argument("--end-date", required=True, help="ISO date, e.g. 2026-08-10")
    parser.add_argument("--output", type=Path, help="Optional local path for the full evidence envelope; never commit this file")
    args = parser.parse_args()

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("FAIL: GOOGLE_APPLICATION_CREDENTIALS is not set", file=sys.stderr)
        return 2
    if not os.environ.get("GOOGLE_PROJECT_ID"):
        print("FAIL: GOOGLE_PROJECT_ID is not set", file=sys.stderr)
        return 2

    try:
        provider = load_provider()
        canonical = validate_query(args.property_id, args.start_date, args.end_date)
        schema = load_evidence_schema(ROOT / "schemas/ga4-evidence-contract.json")

        command = build_mcp_command(provider)
        print(f"provider_version={provider['upstream']['package_version']}")
        print(f"provider_commit={provider['upstream']['pinned_commit']}")
        print(f"query_id={canonical['query_id']}")
        print(f"request_fingerprint={canonical['request_fingerprint']}")
        print("inference_used=false")
        print("mode=read_only")
        print(f"mcp_command={' '.join(command)}")

        with StdioMCPClient(command) as client:
            adapter = GoogleAnalyticsMCPAdapter(
                client,
                provider_version=provider["upstream"]["package_version"],
                provider_commit=provider["upstream"]["pinned_commit"],
            )

            identity = adapter.get_property_details(args.property_id)
            validate_live_evidence(identity, schema, provider)
            print("identity_evidence=PASS")

            report = adapter.run_report(args.property_id, canonical["request"])
            validate_live_evidence(report, schema, provider)
            print("report_evidence=PASS")
            print(f"evidence_request_fingerprint={report['provenance']['request_fingerprint']}")

            if report["provenance"]["request_fingerprint"] != canonical["request_fingerprint"]:
                raise RuntimeError("query and evidence fingerprints do not match")

            if args.output:
                output = args.output.resolve()
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"evidence_output={output}")

        print("LIVE GA4 READ-ONLY SMOKE: PASS")
        return 0
    except (subprocess.SubprocessError, OSError, ValueError, RuntimeError) as exc:
        print(f"LIVE GA4 READ-ONLY SMOKE: FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
