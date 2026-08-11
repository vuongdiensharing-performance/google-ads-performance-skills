---
name: pmax-optimization
version: 1.1.0
description: Diagnose and optimize Performance Max using asset, audience, conversion, budget, and available placement/search evidence.
category: campaign-type
status: core
---
# Performance Max Optimization
## Purpose
Evaluate PMax as a system while protecting conversion quality and avoiding unsupported conclusions from opaque reporting.
## Use When
- Auditing or optimizing PMax.
- Assessing assets, audience signals, budget, bidding, conversion quality, or recent changes.
## Do Not Use When
- Required PMax configuration/conversion evidence is unavailable.
## Required Inputs
Campaign settings, conversion configuration, performance, asset/diagnostic data, business outcomes.
## Optional Inputs
Search categories, audience signals, placement/brand evidence, CRM outcomes, change history.
## Preconditions
Validate primary goal/value and distinguish platform-reported outcomes from business outcomes.
## Knowledge Dependencies
- `knowledge/pmax/pmax-principles.md`
- `knowledge/pmax/pmax-b2b.md`
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/pmax/primary-goal-missing.yaml`
- `rules/pmax/recent-change-learning.yaml`
- `rules/pmax/overrestrictive-negative.yaml`
## Workflow
1. Validate conversion goal/value quality.
2. Check objective, budget, bidding, and settings.
3. Review asset-group/creative coverage.
4. Review audience/search-category signals where available.
5. Run PMax Rules.
6. Separate observed issues from opaque-system hypotheses.
7. Recommend controlled changes/tests and measurement.
## Rule Engine Contract
Evaluate normalized `pmax_context`; do not infer unavailable query/placement detail. Rule findings must preserve evidence limitations.
## Decision Logic
Protect business-quality conversions before optimizing reported volume. Treat recent structural/bidding changes as context for short-term volatility rather than automatic failure.
## Output Contract
- PMax health summary
- Evidence/limitations
- Rule findings
- Findings by component
- Prioritized actions
- Test/measurement plan
- Confidence
## Confidence
High for directly observable settings/data; Medium/Low for causal or hidden-dimension hypotheses.
## Safety
No PMax setting, asset, budget, or bidding change without approval.
## Related Skills
`conversion-tracking`, `budget-optimization`, `ad-copy`, `performance-diagnosis`
## Examples
Explicitly mark unavailable search-term/placement evidence rather than filling gaps with assumptions.
