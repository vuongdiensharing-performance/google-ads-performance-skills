---
name: campaign-structure
version: 1.0.0
description: Design or review Google Ads campaign and ad-group structure for intent separation, budget control, and reporting clarity.
category: strategy
status: core
---

# Campaign Structure

## Purpose
Create or diagnose campaign architecture without unnecessary fragmentation.

## Use When
- Building a new account structure.
- Reviewing campaign segmentation, ad groups, or budget boundaries.

## Required Inputs
- Business goals, products/offers, geographies.
- Existing campaign structure when auditing.
- Budget and volume constraints.

## Knowledge Dependencies
- Account structure
- Intent framework
- Keyword intent

## Workflow
1. Map business lines and demand themes.
2. Separate materially different intent/budget/control requirements.
3. Choose campaign boundaries.
4. Design ad-group/theme structure.
5. Check for fragmentation and insufficient volume.
6. Define naming/reporting conventions.

## Decision Logic
Separate campaigns when budget, bidding, geography, objective, or reporting requirements materially differ. Avoid fragmentation that prevents useful learning.

## Output Contract
- Proposed/current structure
- Rationale per boundary
- Naming convention
- Risks
- Migration steps if restructuring

## Safety
No create/edit operation without approval.

## Related Skills
campaign-strategy, keyword-research, account-audit, bidding-strategy
