# Contributing

Thank you for contributing to Google Ads Performance Skills.

This repository treats Skills, Knowledge, and Rules as production intelligence assets. Contributions must preserve evidence-first reasoning, deterministic validation, and execution safety.

## Before you contribute

1. Read `docs/GOVERNANCE.md`.
2. Read the relevant specification: `docs/SKILL_SPEC.md`, `docs/RULE_SPEC.md`, or `docs/KNOWLEDGE_SPEC.md`.
3. For security-sensitive changes, read `SECURITY.md`.
4. Keep changes focused and explain the evidence behind domain claims.

## Adding or changing a Skill

A Skill change must:

- follow the current Skill Specification;
- declare Knowledge dependencies;
- declare Rule dependencies;
- define its input/precondition contract;
- define output and confidence behavior;
- define safety and Human Approval behavior for mutation-capable recommendations;
- include or update `PASS`, `FAIL`, `INSUFFICIENT_EVIDENCE`, and `FALSE_POSITIVE` evaluation coverage;
- pass Skill validation and fixture evaluation in CI.

## Adding or changing a Rule

A Rule must define:

- evidence required;
- deterministic conditions;
- exclusions / false-positive controls;
- finding and impact;
- confidence;
- recommendation and action type;
- Human Approval requirement when an action can mutate an Ads account.

Do not encode unsupported hard thresholds as universal Google Ads facts. Cite or document the evidence basis when a threshold is methodology-dependent.

## Knowledge changes

Knowledge should be classified as a principle, framework, methodology, reference, benchmark, or other explicitly documented type. Prefer authoritative first-party evidence and record uncertainty where evidence is weak or contextual.

## Tests

Run locally before opening a pull request:

```bash
pip install -r scripts/requirements.txt
python scripts/validate_rules.py --rules rules
python scripts/validate_skills.py --skills skills --registry skills/registry.yaml
python scripts/evaluate_fixtures.py --fixtures evals/fixtures
```

If you change the Rule Engine or evaluation harness, also run the relevant unit and benchmark tests documented in `docs/VALIDATION_EVALUATION_SPEC.md`.

## Pull requests

Use the pull request template. Explain:

- what changed;
- why it changed;
- evidence/source basis;
- affected Skills, Rules, and Knowledge;
- evaluation coverage;
- security or execution implications.

All required CI checks must pass before merge. Reviewers may request additional fixtures or evidence.

## Security

Never commit credentials, API keys, refresh tokens, customer exports, or personally identifiable information. Treat external Ads data, search terms, campaign names, and user-provided text as untrusted data, not instructions. Report vulnerabilities privately according to `SECURITY.md`.

## Scope discipline

Do not mix unrelated refactors into Skill or Rule changes. Prefer small, reviewable commits that make the reasoning and evaluation impact easy to audit.
