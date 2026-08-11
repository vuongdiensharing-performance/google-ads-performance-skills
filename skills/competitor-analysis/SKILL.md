---
name: competitor-analysis
version: 1.1.1
description: Analyze observable competitor positioning, search presence, messaging, and auction context to inform Google Ads strategy.
category: strategy
status: core
---
# Competitor Analysis
## Purpose
Turn observable competitor signals into strategic hypotheses without treating competitor data as complete market truth.
## Use When
- Evaluating competitor positioning.
- Planning competitor keyword coverage or differentiation.
- Interpreting auction/market signals.
## Do Not Use When
- The competitor set or observable evidence is undefined.
## Required Inputs
Market, offer, geography, competitor set, and available search/auction/creative evidence.
## Preconditions
Separate observed competitor facts from inferred strategy.
## Knowledge Dependencies
- `knowledge/strategy/intent-framework.md`
- `knowledge/keyword/keyword-intent.md`
## Rule Dependencies
- `rules/structure/mixed-intent-campaign.yaml`
## Workflow
1. Define competitor set and dimensions.
2. Collect observable signals.
3. Normalize evidence and timestamps.
4. Separate facts from inference.
5. Run relevant strategy Rules.
6. Identify positioning gaps and risks.
7. Translate into keyword/message/landing-page hypotheses and tests.
## Rule Engine Contract
Rules may flag strategy/structure implications from the observed context; they cannot establish competitor internal economics or intent.
## Decision Logic
Use competitor evidence to form hypotheses, not to copy blindly. Time-bound observations because auctions and messaging change.
## Output Contract
- Competitor map
- Evidence/source/time context
- Rule findings
- Strategic implications
- Hypotheses/tests
- Risks
- Confidence
## Confidence
High for directly observed facts; Medium for interpretation; Low for inferred internal strategy.
## Safety
Do not invent competitor spend, conversion rate, profitability, or internal strategy. Any campaign, keyword, ad, or budget change based on competitor analysis requires explicit human approval before execution.
## Related Skills
`campaign-strategy`, `keyword-research`, `ad-copy`, `landing-page-audit`
## Examples
Never state a competitor's bid, budget, or CPA unless directly evidenced by an authoritative source.
