# Skill Registry v2.0

The registry is the canonical machine-readable dependency graph for Core Skills. Each Skill declares exact repository-relative Knowledge and Rule paths, and the registry mirrors those declarations for tooling, validation, orchestration, and model grounding.

## Core Skills

| ID | Skill | Path | Category | Runtime role |
|---|---|---|---|---|
| S01 | account-audit | `skills/account-audit/SKILL.md` | audit | orchestrator |
| S02 | campaign-strategy | `skills/campaign-strategy/SKILL.md` | strategy | planner |
| S03 | campaign-structure | `skills/campaign-structure/SKILL.md` | strategy | architect |
| S04 | keyword-research | `skills/keyword-research/SKILL.md` | acquisition | researcher |
| S05 | search-term-analysis | `skills/search-term-analysis/SKILL.md` | analytics | diagnostician |
| S06 | negative-keyword-mining | `skills/negative-keyword-mining/SKILL.md` | acquisition | action-preparer |
| S07 | quality-score | `skills/quality-score/SKILL.md` | optimization | diagnostician |
| S08 | ad-copy | `skills/ad-copy/SKILL.md` | creative | generator |
| S09 | landing-page-audit | `skills/landing-page-audit/SKILL.md` | conversion | auditor |
| S10 | bidding-strategy | `skills/bidding-strategy/SKILL.md` | optimization | optimizer |
| S11 | budget-optimization | `skills/budget-optimization/SKILL.md` | optimization | optimizer |
| S12 | pmax-optimization | `skills/pmax-optimization/SKILL.md` | campaign-type | specialist |
| S13 | shopping-ads | `skills/shopping-ads/SKILL.md` | campaign-type | specialist |
| S14 | audience-strategy | `skills/audience-strategy/SKILL.md` | targeting | strategist |
| S15 | remarketing-strategy | `skills/remarketing-strategy/SKILL.md` | targeting | strategist |
| S16 | competitor-analysis | `skills/competitor-analysis/SKILL.md` | strategy | researcher |
| S17 | conversion-tracking | `skills/conversion-tracking/SKILL.md` | measurement | measurement-auditor |
| S18 | performance-diagnosis | `skills/performance-diagnosis/SKILL.md` | analytics | diagnostician |

## Machine registry

`skills/registry.yaml` is the source used by tooling and orchestration. Version 2.0 uses this shape:

```yaml
version: 2.0.0
schema: skill-dependency-graph/v1
dependency_policy:
  knowledge: exact_repository_paths
  rules: exact_repository_paths
  no_inference: true
skills:
  - id: S01
    name: account-audit
    path: skills/account-audit/SKILL.md
    knowledge:
      - knowledge/structure/account-structure.md
    rules:
      - rules/structure/fragmentation-risk.yaml
    conditional_rules:
      - when: pmax_or_shopping_campaign_present
        rules:
          - rules/pmax/primary-goal-missing.yaml
```

The full dependency graph lives in `skills/registry.yaml`; this document deliberately does not duplicate all dependency paths.

## Dependency contract

For every Core Skill:

1. `path` points to the exact `SKILL.md`.
2. `knowledge` contains exact repository-relative Knowledge paths.
3. `rules` contains exact repository-relative Rule paths.
4. Conditional Rule dependencies contain exact paths plus a machine-readable activation condition.
5. No consumer may infer Rule filenames from category names or directory names.
6. The registry must match the corresponding Skill frontmatter exactly.
7. Every dependency path must exist in the repository.

## Runtime contract

Every Core Skill follows:

`Validate → Load Knowledge → Normalize Context → Run Rules → Classify → Prioritize → Recommend → Measure`

The exact stages may be shortened for generative/planning Skills, but evidence validation, dependency loading, and safety must remain explicit.

## Dependency graph

`account-audit → specialized Skills → rule engine → prioritized action plan`

`campaign-strategy → campaign-structure → keyword-research → ad-copy`

`search-term-analysis → negative-keyword-mining`

`conversion-tracking → bidding-strategy → performance-diagnosis`

`bidding-strategy ↔ budget-optimization`

`ad-copy ↔ landing-page-audit`

`pmax-optimization` and `shopping-ads` operate as specialized campaign-type workflows.

## Registry rules

- Every Skill must have a matching directory and `SKILL.md`.
- Every Core Skill must declare exact Knowledge and Rule dependencies.
- Rule Engine results must not be presented as causality without supporting evidence.
- Severity and priority remain separate.
- Source-repository claims are lineage, not authority.
- Platform facts should point to current first-party documentation where practical.
