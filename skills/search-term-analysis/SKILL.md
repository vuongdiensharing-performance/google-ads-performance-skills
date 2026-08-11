---
name: search-term-analysis
version: 1.1.0
description: Analyze Google Ads search terms to identify intent, wasted spend, negative candidates, winners, and expansion opportunities.
category: analytics
status: core
---
# Search Term Analysis
## Purpose
Convert query-level evidence into qualified exclusion, expansion, and optimization decisions.
## Use When
- Reviewing Search term/query reports.
- Investigating wasted spend or irrelevant traffic.
- Finding new high-intent opportunities.
## Do Not Use When
- Search-term evidence is absent; request it instead of inferring queries.
## Required Inputs
Query, campaign/ad group, spend, clicks, conversions, and value where available; business relevance definition.
## Optional Inputs
CRM quality, search category, keyword, device, geography, margin/value.
## Preconditions
Confirm lookback, attribution, conversion definition, and whether data is sufficiently mature.
## Knowledge Dependencies
- `knowledge/search/search-term-methodology.md`
- `knowledge/keyword/keyword-intent.md`
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/search-term/irrelevant-intent.yaml`
- `rules/search-term/high-spend-zero-conversion.yaml`
- `rules/search-term/expansion-candidate.yaml`
## Workflow
1. Validate data and business outcome.
2. Classify query intent/relevance.
3. Segment by spend, clicks, conversions, and quality.
4. Run search-term Rules.
5. Separate waste, ambiguous terms, winners, and expansion candidates.
6. Score impact and confidence.
7. Produce approved-scope recommendations and measurement follow-up.
## Rule Engine Contract
Use the canonical Rule Engine on each normalized query context. Preserve `insufficient_evidence` and ambiguous matches for review.
## Decision Logic
A non-converting query is not automatically waste. Consider spend, sample, intent, conversion lag, and business quality before exclusion.
## Output Contract
- Evidence summary
- Waste findings
- Negative candidates with rationale/scope
- Expansion candidates
- Rule trace
- Priority/confidence
- Measurement follow-up
## Confidence
High only when relevance and performance evidence are direct and sufficient; Medium/Low otherwise.
## Safety
Do not add negatives automatically; require approval and check false-positive risk.
## Related Skills
`keyword-research`, `negative-keyword-mining`, `performance-diagnosis`, `account-audit`
## Examples
Never fabricate search queries or conversion results when a report is not supplied.
