# Google Ads Performance Skills

Model-agnostic Google Ads performance marketing skills for Gemini and AI agents — strategy, auditing, optimization, measurement, and data-driven decision making.

## Architecture

- `skills/` — executable workflows
- `knowledge/` — domain principles and frameworks
- `rules/` — evidence-based decision rules
- `templates/` — output contracts
- `evals/` — deterministic fixtures and golden benchmarks
- `docs/` — specifications, architecture, governance, and evaluation
- `integrations/` — platform/API integrations
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

## Validation

The repository uses deterministic fixtures and an end-to-end `account-audit` golden benchmark before model or live API integration. See `docs/VALIDATION_EVALUATION_SPEC.md`.

## Governance & security

- `CONTRIBUTING.md` — contribution and change-control requirements
- `SECURITY.md` — threat model, vulnerability reporting, prompt-injection, credential, and execution-safety policy
- `CODE_OF_CONDUCT.md` — community standards
- `docs/GOVERNANCE.md` — source-of-truth hierarchy and intelligence governance

CI validates Rules, Skills, fixtures, Python dependencies, and static security checks. CodeQL is also configured for Python analysis.

## Status

The repository is currently in the validation and governance hardening stage. Live Google Ads API execution is intentionally not enabled until the evaluation and security baseline is established.
