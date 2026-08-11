---
name: bidding-strategy
version: 1.0.0
description: Select, diagnose, and optimize Google Ads bidding strategies based on conversion maturity, goals, economics, and data quality.
category: optimization
status: core
---

# Bidding Strategy

## Purpose
Match bidding approach to business objective, conversion signal quality, volume, value, and constraints.

## Use When
- Choosing a bidding strategy.
- Diagnosing unstable or inefficient bidding.
- Planning a transition between bidding approaches.

## Required Inputs
Campaign objective, conversion definition, conversion volume/value, current strategy, targets, budget, and data quality.

## Knowledge Dependencies
- Bidding principles
- Conversion framework
- Performance framework

## Workflow
1. Validate the primary conversion and data quality.
2. Define optimization objective.
3. Assess volume/value maturity and constraints.
4. Evaluate current strategy and target realism.
5. Recommend strategy or controlled test.
6. Define transition guardrails and measurement window.

## Output Contract
- Current-state diagnosis
- Strategy fit
- Risks
- Recommended action/test
- Guardrails
- Measurement plan

## Safety
Do not recommend target changes from a single volatile period without sufficient evidence.

## Related Skills
conversion-tracking, budget-optimization, performance-diagnosis, campaign-strategy
