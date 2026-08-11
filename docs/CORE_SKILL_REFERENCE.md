# Core Skill Reference Architecture v1.1

`account-audit` is the reference architecture for all Core Skills. It demonstrates how a Skill consumes Knowledge, evaluates Rules, classifies findings, and produces a deterministic output contract.

## Runtime pattern

```text
User request
   ↓
Skill selection
   ↓
Validate inputs / preconditions
   ↓
Load declared Knowledge
   ↓
Normalize context
   ↓
Run relevant Rules
   ↓
Classify
   ├─ observation
   ├─ inference
   ├─ recommendation
   └─ evidence gap
   ↓
Prioritize
   ├─ impact
   ├─ urgency
   ├─ confidence
   └─ business constraints
   ↓
Output Contract
   ↓
Measurement / next step
```

## Four-layer contract

### 1. Knowledge
Provides principles, definitions, frameworks, and methodology. It does not directly produce account actions.

### 2. Rules
Provide bounded, testable conditions. They can return `matched`, `not_matched`, `excluded`, or `insufficient_evidence`.

### 3. Skill
Orchestrates the workflow and turns Rule/Knowledge outputs into a user-facing diagnosis or plan.

### 4. Output Contract
Makes the result consumable by a human, another Skill, or a future agent runtime.

## Reference finding

```yaml
finding:
  skill: search-term-analysis
  rule_id: ST-WASTE-001
  status: matched
  observation: "Direct evidence from the supplied query report"
  inference: "The query may be economically weak"
  recommendation: "Review exclusion or bid/structure treatment"
  priority: P1
  impact: high
  confidence: medium
  evidence:
    - search_term_report
  approval_required: true
```

## Priority model

Priority is assigned by the Skill, not by Rule severity alone:

`Priority = f(impact, evidence, confidence, urgency, business constraints, reversibility)`

This prevents every `high` severity Rule from becoming an automatic P0.

## Safety model

```text
READ → ANALYZE → RECOMMEND → PREPARE → APPROVAL → EXECUTE
```

Core Skills stop at `RECOMMEND` or `PREPARE` by default. Execution belongs to a separately authorized integration layer.

## Reference implementation

See `skills/account-audit/SKILL.md` for the canonical orchestration pattern.
