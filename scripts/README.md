# Scripts

## Rule Engine

`rule_engine.py` is the deterministic Rule Engine for Rule Spec v1.

It:

- loads YAML rules recursively;
- evaluates `all`, `any`, `not`, equality, membership, and numeric comparisons;
- checks declared evidence before evaluating a rule;
- returns `matched`, `insufficient_evidence`, `excluded`, and `not_matched` states;
- preserves severity, confidence, impact, recommendations, and related Skills;
- enforces human approval for mutating actions (`pause`, `increase`, `decrease`, `change`).

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
