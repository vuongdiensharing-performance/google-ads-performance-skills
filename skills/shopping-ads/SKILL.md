---
name: shopping-ads
version: 1.1.0
description: Plan, audit, and optimize Google Shopping around feed quality, product segmentation, bidding, budget, and commercial economics.
category: campaign-type
status: core
---
# Shopping Ads
## Purpose
Diagnose Shopping performance across product data, structure, bidding, budget, landing-page alignment, and commercial value.
## Use When
- Launching or auditing Shopping.
- Product-level performance needs investigation.
## Do Not Use When
- Product/feed evidence is absent.
## Required Inputs
Product/feed data, campaign structure, spend, clicks, conversions/value, commercial value or margins where available.
## Optional Inputs
Feed diagnostics, product categories, search/category evidence, inventory constraints.
## Preconditions
Validate product eligibility/data quality and define the business value metric.
## Knowledge Dependencies
- `knowledge/pmax/pmax-principles.md`
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/pmax/primary-goal-missing.yaml`
- `rules/budget/budget-constraint-opportunity.yaml`
## Workflow
1. Validate feed/product data.
2. Segment products by commercial value and performance.
3. Review campaign structure, budget, and bidding.
4. Run applicable Rules.
5. Identify waste and scale candidates.
6. Check product/landing-page alignment.
7. Recommend changes and measurement.
## Rule Engine Contract
Evaluate normalized `shopping_context`; do not infer profitability without business-value evidence.
## Decision Logic
Optimize toward qualified commercial outcomes, not clicks or product volume alone. Treat feed quality as both a delivery constraint and a diagnostic input.
## Output Contract
- Feed/data findings
- Product segmentation
- Rule findings
- Campaign/bidding recommendations
- Commercial impact considerations
- Measurement plan
- Confidence
## Confidence
High for observed feed/performance facts; lower when margin or inventory evidence is missing.
## Safety
Product/feed/campaign changes require approval. Do not infer profitability without evidence.
## Related Skills
`budget-optimization`, `bidding-strategy`, `landing-page-audit`, `performance-diagnosis`
## Examples
Label revenue-based conclusions separately from margin/profitability conclusions.
