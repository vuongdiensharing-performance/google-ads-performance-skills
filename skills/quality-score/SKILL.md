---
name: quality-score
version: 1.2.0
description: Diagnose Quality Score and component signals as relevance diagnostics while protecting qualified business outcomes.
category: optimization
status: core
knowledge_dependencies:
  - knowledge/keyword/match-types.md
  - knowledge/ads/rsa-message-match.md
  - knowledge/analytics/performance-diagnosis.md
rule_dependencies:
  - rules/keyword/low-quality-score-investigation.yaml
  - rules/ad/message-match-gap.yaml
---
# Quality Score
## Purpose
Use Quality Score/components to identify relevance and experience hypotheses, not as a standalone business KPI.
## Use When
- Quality Score or components are under review.
- Search efficiency may relate to relevance or landing-page experience.
## Do Not Use When
- The user has no keyword/component evidence; request it rather than infer.
## Required Inputs
Keyword-level Quality Score/components where available, ad relevance, expected CTR/context, landing-page experience, performance data.
## Preconditions
Segment by meaningful theme and confirm the business KPI being protected.
## Knowledge Dependencies
- `knowledge/keyword/match-types.md`
- `knowledge/ads/rsa-message-match.md`
- `knowledge/analytics/performance-diagnosis.md`
## Rule Dependencies
- `rules/keyword/low-quality-score-investigation.yaml`
- `rules/ad/message-match-gap.yaml`
## Workflow
1. Validate component evidence.
2. Segment keywords/themes.
3. Run Quality Score/message-match Rules.
4. Separate diagnostic symptoms from business outcomes.
5. Form root-cause hypotheses.
6. Recommend controlled ad/keyword/landing-page tests.
7. Define measurement beyond Quality Score.
## Rule Engine Contract
Rule matches are diagnostic leads; the Skill must connect them to CTR, qualified conversions, CPA/ROAS, or other business evidence before prioritization.
## Decision Logic
Do not optimize Quality Score at the expense of qualified conversions, revenue, or useful query coverage.
## Output Contract
- Component diagnosis
- Rule findings
- Root-cause hypotheses
- Evidence
- Recommended tests
- Business KPI measurement
- Confidence
## Confidence
High for directly reported component data; Medium/Low for inferred causes.
## Safety
No account changes without approval.
## Related Skills
`keyword-research`, `ad-copy`, `landing-page-audit`, `performance-diagnosis`
## Examples
Never claim that improving Quality Score will produce a specific CPA/ROAS change without evidence.
