---
name: bidding-strategy
version: 1.2.1
description: Select, diagnose, and optimize Google Ads bidding based on objective, conversion maturity, economics, data quality, and constraints.
category: optimization
status: core
knowledge_dependencies:
  - knowledge/bidding/bidding-principles.md
  - knowledge/measurement/conversion-framework.md
  - knowledge/analytics/performance-diagnosis.md
rule_dependencies:
  - rules/bidding/objective-strategy-mismatch.yaml
  - rules/bidding/frequent-target-changes.yaml
  - rules/bidding/conversion-signal-risk.yaml
  - rules/keyword/broad-without-smart-bidding.yaml
---
# Bidding Strategy
## Purpose
Match bidding approach and target settings to business outcome, signal quality, volume/value maturity, and constraints.
## Use When
- Choosing a bidding strategy.
- Diagnosing unstable or inefficient bidding.
- Planning controlled strategy/target transitions.
## Do Not Use When
- Conversion measurement is materially untrusted and no correction path is defined.
## Required Inputs
Objective, conversion definition, volume/value, current strategy, targets, budget, data quality.
## Optional Inputs
Lag, margin, seasonality, portfolio context, historical target changes.
## Preconditions
Validate primary conversion, data quality, lookback, lag, and business target.
## Knowledge Dependencies
- `knowledge/bidding/bidding-principles.md`
- `knowledge/measurement/conversion-framework.md`
- `knowledge/analytics/performance-diagnosis.md`
## Rule Dependencies
- `rules/bidding/objective-strategy-mismatch.yaml`
- `rules/bidding/frequent-target-changes.yaml`
- `rules/bidding/conversion-signal-risk.yaml`
- `rules/keyword/broad-without-smart-bidding.yaml`
## Workflow
1. Validate conversion signal.
2. Define optimization objective and economics.
3. Assess volume/value maturity and constraints.
4. Evaluate current strategy and target stability.
5. Run bidding Rules.
6. Recommend strategy/test with guardrails.
7. Define transition and measurement window.
## Rule Engine Contract
Evaluate normalized `bidding_context`; Rule matches must include evidence and become recommendations, never automatic target changes.
## Decision Logic
Do not change targets based on one volatile period. Measurement quality and business outcome fit precede platform-strategy preference.
## Output Contract
- Current-state diagnosis
- Rule findings
- Strategy fit
- Target/strategy recommendation
- Risks/guardrails
- Measurement plan
- Confidence
## Confidence
High when objective, signal quality, volume/value, and time window are clear.
## Safety
Bid/target changes require human approval.
## Related Skills
`conversion-tracking`, `budget-optimization`, `performance-diagnosis`, `campaign-strategy`
## Examples
State the missing evidence when target recommendations cannot be justified.
