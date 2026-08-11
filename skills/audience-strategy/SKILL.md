---
name: audience-strategy
version: 1.1.0
description: Design and evaluate Google Ads audience strategy using intent, first-party signals, observation/targeting mode, and business value.
category: targeting
status: core
---
# Audience Strategy
## Purpose
Use audience signals and targeting controls to improve relevance, discovery, and measurement without treating audience membership as causal intent.
## Use When
- Planning audience layering or observation.
- Reviewing audience performance.
- Building first-party or lifecycle strategies.
## Do Not Use When
- Audience definitions or business outcome are unknown.
## Required Inputs
Business objective, audience definitions, campaign type, available first-party data, performance evidence.
## Optional Inputs
CRM quality, exclusions, overlap, lifecycle events, incrementality tests.
## Preconditions
Define each audience's role: targeting, observation, signal, or exclusion.
## Knowledge Dependencies
- `knowledge/strategy/intent-framework.md`
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/conversion/lead-quality-gap.yaml`
## Workflow
1. Define audience role and business purpose.
2. Map intent/lifecycle relationship.
3. Check eligibility, size, overlap, and exclusions.
4. Run relevant Rules.
5. Evaluate performance and incremental evidence.
6. Recommend setup/test plan.
## Rule Engine Contract
Evaluate `audience_context`; treat Rule matches as evidence-backed risks/opportunities, not causal proof.
## Decision Logic
Audience correlation does not prove incremental value. Protect exclusions and high-value lifecycle segments explicitly.
## Output Contract
- Audience map
- Role/scope
- Rule findings
- Evidence
- Overlap/risks
- Recommended tests
- Confidence
## Confidence
High for configuration facts; Medium/Low for causal or incremental conclusions.
## Safety
Audience targeting/exclusion changes require human approval.
## Related Skills
`remarketing-strategy`, `campaign-strategy`, `conversion-tracking`, `performance-diagnosis`
## Examples
Do not claim an audience caused better performance from attributed conversions alone.
