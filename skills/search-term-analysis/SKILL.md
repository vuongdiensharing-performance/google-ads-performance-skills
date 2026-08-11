---
name: search-term-analysis
version: 1.0.0
description: Analyze Google Ads search terms to identify intent, wasted spend, negative candidates, winners, and expansion opportunities.
category: analytics
status: core
---

# Search Term Analysis

## Purpose
Convert search-term performance into evidence-based exclusions and expansion decisions.

## Use When
- Reviewing Search query/search-term reports.
- Investigating wasted spend or irrelevant traffic.
- Finding new high-intent keyword opportunities.

## Required Inputs
Search-term data with at least query, campaign/ad group, spend, clicks, conversions, and conversion value where available.

## Knowledge Dependencies
- Search terms and negatives
- Keyword intent
- Conversion methodology

## Rule Dependencies
Search-term relevance, spend-without-conversion, intent, and expansion rules.

## Workflow
1. Validate date range, attribution, and conversion definitions.
2. Classify query intent and relevance.
3. Segment by spend, clicks, conversions, and business quality.
4. Identify negative candidates.
5. Identify winners and expansion candidates.
6. Prioritize actions by impact and evidence.

## Output Contract
- Waste findings
- Negative candidates with rationale
- Expansion candidates
- Evidence table
- Priority and confidence
- Measurement follow-up

## Safety
Do not add negatives automatically; require approval.

## Related Skills
keyword-research, negative-keyword-mining, performance-diagnosis
