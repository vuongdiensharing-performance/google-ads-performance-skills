# Phase 2C — Read-only GA4 MCP Adapter

## Purpose

The adapter is the only repository-owned runtime boundary between the upstream `google-analytics-mcp` server and the GA4 Evidence Contract.

It is intentionally **read-only** and must not:

- create or modify Google Analytics configuration;
- invoke tools outside the provider allowlist;
- generate Rule decisions;
- generate Boundary A–F states;
- infer or invent evidence.

## Runtime flow

```text
Google Analytics MCP (stdio)
        ↓
StdioMCPClient
        ↓
GoogleAnalyticsMCPAdapter
        ↓
GA4 Evidence Contract v1.1.0
        ↓
Rule Engine (future phase)
```

## Upstream pin

The adapter targets the provider declaration in `providers/google_analytics.yaml`:

- package: `analytics-mcp`
- version: `0.7.0`
- pinned commit: `a8ca729d4a8fa99bffe87962c17c0539c6aa9da7`

The adapter does not install or update the upstream package itself. The deployment environment is responsible for supplying the pinned server command, for example the upstream-supported `pipx run analytics-mcp` invocation.

## Tool boundary

Only these upstream tools are callable:

- `get_account_summaries` → `GA4_IDENTITY`
- `get_property_details` → `GA4_IDENTITY`
- `list_google_ads_links` → `GA4_LINKAGE`
- `run_report` → `GA4_REPORT`
- `run_funnel_report` → `GA4_FUNNEL`
- `get_custom_dimensions_and_metrics` → `GA4_METADATA`
- `run_realtime_report` → `GA4_REALTIME`

Unknown or write-capable tool names are rejected before reaching MCP.

## Evidence guarantees

Every successful adapter response contains:

- `source_verified: true`
- `inference_used: false`
- pinned provider version and commit
- canonical SHA-256 request fingerprint
- UTC retrieval timestamp
- evidence type derived from the provider allowlist, not from LLM output

The fingerprint is computed from the canonical JSON object:

```json
{
  "tool": "<source.tool>",
  "request": { }
}
```

using sorted keys and compact separators, matching `scripts/validate_ga4_evidence_contract.py`.

## Authentication

No credentials are stored in this repository. The upstream MCP process receives Google ADC/environment configuration from the runtime environment. Live credentials are deliberately excluded from CI; Phase 2C tests use a fake MCP client.

## Scope boundary

Phase 2C does **not** implement query semantics, metric/dimension policy, identity verification, Google Ads ↔ GA4 linkage resolution, or Rule Engine integration. Those belong to subsequent phases.
