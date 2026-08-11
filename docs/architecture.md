# Architecture

The repository separates four concerns:

```text
Knowledge → explains what is true
Rules     → encode evidence-based decisions
Skills    → execute bounded workflows
Templates → standardize outputs
```

## Runtime flow

```text
User request
   ↓
Skill selection
   ↓
Input validation
   ↓
Knowledge + Rules
   ↓
Analysis / diagnosis
   ↓
Evidence-backed recommendation
   ↓
Output contract
   ↓
Human approval for mutations
```

## Design goals

- Model agnostic.
- Gemini friendly.
- Read-only by default.
- Evidence before conclusions.
- Business outcomes before vanity metrics.
- Reusable Rules and Knowledge across Skills.

## Source lineage

The initial Google Ads domain coverage is synthesized from the referenced `ads-skills` and `agent-skills` repositories. Source lineage informs design; it does not override official platform documentation or verified evidence.
