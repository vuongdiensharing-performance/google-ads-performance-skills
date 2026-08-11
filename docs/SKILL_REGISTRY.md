# Skill Registry v1

The registry is the canonical map of Core Skills, their purpose, source lineage, and dependencies.

| ID | Skill | Category | Knowledge | Core Rules | Status |
|---|---|---|---|---|---|
| S01 | account-audit | audit | account-structure, performance-diagnosis | fragmentation-risk, mixed-intent-campaign | core |
| S02 | campaign-strategy | strategy | intent-framework, account-structure | mixed-intent-campaign | core |
| S03 | campaign-structure | strategy | account-structure, intent-framework | fragmentation-risk, mixed-intent-campaign | core |
| S04 | keyword-research | acquisition | keyword-intent, match-types | intent-theme-mismatch, broad-without-smart-bidding | core |
| S05 | search-term-analysis | analytics | search-term-methodology, keyword-intent | irrelevant-intent, high-spend-zero-conversion, expansion-candidate | core |
| S06 | negative-keyword-mining | acquisition | search-term-methodology, match-types | irrelevant-intent, high-spend-zero-conversion | core |
| S07 | quality-score | optimization | match-types, rsa-message-match | low-quality-score-investigation | core |
| S08 | ad-copy | creative | rsa-message-match, keyword-intent | excessive-pinning, message-match-gap | core |
| S09 | landing-page-audit | conversion | rsa-message-match, conversion-framework | message-match-gap | core |
| S10 | bidding-strategy | optimization | bidding-principles, conversion-framework | objective-strategy-mismatch, frequent-target-changes, conversion-signal-risk | core |
| S11 | budget-optimization | optimization | bidding-principles, performance-diagnosis | budget-constraint-opportunity, scale-with-quality-risk | core |
| S12 | pmax-optimization | campaign-type | pmax-principles, pmax-b2b, conversion-framework | primary-goal-missing, recent-change-learning, overrestrictive-negative | core |
| S13 | shopping-ads | campaign-type | pmax-principles, conversion-framework | primary-goal-missing | core |
| S14 | audience-strategy | targeting | intent-framework, conversion-framework | lead-quality-gap | core |
| S15 | remarketing-strategy | targeting | intent-framework, conversion-framework | lead-quality-gap | core |
| S16 | competitor-analysis | strategy | intent-framework, keyword-intent | mixed-intent-campaign | core |
| S17 | conversion-tracking | measurement | conversion-framework | primary-micro-conversion, tracking-integrity-risk, lead-quality-gap | core |
| S18 | performance-diagnosis | analytics | performance-diagnosis, conversion-framework, bidding-principles | high-spend-zero-conversion, conversion-signal-risk, scale-with-quality-risk | core |

## Knowledge Registry

V1 populated knowledge assets:

- `strategy/intent-framework.md`
- `structure/account-structure.md`
- `keyword/keyword-intent.md`
- `keyword/match-types.md`
- `bidding/bidding-principles.md`
- `measurement/conversion-framework.md`
- `search/search-term-methodology.md`
- `ads/rsa-message-match.md`
- `pmax/pmax-principles.md`
- `pmax/pmax-b2b.md`
- `analytics/performance-diagnosis.md`

## Rule Registry

V1 contains 21 reusable rules across search terms, keywords, bidding, conversion, budget, structure, ads, and Performance Max. Rules are evidence-gated and do not execute account changes by default.

## Dependency graph

`account-audit → performance-diagnosis → action plan`

`campaign-strategy → campaign-structure → keyword-research → ad-copy`

`search-term-analysis → negative-keyword-mining`

`conversion-tracking → performance-diagnosis`

`bidding-strategy ↔ budget-optimization`

`ad-copy ↔ landing-page-audit`

`pmax-optimization` and `shopping-ads` operate as specialized campaign-type workflows.

## Registry rules

- Every Skill must have a matching directory and `SKILL.md`.
- A Skill may consume multiple Knowledge and Rule assets.
- Duplicate source concepts should be merged into one canonical Skill.
- Source-repository claims are lineage, not authority.
- Platform facts should point to current first-party documentation where practical.
- Status values: `draft`, `core`, `experimental`, `deprecated`.
