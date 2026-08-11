# Changelog

## 2026-08-11 — Gate 2B.1 Rule Knowledge Provenance Hardening

### Changed

- Added mandatory `knowledge_dependencies` to the canonical Rule schema in `docs/RULE_SPEC.md`.
- Added exact Rule → Knowledge declarations to all 21 active V1 Rules referenced by the Skill Registry.
- Added `rules/registry.yaml` as the machine-readable `rule-knowledge-provenance/v1` registry.
- Upgraded `skills/registry.yaml` to `2.1.0` and linked it to `rules/registry.yaml` via `rule_provenance_registry`.
- Extended `scripts/validate_skills.py` to validate Rule file ↔ Rule Registry ↔ Knowledge paths and Skill Rule dependencies ↔ Rule Registry membership.
- Added a hard no-inference policy for Rule → Knowledge resolution.

### Traceability contract

The intended provenance chain is now explicitly resolvable as:

```text
Finding
  ↓
Evidence
  ↓
Rule
  ↓
Knowledge
  ↓
Skill
```

Rule → Knowledge links are exact repository-relative paths and are no longer inferred from Rule category, filename, directory, or related Skill.

## 2026-08-11 — Phase 6 Gate 2 Preparation

### Changed

- Upgraded `skills/registry.yaml` to a machine-readable `skill-dependency-graph/v1` registry with exact repository-relative Knowledge and Rule paths.
- Rewired all 18 Core Skills with explicit `knowledge_dependencies` and exact `rule_dependencies` in frontmatter.
- Added conditional Rule dependency declarations for `account-audit` so Search/ad and PMax/Shopping Rules are activated by explicit conditions rather than filename inference.
- Bumped the 18 Core Skill versions to `1.2.0` to mark the dependency-contract change.
- Upgraded `docs/SKILL_SPEC.md` to define exact dependency-path and registry-consistency requirements.
- Upgraded `docs/SKILL_REGISTRY.md` to document the v2 dependency graph contract.
- Extended `scripts/validate_skills.py` to cross-check registry ↔ Skill frontmatter, validate exact dependency paths, and reject inference-based dependency declarations.

### Design decisions

- Consumers must never infer Rule filenames from category names, directory names, or descriptive labels.
- Skill frontmatter and `skills/registry.yaml` are mirrored, cross-validated declarations of the same dependency graph.
- Conditional Rules retain exact repository paths; only their activation condition is conditional.
- The dependency graph is designed for Gemini repository grounding and future orchestrator/runtime resolution.

## 2026-08-11 — Phase 3B

### Added

- Populated V1 Knowledge layer with 11 canonical assets covering strategy, structure, keyword intent/match types, bidding, conversion measurement, search terms, RSA/message match, Performance Max, B2B lead generation, and performance diagnosis.
- Added 21 reusable evidence-gated Rules across search terms, keywords, bidding, conversion, budget, structure, ads, and Performance Max.
- Connected the 18 Core Skills to Knowledge and Rule dependencies in `docs/SKILL_REGISTRY.md`.
- Updated Knowledge and Rule indexes.

### Design decisions

- Google first-party documentation is the preferred authority for platform behavior.
- Rules require evidence and explicitly account for false positives, insufficient data, conversion lag, or tracking integrity where relevant.
- Material account changes remain human-approval actions by default.
- Thresholds are contextual rather than universal unless explicitly supported by authoritative documentation.
