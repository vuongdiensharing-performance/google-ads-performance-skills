---
name: negative-keyword-mining
version: 1.2.0
description: Identify, classify, and prioritize negative keyword candidates from search-term evidence and business relevance.
category: acquisition
status: core
knowledge_dependencies:
  - knowledge/keyword/keyword-intent.md
  - knowledge/keyword/match-types.md
  - knowledge/search/search-term-methodology.md
rule_dependencies:
  - rules/search-term/irrelevant-intent.yaml
  - rules/search-term/high-spend-zero-conversion.yaml
---
# Negative Keyword Mining
## Purpose
Reduce irrelevant or economically harmful demand while protecting valuable intent.
## Use When
- Search-term analysis reveals irrelevant or low-value patterns.
- Systematic negative maintenance is required.
## Do Not Use When
- There is no query evidence or business relevance definition.
## Required Inputs
Search terms plus business relevance criteria and conversion-quality definitions where available.
## Preconditions
Define what counts as irrelevant, commercially harmful, ambiguous, or protected intent.
## Knowledge Dependencies
- `knowledge/keyword/keyword-intent.md`
- `knowledge/keyword/match-types.md`
- `knowledge/search/search-term-methodology.md`
## Rule Dependencies
- `rules/search-term/irrelevant-intent.yaml`
- `rules/search-term/high-spend-zero-conversion.yaml`
## Workflow
1. Classify relevance.
2. Run canonical search-term Rules.
3. Separate clearly irrelevant from ambiguous candidates.
4. Check conversion/business-value evidence.
5. Recommend negative scope and match behavior.
6. Identify false-positive risk.
7. Produce approval-ready list and validation plan.
## Rule Engine Contract
A Rule match creates a candidate, not an automatic negative. `insufficient_evidence` and ambiguous cases stay in review.
## Decision Logic
Protect high-value or strategically important intent even when short-term efficiency is weak. Prefer evidence-backed patterns over one-off guesses.
## Output Contract
- Candidate term/pattern
- Rule/evidence trace
- Reason
- Scope recommendation
- False-positive risk
- Confidence
- Approval status
## Confidence
High for clearly irrelevant terms with direct evidence; Medium for economic-risk candidates; Low for ambiguous patterns.
## Safety
Never auto-apply negatives. Human approval is required.
## Related Skills
`search-term-analysis`, `keyword-research`, `account-audit`
## Examples
Do not recommend blocking a broad semantic class when only one query is irrelevant unless evidence supports the broader pattern.
