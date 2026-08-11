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
canonical request construction
    ↓
SHA-256 request fingerprint
    ↓
read-only GA4 MCP adapter
```

There is no supported path from an LLM directly to raw `run_report` arguments.

## Query ownership

- `schemas/ga4-query-contract.json` — canonical request schema.
- `queries/google_analytics/registry.yaml` — machine-readable query index and execution policy.
- `queries/google_analytics/*.yaml` — source of truth for each registered query's dimensions, metrics, filters, and output evidence type.
- `scripts/validate_ga4_query.py` — schema + semantic validation and canonical request/fingerprint construction.
- `evals/ga4/` — positive and negative fixtures.

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

## Determinism

The adapter receives a canonical request whose fingerprint is calculated from:

```json
{
  "tool": "run_report",
  "request": {
    "property_id": "...",
    "date_range": {"start_date": "...", "end_date": "..."},
    "dimensions": ["..."],
    "metrics": ["..."],
    "filters": {}
  }
}
```

Keys are sorted and JSON is encoded with compact separators before SHA-256 hashing. The same logical contract request must therefore produce the same fingerprint.

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

## Scope boundary

Phase 2D does not authenticate against Google, verify account/property ownership, or connect GA4 evidence to a Rule. Those are later runtime/integration concerns. The Query Contract only determines **what the adapter is permitted to ask**.
