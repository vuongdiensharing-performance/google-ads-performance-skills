# Scripts

## Rule Engine

`rule_engine.py` is the deterministic Rule Engine for Rule Spec v1.

It:

- loads YAML rules recursively;
- evaluates `all`, `any`, `not`, equality, membership, numeric comparisons, and declarative expressions such as `field.path == value`;
- checks declared evidence before evaluating a rule;
- returns `matched`, `insufficient_evidence`, `excluded`, and `not_matched` states;
- preserves severity, confidence, impact, recommendations, and related Skills;
- enforces human approval for mutating actions (`pause`, `increase`, `decrease`, `change`).

### Rule validation

`validate_rules.py` checks Rule Spec v1 required fields, severity/confidence values, supported action types, and mutation approval requirements.

```bash
python scripts/validate_rules.py --rules rules
```

### Install

```bash
pip install -r scripts/requirements.txt
```

### Run

```bash
python scripts/rule_engine.py --rules rules --input examples/rule-engine/context.json
```

### Smoke test

```bash
python scripts/test_rule_engine.py
```

The engine deliberately does not assign business priority. Consuming Skills must prioritize findings using impact, evidence, dependencies, and business context.
