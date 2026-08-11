# Google Ads Performance Skills

Model-agnostic Google Ads performance marketing skills for Gemini and AI agents — strategy, auditing, optimization, measurement, and data-driven decision making.

## Architecture

- `skills/` — executable workflows
- `knowledge/` — domain principles and frameworks
- `rules/` — evidence-based decision rules
- `templates/` — output contracts
- `docs/` — specifications and architecture
- `integrations/` — platform/API integrations
- `scripts/` — validation tooling

## Core design principles

1. Evidence before conclusions.
2. Observation, inference, recommendation, and confidence stay distinct.
3. Knowledge, workflow, and decision rules are separate assets.
4. Human approval is required for account-changing actions by default.
5. The system is model-agnostic and avoids vendor-specific agent assumptions.
6. Business outcomes outrank surface metrics when evidence is available.
7. Current Google first-party documentation outranks repository lineage or generic best practice for platform behavior.

## Phase 3B

The repository now contains the V1 Knowledge and Rule population for the 18 Core Skills:

- 11 canonical Knowledge assets
- 21 evidence-gated Rules
- Skill-to-Knowledge-to-Rule mappings in `docs/SKILL_REGISTRY.md`

The next layer is validation: schema checks, rule fixtures, Skill examples, and end-to-end diagnostic tests before adding live Google Ads API execution.
