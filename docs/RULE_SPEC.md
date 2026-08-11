# Rule Specification v1

## Purpose

A Rule encodes a bounded decision condition: when evidence matches a defined pattern, produce a finding and an appropriate recommendation/action. Rules are not prose knowledge.

## Canonical schema

```yaml
id: KW-BROAD-001
name: Broad match without conversion-oriented Smart Bidding
version: 1.0.0
category: bidding

description: Identify broad-match usage that lacks an appropriate conversion-oriented bidding context.

when:
  match_type: broad
  bidding_strategy:
    not_in:
      - maximize_conversions
      - target_cpa
      - maximize_conversion_value
      - target_roas

exclude_when: []

evidence_required:
  - account_or_campaign_bidding_strategy
  - keyword_match_type

severity:
  level: high

confidence:
  level: high

finding:
  title: Broad match without conversion-oriented Smart Bidding

recommendation:
  - review_bidding_strategy
  - verify_conversion_volume_and_quality

impact:
  dimensions:
    - efficiency
    - wasted_spend
  level: high

action:
  type: investigate

human_approval_required: false

related_skills:
  - keyword-research
  - bidding-strategy
```

## Rule requirements

Every Rule must define:

- unique `id`;
- category;
- condition/evidence logic;
- exclusions where false positives are likely;
- severity;
- confidence;
- finding;
- recommendation;
- impact;
- action type;
- human-approval behavior where an account mutation is possible.

## Evidence first

Rules must not rely on arbitrary thresholds without documenting the rationale, minimum sample, lookback period, or contextual assumptions. A rule may return `insufficient_evidence` rather than force a conclusion.

## Severity vs priority

- Severity = how serious the underlying issue/opportunity is.
- Priority = how urgently it should be addressed relative to other findings.

Priority is assigned by the consuming Skill using impact, evidence, business context, and dependencies; it is not automatically identical to severity.

## Actions

Supported action intents:

- `investigate`
- `recommend`
- `prepare`
- `pause`
- `increase`
- `decrease`
- `change`

Mutation actions require human approval by default.

## Rule quality gates

A Rule is valid when it is testable, evidence-bound, explicit about false positives, and does not present an industry heuristic as an immutable Google Ads platform rule.
