# Rules

Evidence-based decision rules live here. Every rule must follow `docs/RULE_SPEC.md`.

## V1 rule families

### Search terms
- `search-term/irrelevant-intent.yaml`
- `search-term/high-spend-zero-conversion.yaml`
- `search-term/expansion-candidate.yaml`

### Keywords
- `keyword/broad-without-smart-bidding.yaml`
- `keyword/intent-theme-mismatch.yaml`
- `keyword/low-quality-score-investigation.yaml`

### Bidding
- `bidding/objective-strategy-mismatch.yaml`
- `bidding/frequent-target-changes.yaml`
- `bidding/conversion-signal-risk.yaml`

### Conversion
- `conversion/primary-micro-conversion.yaml`
- `conversion/tracking-integrity-risk.yaml`
- `conversion/lead-quality-gap.yaml`

### Budget
- `budget/budget-constraint-opportunity.yaml`
- `budget/scale-with-quality-risk.yaml`

### Structure
- `structure/fragmentation-risk.yaml`
- `structure/mixed-intent-campaign.yaml`

### Ads
- `ad/excessive-pinning.yaml`
- `ad/message-match-gap.yaml`

### Performance Max
- `pmax/primary-goal-missing.yaml`
- `pmax/recent-change-learning.yaml`
- `pmax/overrestrictive-negative.yaml`

## Rule safety

Rules do not execute account changes by default. Recommendations involving budget, bidding, exclusions, campaign changes, or other material account changes require human approval.

Rules must explicitly account for insufficient evidence, conversion lag, tracking integrity, and false-positive risk.
