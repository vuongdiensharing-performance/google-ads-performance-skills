# Validation & Evaluation Specification v1

## Purpose

Define a repeatable evaluation framework for Google Ads Skills before model or API integration.

## Test classes

Every Core Skill should have fixtures for four canonical outcomes:

- `PASS` — the Skill has sufficient evidence and reaches the expected conclusion/action.
- `FAIL` — the Skill misses a required condition, produces the wrong conclusion, or violates its output/safety contract.
- `INSUFFICIENT_EVIDENCE` — required evidence is missing or below the rule's evidence threshold; the Skill must not manufacture a conclusion.
- `FALSE_POSITIVE` — the apparent issue exists superficially but an exclusion/context condition should prevent the finding.

## Fixture contract

Each fixture should contain:

```yaml
id:
skill:
class: PASS | FAIL | INSUFFICIENT_EVIDENCE | FALSE_POSITIVE
context: {}
expected:
  status:
  matched_rules: []
  excluded_rules: []
  findings: []
  priority:
  confidence:
  approval_required:
```

## Evaluation principles

1. Evidence before conclusion.
2. A rule match is not automatically a high-priority action.
3. `INSUFFICIENT_EVIDENCE` is a valid and expected result.
4. False-positive resistance is measured explicitly.
5. Mutation-capable recommendations must preserve human approval.
6. Tests should evaluate deterministic contracts first; model wording is secondary.

## Account-audit benchmark

`account-audit` is the end-to-end reference benchmark. It should verify:

```text
fixture
  -> skill registry
  -> dependency resolution
  -> knowledge/rule selection
  -> rule engine
  -> finding classification
  -> priority/confidence
  -> output contract
  -> safety/approval
```

## Benchmark metrics

- Rule precision
- Rule recall
- False-positive rate
- Evidence-gating accuracy
- Priority accuracy
- Confidence calibration
- Approval-safety compliance
- Output-schema compliance
- End-to-end pass rate

## Release gate

A Skill should not be considered production-ready merely because its prompt is complete. It must have representative fixtures, pass validation, and demonstrate acceptable false-positive and evidence-gating behavior.
