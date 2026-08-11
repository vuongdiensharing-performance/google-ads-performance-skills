# GA4 MCP Integration Contract

## Status

Phase 2A/2B — provider audit and evidence boundary.

This document defines how the repository may consume Google Analytics MCP evidence without changing the frozen Gate 2C Boundary Contract.

## 1. Governance rule

Google Analytics MCP is an **external, read-only evidence provider**.

It MUST NOT:

- generate a Rule decision;
- generate or choose a Boundary State A–F;
- infer missing evidence;
- override Rule-local semantics;
- override `schemas/boundary-contract.json`;
- become a dependency of Skills.

The data flow is:

```text
Google Analytics MCP
        |
        v
Provider Adapter
        |
        v
GA4 Evidence Contract
        |
        v
Evidence Layer
        |
        v
Rule Engine
        |
        v
Boundary State A-F
```

The LLM may request an evidence query, but the returned data remains untrusted external input until it satisfies the Evidence Contract.

## 2. Upstream source

The upstream implementation is the official Google Analytics MCP repository:

- repository: `https://github.com/googleanalytics/google-analytics-mcp.git`
- current integration baseline: commit `a8ca729d4a8fa99bffe87962c17c0539c6aa9da7`
- package: `analytics-mcp`
- package version at the pinned baseline: `0.7.0`
- license: Apache-2.0
- maturity: Beta / Experimental

The upstream README states that the server uses the Google Analytics Admin API and Google Analytics Data API and exposes account/property discovery, Google Ads linkage, core reporting, funnel reporting, metadata, and realtime reporting tools. See the upstream README for the authoritative tool list.

## 3. Phase 2 scope

### Phase 2A — External MCP audit

Completed at the repository-contract level:

- upstream repository identified;
- upstream commit pinned;
- package/version recorded;
- read-only mode declared;
- allowed tool surface recorded;
- trust boundary declared.

### Phase 2B — Identity contract

The first runtime integration MUST establish the GA4 identity before querying performance evidence:

```text
get_account_summaries
        |
        v
GA4 account/property
        |
        v
get_property_details
        |
        v
list_google_ads_links
```

A report query MUST NOT be treated as canonical evidence until the property identity is known and the returned property ID matches the requested property.

### Phase 2C — Evidence contract

All accepted GA4 report evidence MUST conform to:

`schemas/ga4-evidence-contract.json`

The contract requires:

- provider identity;
- MCP transport identity;
- tool identity;
- GA4 property identity;
- query inputs;
- returned rows;
- retrieval timestamp;
- source verification;
- `inference_used: false`.

### Phase 2D — Google Ads linkage

`list_google_ads_links` is an identity/linkage evidence source. Its result may establish that a GA4 property has a Google Ads link, but it does not itself prove campaign-level conversion correctness, attribution correctness, or performance quality.

Those conclusions remain Rule semantics.

### Phase 2E — first Rule pilot

The first Rule integration target is `CV-TRACK-001`.

No other Rule should consume GA4 evidence until the pilot proves that:

1. evidence can be retrieved deterministically;
2. provenance is preserved;
3. source failures become explicit insufficient evidence rather than inferred values;
4. cross-source disagreement can enter `CONFLICTING_EVIDENCE` through existing Gate 2C policy;
5. `inference_used` remains `false`.

## 4. Query safety boundary

The repository MUST NOT allow an unconstrained LLM-generated GA4 query to become canonical evidence.

Before execution, a future GA4 Query Contract should validate at minimum:

- property ID;
- date range;
- dimensions;
- metrics;
- filters;
- allowed tool;
- source identity.

This is deliberately a future contract. Phase 2A/2B does not yet define GA4 business metrics or Rule semantics.

## 5. Failure semantics

Provider failures MUST NOT be converted into fabricated values.

Examples:

```text
GA4 unavailable
    -> evidence unavailable
    -> Rule may become APPLICABLE_MISSING_EVIDENCE
```

```text
Google Ads says conversions=127
GA4 evidence says conversions=0
    -> preserve both sources
    -> Rule policy decides whether this is CONFLICTING_EVIDENCE
```

The Evidence Layer must never silently choose the more convenient source.

## 6. Separation from Gate 2C

Gate 2C is frozen.

This integration does not modify:

- A–F state definitions;
- resolution precedence;
- canonical decisions;
- finding generation semantics;
- Rule-local boundary contracts;
- Skill dependency declarations.

GA4 is an evidence provider below the Rule Engine, not a new governance layer above it.

## 7. Next implementation step

Implement a **read-only GA4 adapter** that can validate and wrap MCP responses into the Evidence Contract without requiring live customer data in CI.

CI should first use synthetic fixtures. Live GA4 access belongs in a separate integration environment and must never be required for the core Rule/Skill validation pipeline.
