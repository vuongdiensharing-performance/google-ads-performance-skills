---
name: conversion-tracking
version: 1.1.0
description: Audit Google Ads conversion measurement for correctness, business relevance, attribution, and data quality.
category: measurement
status: core
---
# Conversion Tracking
## Purpose
Establish whether optimization decisions can rely on the configured conversion signals.
## Use When
- Auditing conversion setup.
- Investigating sudden performance changes.
- Choosing primary versus secondary conversion actions.
## Do Not Use When
- Configuration/data evidence is unavailable; request it rather than infer tracking health.
## Required Inputs
Conversion actions, definitions, source/platform configuration, attribution settings, volumes, and CRM outcomes where available.
## Optional Inputs
Tag/GTM/GA4 evidence, deduplication evidence, consent/diagnostic signals, offline conversion logs.
## Preconditions
Inventory every conversion action and map it to a business outcome before judging optimization suitability.
## Knowledge Dependencies
- `knowledge/measurement/conversion-framework.md`
## Rule Dependencies
- `rules/conversion/primary-micro-conversion.yaml`
- `rules/conversion/tracking-integrity-risk.yaml`
- `rules/conversion/lead-quality-gap.yaml`
## Workflow
1. Inventory conversion actions.
2. Map each to business value and funnel role.
3. Run integrity/primary-signal Rules.
4. Check duplication, firing, attribution, and data gaps.
5. Compare platform conversions with downstream/CRM evidence.
6. Identify optimization-signal risks.
7. Recommend fixes and validation tests.
## Rule Engine Contract
Evaluate normalized `conversion_context`; preserve insufficient evidence and distinguish configuration defects from business-quality gaps.
## Decision Logic
Recorded conversions do not prove correct tracking. A technically firing event can still be the wrong optimization signal.
## Output Contract
- Measurement map
- Rule findings
- Integrity issues
- Business-impact assessment
- Optimization-signal assessment
- Fixes
- Validation plan
- Confidence
## Confidence
High for directly verified configuration/firing evidence; Medium when downstream reconciliation is partial; Low when instrumentation cannot be inspected.
## Safety
Never change conversion settings automatically. Human approval is required for measurement mutations.
## Related Skills
`account-audit`, `performance-diagnosis`, `landing-page-audit`, `bidding-strategy`
## Examples
State exactly which layer is verified: configuration, event firing, platform receipt, or downstream business quality.
