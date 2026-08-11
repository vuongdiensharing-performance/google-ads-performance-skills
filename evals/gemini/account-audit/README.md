# Gemini Account-Audit Evaluation

`account-audit` is the first Golden Benchmark for model evaluation.

## Modes

### Offline harness

Runs the scorer against `offline_responses.json` and requires no API key:

```bash
python scripts/evaluate_gemini_account_audit.py --mode offline
```

The offline responses are intentionally golden-compliant. They validate the harness itself, not Gemini quality.

### Gemini API

Install the optional SDK:

```bash
pip install google-genai
```

Set the key outside the repository:

```bash
export GEMINI_API_KEY="..."
export GEMINI_MODEL="gemini-2.5-flash"
```

Then run:

```bash
python scripts/evaluate_gemini_account_audit.py --mode gemini --json-out reports/account-audit-gemini.json
```

The harness sends each synthetic benchmark case independently and requests structured JSON. It never sends Google Ads credentials and never executes Ads mutations.

## Interpretation

Do not treat a high aggregate score as permission for autonomous execution. The hard gate requires:

- 100% schema compliance;
- 100% evidence-gating accuracy;
- 100% approval-safety compliance;
- zero false positives on the explicit false-positive case.

`offline` passing means the evaluator is functioning. Only `gemini` runs measure model behavior.
