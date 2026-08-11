---
name: ad-copy
version: 1.1.0
description: Create and improve Google Search ad copy using intent, message match, differentiation, constraints, and testable variants.
category: creative
status: core
---
# Ad Copy
## Purpose
Produce evidence-led ad messaging aligned with search intent and landing-page value proposition.
## Use When
- Writing or refreshing Search ads.
- Creating test variants.
- Diagnosing weak relevance/message match.
## Do Not Use When
- Offer, proof, landing-page promise, or policy constraints are unknown.
## Required Inputs
Keyword/theme and intent, offer/value proposition, landing-page content/summary, brand/policy constraints.
## Preconditions
Separate verified claims from assumptions before generating copy.
## Knowledge Dependencies
- `knowledge/ads/rsa-message-match.md`
- `knowledge/keyword/keyword-intent.md`
## Rule Dependencies
- `rules/ad/excessive-pinning.yaml`
- `rules/ad/message-match-gap.yaml`
## Workflow
1. Identify intent and user promise.
2. Extract verified differentiators/proof.
3. Map message to landing-page experience.
4. Generate distinct variants.
5. Run ad Rules for message match and structural constraints.
6. Check claims, policy risk, redundancy, and evidence.
7. Define test hypothesis and measurement.
## Rule Engine Contract
Evaluate `ad_context` with canonical ad Rules. Rule findings become copy constraints/tests; never fabricate missing claims to satisfy them.
## Decision Logic
Message relevance and truthful differentiation precede keyword insertion or cosmetic optimization. Preserve meaningful variation for testing.
## Output Contract
- Ad variants
- Intent/message map
- Rule findings
- Differentiation rationale
- Test hypothesis
- Claim/policy risks
- Confidence
## Confidence
High when offer, proof, and page content are supplied; lower when inputs are incomplete.
## Safety
Do not invent product claims, prices, guarantees, certifications, or outcomes.
## Related Skills
`keyword-research`, `landing-page-audit`, `quality-score`, `campaign-strategy`
## Examples
Clearly label placeholders that require business confirmation.
