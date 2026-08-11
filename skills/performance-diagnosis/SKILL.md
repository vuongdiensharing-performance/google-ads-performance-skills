---
name: performance-diagnosis
version: 1.0.0
description: Diagnose Google Ads performance changes and identify likely drivers, business impact, actions, and measurement requirements.
category: analytics
status: core
---
# Performance Diagnosis
## Purpose
Move from metric movement to evidence-backed hypotheses and prioritized actions.
## Use When
- CPA/ROAS/CVR/CTR/spend changes unexpectedly.
- A campaign or account is underperforming.
- Management asks “what happened and what should we do?”
## Required Inputs
Time-series or comparative performance data, campaign segmentation, conversion definitions, and business context.
## Workflow
1. Validate data integrity and comparison windows.
2. Establish what changed.
3. Decompose by campaign, query, device, geography, audience, creative, bidding, budget, and conversion quality where available.
4. Separate correlation from plausible causation.
5. Apply relevant Rules.
6. Rank hypotheses by evidence and impact.
7. Recommend actions and a measurement plan.
## Output Contract
- Executive summary
- Observation table
- Root-cause hypotheses
- Evidence
- Priority/impact/confidence
- Recommended actions
- Data gaps
- Next measurement
## Safety
Do not attribute causality from correlation alone. Do not invent missing dimensions.
## Related Skills
account-audit, search-term-analysis, conversion-tracking, bidding-strategy, budget-optimization
