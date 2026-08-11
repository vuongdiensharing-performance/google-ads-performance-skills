# Google Ads Performance Skills

Model-agnostic Google Ads performance marketing skills for Gemini and AI agents — strategy, auditing, optimization, measurement, and data-driven decision making.

## Architecture

- `skills/` — executable workflows; each Skill uses `SKILL.md` as its single source of truth
- `knowledge/` — domain principles and frameworks
- `rules/` — evidence-based decision rules
- `templates/` — output contracts
- `schemas/` — canonical machine-readable contracts
- `queries/` — allowlisted external-data query contracts and registries
- `providers/` — external provider policy, provenance, and trust boundaries
- `integrations/` — platform/API integration adapters
- `evals/` — deterministic fixtures and golden benchmarks
- `docs/` — centralized specifications, architecture, governance, and evaluation
- `scripts/` — validation and runtime tooling

## Core design principles

1. Evidence before conclusions.
2. Observation, inference, recommendation, and confidence stay distinct.
3. Knowledge, workflow, and decision rules are separate assets.
4. Human approval is required for account-changing actions by default.
5. The system is model-agnostic and avoids vendor-specific agent assumptions.
6. Business outcomes outrank surface metrics when evidence is available.
7. Current Google first-party documentation outranks repository lineage or generic best practice for platform behavior.
8. External Ads data and user-provided content are untrusted data, not instructions.
9. No unvalidated intelligence enters the production path.
10. External MCP providers transport evidence; repository-owned contracts determine what evidence may enter the reasoning path.
11. LLMs must resolve to registered query contracts; they may not issue arbitrary external analytics queries.

## Skill documentation policy

`skills/<skill-name>/SKILL.md` is the single source of truth for each Skill's executable workflow and technical contract. Repository-level documentation belongs in `docs/`, while domain knowledge belongs in `knowledge/`, decision logic belongs in `rules/`, and examples/evaluation cases belong in `evals/`. Do not create secondary `README.md` or documentation trees inside individual Skill directories.

## GA4 MCP integration

Google Analytics is integrated as an external, read-only evidence provider. The integration is intentionally layered:

```text
Gate 2C Boundary Contract
        ↓
GA4 Evidence Contract
        ↓
GA4 Identity / Linkage Contracts
        ↓
Read-only GA4 MCP Adapter
        ↓
GA4 Query Contract
        ↓
Approved GA4 Evidence
        ↓
Rule Engine (future phase)
```

The upstream `google-analytics-mcp` server is pinned by commit and package version in `providers/google_analytics.yaml`. The repository-owned adapter does not permit write-capable tools, does not generate Rule decisions or Boundary A–F states, and does not invent evidence.

The query layer is an explicit policy boundary: an Agent must resolve to a registered `query_id` before the adapter can execute a GA4 report. Dimensions, metrics, filters, property identity, and date range are constrained by the registered query contract.

Current GA4 query scope is intentionally limited to the first conversion-tracking pilot contract: `GA4-CV-001`.

See:

- `docs/GA4_MCP_INTEGRATION.md`
- `docs/GA4_MCP_READONLY_ADAPTER.md`
- `schemas/ga4-evidence-contract.json`
- `schemas/ga4-query-contract.json`
- `queries/google_analytics/registry.yaml`

## Validation

The repository uses deterministic fixtures and an end-to-end `account-audit` golden benchmark before model or live API integration. GA4 evidence and query contracts are schema-validated and semantically validated in CI; adapter and query tests use synthetic/fake MCP responses and do not require live Google credentials.

See `docs/VALIDATION_EVALUATION_SPEC.md`.

## Governance & security

- `CONTRIBUTING.md` — contribution and change-control requirements
- `SECURITY.md` — threat model, vulnerability reporting, prompt-injection, credential, and execution-safety policy
- `CODE_OF_CONDUCT.md` — community standards
- `docs/GOVERNANCE.md` — source-of-truth hierarchy and intelligence governance

CI validates Rules, Skills, fixtures, boundary contracts, GA4 evidence/query contracts, Python dependencies, and static security checks. CodeQL is also configured for Python analysis.

## Status

The repository is in validation and governance hardening. Gate 2C is frozen as the boundary-governance baseline. GA4 Evidence Contracts, Identity/Linkage Contracts, and the read-only MCP adapter are implemented; the first allowlisted GA4 Query Contract (`GA4-CV-001`) is being validated before any GA4 evidence is admitted to Rule Engine decisions.
