---
id: match-types
version: 1.0.0
type: reference
category: keyword
authority: google-first-party
status: stable
---

# Keyword Match Types

## Current platform model

Google Ads Search supports exact, phrase, and broad match keywords. Match behavior is not a simple literal string filter; the platform uses meaning and other signals to determine eligibility.

## Guidance

- Treat match type as a traffic-control input, not a guarantee of query intent.
- Use search-term data to validate actual traffic.
- Broad match should be evaluated together with conversion-based Smart Bidding, conversion quality, query controls, and sufficient evidence.
- Exact and phrase should not be assumed to provide perfect literal isolation.
- Negative keywords use different matching behavior from positive keywords and should be reviewed separately.

## Important 2026 note

Google states that its campaign-level broad-match setting requires conversion-based Smart Bidding and that changes related to AI Max are being introduced in 2026. Do not hard-code future rollout behavior into rules without checking current Google documentation.

## Sources

- https://support.google.com/google-ads/answer/13389795
- https://support.google.com/google-ads/answer/2453972

## Related skills

- keyword-research
- search-term-analysis
- negative-keyword-mining
- bidding-strategy
