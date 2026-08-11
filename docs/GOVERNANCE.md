# Governance

## Purpose

Governance protects the quality, provenance, safety, and reproducibility of the Google Ads Performance Skills system.

## Source-of-truth hierarchy

When claims conflict, prefer evidence in this order:

1. Google official documentation and first-party product behavior.
2. Verified first-party account or experiment data.
3. Validated methodology with explicit evidence.
4. Industry best practice with stated scope and limitations.
5. Community or source-repository material.
6. LLM inference.

Lower-level sources must not silently override higher-authority evidence.

## Asset ownership

### Knowledge

Knowledge describes principles, frameworks, methodologies, references, or benchmarks. It should explain what is believed to be true and under what conditions.

### Rules

Rules translate evidence into deterministic conditions, exclusions, findings, and recommendations. A Rule should not hide an unsupported assumption behind an arbitrary threshold.

### Skills

Skills orchestrate Knowledge and Rules into a workflow and output contract. They should not duplicate large bodies of domain knowledge unnecessarily.

### Evaluations

Fixtures and golden benchmarks define expected behavior. Changes to Skills, Rules, or Knowledge that affect behavior must update evaluation coverage.

## Change control

A production intelligence change should follow:

```text
Proposal
  -> evidence review
  -> specification check
  -> implementation
  -> fixture update
  -> CI validation
  -> review
  -> merge
```

Breaking changes to the Skill, Rule, Knowledge, or evaluation contracts require explicit documentation in `CHANGELOG.md` and the relevant specification.

## Versioning

Use semantic intent for behavior changes:

- patch: wording, documentation, or non-behavioral corrections;
- minor: backward-compatible Skill/Rule/Knowledge additions;
- major: breaking changes to contracts, schemas, or expected behavior.

## Review principles

Reviewers should ask:

- Is the claim supported by appropriate evidence?
- Is the Rule deterministic and appropriately scoped?
- Are exclusions and false positives covered?
- Is insufficient evidence handled safely?
- Does the Skill preserve its output and safety contract?
- Are fixtures representative?
- Could the change cause an unsafe or surprising advertising action?

## Execution boundary

This repository may recommend account changes, but recommendation and execution remain separate concerns. Any future API integration must preserve explicit Human Approval and least-privilege access.

## Maintainer discretion

Maintainers may reject changes that are technically functional but weaken evidence quality, evaluation reliability, security, or execution safety.
