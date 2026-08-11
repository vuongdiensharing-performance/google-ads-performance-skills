---
name: account-audit
version: 1.1.0
description: Run a read-only, evidence-gated Google Ads account health audit and turn findings into a prioritized action plan.
category: audit
status: core
---

# Account Audit

## Purpose
Orchestrate Core Skills and the Rule Engine to assess measurement, structure, targeting, keywords, ads, bidding, budget, campaign type, and conversion quality.

## Use When
- The user asks for a full Google Ads account audit.
- Multiple campaign-level problems must be assessed together.
- Data spans more than one optimization domain.

## Do Not Use When
- The request is limited to one component; route to the specialized Skill.
- Required account/performance evidence is unavailable.

## Required Inputs
- Account/campaign configuration export.
- Performance data for a stated lookback period.
- Conversion definitions and primary business outcome.

## Optional Inputs
- Search-term report, keyword/ad assets, landing-page content.
- CRM-qualified lead or revenue data.
- Business targets such as CPA, ROAS, volume, or margin.

## Preconditions
1. Confirm date range, currency, account scope, campaign types, and data freshness.
2. Confirm whether conversion tracking and business outcomes are interpretable.
3. Mark missing evidence before applying optimization Rules.

## Knowledge Dependencies
- `knowledge/structure/account-structure.md`
- `knowledge/strategy/intent-framework.md`
- `knowledge/bidding/bidding-principles.md`
- `knowledge/measurement/conversion-framework.md`
- `knowledge/analytics/performance-diagnosis.md`

## Rule Dependencies
- Structure fragmentation and mixed-intent Rules.
- Bidding objective, target-change, and conversion-signal Rules.
- Search-term waste and expansion Rules.
- Conversion integrity and lead-quality Rules.
- Budget opportunity and scaling-risk Rules.
- Ad, PMax, and campaign-type Rules when applicable.

## Workflow
1. **Validate** scope, lookback, evidence coverage, and gaps.
2. **Gate measurement** before interpreting performance.
3. **Segment** by campaign, funnel stage, and optimization domain.
4. **Diagnose** with specialized Skill logic where applicable.
5. **Run Rules** through the canonical Rule Engine against normalized context.
6. **Classify** observation, inference, recommendation, and evidence gaps.
7. **Prioritize** by impact, urgency, confidence, and reversibility.
8. **Recommend** an ordered action plan without mutating the account.
9. **Measure** the metric/event that should confirm or reject each action.

## Rule Engine Contract
The consuming runtime normalizes account data into a context object and evaluates relevant Rules. `insufficient_evidence` results are reported as data gaps, never converted into conclusions.

```text
context.json → rule_engine → matched findings → priority/impact layer → audit output
```

## Decision Logic
- Measurement defects outrank optimization opportunities when they can invalidate interpretation.
- Critical/high-impact findings outrank cosmetic improvements.
- Low-confidence findings require validation steps.
- Never recommend a budget increase without checking conversion quality and scale constraints.
- Never recommend pausing from a single weak metric without sufficient sample/context.

## Output Contract
```markdown
# Account Audit
## Executive Summary
## Data Coverage
## Findings
| Priority | Domain | Observation | Inference | Impact | Confidence |
## Recommended Actions
### P0
### P1
### P2
## Measurement Plan
```
Every finding must carry evidence, impact, confidence, and a traceable Rule/Skill source when applicable.

## Confidence
- **High** — direct evidence satisfies Rule requirements and ambiguity is low.
- **Medium** — evidence is sufficient but context or causality is incomplete.
- **Low** — directional signal only; validation required.

## Safety
Read-only by default. Any campaign, budget, bid, keyword, ad, targeting, or conversion change requires human approval.

## Related Skills
`campaign-structure`, `conversion-tracking`, `search-term-analysis`, `bidding-strategy`, `budget-optimization`, `performance-diagnosis`, `landing-page-audit`, `pmax-optimization`

## Examples
Do not fabricate account results. Findings must reference actual input evidence or be labeled as evidence gaps.
