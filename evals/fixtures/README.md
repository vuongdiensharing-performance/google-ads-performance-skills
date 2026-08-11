# Skill Evaluation Fixtures

Fixtures are grouped by Skill and use four canonical classes:

- `PASS`
- `FAIL`
- `INSUFFICIENT_EVIDENCE`
- `FALSE_POSITIVE`

Directory convention:

```text
evals/fixtures/<skill>/
├── pass.yaml
├── fail.yaml
├── insufficient-evidence.yaml
└── false-positive.yaml
```

Fixtures are intentionally deterministic. They validate Skill contracts and Rule Engine behavior before model-generated language is evaluated.
