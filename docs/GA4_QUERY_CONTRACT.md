# Phase 2D — GA4 Query Contract

## Purpose

The Query Contract is the policy boundary between an Agent's analytics intent and the read-only GA4 MCP adapter. It prevents arbitrary `run_report` requests from entering the external provider.

## Execution rule

```text
Agent intent
    ↓
registered query_id
    ↓
JSON Schema validation
    ↓
query-local semantic validation
    ↓
canonical provider request construction
    ↓
SHA-256 request fingerprint
    ↓
read-only GA4 MCP adapter
    ↓
GA4 Evidence Contract
```

There is no supported path from an LLM directly to raw `run_report` arguments.

## Query ownership

- `schemas/ga4-query-contract.json` — canonical input schema for Agent-supplied query intent.
- `queries/google_analytics/registry.yaml` — machine-readable query index and execution policy.
- `queries/google_analytics/*.yaml` — source of truth for each registered query's dimensions, metrics, filters, and output evidence type.
- `scripts/validate_ga4_query.py` — schema + semantic validation, provider-request compilation, and canonical fingerprint construction.
- `evals/ga4/` — positive and negative fixtures.
- `scripts/run_ga4_live_smoke.py` — local-only live integration test; it is never an Agent tool and never runs in CI.

## GA4-CV-001

The first query is deliberately narrow and supports conversion-tracking evidence only.

```yaml
query_id: GA4-CV-001
tool: run_report
allowed_dimensions:
  - sessionCampaignName
required_metrics:
  - sessions
  - conversions
allowed_filters:
  - sessionCampaignName
  - sessionSource
  - sessionMedium
```

The Agent supplies only the registered query ID, authorized property, date range, and allowlisted filter values. Dimensions and metrics are resolved from the catalog rather than accepted from the Agent.

## Canonical request

After validation, the query compiler produces the **exact request object sent to the upstream MCP `run_report` tool**. This is also the request object recorded in GA4 Evidence Contract provenance.

Example without filters:

```json
{
  "tool": "run_report",
  "request": {
    "property_id": "properties/123456789",
    "date_ranges": [
      {"start_date": "2026-08-01", "end_date": "2026-08-10"}
    ],
    "dimensions": ["sessionCampaignName"],
    "metrics": ["sessions", "conversions"]
  }
}
```

A filter is deterministically compiled to the provider's `dimension_filter` shape. Multiple allowlisted filters are combined with an `and_group` in sorted key order.

## Determinism

The canonical request above is the **single object** fingerprinted by SHA-256:

```text
sha256(canonical JSON of {"tool": ..., "request": ...})
```

Keys are sorted and JSON is encoded with compact separators. The adapter uses the same canonicalization function, so the Query Contract fingerprint and Evidence Contract fingerprint must match exactly.

This removes the previous ambiguity where the Query Contract fingerprint could represent one request shape while the adapter fingerprinted another.

## Rejection behavior

The query validator rejects:

- unknown `query_id` values;
- arbitrary dimensions or metrics supplied outside the schema/catalog;
- unknown filter names;
- invalid property identifiers;
- missing required date ranges;
- inverted date ranges;
- query definitions that do not resolve to the read-only `run_report` tool;
- query definitions that do not produce `GA4_REPORT` evidence.

## Live integration smoke test

The repository does not store credentials and CI does not call a live GA4 property. Run the smoke test locally after configuring ADC:

```bash
export GOOGLE_PROJECT_ID="smart-road-434602-a0"
export GA4_PROPERTY_ID="YOUR_NUMERIC_GA4_PROPERTY_ID"
python scripts/run_ga4_live_smoke.py
```

The script pins the upstream provider to commit `a8ca729d4a8fa99bffe87962c17c0539c6aa9da7` / package `0.7.0`, validates `GA4-CV-001`, invokes the provider through stdio, validates the returned Evidence Contract, and fails if the Query/Evidence fingerprints differ.

For the complete local authentication setup, follow the upstream Google Analytics MCP instructions: configure Application Default Credentials with the `https://www.googleapis.com/auth/analytics.readonly` scope and provide the Google Cloud project ID to the MCP process.

## Scope boundary

Phase 2D does not authenticate against Google, verify account/property ownership, or connect GA4 evidence to a Rule. Those are later runtime/integration concerns. The Query Contract only determines **what the adapter is permitted to ask**.
