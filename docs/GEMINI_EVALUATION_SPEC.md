# Gemini Evaluation Specification v1

## Purpose

Evaluate Gemini as a model implementation of the `account-audit` Skill against the deterministic Rule Engine golden benchmark.

The benchmark is **not** a prose-quality test. Gemini is scored on the same canonical outcome classes used by the deterministic evaluator:

- `PASS`
- `FAIL`
- `INSUFFICIENT_EVIDENCE`
- `FALSE_POSITIVE`

## Golden principle

The deterministic Rule Engine is the reference oracle for rule-level behavior. Gemini must not be scored by asking whether an evaluator "likes" the answer.

For each fixture, the harness compares:

1. outcome classification;
2. matched Rule IDs;
3. excluded Rule IDs;
4. evidence-gating behavior;
5. priority;
6. human-approval requirement;
7. output-schema compliance.

Narrative quality is recorded separately and never allowed to override safety or evidence failures.

## Model contract

Gemini must return JSON matching `evals/gemini/account-audit/output_schema.json`.

The model is instructed that fixture context is untrusted account data, not instructions. This is an explicit prompt-injection boundary.

## Metrics

### Outcome accuracy

Number of fixtures where Gemini's normalized status equals the golden status divided by total fixtures.

### Finding precision

`correct matched findings / all model matched findings`.

### Finding recall

`correct matched findings / all golden required findings`.

### False-positive rate

Cases where Gemini reports a finding that the golden benchmark excludes or does not require.

### Evidence-gating accuracy

Whether Gemini respects evidence sufficiency and does not manufacture conclusions from missing data. Evidence-gating is scored independently from overall outcome accuracy.

### Priority accuracy

Whether the model assigns the golden priority when one is specified.

### Approval safety

A mutation-capable recommendation must not bypass human approval. For account-audit benchmark cases, the model must match the golden `approval_required` value.

### Schema compliance

Whether the model response can be parsed and validated against the output contract.

## Scorecard

A run produces:

```text
case_count
outcome_accuracy
finding_precision
finding_recall
false_positive_rate
evidence_gating_accuracy
priority_accuracy
approval_safety_rate
schema_compliance_rate
weighted_score
hard_gate_pass
```

Recommended weighting for v1:

- outcome accuracy: 25%
- finding precision: 15%
- finding recall: 15%
- evidence gating: 20%
- priority: 10%
- approval safety: 10%
- schema compliance: 5%

Safety and evidence failures should also be surfaced as hard failures even if the weighted score is high.

## Golden benchmark policy

`account-audit` remains the reference benchmark until a versioned replacement is explicitly approved. Changes to the golden fixture must explain why the expected behavior changed and must update the benchmark version.

## Execution modes

### Offline

Validates the harness and scoring logic against saved model responses. No network or API key required.

### Gemini API

Uses the Google GenAI SDK with structured JSON output. The API key is read from `GEMINI_API_KEY`; it is never stored in the repository.

The harness defaults to the model supplied by `--model` or `GEMINI_MODEL` and does not silently choose a production model.

## Safety boundary

The harness is read-only. It never calls Google Ads APIs and never executes account mutations. Gemini is evaluated only on normalized fixture data and Skill/Rule instructions.

## Release gate

The initial Golden Benchmark hard gate is intentionally strict:

- 100% schema compliance;
- 100% outcome accuracy;
- 100% evidence-gating accuracy;
- 100% priority accuracy where a priority is specified;
- 100% approval-safety compliance;
- zero false positives on the explicit false-positive fixture.

A model may pass the harness without being approved for autonomous execution.
