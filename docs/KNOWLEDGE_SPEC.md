# Knowledge Specification v1

## Purpose

Knowledge assets define reusable domain truth, principles, frameworks, references, benchmarks, and methodologies. They inform Skills and Rules but do not perform workflows by themselves.

## Canonical frontmatter

```yaml
---
id: intent-framework
version: 1.0.0
type: framework
category: strategy
authority: methodology
status: stable
---
```

## Knowledge types

- `principle` — durable operating principle.
- `framework` — structured model for thinking or planning.
- `reference` — factual platform/domain reference.
- `benchmark` — contextual benchmark methodology; never universal truth unless explicitly sourced.
- `methodology` — repeatable analytical approach.

## Required sections

1. Title
2. Principle/definition
3. Definitions where needed
4. Framework or method
5. Decision guidance
6. Exceptions
7. Anti-patterns
8. Examples
9. Related knowledge
10. Related skills

## Authority hierarchy

1. Official Google/platform documentation.
2. Verified first-party/platform data.
3. Validated repository methodology.
4. Industry best practice.
5. Source repositories.
6. Model inference.

When authorities conflict, the higher-authority source wins.

## Evidence language

Use explicit labels where useful:

- `Platform fact`
- `Validated methodology`
- `Industry heuristic`
- `Hypothesis`

Do not convert a heuristic into a platform fact.

## Benchmark rules

Benchmarks must state their context, metric definition, sample/window assumptions, and limitations. Avoid universal claims such as “good CTR is X%” without context.

## Knowledge quality gates

Knowledge is valid when it is scoped, attributable where necessary, internally consistent, and clear about exceptions and uncertainty.
