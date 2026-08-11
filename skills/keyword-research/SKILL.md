---
name: keyword-research
version: 1.2.1
description: Research and organize Google Ads keywords by intent, theme, match strategy, opportunity, and exclusions.
category: acquisition
status: core
knowledge_dependencies:
  - knowledge/keyword/keyword-intent.md
  - knowledge/keyword/match-types.md
  - knowledge/strategy/intent-framework.md
rule_dependencies:
  - rules/keyword/intent-theme-mismatch.yaml
  - rules/keyword/broad-without-smart-bidding.yaml
---
# Keyword Research
## Purpose
Turn business/product language and demand signals into an intent-led, testable keyword set.
## Use When
- Building Search coverage.
- Expanding proven themes.
- Reworking keyword architecture.
## Do Not Use When
- Existing search-term evidence is the primary input; use `search-term-analysis`.
## Required Inputs
Offer/product/service context, seed terms or landing pages, geography, language.
## Optional Inputs
Search terms, competitor evidence, Keyword Planner exports, CRM outcomes.
## Preconditions
Define business-relevant intent classes and exclusion criteria before expansion.
## Knowledge Dependencies
- `knowledge/keyword/keyword-intent.md`
- `knowledge/keyword/match-types.md`
- `knowledge/strategy/intent-framework.md`
## Rule Dependencies
- `rules/keyword/intent-theme-mismatch.yaml`
- `rules/keyword/broad-without-smart-bidding.yaml`
## Workflow
1. Build seed themes.
2. Expand semantic/problem-aware variants.
3. Classify intent.
4. Deduplicate and normalize.
5. Map themes to campaign/ad-group boundaries.
6. Recommend match strategy.
7. Run intent/match Rules.
8. Generate negative candidates and gaps.
## Rule Engine Contract
Evaluate keyword candidates against normalized `keyword_context`; Rules provide flags and recommendations, never automatic additions.
## Decision Logic
Intent relevance precedes search volume. Match type is a control choice, not a proxy for keyword quality. Do not reject a theme solely because volume is unknown.
## Output Contract
- Keyword clusters
- Intent classification
- Match recommendation
- Campaign/ad-group mapping
- Rule findings
- Negative candidates
- Gaps/assumptions
## Confidence
High for terms supported by direct business/search evidence; Medium for semantic expansion; Low for speculative themes.
## Safety
Research/recommendation only. Keyword changes require approval.
## Related Skills
`campaign-structure`, `search-term-analysis`, `negative-keyword-mining`, `ad-copy`, `bidding-strategy`
## Examples
Clearly label generated ideas versus evidence-backed keywords.
