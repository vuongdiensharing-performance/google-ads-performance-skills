---
name: account-audit
version: 1.0.0
description: Audit a Google Ads account across structure, bidding, keywords, ads, measurement, budget, targeting, and landing pages.
category: audit
status: core
---

# Account Audit

## Purpose
Produce a prioritized account health assessment from available Google Ads data and configuration evidence.

## Use When
- A user asks for a Google Ads account audit.
- Multiple campaign-level issues must be assessed together.

## Do Not Use When
- Only one isolated component needs analysis; use the specialized Skill.

## Required Inputs
- Account/campaign configuration or export.
- Relevant performance data for the requested lookback period.

## Knowledge Dependencies
- Account structure
- Intent framework
- Bidding principles
- Measurement framework

## Rule Dependencies
- Structure rules
- Bidding rules
- Keyword/search-term rules
- Conversion and budget rules

## Workflow
1. Validate data coverage and date range.
2. Check measurement integrity before interpreting performance.
3. Audit structure, targeting, bidding, keywords, ads, budget, and landing-page signals.
4. Apply relevant Rules and suppress findings lacking evidence.
5. Prioritize by business impact and urgency.
6. Produce an action plan and measurement plan.

## Output Contract
- Executive summary
- Data coverage/gaps
- Findings with evidence, impact, severity, priority, confidence
- Recommended actions
- Measurement/validation plan

## Safety
Read-only by default. No account mutation without human approval.

## Related Skills
campaign-structure, bidding-strategy, conversion-tracking, performance-diagnosis, landing-page-audit
