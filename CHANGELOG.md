# Changelog

## 2026-08-11 — Phase 3B

### Added

- Populated V1 Knowledge layer with 11 canonical assets covering strategy, structure, keyword intent/match types, bidding, conversion measurement, search terms, RSA/message match, Performance Max, B2B lead generation, and performance diagnosis.
- Added 21 reusable evidence-gated Rules across search terms, keywords, bidding, conversion, budget, structure, ads, and Performance Max.
- Connected the 18 Core Skills to Knowledge and Rule dependencies in `docs/SKILL_REGISTRY.md`.
- Updated Knowledge and Rule indexes.

### Design decisions

- Google first-party documentation is the preferred authority for platform behavior.
- Rules require evidence and explicitly account for false positives, insufficient data, conversion lag, or tracking integrity where relevant.
- Material account changes remain human-approval actions by default.
- Thresholds are contextual rather than universal unless explicitly supported by authoritative documentation.
