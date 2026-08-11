# Skill Registry v1

The registry is the canonical map of Core Skills, their purpose, source lineage, and dependencies.

| ID | Skill | Category | Source lineage | Status |
|---|---|---|---|---|
| S01 | account-audit | audit | agent-skills audit + ads-skills structure | core |
| S02 | campaign-strategy | strategy | both repos | core |
| S03 | campaign-structure | strategy | ads-skills account structure | core |
| S04 | keyword-research | acquisition | agent-skills + ads-skills keyword knowledge | core |
| S05 | search-term-analysis | analytics | both repos search-term knowledge | core |
| S06 | negative-keyword-mining | acquisition | merged search-term/negative skills | core |
| S07 | quality-score | optimization | agent-skills | core |
| S08 | ad-copy | creative | agent-skills ad-copy + ads-skills RSA | core |
| S09 | landing-page-audit | conversion | agent-skills + ads-skills RSA/LP | core |
| S10 | bidding-strategy | optimization | both repos | core |
| S11 | budget-optimization | optimization | agent-skills + ads-skills measurement | core |
| S12 | pmax-optimization | campaign-type | both repos | core |
| S13 | shopping-ads | campaign-type | agent-skills | core |
| S14 | audience-strategy | targeting | agent-skills | core |
| S15 | remarketing-strategy | targeting | agent-skills | core |
| S16 | competitor-analysis | strategy | agent-skills | core |
| S17 | conversion-tracking | measurement | agent-skills + ads-skills API/measurement | core |
| S18 | performance-diagnosis | analytics | new synthesis from both repos | core |

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
- Status values: `draft`, `core`, `experimental`, `deprecated`.
