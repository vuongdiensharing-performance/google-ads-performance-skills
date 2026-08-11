---
name: account-audit
version: 1.2.0
description: Run a read-only, evidence-gated Google Ads account health audit and turn findings into a prioritized action plan.
category: audit
status: core
knowledge_dependencies:
  - knowledge/structure/account-structure.md
  - knowledge/strategy/intent-framework.md
  - knowledge/bidding/bidding-principles.md
  - knowledge/measurement/conversion-framework.md
  - knowledge/analytics/performance-diagnosis.md
rule_dependencies:
  - rules/structure/fragmentation-risk.yaml
  - rules/structure/mixed-intent-campaign.yaml
  - rules/bidding/objective-strategy-mismatch.yaml
  - rules/bidding/frequent-target-changes.yaml
  - rules/bidding/conversion-signal-risk.yaml
  - rules/search-term/irrelevant-intent.yaml
  - rules/search-term/high-spend-zero-conversion.yaml
  - rules/search-term/expansion-candidate.yaml
  - rules/conversion/tracking-integrity-risk.yaml
  - rules/conversion/lead-quality-gap.yaml
  - rules/budget/budget-constraint-opportunity.yaml
  - rules/budget/scale-with-quality-risk.yaml
conditional_rule_dependencies:
  - when: search_ads_or_ad_assets_present
    rules:
      - rules/ad/excessive-pinning.yaml
      - rules/ad/message-match-gap.yaml
  - when: pmax_or_shopping_campaign_present
    rules:
      - rules/pmax/primary-goal-missing.yaml
      - rules/pmax/recent-change-learning.yaml
      - rules/pmax/overrestrictive-negative.yaml
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
- `rules/structure/fragmentation-risk.yaml`
- `rules/structure/mixed-intent-campaign.yaml`
- `rules/bidding/objective-strategy-mismatch.yaml`
- `rules/bidding/frequent-target-changes.yaml`
- `rules/bidding/conversion-signal-risk.yaml`
- `rules/search-term/irrelevant-intent.yaml`
- `rules/search-term/high-spend-zero-conversion.yaml`
- `rules/search-term/expansion-candidate.yaml`
- `rules/conversion/tracking-integrity-risk.yaml`
- `rules/conversion/lead-quality-gap.yaml`
- `rules/budget/budget-constraint-opportunity.yaml`
- `rules/budget/scale-with-quality-risk.yaml`

### Conditional Rule Dependencies
- When Search ads or ad assets are present:
  - `rules/ad/excessive-pinning.yaml`
  - `rules/ad/message-match-gap.yaml`
- When PMax or Shopping campaigns are present:
  - `rules/pmax/primary-goal-missing.yaml`
  - `rules/pmax/recent-change-learning.yaml`
  - `rules/pmax/overrestrictive-negative.yaml`

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
