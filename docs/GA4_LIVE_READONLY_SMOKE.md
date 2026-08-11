# GA4 Live Read-only Smoke Test

This is the runtime checkpoint after Phase 2D. It verifies the full path:

```text
GA4-CV-001
    ↓
Query Contract validation
    ↓
canonical upstream MCP request
    ↓
pinned google-analytics-mcp
    ↓
GA4_IDENTITY evidence
    ↓
GA4_REPORT evidence
    ↓
Evidence Contract validation
```

## Prerequisites

The upstream Google Analytics MCP server is experimental and requires local Google credentials. The official setup uses Application Default Credentials with the Analytics read-only scope and recommends setting `GOOGLE_PROJECT_ID`.

See the official Google Analytics MCP README: https://github.com/googleanalytics/google-analytics-mcp/blob/main/README.md

Required local environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/adc-credentials.json"
export GOOGLE_PROJECT_ID="your-google-cloud-project-id"
```

The smoke test itself does not store credentials or commit returned analytics data.

## Run

Use an authorized GA4 property and explicit dates:

```bash
python scripts/run_ga4_live_smoke.py \
  --property-id properties/123456789 \
  --start-date 2026-08-01 \
  --end-date 2026-08-10
```

The script installs/runs the **pinned provider commit** from `providers/google_analytics.yaml` with `pipx --no-cache`; it does not silently use the latest upstream version.

## Required assertions

A successful smoke test must prove all of the following:

- `GA4-CV-001` resolves through the registry.
- The canonical request uses the exact snake_case `run_report` shape accepted by the pinned provider.
- `GA4_IDENTITY` evidence validates against the canonical Evidence Contract.
- `GA4_REPORT` evidence validates against the canonical Evidence Contract.
- Provider version and commit match repository policy.
- `inference_used=false`.
- Query fingerprint equals evidence fingerprint.
- No Rule decision or Boundary A–F state is produced.

## Important boundary

This smoke test is **manual and read-only**. It is intentionally not part of normal CI because credentials and live GA4 property access must not be placed in GitHub Actions for this repository phase.

A failed live call is not a Rule failure. It is an integration/evidence acquisition failure and must be resolved before the evidence can be admitted to a Rule.

## Known upstream runtime caveat

The upstream project has had historical reports of MCP tool-call timeouts in some clients. A live failure should therefore be classified as transport/auth/provider failure rather than interpreted as GA4 evidence.

See the upstream timeout report: https://github.com/googleanalytics/google-analytics-mcp/issues/150
