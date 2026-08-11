---
name: performance-diagnosis
version: 1.1.0
description: Diagnose Google Ads performance changes and identify evidence-backed drivers, business impact, actions, and measurement requirements.
category: analytics
status: core
---
# Performance Diagnosis
## Purpose
Move from metric movement to ranked hypotheses and actions while separating observation from causality.
## Use When
- CPA/ROAS/CVR/CTR/spend changes unexpectedly.
- A campaign/account is underperforming.
- Management asks what happened and what to do next.
## Do Not Use When
- There is no valid comparison window or business outcome definition.
## Required Inputs
Time-series/comparative performance, campaign segmentation, conversion definitions, business context.
## Optional Inputs
Search terms, device, geography, audience, creative, bidding, budget, CRM quality, change history.
## Preconditions
Validate data integrity, date comparability, attribution, lag, and material account changes.
## Knowledge Dependencies
- `knowledge/analytics/performance-diagnosis.md`
- `knowledge/measurement/conversion-framework.md`
- `knowledge/bidding/bidding-principles.md`
## Rule Dependencies
- `rules/search-term/high-spend-zero-conversion.yaml`
- `rules/bidding/conversion-signal-risk.yaml`
- `rules/budget/scale-with-quality-risk.yaml`
## Workflow
1. Validate comparison windows and data integrity.
2. Establish exactly what changed.
3. Decompose by available dimensions.
4. Run relevant Rules on normalized contexts.
5. Rank hypotheses by evidence, impact, and alternative explanations.
6. Separate observation, inference, and recommendation.
7. Define actions, counterfactual tests, and measurement plan.
## Rule Engine Contract
Use Rule Engine outputs as evidence-backed signals. Never turn a matched Rule into causal proof; combine it with comparative evidence and change history.
## Decision Logic
Prefer explanations supported by multiple independent signals. Causality requires stronger evidence than correlation; label hypotheses accordingly.
## Output Contract
- Executive summary
- What changed
- Observation table
- Rule findings
- Root-cause hypotheses
- Evidence/alternative explanations
- Priority/impact/confidence
- Recommended actions
- Data gaps
- Next measurement
## Confidence
High only when multiple evidence streams support the same driver; Medium for strong directional evidence; Low for single-signal hypotheses.
## Safety
Do not invent missing dimensions or causal explanations. Account changes require human approval.
## Related Skills
`account-audit`, `search-term-analysis`, `conversion-tracking`, `bidding-strategy`, `budget-optimization`
## Examples
If only CPA changed and no decomposition data exists, report the movement and request the dimensions needed to diagnose it.
