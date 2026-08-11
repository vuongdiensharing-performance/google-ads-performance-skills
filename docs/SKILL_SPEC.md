# Skill Specification v1.2

## Purpose
A Skill is a bounded, reusable workflow that transforms defined inputs into a structured output. A Skill is not a knowledge dump and must not contain undocumented platform claims as hard-coded truth.

## Canonical frontmatter
```yaml
---
name: search-term-analysis
version: 1.2.0
description: Analyze Google Ads search terms for intent, waste, negatives, and expansion opportunities.
category: analytics
status: core
knowledge_dependencies:
  - knowledge/search/search-term-methodology.md
  - knowledge/keyword/keyword-intent.md
  - knowledge/measurement/conversion-framework.md
rule_dependencies:
  - rules/search-term/irrelevant-intent.yaml
  - rules/search-term/high-spend-zero-conversion.yaml
  - rules/search-term/expansion-candidate.yaml
---
```

## Dependency declaration standard

Core Skills must declare dependency paths twice:

1. In frontmatter for machine-readable local resolution.
2. In the human-readable `Knowledge Dependencies` and `Rule Dependencies` sections for inspection.

Dependency paths must be exact repository-relative paths. Consumers must not infer filenames from category names, directory names, or Rule descriptions.

### Knowledge dependencies

`knowledge_dependencies` is a list of exact repository-relative Knowledge asset paths.

### Rule dependencies

`rule_dependencies` is a list of exact repository-relative Rule paths that are applicable by default.

Conditional Rules must use:

```yaml
conditional_rule_dependencies:
  - when: search_ads_or_ad_assets_present
    rules:
      - rules/ad/message-match-gap.yaml
```

The `when` value is a machine-readable condition identifier defined by the consuming runtime. Conditional dependencies are still exact repository paths; only activation is conditional.

## Required sections
1. `# <Skill Name>`
2. `## Purpose`
3. `## Use When`
4. `## Do Not Use When`
5. `## Required Inputs`
6. `## Preconditions`
7. `## Knowledge Dependencies`
8. `## Rule Dependencies`
9. `## Workflow`
10. `## Rule Engine Contract`
11. `## Decision Logic`
12. `## Output Contract`
13. `## Confidence`
14. `## Safety`
15. `## Related Skills`
16. `## Examples`

Optional sections such as `Optional Inputs` may be included when useful.

## Runtime standard

Core Skills follow:

`Validate → Load Knowledge → Normalize Context → Run Rules → Classify → Prioritize → Recommend → Measure`

Not every Skill needs every stage, but omissions must be intentional and documented.

## Knowledge wiring

Every Core Skill must explicitly name the Knowledge assets it consumes. Knowledge provides principles, frameworks, definitions, and methodology; it does not by itself create account findings.

## Rule wiring

Every Core Skill must explicitly name its Rule dependencies. The canonical Rule Engine evaluates the normalized context and returns:

- `matched`
- `not_matched`
- `excluded`
- `insufficient_evidence`

A Skill must preserve `insufficient_evidence` as a data gap rather than force a conclusion.

## Registry consistency

`skills/registry.yaml` is the machine-readable dependency graph. For every Core Skill:

- `path` must point to the exact `SKILL.md`.
- `knowledge` must equal the Skill frontmatter `knowledge_dependencies`.
- `rules` must equal the Skill frontmatter `rule_dependencies`.
- Conditional Rules must be represented identically in the Skill frontmatter and registry.
- Every referenced dependency path must exist in the repository.

The registry and Skill frontmatter are therefore cross-validated artifacts, not independent summaries.

## Evidence discipline

A Skill must never invent account data. If required evidence is absent, request the missing input or downgrade the conclusion explicitly.

## Diagnostic output

Diagnostic Skills should separate:

- Observation — directly supported by data.
- Inference — interpretation of the evidence.
- Recommendation — proposed action.
- Confidence — high, medium, or low.

## Prioritization

Severity comes from Rules; priority is assigned by the Skill using impact, evidence, confidence, urgency, business constraints, and reversibility. Severity and priority are not interchangeable.

## Safety

Read/analyze/recommend/prepare are allowed by default. Changes to campaigns, budgets, bids, keywords, ads, targeting, conversion settings, or other account state require human approval unless a consuming system explicitly grants execution authority.

## Output Contract

Outputs must be deterministic enough for a human or downstream agent to consume. Findings should expose evidence, impact, confidence, Rule/Skill provenance where applicable, recommended action, approval state, and measurement.

## Quality gates

A Core Skill is valid when:
- frontmatter is complete;
- inputs and preconditions are explicit;
- Knowledge and Rule dependencies are named with exact repository paths;
- human-readable and machine-readable dependency declarations agree;
- workflow is actionable;
- Rule Engine contract is explicit;
- output is deterministic enough to consume;
- safety behavior is explicit;
- examples do not fabricate real account results.
