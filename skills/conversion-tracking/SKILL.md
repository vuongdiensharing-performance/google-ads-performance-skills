---
name: conversion-tracking
version: 1.0.0
description: Audit Google Ads conversion measurement for correctness, business relevance, attribution, and data quality.
category: measurement
status: core
---
# Conversion Tracking
## Purpose
Ensure optimization decisions are based on trustworthy conversion signals.
## Use When
- Auditing conversion setup.
- Investigating sudden performance changes.
- Choosing primary versus secondary conversion actions.
## Required Inputs
Conversion actions, definitions, source/platform configuration, attribution settings, volumes, and CRM outcomes where available.
## Workflow
1. Inventory conversion actions.
2. Map each action to business value.
3. Check duplication, firing, attribution, and data gaps.
4. Compare platform conversions with downstream/CRM evidence.
5. Identify optimization-signal risks.
6. Recommend fixes and validation tests.
## Output Contract
Measurement map, issues, evidence, business-impact assessment, fixes, validation plan, confidence.
## Safety
Never declare tracking correct solely because conversions are being recorded.
## Related Skills
account-audit, performance-diagnosis, landing-page-audit, bidding-strategy
