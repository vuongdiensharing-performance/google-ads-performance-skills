# Skill Registry v2.1

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

`skills/registry.yaml` is the Skill dependency graph. Version 2.1 additionally points to the Rule Knowledge provenance registry:

```yaml
version: 2.1.0
schema: skill-dependency-graph/v1
dependency_policy:
  knowledge: exact_repository_paths
  rules: exact_repository_paths
  rule_knowledge_provenance: exact_repository_paths
  no_inference: true
rule_provenance_registry: rules/registry.yaml
```

The full Skill dependency graph lives in `skills/registry.yaml`; Rule → Knowledge provenance lives in `rules/registry.yaml`.

## Rule Knowledge provenance registry

`rules/registry.yaml` uses schema `rule-knowledge-provenance/v1` and maps every active Rule ID to:

- its exact Rule path;
- its exact Knowledge dependency paths;
- the same dependency declaration stored inside the Rule file.

Example:

```yaml
- id: STR-FRAG-001
  path: rules/structure/fragmentation-risk.yaml
  knowledge:
    - knowledge/structure/account-structure.md
```

This closes the provenance gap identified during Gate 2B: a resolved Rule now has an explicit machine-readable path to the Knowledge that informs it.

## Dependency contract

For every Core Skill:

1. `path` points to the exact `SKILL.md`.
2. `knowledge` contains exact repository-relative Knowledge paths.
3. `rules` contains exact repository-relative Rule paths.
4. Conditional Rule dependencies contain exact paths plus a machine-readable activation condition.
5. Every referenced Rule must exist in `rules/registry.yaml`.
6. Every Rule in the provenance registry must declare non-empty exact Knowledge dependencies.
7. Rule file `knowledge_dependencies` must match the provenance registry exactly.
8. No consumer may infer Rule filenames or Rule → Knowledge relationships from category names, filenames, directory names, related Skills, or semantic similarity.
9. The registry must match the corresponding Skill frontmatter exactly.
10. Every dependency path must exist in the repository.

## Runtime contract

Every Core Skill follows:

`Validate → Load Knowledge → Normalize Context → Run Rules → Classify → Prioritize → Recommend → Measure`

The exact stages may be shortened for generative/planning Skills, but evidence validation, dependency loading, provenance, and safety must remain explicit.

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
- Every active Rule must declare exact Knowledge provenance.
- Rule Engine results must not be presented as causality without supporting evidence.
- Severity and priority remain separate.
- Source-repository claims are lineage, not authority.
- Platform facts should point to current first-party documentation where practical.
