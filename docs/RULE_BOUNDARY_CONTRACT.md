# Rule Boundary Contract v1.0.0

## Purpose

The Boundary Contract makes Rule Engine state transitions explicit, deterministic, machine-readable, and auditable. It governs the six boundary states returned by a Rule evaluation.

## Canonical state machine

| State | ID | Decision | Finding |
|---|---|---|---|
| A | `APPLICABLE_VALID` | `PASS` | false |
| B | `APPLICABLE_TRIGGERED` | `FAIL` | true |
| C | `APPLICABLE_MISSING_EVIDENCE` | `INSUFFICIENT_EVIDENCE` | false |
| D | `NOT_APPLICABLE` | `NOT_APPLICABLE` | false |
| E | `CONFLICTING_EVIDENCE` | `POLICY_DEFINED` | false |
| F | `EXPLICIT_EXCLUSION` | `SUPPRESSED` | false |

State `E` is resolved only through the Rule-local `conflict_policy`. The Rule Engine must never infer a conflict resolution from model reasoning.

## Resolution precedence

The canonical precedence is:

```yaml
resolution_precedence:
  - NOT_APPLICABLE
  - APPLICABLE_MISSING_EVIDENCE
  - CONFLICTING_EVIDENCE
  - EXPLICIT_EXCLUSION
  - APPLICABLE_TRIGGERED
  - APPLICABLE_VALID
```

The precedence is contract data, not an implementation-specific ordering. Validators must reject a different order.

## Rule-local contract

Every Rule participating in Gate 2C must declare:

- `boundary_contract.applicable_when` — explicit applicability scope;
- `boundary_contract.evidence_required` — evidence needed to distinguish valid/triggered states;
- `boundary_contract.states` — explicit A–F mappings;
- `boundary_contract.conflict_policy` — policy for state E when conflicts are possible.

The existing Rule fields `when`, `exclude_when`, and `evidence_required` remain authoritative for legacy Rule semantics. The Boundary Contract does not replace them; it makes the boundary transitions explicit around them.

## Evidence and inference invariant

For every boundary state A–F:

```text
inference_used == false
```

The LLM may classify or serialize evidence already supplied to it, but it must not invent evidence, missing facts, or policy exceptions in order to reach a state.

## Provenance invariant

`knowledge_dependencies` remains Rule-local source of truth. `rules/registry.yaml` remains an index and cross-check only. Boundary validation must not infer Knowledge dependencies from category, path, filename, related skills, or semantic similarity.

## Machine-readable output

A valid runtime result must contain at least:

```yaml
rule_id: STR-FRAG-001
boundary_state: EXPLICIT_EXCLUSION
decision: SUPPRESSED
inference_used: false
evidence_sufficient: true
audit_trail:
  evidence: "separation_reason: distinct_location_budgets"
  rule: "rules/structure/fragmentation-risk.yaml"
  knowledge:
    - "knowledge/structure/account-structure.md"
```

The validator compares the machine-readable contract, not a free-form `PASS`/`FAIL` string.
