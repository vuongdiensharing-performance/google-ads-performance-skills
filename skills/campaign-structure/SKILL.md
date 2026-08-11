---
name: campaign-structure
version: 1.1.0
description: Design or review Google Ads campaign and ad-group structure for intent separation, budget control, learning, and reporting clarity.
category: strategy
status: core
---
# Campaign Structure
## Purpose
Create or diagnose campaign architecture without unnecessary fragmentation or mixed intent.
## Use When
- Building a new account structure.
- Reviewing campaign segmentation, ad groups, themes, or budget boundaries.
## Do Not Use When
- The problem is isolated to copy, bidding, tracking, or search terms.
## Required Inputs
Business goals, offers, geographies, existing structure, budget, volume constraints.
## Preconditions
Normalize campaigns, objectives, budgets, locations, themes, and volume evidence.
## Knowledge Dependencies
- `knowledge/structure/account-structure.md`
- `knowledge/strategy/intent-framework.md`
- `knowledge/keyword/keyword-intent.md`
## Rule Dependencies
- `rules/structure/fragmentation-risk.yaml`
- `rules/structure/mixed-intent-campaign.yaml`
## Workflow
1. Map business lines and demand themes.
2. Identify material differences in budget, bidding, geography, objective, or reporting.
3. Propose campaign boundaries.
4. Map ad groups/themes.
5. Run structure Rules against the normalized structure context.
6. Separate necessary boundaries from unnecessary fragmentation.
7. Produce migration and validation steps.
## Rule Engine Contract
Rules are evidence-gated. A matched fragmentation/mixed-intent Rule is a finding, not an automatic restructuring command.
## Decision Logic
Separate campaigns only when control, economics, intent, geography, objective, or reporting materially differs. Prefer consolidation when fragmentation reduces learning or makes evidence thin.
## Output Contract
- Current/proposed structure
- Boundary rationale
- Rule findings
- Naming/reporting convention
- Risks
- Migration steps
- Validation plan
## Confidence
High when configuration and volume data are complete; Medium when volume or intent evidence is partial.
## Safety
No create/edit operation without human approval.
## Related Skills
`campaign-strategy`, `keyword-research`, `account-audit`, `bidding-strategy`, `performance-diagnosis`
## Examples
Do not claim a campaign is over-fragmented without showing the relevant control/volume evidence.
