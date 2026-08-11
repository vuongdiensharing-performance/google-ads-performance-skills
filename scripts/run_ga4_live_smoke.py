#!/usr/bin/env python3
"""Run a local, read-only GA4 live smoke test through the pinned MCP provider.

This script is intentionally not an Agent/LLM tool. It validates the complete
Phase 2D -> 2C path using Application Default Credentials (ADC):

    Query Contract -> canonical request -> MCP stdio -> GA4 Evidence Contract

No credentials or GA4 data are written to the repository. The default provider
command is pinned to the provider commit declared in providers/google_analytics.yaml.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROVIDER_COMMIT = "a8ca729d4a8fa99bffe87962c17c0539c6aa9da7"
DEFAULT_PROVIDER_VERSION = "0.7.0"
DEFAULT_MCP_COMMAND = (
    "pipx run --spec "
    f"git+https://github.com/googleanalytics/google-analytics-mcp.git@{DEFAULT_PROVIDER_COMMIT} "
    "analytics-mcp"
)

sys.path.insert(0, str(ROOT))

from integrations.google_analytics.adapter import GoogleAnalyticsMCPAdapter  # noqa: E402
from integrations.google_analytics.client import StdioMCPClient  # noqa: E402
from scripts.validate_ga4_evidence_contract import (  # noqa: E402
    load_json,
    load_yaml,
    validate as validate_evidence,
)
from scripts.validate_ga4_query import (  # noqa: E402
    REGISTRY_PATH,
    SCHEMA_PATH,
    validate as validate_query,
)

SCHEMA_EVIDENCE_PATH = ROOT / "schemas/ga4-evidence-contract.json"
PROVIDER_PATH = ROOT / "providers/google_analytics.yaml"


def build_contract(property_id: str, start_date: str, end_date: str) -> dict[str, Any]:
    return {
        "query_id": "GA4-CV-001",
        "property_id": f"properties/{property_id}",
        "date_range": {"start_date": start_date, "end_date": end_date},
    }


def parse_args() -> argparse.Namespace:
    today = date.today()
    parser = argparse.ArgumentParser(description="Live GA4 read-only MCP smoke test")
    parser.add_argument("--property-id", default=os.getenv("GA4_PROPERTY_ID"))
    parser.add_argument(
        "--start-date",
        default=os.getenv("GA4_SMOKE_START_DATE", (today - timedelta(days=7)).isoformat()),
    )
    parser.add_argument(
        "--end-date",
        default=os.getenv("GA4_SMOKE_END_DATE", (today - timedelta(days=1)).isoformat()),
    )
    parser.add_argument(
        "--mcp-command",
        default=os.getenv("GA4_MCP_COMMAND", DEFAULT_MCP_COMMAND),
        help="Override the pinned MCP command for local debugging only.",
    )
    parser.add_argument(
        "--print-evidence",
        action="store_true",
        help="Print the complete evidence envelope, including returned report data.",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()

    if not args.property_id or not args.property_id.isdigit():
        return fail(
            "GA4 Property ID is required and must be numeric "
            "(use --property-id or GA4_PROPERTY_ID)."
        )

    if not os.getenv("GOOGLE_PROJECT_ID"):
        return fail("GOOGLE_PROJECT_ID is required for the pinned Google Analytics MCP runtime.")

    try:
        contract = build_contract(args.property_id, args.start_date, args.end_date)
        schema = load_json(SCHEMA_PATH)
        registry = load_yaml(REGISTRY_PATH)
        query_errors, canonical = validate_query(contract, schema, registry)
        if query_errors or canonical is None:
            return fail("Query Contract rejected:\n  - " + "\n  - ".join(query_errors))

        provider = load_yaml(PROVIDER_PATH)
        evidence_schema = load_json(SCHEMA_EVIDENCE_PATH)
        command = shlex.split(args.mcp_command)

        print("=" * 64)
        print("GA4 LIVE SMOKE TEST")
        print("=" * 64)
        print(f"query_id:            {canonical['query_id']}")
        print(f"property_id:         {contract['property_id']}")
        print(
            f"date_range:          {contract['date_range']['start_date']} -> "
            f"{contract['date_range']['end_date']}"
        )
        print(f"provider_version:    {DEFAULT_PROVIDER_VERSION}")
        print(f"provider_commit:     {DEFAULT_PROVIDER_COMMIT}")
        print(f"mcp_command:         {' '.join(command)}")
        print("authentication:       Application Default Credentials")
        print()

        with StdioMCPClient(command, timeout_seconds=120) as client:
            adapter = GoogleAnalyticsMCPAdapter(
                client,
                provider_version=DEFAULT_PROVIDER_VERSION,
                provider_commit=DEFAULT_PROVIDER_COMMIT,
            )
            evidence = adapter.run_report(contract["property_id"], canonical["request"])

        errors = validate_evidence(evidence, evidence_schema, provider)
        if errors:
            return fail("Evidence Contract rejected:\n  - " + "\n  - ".join(errors))

        expected_fingerprint = evidence["provenance"]["request_fingerprint"]
        if canonical["request_fingerprint"] != expected_fingerprint:
            return fail(
                "Query and evidence fingerprints differ. "
                "The canonical request must be the same object fingerprinted at the evidence boundary."
            )

        print("PASS: live GA4 report returned and passed Evidence Contract validation.")
        print(f"evidence_type:       {evidence['evidence_type']}")
        print(f"request_fingerprint: {expected_fingerprint}")
        print("source_verified:     true")
        print("inference_used:      false")
        if args.print_evidence:
            print(json.dumps(evidence, ensure_ascii=False, indent=2))
        return 0
    except subprocess.CalledProcessError as exc:
        return fail(f"MCP process failed with exit code {exc.returncode}.")
    except Exception as exc:
        return fail(f"Live smoke test error: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
