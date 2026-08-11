---
id: performance-diagnosis
version: 1.0.0
type: methodology
category: analytics
authority: validated-methodology
status: stable
---

# Performance Diagnosis Framework

## Principle

Diagnose the system before changing the lever. A weak KPI can originate in demand quality, targeting, auction economics, creative, landing page, measurement, or business quality.

## Diagnostic chain

Business outcome → conversion quality → conversion rate → traffic quality → ad relevance → targeting → bidding → budget → delivery.

## Required separation

- Observation: directly supported by data.
- Inference: plausible explanation supported by evidence.
- Recommendation: proposed action.
- Confidence: high, medium, or low.

## Minimum diagnostic questions

1. Is measurement trustworthy?
2. Is the conversion being optimized the right business outcome?
3. Did traffic mix change?
4. Did auction conditions change?
5. Did creative or landing-page relevance change?
6. Is there enough data and conversion lag accounted for?
7. Which action has the highest expected business impact?

## Anti-patterns

- Optimizing a downstream KPI using only top-of-funnel metrics.
- Treating correlation as causation.
- Making multiple major changes simultaneously and then claiming causal certainty.

## Related skills

- account-audit
- conversion-tracking
- bidding-strategy
- budget-optimization
- performance-diagnosis
