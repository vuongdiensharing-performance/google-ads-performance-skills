# Gate 2C.1A — Boundary Contract Validator

## Purpose

Gate 2C.1A is the schema-enforcement layer for Rule Execution State Machine contracts. It prevents an AI agent or a human maintainer from changing the meaning of A–F states through prose, implicit defaults, or model reasoning.

The canonical execution path is:

```text
Evidence
  ↓
Applicability
  ↓
Boundary State A–F
  ↓
Rule Decision
  ↓
Finding
```

## Source-of-truth policy

- Rule-local `boundary_contract` is authoritative for the Rule's declared boundary behavior.
- `rules/registry.yaml` is a machine-readable index and cross-check only.
- `knowledge_dependencies` remains Rule-local source of truth.
- Knowledge paths are never inferred from category, filename, folder structure, related skills, or semantic similarity.

## Canonical states

| State | ID | Decision | Finding |
|---|---|---|---:|
| A | `APPLICABLE_VALID` | `PASS` | false |
| B | `APPLICABLE_TRIGGERED` | `FAIL` | true |
| C | `APPLICABLE_MISSING_EVIDENCE` | `INSUFFICIENT_EVIDENCE` | false |
| D | `NOT_APPLICABLE` | `NOT_APPLICABLE` | false |
| E | `CONFLICTING_EVIDENCE` | Rule-local `conflict_policy` | false |
| F | `EXPLICIT_EXCLUSION` | `SUPPRESSED` | false |

Canonical precedence is fixed as:

```yaml
- NOT_APPLICABLE
- APPLICABLE_MISSING_EVIDENCE
- CONFLICTING_EVIDENCE
- EXPLICIT_EXCLUSION
- APPLICABLE_TRIGGERED
- APPLICABLE_VALID
```

## Rule-local contract requirements

Every Rule in the Gate 2C benchmark set must declare:

```yaml
boundary_contract:
  version: "1.0.0"
  applicable_when: [...]
  evidence_required: [...]
  states:
    A: {state: APPLICABLE_VALID, decision: PASS, finding_generated: false}
    B: {state: APPLICABLE_TRIGGERED, decision: FAIL, finding_generated: true}
    C: {state: APPLICABLE_MISSING_EVIDENCE, decision: INSUFFICIENT_EVIDENCE, finding_generated: false}
    D: {state: NOT_APPLICABLE, decision: NOT_APPLICABLE, finding_generated: false}
    E: {state: CONFLICTING_EVIDENCE, decision: POLICY_DEFINED, finding_generated: false}
    F: {state: EXPLICIT_EXCLUSION, decision: SUPPRESSED, finding_generated: false}
  conflict_policy:
    enabled: true
    when: {...}
    resolution:
      state: CONFLICTING_EVIDENCE
      decision: FAIL
      inference_used: false
```

`boundary_contract.evidence_required` must exactly mirror the Rule's legacy `evidence_required` field. The explicit state mapping must match the canonical schema; drift is a validation failure.

## Validator responsibilities

`python scripts/validate_boundary_contract.py` performs four classes of checks:

1. **Canonical schema validity** — the JSON Schema itself must be valid Draft 2020-12 and contain the canonical A–F metadata.
2. **Rule-local state validity** — every A–F mapping is explicit and matches the canonical state, decision, and finding semantics.
3. **Conflict-policy safety** — state E must be resolved only by the Rule-local policy and must declare `inference_used: false`.
4. **Provenance cross-check** — Rule path and `knowledge_dependencies` must match `rules/registry.yaml` exactly.

## Gate 2C.1 acceptance criteria

Gate 2C.1A passes only when:

- the canonical JSON Schema validates;
- all six benchmark Rules validate;
- all A–F mappings are explicit;
- no Rule-local decision/finding mapping drifts from canonical semantics;
- conflict policies cannot introduce inference;
- registry provenance remains an exact cross-check.

After 2C.1A passes, the next validation layer is the 36-fixture boundary matrix, followed by repeated deterministic execution in Gate 2C.2.
