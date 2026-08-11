---
name: remarketing-strategy
version: 1.1.0
description: Design and evaluate Google Ads remarketing using lifecycle intent, first-party audiences, exclusions, and incremental-value considerations.
category: targeting
status: core
---
# Remarketing Strategy
## Purpose
Reconnect relevant users by lifecycle stage while separating attribution from incremental value.
## Use When
- Designing remarketing audiences.
- Reviewing windows, exclusions, overlap, lifecycle segmentation, or attributed performance.
## Do Not Use When
- Lifecycle events or audience evidence are unavailable.
## Required Inputs
Audience definitions, lifecycle events, campaign type, conversion goals, performance data.
## Optional Inputs
CRM stages, customer lists, exclusion logic, experiment results.
## Preconditions
Define lifecycle stages, eligibility, windows, exclusions, and business outcome.
## Knowledge Dependencies
- `knowledge/strategy/intent-framework.md`
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/conversion/lead-quality-gap.yaml`
## Workflow
1. Define lifecycle segments.
2. Set windows and exclusions.
3. Map message to lifecycle stage.
4. Run audience/quality Rules.
5. Review overlap and attribution.
6. Assess incremental evidence.
7. Recommend controlled tests and measurement.
## Rule Engine Contract
Evaluate `remarketing_context`; a Rule match flags a review item and never proves incrementality.
## Decision Logic
Attributed remarketing conversions alone do not establish incremental conversions. Favor lifecycle relevance and controlled exclusions/tests.
## Output Contract
- Audience/lifecycle map
- Exclusions
- Rule findings
- Messaging approach
- Evidence/limitations
- Incrementality risks
- Test plan
## Confidence
High for audience configuration; Medium/Low for incremental claims.
## Safety
Audience and exclusion changes require human approval.
## Related Skills
`audience-strategy`, `conversion-tracking`, `campaign-strategy`, `performance-diagnosis`
## Examples
Explicitly distinguish platform attribution from experiment-based incrementality.
