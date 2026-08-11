---
name: campaign-strategy
version: 1.2.0
description: Translate business goals and demand intent into a Google Ads campaign strategy and measurement plan.
category: strategy
status: core
knowledge_dependencies:
  - knowledge/strategy/intent-framework.md
  - knowledge/strategy/funnel-strategy.md
  - knowledge/structure/account-structure.md
  - knowledge/bidding/bidding-principles.md
rule_dependencies:
  - rules/structure/mixed-intent-campaign.yaml
  - rules/structure/fragmentation-risk.yaml
---
# Campaign Strategy
## Purpose
Turn business objectives into an intent-led campaign portfolio, bidding direction, budget logic, and measurement plan.
## Use When
- Planning a new Google Ads program.
- Reworking account strategy after business, offer, or funnel changes.
## Do Not Use When
- The request is only keyword, ad, bid, or tracking execution.
## Required Inputs
Business objective, primary conversion outcome, offer, market, geography, budget, constraints.
## Optional Inputs
Historical performance, CRM quality, margin/economics, competitor evidence.
## Preconditions
Validate the business outcome, conversion definition, market scope, and measurement maturity.
## Knowledge Dependencies
- `knowledge/strategy/intent-framework.md`
- `knowledge/strategy/funnel-strategy.md`
- `knowledge/structure/account-structure.md`
- `knowledge/bidding/bidding-principles.md`
## Rule Dependencies
- `rules/structure/mixed-intent-campaign.yaml`
- `rules/structure/fragmentation-risk.yaml`
## Workflow
1. Validate business outcome and constraints.
2. Map demand by intent/funnel stage.
3. Design campaign boundaries and sequencing.
4. Define budget and bidding direction compatible with data maturity.
5. Define conversion/learning signals.
6. Run relevant structure Rules on the proposed context.
7. Produce implementation, test, and measurement roadmap.
## Rule Engine Contract
Evaluate proposed `strategy_context` with the canonical Rule Engine. Matched Rules become design warnings/recommendations; no account mutation is permitted.
## Decision Logic
Prioritize proven high-intent demand before speculative expansion unless the stated objective is demand generation. Avoid segmentation that creates thin data without a control/reporting reason.
## Output Contract
- Strategy objective
- Intent map
- Campaign portfolio
- Budget/bidding logic
- Measurement requirements
- Risks/assumptions
- Test roadmap
## Confidence
High when objective, economics, and measurement are explicit; otherwise Medium/Low.
## Safety
Planning only. Campaign creation or changes require human approval.
## Related Skills
`campaign-structure`, `keyword-research`, `audience-strategy`, `bidding-strategy`, `budget-optimization`, `conversion-tracking`
## Examples
Never invent demand, competitor behavior, or benchmarks without evidence.
