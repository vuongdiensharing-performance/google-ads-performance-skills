---
name: negative-keyword-mining
version: 1.0.0
description: Identify, classify, and prioritize negative keyword candidates from search-term evidence and business relevance.
category: acquisition
status: core
---

# Negative Keyword Mining

## Purpose
Reduce irrelevant or economically harmful search demand while protecting valuable intent.

## Use When
- Search-term analysis reveals irrelevant or low-value patterns.
- The account needs systematic negative-keyword maintenance.

## Required Inputs
Search terms plus business relevance criteria and conversion-quality definitions where available.

## Knowledge Dependencies
- Negative keywords
- Keyword intent
- Match types

## Workflow
1. Classify query relevance.
2. Separate clearly irrelevant from uncertain terms.
3. Check conversion evidence and business value.
4. Recommend negative scope: campaign, ad group, or account.
5. Flag potential false-positive risks.

## Output Contract
- Candidate term/pattern
- Reason
- Scope recommendation
- Evidence
- Risk of blocking valuable demand
- Confidence

## Safety
Never auto-apply negatives. Preserve potentially valuable ambiguous intent for review.

## Related Skills
search-term-analysis, keyword-research, account-audit
