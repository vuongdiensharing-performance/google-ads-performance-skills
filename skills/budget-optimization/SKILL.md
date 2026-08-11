---
name: budget-optimization
version: 1.0.0
description: Reallocate Google Ads budget using performance evidence, marginal opportunity, business constraints, and portfolio logic.
category: optimization
status: core
---

# Budget Optimization

## Purpose
Identify where budget can be protected, reduced, increased, or tested without optimizing on a single metric.

## Use When
- Budget allocation is under review.
- Some campaigns are constrained while others have weaker marginal returns.
- Scaling decisions need evidence.

## Required Inputs
Campaign spend, conversions/value, targets, budget limits, impression-share signals where available, and conversion lag context.

## Workflow
1. Validate data windows and attribution.
2. Segment campaigns by objective/intent.
3. Assess efficiency and volume.
4. Look for marginal scale opportunity and constraint signals.
5. Model scenarios rather than asserting guaranteed outcomes.
6. Recommend reallocations with guardrails.

## Output Contract
- Portfolio view
- Campaign opportunity/risk table
- Proposed budget changes
- Scenario assumptions
- Measurement plan

## Safety
Never claim an exact incremental return without a validated model or experiment.

## Related Skills
bidding-strategy, campaign-strategy, performance-diagnosis, account-audit
