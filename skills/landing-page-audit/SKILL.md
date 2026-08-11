---
name: landing-page-audit
version: 1.1.1
description: Audit landing pages for message match, relevance, trust, usability, conversion friction, and measurement readiness.
category: conversion
status: core
---
# Landing Page Audit
## Purpose
Determine whether the post-click experience supports promised intent and qualified conversion.
## Use When
- Search/campaign performance suggests post-click friction.
- Reviewing a page before launch or optimization.
## Do Not Use When
- Page content/URL and ad/keyword intent are unavailable.
## Required Inputs
Landing-page URL/content plus ad/keyword intent. Performance/conversion-quality data when available.
## Preconditions
Use actual page content or supplied evidence; never infer technical metrics from appearance alone.
## Knowledge Dependencies
- `knowledge/ads/rsa-message-match.md`
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/ad/message-match-gap.yaml`
- `rules/conversion/tracking-integrity-risk.yaml`
## Workflow
1. Map keyword → ad promise → page content.
2. Check relevance and clarity.
3. Review proof, trust, CTA, friction, mobile/usability evidence.
4. Run message-match and tracking Rules.
5. Prioritize fixes by business impact and confidence.
6. Define tests and measurement.
## Rule Engine Contract
Evaluate `landing_page_context` with applicable Rules. Missing technical evidence remains a data gap.
## Decision Logic
Prioritize issues that can block qualified users or break measurement. Do not equate visual quality with conversion performance.
## Output Contract
- Message-match assessment
- Rule findings
- UX/conversion findings
- Evidence and limitations
- Priority fixes
- Test ideas
- Tracking gaps
## Confidence
High for directly observable content; Medium/Low for technical or causal claims without measurement.
## Safety
Do not claim page-speed, Core Web Vitals, or technical metrics without measured evidence. Recommendations that change the live page, tracking, or campaign configuration require explicit human approval before execution.
## Related Skills
`ad-copy`, `conversion-tracking`, `quality-score`, `performance-diagnosis`
## Examples
Use explicit evidence labels for observations made from page content versus performance data.
