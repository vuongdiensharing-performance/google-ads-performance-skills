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

## Phase 3

This release establishes the canonical specifications, Skill Registry, and 18 Core Skills. Platform integrations and advanced intelligence layers follow after the core contracts are stable.
