---
name: budget-optimization
version: 1.2.0
description: Reallocate Google Ads budget using performance evidence, marginal opportunity, business constraints, and portfolio logic.
category: optimization
status: core
knowledge_dependencies:
  - knowledge/bidding/bidding-principles.md
  - knowledge/analytics/performance-diagnosis.md
rule_dependencies:
  - rules/budget/budget-constraint-opportunity.yaml
  - rules/budget/scale-with-quality-risk.yaml
---
# Budget Optimization
## Purpose
Identify where budget can be protected, reduced, increased, or tested without optimizing on a single metric.
## Use When
- Budget allocation is under review.
- Campaigns are constrained while others show weaker evidence of marginal return.
- Scaling decisions need portfolio context.
## Do Not Use When
- Conversion quality or attribution is materially unreliable.
## Required Inputs
Campaign spend, conversions/value, targets, budget limits, impression-share signals where available, lag context.
## Optional Inputs
Margins, seasonality, capacity constraints, experiment history, CRM quality.
## Preconditions
Normalize campaigns by objective/intent and validate comparable windows.
## Knowledge Dependencies
- `knowledge/bidding/bidding-principles.md`
- `knowledge/analytics/performance-diagnosis.md`
## Rule Dependencies
- `rules/budget/budget-constraint-opportunity.yaml`
- `rules/budget/scale-with-quality-risk.yaml`
## Workflow
1. Validate data and attribution.
2. Segment by objective/intent.
3. Assess efficiency, volume, constraints, and quality.
4. Run budget Rules.
5. Model scenarios and assumptions.
6. Recommend reallocation/test with guardrails.
7. Define measurement and rollback conditions.
## Rule Engine Contract
Evaluate normalized `budget_context`; matched Rules identify opportunities/risks, while exact incremental returns remain scenarios unless validated.
## Decision Logic
A constrained high-performing campaign is not automatically the best destination for more budget. Check marginal opportunity, conversion quality, capacity, and business economics.
## Output Contract
- Portfolio view
- Rule findings
- Opportunity/risk table
- Proposed budget changes
- Scenario assumptions
- Guardrails
- Measurement plan
## Confidence
High for observed constraints/performance; Medium/Low for incremental forecasts.
## Safety
Budget changes require human approval. Never present a scenario as guaranteed incremental return.
## Related Skills
`bidding-strategy`, `campaign-strategy`, `performance-diagnosis`, `account-audit`
## Examples
Label modeled outcomes separately from historical observations.
