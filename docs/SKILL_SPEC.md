# Skill Specification v1

## Purpose

A Skill is a bounded, reusable workflow that transforms defined inputs into a structured output. A Skill is not a knowledge dump and must not contain undocumented platform claims as hard-coded truth.

## Canonical frontmatter

```yaml
---
name: search-term-analysis
version: 1.0.0
description: Analyze Google Ads search terms for intent, waste, negatives, and expansion opportunities.
category: analytics
status: stable
---
```

## Required sections

1. `# <Skill Name>`
2. `## Purpose`
3. `## Use When`
4. `## Do Not Use When`
5. `## Required Inputs`
6. `## Optional Inputs`
7. `## Preconditions`
8. `## Knowledge Dependencies`
9. `## Rule Dependencies`
10. `## Workflow`
11. `## Decision Logic`
12. `## Output Contract`
13. `## Confidence`
14. `## Safety`
15. `## Related Skills`
16. `## Examples`

## Workflow standard

Use the smallest workflow that is sufficient:

`Validate → Segment → Diagnose → Classify → Prioritize → Recommend → Measure`

Not every Skill needs every stage, but missing stages must be intentional.

## Evidence discipline

A Skill must never invent account data. If required evidence is absent, it must request the missing input or explicitly downgrade the conclusion.

## Diagnostic output

Diagnostic Skills should separate:

- Observation — directly supported by data.
- Inference — interpretation of the evidence.
- Recommendation — proposed action.
- Confidence — high, medium, or low.

## Safety

Read/analyze/recommend/prepare are allowed by default. Changes to campaigns, budgets, bids, keywords, ads, targeting, conversion settings, or other account state require human approval unless a consuming system explicitly grants execution authority.

## Quality gates

A Skill is valid when:

- frontmatter is complete;
- inputs and preconditions are explicit;
- dependencies are named;
- workflow is actionable;
- output is deterministic enough to consume;
- safety behavior is explicit;
- examples do not fabricate real account results.
