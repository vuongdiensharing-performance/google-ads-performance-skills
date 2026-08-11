# Skill Registry v1.1

The registry is the canonical map of Core Skills, their Knowledge and Rule dependencies, and their runtime role. Every Core Skill must follow `docs/SKILL_SPEC.md` and consume the Rule Engine where deterministic checks are applicable.

| ID | Skill | Category | Knowledge | Core Rules | Runtime role |
|---|---|---|---|---|---|
| S01 | account-audit | audit | structure, intent, bidding, measurement, diagnosis | structure, bidding, search, conversion, budget, ad/PMax | orchestrator |
| S02 | campaign-strategy | strategy | intent, funnel, structure, bidding | mixed-intent, fragmentation | planner |
| S03 | campaign-structure | strategy | structure, intent, keyword | fragmentation, mixed-intent | architect |
| S04 | keyword-research | acquisition | keyword-intent, match-types, intent | intent-mismatch, broad-without-smart-bidding | researcher |
| S05 | search-term-analysis | analytics | search-methodology, keyword-intent, conversion | irrelevant-intent, spend-zero-conversion, expansion | diagnostician |
| S06 | negative-keyword-mining | acquisition | keyword-intent, match-types, search-methodology | irrelevant-intent, spend-zero-conversion | action-preparer |
| S07 | quality-score | optimization | match-types, message-match, diagnosis | low-quality-score, message-match | diagnostician |
| S08 | ad-copy | creative | message-match, keyword-intent | pinning, message-match | generator |
| S09 | landing-page-audit | conversion | message-match, conversion | message-match, tracking-integrity | auditor |
| S10 | bidding-strategy | optimization | bidding, conversion, diagnosis | objective-mismatch, target-changes, signal-risk, broad-context | optimizer |
| S11 | budget-optimization | optimization | bidding, diagnosis | budget-opportunity, scale-quality-risk | optimizer |
| S12 | pmax-optimization | campaign-type | PMax, PMax-B2B, conversion | primary-goal, recent-change, negative-restriction | specialist |
| S13 | shopping-ads | campaign-type | PMax, conversion | primary-goal, budget-opportunity | specialist |
| S14 | audience-strategy | targeting | intent, conversion | lead-quality-gap | strategist |
| S15 | remarketing-strategy | targeting | intent, conversion | lead-quality-gap | strategist |
| S16 | competitor-analysis | strategy | intent, keyword | mixed-intent | researcher |
| S17 | conversion-tracking | measurement | conversion | primary-micro-conversion, tracking-integrity, lead-quality | measurement auditor |
| S18 | performance-diagnosis | analytics | diagnosis, conversion, bidding | spend-zero-conversion, signal-risk, scale-quality-risk | diagnostician |

## Runtime contract

Every Core Skill follows:

`Validate → Load Knowledge → Normalize Context → Run Rules → Classify → Prioritize → Recommend → Measure`

The exact stages may be shortened for generative/planning Skills, but evidence validation, dependency loading, and safety must remain explicit.

## Machine registry

`skills/registry.yaml` mirrors this document for tooling and validation.

## Knowledge Registry

V1 populated assets include intent, funnel strategy, account structure, keyword intent, match types, bidding principles, conversion framework, search-term methodology, RSA/message match, PMax principles/B2B, and performance diagnosis.

## Rule Registry

V1 contains reusable evidence-gated Rules across search terms, keywords, bidding, conversion, budget, structure, ads, and Performance Max. Rules return findings; Skills assign business priority.

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
- Every Core Skill must name Knowledge and Rule dependencies.
- Rule Engine results must not be presented as causality without supporting evidence.
- Severity and priority remain separate.
- Source-repository claims are lineage, not authority.
- Platform facts should point to current first-party documentation where practical.
